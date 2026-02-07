import streamlit as st
import pandas as pd
import calendar, datetime, holidays
import plotly.express as px
from database import *

st.set_page_config(page_title="Escala Militar - Sistema Final", layout="wide")

criar_tabelas()
criar_admin()

# ---------- LOGIN ----------
if "perfil" not in st.session_state:
    st.title("🔐 Login")
    u = st.text_input("Usuário")
    s = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        perfil = autenticar(u, s)
        if perfil:
            st.session_state["perfil"] = perfil
            st.rerun()
        else:
            st.error("Login inválido")
    st.stop()

# ---------- SISTEMA ----------
st.title("🎖 Sistema Profissional de Escala Militar")
st.caption(f"Perfil: {st.session_state['perfil']}")

tabs = st.tabs(["📋 Militares", "🗓 Escala", "📚 Histórico", "📊 Estatísticas"])

# ---------- TAB 1 ----------
with tabs[0]:
    if st.session_state["perfil"] == "ADMIN":
        nome = st.text_input("Nome")
        posto = st.selectbox("Posto", ["3S","2S","1S"])
        if st.button("Cadastrar"):
            conn = conectar()
            conn.execute("INSERT INTO militares VALUES (NULL,?,?,0)", (nome, posto))
            conn.commit()
            conn.close()
            st.rerun()

    df = pd.DataFrame(listar_militares(), columns=["ID","Nome","Posto","Disp"])
    df["Status"] = df["Disp"].apply(lambda x: "DISPENSADO" if x else "ATIVO")
    st.dataframe(df[["ID","Nome","Posto","Status"]], use_container_width=True)

# ---------- TAB 2 ----------
with tabs[1]:
    mes = st.selectbox("Mês", range(1,13), format_func=lambda x: calendar.month_name[x])
    ano = st.number_input("Ano", 2024, 2035, datetime.date.today().year)

    if st.button("Gerar Escala"):
        ativos = [m for m in listar_militares() if m[3] == 0]
        feriados = holidays.Brazil(years=ano)

        cont = {m[1]: 0 for m in ativos}
        ultimo = None
        escala = []

        for d in range(1, calendar.monthrange(ano, mes)[1]+1):
            data = datetime.date(ano, mes, d)
            tipo = "VERMELHA" if data.weekday()>=5 or data in feriados else "PRETA"
            ordenados = sorted(cont, key=cont.get)
            esc = next(x for x in ordenados if x != ultimo)
            cont[esc]+=1
            ultimo=esc
            escala.append([data.strftime("%d/%m/%Y"), tipo, esc])

        df = pd.DataFrame(escala, columns=["Data","Tipo","Militar"])
        st.dataframe(df, use_container_width=True)

# ---------- TAB 3 ----------
with tabs[2]:
    st.info("Histórico pronto para expansão anual")

# ---------- TAB 4 ----------
with tabs[3]:
    s = pd.Series(cont).reset_index()
    s.columns=["Militar","Qtd"]
    st.plotly_chart(px.bar(s, x="Militar", y="Qtd"), use_container_width=True)
