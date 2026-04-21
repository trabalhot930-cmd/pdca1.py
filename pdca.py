import streamlit as st
import pandas as pd
from database import conectar, criar_tabelas
from risk_engine import calcular_risco

st.set_page_config(layout="wide", page_title="GRC - Segurança da Informação")

criar_tabelas()

st.title("🛡️ Sistema GRC - Governança, Risco e Compliance")

menu = st.sidebar.selectbox("Menu", ["Dashboard", "Riscos", "PDCA"])

# =========================
# 📊 DASHBOARD
# =========================
if menu == "Dashboard":
    st.header("📊 Visão Geral")

    conn = conectar()
    df = pd.read_sql("SELECT * FROM riscos", conn)

    if not df.empty:
        col1, col2 = st.columns(2)

        col1.metric("Total de Riscos", len(df))
        col2.metric("Críticos", len(df[df["nivel"] == "Crítico"]))

        st.subheader("Distribuição de Risco")
        st.bar_chart(df["nivel"].value_counts())
    else:
        st.info("Nenhum risco cadastrado.")

# =========================
# ⚠️ RISCOS
# =========================
elif menu == "Riscos":
    st.header("🔎 Cadastro de Riscos")

    with st.form("form_risco"):
        col1, col2, col3 = st.columns(3)

        ativo = col1.text_input("Ativo")
        ameaca = col2.text_input("Ameaça")
        vulnerabilidade = col3.text_input("Vulnerabilidade")

        col4, col5, col6 = st.columns(3)

        localidade = col4.selectbox("Localidade", ["Matriz", "Filial", "Cloud", "Externo"])
        prob = col5.selectbox("Probabilidade", ["Baixa", "Média", "Alta"])
        imp = col6.selectbox("Impacto", ["Baixo", "Médio", "Alto"])

        submit = st.form_submit_button("Salvar Risco")

    if submit:
        score, nivel = calcular_risco(prob, imp, localidade)

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO riscos (ativo, ameaca, vulnerabilidade, localidade, probabilidade, impacto, score, nivel)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (ativo, ameaca, vulnerabilidade, localidade, prob, imp, score, nivel))

        conn.commit()
        conn.close()

        st.success(f"Risco cadastrado | Nível: {nivel}")

    # Exibir tabela
    conn = conectar()
    df = pd.read_sql("SELECT * FROM riscos", conn)

    if not df.empty:
        st.subheader("📋 Riscos Registrados")

        def cor(val):
            cores = {
                "Baixo": "background-color: green; color:white",
                "Médio": "background-color: orange",
                "Alto": "background-color: red; color:white",
                "Crítico": "background-color: darkred; color:white"
            }
            return cores.get(val, "")

        st.dataframe(df.style.applymap(cor, subset=["nivel"]))

# =========================
# 🔄 PDCA AUTOMÁTICO
# =========================
elif menu == "PDCA":
    st.header("🔄 PDCA Automatizado")

    conn = conectar()
    df = pd.read_sql("SELECT * FROM riscos", conn)

    if df.empty:
        st.warning("Cadastre riscos primeiro.")
    else:
        riscos_prioritarios = df[df["nivel"].isin(["Alto", "Crítico"])]

        st.subheader("🚨 Ações Prioritárias")

        for _, r in riscos_prioritarios.iterrows():
            st.error(f"""
            Ativo: {r['ativo']}
            Ameaça: {r['ameaca']}
            Nível: {r['nivel']}
            
            👉 Ação:
            - Implementar controle de acesso
            - Revisar políticas
            - Monitoramento contínuo
            """)

        st.subheader("📘 PDCA Estruturado")

        st.markdown("### 🟦 Planejar (Plan)")
        st.write("Definir controles para riscos críticos")

        st.markdown("### 🟥 Executar (Do)")
        st.write("Aplicar controles de segurança")

        st.markdown("### 🟩 Verificar (Check)")
        st.write("Auditoria e monitoramento")

        st.markdown("### 🟧 Agir (Act)")
        st.write("Melhoria contínua baseada nos riscos")
