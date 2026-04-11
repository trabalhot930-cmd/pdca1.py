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

# CSS
st.markdown("""
<style>
textarea {
    height: 120px !important;
}
</style>
""", unsafe_allow_html=True)

cols = st.columns(len(colunas))

# Armazenar dados
dados = {}

for i, col_info in enumerate(colunas):
    with cols[i]:
        st.markdown(f"""
            <div style="
                background-color: {col_info['cor']};
                padding: 10px;
                border-radius: 10px 10px 0 0;
                text-align: center;
                color: white;
                font-weight: bold;
                font-size: 14px;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;">
                {col_info['nome']}
            </div>
        """, unsafe_allow_html=True)

        for j, titulo_linha in enumerate(linhas):
            key_id = f"cell_{i}_{j}"

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

            valor = st.text_area(
                label="",
                key=key_id,
                placeholder="Digite aqui...",
                label_visibility="collapsed"
            )

            dados[(i, j)] = valor

st.markdown("---")

# BOTÃO DE IMPRESSÃO
if st.button("🖨️ Imprimir PDCA"):
    
    html = """
    <html>
    <head>
    <style>
        body { font-family: Arial; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ccc; padding: 8px; vertical-align: top; }
        th { color: white; }
    </style>
    </head>
    <body>
    <h2>PDCA - Controle de Acesso</h2>
    <table>
    """

    # Cabeçalho
    html += "<tr>"
    for col in colunas:
        html += f"<th style='background:{col['cor']}'>{col['nome']}</th>"
    html += "</tr>"

    # Linhas
    for j, linha_nome in enumerate(linhas):
        html += "<tr>"
        for i in range(len(colunas)):
            conteudo = dados[(i, j)].replace("\n", "<br>")
            html += f"<td><b>{linha_nome}</b><br>{conteudo}</td>"
        html += "</tr>"

    html += """
    </table>

    <script>
        window.onload = function() {
            window.print();
        }
    </script>

    </body>
    </html>
    """

    st.components.v1.html(html, height=800)

st.success("✅ P = Planejamento | D = Execução | C = Auditoria | A = Melhoria Contínua")

st.success(
    "✅ P = Planejamento | D = Execução | C = Auditoria | A = Melhoria Contínua"
)
