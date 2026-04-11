import streamlit as st

# Configuração da página
st.set_page_config(layout="wide", page_title="PDCA Controle de Acesso")

st.title("🔄 PDCA de Controle de Acesso - Gestão de Segurança")
st.markdown("---")

# Colunas (PDCA)
colunas = [
    {"nome": "1. Contexto (P)", "cor": "#1E88E5"},
    {"nome": "2. Liderança (P)", "cor": "#1E88E5"},
    {"nome": "3. Planejamento (P)", "cor": "#1E88E5"},
    {"nome": "4. Suporte (D)", "cor": "#E53935"},
    {"nome": "5. Operação (D)", "cor": "#E53935"},
    {"nome": "6. Avaliação (C)", "cor": "#43A047"},
    {"nome": "7. Melhoria (A)", "cor": "#FB8C00"}
]

linhas = [
    "🎯 Objetivo Estratégico",
    "⚙️ Ação Técnica (TI/OT)",
    "📊 Indicador (KPI)",
    "🚩 Evidência / Status"
]

# CSS para padronizar altura
st.markdown("""
<style>
textarea {
    height: 120px !important;
}
</style>
""", unsafe_allow_html=True)

cols = st.columns(len(colunas))

for i, col_info in enumerate(colunas):
    with cols[i]:
        # Cabeçalho
        st.markdown(f"""
            <div style="
                background-color: {col_info['cor']};
                padding: 12px;
                border-radius: 10px 10px 0 0;
                text-align: center;
                color: white;
                font-weight: bold;
                font-size: 16px;">
                {col_info['nome']}
            </div>
        """, unsafe_allow_html=True)

        # Linhas
        for j, titulo_linha in enumerate(linhas):
            key_id = f"cell_{i}_{j}"

            # Label
            st.markdown(f"""
                <div style="
                    background-color: #f4f4f4;
                    padding: 6px;
                    border-left: 5px solid {col_info['cor']};
                    font-size: 12px;
                    font-weight: bold;">
                    {titulo_linha}
                </div>
            """, unsafe_allow_html=True)

            # Campo
            st.text_area(
                label="",
                key=key_id,
                placeholder="Digite aqui...",
                label_visibility="collapsed"
            )

st.markdown("---")

st.success(
    "✅ P = Planejamento | D = Execução | C = Auditoria | A = Melhoria Contínua"
)
