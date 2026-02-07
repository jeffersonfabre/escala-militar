import sqlite3

DB = "escala.db"


def conectar():
    return sqlite3.connect(DB)


def criar_tabelas():
    conn = conectar()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS militares (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            posto TEXT,
            dispensado INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


def listar_militares():
    conn = conectar()
    c = conn.cursor()
    c.execute("SELECT * FROM militares")
    dados = c.fetchall()
    conn.close()
    return dados


def adicionar_militar(nome, posto):
    conn = conectar()
    c = conn.cursor()
    c.execute(
        "INSERT INTO militares VALUES (NULL,?,?,0)",
        (nome, posto)
    )
    conn.commit()
    conn.close()
