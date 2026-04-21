import streamlit as st
import pandas as pd

# -------------------------------
# CONFIGURAÇÃO DA PÁGINA
# -------------------------------
st.set_page_config(layout="wide", page_title="PDCA + Análise de Risco", page_icon="🛡️")

st.title("🛡️ PDCA de Controle de Acesso + Análise de Risco")
st.markdown("---")

# -------------------------------
# PARTE 1: ANÁLISE DE RISCO QUALITATIVA
# -------------------------------
with st.expander("📊 Matriz de Análise de Risco (Probabilidade x Impacto)", expanded=True):
    st.markdown("""
    **Critérios:**  
    - **Probabilidade:** Baixa | Média | Alta  
    - **Impacto:** Baixo | Médio | Alto  
    - **Nível do risco:**  
        - 🟢 Baixo (Baixa x Baixo, Baixa x Médio, Média x Baixo)  
        - 🟡 Médio (Baixa x Alto, Média x Médio, Alta x Baixo)  
        - 🔴 Alto (Média x Alto, Alta x Médio, Alta x Alto)
    """)

    # Dados iniciais (baseado no seu exemplo)
    dados_risco = pd.DataFrame({
        "Ativo": ["Cabos na sala de servidores", "Pen drive ou HD", "Servidor de internet", "Switch de borda (novo)"],
        "Ameaça": ["Rompimento", "Contaminação por vírus", "Invasão externa", "Desligamento acidental"],
        "Vulnerabilidade": ["Cabos fora de dutos", "Antivírus desatualizado", "Internet ligada direto na rede interna", "Sem trava física no rack"],
        "Probabilidade": ["Baixa", "Alta", "Média", "Média"],
        "Impacto": ["Alto", "Alto", "Alto", "Médio"],
    })

    # Função para calcular nível do risco
    def nivel_risco(prob, imp):
        prob = prob.lower()
        imp = imp.lower()
        if (prob == "baixa" and imp == "baixo") or (prob == "baixa" and imp == "médio") or (prob == "média" and imp == "baixo"):
            return "🟢 Baixo"
        elif (prob == "baixa" and imp == "alto") or (prob == "média" and imp == "médio") or (prob == "alta" and imp == "baixo"):
            return "🟡 Médio"
        else:
            return "🔴 Alto"

    # Aplicar cálculo
    dados_risco["Nível do risco"] = dados_risco.apply(lambda row: nivel_risco(row["Probabilidade"], row["Impacto"]), axis=1)

    # Editor interativo da tabela de risco
    edited_risco = st.data_editor(
        dados_risco,
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            "Probabilidade": st.column_config.SelectboxColumn(options=["Baixa", "Média", "Alta"]),
            "Impacto": st.column_config.SelectboxColumn(options=["Baixo", "Médio", "Alto"]),
            "Nível do risco": st.column_config.TextColumn(disabled=True),
        },
        hide_index=True,
    )

    # Recalcular risco após edição
    edited_risco["Nível do risco"] = edited_risco.apply(lambda row: nivel_risco(row["Probabilidade"], row["Impacto"]), axis=1)

    st.markdown("---")
    st.caption("✅ Edite a tabela acima. O nível do risco é atualizado automaticamente.")

st.markdown("---")

# -------------------------------
# PARTE 2: PDCA (como você já tinha)
# -------------------------------
st.subheader("🔄 PDCA de Controle de Acesso")

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

# CSS para altura dos textareas
st.markdown("""
<style>
    textarea {
        height: 100px !important;
    }
    [data-testid="stExpander"] summary {
        font-size: 1.2rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

cols = st.columns(len(colunas))
dados_pdca = {}

for i, col_info in enumerate(colunas):
    with cols[i]:
        st.markdown(f"""
            <div style="background-color: {col_info['cor']}; padding: 10px; border-radius: 10px 10px 0 0; text-align: center; color: white; font-weight: bold;">
                {col_info['nome']}
            </div>
        """, unsafe_allow_html=True)
        for j, titulo in enumerate(linhas):
            st.markdown(f"**{titulo}**")
            key_id = f"pdca_{i}_{j}"
            valor = st.text_area(
                label="",
                key=key_id,
                placeholder=f"Digite o {titulo.lower()}...",
                label_visibility="collapsed"
            )
            dados_pdca[(i, j)] = valor

# -------------------------------
# PARTE 3: IMPRESSÃO UNIFICADA
# -------------------------------
st.markdown("---")
col_btn1, col_btn2 = st.columns([1, 5])
with col_btn1:
    if st.button("🖨️ Imprimir PDCA + Análise de Risco", use_container_width=True):
        # Gerar HTML da análise de risco
        risco_html = edited_risco.to_html(index=False, escape=False)
        
        # Gerar HTML do PDCA
        pdca_html = "<table border='1' cellpadding='8' cellspacing='0' style='border-collapse: collapse; width: 100%;'>"
        # Cabeçalho
        pdca_html += "<tr>"
        for col in colunas:
            pdca_html += f"<th style='background:{col['cor']}; color:white'>{col['nome']}</th>"
        pdca_html += "</tr>"
        # Linhas
        for j, linha_nome in enumerate(linhas):
            pdca_html += "<tr>"
            for i in range(len(colunas)):
                conteudo = dados_pdca.get((i, j), "").replace("\n", "<br>")
                pdca_html += f"<td><b>{linha_nome}</b><br>{conteudo}</td>"
            pdca_html += "</tr>"
        pdca_html += "</table>"

        # HTML completo
        html_completo = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1, h2, h3 {{ color: #1E3A5F; }}
                table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
                th, td {{ border: 1px solid #aaa; padding: 8px; vertical-align: top; }}
                th {{ background-color: #f2f2f2; }}
                .risco-alto {{ background-color: #ffcccc; }}
                .risco-medio {{ background-color: #fff2cc; }}
                .risco-baixo {{ background-color: #ccffcc; }}
            </style>
        </head>
        <body>
            <h1>🛡️ Relatório de Segurança - PDCA + Análise de Risco</h1>
            <h2>📊 Matriz de Análise de Risco</h2>
            {risco_html}
            <h2>🔄 PDCA de Controle de Acesso</h2>
            {pdca_html}
            <script>window.onload = function() {{ window.print(); }}</script>
        </body>
        </html>
        """
        st.components.v1.html(html_completo, height=600)

with col_btn2:
    st.caption("✅ A análise de risco alimenta as ações do PDCA (especialmente Planejamento e Melhoria)")

# -------------------------------
# PARTE 4: MELHORIAS ADICIONAIS
# -------------------------------
with st.expander("💡 Sugestões de melhoria contínua (baseadas nos riscos)"):
    st.markdown("""
    - **Risco Alto (ex: Pen drive contaminado)** → Reforçar no PDCA:  
        - *Ação Técnica:* Implantar DLP (Data Loss Prevention) + Antivírus com atualização automática  
        - *Indicador:* % de estações com antivírus atualizado (>98%)  
    - **Risco Alto (invasão externa)** → Adicionar no Planejamento:  
        - Segmentação de rede (DMZ)  
        - Firewall de última geração + IDS/IPS  
    - **Risco Médio (cabos rompidos)** → Na Operação:  
        - Passar cabos em dutos sinalizados  
        - Backup de switch/core
    """)

st.success("🔁 PDCA + Análise de Risco integrados. Toda edição na tabela de risco pode ser usada como entrada para o ciclo de melhoria.")
