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
# CSS
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    font-size: 15px;
    color: #1a1a2e;
}

[data-testid="stAppViewContainer"] { background: #F5F7FA; }
[data-testid="stSidebar"] { background: #1a1a2e !important; border-right: none !important; }

.block-container { padding: 2rem 2.5rem 3rem !important; max-width: 100% !important; }

/* SIDEBAR */
.sb-logo { font-size: 22px; font-weight: 800; color: #fff; letter-spacing: -0.5px; padding: 1.2rem 0 0.2rem; }
.sb-sub  { font-size: 11px; color: #64748b; margin-bottom: 1rem; }
.sb-div  { border: none; border-top: 1px solid rgba(255,255,255,0.08); margin: 0.8rem 0; }
.sb-lbl  { font-size: 10px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: #475569; margin-bottom: 0.4rem; }
.sb-user { font-size: 14px; font-weight: 600; color: #e2e8f0; margin-bottom: 2px; }
.sb-role { font-size: 11px; color: #64748b; }
.sb-badge { display: flex; align-items: center; justify-content: space-between; padding: 9px 12px; border-radius: 8px; margin-bottom: 6px; font-size: 14px; font-weight: 600; }
.sb-red    { background: #fef2f2; color: #dc2626; }
.sb-yellow { background: #fefce8; color: #ca8a04; }
.sb-green  { background: #f0fdf4; color: #16a34a; }
.sb-num { font-size: 18px; font-weight: 800; }
.sb-time { font-size: 11px; color: #475569; margin-top: 1.2rem; }

/* TABS */
.stTabs [data-baseweb="tab-list"] {
    gap: 0; background: #e2e8f0 !important; padding: 4px !important;
    border-radius: 10px !important; width: fit-content; border: none !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 7px !important; padding: 8px 22px !important;
    font-size: 14px !important; font-weight: 600 !important;
    color: #64748b !important; background: transparent !important; border: none !important;
}
.stTabs [aria-selected="true"] {
    background: #fff !important; color: #1a1a2e !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.1) !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 1.8rem !important; }

/* PAGE TITLE */
.page-title { font-size: 26px; font-weight: 800; color: #1a1a2e; letter-spacing: -0.5px; margin-bottom: 2px; }
.page-sub   { font-size: 13px; color: #64748b; margin-bottom: 1.5rem; }

/* SECTION TITLE */
.sec-title {
    font-size: 12px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 1px; color: #94a3b8;
    margin: 2rem 0 0.8rem;
    border-bottom: 1px solid #e2e8f0; padding-bottom: 8px;
}

/* METRIC CARDS */
.mcard { background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px 18px 16px; }
.mcard-num { font-size: 40px; font-weight: 800; letter-spacing: -1.5px; line-height: 1; margin-bottom: 4px; }
.mcard-lbl { font-size: 13px; font-weight: 500; color: #64748b; }
.c-blue   { color: #2563eb; }
.c-red    { color: #dc2626; }
.c-yellow { color: #d97706; }
.c-green  { color: #16a34a; }
.c-gray   { color: #475569; }

/* STACKED BAR CHART */
.chart-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 22px; }
.chart-title { font-size: 14px; font-weight: 700; color: #1a1a2e; margin-bottom: 20px; }
.sbar-wrap { margin-bottom: 14px; }
.sbar-label { font-size: 13px; font-weight: 500; color: #334155; margin-bottom: 5px; display: flex; justify-content: space-between; }
.sbar-track { height: 26px; border-radius: 6px; background: #f1f5f9; overflow: hidden; display: flex; }
.sbar-seg { height: 100%; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; color: #fff; min-width: 16px; }
.legend-row { display: flex; gap: 14px; margin-top: 14px; flex-wrap: wrap; }
.legend-dot { display: flex; align-items: center; gap: 5px; font-size: 12px; color: #64748b; }
.ldot { width: 10px; height: 10px; border-radius: 3px; flex-shrink: 0; }

/* PDCA */
.pdca-header { border-radius: 8px; padding: 10px 8px; text-align: center; margin-bottom: 10px; }
.pdca-row-lbl { font-size: 13px; font-weight: 600; color: #475569; padding: 8px 0 4px; border-bottom: 1px solid #e2e8f0; margin: 6px 0 4px; }

/* INPUTS */
textarea {
    border-radius: 8px !important; border: 1px solid #e2e8f0 !important;
    font-size: 13px !important; font-family: 'Inter', sans-serif !important;
    background: #fff !important; color: #1a1a2e !important;
}
textarea:focus { border-color: #2563eb !important; box-shadow: 0 0 0 2px rgba(37,99,235,0.1) !important; }
[data-testid="stTextInput"] input {
    border-radius: 8px !important; border: 1px solid #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important; font-size: 14px !important; background: #fff !important;
}

/* BUTTON */
.stButton > button {
    background: #1a1a2e !important; color: #fff !important;
    border: none !important; border-radius: 8px !important;
    font-size: 14px !important; font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
}
.stButton > button:hover { background: #2d2d4e !important; }

/* ALERTS */
[data-testid="stSuccess"] { background: #f0fdf4 !important; border: 1px solid #bbf7d0 !important; border-radius: 8px !important; color: #166534 !important; }
[data-testid="stError"]   { background: #fef2f2 !important; border: 1px solid #fecaca !important; border-radius: 8px !important; color: #991b1b !important; }

hr { border: none; border-top: 1px solid #e2e8f0 !important; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# LOGIN
# ──────────────────────────────────────────────
if not verificar_login():
    _, col, _ = st.columns([1, 1.4, 1])
    with col:
        st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)
        st.markdown("<div class='page-title' style='text-align:center'>🛡️ SecureOps</div>", unsafe_allow_html=True)
        st.markdown("<div class='page-sub' style='text-align:center'>Sistema de Gestão de Segurança da Informação</div>", unsafe_allow_html=True)
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
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
        st.markdown("<p style='text-align:center;font-size:12px;color:#94a3b8;margin-top:12px;'>Usuário: Juan · Senha: Ju@n1990</p>", unsafe_allow_html=True)
    st.stop()

# ──────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────
def nivel_risco(prob, imp):
    prob = str(prob).lower().strip()
    imp  = str(imp).lower().strip()
    if (prob == "baixa" and imp in ["baixo","médio"]) or (prob == "média" and imp == "baixo"):
        return "🟢 Baixo"
    elif (prob == "baixa" and imp == "alto") or (prob == "média" and imp == "médio") or (prob == "alta" and imp == "baixo"):
        return "🟡 Médio"
    else:
        return "🔴 Alto"

CORES_RISCO  = {"🔴 Alto": "#dc2626", "🟡 Médio": "#d97706", "🟢 Baixo": "#16a34a"}
CORES_TIPO   = {"Segurança": "#2563eb", "Rede": "#7c3aed", "Servidor": "#0891b2", "Storage": "#059669", "Infraestrutura": "#d97706"}
CORES_STATUS = {"Ativo": "#16a34a", "Em Manutenção": "#d97706", "Desativado": "#dc2626", "Reserva": "#64748b"}

def stacked_bar(df, title, cores, col_group, col_stack):
    pivot = df.groupby([col_group, col_stack]).size().unstack(fill_value=0)
    cats  = list(pivot.columns)
    tmax  = pivot.sum(axis=1).max() or 1

    legend = "".join([
        f"<div class='legend-dot'><div class='ldot' style='background:{cores.get(c,\"#94a3b8\")}'></div>{c}</div>"
        for c in cats
    ])

    bars = ""
    for idx, row in pivot.iterrows():
        total = row.sum() or 1
        segs  = ""
        for cat in cats:
            val = row.get(cat, 0)
            pct = (val / total) * 100
            cor = cores.get(cat, "#94a3b8")
            if pct > 0:
                segs += f"<div class='sbar-seg' style='width:{pct}%;background:{cor};' title='{cat}: {val}'>{val if pct > 9 else ''}</div>"
        w = max((total / tmax) * 100, 12)
        bars += f"""
        <div class='sbar-wrap'>
            <div class='sbar-label'>
                <span>{str(idx)[:38]}</span>
                <span style='font-weight:700;color:#1a1a2e'>{int(total)}</span>
            </div>
            <div class='sbar-track' style='width:{w}%'>{segs}</div>
        </div>"""

    return f"<div class='chart-card'><div class='chart-title'>{title}</div>{bars}<div class='legend-row'>{legend}</div></div>"

def mcard(num, lbl, cor):
    return f"<div class='mcard'><div class='mcard-num {cor}'>{num}</div><div class='mcard-lbl'>{lbl}</div></div>"

def sec(t):
    st.markdown(f"<div class='sec-title'>{t}</div>", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div class='sb-logo'>🛡️ SecureOps</div>
    <div class='sb-sub'>Gestão de Segurança da Informação</div>
    <hr class='sb-div'>
    <div class='sb-lbl'>Usuário</div>
    <div class='sb-user'>{st.session_state.usuario}</div>
    <div class='sb-role'>Administrador de TI</div>
    <hr class='sb-div'>
    <div class='sb-lbl'>Resumo de Riscos</div>
    """, unsafe_allow_html=True)
    sidebar_ph = st.empty()
    st.markdown("<hr class='sb-div'>", unsafe_allow_html=True)
    if st.button("Encerrar Sessão", use_container_width=True):
        fazer_logout()
    st.markdown(f"<div class='sb-time'>🕐 {datetime.now().strftime('%d/%m/%Y  %H:%M')}</div>", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# CABEÇALHO
# ──────────────────────────────────────────────
st.markdown(f"""
<div class='page-title'>PDCA + Análise de Risco</div>
<div class='page-sub'>Segurança da Informação · {datetime.now().strftime('%d/%m/%Y')}</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📊  Análise de Risco", "🖥️  Equipamentos", "🔄  PDCA"])

# ══════════════════════════════════════════════
# TAB 1 — ANÁLISE DE RISCO
# ══════════════════════════════════════════════
with tab1:
    sec("Matriz de Risco")
    dados_risco = pd.DataFrame({
        "Ativo":           ["Cabos na sala de servidores","Pen drive ou HD","Servidor de internet",
                            "Switch de borda","Firewall","Router core"],
        "Localidade":      ["Sala de servidores - Bloco A","TI - Sala 210","Data Center - Rack 05",
                            "Sala de rede - Andar 3","Data Center - Rack 02","Data Center - Rack 01"],
        "Ameaça":          ["Rompimento","Contaminação por vírus","Invasão externa",
                            "Desligamento acidental","Ataque DDoS","Configuração errada"],
        "Vulnerabilidade": ["Cabos fora de dutos","Antivírus desatualizado",
                            "Internet ligada direto na rede interna","Sem trava física no rack",
                            "Firmware desatualizado","Senha fraca"],
        "Probabilidade":   ["Baixa","Alta","Média","Média","Baixa","Média"],
        "Impacto":         ["Alto","Alto","Alto","Médio","Alto","Alto"],
    })
    dados_risco["Nível do Risco"] = dados_risco.apply(lambda r: nivel_risco(r["Probabilidade"], r["Impacto"]), axis=1)

    edited_risco = st.data_editor(
        dados_risco, use_container_width=True, num_rows="dynamic",
        column_config={
            "Ativo":           st.column_config.TextColumn("Ativo", required=True),
            "Localidade":      st.column_config.TextColumn("Localidade"),
            "Ameaça":          st.column_config.TextColumn("Ameaça"),
            "Vulnerabilidade": st.column_config.TextColumn("Vulnerabilidade"),
            "Probabilidade":   st.column_config.SelectboxColumn("Probabilidade", options=["Baixa","Média","Alta"]),
            "Impacto":         st.column_config.SelectboxColumn("Impacto", options=["Baixo","Médio","Alto"]),
            "Nível do Risco":  st.column_config.TextColumn("Nível do Risco", disabled=True),
        }, hide_index=True,
    )
    edited_risco["Nível do Risco"] = edited_risco.apply(lambda r: nivel_risco(r["Probabilidade"], r["Impacto"]), axis=1)

    qtd_alto  = len(edited_risco[edited_risco["Nível do Risco"] == "🔴 Alto"])
    qtd_medio = len(edited_risco[edited_risco["Nível do Risco"] == "🟡 Médio"])
    qtd_baixo = len(edited_risco[edited_risco["Nível do Risco"] == "🟢 Baixo"])

    sec("Indicadores")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(mcard(len(edited_risco), "Total de Riscos",  "c-blue"),   unsafe_allow_html=True)
    with c2: st.markdown(mcard(qtd_alto,  "Riscos Críticos",  "c-red"),    unsafe_allow_html=True)
    with c3: st.markdown(mcard(qtd_medio, "Riscos Médios",    "c-yellow"), unsafe_allow_html=True)
    with c4: st.markdown(mcard(qtd_baixo, "Riscos Baixos",    "c-green"),  unsafe_allow_html=True)

    sec("Gráficos")
    g1, g2 = st.columns(2)
    with g1:
        st.markdown(stacked_bar(edited_risco, "Riscos por Localidade", CORES_RISCO, "Localidade", "Nível do Risco"), unsafe_allow_html=True)
    with g2:
        st.markdown(stacked_bar(edited_risco, "Riscos por Probabilidade", CORES_RISCO, "Probabilidade", "Nível do Risco"), unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB 2 — EQUIPAMENTOS
# ══════════════════════════════════════════════
with tab2:
    sec("Inventário de Equipamentos TI/OT")
    dados_eq = pd.DataFrame({
        "Equipamento": ["Firewall Fortinet","Switch Core Huawei","Router Cisco","Servidor Dell",
                        "Storage EMC","Access Point","Patch Panel"],
        "Tipo":        ["Segurança","Rede","Rede","Servidor","Storage","Rede","Infraestrutura"],
        "Localidade":  ["Data Center - Rack 02","Data Center - Rack 01","Data Center - Rack 01",
                        "Data Center - Rack 03","Data Center - Rack 04","Sala 210 - Teto","Sala de servidores"],
        "Fabricante":  ["Fortinet","Huawei","Cisco","Dell","EMC","Ubiquiti","Intelbras"],
        "Modelo":      ["FG-100F","S12700","ISR 4321","PowerEdge R750","Unity XT 380","U6-LR","CAT6"],
        "Status":      ["Ativo","Ativo","Ativo","Ativo","Ativo","Ativo","Ativo"],
        "Motivo":      ["","","","","","",""],
    })

    edited_eq = st.data_editor(
        dados_eq, use_container_width=True, num_rows="dynamic",
        column_config={
            "Equipamento": st.column_config.TextColumn("Equipamento", required=True),
            "Tipo":        st.column_config.SelectboxColumn("Tipo", options=["Segurança","Rede","Servidor","Storage","Infraestrutura"]),
            "Localidade":  st.column_config.TextColumn("Localidade"),
            "Fabricante":  st.column_config.TextColumn("Fabricante"),
            "Modelo":      st.column_config.TextColumn("Modelo"),
            "Status":      st.column_config.SelectboxColumn("Status", options=["Ativo","Em Manutenção","Desativado","Reserva"]),
            "Motivo":      st.column_config.TextColumn("Motivo / Observação"),
        }, hide_index=True,
    )

    sec("Indicadores")
    ativos     = len(edited_eq[edited_eq["Status"] == "Ativo"])
    manutencao = len(edited_eq[edited_eq["Status"] == "Em Manutenção"])
    seg_count  = len(edited_eq[edited_eq["Tipo"] == "Segurança"])
    fab_count  = edited_eq["Fabricante"].nunique()

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(mcard(len(edited_eq), "Total de Equipamentos",   "c-blue"),   unsafe_allow_html=True)
    with c2: st.markdown(mcard(ativos,         "Ativos",                  "c-green"),  unsafe_allow_html=True)
    with c3: st.markdown(mcard(manutencao,     "Em Manutenção",           "c-yellow"), unsafe_allow_html=True)
    with c4: st.markdown(mcard(fab_count,      "Fabricantes",             "c-gray"),   unsafe_allow_html=True)

    sec("Gráficos")
    g1, g2 = st.columns(2)
    with g1:
        st.markdown(stacked_bar(edited_eq, "Equipamentos por Tipo (status)", CORES_STATUS, "Tipo", "Status"), unsafe_allow_html=True)
    with g2:
        st.markdown(stacked_bar(edited_eq, "Equipamentos por Localidade (tipo)", CORES_TIPO, "Localidade", "Tipo"), unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB 3 — PDCA
# ══════════════════════════════════════════════
with tab3:
    sec("PDCA de Controle de Acesso")

    fases = [
        {"nome": "1. Contexto",     "fase": "PLAN",  "cor": "#2563eb"},
        {"nome": "2. Liderança",    "fase": "PLAN",  "cor": "#2563eb"},
        {"nome": "3. Planejamento", "fase": "PLAN",  "cor": "#2563eb"},
        {"nome": "4. Suporte",      "fase": "DO",    "cor": "#d97706"},
        {"nome": "5. Operação",     "fase": "DO",    "cor": "#d97706"},
        {"nome": "6. Avaliação",    "fase": "CHECK", "cor": "#16a34a"},
        {"nome": "7. Melhoria",     "fase": "ACT",   "cor": "#7c3aed"},
    ]
    linhas = [
        "🎯 Objetivo Estratégico",
        "⚙️ Ação Técnica (TI/OT)",
        "📊 Indicador (KPI)",
        "🚩 Evidência / Status",
    ]

    cols = st.columns(len(fases), gap="small")
    dados_pdca = {}

    for i, (col, f) in enumerate(zip(cols, fases)):
        with col:
            st.markdown(f"""
            <div class='pdca-header' style='background:{f["cor"]}15;border:1px solid {f["cor"]}30;'>
                <div style='font-size:9px;font-weight:700;letter-spacing:1.5px;color:{f["cor"]};text-transform:uppercase;'>{f["fase"]}</div>
                <div style='font-size:13px;font-weight:700;color:{f["cor"]};margin-top:2px;'>{f["nome"]}</div>
            </div>
            """, unsafe_allow_html=True)
            for j, linha in enumerate(linhas):
                if i == 0:
                    st.markdown(f"<div class='pdca-row-lbl'>{linha}</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='height:37px;'></div>", unsafe_allow_html=True)
                dados_pdca[(i,j)] = st.text_area(
                    label="", key=f"p_{i}_{j}",
                    placeholder="Registre...",
                    label_visibility="collapsed",
                    height=88,
                )

    st.markdown("<br>", unsafe_allow_html=True)
    col_b, _, _ = st.columns([1.5, 3, 1.5])
    with col_b:
        if st.button("🖨️  Gerar Relatório", use_container_width=True):
            r_html = edited_risco.to_html(index=False)
            e_html = edited_eq.to_html(index=False)
            p_html = "<table border='1' style='width:100%;border-collapse:collapse;font-size:12px;'>"
            p_html += "<tr>" + "".join(
                f"<th style='background:{f['cor']};color:#fff;padding:8px;'>{f['nome']}</th>"
                for f in fases) + "</tr>"
            for j in range(len(linhas)):
                p_html += "<tr>" + "".join(
                    f"<td style='padding:8px;vertical-align:top;'><b>{linhas[j]}</b><br>{dados_pdca.get((i,j),'').replace(chr(10),'<br>') or '—'}</td>"
                    for i in range(len(fases))) + "</tr>"
            p_html += "</table>"
            html_full = f"""<html><head><style>
            body{{font-family:Arial;margin:30px;color:#111;font-size:13px;}}
            h1{{font-size:20px;}} h2{{font-size:15px;margin:20px 0 8px;color:#1d4ed8;border-bottom:2px solid #bfdbfe;padding-bottom:4px;}}
            table{{border-collapse:collapse;width:100%;margin-bottom:20px;}}
            th,td{{border:1px solid #cbd5e1;padding:7px 10px;}}
            th{{background:#1e3a8a;color:#fff;}} tr:nth-child(even){{background:#f8fafc;}}
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
# SIDEBAR — riscos
# ──────────────────────────────────────────────
with sidebar_ph:
    st.markdown(f"""
    <div class='sb-badge sb-red'>   <span>🔴 Alto</span>  <span class='sb-num'>{qtd_alto}</span>  </div>
    <div class='sb-badge sb-yellow'><span>🟡 Médio</span> <span class='sb-num'>{qtd_medio}</span> </div>
    <div class='sb-badge sb-green'> <span>🟢 Baixo</span> <span class='sb-num'>{qtd_baixo}</span> </div>
    """, unsafe_allow_html=True)
