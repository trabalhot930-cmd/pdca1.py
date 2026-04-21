import streamlit as st
import pandas as pd
from datetime import datetime

# -------------------------------
# CONFIGURAÇÃO DA PÁGINA
# -------------------------------
st.set_page_config(layout="wide", page_title="PDCA + Análise de Risco", page_icon="🛡️")

st.title("🛡️ PDCA de Controle de Acesso + Análise de Risco")
st.markdown("---")

# -------------------------------
# PARTE 1: ANÁLISE DE RISCO QUALITATIVA (COMPLETAMENTE EDITÁVEL)
# -------------------------------
with st.expander("📊 Matriz de Análise de Risco (Probabilidade x Impacto)", expanded=True):
    st.markdown("""
    **Critérios:**  
    - **Probabilidade:** Baixa | Média | Alta  
    - **Impacto:** Baixo | Médio | Alto  
    - **Nível do risco:**  
        - 🟢 **Baixo** (Baixa x Baixo, Baixa x Médio, Média x Baixo)  
        - 🟡 **Médio** (Baixa x Alto, Média x Médio, Alta x Baixo)  
        - 🔴 **Alto** (Média x Alto, Alta x Médio, Alta x Alto)
    
    **Instruções:**  
    ✏️ Clique duas vezes em qualquer célula para editar  
    🗑️ Use os botões abaixo para adicionar ou remover linhas  
    📍 A coluna **Localidade** ajuda a mapear onde está o ativo
    """)

    # Dados iniciais (com Localidade)
    dados_risco_inicial = pd.DataFrame({
        "Ativo": ["Cabos na sala de servidores", "Pen drive ou HD", "Servidor de internet", "Switch de borda"],
        "Localidade": ["Sala de servidores - Bloco A", "TI - Sala 210", "Data Center - Rack 05", "Sala de rede - Andar 3"],
        "Ameaça": ["Rompimento", "Contaminação por vírus", "Invasão externa", "Desligamento acidental"],
        "Vulnerabilidade": ["Cabos fora de dutos", "Antivírus desatualizado", "Internet ligada direto na rede interna", "Sem trava física no rack"],
        "Probabilidade": ["Baixa", "Alta", "Média", "Média"],
        "Impacto": ["Alto", "Alto", "Alto", "Médio"],
    })

    # Função para calcular nível do risco
    def nivel_risco(prob, imp):
        prob = str(prob).lower().strip()
        imp = str(imp).lower().strip()
        
        if (prob == "baixa" and imp == "baixo") or (prob == "baixa" and imp == "médio") or (prob == "média" and imp == "baixo"):
            return "🟢 Baixo"
        elif (prob == "baixa" and imp == "alto") or (prob == "média" and imp == "médio") or (prob == "alta" and imp == "baixo"):
            return "🟡 Médio"
        else:
            return "🔴 Alto"

    # Adicionar coluna de nível do risco
    dados_risco_inicial["Nível do risco"] = dados_risco_inicial.apply(
        lambda row: nivel_risco(row["Probabilidade"], row["Impacto"]), axis=1
    )

    # Configuração do data_editor completo
    edited_risco = st.data_editor(
        dados_risco_inicial,
        use_container_width=True,
        num_rows="dynamic",  # Permite adicionar/excluir linhas
        column_config={
            "Ativo": st.column_config.TextColumn("🏷️ Ativo", required=True),
            "Localidade": st.column_config.TextColumn("📍 Localidade", required=True),
            "Ameaça": st.column_config.TextColumn("⚠️ Ameaça", required=True),
            "Vulnerabilidade": st.column_config.TextColumn("🔓 Vulnerabilidade", required=True),
            "Probabilidade": st.column_config.SelectboxColumn(
                "📊 Probabilidade",
                options=["Baixa", "Média", "Alta"],
                required=True
            ),
            "Impacto": st.column_config.SelectboxColumn(
                "💥 Impacto",
                options=["Baixo", "Médio", "Alto"],
                required=True
            ),
            "Nível do risco": st.column_config.TextColumn("🎯 Nível do Risco", disabled=True),
        },
        hide_index=True,
    )

    # Recalcular risco após qualquer edição
    edited_risco["Nível do risco"] = edited_risco.apply(
        lambda row: nivel_risco(row["Probabilidade"], row["Impacto"]), axis=1
    )

    # Estatísticas rápidas
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total de Riscos", len(edited_risco))
    with col2:
        qtd_alto = len(edited_risco[edited_risco["Nível do risco"] == "🔴 Alto"])
        st.metric("🔴 Riscos Altos", qtd_alto, delta="Prioridade crítica" if qtd_alto > 0 else None)
    with col3:
        qtd_medio = len(edited_risco[edited_risco["Nível do risco"] == "🟡 Médio"])
        st.metric("🟡 Riscos Médios", qtd_medio)
    with col4:
        qtd_baixo = len(edited_risco[edited_risco["Nível do risco"] == "🟢 Baixo"])
        st.metric("🟢 Riscos Baixos", qtd_baixo)

    # Filtro por Localidade
    st.markdown("---")
    with st.expander("🔍 Filtrar por Localidade"):
        localidades = ["Todas"] + sorted(edited_risco["Localidade"].unique().tolist())
        filtro_local = st.selectbox("Selecione a localidade:", localidades)
        
        if filtro_local != "Todas":
            risco_filtrado = edited_risco[edited_risco["Localidade"] == filtro_local]
            st.dataframe(risco_filtrado, use_container_width=True, hide_index=True)
            
            # Mostrar resumo da localidade
            st.caption(f"📍 Localidade: {filtro_local} - Total de riscos: {len(risco_filtrado)}")
            st.progress(len(risco_filtrado) / len(edited_risco) if len(edited_risco) > 0 else 0)
    
    # Botão para exportar análise de risco
    col_exp1, col_exp2 = st.columns(2)
    with col_exp1:
        if st.button("📥 Exportar Análise de Risco (CSV)", use_container_width=True):
            csv = edited_risco.to_csv(index=False)
            st.download_button(
                label="📎 Clique para baixar CSV",
                data=csv,
                file_name=f"analise_risco_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )

st.markdown("---")

# -------------------------------
# PARTE 2: PDCA (MELHORADO)
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

# CSS para melhorar visualização
st.markdown("""
<style>
    textarea {
        height: 100px !important;
    }
    [data-testid="stExpander"] summary {
        font-size: 1.2rem;
        font-weight: bold;
    }
    .stDataFrame {
        font-size: 12px;
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
            # Adicionar sugestão baseada nos riscos altos
            sugestao = ""
            if titulo == "⚙️ Ação Técnica (TI/OT)" and len(edited_risco[edited_risco["Nível do risco"] == "🔴 Alto"]) > 0:
                sugestao = " (⚠️ Prioridade: tratar riscos altos primeiro)"
            valor = st.text_area(
                label="",
                key=key_id,
                placeholder=f"Digite o {titulo.lower()}{sugestao}...",
                label_visibility="collapsed",
                height=100
            )
            dados_pdca[(i, j)] = valor

# -------------------------------
# PARTE 3: IMPRESSÃO UNIFICADA E EXPORTAÇÃO
# -------------------------------
st.markdown("---")
col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])

with col_btn1:
    if st.button("🖨️ Imprimir Relatório Completo", use_container_width=True):
        # Gerar HTML da análise de risco com Localidade
        risco_html = edited_risco.to_html(index=False, escape=False)
        
        # Gerar HTML do PDCA
        pdca_html = "<table border='1' cellpadding='8' cellspacing='0' style='border-collapse: collapse; width: 100%;'>"
        pdca_html += "<tr>"
        for col in colunas:
            pdca_html += f"<th style='background:{col['cor']}; color:white'>{col['nome']}</th>"
        pdca_html += "</tr>"
        for j, linha_nome in enumerate(linhas):
            pdca_html += "<tr>"
            for i in range(len(colunas)):
                conteudo = dados_pdca.get((i, j), "").replace("\n", "<br>")
                pdca_html += f"<td><b>{linha_nome}</b><br>{conteudo}</td>"
            pdca_html += "</tr>"
        pdca_html += "</table>"

        # Resumo de riscos por localidade
        resumo_localidade = edited_risco.groupby(["Localidade", "Nível do risco"]).size().unstack(fill_value=0)
        resumo_html = resumo_localidade.to_html()

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
            <p><strong>Data de emissão:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
            
            <h2>📊 Matriz de Análise de Risco (com Localidade)</h2>
            {risco_html}
            
            <h2>📍 Resumo de Riscos por Localidade</h2>
            {resumo_html}
            
            <h2>🔄 PDCA de Controle de Acesso</h2>
            {pdca_html}
            
            <script>window.onload = function() {{ window.print(); }}</script>
        </body>
        </html>
        """
        st.components.v1.html(html_completo, height=600)

with col_btn2:
    if st.button("📊 Exportar Tudo para Excel", use_container_width=True):
        with pd.ExcelWriter("relatorio_seguranca.xlsx", engine="openpyxl") as writer:
            edited_risco.to_excel(writer, sheet_name="Analise_Risco", index=False)
            
            # Exportar PDCA para Excel
            pdca_df = pd.DataFrame()
            for i, col_info in enumerate(colunas):
                for j, linha_nome in enumerate(linhas):
                    key = (i, j)
                    pdca_df.loc[linha_nome, col_info["nome"]] = dados_pdca.get(key, "")
            pdca_df.to_excel(writer, sheet_name="PDCA")
        
        with open("relatorio_seguranca.xlsx", "rb") as f:
            st.download_button(
                label="📎 Baixar Excel",
                data=f,
                file_name=f"relatorio_seguranca_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

with col_btn3:
    st.caption("✅ A análise de risco (com localidade) alimenta diretamente as ações do PDCA")

# -------------------------------
# PARTE 4: SUGESTÕES INTELIGENTES BASEADAS NOS RISCOS
# -------------------------------
with st.expander("💡 Sugestões de melhoria baseadas na sua análise de risco"):
    # Identificar riscos altos por localidade
    riscos_altos = edited_risco[edited_risco["Nível do risco"] == "🔴 Alto"]
    
    if len(riscos_altos) > 0:
        st.markdown("### 🔴 **Riscos Altos Identificados (Prioridade Máxima)**")
        for _, row in riscos_altos.iterrows():
            st.markdown(f"""
            - **📍 {row['Localidade']}** | **Ativo:** {row['Ativo']}  
                - **Ameaça:** {row['Ameaça']}  
                - **Vulnerabilidade:** {row['Vulnerabilidade']}  
                - **Ação sugerida no PDCA:**  
                    → Incluir no *Planejamento* uma ação específica para mitigar este risco  
                    → Reforçar no *Suporte* (treinamento, recursos)  
                    → Monitorar na *Avaliação* com indicador específico
            """)
    else:
        st.success("✅ Nenhum risco alto identificado! Continue monitorando os riscos médios.")
    
    # Riscos médios
    riscos_medios = edited_risco[edited_risco["Nível do risco"] == "🟡 Médio"]
    if len(riscos_medios) > 0:
        st.markdown("### 🟡 **Riscos Médios (Planejamento de médio prazo)**")
        for _, row in riscos_medios.iterrows():
            st.markdown(f"- **{row['Localidade']}** - {row['Ativo']}: {row['Vulnerabilidade']}")

st.success("🔁 PDCA + Análise de Risco (com Localidade) integrados e totalmente editáveis!")

# -------------------------------
# SIDEBAR COM INFORMAÇÕES
# -------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/security-checked--v1.png", width=80)
    st.markdown("## 📋 Instruções Rápidas")
    st.markdown("""
    1. **Edite a tabela de risco** - Adicione/remova linhas, altere localidades, probabilidade e impacto
    2. **Preencha o PDCA** - Use os riscos identificados como base para as ações
    3. **Filtre por localidade** - Para focar em áreas específicas
    4. **Exporte ou imprima** - Relatório completo com todos os dados
    
    ### 🎯 Dicas:
    - Riscos **Altos** → Ação imediata no PDCA
    - Riscos **Médios** → Plano de 30-60 dias
    - Riscos **Baixos** → Monitoramento contínuo
    """)
    
    st.markdown("---")
    st.caption(f"Última atualização: {datetime.now().strftime('%H:%M:%S')}")
