import streamlit as st
import pandas as pd
from datetime import datetime
import sqlite3
import os

st.set_page_config(
    layout="wide",
    page_title="SecureOps — Gestão de Segurança",
    page_icon="🛡️",
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────
# BANCO DE DADOS SQLITE (PERMANENTE)
# ──────────────────────────────────────────────
DB_NAME = "secureops.db"

def init_database():
    """Inicializa o banco de dados"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Tabela de histórico
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            dados TEXT,
            usuario TEXT NOT NULL,
            data TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    
    # Tabela de configurações
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS configuracoes (
            chave TEXT PRIMARY KEY,
            valor TEXT,
            atualizado_em TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def salvar_historico_db(tipo, dados, usuario):
    """Salva histórico no SQLite"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Converter dados para string
        dados_str = str(dados)
        
        cursor.execute('''
            INSERT INTO historico (tipo, dados, usuario, data, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            tipo,
            dados_str[:5000],  # Limitar tamanho
            usuario,
            datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Erro ao salvar: {e}")
        return False

def carregar_historico_db(tipo=None):
    """Carrega histórico do SQLite"""
    try:
        conn = sqlite3.connect(DB_NAME)
        
        if tipo and tipo != "Todos":
            query = "SELECT id, tipo, usuario, data FROM historico WHERE tipo = ? ORDER BY id DESC"
            df = pd.read_sql_query(query, conn, params=(tipo,))
        else:
            query = "SELECT id, tipo, usuario, data FROM historico ORDER BY id DESC"
            df = pd.read_sql_query(query, conn)
        
        conn.close()
        return df
    except Exception as e:
        return pd.DataFrame()

def limpar_historico_db():
    """Limpa todo o histórico"""
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.execute("DELETE FROM historico")
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

def salvar_risco_db(df_risco):
    """Salva análise de risco atual"""
    try:
        conn = sqlite3.connect(DB_NAME)
        df_risco.to_sql('risco_atual', conn, if_exists='replace', index=False)
        conn.close()
        return True
    except:
        return False

def carregar_risco_db():
    """Carrega análise de risco salva"""
    try:
        conn = sqlite3.connect(DB_NAME)
        df = pd.read_sql_query("SELECT * FROM risco_atual", conn)
        conn.close()
        return df
    except:
        return None

def salvar_equipamento_db(df_eq):
    """Salva equipamentos atuais"""
    try:
        conn = sqlite3.connect(DB_NAME)
        df_eq.to_sql('equipamentos_atual', conn, if_exists='replace', index=False)
        conn.close()
        return True
    except:
        return False

def carregar_equipamento_db():
    """Carrega equipamentos salvos"""
    try:
        conn = sqlite3.connect(DB_NAME)
        df = pd.read_sql_query("SELECT * FROM equipamentos_atual", conn)
        conn.close()
        return df
    except:
        return None

# Inicializar banco
init_database()

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
html, body, [class*="css"] { font-family: 'Inter', sans-serif; font-size: 14px; color: #1e293b; }

[data-testid="stAppViewContainer"] { background: #f8fafc; }
[data-testid="stSidebar"] { background: #f1f5f9 !important; border-right: 1px solid #e2e8f0 !important; }

.block-container { padding: 1.5rem 2rem 2rem !important; }

.sb-logo { font-size: 20px; font-weight: 700; color: #0f172a; padding: 1rem 0 0.2rem; }
.sb-sub { font-size: 11px; color: #64748b; }
.sb-div { border-top: 1px solid #e2e8f0; margin: 0.8rem 0; }
.sb-lbl { font-size: 10px; font-weight: 600; text-transform: uppercase; color: #64748b; }
.sb-user { font-size: 14px; font-weight: 600; color: #0f172a; }
.sb-role { font-size: 11px; color: #64748b; }
.sb-badge { display: flex; justify-content: space-between; padding: 8px 12px; border-radius: 8px; margin-bottom: 6px; }
.sb-red { background: #fee2e2; color: #dc2626; }
.sb-yellow { background: #fef3c7; color: #d97706; }
.sb-green { background: #dcfce7; color: #16a34a; }
.sb-num { font-size: 18px; font-weight: 700; }

.stTabs [data-baseweb="tab-list"] { gap: 0; background: #e2e8f0; padding: 4px; border-radius: 10px; }
.stTabs [data-baseweb="tab"] { padding: 6px 20px; font-size: 13px; color: #64748b; }
.stTabs [aria-selected="true"] { background: #fff; color: #0f172a; }

.page-title { font-size: 24px; font-weight: 700; color: #0f172a; }
.page-sub { font-size: 13px; color: #64748b; margin-bottom: 1.2rem; }

.sec-title { font-size: 11px; font-weight: 600; text-transform: uppercase; color: #94a3b8; margin: 1.5rem 0 0.8rem; border-bottom: 1px solid #e2e8f0; }

.mcard { background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px; }
.mcard-num { font-size: 32px; font-weight: 700; }
.mcard-lbl { font-size: 12px; color: #64748b; }
.c-blue { color: #2563eb; }
.c-red { color: #dc2626; }
.c-green { color: #16a34a; }

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

CORES_RISCO = {"🔴 Alto": "#dc2626", "🟡 Médio": "#d97706", "🟢 Baixo": "#16a34a"}
CORES_TIPO = {"Segurança": "#2563eb", "Rede": "#7c3aed", "Servidor": "#0891b2", "Storage": "#059669", "Infraestrutura": "#d97706"}
CORES_STATUS = {"Ativo": "#16a34a", "Em Manutenção": "#d97706", "Desativado": "#dc2626", "Reserva": "#64748b"}

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
# SIDEBAR
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div class='sb-logo'>🛡️ SecureOps</div>", unsafe_allow_html=True)
    st.markdown("<div class='sb-sub'>Gestão de Segurança</div>")
    st.markdown("<hr class='sb-div'>")
    st.markdown(f"<div class='sb-user'>{st.session_state.usuario}</div>", unsafe_allow_html=True)
    st.markdown("<div class='sb-role'>Administrador</div>")
    st.markdown("<hr class='sb-div'>")
    st.markdown("<div class='sb-lbl'>Resumo</div>")
    sidebar_ph = st.empty()
    st.markdown("<hr class='sb-div'>")
    st.markdown(f"<div class='sb-lbl'>📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}</div>", unsafe_allow_html=True)
    st.markdown("<hr class='sb-div'>")
    
    if st.button("🚪 Sair", use_container_width=True):
        fazer_logout()

# ──────────────────────────────────────────────
# CABEÇALHO
# ──────────────────────────────────────────────
st.markdown(f"""
<div class='page-title'>SecureOps - Gestão de Segurança</div>
<div class='page-sub'>PDCA + Análise de Risco · Dados salvos em banco local</div>
""", unsafe_allow_html=True)

# Carregar dados salvos ou criar novos
dados_risco_carregado = carregar_risco_db()
dados_eq_carregado = carregar_equipamento_db()

if dados_risco_carregado is not None:
    edited_risco = dados_risco_carregado
    st.info("📀 Dados de risco carregados do banco")
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

if dados_eq_carregado is not None:
    edited_eq = dados_eq_carregado
    st.info("💾 Dados de equipamentos carregados do banco")
else:
    edited_eq = pd.DataFrame({
        "Equipamento": ["Firewall", "Switch", "Router", "Servidor", "Storage", "Access Point", "Patch Panel"],
        "Tipo": ["Segurança", "Rede", "Rede", "Servidor", "Storage", "Rede", "Infra"],
        "Localidade": ["DC Rack 02", "DC Rack 01", "DC Rack 01", "DC Rack 03", "DC Rack 04", "Sala 210", "Sala server"],
        "Fabricante": ["Fortinet", "Huawei", "Cisco", "Dell", "EMC", "Ubiquiti", "Intelbras"],
        "Modelo": ["FG-100F", "S12700", "ISR4321", "R750", "XT380", "U6-LR", "CAT6"],
        "Status": ["Ativo", "Ativo", "Ativo", "Ativo", "Ativo", "Ativo", "Ativo"],
        "Motivo": ["", "", "", "", "", "", ""],
    })

tab_dados, tab_graficos, tab_pdca, tab_historico = st.tabs(["📋 Dados", "📊 Gráficos", "🔄 PDCA", "📜 Histórico"])

# ══════════════════════════════════════════════
# TAB DADOS
# ══════════════════════════════════════════════
with tab_dados:
    st.markdown("### 📋 Gestão de Dados")
    st.success("💾 **Dados são salvos automaticamente no banco SQLite!** Feche e reabra que os dados continuam.")
    
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

    # Botões de salvamento
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        if st.button("💾 SALVAR DADOS NO BANCO", use_container_width=True):
            salvar_risco_db(edited_risco)
            salvar_equipamento_db(edited_eq)
            salvar_historico_db("analise_risco", edited_risco, st.session_state.usuario)
            st.success("✅ Dados salvos permanentemente!")
    
    with col_s2:
        if st.button("📥 Exportar Excel", use_container_width=True):
            with pd.ExcelWriter(f"relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx") as writer:
                edited_risco.to_excel(writer, sheet_name="Riscos", index=False)
                edited_eq.to_excel(writer, sheet_name="Equipamentos", index=False)
            st.success("Excel exportado!")
    
    with col_s3:
        if st.button("📊 Ver Métricas", use_container_width=True):
            st.metric("Total Riscos", len(edited_risco))
            st.metric("Riscos Altos", len(edited_risco[edited_risco["Nível do Risco"] == "🔴 Alto"]))
            st.metric("Equipamentos", len(edited_eq))

# ══════════════════════════════════════════════
# TAB GRÁFICOS
# ══════════════════════════════════════════════
with tab_graficos:
    st.markdown("### 📊 Dashboard")
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.markdown(mcard(len(edited_risco), "Total Riscos", "c-blue"), unsafe_allow_html=True)
    with col2: st.markdown(mcard(len(edited_risco[edited_risco["Nível do Risco"] == "🔴 Alto"]), "Riscos Altos", "c-red"), unsafe_allow_html=True)
    with col3: st.markdown(mcard(len(edited_eq), "Equipamentos", "c-green"), unsafe_allow_html=True)
    with col4: st.markdown(mcard(edited_eq["Fabricante"].nunique(), "Fabricantes", "c-blue"), unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown(stacked_bar(edited_risco, "Riscos por Localidade", CORES_RISCO, "Localidade", "Nível do Risco"), unsafe_allow_html=True)
    st.markdown(stacked_bar(edited_eq, "Equipamentos por Localidade", CORES_TIPO, "Localidade", "Tipo"), unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB PDCA
# ══════════════════════════════════════════════
with tab_pdca:
    st.markdown("### 🔄 PDCA")
    st.info("Preencha e clique em salvar para manter os dados")
    
    fases = ["1.Contexto", "2.Liderança", "3.Planejamento", "4.Suporte", "5.Operação", "6.Avaliação", "7.Melhoria"]
    linhas = ["🎯 Objetivo", "⚙️ Ação", "📊 KPI", "🚩 Evidência"]
    
    cols = st.columns(7)
    dados_pdca = {}
    
    for i, fase in enumerate(fases):
        with cols[i]:
            st.markdown(f"**{fase}**")
            for j, linha in enumerate(linhas):
                key = f"pdca_{i}_{j}"
                dados_pdca[(i, j)] = st.text_area(linha, key=key, height=80, placeholder="...")
    
    if st.button("💾 Salvar PDCA", use_container_width=True):
        salvar_historico_db("pdca", str(dados_pdca), st.session_state.usuario)
        st.success("PDCA salvo no histórico!")

# ══════════════════════════════════════════════
# TAB HISTÓRICO
# ══════════════════════════════════════════════
with tab_historico:
    st.markdown("### 📜 Histórico")
    
    tipo_filtro = st.selectbox("Filtrar", ["Todos", "analise_risco", "equipamentos", "pdca"])
    df_hist = carregar_historico_db(None if tipo_filtro == "Todos" else tipo_filtro)
    
    if not df_hist.empty:
        st.dataframe(df_hist, use_container_width=True, hide_index=True)
        if st.button("🗑️ Limpar Histórico"):
            limpar_historico_db()
            st.rerun()
    else:
        st.info("Nenhum registro")

# ──────────────────────────────────────────────
# SIDEBAR ATUALIZAÇÃO
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

st.success("✅ **Dados salvos permanentemente em SQLite!** Feche e reabra o app que os dados continuam.")
