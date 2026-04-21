import sqlite3

# =========================
# 🔌 Conexão com banco
# =========================
def conectar():
    return sqlite3.connect("grc.db", check_same_thread=False)


# =========================
# 🏗️ Criar tabelas
# =========================
def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS riscos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ativo TEXT,
        ameaca TEXT,
        vulnerabilidade TEXT,
        localidade TEXT,
        probabilidade TEXT,
        impacto TEXT,
        score REAL,
        nivel TEXT,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


# =========================
# ➕ Inserir risco
# =========================
def inserir_risco(ativo, ameaca, vulnerabilidade, localidade, probabilidade, impacto, score, nivel):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO riscos (ativo, ameaca, vulnerabilidade, localidade, probabilidade, impacto, score, nivel)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (ativo, ameaca, vulnerabilidade, localidade, probabilidade, impacto, score, nivel))

    conn.commit()
    conn.close()


# =========================
# 📊 Listar riscos
# =========================
def listar_riscos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM riscos ORDER BY id DESC")
    dados = cursor.fetchall()

    conn.close()
    return dados


# =========================
# ❌ Deletar risco
# =========================
def deletar_risco(risco_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM riscos WHERE id = ?", (risco_id,))

    conn.commit()
    conn.close()
