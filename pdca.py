import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    layout="wide",
    page_title="SecureOps — Gestão de Segurança",
    page_icon="🛡️",
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────
# AUTH
# ──────────────────────────────────────────────
def verificar_login():
    if 'autenticado' not in st.session_state:
        st.session_state.autenticado = False
    return st.session_state.autenticado

def fazer_login(username, password):
    if username == "Juan" and password == "Ju@n1990":
        st.session_state.autenticado = True
        st.session_state.usuario = username
        return True
    return False

def fazer_logout():
    st.session_state.autenticado = False
    st.session_state.usuario = ""
    st.rerun()

# ──────────────────────────────────────────────
# CSS OTIMIZADO - SIDEBAR MAIS CLARA
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    font-size: 14px;
    color: #1e293b;
}

[data-testid="stAppViewContainer"] { background: #f8fafc; }
[data-testid="stSidebar"] { background: #f1f5f9 !important; border-right: 1px solid #e2e8f0 !important; }

.block-container { padding: 1.5rem 2rem 2rem !important; max-width: 100% !important; }

/* SIDEBAR MAIS CLARA */
.sb-logo { font-size: 20px; font-weight: 700; color: #0f172a; letter-spacing: -0.3px; padding: 1rem 0 0.2rem; }
.sb-sub  { font-size: 11px; color: #64748b; margin-bottom: 0.8rem; }
.sb-div  { border: none; border-top: 1px solid #e2e8f0; margin: 0.8rem 0; }
.sb-lbl  { font-size: 10px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; color: #64748b; margin-bottom: 0.4rem; }
.sb-user { font-size: 14px; font-weight: 600; color: #0f172a; margin-bottom: 2px; }
.sb-role { font-size: 11px; color: #64748b; }
.sb-badge { display: flex; align-items: center; justify-content: space-between; padding: 8px 12px; border-radius: 8px; margin-bottom: 6px; font-size: 13px; font-weight: 500; }
.sb-red    { background: #fee2e2; color: #dc2626; }
.sb-yellow { background: #fef3c7; color: #d97706; }
.sb-green  { background: #dcfce7; color: #16a34a; }
.sb-num { font-size: 18px; font-weight: 700; }
.sb-time { font-size: 10px; color: #64748b; margin-top: 1rem; }

/* TABS */
.stTabs [data-baseweb="tab-list"] {
    gap: 0; background: #e2e8f0; padding: 4px;
    border-radius: 10px; width: fit-content;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 7px; padding: 6px 20px;
    font-size: 13px; font-weight: 500;
    color: #64748b; background: transparent;
}
.stTabs [aria-selected="true"] {
    background: #fff; color: #0f172a;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 1.5rem; }

/* TÍTULOS PADRONIZADOS */
.page-title { font-size: 24px; font-weight: 700; color: #0f172a; letter-spacing: -0.3px; margin-bottom: 4px; }
.page-sub   { font-size: 13px; color: #64748b; margin-bottom: 1.2rem; }

.sec-title {
    font-size: 11px; font-weight: 600; text-transform: uppercase;
    letter-spacing: 1px; color: #94a3b8;
    margin: 1.5rem 0 0.8rem;
    border-bottom: 1px solid #e2e8f0; padding-bottom: 6px;
}

/* METRIC CARDS */
.mcard { background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px 16px 12px; }
.mcard-num { font-size: 32px; font-weight: 700; letter-spacing: -1px; line-height: 1; margin-bottom: 4px; }
.mcard-lbl { font-size: 12px; font-weight: 500; color: #64748b; }
.c-blue   { color: #2563eb; }
.c-red    { color: #dc2626; }
.c-yellow { color: #d97706; }
.c-green  { color: #16a34a; }
.c-gray   { color: #475569; }

/* CHART CARDS */
.chart-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 18px; margin-bottom: 16px; }
.chart-title { font-size: 14px; font-weight: 600; color: #1e293b; margin-bottom: 16px; border-left: 3px solid #2563eb; padding-left: 10px; }
.sbar-wrap { margin-bottom: 12px; }
.sbar-label { font-size: 12px; font-weight: 500; color: #334155; margin-bottom: 4px; display: flex; justify-content: space-between; }
.sbar-track { height: 32px; border-radius: 6px; background: #f1f5f9; overflow: hidden; display: flex; }
.sbar-seg { height: 100%; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 600; color: #fff; min-width: 24px; }
.legend-row { display: flex; gap: 16px; margin-top: 16px; flex-wrap: wrap; padding-top: 12px; border-top: 1px solid #e2e8f0; }
.legend-dot { display: flex; align-items: center; gap: 6px; font-size: 12px; color: #475569; }
.ldot { width: 10px; height: 10px; border-radius: 3px; }

/* PDCA */
.pdca-header { border-radius: 8px; padding: 8px 6px; text-align: center; margin-bottom: 8px; }
.pdca-row-lbl { font-size: 12px; font-weight: 600; color: #475569; padding: 6px 0 3px; border-bottom: 1px solid #e2e8f0; margin: 4px 0 3px; }

/* INPUTS */
textarea {
    border-radius: 8px !important; border: 1px solid #e2e8f0 !important;
    font-size: 12px !important; font-family: 'Inter', sans-serif !important;
    background: #fff !important;
}
textarea:focus { border-color: #2563eb !important; box-shadow: 0 0 0 2px rgba(37,99,235,0.1) !important; }

/* DATA EDITOR */
.stDataFrame { font-size: 12px !important; }
[data-testid="stDataFrame"] table { font-size: 12px !important; }

/* BUTTON */
.stButton > button {
    background: #0f172a !important; color: #fff !important;
    border: none !important; border-radius: 8px !important;
    font-size: 13px !important; font-weight: 500 !important;
}
.stButton > button:hover { background: #1e293b !important; }

hr { border: none; border-top: 1px solid #e2e8f0 !important; margin: 0.8rem 0; }

/* GRID PARA GRÁFICOS */
.chart-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
    gap: 20px;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# LOGIN
# ──────────────────────────────────────────────
if not verificar_login():
    _, col, _ = st.columns([1, 1.3, 1])
    with col:
        st.markdown("<div style='height:50px'></div>", unsafe_allow_html=True)
        st.markdown("<div class='page-title' style='text-align:center'>🛡️ SecureOps</div>", unsafe_allow_html=True)
        st.markdown("<div class='page-sub' style='text-align:center'>Sistema de Gestão de Segurança</div>", unsafe_allow_html=True)
        st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)
        with st.form("login_form"):
            username = st.text_input("Usuário", placeholder="Digite seu usuário")
            password = st.text_input("Senha", type="password", placeholder="Digite sua senha")
            submit = st.form_submit_button("Entrar", use_container_width=True)
            if submit:
                if fazer_login(username, password):
                    st.success("Bem-vindo!")
                    st.rerun()
                else:
                    st.error("Usuário ou senha inválidos.")
        st.markdown("<p style='text-align:center;font-size:11px;color:#94a3b8;margin-top:10px;'>Usuário: Juan | Senha: Ju@n1990</p>", unsafe_allow_html=True)
    st.stop()

# ──────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────
def nivel_risco(prob, imp):
    prob = str(prob).lower().strip()
    imp = str(imp).lower().strip()
    if (prob == "baixa" and imp in ["baixo", "médio"]) or (prob == "média" and imp == "baixo"):
        return "🟢 Baixo"
    elif (prob == "baixa" and imp == "alto") or (prob == "média" and imp == "médio") or (prob == "alta" and imp == "baixo"):
        return "🟡 Médio"
    else:
        return "🔴 Alto"

CORES_RISCO = {"🔴 Alto": "#dc2626", "🟡 Médio": "#d97706", "🟢 Baixo": "#16a34a"}
CORES_TIPO = {"Segurança": "#2563eb", "Rede": "#7c3aed", "Servidor": "#0891b2", "Storage": "#059669", "Infraestrutura": "#d97706"}
CORES_STATUS = {"Ativo": "#16a34a", "Em Manutenção": "#d97706", "Desativado": "#dc2626", "Reserva": "#64748b"}

def stacked_bar(df, title, cores, col_group, col_stack):
    """Gera gráfico de barras empilhadas"""
    if df.empty:
        return "<div class='chart-card'>Sem dados para exibir</div>"
    
    pivot = df.groupby([col_group, col_stack]).size().unstack(fill_value=0)
    cats = list(pivot.columns)
    tmax = pivot.sum(axis=1).max() or 1

    # Construir legenda
    legend_items = []
    for c in cats:
        cor = cores.get(c, "#94a3b8")
        legend_items.append(f"<div class='legend-dot'><div class='ldot' style='background:{cor};'></div>{c}</div>")
    legend = "".join(legend_items)

    bars = ""
    for idx, row in pivot.iterrows():
        total = row.sum() or 1
        segs = ""
        for cat in cats:
            val = row.get(cat, 0)
            pct = (val / total) * 100
            cor = cores.get(cat, "#94a3b8")
            if pct > 0:
                segs += f"<div class='sbar-seg' style='width:{pct}%;background:{cor};' title='{cat}: {val}'>{val if pct > 8 else ''}</div>"
        w = max((total / tmax) * 100, 10)
        bars += f"""
        <div class='sbar-wrap'>
            <div class='sbar-label'>
                <span>{str(idx)[:40]}</span>
                <span style='font-weight:600;color:#0f172a'>{int(total)}</span>
            </div>
            <div class='sbar-track' style='width:{w}%'>{segs}</div>
        </div>"""

    return f"<div class='chart-card'><div class='chart-title'>{title}</div>{bars}<div class='legend-row'>{legend}</div></div>"

def mcard(num, lbl, cor):
    return f"<div class='mcard'><div class='mcard-num {cor}'>{num}</div><div class='mcard-lbl'>{lbl}</div></div>"

def sec(t):
    st.markdown(f"<div class='sec-title'>{t}</div>", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# SIDEBAR MAIS CLARA
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class='sb-logo'>🛡️ SecureOps</div>
    <div class='sb-sub'>Gestão de Segurança</div>
    <hr class='sb-div'>
    <div class='sb-lbl'>Usuário</div>
    """, unsafe_allow_html=True)
    st.markdown(f"<div class='sb-user'>{st.session_state.usuario}</div>", unsafe_allow_html=True)
    st.markdown("<div class='sb-role'>Administrador</div>", unsafe_allow_html=True)
    st.markdown("<hr class='sb-div'>", unsafe_allow_html=True)
    st.markdown("<div class='sb-lbl'>Resumo de Riscos</div>", unsafe_allow_html=True)
    sidebar_ph = st.empty()
    st.markdown("<hr class='sb-div'>", unsafe_allow_html=True)
    
    # Navegação rápida
    st.markdown("<div class='sb-lbl'>Navegação</div>", unsafe_allow_html=True)
    st.markdown("📊 Dados", unsafe_allow_html=True)
    st.markdown("📈 Gráficos", unsafe_allow_html=True)
    st.markdown("🔄 PDCA", unsafe_allow_html=True)
    st.markdown("<hr class='sb-div'>", unsafe_allow_html=True)
    
    if st.button("Encerrar Sessão", use_container_width=True):
        fazer_logout()
    st.markdown(f"<div class='sb-time'>🕐 {datetime.now().strftime('%d/%m/%Y %H:%M')}</div>", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# CABEÇALHO
# ──────────────────────────────────────────────
st.markdown(f"""
<div class='page-title'>SecureOps - Gestão de Segurança</div>
<div class='page-sub'>PDCA + Análise de Risco · {datetime.now().strftime('%d/%m/%Y')}</div>
""", unsafe_allow_html=True)

# Criar abas: Dados, Gráficos, PDCA
tab_dados, tab_graficos, tab_pdca = st.tabs(["📋 Dados", "📊 Gráficos", "🔄 PDCA"])

# ══════════════════════════════════════════════
# TAB DADOS
# ══════════════════════════════════════════════
with tab_dados:
    st.markdown("### 📋 Gestão de Dados")
    
    # Dados de Risco
    sec("Análise de Risco")
    dados_risco = pd.DataFrame({
        "Ativo": ["Cabos na sala de servidores", "Pen drive ou HD", "Servidor de internet",
                  "Switch de borda", "Firewall", "Router core"],
        "Localidade": ["Sala de servidores - Bloco A", "TI - Sala 210", "Data Center - Rack 05",
                       "Sala de rede - Andar 3", "Data Center - Rack 02", "Data Center - Rack 01"],
        "Ameaça": ["Rompimento", "Contaminação por vírus", "Invasão externa",
                   "Desligamento acidental", "Ataque DDoS", "Configuração errada"],
        "Vulnerabilidade": ["Cabos fora de dutos", "Antivírus desatualizado",
                            "Internet ligada direto na rede interna", "Sem trava física no rack",
                            "Firmware desatualizado", "Senha fraca"],
        "Probabilidade": ["Baixa", "Alta", "Média", "Média", "Baixa", "Média"],
        "Impacto": ["Alto", "Alto", "Alto", "Médio", "Alto", "Alto"],
    })
    dados_risco["Nível do Risco"] = dados_risco.apply(lambda r: nivel_risco(r["Probabilidade"], r["Impacto"]), axis=1)

    edited_risco = st.data_editor(
        dados_risco, use_container_width=True, num_rows="dynamic",
        column_config={
            "Ativo": st.column_config.TextColumn("Ativo", required=True),
            "Localidade": st.column_config.TextColumn("Localidade"),
            "Ameaça": st.column_config.TextColumn("Ameaça"),
            "Vulnerabilidade": st.column_config.TextColumn("Vulnerabilidade"),
            "Probabilidade": st.column_config.SelectboxColumn("Probabilidade", options=["Baixa", "Média", "Alta"]),
            "Impacto": st.column_config.SelectboxColumn("Impacto", options=["Baixo", "Médio", "Alto"]),
            "Nível do Risco": st.column_config.TextColumn("Nível", disabled=True),
        }, hide_index=True,
    )
    edited_risco["Nível do Risco"] = edited_risco.apply(lambda r: nivel_risco(r["Probabilidade"], r["Impacto"]), axis=1)

    # Dados de Equipamentos
    sec("Inventário de Equipamentos")
    dados_eq = pd.DataFrame({
        "Equipamento": ["Firewall Fortinet", "Switch Core Huawei", "Router Cisco", "Servidor Dell",
                        "Storage EMC", "Access Point", "Patch Panel"],
        "Tipo": ["Segurança", "Rede", "Rede", "Servidor", "Storage", "Rede", "Infraestrutura"],
        "Localidade": ["Data Center - Rack 02", "Data Center - Rack 01", "Data Center - Rack 01",
                       "Data Center - Rack 03", "Data Center - Rack 04", "Sala 210 - Teto", "Sala de servidores"],
        "Fabricante": ["Fortinet", "Huawei", "Cisco", "Dell", "EMC", "Ubiquiti", "Intelbras"],
        "Modelo": ["FG-100F", "S12700", "ISR 4321", "PowerEdge R750", "Unity XT 380", "U6-LR", "CAT6"],
        "Status": ["Ativo", "Ativo", "Ativo", "Ativo", "Ativo", "Ativo", "Ativo"],
        "Motivo": ["", "", "", "", "", "", ""],
    })

    edited_eq = st.data_editor(
        dados_eq, use_container_width=True, num_rows="dynamic",
        column_config={
            "Equipamento": st.column_config.TextColumn("Equipamento", required=True),
            "Tipo": st.column_config.SelectboxColumn("Tipo", options=["Segurança", "Rede", "Servidor", "Storage", "Infraestrutura"]),
            "Localidade": st.column_config.TextColumn("Localidade"),
            "Fabricante": st.column_config.TextColumn("Fabricante"),
            "Modelo": st.column_config.TextColumn("Modelo"),
            "Status": st.column_config.SelectboxColumn("Status", options=["Ativo", "Em Manutenção", "Desativado", "Reserva"]),
            "Motivo": st.column_config.TextColumn("Motivo / Observação"),
        }, hide_index=True,
    )

    # Métricas
    sec("Indicadores")
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.markdown(mcard(len(edited_risco), "Total Riscos", "c-blue"), unsafe_allow_html=True)
    with col2: st.markdown(mcard(len(edited_eq), "Equipamentos", "c-green"), unsafe_allow_html=True)
    with col3: 
        ativos_eq = len(edited_eq[edited_eq["Status"] == "Ativo"])
        st.markdown(mcard(ativos_eq, "Equipamentos Ativos", "c-green"), unsafe_allow_html=True)
    with col4:
        risco_alto = len(edited_risco[edited_risco["Nível do Risco"] == "🔴 Alto"])
        st.markdown(mcard(risco_alto, "Riscos Críticos", "c-red"), unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB GRÁFICOS - PÁGINA EXCLUSIVA PARA GRÁFICOS
# ══════════════════════════════════════════════
with tab_graficos:
    st.markdown("### 📊 Dashboard de Gráficos")
    st.markdown("<div class='page-sub'>Análise visual de riscos, localidades e equipamentos</div>", unsafe_allow_html=True)
    
    # Métricas rápidas
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.markdown(mcard(len(edited_risco), "Total Riscos", "c-blue"), unsafe_allow_html=True)
    with col_m2:
        risco_alto = len(edited_risco[edited_risco["Nível do Risco"] == "🔴 Alto"])
        st.markdown(mcard(risco_alto, "Riscos Altos", "c-red"), unsafe_allow_html=True)
    with col_m3:
        total_eq = len(edited_eq)
        st.markdown(mcard(total_eq, "Total Equipamentos", "c-green"), unsafe_allow_html=True)
    with col_m4:
        localidades = edited_risco["Localidade"].nunique()
        st.markdown(mcard(localidades, "Localidades", "c-gray"), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # GRÁFICO 1: Riscos por Localidade
    st.markdown(stacked_bar(edited_risco, "📍 Riscos por Localidade (Distribuição por Nível)", CORES_RISCO, "Localidade", "Nível do Risco"), unsafe_allow_html=True)
    
    # GRÁFICO 2: Riscos por Probabilidade
    st.markdown(stacked_bar(edited_risco, "📊 Riscos por Probabilidade", CORES_RISCO, "Probabilidade", "Nível do Risco"), unsafe_allow_html=True)
    
    # GRÁFICO 3: Equipamentos por Localidade
    st.markdown(stacked_bar(edited_eq, "🏢 Equipamentos por Localidade (Distribuição por Tipo)", CORES_TIPO, "Localidade", "Tipo"), unsafe_allow_html=True)
    
    # GRÁFICO 4: Equipamentos por Tipo e Status
    st.markdown(stacked_bar(edited_eq, "⚙️ Equipamentos por Tipo (Status)", CORES_STATUS, "Tipo", "Status"), unsafe_allow_html=True)
    
    # GRÁFICO 5: Equipamentos por Fabricante
    if len(edited_eq) > 0:
        st.markdown("### 🏭 Equipamentos por Fabricante")
        fabricante_count = edited_eq["Fabricante"].value_counts().to_dict()
        if fabricante_count:
            max_fab = max(fabricante_count.values()) or 1
            fab_html = "<div class='chart-card'><div class='chart-title'>Distribuição por Fabricante</div>"
            for fab, qtd in fabricante_count.items():
                percentual = (qtd / max_fab) * 100
                fab_html += f"""
                <div class='sbar-wrap'>
                    <div class='sbar-label'>
                        <span>{fab}</span>
                        <span style='font-weight:600;color:#0f172a'>{qtd}</span>
                    </div>
                    <div class='sbar-track' style='width:{percentual}%'>
                        <div class='sbar-seg' style='width:100%;background:#7c3aed;'>{qtd if percentual > 8 else ''}</div>
                    </div>
                </div>"""
            fab_html += "</div>"
            st.markdown(fab_html, unsafe_allow_html=True)
    
    # GRÁFICO 6: Resumo Geral
    st.markdown("### 📈 Resumo Geral")
    col_res1, col_res2 = st.columns(2)
    with col_res1:
        # Distribuição de riscos
        risco_count = edited_risco["Nível do Risco"].value_counts().to_dict()
        risco_html = "<div class='chart-card'><div class='chart-title'>Distribuição de Riscos</div>"
        for nivel, qtd in risco_count.items():
            cor = CORES_RISCO.get(nivel, "#94a3b8")
            percentual = (qtd / len(edited_risco)) * 100 if len(edited_risco) > 0 else 0
            risco_html += f"""
            <div class='sbar-wrap'>
                <div class='sbar-label'>
                    <span>{nivel}</span>
                    <span style='font-weight:600;color:#0f172a'>{qtd} ({percentual:.0f}%)</span>
                </div>
                <div class='sbar-track' style='width:100%'>
                    <div class='sbar-seg' style='width:{percentual}%;background:{cor};'>{percentual:.0f}%</div>
                </div>
            </div>"""
        risco_html += "</div>"
        st.markdown(risco_html, unsafe_allow_html=True)
    
    with col_res2:
        # Status dos equipamentos
        status_count = edited_eq["Status"].value_counts().to_dict()
        status_html = "<div class='chart-card'><div class='chart-title'>Status dos Equipamentos</div>"
        for status, qtd in status_count.items():
            cor = CORES_STATUS.get(status, "#94a3b8")
            percentual = (qtd / len(edited_eq)) * 100 if len(edited_eq) > 0 else 0
            status_html += f"""
            <div class='sbar-wrap'>
                <div class='sbar-label'>
                    <span>{status}</span>
                    <span style='font-weight:600;color:#0f172a'>{qtd} ({percentual:.0f}%)</span>
                </div>
                <div class='sbar-track' style='width:100%'>
                    <div class='sbar-seg' style='width:{percentual}%;background:{cor};'>{percentual:.0f}%</div>
                </div>
            </div>"""
        status_html += "</div>"
        st.markdown(status_html, unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB PDCA
# ══════════════════════════════════════════════
with tab_pdca:
    st.markdown("### 🔄 PDCA de Controle de Acesso")

    fases = [
        {"nome": "1. Contexto", "fase": "PLAN", "cor": "#2563eb"},
        {"nome": "2. Liderança", "fase": "PLAN", "cor": "#2563eb"},
        {"nome": "3. Planejamento", "fase": "PLAN", "cor": "#2563eb"},
        {"nome": "4. Suporte", "fase": "DO", "cor": "#d97706"},
        {"nome": "5. Operação", "fase": "DO", "cor": "#d97706"},
        {"nome": "6. Avaliação", "fase": "CHECK", "cor": "#16a34a"},
        {"nome": "7. Melhoria", "fase": "ACT", "cor": "#7c3aed"},
    ]
    linhas = [
        "🎯 Objetivo Estratégico",
        "⚙️ Ação Técnica",
        "📊 Indicador (KPI)",
        "🚩 Evidência / Status",
    ]

    cols = st.columns(len(fases), gap="small")
    dados_pdca = {}

    for i, (col, f) in enumerate(zip(cols, fases)):
        with col:
            st.markdown(f"""
            <div class='pdca-header' style='background:{f["cor"]}10;border:1px solid {f["cor"]}30;'>
                <div style='font-size:9px;font-weight:600;letter-spacing:1px;color:{f["cor"]};text-transform:uppercase;'>{f["fase"]}</div>
                <div style='font-size:12px;font-weight:600;color:{f["cor"]};margin-top:2px;'>{f["nome"]}</div>
            </div>
            """, unsafe_allow_html=True)
            for j, linha in enumerate(linhas):
                if i == 0:
                    st.markdown(f"<div class='pdca-row-lbl'>{linha}</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='height:34px;'></div>", unsafe_allow_html=True)
                dados_pdca[(i, j)] = st.text_area(
                    label="", key=f"p_{i}_{j}",
                    placeholder="Registre...",
                    label_visibility="collapsed",
                    height=85,
                )

    st.markdown("<br>", unsafe_allow_html=True)
    col_b, _, _ = st.columns([1.5, 3, 1.5])
    with col_b:
        if st.button("🖨️ Gerar Relatório Completo", use_container_width=True):
            r_html = edited_risco.to_html(index=False)
            e_html = edited_eq.to_html(index=False)
            p_html = "<table style='width:100%;border-collapse:collapse;font-size:12px;'>"
            p_html += "<tr>" + "".join(
                f"<th style='background:{f['cor']};color:#fff;padding:8px;'>{f['nome']}</th>"
                for f in fases) + "</tr>"
            for j in range(len(linhas)):
                p_html += "<tr>" + "".join(
                    f"<td style='padding:8px;vertical-align:top;border:1px solid #e2e8f0;'><b>{linhas[j]}</b><br>{dados_pdca.get((i,j),'').replace(chr(10),'<br>') or '—'}</td>"
                    for i in range(len(fases))) + "</tr>"
            p_html += "</table>"
            
            html_full = f"""<html><head><style>
            body{{font-family:'Inter',Arial;margin:30px;font-size:13px;}}
            h1{{font-size:20px;}} h2{{font-size:14px;margin:20px 0 8px;color:#2563eb;border-bottom:2px solid #e2e8f0;padding-bottom:4px;}}
            table{{border-collapse:collapse;width:100%;margin-bottom:20px;}}
            th,td{{border:1px solid #cbd5e1;padding:6px 8px;}}
            th{{background:#0f172a;color:#fff;}}
            </style></head><body>
            <h1>Relatório de Gestão de Segurança</h1>
            <p style='color:#64748b;font-size:11px;'>Gerado por: {st.session_state.usuario} · {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
            <h2>Análise de Risco</h2>{r_html}
            <h2>Equipamentos TI/OT</h2>{e_html}
            <h2>PDCA</h2>{p_html}
            <script>window.onload=function(){{window.print();}}</script>
            </body></html>"""
            st.components.v1.html(html_full, height=500)

# ──────────────────────────────────────────────
# SIDEBAR - RISCOS (ATUALIZADO)
# ──────────────────────────────────────────────
with sidebar_ph:
    risco_alto = len(edited_risco[edited_risco["Nível do Risco"] == "🔴 Alto"])
    risco_medio = len(edited_risco[edited_risco["Nível do Risco"] == "🟡 Médio"])
    risco_baixo = len(edited_risco[edited_risco["Nível do Risco"] == "🟢 Baixo"])
    
    st.markdown(f"""
    <div class='sb-badge sb-red'>   <span>🔴 Alto</span>  <span class='sb-num'>{risco_alto}</span>  </div>
    <div class='sb-badge sb-yellow'><span>🟡 Médio</span> <span class='sb-num'>{risco_medio}</span> </div>
    <div class='sb-badge sb-green'> <span>🟢 Baixo</span> <span class='sb-num'>{risco_baixo}</span> </div>
    """, unsafe_allow_html=True)
