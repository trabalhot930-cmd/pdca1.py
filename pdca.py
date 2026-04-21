import streamlit as st
import pandas as pd
from datetime import datetime
import hashlib

# Tentar importar supabase, se não tiver, instalar
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    st.warning("⚠️ Biblioteca supabase não instalada. Instale com: pip install supabase")

# ──────────────────────────────────────────────
# CONFIGURAÇÃO SUPABASE
# ──────────────────────────────────────────────
# Configurações do Supabase (substitua pelos seus dados)
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "")

def init_supabase():
    """Inicializa conexão com Supabase"""
    if SUPABASE_AVAILABLE and SUPABASE_URL and SUPABASE_KEY:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    return None

def salvar_historico(supabase, tipo, dados, usuario):
    """Salva dados no histórico do Supabase"""
    if not supabase:
        return False
    try:
        data = {
            "tipo": tipo,
            "dados": dados.to_dict('records') if isinstance(dados, pd.DataFrame) else dados,
            "usuario": usuario,
            "data_criacao": datetime.now().isoformat()
        }
        supabase.table("historico_seguranca").insert(data).execute()
        return True
    except Exception as e:
        st.error(f"Erro ao salvar histórico: {e}")
        return False

def carregar_historico(supabase, tipo=None):
    """Carrega histórico do Supabase"""
    if not supabase:
        return pd.DataFrame()
    try:
        query = supabase.table("historico_seguranca").select("*").order("data_criacao", desc=True)
        if tipo:
            query = query.eq("tipo", tipo)
        response = query.execute()
        return pd.DataFrame(response.data)
    except Exception as e:
        st.error(f"Erro ao carregar histórico: {e}")
        return pd.DataFrame()

# ──────────────────────────────────────────────
# CONFIGURAÇÃO DA PÁGINA
# ──────────────────────────────────────────────
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
# CSS OTIMIZADO
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

/* SIDEBAR */
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

/* TÍTULOS */
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

/* BUTTON */
.stButton > button {
    background: #0f172a !important; color: #fff !important;
    border: none !important; border-radius: 8px !important;
    font-size: 13px !important; font-weight: 500 !important;
}
.stButton > button:hover { background: #1e293b !important; }

hr { border: none; border-top: 1px solid #e2e8f0 !important; margin: 0.8rem 0; }

/* EXPORTER */
.export-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
    border-radius: 12px;
    color: white;
    margin-bottom: 20px;
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
# INICIALIZAR SUPABASE
# ──────────────────────────────────────────────
supabase = init_supabase()
if supabase:
    st.success("✅ Conectado ao Supabase - Histórico disponível")
elif SUPABASE_AVAILABLE:
    st.info("ℹ️ Configure as credenciais do Supabase nos secrets do Streamlit")

# ──────────────────────────────────────────────
# SIDEBAR
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
    
    st.markdown("<div class='sb-lbl'>Data/Hora</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sb-time'>📅 {datetime.now().strftime('%d/%m/%Y')}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sb-time'>🕐 {datetime.now().strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)
    st.markdown("<hr class='sb-div'>", unsafe_allow_html=True)
    
    if st.button("Encerrar Sessão", use_container_width=True):
        fazer_logout()

# ──────────────────────────────────────────────
# CABEÇALHO COM DATA
# ──────────────────────────────────────────────
st.markdown(f"""
<div class='page-title'>SecureOps - Gestão de Segurança</div>
<div class='page-sub'>PDCA + Análise de Risco · Relatório: {datetime.now().strftime('%d/%m/%Y %H:%M')}</div>
""", unsafe_allow_html=True)

# Criar abas
tab_dados, tab_graficos, tab_pdca, tab_historico = st.tabs(["📋 Dados", "📊 Gráficos", "🔄 PDCA", "📜 Histórico"])

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

    # Exportação
    st.markdown("---")
    st.markdown("### 📤 Exportar Relatório")
    
    col_exp1, col_exp2, col_exp3 = st.columns(3)
    with col_exp1:
        if st.button("📥 Exportar Excel", use_container_width=True):
            with pd.ExcelWriter(f"relatorio_seguranca_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx", engine="openpyxl") as writer:
                edited_risco.to_excel(writer, sheet_name="Analise_Risco", index=False)
                edited_eq.to_excel(writer, sheet_name="Equipamentos", index=False)
            
            # Salvar no Supabase
            if supabase:
                salvar_historico(supabase, "analise_risco", edited_risco, st.session_state.usuario)
                salvar_historico(supabase, "equipamentos", edited_eq, st.session_state.usuario)
                st.success("✅ Dados salvos no histórico do Supabase!")
    
    with col_exp2:
        if st.button("📊 Exportar CSV", use_container_width=True):
            csv_risco = edited_risco.to_csv(index=False)
            csv_eq = edited_eq.to_csv(index=False)
            st.download_button("Baixar Riscos CSV", csv_risco, f"riscos_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
            st.download_button("Baixar Equipamentos CSV", csv_eq, f"equipamentos_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
    
    with col_exp3:
        if st.button("🖨️ Imprimir Relatório", use_container_width=True):
            r_html = edited_risco.to_html(index=False)
            e_html = edited_eq.to_html(index=False)
            html_full = f"""<html><head><style>
            body{{font-family:'Inter',Arial;margin:30px;}}
            h1{{font-size:20px;}} h2{{font-size:14px;margin:20px 0 8px;color:#2563eb;}}
            table{{border-collapse:collapse;width:100%;}}
            th,td{{border:1px solid #cbd5e1;padding:6px 8px;}}
            th{{background:#0f172a;color:#fff;}}
            </style></head><body>
            <h1>Relatório de Gestão de Segurança</h1>
            <p>Gerado por: {st.session_state.usuario} · {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
            <h2>Análise de Risco</h2>{r_html}
            <h2>Equipamentos TI/OT</h2>{e_html}
            <script>window.onload=function(){{window.print();}}</script>
            </body></html>"""
            st.components.v1.html(html_full, height=500)

# ══════════════════════════════════════════════
# TAB GRÁFICOS
# ══════════════════════════════════════════════
with tab_graficos:
    st.markdown("### 📊 Dashboard de Gráficos")
    
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
    
    # Gráficos
    st.markdown(stacked_bar(edited_risco, "📍 Riscos por Localidade", CORES_RISCO, "Localidade", "Nível do Risco"), unsafe_allow_html=True)
    st.markdown(stacked_bar(edited_risco, "📊 Riscos por Probabilidade", CORES_RISCO, "Probabilidade", "Nível do Risco"), unsafe_allow_html=True)
    st.markdown(stacked_bar(edited_eq, "🏢 Equipamentos por Localidade", CORES_TIPO, "Localidade", "Tipo"), unsafe_allow_html=True)
    st.markdown(stacked_bar(edited_eq, "⚙️ Equipamentos por Tipo", CORES_STATUS, "Tipo", "Status"), unsafe_allow_html=True)

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
            # Salvar PDCA no Supabase
            if supabase:
                pdca_dict = {}
                for i, f in enumerate(fases):
                    for j, linha in enumerate(linhas):
                        key = f"pdca_{i}_{j}"
                        pdca_dict[f"{f['nome']}_{linha}"] = dados_pdca.get((i, j), "")
                salvar_historico(supabase, "pdca", pdca_dict, st.session_state.usuario)
            
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

# ══════════════════════════════════════════════
# TAB HISTÓRICO
# ══════════════════════════════════════════════
with tab_historico:
    st.markdown("### 📜 Histórico de Alterações")
    
    if supabase:
        col_h1, col_h2 = st.columns(2)
        with col_h1:
            tipo_filtro = st.selectbox("Filtrar por tipo:", ["Todos", "analise_risco", "equipamentos", "pdca"])
        
        with col_h2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔄 Atualizar Histórico", use_container_width=True):
                st.rerun()
        
        # Carregar histórico
        tipo = None if tipo_filtro == "Todos" else tipo_filtro
        historico_df = carregar_historico(supabase, tipo)
        
        if not historico_df.empty:
            st.markdown(f"**Total de registros:** {len(historico_df
