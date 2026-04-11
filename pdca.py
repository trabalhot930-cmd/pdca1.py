import streamlit as st

# Configuração para usar a tela toda
st.set_page_config(layout="wide", page_title="PDCA Controle de Acesso")

st.title("🔄 PDCA de Controle de Acesso - Gestão de Segurança")
st.markdown("---")

# Definição das Colunas (7) e Linhas (4)
# Agrupadas por cores conforme seu pedido
colunas = [
    {"nome": "1. Contexto (P)", "cor": "#1E88E5"},  # Azul
    {"nome": "2. Liderança (P)", "cor": "#1E88E5"}, # Azul
    {"nome": "3. Planejamento (P)", "cor": "#1E88E5"}, # Azul
    {"nome": "4. Suporte (D)", "cor": "#E53935"},   # Vermelho
    {"nome": "5. Operação (D)", "cor": "#E53935"},  # Vermelho
    {"nome": "6. Avaliação (C)", "cor": "#43A047"}, # Verde
    {"nome": "7. Melhoria (A)", "cor": "#FB8C00"}   # Laranja/Ajuste
]

linhas = [
    "🎯 Objetivo Estratégico",
    "⚙️ Ação Técnica (TI/OT)",
    "📊 Indicador (KPI)",
    "🚩 Evidência / Status"
]

# Criando o layout
cols = st.columns(7)

for i, col_info in enumerate(colunas):
    with cols[i]:
        # Cabeçalho da Coluna com a cor específica
        st.markdown(f"""
            <div style="background-color: {col_info['cor']}; padding: 15px; border-radius: 10px 10px 0px 0px; border: 1px solid #212121;">
                <h3 style="color: white; text-align: center; margin: 0; font-size: 18px; font-weight: bold;">
                    {col_info['nome']}
                </h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Criando as 4 linhas para cada coluna
        for j, titulo_linha in enumerate(linhas):
            # ID único para cada campo de texto
            key_id = f"cell_{i}_{j}"
            
            # Container para a célula
            st.markdown(f"""
                <div style="background-color: #f9f9f9; padding: 5px; border-left: 4px solid {col_info['cor']}; border-right: 1px solid #ddd; border-bottom: 1px solid #ddd;">
                    <label style="font-size: 11px; font-weight: bold; color: {col_info['cor']};">{titulo_linha}</label>
                </div>
            """, unsafe_allow_html=True)
            
            # Campo para você digitar as informações reais da Usina
            st.text_area(label=titulo_linha, label_visibility="collapsed", height=100, key=key_id, placeholder="Digite aqui...")

st.markdown("---")
st.success("✅ Dica: O P (Plan) foca na estratégia, o D (Do) na operação técnica, o C (Check) na auditoria via Power BI e o A (Act) na melhoria contínua.")
