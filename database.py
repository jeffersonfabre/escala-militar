import sqlite3
from passlib.hash import bcrypt

DB = "escala.db"

def conectar():
    return sqlite3.connect(DB)

def criar_tabelas():
    conn = conectar()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        senha TEXT,
        perfil TEXT
    )""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS militares (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        posto TEXT,
        dispensado INTEGER DEFAULT 0
    )""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS historico (
        mes INTEGER,
        ano INTEGER,
        data TEXT,
        tipo TEXT,
        posto TEXT,
        militar TEXT
    )""")

    conn.commit()
    conn.close()

def criar_admin():
    conn = conectar()
    c = conn.cursor()
    c.execute("SELECT * FROM usuarios")
    if not c.fetchone():
        c.execute(
            "INSERT INTO usuarios VALUES (NULL,?,?,?)",
            ("admin", bcrypt.hash("admin123"), "ADMIN")
        )
    conn.commit()
    conn.close()

def autenticar(user, senha):
    conn = conectar()
    c = conn.cursor()
    c.execute("SELECT senha, perfil FROM usuarios WHERE username=?", (user,))
    r = c.fetchone()
    conn.close()
    if r and bcrypt.verify(senha, r[0]):
        return r[1]
    return None

def listar_militares():
    conn = conectar()
    c = conn.cursor()
    c.execute("SELECT * FROM militares")
    d = c.fetchall()
    conn.close()
    return d
