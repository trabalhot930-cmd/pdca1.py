import streamlit as st
import pandas as pd
from datetime import datetime

# -------------------------------
# CONFIGURAÇÃO DA PÁGINA
# -------------------------------
st.set_page_config(layout="wide", page_title="PDCA + Análise de Risco", page_icon="🛡️")

# -------------------------------
# SISTEMA DE AUTENTICAÇÃO
# -------------------------------
def verificar_login():
    """Verifica se o usuário está logado"""
    if 'autenticado' not in st.session_state:
        st.session_state.autenticado = False
    return st.session_state.autenticado

def fazer_login(username, password):
    """Função de login"""
    USUARIO_VALIDO = "Juan"
    SENHA_VALIDA = "Ju@n1990"
    
    if username == USUARIO_VALIDO and password == SENHA_VALIDA:
        st.session_state.autenticado = True
        st.session_state.usuario = username
        return True
    return False

def fazer_logout():
    """Função de logout"""
    st.session_state.autenticado = False
    st.session_state.usuario = ""
    st.rerun()

# Tela de login
if not verificar_login():
    st.title("🔐 Sistema de Gestão de Segurança")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 📋 Acesso Restrito")
        st.markdown("Digite suas credenciais para continuar:")
        
        with st.form("login_form"):
            username = st.text_input("👤 Usuário", placeholder="Digite seu usuário")
            password = st.text_input("🔒 Senha", type="password", placeholder="Digite sua senha")
            submit = st.form_submit_button("🚪 Entrar", use_container_width=True)
            
            if submit:
                if fazer_login(username, password):
                    st.success(f"✅ Bem-vindo, {username}!")
                    st.rerun()
                else:
                    st.error("❌ Usuário ou senha inválidos!")
        
        st.markdown("---")
        st.caption("💡 Credenciais:\nUsuário: Juan\nSenha: Ju@n1990")
    
    st.stop()

# -------------------------------
# CABEÇALHO COM LOGOUT
# -------------------------------
col_logout1, col_logout2 = st.columns([6, 1])
with col_logout1:
    st.title("🛡️ PDCA de Controle de Acesso + Análise de Risco")
with col_logout2:
    if st.button("🚪 Sair", use_container_width=True):
        fazer_logout()

st.markdown(f"👋 **Bem-vindo, {st.session_state.usuario}!** | 📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}")
st.markdown("---")

# CSS para alinhamento
st.markdown("""
<style>
    .stColumn {
        flex: 1 !important;
        min-width: 0 !important;
    }
    
    textarea {
        height: 120px !important;
        min-height: 120px !important;
        max-height: 120px !important;
        resize: vertical !important;
        font-size: 13px !important;
    }
    
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
    
    .stTextArea > div {
        height: 120px !important;
    }
    
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
    
    @media (max-width: 1200px) {
        .pdca-header {
            font-size: 11px;
            padding: 5px;
        }
        .row-title {
            font-size: 11px;
            padding: 8px 4px;
        }
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 4px 4px 0 0;
        padding: 8px 16px;
        font-weight: bold;
    }
    
    div[data-testid="column"]:nth-of-type(2) button {
        background-color: #dc3545;
        color: white;
    }
    div[data-testid="column"]:nth-of-type(2) button:hover {
        background-color: #c82333;
        color: white;
    }
    
    .metric-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin: 10px 0;
    }
    .metric-value {
        font-size: 28px;
        font-weight: bold;
    }
    .metric-label {
        font-size: 14px;
        color: #666;
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

def criar_grafico_barras(dados, titulo):
    """Cria um gráfico de barras usando HTML/CSS"""
    if len(dados) == 0:
        return "<p>Sem dados para exibir</p>"
    
    max_valor = max(dados.values()) if dados.values() else 1
    html = f"<div style='margin: 20px 0;'><h4>{titulo}</h4>"
    for label, valor in dados.items():
        percentual = (valor / max_valor) * 100
        cor = "#F44336" if "Alto" in label else "#FFC107" if "Médio" in label else "#4CAF50"
        html += f"""
        <div style='margin: 10px 0;'>
            <div style='display: flex; justify-content: space-between;'>
                <span>{label}</span>
                <span><strong>{valor}</strong></span>
            </div>
            <div style='background-color: #e0e0e0; border-radius: 10px; overflow: hidden;'>
                <div style='background-color: {cor}; width: {percentual}%; height: 30px; display: flex; align-items: center; justify-content: flex-end; padding-right: 10px; color: white; font-weight: bold;'>
                    {percentual:.0f}%
                </div>
            </div>
        </div>
        """
    html += "</div>"
    return html

# -------------------------------
# CRIAÇÃO DAS ABAS
# -------------------------------
tab1, tab2, tab3 = st.tabs(["📊 Análise de Risco", "🖥️ Gestão de Equipamentos", "🔄 PDCA de Controle de Acesso"])

# ======================== TAB 1: ANÁLISE DE RISCO ========================
with tab1:
    st.markdown("## 📊 Matriz de Análise de Risco")
    st.markdown("""
    **Critérios:** Probabilidade (Baixa|Média|Alta) x Impacto (Baixo|Médio|Alto)
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
            "Ativo": st.column_config.TextColumn("🏷️ Ativo", required=True),
            "Localidade": st.column_config.TextColumn("📍 Localidade", required=True),
            "Ameaça": st.column_config.TextColumn("⚠️ Ameaça", required=True),
            "Vulnerabilidade": st.column_config.TextColumn("🔓 Vulnerabilidade", required=True),
            "Probabilidade": st.column_config.SelectboxColumn("📊 Probabilidade", options=["Baixa", "Média", "Alta"]),
            "Impacto": st.column_config.SelectboxColumn("💥 Impacto", options=["Baixo", "Médio", "Alto"]),
            "Nível do risco": st.column_config.TextColumn("🎯 Nível", disabled=True),
        },
        hide_index=True,
    )

    # Recalcular risco
    edited_risco["Nível do risco"] = edited_risco.apply(
        lambda row: nivel_risco(row["Probabilidade"], row["Impacto"]), axis=1
    )

    # Dashboard de Riscos
    st.markdown("---")
    st.markdown("## 📈 Dashboard de Riscos")
    
    # Métricas
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(edited_risco)}</div>
            <div class="metric-label">📊 Total de Riscos</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        qtd_alto = len(edited_risco[edited_risco["Nível do risco"] == "🔴 Alto"])
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color:#F44336;">{qtd_alto}</div>
            <div class="metric-label">🔴 Riscos Altos</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        qtd_medio = len(edited_risco[edited_risco["Nível do risco"] == "🟡 Médio"])
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color:#FFC107;">{qtd_medio}</div>
            <div class="metric-label">🟡 Riscos Médios</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        qtd_baixo = len(edited_risco[edited_risco["Nível do risco"] == "🟢 Baixo"])
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color:#4CAF50;">{qtd_baixo}</div>
            <div class="metric-label">🟢 Riscos Baixos</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Gráficos HTML
    col_graf1, col_graf2 = st.columns(2)
    
    with col_graf1:
        # Gráfico de distribuição por localidade
        st.markdown("### 📊 Riscos por Localidade")
        risco_local = edited_risco.groupby('Localidade').size().to_dict()
        
        if risco_local:
            max_valor = max(risco_local.values())
            for loc, qtd in risco_local.items():
                percentual = (qtd / max_valor) * 100
                st.markdown(f"""
                <div style='margin: 10px 0;'>
                    <div style='display: flex; justify-content: space-between;'>
                        <span>{loc[:30]}</span>
                        <span><strong>{qtd}</strong></span>
                    </div>
                    <div style='background-color: #e0e0e0; border-radius: 10px; overflow: hidden;'>
                        <div style='background-color: #1E88E5; width: {percentual}%; height: 25px;'></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with col_graf2:
        # Distribuição por nível de risco
        st.markdown("### 🎯 Distribuição por Nível")
        niveis = edited_risco['Nível do risco'].value_counts().to_dict()
        st.markdown(criar_grafico_barras(niveis, ""), unsafe_allow_html=True)
    
    # Tabela de resumo por localidade
    st.markdown("---")
    st.markdown("### 📍 Resumo por Localidade")
    resumo_local = edited_risco.groupby(['Localidade', 'Nível do risco']).size().unstack(fill_value=0)
    st.dataframe(resumo_local, use_container_width=True)

# ======================== TAB 2: GESTÃO DE EQUIPAMENTOS ========================
with tab2:
    st.markdown("## 🖥️ Gestão de Equipamentos de TI/OT")
    
    dados_equipamentos_inicial = pd.DataFrame({
        "Equipamento": ["Firewall Fortinet", "Switch Core Huawei", "Router Cisco", "Servidor Dell", "Storage EMC", "Access Point", "Patch Panel"],
        "Tipo": ["Segurança", "Rede", "Rede", "Servidor", "Storage", "Rede", "Infraestrutura"],
        "Localidade": ["Data Center - Rack 02", "Data Center - Rack 01", "Data Center - Rack 01", "Data Center - Rack 03", "Data Center - Rack 04", "Sala 210 - Teto", "Sala de servidores"],
        "Fabricante": ["Fortinet", "Huawei", "Cisco", "Dell", "EMC", "Ubiquiti", "Intelbras"],
        "Modelo": ["FG-100F", "S12700", "ISR 4321", "PowerEdge R750", "Unity XT 380", "U6-LR", "CAT6"],
        "Status": ["Ativo", "Ativo", "Ativo", "Ativo", "Ativo", "Ativo", "Ativo"],
    })
    
    edited_equipamentos = st.data_editor(
        dados_equipamentos_inicial,
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            "Equipamento": st.column_config.TextColumn("🖥️ Equipamento", required=True),
            "Tipo": st.column_config.SelectboxColumn("📂 Tipo", options=["Segurança", "Rede", "Servidor", "Storage", "Infraestrutura"]),
            "Localidade": st.column_config.TextColumn("📍 Localidade"),
            "Fabricante": st.column_config.TextColumn("🏭 Fabricante"),
            "Modelo": st.column_config.TextColumn("📟 Modelo"),
            "Status": st.column_config.SelectboxColumn("⚙️ Status", options=["Ativo", "Em Manutenção", "Desativado", "Reserva"]),
        },
        hide_index=True,
    )
    
    # Dashboard Equipamentos
    st.markdown("---")
    st.markdown("## 📊 Dashboard de Equipamentos")
    
    col_eq1, col_eq2, col_eq3, col_eq4 = st.columns(4)
    with col_eq1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(edited_equipamentos)}</div>
            <div class="metric-label">📦 Total Equipamentos</div>
        </div>
        """, unsafe_allow_html=True)
    with col_eq2:
        ativos = len(edited_equipamentos[edited_equipamentos["Status"] == "Ativo"])
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color:#4CAF50;">{ativos}</div>
            <div class="metric-label">✅ Equipamentos Ativos</div>
        </div>
        """, unsafe_allow_html=True)
    with col_eq3:
        seguranca = len(edited_equipamentos[edited_equipamentos["Tipo"] == "Segurança"])
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color:#1E88E5;">{seguranca}</div>
            <div class="metric-label">🔒 Equipamentos Segurança</div>
        </div>
        """, unsafe_allow_html=True)
    with col_eq4:
        fabricantes = edited_equipamentos["Fabricante"].nunique()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{fabricantes}</div>
            <div class="metric-label">🏭 Fabricantes</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Gráficos
    col_eq_graf1, col_eq_graf2 = st.columns(2)
    
    with col_eq_graf1:
        st.markdown("### 📊 Equipamentos por Tipo")
        tipo_count = edited_equipamentos["Tipo"].value_counts().to_dict()
        st.markdown(criar_grafico_barras(tipo_count, ""), unsafe_allow_html=True)
    
    with col_eq_graf2:
        st.markdown("### 📍 Top Localidades")
        local_count = edited_equipamentos["Localidade"].value_counts().head(5).to_dict()
        if local_count:
            max_local = max(local_count.values())
            for loc, qtd in local_count.items():
                percentual = (qtd / max_local) * 100
                st.markdown(f"""
                <div style='margin: 10px 0;'>
                    <div style='display: flex; justify-content: space-between;'>
                        <span>{loc[:25]}</span>
                        <span><strong>{qtd}</strong></span>
                    </div>
                    <div style='background-color: #e0e0e0; border-radius: 10px; overflow: hidden;'>
                        <div style='background-color: #FF9800; width: {percentual}%; height: 25px;'></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ======================== TAB 3: PDCA ========================
with tab3:
    st.markdown("## 🔄 PDCA de Controle de Acesso")
    
    colunas_pdca = [
        {"nome": "1. Contexto (P)", "cor": "#1E88E5", "desc": "Análise do ambiente"},
        {"nome": "2. Liderança (P)", "cor": "#1E88E5", "desc": "Comprometimento"},
        {"nome": "3. Planejamento (P)", "cor": "#1E88E5", "desc": "Objetivos e riscos"},
        {"nome": "4. Suporte (D)", "cor": "#E53935", "desc": "Recursos"},
        {"nome": "5. Operação (D)", "cor": "#E53935", "desc": "Controles"},
        {"nome": "6. Avaliação (C)", "cor": "#43A047", "desc": "Monitoramento"},
        {"nome": "7. Melhoria (A)", "cor": "#FB8C00", "desc": "Ações corretivas"}
    ]
    
    linhas_pdca = [
        "🎯 Objetivo Estratégico",
        "⚙️ Ação Técnica (TI/OT)",
        "📊 Indicador (KPI)",
        "🚩 Evidência / Status"
    ]
    
    cols = st.columns(len(colunas_pdca), gap="small")
    dados_pdca = {}
    
    for i, col_info in enumerate(colunas_pdca):
        with cols[i]:
            st.markdown(f"""
                <div class="pdca-header" style="background-color: {col_info['cor']}; color: white;">
                    <div>
                        <strong>{col_info['nome']}</strong><br>
                        <small style="font-size: 10px;">{col_info['desc']}</small>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            for j, linha in enumerate(linhas_pdca):
                if i == 0:
                    st.markdown(f"""
                        <div class="row-title" style="border-left-color: {col_info['cor']};">
                            <strong>{linha}</strong>
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
                    height=100
                )
                dados_pdca[(i, j)] = valor
                st.markdown("<div style='margin-bottom: 5px;'></div>", unsafe_allow_html=True)
    
    # Botões
    st.markdown("---")
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        if st.button("🖨️ Imprimir Relatório", use_container_width=True):
            risco_html = edited_risco.to_html(index=False)
            equip_html = edited_equipamentos.to_html(index=False)
            
            pdca_html = "<table border='1' style='width:100%;'>"
            pdca_html += "<tr>"
            for col in colunas_pdca:
                pdca_html += f"<th style='background:{col['cor']}; color:white;'>{col['nome']}</th>"
            pdca_html += "</tr>"
            for j in range(len(linhas_pdca)):
                pdca_html += "<tr>"
                for i in range(len(colunas_pdca)):
                    conteudo = dados_pdca.get((i, j), "").replace("\n", "<br>")
                    pdca_html += f"<td><b>{linhas_pdca[j]}</b><br>{conteudo or '—'}</td>"
                pdca_html += "</tr>"
            pdca_html += "</table>"
            
            html_completo = f"""
            <html>
            <head><style>body{{font-family:Arial;margin:20px;}} table{{border-collapse:collapse;width:100%;}} th,td{{border:1px solid #aaa;padding:8px;}}</style></head>
            <body>
                <h1>Relatório de Segurança</h1>
                <p>Usuário: {st.session_state.usuario} | Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
                <h2>Análise de Risco</h2>{risco_html}
                <h2>Equipamentos</h2>{equip_html}
                <h2>PDCA</h2>{pdca_html}
                <script>window.onload=function(){{window.print();}}</script>
            </body>
            </html>
            """
            st.components.v1.html(html_completo, height=500)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/security-checked--v1.png", width=80)
    st.markdown(f"### 👤 {st.session_state.usuario}")
    st.markdown("---")
    
    st.markdown("### 🎯 Riscos")
    st.markdown(f"- 🔴 Alto: {len(edited_risco[edited_risco['Nível do risco'] == '🔴 Alto'])}")
    st.markdown(f"- 🟡 Médio: {len(edited_risco[edited_risco['Nível do risco'] == '🟡 Médio'])}")
    st.markdown(f"- 🟢 Baixo: {len(edited_risco[edited_risco['Nível do risco'] == '🟢 Baixo'])}")
    
    st.markdown("---")
    st.markdown(f"🕐 {datetime.now().strftime('%H:%M:%S')}")

st.success("✅ Sistema funcionando sem plotly! Todos os gráficos são nativos.")
