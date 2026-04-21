import streamlit as st
import pandas as pd
from datetime import datetime

# -------------------------------
# CONFIGURAÇÃO DA PÁGINA
# -------------------------------
st.set_page_config(
    layout="wide",
    page_title="SecureOps — Gestão de Segurança",
    page_icon="🛡️",
    initial_sidebar_state="expanded"
)

# -------------------------------
# SISTEMA DE AUTENTICAÇÃO
# -------------------------------
def verificar_login():
    if 'autenticado' not in st.session_state:
        st.session_state.autenticado = False
    return st.session_state.autenticado

def fazer_login(username, password):
    USUARIO_VALIDO = "Juan"
    SENHA_VALIDA = "Ju@n1990"
    if username == USUARIO_VALIDO and password == SENHA_VALIDA:
        st.session_state.autenticado = True
        st.session_state.usuario = username
        return True
    return False

def fazer_logout():
    st.session_state.autenticado = False
    st.session_state.usuario = ""
    st.rerun()

# -------------------------------
# CSS GLOBAL PROFISSIONAL
# -------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ─── RESET & BASE ─────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: #E2E8F0;
}

[data-testid="stAppViewContainer"] {
    background: #0A0E1A;
    background-image:
        radial-gradient(ellipse 80% 60% at 10% 0%, rgba(14,165,233,0.08) 0%, transparent 55%),
        radial-gradient(ellipse 60% 50% at 90% 100%, rgba(99,102,241,0.07) 0%, transparent 55%);
}

[data-testid="stSidebar"] {
    background: #0D1220 !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}

.block-container {
    padding: 1.5rem 2rem 2rem !important;
    max-width: 100% !important;
}

/* ─── SIDEBAR ───────────────────────────────────────────────── */
.sidebar-brand {
    display: flex; align-items: center; gap: 12px;
    padding: 1.2rem 0 1rem;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 1.2rem;
}
.sidebar-brand-icon {
    width: 42px; height: 42px;
    background: linear-gradient(135deg, #0EA5E9, #6366F1);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
}
.sidebar-brand-name {
    font-family: 'Syne', sans-serif;
    font-size: 18px; font-weight: 800;
    letter-spacing: -0.3px;
    color: #F1F5F9;
}
.sidebar-brand-sub {
    font-size: 10px; color: #64748B;
    letter-spacing: 0.8px; text-transform: uppercase;
    margin-top: 1px;
}

.sidebar-user {
    display: flex; align-items: center; gap: 10px;
    padding: 10px 12px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px; margin-bottom: 1rem;
}
.sidebar-avatar {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, #0EA5E9, #6366F1);
    border-radius: 8px; font-size: 16px;
    display: flex; align-items: center; justify-content: center;
}
.sidebar-username { font-size: 13px; font-weight: 600; color: #CBD5E1; }
.sidebar-role { font-size: 10px; color: #64748B; letter-spacing: 0.5px; }

.sidebar-section { margin: 1.2rem 0 0.4rem; }
.sidebar-section-label {
    font-size: 9px; font-weight: 700;
    letter-spacing: 1.5px; text-transform: uppercase;
    color: #475569; margin-bottom: 0.6rem;
}

.risk-stat {
    display: flex; align-items: center; justify-content: space-between;
    padding: 8px 12px;
    background: rgba(255,255,255,0.03);
    border-radius: 8px; margin-bottom: 6px;
    border: 1px solid rgba(255,255,255,0.05);
}
.risk-stat-label { font-size: 12px; color: #94A3B8; }
.risk-stat-badge {
    font-size: 12px; font-weight: 700;
    padding: 2px 9px; border-radius: 20px;
}
.badge-alto { background: rgba(239,68,68,0.15); color: #F87171; border: 1px solid rgba(239,68,68,0.25); }
.badge-medio { background: rgba(245,158,11,0.15); color: #FCD34D; border: 1px solid rgba(245,158,11,0.25); }
.badge-baixo { background: rgba(34,197,94,0.15); color: #4ADE80; border: 1px solid rgba(34,197,94,0.25); }

.sidebar-time {
    font-size: 11px; color: #475569;
    text-align: center; margin-top: 1.5rem;
    padding-top: 1rem;
    border-top: 1px solid rgba(255,255,255,0.06);
}

/* ─── TOPBAR ────────────────────────────────────────────────── */
.topbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 0 1.2rem;
    margin-bottom: 1rem;
    border-bottom: 1px solid rgba(255,255,255,0.07);
}
.topbar-title {
    font-family: 'Syne', sans-serif;
    font-size: 26px; font-weight: 800;
    letter-spacing: -0.5px; color: #F8FAFC;
    line-height: 1.1;
}
.topbar-title span { color: #0EA5E9; }
.topbar-meta { font-size: 12px; color: #475569; margin-top: 2px; }

/* ─── TABS ──────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: rgba(255,255,255,0.03) !important;
    padding: 5px !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    width: fit-content;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    padding: 8px 20px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    color: #64748B !important;
    background: transparent !important;
    border: none !important;
    font-family: 'DM Sans', sans-serif !important;
    letter-spacing: 0.2px;
    transition: all 0.2s ease;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #0EA5E9, #6366F1) !important;
    color: white !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding-top: 1.5rem !important;
}

/* ─── METRIC CARDS ──────────────────────────────────────────── */
.metric-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 20px 18px;
    position: relative; overflow: hidden;
    transition: border-color 0.2s ease;
}
.metric-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #0EA5E9, #6366F1);
    opacity: 0.7;
}
.metric-card:hover { border-color: rgba(14,165,233,0.2); }
.metric-icon {
    font-size: 22px; margin-bottom: 10px; display: block;
}
.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 34px; font-weight: 800;
    letter-spacing: -1px; color: #F8FAFC;
    line-height: 1;
}
.metric-label {
    font-size: 11px; font-weight: 600;
    letter-spacing: 1px; text-transform: uppercase;
    color: #475569; margin-top: 6px;
}
.metric-accent { color: #0EA5E9; }
.metric-accent-red { color: #F87171; }
.metric-accent-yellow { color: #FCD34D; }
.metric-accent-green { color: #4ADE80; }

/* ─── SECTION HEADERS ───────────────────────────────────────── */
.section-header {
    display: flex; align-items: center; gap: 10px;
    margin: 1.8rem 0 1rem;
}
.section-header-line {
    flex: 1; height: 1px;
    background: linear-gradient(90deg, rgba(14,165,233,0.3), transparent);
}
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 14px; font-weight: 700;
    letter-spacing: 1.5px; text-transform: uppercase;
    color: #94A3B8;
    white-space: nowrap;
}

/* ─── BAR CHARTS ────────────────────────────────────────────── */
.chart-container {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px; padding: 20px;
}
.chart-title {
    font-family: 'Syne', sans-serif;
    font-size: 13px; font-weight: 700;
    letter-spacing: 0.5px; color: #94A3B8;
    text-transform: uppercase; margin-bottom: 18px;
}
.bar-row { margin: 12px 0; }
.bar-label-row {
    display: flex; justify-content: space-between;
    margin-bottom: 5px;
}
.bar-label { font-size: 12px; color: #94A3B8; }
.bar-count { font-size: 12px; font-weight: 700; color: #E2E8F0; }
.bar-track {
    background: rgba(255,255,255,0.06);
    border-radius: 6px; overflow: hidden; height: 8px;
}
.bar-fill {
    height: 100%; border-radius: 6px;
    transition: width 0.6s ease;
}

/* ─── PDCA GRID ─────────────────────────────────────────────── */
.pdca-phase-header {
    border-radius: 10px; padding: 12px 8px;
    text-align: center; margin-bottom: 10px;
}
.pdca-phase-tag {
    font-size: 9px; font-weight: 700;
    letter-spacing: 2px; text-transform: uppercase;
    opacity: 0.75; margin-bottom: 3px;
}
.pdca-phase-name {
    font-family: 'Syne', sans-serif;
    font-size: 13px; font-weight: 700;
}
.pdca-phase-desc { font-size: 10px; opacity: 0.65; margin-top: 2px; }

.pdca-row-label {
    display: flex; align-items: center;
    padding: 10px 10px; margin: 4px 0 6px;
    background: rgba(255,255,255,0.03);
    border-radius: 8px;
    border-left: 3px solid #0EA5E9;
    font-size: 12px; font-weight: 600; color: #94A3B8;
    min-height: 54px;
}

/* ─── DATAFRAMES ────────────────────────────────────────────── */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}
[data-testid="stDataFrameResizable"] thead {
    background: rgba(14,165,233,0.08) !important;
}

/* ─── TEXTAREAS ─────────────────────────────────────────────── */
textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 8px !important;
    color: #CBD5E1 !important;
    font-size: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
    resize: none !important;
}
textarea:focus {
    border-color: rgba(14,165,233,0.5) !important;
    box-shadow: 0 0 0 2px rgba(14,165,233,0.12) !important;
}

/* ─── BUTTONS ───────────────────────────────────────────────── */
.stButton > button {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: #CBD5E1 !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important; font-size: 13px !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: rgba(14,165,233,0.12) !important;
    border-color: rgba(14,165,233,0.3) !important;
    color: #0EA5E9 !important;
}

/* ─── LOGIN ─────────────────────────────────────────────────── */
.login-wrap {
    min-height: 100vh; display: flex;
    align-items: center; justify-content: center;
}
.login-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px; padding: 40px 36px;
    width: 100%; max-width: 420px;
    box-shadow: 0 25px 60px rgba(0,0,0,0.5);
}
.login-logo {
    width: 56px; height: 56px;
    background: linear-gradient(135deg, #0EA5E9, #6366F1);
    border-radius: 14px; font-size: 26px;
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 20px;
}
.login-title {
    font-family: 'Syne', sans-serif;
    font-size: 22px; font-weight: 800;
    text-align: center; color: #F8FAFC;
    letter-spacing: -0.3px; margin-bottom: 4px;
}
.login-subtitle {
    font-size: 13px; color: #475569;
    text-align: center; margin-bottom: 28px;
}

/* ─── ALERTS & MESSAGES ─────────────────────────────────────── */
[data-testid="stSuccess"] {
    background: rgba(34,197,94,0.08) !important;
    border: 1px solid rgba(34,197,94,0.2) !important;
    border-radius: 10px !important;
}
[data-testid="stError"] {
    background: rgba(239,68,68,0.08) !important;
    border: 1px solid rgba(239,68,68,0.2) !important;
    border-radius: 10px !important;
}

/* ─── FORM INPUTS ───────────────────────────────────────────── */
[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 8px !important;
    color: #E2E8F0 !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: rgba(14,165,233,0.5) !important;
    box-shadow: 0 0 0 2px rgba(14,165,233,0.12) !important;
}

/* ─── SCROLLBAR ─────────────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: rgba(14,165,233,0.4); }

/* ─── DIVIDER ───────────────────────────────────────────────── */
hr { border: none; border-top: 1px solid rgba(255,255,255,0.07) !important; }

/* ─── MISC ──────────────────────────────────────────────────── */
.stMarkdown p { color: #94A3B8; }
[data-testid="stSelectbox"] select {
    background: rgba(255,255,255,0.04) !important;
}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# TELA DE LOGIN
# ──────────────────────────────────────────────
if not verificar_login():
    st.markdown("""
    <div style="display:flex;align-items:center;justify-content:center;min-height:80vh;">
        <div style="width:100%;max-width:400px;">
    """, unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns([1, 2.2, 1])
    with col_b:
        st.markdown("""
        <div style="
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 20px; padding: 40px 32px;
            box-shadow: 0 30px 70px rgba(0,0,0,0.5);
        ">
            <div style="
                width:54px;height:54px;
                background:linear-gradient(135deg,#0EA5E9,#6366F1);
                border-radius:13px;font-size:24px;
                display:flex;align-items:center;justify-content:center;
                margin:0 auto 18px;
            ">🛡️</div>
            <div style="
                font-family:'Syne',sans-serif;font-size:22px;
                font-weight:800;text-align:center;color:#F8FAFC;
                letter-spacing:-0.3px;margin-bottom:4px;
            ">SecureOps</div>
            <div style="font-size:12px;color:#475569;text-align:center;margin-bottom:28px;">
                Sistema de Gestão de Segurança da Informação
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            username = st.text_input("Usuário", placeholder="Digite seu usuário")
            password = st.text_input("Senha", type="password", placeholder="Digite sua senha")
            submit = st.form_submit_button("Entrar →", use_container_width=True)

            if submit:
                if fazer_login(username, password):
                    st.success(f"Bem-vindo, {username}!")
                    st.rerun()
                else:
                    st.error("Credenciais inválidas. Tente novamente.")

        st.markdown("<p style='text-align:center;font-size:11px;color:#334155;margin-top:16px;'>Usuário: Juan &nbsp;·&nbsp; Senha: Ju@n1990</p>", unsafe_allow_html=True)

    st.stop()

# ──────────────────────────────────────────────
# FUNÇÕES AUXILIARES
# ──────────────────────────────────────────────
def nivel_risco(prob, imp):
    prob = str(prob).lower().strip()
    imp = str(imp).lower().strip()
    if (prob == "baixa" and imp in ["baixo","médio"]) or (prob == "média" and imp == "baixo"):
        return "🟢 Baixo"
    elif (prob == "baixa" and imp == "alto") or (prob == "média" and imp == "médio") or (prob == "alta" and imp == "baixo"):
        return "🟡 Médio"
    else:
        return "🔴 Alto"

def bar_chart_html(dados, title="", palette=None):
    if not dados:
        return "<p style='color:#475569;font-size:13px;'>Sem dados.</p>"
    max_v = max(dados.values()) if dados.values() else 1
    html = f"<div class='chart-container'><div class='chart-title'>{title}</div>"
    default_colors = ["#0EA5E9", "#6366F1", "#F59E0B", "#10B981", "#F87171"]
    for idx, (label, val) in enumerate(dados.items()):
        pct = (val / max_v) * 100
        if palette:
            cor = "#F87171" if "Alto" in label else "#FCD34D" if "Médio" in label else "#4ADE80"
        else:
            cor = default_colors[idx % len(default_colors)]
        html += f"""
        <div class='bar-row'>
            <div class='bar-label-row'>
                <span class='bar-label'>{label[:36]}</span>
                <span class='bar-count'>{val}</span>
            </div>
            <div class='bar-track'>
                <div class='bar-fill' style='width:{pct}%;background:{cor};'></div>
            </div>
        </div>"""
    html += "</div>"
    return html

def section_header(title):
    st.markdown(f"""
    <div class='section-header'>
        <span class='section-title'>{title}</span>
        <div class='section-header-line'></div>
    </div>
    """, unsafe_allow_html=True)

# ──────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div class='sidebar-brand'>
        <div class='sidebar-brand-icon'>🛡️</div>
        <div>
            <div class='sidebar-brand-name'>SecureOps</div>
            <div class='sidebar-brand-sub'>Gestão de Segurança</div>
        </div>
    </div>
    <div class='sidebar-user'>
        <div class='sidebar-avatar'>👤</div>
        <div>
            <div class='sidebar-username'>{st.session_state.usuario}</div>
            <div class='sidebar-role'>Administrador</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # placeholder — será preenchido após calcular os riscos
    sidebar_risk_placeholder = st.empty()

    if st.button("⎋  Encerrar Sessão", use_container_width=True):
        fazer_logout()

    st.markdown(f"<div class='sidebar-time'>🕐 {datetime.now().strftime('%d/%m/%Y  %H:%M')}</div>", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# TOPBAR
# ──────────────────────────────────────────────
st.markdown(f"""
<div class='topbar'>
    <div>
        <div class='topbar-title'>PDCA + <span>Análise de Risco</span></div>
        <div class='topbar-meta'>Segurança da Informação · {datetime.now().strftime('%A, %d de %B de %Y')}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# TABS
# ──────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["  📊  Análise de Risco  ", "  🖥️  Equipamentos  ", "  🔄  PDCA  "])

# ══════════════════════════════════════════════
# TAB 1 — ANÁLISE DE RISCO
# ══════════════════════════════════════════════
with tab1:
    section_header("Matriz de Risco")

    dados_risco_inicial = pd.DataFrame({
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
    dados_risco_inicial["Nível do Risco"] = dados_risco_inicial.apply(
        lambda r: nivel_risco(r["Probabilidade"], r["Impacto"]), axis=1)

    edited_risco = st.data_editor(
        dados_risco_inicial,
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            "Ativo":          st.column_config.TextColumn("🏷️ Ativo", required=True),
            "Localidade":     st.column_config.TextColumn("📍 Localidade"),
            "Ameaça":         st.column_config.TextColumn("⚠️ Ameaça"),
            "Vulnerabilidade":st.column_config.TextColumn("🔓 Vulnerabilidade"),
            "Probabilidade":  st.column_config.SelectboxColumn("📊 Probabilidade", options=["Baixa","Média","Alta"]),
            "Impacto":        st.column_config.SelectboxColumn("💥 Impacto", options=["Baixo","Médio","Alto"]),
            "Nível do Risco": st.column_config.TextColumn("🎯 Nível", disabled=True),
        },
        hide_index=True,
    )
    edited_risco["Nível do Risco"] = edited_risco.apply(
        lambda r: nivel_risco(r["Probabilidade"], r["Impacto"]), axis=1)

    qtd_alto  = len(edited_risco[edited_risco["Nível do Risco"] == "🔴 Alto"])
    qtd_medio = len(edited_risco[edited_risco["Nível do Risco"] == "🟡 Médio"])
    qtd_baixo = len(edited_risco[edited_risco["Nível do Risco"] == "🟢 Baixo"])

    section_header("Dashboard de Riscos")
    c1, c2, c3, c4 = st.columns(4)
    cards = [
        ("📋", str(len(edited_risco)), "Total de Riscos", "metric-accent"),
        ("🔴", str(qtd_alto),  "Riscos Críticos",  "metric-accent-red"),
        ("🟡", str(qtd_medio), "Riscos Médios",    "metric-accent-yellow"),
        ("🟢", str(qtd_baixo), "Riscos Baixos",    "metric-accent-green"),
    ]
    for col, (icon, val, label, accent) in zip([c1,c2,c3,c4], cards):
        with col:
            st.markdown(f"""
            <div class='metric-card'>
                <span class='metric-icon'>{icon}</span>
                <div class='metric-value {accent}'>{val}</div>
                <div class='metric-label'>{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    g1, g2 = st.columns(2)
    with g1:
        risco_local = edited_risco.groupby('Localidade').size().to_dict()
        st.markdown(bar_chart_html(risco_local, "Riscos por Localidade"), unsafe_allow_html=True)
    with g2:
        niveis = edited_risco['Nível do Risco'].value_counts().to_dict()
        st.markdown(bar_chart_html(niveis, "Distribuição por Nível de Risco", palette=True), unsafe_allow_html=True)

    section_header("Resumo por Localidade")
    resumo_local = edited_risco.groupby(['Localidade','Nível do Risco']).size().unstack(fill_value=0)
    st.dataframe(resumo_local, use_container_width=True)

# ══════════════════════════════════════════════
# TAB 2 — EQUIPAMENTOS
# ══════════════════════════════════════════════
with tab2:
    section_header("Inventário de Equipamentos TI/OT")

    dados_equipamentos_inicial = pd.DataFrame({
        "Equipamento": ["Firewall Fortinet","Switch Core Huawei","Router Cisco","Servidor Dell","Storage EMC","Access Point","Patch Panel"],
        "Tipo":        ["Segurança","Rede","Rede","Servidor","Storage","Rede","Infraestrutura"],
        "Localidade":  ["Data Center - Rack 02","Data Center - Rack 01","Data Center - Rack 01",
                        "Data Center - Rack 03","Data Center - Rack 04","Sala 210 - Teto","Sala de servidores"],
        "Fabricante":  ["Fortinet","Huawei","Cisco","Dell","EMC","Ubiquiti","Intelbras"],
        "Modelo":      ["FG-100F","S12700","ISR 4321","PowerEdge R750","Unity XT 380","U6-LR","CAT6"],
        "Status":      ["Ativo","Ativo","Ativo","Ativo","Ativo","Ativo","Ativo"],
    })

    edited_equipamentos = st.data_editor(
        dados_equipamentos_inicial,
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            "Equipamento": st.column_config.TextColumn("🖥️ Equipamento", required=True),
            "Tipo":        st.column_config.SelectboxColumn("📂 Tipo", options=["Segurança","Rede","Servidor","Storage","Infraestrutura"]),
            "Localidade":  st.column_config.TextColumn("📍 Localidade"),
            "Fabricante":  st.column_config.TextColumn("🏭 Fabricante"),
            "Modelo":      st.column_config.TextColumn("📟 Modelo"),
            "Status":      st.column_config.SelectboxColumn("⚙️ Status", options=["Ativo","Em Manutenção","Desativado","Reserva"]),
        },
        hide_index=True,
    )

    section_header("Dashboard de Equipamentos")
    ativos     = len(edited_equipamentos[edited_equipamentos["Status"] == "Ativo"])
    seguranca  = len(edited_equipamentos[edited_equipamentos["Tipo"] == "Segurança"])
    fabricantes = edited_equipamentos["Fabricante"].nunique()

    c1, c2, c3, c4 = st.columns(4)
    eq_cards = [
        ("📦", str(len(edited_equipamentos)), "Total de Equipamentos", "metric-accent"),
        ("✅", str(ativos),     "Equipamentos Ativos",    "metric-accent-green"),
        ("🔒", str(seguranca),  "Dispositivos de Segurança","metric-accent"),
        ("🏭", str(fabricantes),"Fabricantes",             ""),
    ]
    for col, (icon, val, label, accent) in zip([c1,c2,c3,c4], eq_cards):
        with col:
            st.markdown(f"""
            <div class='metric-card'>
                <span class='metric-icon'>{icon}</span>
                <div class='metric-value {accent}'>{val}</div>
                <div class='metric-label'>{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    g1, g2 = st.columns(2)
    with g1:
        tipo_count = edited_equipamentos["Tipo"].value_counts().to_dict()
        st.markdown(bar_chart_html(tipo_count, "Distribuição por Tipo"), unsafe_allow_html=True)
    with g2:
        local_count = edited_equipamentos["Localidade"].value_counts().head(6).to_dict()
        st.markdown(bar_chart_html(local_count, "Top Localidades"), unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB 3 — PDCA
# ══════════════════════════════════════════════
with tab3:
    section_header("PDCA de Controle de Acesso")

    colunas_pdca = [
        {"nome": "Contexto",     "fase": "P — PLAN", "cor": "#0EA5E9", "desc": "Análise do ambiente"},
        {"nome": "Liderança",    "fase": "P — PLAN", "cor": "#0EA5E9", "desc": "Comprometimento"},
        {"nome": "Planejamento", "fase": "P — PLAN", "cor": "#0EA5E9", "desc": "Objetivos e riscos"},
        {"nome": "Suporte",      "fase": "D — DO",   "cor": "#F59E0B", "desc": "Recursos e comunicação"},
        {"nome": "Operação",     "fase": "D — DO",   "cor": "#F59E0B", "desc": "Execução e controles"},
        {"nome": "Avaliação",    "fase": "C — CHECK","cor": "#10B981", "desc": "Monitoramento"},
        {"nome": "Melhoria",     "fase": "A — ACT",  "cor": "#6366F1", "desc": "Ações corretivas"},
    ]

    linhas_pdca = [
        "🎯 Objetivo Estratégico",
        "⚙️ Ação Técnica (TI/OT)",
        "📊 Indicador (KPI)",
        "🚩 Evidência / Status",
    ]

    cols = st.columns(len(colunas_pdca), gap="small")
    dados_pdca = {}

    for i, (col_obj, col_info) in enumerate(zip(cols, colunas_pdca)):
        with col_obj:
            st.markdown(f"""
            <div class='pdca-phase-header' style='
                background: linear-gradient(135deg, {col_info["cor"]}22, {col_info["cor"]}11);
                border: 1px solid {col_info["cor"]}44;
            '>
                <div class='pdca-phase-tag' style='color:{col_info["cor"]};'>{col_info["fase"]}</div>
                <div class='pdca-phase-name' style='color:{col_info["cor"]};'>{col_info["nome"]}</div>
                <div class='pdca-phase-desc' style='color:{col_info["cor"]};'>{col_info["desc"]}</div>
            </div>
            """, unsafe_allow_html=True)

            for j, linha in enumerate(linhas_pdca):
                if i == 0:
                    st.markdown(f"<div class='pdca-row-label' style='border-left-color:{col_info['cor']};'>{linha}</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='height:54px;margin:4px 0 6px;'></div>", unsafe_allow_html=True)

                key_id = f"pdca_{i}_{j}"
                valor = st.text_area(
                    label="", key=key_id,
                    placeholder="Registre aqui...",
                    label_visibility="collapsed",
                    height=90,
                )
                dados_pdca[(i, j)] = valor
                st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)

    # Botão de impressão
    st.markdown("<br>", unsafe_allow_html=True)
    c_btn1, _, _ = st.columns([1.5, 3, 1.5])
    with c_btn1:
        if st.button("🖨️  Gerar Relatório para Impressão", use_container_width=True):
            risco_html = edited_risco.to_html(index=False)
            equip_html = edited_equipamentos.to_html(index=False)
            pdca_html = "<table border='1' style='width:100%;border-collapse:collapse;'>"
            pdca_html += "<tr>" + "".join(
                f"<th style='background:{c['cor']};color:white;padding:8px;'>{c['nome']}<br><small>{c['fase']}</small></th>"
                for c in colunas_pdca) + "</tr>"
            for j in range(len(linhas_pdca)):
                pdca_html += "<tr>"
                for i in range(len(colunas_pdca)):
                    cont = dados_pdca.get((i, j), "").replace("\n", "<br>")
                    pdca_html += f"<td style='padding:8px;vertical-align:top;'><b>{linhas_pdca[j]}</b><br>{cont or '—'}</td>"
                pdca_html += "</tr>"
            pdca_html += "</table>"

            html_completo = f"""
            <html><head>
            <style>
                body{{font-family:Arial;margin:30px;color:#111;}}
                h1{{font-size:22px;margin-bottom:4px;}}
                h2{{font-size:16px;margin:20px 0 8px;color:#1e40af;border-bottom:2px solid #93c5fd;padding-bottom:4px;}}
                table{{border-collapse:collapse;width:100%;margin-bottom:20px;font-size:12px;}}
                th,td{{border:1px solid #cbd5e1;padding:7px 10px;}}
                th{{background:#1e3a5f;color:white;}}
                tr:nth-child(even){{background:#f8fafc;}}
                .meta{{font-size:11px;color:#64748b;margin-bottom:20px;}}
            </style></head>
            <body>
                <h1>📋 Relatório de Gestão de Segurança</h1>
                <div class='meta'>Gerado por: {st.session_state.usuario} &nbsp;|&nbsp; {datetime.now().strftime('%d/%m/%Y às %H:%M')}</div>
                <h2>Análise de Risco</h2>{risco_html}
                <h2>Equipamentos TI/OT</h2>{equip_html}
                <h2>PDCA de Controle de Acesso</h2>{pdca_html}
                <script>window.onload=function(){{window.print();}}</script>
            </body></html>"""
            st.components.v1.html(html_completo, height=500)

# ─── Atualizar sidebar com os riscos calculados ───
with sidebar_risk_placeholder:
    st.markdown(f"""
    <div class='sidebar-section'>
        <div class='sidebar-section-label'>Visão de Riscos</div>
    </div>
    <div class='risk-stat'>
        <span class='risk-stat-label'>🔴 Alto</span>
        <span class='risk-stat-badge badge-alto'>{qtd_alto}</span>
    </div>
    <div class='risk-stat'>
        <span class='risk-stat-label'>🟡 Médio</span>
        <span class='risk-stat-badge badge-medio'>{qtd_medio}</span>
    </div>
    <div class='risk-stat'>
        <span class='risk-stat-label'>🟢 Baixo</span>
        <span class='risk-stat-badge badge-baixo'>{qtd_baixo}</span>
    </div>
    <br>
    """, unsafe_allow_html=True)
