import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from plotly.subplots import make_subplots

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
    
    /* Estilo para abas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 4px 4px 0 0;
        padding: 8px 16px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# FUNÇÕES AUXILIARES
# -------------------------------
def nivel_risco(prob, imp):
    prob = str(prob).lower().strip()
    imp = str(imp).lower().strip()
    
    if (prob == "baixa" and imp == "baixo") or (prob == "baixa" and imp == "médio") or (prob == "média" and imp == "baixo"):
        return "🟢 Baixo"
    elif (prob == "baixa" and imp == "alto") or (prob == "média" and imp == "médio") or (prob == "alta" and imp == "baixo"):
        return "🟡 Médio"
    else:
        return "🔴 Alto"

# -------------------------------
# CRIAÇÃO DAS ABAS PRINCIPAIS
# -------------------------------
tab1, tab2, tab3 = st.tabs(["📊 Análise de Risco", "🖥️ Gestão de Equipamentos", "🔄 PDCA de Controle de Acesso"])

# ======================== TAB 1: ANÁLISE DE RISCO ========================
with tab1:
    st.markdown("## 📊 Matriz de Análise de Risco")
    st.markdown("""
    **Critérios:**  
    - **Probabilidade:** Baixa | Média | Alta  
    - **Impacto:** Baixo | Médio | Alto  
    - **Nível do risco:** 🟢 Baixo | 🟡 Médio | 🔴 Alto
    """)

    # Dados iniciais
    dados_risco_inicial = pd.DataFrame({
        "Ativo": ["Cabos na sala de servidores", "Pen drive ou HD", "Servidor de internet", "Switch de borda", "Firewall", "Router core"],
        "Localidade": ["Sala de servidores - Bloco A", "TI - Sala 210", "Data Center - Rack 05", "Sala de rede - Andar 3", "Data Center - Rack 02", "Data Center - Rack 01"],
        "Ameaça": ["Rompimento", "Contaminação por vírus", "Invasão externa", "Desligamento acidental", "Ataque DDoS", "Configuração errada"],
        "Vulnerabilidade": ["Cabos fora de dutos", "Antivírus desatualizado", "Internet ligada direto na rede interna", "Sem trava física no rack", "Firmware desatualizado", "Senha fraca"],
        "Probabilidade": ["Baixa", "Alta", "Média", "Média", "Baixa", "Média"],
        "Impacto": ["Alto", "Alto", "Alto", "Médio", "Alto", "Alto"],
    })

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

    # ========== GRÁFICOS ==========
    st.markdown("---")
    st.markdown("## 📈 Dashboard de Riscos por Localidade")
    
    # Preparar dados para gráficos
    risco_por_local = edited_risco.groupby(['Localidade', 'Nível do risco']).size().reset_index(name='Quantidade')
    
    # Gráfico 1: Barras empilhadas por localidade
    col_graf1, col_graf2 = st.columns(2)
    
    with col_graf1:
        fig1 = px.bar(
            risco_por_local,
            x='Localidade',
            y='Quantidade',
            color='Nível do risco',
            title='📊 Riscos por Localidade (Distribuição)',
            color_discrete_map={'🟢 Baixo': '#4CAF50', '🟡 Médio': '#FFC107', '🔴 Alto': '#F44336'},
            text='Quantidade',
            height=400
        )
        fig1.update_layout(
            xaxis_title="Localidade",
            yaxis_title="Quantidade de Riscos",
            showlegend=True,
            bargap=0.2
        )
        fig1.update_traces(textposition='inside')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col_graf2:
        # Gráfico 2: Pizza - distribuição geral
        geral_riscos = edited_risco['Nível do risco'].value_counts()
        fig2 = px.pie(
            values=geral_riscos.values,
            names=geral_riscos.index,
            title='🎯 Distribuição Geral de Riscos',
            color_discrete_map={'🟢 Baixo': '#4CAF50', '🟡 Médio': '#FFC107', '🔴 Alto': '#F44336'},
            hole=0.3,
            height=400
        )
        fig2.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig2, use_container_width=True)
    
    # Gráfico 3: Mapa de calor de riscos
    st.markdown("---")
    col_graf3, col_graf4 = st.columns(2)
    
    with col_graf3:
        # Matriz Probabilidade x Impacto
        matriz_risco = pd.crosstab(
            edited_risco['Probabilidade'], 
            edited_risco['Impacto'],
            values=edited_risco['Nível do risco'],
            aggfunc=lambda x: len(x),
            fill_value=0
        )
        
        fig3 = px.imshow(
            matriz_risco,
            text_auto=True,
            title='🔥 Matriz de Calor (Prob x Impacto)',
            color_continuous_scale=['#4CAF50', '#FFC107', '#F44336'],
            aspect='auto',
            height=400
        )
        fig3.update_layout(xaxis_title="Impacto", yaxis_title="Probabilidade")
        st.plotly_chart(fig3, use_container_width=True)
    
    with col_graf4:
        # Gráfico de radar por localidade
        localidades_risco = edited_risco.groupby('Localidade').size().reset_index(name='Total')
        fig4 = px.bar(
            localidades_risco,
            x='Localidade',
            y='Total',
            title='🏢 Total de Riscos por Localidade',
            color='Total',
            color_continuous_scale='Reds',
            text='Total',
            height=400
        )
        fig4.update_layout(xaxis_title="Localidade", yaxis_title="Total de Riscos")
        fig4.update_traces(textposition='outside')
        st.plotly_chart(fig4, use_container_width=True)
    
    # Estatísticas
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📊 Total de Riscos", len(edited_risco))
    with col2:
        qtd_alto = len(edited_risco[edited_risco["Nível do risco"] == "🔴 Alto"])
        st.metric("🔴 Riscos Altos", qtd_alto, delta="Prioridade crítica" if qtd_alto > 0 else None)
    with col3:
        qtd_medio = len(edited_risco[edited_risco["Nível do risco"] == "🟡 Médio"])
        st.metric("🟡 Riscos Médios", qtd_medio)
    with col4:
        qtd_baixo = len(edited_risco[edited_risco["Nível do risco"] == "🟢 Baixo"])
        st.metric("🟢 Riscos Baixos", qtd_baixo)

# ======================== TAB 2: GESTÃO DE EQUIPAMENTOS ========================
with tab2:
    st.markdown("## 🖥️ Gestão de Equipamentos de TI/OT")
    
    # Dados iniciais de equipamentos
    dados_equipamentos_inicial = pd.DataFrame({
        "Equipamento": ["Firewall Fortinet", "Switch Core Huawei", "Router Cisco", "Servidor Dell", "Storage EMC", "Access Point", "Patch Panel"],
        "Tipo": ["Segurança", "Rede", "Rede", "Servidor", "Storage", "Rede", "Infraestrutura"],
        "Localidade": ["Data Center - Rack 02", "Data Center - Rack 01", "Data Center - Rack 01", "Data Center - Rack 03", "Data Center - Rack 04", "Sala 210 - Teto", "Sala de servidores"],
        "Fabricante": ["Fortinet", "Huawei", "Cisco", "Dell", "EMC", "Ubiquiti", "Intelbras"],
        "Modelo": ["FG-100F", "S12700", "ISR 4321", "PowerEdge R750", "Unity XT 380", "U6-LR", "CAT6"],
        "Número Série": ["FGT100F12345", "HW127001234", "CISCO4321ABC", "DELL123456", "EMC789012", "UBI678901", "INT345678"],
        "Data Instalação": ["2023-01-15", "2022-06-20", "2023-03-10", "2024-01-05", "2023-08-22", "2024-02-14", "2022-11-30"],
        "Status": ["Ativo", "Ativo", "Ativo", "Ativo", "Ativo", "Ativo", "Ativo"],
        "Última Manutenção": ["2024-01-20", "2023-12-15", "2024-02-01", "2024-01-10", "2023-11-05", "2024-02-20", "2023-10-10"],
        "Próxima Manutenção": ["2024-04-20", "2024-03-15", "2024-05-01", "2024-04-10", "2024-02-05", "2024-05-20", "2024-01-10"],
    })
    
    # Editor de equipamentos
    edited_equipamentos = st.data_editor(
        dados_equipamentos_inicial,
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            "Equipamento": st.column_config.TextColumn("🖥️ Equipamento", required=True, width="medium"),
            "Tipo": st.column_config.SelectboxColumn("📂 Tipo", options=["Segurança", "Rede", "Servidor", "Storage", "Infraestrutura", "Cliente"], width="small"),
            "Localidade": st.column_config.TextColumn("📍 Localidade", required=True, width="medium"),
            "Fabricante": st.column_config.TextColumn("🏭 Fabricante", width="medium"),
            "Modelo": st.column_config.TextColumn("📟 Modelo", width="medium"),
            "Número Série": st.column_config.TextColumn("🔢 Número Série", width="small"),
            "Data Instalação": st.column_config.DateColumn("📅 Data Instalação", width="small"),
            "Status": st.column_config.SelectboxColumn("⚙️ Status", options=["Ativo", "Em Manutenção", "Desativado", "Reserva"], width="small"),
            "Última Manutenção": st.column_config.DateColumn("🔧 Última Manutenção", width="small"),
            "Próxima Manutenção": st.column_config.DateColumn("📅 Próxima Manutenção", width="small"),
        },
        hide_index=True,
    )
    
    # Dashboard de equipamentos
    st.markdown("---")
    st.markdown("## 📊 Dashboard de Equipamentos")
    
    col_eq1, col_eq2, col_eq3, col_eq4 = st.columns(4)
    with col_eq1:
        st.metric("📦 Total Equipamentos", len(edited_equipamentos))
    with col_eq2:
        qtd_ativo = len(edited_equipamentos[edited_equipamentos["Status"] == "Ativo"])
        st.metric("✅ Equipamentos Ativos", qtd_ativo)
    with col_eq3:
        qtd_seguranca = len(edited_equipamentos[edited_equipamentos["Tipo"] == "Segurança"])
        st.metric("🔒 Equipamentos Segurança", qtd_seguranca)
    with col_eq4:
        # Equipamentos com manutenção próxima (30 dias)
        hoje = datetime.now().date()
        try:
            edited_equipamentos["Próxima Manutenção"] = pd.to_datetime(edited_equipamentos["Próxima Manutenção"]).dt.date
            prox_manut = len(edited_equipamentos[
                (edited_equipamentos["Próxima Manutenção"] >= hoje) & 
                (edited_equipamentos["Próxima Manutenção"] <= hoje + pd.Timedelta(days=30))
            ])
            st.metric("⚠️ Manutenção (30 dias)", prox_manut, delta="Agendar" if prox_manut > 0 else None)
        except:
            st.metric("⚠️ Manutenção (30 dias)", 0)
    
    # Gráficos de equipamentos
    st.markdown("---")
    col_eq_graf1, col_eq_graf2 = st.columns(2)
    
    with col_eq_graf1:
        # Distribuição por tipo
        tipo_count = edited_equipamentos["Tipo"].value_counts()
        fig_eq1 = px.pie(
            values=tipo_count.values,
            names=tipo_count.index,
            title="📊 Distribuição por Tipo de Equipamento",
            hole=0.3,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig_eq1, use_container_width=True)
    
    with col_eq_graf2:
        # Equipamentos por localidade
        local_count = edited_equipamentos["Localidade"].value_counts().head(10)
        fig_eq2 = px.bar(
            x=local_count.values,
            y=local_count.index,
            orientation='h',
            title="📍 Equipamentos por Localidade",
            color=local_count.values,
            color_continuous_scale='Blues',
            text=local_count.values
        )
        fig_eq2.update_layout(xaxis_title="Quantidade", yaxis_title="Localidade", height=400)
        fig_eq2.update_traces(textposition='outside')
        st.plotly_chart(fig_eq2, use_container_width=True)
    
    col_eq_graf3, col_eq_graf4 = st.columns(2)
    
    with col_eq_graf3:
        # Status dos equipamentos
        status_count = edited_equipamentos["Status"].value_counts()
        fig_eq3 = px.bar(
            x=status_count.index,
            y=status_count.values,
            title="⚙️ Status dos Equipamentos",
            color=status_count.values,
            color_continuous_scale='RdYlGn',
            text=status_count.values
        )
        fig_eq3.update_layout(xaxis_title="Status", yaxis_title="Quantidade")
        fig_eq3.update_traces(textposition='outside')
        st.plotly_chart(fig_eq3, use_container_width=True)
    
    with col_eq_graf4:
        # Fabricantes
        fabricante_count = edited_equipamentos["Fabricante"].value_counts().head(8)
        fig_eq4 = px.bar(
            x=fabricante_count.index,
            y=fabricante_count.values,
            title="🏭 Equipamentos por Fabricante",
            color=fabricante_count.values,
            color_continuous_scale='Viridis',
            text=fabricante_count.values
        )
        fig_eq4.update_layout(xaxis_title="Fabricante", yaxis_title="Quantidade")
        fig_eq4.update_traces(textposition='outside')
        st.plotly_chart(fig_eq4, use_container_width=True)
    
    # Exportar equipamentos
    col_export1, col_export2 = st.columns(2)
    with col_export1:
        if st.button("📥 Exportar Equipamentos (CSV)", use_container_width=True):
            csv_eq = edited_equipamentos.to_csv(index=False)
            st.download_button(
                label="📎 Baixar CSV",
                data=csv_eq,
                file_name=f"equipamentos_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

# ======================== TAB 3: PDCA ========================
with tab3:
    st.markdown("## 🔄 PDCA de Controle de Acesso - Gestão de Segurança")
    
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
    
    linhas_pdca = [
        {"nome": "🎯 Objetivo Estratégico", "icon": "🎯", "tooltip": "Meta principal do controle de acesso"},
        {"nome": "⚙️ Ação Técnica (TI/OT)", "icon": "⚙️", "tooltip": "Implementações técnicas e operacionais"},
        {"nome": "📊 Indicador (KPI)", "icon": "📊", "tooltip": "Métrica para medir sucesso"},
        {"nome": "🚩 Evidência / Status", "icon": "🚩", "tooltip": "Comprovação da execução"}
    ]
    
    # Criar colunas
    cols = st.columns(len(colunas_pdca), gap="small")
    dados_pdca = {}
    
    # Renderizar cabeçalhos e células
    for i, col_info in enumerate(colunas_pdca):
        with cols[i]:
            st.markdown(f"""
                <div class="pdca-header" style="background-color: {col_info['cor']}; color: white;">
                    <div>
                        <strong>{col_info['nome']}</strong><br>
                        <small style="font-size: 10px; opacity: 0.9;">{col_info['desc']}</small>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            for j, linha_info in enumerate(linhas_pdca):
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
                    st.markdown(f"""
                        <div class="row-title" style="border-left-color: transparent; background-color: transparent;">
                            &nbsp;
                        </div>
                    """, unsafe_allow_html=True)
                
                key_id = f"pdca_{i}_{j}"
                valor = st.text_area(
                    label="",
                    key=key_id,
                    placeholder=f"Digite aqui...",
                    label_visibility="collapsed",
                    help=f"{linha_info['tooltip']}"
                )
                dados_pdca[(i, j)] = valor
                st.markdown("<div style='margin-bottom: 5px;'></div>", unsafe_allow_html=True)
    
    # Botões de ação do PDCA
    st.markdown("---")
    col_btn1, col_btn2, col_btn3, col_btn4 = st.columns([1, 1, 1, 2])
    
    with col_btn1:
        if st.button("🖨️ Imprimir Relatório", use_container_width=True):
            # Gerar HTML completo com todos os dados
            risco_html = edited_risco.to_html(index=False, escape=False)
            equip_html = edited_equipamentos.to_html(index=False, escape=False)
            
            pdca_html = "<table border='1' style='width:100%; border-collapse:collapse;'>"
            pdca_html += "<tr>"
            for col in colunas_pdca:
                pdca_html += f"<th style='background:{col['cor']}; color:white; padding:8px;'>{col['nome']}</th>"
            pdca_html += "</tr>"
            for j in range(len(linhas_pdca)):
                pdca_html += "<tr>"
                for i in range(len(colunas_pdca)):
                    conteudo = dados_pdca.get((i, j), "").replace("\n", "<br>")
                    pdca_html += f"<td style='padding:8px; border:1px solid #ddd; vertical-align:top;'><b>{linhas_pdca[j]['nome']}</b><br>{conteudo if conteudo else '—'}</td>"
                pdca_html += "</tr>"
            pdca_html += "</table>"
            
            html_completo = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    h1, h2, h3 {{ color: #1E3A5F; }}
                    table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
                    th, td {{ border: 1px solid #aaa; padding: 8px; vertical-align: top; }}
                    th {{ background-color: #f2f2f2; }}
                </style>
            </head>
            <body>
                <h1>🛡️ Relatório Completo - Segurança da Informação</h1>
                <p><strong>Data:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
                
                <h2>📊 Análise de Risco</h2>
                {risco_html}
                
                <h2>🖥️ Inventário de Equipamentos</h2>
                {equip_html}
                
                <h2>🔄 PDCA de Controle de Acesso</h2>
                {pdca_html}
                
                <script>window.onload = function() {{ window.print(); }}</script>
            </body>
            </html>
            """
            st.components.v1.html(html_completo, height=600)
    
    with col_btn2:
        if st.button("📥 Exportar Excel", use_container_width=True):
            with pd.ExcelWriter("relatorio_completo.xlsx", engine="openpyxl") as writer:
                edited_risco.to_excel(writer, sheet_name="Analise_Risco", index=False)
                edited_equipamentos.to_excel(writer, sheet_name="Equipamentos", index=False)
                
                pdca_df = pd.DataFrame()
                for j, linha_info in enumerate(linhas_pdca):
                    row_data = {"Área": linha_info['nome']}
                    for i, col_info in enumerate(colunas_pdca):
                        row_data[col_info['nome']] = dados_pdca.get((i, j), "")
                    pdca_df = pd.concat([pdca_df, pd.DataFrame([row_data])], ignore_index=True)
                pdca_df.to_excel(writer, sheet_name="PDCA", index=False)
            
            with open("relatorio_completo.xlsx", "rb") as f:
                st.download_button(
                    label="📎 Baixar Excel",
                    data=f,
                    file_name=f"relatorio_completo_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

# -------------------------------
# SIDEBAR COM INFORMAÇÕES
# -------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/security-checked--v1.png", width=80)
    st.markdown("## 📋 Painel de Controle")
    st.markdown("---")
    
    # Resumo rápido
    st.markdown("### 🎯 Resumo Riscos")
    risco_alto = len(edited_risco[edited_risco["Nível do risco"] == "🔴 Alto"])
    risco_medio = len(edited_risco[edited_risco["Nível do risco"] == "🟡 Médio"])
    risco_baixo = len(edited_risco[edited_risco["Nível do risco"] == "🟢 Baixo"])
    
    st.markdown(f"""
    - 🔴 **Alto:** {risco_alto}
    - 🟡 **Médio:** {risco_medio}
    - 🟢 **Baixo:** {risco_baixo}
    """)
    
    st.markdown("### 🖥️ Equipamentos")
    st.markdown(f"- **Total:** {len(edited_equipamentos)}")
    st.markdown(f"- **Ativos:** {len(edited_equipamentos[edited_equipamentos['Status'] == 'Ativo'])}")
    st.markdown(f"- **Segurança:** {len(edited_equipamentos[edited_equipamentos['Tipo'] == 'Segurança'])}")
    
    st.markdown("---")
    st.markdown("### 📍 Top Localidades")
    for loc in edited_risco["Localidade"].value_counts().head(3).index:
        st.markdown(f"- {loc[:30]}...")
    
    st.markdown("---")
    st.caption(f"🕐 Última atualização: {datetime.now().strftime('%H:%M:%S')}")

st.success("✅ **Sistema completo!** Análise de risco com gráficos + Gestão de equipamentos + PDCA alinhado")
