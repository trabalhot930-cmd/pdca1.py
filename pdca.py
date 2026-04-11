import streamlit as st

# Configuração da página para usar o máximo de espaço
st.set_page_config(layout="wide", page_title="PDCA Controle de Acesso")

st.title("🔄 Matriz PDCA de Controle de Acesso")
st.markdown("---")

# Definição das 7 Colunas e 4 Linhas
colunas = [
    "1. Contexto (P)", "2. Liderança (P)", "3. Planejamento (P)", 
    "4. Suporte (D)", "5. Operação (D)", "6. Avaliação (C)", "7. Melhoria (A)"
]

linhas = [
    "🎯 Objetivo Estratégico",
    "⚙️ Ação Técnica (TI/OT)",
    "📊 Indicador (KPI)",
    "🚩 Status/Responsável"
]

# Conteúdos sugeridos para preencher a matriz (exemplo focado na Usina)
# Você pode transformar isso em inputs de texto depois
conteudo_matriz = {
    (0,0): "Definir perímetro de Belo Monte", (0,1): "Política de Acesso aprovada", (0,2): "Análise de Riscos de Invasão",
    (0,3): "Recursos e Infra de Redes", (0,4): "Execução do Controle Físico", (0,5): "Auditoria de Logs Mensal", (0,6): "Correção de vulnerabilidades",
    # ... adicionei aqui uma lógica para preencher visualmente
}

# Criação da estrutura em Streamlit
cols = st.columns(7)

for i, nome_col in enumerate(colunas):
    with cols[i]:
        # Cabeçalho da Coluna
        color_header = "#2E4053"
        st.markdown(f"""
            <div style="background-color: {color_header}; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                <h5 style="color: white; text-align: center; margin: 0; font-size: 14px;">{nome_col}</h5>
            </div>
        """, unsafe_allow_html=True)
        
        # Loop para criar as 4 linhas em cada coluna
        for j, nome_linha in enumerate(linhas):
            # Cores alternadas para as linhas para facilitar a leitura
            bg_color = "#F8F9F9" if j % 2 == 0 else "#E5E8E8"
            
            st.markdown(f"""
                <div style="background-color: {bg_color}; padding: 10px; border-radius: 5px; border-left: 5px solid #5D6D7E; margin-bottom: 8px; min-height: 120px;">
                    <strong style="font-size: 11px; color: #1B2631;">{nome_linha}</strong>
                    <p style="font-size: 13px; color: #515A5A; margin-top: 5px;">
                        {conteudo_matriz.get((j,i), "Definir detalhes para esta etapa...")}
                    </p>
                </div>
            """, unsafe_allow_html=True)

st.markdown("---")
st.info("💡 Este quadro integra os requisitos da EXIN (ISO 27001) com a operação real dos Meios Eletrônicos.")
