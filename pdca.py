import streamlit as st
import pandas as pd
from datetime import datetime

# -------------------------------
# CONFIGURAÇÃO DA PÁGINA
# -------------------------------
st.set_page_config(layout="wide", page_title="PDCA + Análise de Risco", page_icon="🛡️")

st.title("🛡️ PDCA de Controle de Acesso + Análise de Risco")
st.markdown("---")

# CSS para garantir alinhamento perfeito
st.markdown("""
<style>
    /* Garantir que todas as colunas tenham mesma largura */
    .stColumn {
        flex: 1 !important;
        min-width: 0 !important;
    }
    
    /* Uniformizar altura dos textareas */
    textarea {
        height: 120px !important;
        min-height: 120px !important;
        max-height: 120px !important;
        resize: vertical !important;
        font-size: 13px !important;
        line-height: 1.4 !important;
    }
    
    /* Estilo dos cabeçalhos das colunas */
    .pdca-header {
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        font-weight: bold;
        font-size: 14px;
        border-radius: 10px 10px 0 0;
        margin-bottom: 10px;
        white-space: normal;
        word-wrap: break-word;
    }
    
    /* Títulos das linhas */
    .row-title {
        background-color: #f8f9fa;
        padding: 12px 8px;
        margin: 5px 0;
        border-left: 4px solid;
        border-radius: 4px;
        font-weight: 600;
        font-size: 13px;
        height: 130px;
        display: flex;
        align-items: center;
    }
    
    /* Container para cada célula do PDCA */
    .pdca-cell {
        margin-bottom: 10px;
        height: 130px;
    }
    
    /* Garantir altura consistente */
    .stTextArea > div {
        height: 120px !important;
    }
    
    /* Remover padding extra */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
    
    /* Melhorar visualização em telas menores */
    @media (max-width: 1200px) {
        .pdca-header {
            font-size: 11px;
            white-space: normal;
            padding: 5px;
        }
        .row-title {
            font-size: 11px;
            padding: 8px 4px;
        }
        textarea {
            font-size: 11px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# PARTE 1: ANÁLISE DE RISCO QUALITATIVA
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

    # Dados iniciais
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

    dados_risco_inicial["Nível do risco"] = dados_risco_inicial.apply(
        lambda row: nivel_risco(row["Probabilidade"], row["Impacto"]), axis=1
    )

    # Data editor editável
    edited_risco = st.data_editor(
        dados_risco_inicial,
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            "Ativo": st.column_config.TextColumn("🏷️ Ativo", required=True, width="medium"),
            "Localidade": st.column_config.TextColumn("📍 Localidade", required=True, width="medium"),
            "Ameaça": st.column_config.TextColumn("⚠️ Ameaça", required=True, width="medium"),
            "Vulnerabilidade": st.column_config.TextColumn("🔓 Vulnerabilidade", required=True, width="large"),
            "Probabilidade": st.column_config.SelectboxColumn("📊 Probabilidade", options=["Baixa", "Média", "Alta"], required=True, width="small"),
            "Impacto": st.column_config.SelectboxColumn("💥 Impacto", options=["Baixo", "Médio", "Alto"], required=True, width="small"),
            "Nível do risco": st.column_config.TextColumn("🎯 Nível", disabled=True, width="small"),
        },
        hide_index=True,
    )

    # Recalcular risco
    edited_risco["Nível do risco"] = edited_risco.apply(
        lambda row: nivel_risco(row["Probabilidade"], row["Impacto"]), axis=1
    )

    # Estatísticas
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

st.markdown("---")

# -------------------------------
# PARTE 2: PDCA COM ALINHAMENTO PERFEITO
# -------------------------------
st.subheader("🔄 PDCA de Controle de Acesso - Gestão de Segurança")

# Definição das colunas do PDCA
colunas_pdca = [
    {"nome": "1. Contexto (P)", "cor": "#1E88E5", "desc": "Análise do ambiente interno/externo"},
    {"nome": "2. Liderança (P)", "cor": "#1E88E5", "desc": "Comprometimento da alta direção"},
    {"nome": "3. Planejamento (P)", "cor": "#1E88E5", "desc": "Objetivos e riscos"},
    {"nome": "4. Suporte (D)", "cor": "#E53935", "desc": "Recursos, competência, comunicação"},
    {"nome": "5. Operação (D)", "cor": "#E53935", "desc": "Controles operacionais"},
    {"nome": "6. Avaliação (C)", "cor": "#43A047", "desc": "Monitoramento e medição"},
    {"nome": "7. Melhoria (A)", "cor": "#FB8C00", "desc": "Ações corretivas e preventivas"}
]

# Linhas do PDCA
linhas_pdca = [
    {"nome": "🎯 Objetivo Estratégico", "icon": "🎯", "tooltip": "Meta principal do controle de acesso"},
    {"nome": "⚙️ Ação Técnica (TI/OT)", "icon": "⚙️", "tooltip": "Implementações técnicas e operacionais"},
    {"nome": "📊 Indicador (KPI)", "icon": "📊", "tooltip": "Métrica para medir sucesso"},
    {"nome": "🚩 Evidência / Status", "icon": "🚩", "tooltip": "Comprovação da execução"}
]

# Criar colunas com largura igual
cols = st.columns(len(colunas_pdca), gap="small")

# Dicionário para armazenar dados
dados_pdca = {}

# Renderizar cabeçalhos e células
for i, col_info in enumerate(colunas_pdca):
    with cols[i]:
        # Cabeçalho da coluna
        st.markdown(f"""
            <div class="pdca-header" style="background-color: {col_info['cor']}; color: white;">
                <div>
                    <strong>{col_info['nome']}</strong><br>
                    <small style="font-size: 10px; opacity: 0.9;">{col_info['desc']}</small>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Para cada linha
        for j, linha_info in enumerate(linhas_pdca):
            # Título da linha (apenas na primeira coluna)
            if i == 0:
                st.markdown(f"""
                    <div class="row-title" style="border-left-color: {col_info['cor']};">
                        <div>
                            <strong>{linha_info['nome']}</strong><br>
                            <small style="font-size: 10px; color: #666;">{linha_info['tooltip']}</small>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                # Espaço para alinhar verticalmente
                st.markdown(f"""
                    <div class="row-title" style="border-left-color: transparent; background-color: transparent;">
                        &nbsp;
                    </div>
                """, unsafe_allow_html=True)
            
            # Campo de texto
            key_id = f"pdca_{i}_{j}"
            valor = st.text_area(
                label="",
                key=key_id,
                placeholder=f"Digite aqui...",
                label_visibility="collapsed",
                help=f"{linha_info['tooltip']}"
            )
            dados_pdca[(i, j)] = valor
            
            # Pequeno espaço entre campos
            st.markdown("<div style='margin-bottom: 5px;'></div>", unsafe_allow_html=True)

# Botões de ação
st.markdown("---")
col_btn1, col_btn2, col_btn3, col_btn4 = st.columns([1, 1, 1, 2])

with col_btn1:
    if st.button("🖨️ Imprimir Relatório", use_container_width=True):
        # Gerar HTML do PDCA com alinhamento perfeito
        pdca_html = """
        <style>
            .pdca-table {
                width: 100%;
                border-collapse: collapse;
                font-family: Arial, sans-serif;
            }
            .pdca-table th {
                padding: 12px;
                text-align: center;
                color: white;
                font-weight: bold;
                border: 1px solid #ddd;
            }
            .pdca-table td {
                padding: 10px;
                vertical-align: top;
                border: 1px solid #ddd;
                background-color: #f9f9f9;
            }
            .pdca-table .row-label {
                background-color: #f0f0f0;
                font-weight: bold;
                width: 120px;
            }
            .pdca-content {
                min-height: 100px;
            }
        </style>
        """
        
        pdca_html += "<table class='pdca-table'>"
        # Cabeçalho
        pdca_html += "<tr>"
        pdca_html += "<th style='background:#666;'>Área</th>"
        for col in colunas_pdca:
            pdca_html += f"<th style='background:{col['cor']};'>{col['nome']}</th>"
        pdca_html += "</tr>"
        
        # Linhas
        for j, linha_info in enumerate(linhas_pdca):
            pdca_html += "<tr>"
            pdca_html += f"<td class='row-label' style='background:#f5f5f5;'>{linha_info['nome']}</td>"
            for i in range(len(colunas_pdca)):
                conteudo = dados_pdca.get((i, j), "").replace("\n", "<br>")
                pdca_html += f"<td><div class='pdca-content'>{conteudo if conteudo else '—'}</div></td>"
            pdca_html += "</tr>"
        pdca_html += "</table>"
        
        # HTML completo
        risco_html = edited_risco.to_html(index=False, escape=False)
        html_completo = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1, h2 {{ color: #1E3A5F; }}
                table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
                th, td {{ border: 1px solid #aaa; padding: 8px; vertical-align: top; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <h1>🛡️ Relatório de Segurança - PDCA + Análise de Risco</h1>
            <p><strong>Data:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
            
            <h2>📊 Análise de Risco</h2>
            {risco_html}
            
            <h2>🔄 PDCA de Controle de Acesso</h2>
            {pdca_html}
            
            <script>window.onload = function() {{ window.print(); }}</script>
        </body>
        </html>
        """
        st.components.v1.html(html_completo, height=600)

with col_btn2:
    if st.button("📥 Exportar Excel", use_container_width=True):
        with pd.ExcelWriter("relatorio_seguranca.xlsx", engine="openpyxl") as writer:
            edited_risco.to_excel(writer, sheet_name="Analise_Risco", index=False)
            
            # Exportar PDCA formatado
            pdca_df = pd.DataFrame()
            for j, linha_info in enumerate(linhas_pdca):
                row_data = {"Área": linha_info['nome']}
                for i, col_info in enumerate(colunas_pdca):
                    row_data[col_info['nome']] = dados_pdca.get((i, j), "")
                pdca_df = pd.concat([pdca_df, pd.DataFrame([row_data])], ignore_index=True)
            pdca_df.to_excel(writer, sheet_name="PDCA", index=False)
        
        with open("relatorio_seguranca.xlsx", "rb") as f:
            st.download_button(
                label="📎 Baixar",
                data=f,
                file_name=f"relatorio_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

with col_btn3:
    if st.button("🗑️ Limpar PDCA", use_container_width=True):
        for i in range(len(colunas_pdca)):
            for j in range(len(linhas_pdca)):
                st.session_state[f"pdca_{i}_{j}"] = ""
        st.rerun()

with col_btn4:
    st.caption("✅ PDCA alinhado | Riscos por localidade | Gestão integrada")

# -------------------------------
# SIDEBAR
# -------------------------------
with st.sidebar:
    st.markdown("## 📋 Painel de Controle")
    st.markdown("---")
    
    # Resumo dos riscos
    st.markdown("### 🎯 Resumo Riscos")
    risco_alto = len(edited_risco[edited_risco["Nível do risco"] == "🔴 Alto"])
    risco_medio = len(edited_risco[edited_risco["Nível do risco"] == "🟡 Médio"])
    risco_baixo = len(edited_risco[edited_risco["Nível do risco"] == "🟢 Baixo"])
    
    st.markdown(f"""
    - 🔴 **Alto:** {risco_alto}
    - 🟡 **Médio:** {risco_medio}
    - 🟢 **Baixo:** {risco_baixo}
    """)
    
    # Localidades únicas
    st.markdown("### 📍 Localidades")
    for loc in edited_risco["Localidade"].unique():
        st.markdown(f"- {loc}")
    
    st.markdown("---")
    st.markdown("### 💡 Dicas")
    st.markdown("""
    - **Altura dos campos:** 120px (padronizada)
    - **Largura:** Colunas proporcionais
    - **Alinhamento:** Perfeito entre linhas
    - **Responsivo:** Adapta à tela
    """)
    
    st.caption(f"🕐 {datetime.now().strftime('%H:%M:%S')}")

st.success("✅ **PDCA perfeitamente alinhado e simétrico!** Todas as colunas têm largura igual e campos com altura padronizada.")
