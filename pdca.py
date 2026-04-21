import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client, Client
import json

st.set_page_config(
    layout="wide",
    page_title="SecureOps — Gestão de Segurança",
    page_icon="🛡️",
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────
# CONFIGURAÇÃO DO SUPABASE (SUAS CREDENCIAIS)
# ──────────────────────────────────────────────
SUPABASE_URL = "https://bhwqrfolkusuzvwavanc.supabase.co"
SUPABASE_KEY = "sb_publishable_J_z2LmOOVT0cmJuYhqW0qg_9iAEHt4u"

def init_supabase():
    """Inicializa conexão com Supabase"""
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        st.error(f"Erro ao conectar Supabase: {e}")
        return None

# ──────────────────────────────────────────────
# FUNÇÕES DO SUPABASE
# ──────────────────────────────────────────────
def salvar_riscos_supabase(supabase, df_riscos, usuario):
    """Salva análise de risco no Supabase"""
    if not supabase:
        return False
    try:
        # Limpar dados antigos
        supabase.table("riscos_atuais").delete().neq("id", 0).execute()
        
        # Inserir novos dados
        for _, row in df_riscos.iterrows():
            supabase.table("riscos_atuais").insert({
                "ativo": row["Ativo"],
                "localidade": row["Localidade"],
                "ameaca": row["Ameaça"],
                "vulnerabilidade": row["Vulnerabilidade"],
                "probabilidade": row["Probabilidade"],
                "impacto": row["Impacto"],
                "nivel_risco": row["Nível do Risco"],
                "usuario": usuario
            }).execute()
        
        # Salvar no histórico
        supabase.table("historico_seguranca").insert({
            "tipo": "analise_risco",
            "dados": json.dumps(df_riscos.to_dict('records')),
            "usuario": usuario
        }).execute()
        
        return True
    except Exception as e:
        st.error(f"Erro ao salvar riscos: {e}")
        return False

def carregar_riscos_supabase(supabase):
    """Carrega análise de risco do Supabase"""
    if not supabase:
        return None
    try:
        response = supabase.table("riscos_atuais").select("*").execute()
        if response.data:
            df = pd.DataFrame(response.data)
            df = df.rename(columns={
                "ativo": "Ativo",
                "localidade": "Localidade",
                "ameaca": "Ameaça",
                "vulnerabilidade": "Vulnerabilidade",
                "probabilidade": "Probabilidade",
                "impacto": "Impacto",
                "nivel_risco": "Nível do Risco"
            })
            return df[["Ativo", "Localidade", "Ameaça", "Vulnerabilidade", "Probabilidade", "Impacto", "Nível do Risco"]]
        return None
    except Exception as e:
        st.error(f"Erro ao carregar riscos: {e}")
        return None

def salvar_equipamentos_supabase(supabase, df_eq, usuario):
    """Salva equipamentos no Supabase"""
    if not supabase:
        return False
    try:
        supabase.table("equipamentos").delete().neq("id", 0).execute()
        
        for _, row in df_eq.iterrows():
            supabase.table("equipamentos").insert({
                "equipamento": row["Equipamento"],
                "tipo": row["Tipo"],
                "localidade": row["Localidade"],
                "fabricante": row["Fabricante"],
                "modelo": row["Modelo"],
                "status": row["Status"],
                "motivo": row.get("Motivo", ""),
                "usuario": usuario
            }).execute()
        
        supabase.table("historico_seguranca").insert({
            "tipo": "equipamentos",
            "dados": json.dumps(df_eq.to_dict('records')),
            "usuario": usuario
        }).execute()
        
        return True
    except Exception as e:
        st.error(f"Erro ao salvar equipamentos: {e}")
        return False

def carregar_equipamentos_supabase(supabase):
    """Carrega equipamentos do Supabase"""
    if not supabase:
        return None
    try:
        response = supabase.table("equipamentos").select("*").execute()
        if response.data:
            df = pd.DataFrame(response.data)
            df = df.rename(columns={
                "equipamento": "Equipamento",
                "tipo": "Tipo",
                "localidade": "Localidade",
                "fabricante": "Fabricante",
                "modelo": "Modelo",
                "status": "Status",
                "motivo": "Motivo"
            })
            return df[["Equipamento", "Tipo", "Localidade", "Fabricante", "Modelo", "Status", "Motivo"]]
        return None
    except Exception as e:
        st.error(f"Erro ao carregar equipamentos: {e}")
        return None

def carregar_historico_supabase(supabase, tipo=None):
    """Carrega histórico do Supabase"""
    if not supabase:
        return pd.DataFrame()
    try:
        query = supabase.table("historico_seguranca").select("id,tipo,usuario,data").order("id", desc=True).limit(50)
        if tipo and tipo != "Todos":
            query = query.eq("tipo", tipo)
        response = query.execute()
        if response.data:
            return pd.DataFrame(response.data)
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro ao carregar histórico: {e}")
        return pd.DataFrame()

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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif !important; }
[data-testid="stSidebar"] { background: #f1f5f9 !important; border-right: 1px solid #e2e8f0 !important; }
.block-container { padding: 1.5rem 2rem 2rem !important; }
.sb-logo { font-size: 20px; font-weight: 700; color: #0f172a; }
.sb-sub { font-size: 11px; color: #64748b; }
.sb-div { border-top: 1px solid #e2e8f0; margin: 0.8rem 0; }
.sb-lbl { font-size: 10px; font-weight: 600; text-transform: uppercase; color: #64748b; }
.sb-badge { display: flex; justify-content: space-between; padding: 8px 12px; border-radius: 8px; margin-bottom: 6px; }
.sb-red { background: #fee2e2; color: #dc2626; }
.sb-yellow { background: #fef3c7; color: #d97706; }
.sb-green { background: #dcfce7; color: #16a34a; }
.sb-num { font-size: 18px; font-weight: 700; }
.page-title { font-size: 24px; font-weight: 700; color: #0f172a; }
.page-sub { font-size: 13px; color: #64748b; margin-bottom: 1.2rem; }
.sec-title { font-size: 11px; font-weight: 600; text-transform: uppercase; color: #94a3b8; border-bottom: 1px solid #e2e8f0; margin: 1.5rem 0 0.8rem; }
.mcard { background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px; }
.mcard-num { font-size: 32px; font-weight: 700; }
.mcard-lbl { font-size: 12px; color: #64748b; }
.c-blue { color: #2563eb; }
.c-red { color: #dc2626; }
.c-green { color: #16a34a; }
.c-yellow { color: #d97706; }
.chart-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 18px; margin-bottom: 16px; }
.chart-title { font-size: 14px; font-weight: 600; border-left: 3px solid #2563eb; padding-left: 10px; }
.sbar-track { height: 32px; background: #f1f5f9; border-radius: 6px; overflow: hidden; display: flex; }
.sbar-seg { display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 600; color: #fff; }
.stButton > button { background: #0f172a !important; color: #fff !important; border-radius: 8px !important; }
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
        
        st.markdown("<p style='text-align:center;font-size:11px;'>Usuário: Juan | Senha: Ju@n1990</p>", unsafe_allow_html=True)
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

def stacked_bar(df, title, cores, col_group, col_stack):
    if df.empty:
        return "<div class='chart-card'>Sem dados</div>"
    
    pivot = df.groupby([col_group, col_stack]).size().unstack(fill_value=0)
    cats = list(pivot.columns)
    tmax = pivot.sum(axis=1).max() or 1

    legend = "".join([f"<span style='margin-right:12px'><span style='background:{cores.get(c,'#ccc')};display:inline-block;width:10px;height:10px;border-radius:3px;'></span> {c}</span>" for c in cats])

    bars = ""
    for idx, row in pivot.iterrows():
        total = row.sum() or 1
        segs = ""
        for cat in cats:
            val = row.get(cat, 0)
            pct = (val / total) * 100
            if pct > 0:
                segs += f"<div class='sbar-seg' style='width:{pct}%;background:{cores.get(cat,'#ccc')};'>{val if pct > 8 else ''}</div>"
        w = max((total / tmax) * 100, 10)
        bars += f"""
        <div style='margin-bottom:12px'>
            <div style='display:flex;justify-content:space-between;margin-bottom:4px'><span>{str(idx)[:35]}</span><b>{int(total)}</b></div>
            <div class='sbar-track' style='width:{w}%'>{segs}</div>
        </div>"""
    
    return f"<div class='chart-card'><div class='chart-title'>{title}</div>{bars}<div style='margin-top:12px'>{legend}</div></div>"

def mcard(num, lbl, cor):
    return f"<div class='mcard'><div class='mcard-num {cor}'>{num}</div><div class='mcard-lbl'>{lbl}</div></div>"

def sec(t):
    st.markdown(f"<div class='sec-title'>{t}</div>", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# INICIALIZAR SUPABASE
# ──────────────────────────────────────────────
supabase = init_supabase()

if supabase:
    st.success("✅ Conectado ao Supabase - Dados salvos na nuvem!")
else:
    st.error("❌ Erro ao conectar ao Supabase")

# ──────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div class='sb-logo'>🛡️ SecureOps</div>", unsafe_allow_html=True)
    st.markdown("<div class='sb-sub'>Gestão de Segurança</div>", unsafe_allow_html=True)
    st.markdown("<hr class='sb-div'>", unsafe_allow_html=True)
    st.markdown(f"**{st.session_state.usuario}**", unsafe_allow_html=True)
    st.markdown("<div class='sb-role'>Administrador</div>", unsafe_allow_html=True)
    st.markdown("<hr class='sb-div'>", unsafe_allow_html=True)
    st.markdown("<div class='sb-lbl'>Resumo</div>", unsafe_allow_html=True)
    sidebar_ph = st.empty()
    st.markdown("<hr class='sb-div'>", unsafe_allow_html=True)
    st.markdown(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}", unsafe_allow_html=True)
    st.markdown("<hr class='sb-div'>", unsafe_allow_html=True)
    
    if st.button("🚪 Sair", use_container_width=True):
        fazer_logout()

# ──────────────────────────────────────────────
# CABEÇALHO
# ──────────────────────────────────────────────
st.markdown("<div class='page-title'>SecureOps - Gestão de Segurança</div>", unsafe_allow_html=True)
st.markdown("<div class='page-sub'>PDCA + Análise de Risco com Supabase (Dados na Nuvem)</div>", unsafe_allow_html=True)

# Carregar dados do Supabase ou criar padrão
if supabase:
    dados_risco_carregado = carregar_riscos_supabase(supabase)
    dados_eq_carregado = carregar_equipamentos_supabase(supabase)
else:
    dados_risco_carregado = None
    dados_eq_carregado = None

if dados_risco_carregado is not None and not dados_risco_carregado.empty:
    edited_risco = dados_risco_carregado
    st.info("📀 Dados carregados do Supabase (nuvem)")
else:
    edited_risco = pd.DataFrame({
        "Ativo": ["Cabos na sala", "Pen drive", "Servidor internet", "Switch", "Firewall", "Router"],
        "Localidade": ["Sala A", "TI Sala 210", "DC Rack 05", "Sala rede", "DC Rack 02", "DC Rack 01"],
        "Ameaça": ["Rompimento", "Vírus", "Invasão", "Desligamento", "DDoS", "Configuração"],
        "Vulnerabilidade": ["Cabos soltos", "Antivírus antigo", "Rede interna", "Sem trava", "Firmware", "Senha fraca"],
        "Probabilidade": ["Baixa", "Alta", "Média", "Média", "Baixa", "Média"],
        "Impacto": ["Alto", "Alto", "Alto", "Médio", "Alto", "Alto"],
    })
    edited_risco["Nível do Risco"] = edited_risco.apply(lambda r: nivel_risco(r["Probabilidade"], r["Impacto"]), axis=1)

if dados_eq_carregado is not None and not dados_eq_carregado.empty:
    edited_eq = dados_eq_carregado
else:
    edited_eq = pd.DataFrame({
        "Equipamento": ["Firewall Fortinet", "Switch Core Huawei", "Router Cisco", "Servidor Dell", "Storage EMC", "Access Point", "Patch Panel"],
        "Tipo": ["Segurança", "Rede", "Rede", "Servidor", "Storage", "Rede", "Infraestrutura"],
        "Localidade": ["DC Rack 02", "DC Rack 01", "DC Rack 01", "DC Rack 03", "DC Rack 04", "Sala 210", "Sala servidores"],
        "Fabricante": ["Fortinet", "Huawei", "Cisco", "Dell", "EMC", "Ubiquiti", "Intelbras"],
        "Modelo": ["FG-100F", "S12700", "ISR4321", "R750", "XT380", "U6-LR", "CAT6"],
        "Status": ["Ativo", "Ativo", "Ativo", "Ativo", "Ativo", "Ativo", "Ativo"],
        "Motivo": ["", "", "", "", "", "", ""],
    })

tab_dados, tab_graficos, tab_historico = st.tabs(["📋 Dados", "📊 Gráficos", "📜 Histórico"])

# ══════════════════════════════════════════════
# TAB DADOS
# ══════════════════════════════════════════════
with tab_dados:
    sec("Análise de Risco")
    edited_risco = st.data_editor(
        edited_risco, use_container_width=True, num_rows="dynamic",
        column_config={
            "Probabilidade": st.column_config.SelectboxColumn(options=["Baixa", "Média", "Alta"]),
            "Impacto": st.column_config.SelectboxColumn(options=["Baixo", "Médio", "Alto"]),
            "Nível do Risco": st.column_config.TextColumn(disabled=True),
        }, hide_index=True,
    )
    edited_risco["Nível do Risco"] = edited_risco.apply(lambda r: nivel_risco(r["Probabilidade"], r["Impacto"]), axis=1)

    sec("Inventário de Equipamentos")
    edited_eq = st.data_editor(
        edited_eq, use_container_width=True, num_rows="dynamic",
        column_config={
            "Tipo": st.column_config.SelectboxColumn(options=["Segurança", "Rede", "Servidor", "Storage", "Infraestrutura"]),
            "Status": st.column_config.SelectboxColumn(options=["Ativo", "Em Manutenção", "Desativado", "Reserva"]),
        }, hide_index=True,
    )

    st.markdown("---")
    st.markdown("### 💾 Salvar no Supabase (Nuvem)")
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        if st.button("☁️ Salvar no Supabase", use_container_width=True):
            if supabase:
                if salvar_riscos_supabase(supabase, edited_risco, st.session_state.usuario):
                    st.success("✅ Riscos salvos na nuvem!")
                if salvar_equipamentos_supabase(supabase, edited_eq, st.session_state.usuario):
                    st.success("✅ Equipamentos salvos na nuvem!")
            else:
                st.error("❌ Supabase não conectado")
    
    with col_s2:
        if st.button("📥 Exportar Excel", use_container_width=True):
            with pd.ExcelWriter(f"relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx") as writer:
                edited_risco.to_excel(writer, sheet_name="Riscos", index=False)
                edited_eq.to_excel(writer, sheet_name="Equipamentos", index=False)
            st.success("Excel exportado!")

# ══════════════════════════════════════════════
# TAB GRÁFICOS
# ══════════════════════════════════════════════
with tab_graficos:
    st.markdown("### 📊 Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(mcard(len(edited_risco), "Total Riscos", "c-blue"), unsafe_allow_html=True)
    with col2:
        st.markdown(mcard(len(edited_risco[edited_risco["Nível do Risco"] == "🔴 Alto"]), "Riscos Altos", "c-red"), unsafe_allow_html=True)
    with col3:
        st.markdown(mcard(len(edited_risco[edited_risco["Nível do Risco"] == "🟡 Médio"]), "Riscos Médios", "c-yellow"), unsafe_allow_html=True)
    with col4:
        st.markdown(mcard(len(edited_risco[edited_risco["Nível do Risco"] == "🟢 Baixo"]), "Riscos Baixos", "c-green"), unsafe_allow_html=True)
    
    st.markdown("---")
    
    CORES_RISCO = {"🔴 Alto": "#dc2626", "🟡 Médio": "#d97706", "🟢 Baixo": "#16a34a"}
    CORES_TIPO = {"Segurança": "#2563eb", "Rede": "#7c3aed", "Servidor": "#0891b2", "Storage": "#059669", "Infraestrutura": "#d97706"}
    CORES_STATUS = {"Ativo": "#16a34a", "Em Manutenção": "#d97706", "Desativado": "#dc2626", "Reserva": "#64748b"}
    
    st.markdown(stacked_bar(edited_risco, "Riscos por Localidade", CORES_RISCO, "Localidade", "Nível do Risco"), unsafe_allow_html=True)
    st.markdown(stacked_bar(edited_eq, "Equipamentos por Localidade", CORES_TIPO, "Localidade", "Tipo"), unsafe_allow_html=True)
    st.markdown(stacked_bar(edited_eq, "Status dos Equipamentos", CORES_STATUS, "Status", "Tipo"), unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB HISTÓRICO
# ══════════════════════════════════════════════
with tab_historico:
    st.markdown("### 📜 Histórico de Alterações")
    
    tipo_filtro = st.selectbox("Filtrar:", ["Todos", "analise_risco", "equipamentos"])
    
    if supabase:
        df_hist = carregar_historico_supabase(supabase, tipo_filtro)
        if not df_hist.empty:
            st.dataframe(df_hist, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum registro no histórico. Clique em 'Salvar no Supabase' para começar.")
    else:
        st.warning("Conecte ao Supabase para ver o histórico")

# ──────────────────────────────────────────────
# SIDEBAR ATUALIZADA
# ──────────────────────────────────────────────
with sidebar_ph:
    alto = len(edited_risco[edited_risco["Nível do Risco"] == "🔴 Alto"])
    medio = len(edited_risco[edited_risco["Nível do Risco"] == "🟡 Médio"])
    baixo = len(edited_risco[edited_risco["Nível do Risco"] == "🟢 Baixo"])
    st.markdown(f"""
    <div class='sb-badge sb-red'>🔴 Alto <span class='sb-num'>{alto}</span></div>
    <div class='sb-badge sb-yellow'>🟡 Médio <span class='sb-num'>{medio}</span></div>
    <div class='sb-badge sb-green'>🟢 Baixo <span class='sb-num'>{baixo}</span></div>
    """, unsafe_allow_html=True)

st.success("✅ **Sistema completo!** Dados salvos permanentemente no Supabase na nuvem!")
