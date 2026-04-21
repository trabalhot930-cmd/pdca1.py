import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
from supabase import create_client, Client
import json

st.set_page_config(
    layout="wide",
    page_title="SecureOps — Gestão de Segurança",
    page_icon="🛡️",
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────
# CONFIGURAÇÃO DO SUPABASE
# ──────────────────────────────────────────────
SUPABASE_URL = "https://bhwqrfolkusuzvwavanc.supabase.co"
SUPABASE_KEY = "sb_publishable_J_z2LmOOVT0cmJuYhqW0qg_9iAEHt4u"

def init_supabase():
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except:
        return None

# ──────────────────────────────────────────────
# FUNÇÕES DO SUPABASE
# ──────────────────────────────────────────────
def salvar_riscos_supabase(supabase, df_riscos, usuario):
    if not supabase:
        return False
    try:
        supabase.table("riscos_atuais").delete().neq("id", 0).execute()
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
        supabase.table("historico_seguranca").insert({
            "tipo": "analise_risco",
            "dados": json.dumps(df_riscos.to_dict('records')),
            "usuario": usuario
        }).execute()
        return True
    except:
        return False

def carregar_riscos_supabase(supabase):
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
    except:
        return None

def salvar_equipamentos_supabase(supabase, df_eq, usuario):
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
    except:
        return False

def carregar_equipamentos_supabase(supabase):
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
    except:
        return None

def salvar_pdca_supabase(supabase, dados_pdca, usuario):
    """Salva PDCA no Supabase"""
    if not supabase:
        return False
    try:
        supabase.table("pdca").delete().neq("id", 0).execute()
        for key, value in dados_pdca.items():
            fase_idx, linha_idx = key
            fases = ["1. Contexto", "2. Liderança", "3. Planejamento", "4. Suporte", "5. Operação", "6. Avaliação", "7. Melhoria"]
            linhas = ["Objetivo Estratégico", "Ação Técnica", "Indicador (KPI)", "Evidência / Status"]
            
            supabase.table("pdca").insert({
                "fase": fases[fase_idx],
                "linha": linhas[linha_idx],
                "conteudo": value,
                "usuario": usuario
            }).execute()
        
        supabase.table("historico_seguranca").insert({
            "tipo": "pdca",
            "dados": json.dumps(dados_pdca),
            "usuario": usuario
        }).execute()
        return True
    except:
        return False

def carregar_pdca_supabase(supabase):
    """Carrega PDCA do Supabase"""
    if not supabase:
        return {}
    try:
        response = supabase.table("pdca").select("*").execute()
        if response.data:
            dados_pdca = {}
            for item in response.data:
                fase = item["fase"]
                linha = item["linha"]
                # Encontrar índices
                fases = ["1. Contexto", "2. Liderança", "3. Planejamento", "4. Suporte", "5. Operação", "6. Avaliação", "7. Melhoria"]
                linhas = ["Objetivo Estratégico", "Ação Técnica", "Indicador (KPI)", "Evidência / Status"]
                
                if fase in fases and linha in linhas:
                    i = fases.index(fase)
                    j = linhas.index(linha)
                    dados_pdca[(i, j)] = item["conteudo"]
            return dados_pdca
        return {}
    except:
        return {}

def carregar_historico_supabase(supabase, tipo=None):
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
    except:
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
.chart-title { font-size: 14px; font-weight: 600; border-left: 3px solid #2563eb; padding-left: 10px; margin-bottom: 16px; }
.pdca-header { background: #f8fafc; border-radius: 8px; padding: 10px; text-align: center; margin-bottom: 10px; border: 1px solid #e2e8f0; }
.pdca-row-lbl { font-size: 12px; font-weight: 600; color: #475569; padding: 8px 0 4px; border-bottom: 1px solid #e2e8f0; margin: 8px 0 4px; }
.stButton > button { background: #0f172a !important; color: #fff !important; border-radius: 8px !important; }
.status-ativo { color: #16a34a; font-weight: 600; }
.status-inativo { color: #dc2626; font-weight: 600; }
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
def obter_hora_brasil():
    fuso_br = pytz.timezone('America/Sao_Paulo')
    return datetime.now(fuso_br)

def nivel_risco(prob, imp):
    prob = str(prob).lower().strip()
    imp = str(imp).lower().strip()
    if (prob == "baixa" and imp in ["baixo", "médio"]) or (prob == "média" and imp == "baixo"):
        return "🟢 Baixo"
    elif (prob == "baixa" and imp == "alto") or (prob == "média" and imp == "médio") or (prob == "alta" and imp == "baixo"):
        return "🟡 Médio"
    else:
        return "🔴 Alto"

def grafico_rosca(dados, titulo, cores):
    if not dados or sum(dados.values()) == 0:
        return "<div class='chart-card'>Sem dados</div>"
    
    total = sum(dados.values())
    gradiente = []
    angulo_atual = 0
    for label, valor in dados.items():
        percentual = (valor / total) * 360
        cor = cores.get(label, "#ccc")
        gradiente.append(f"{cor} {angulo_atual}deg {angulo_atual + percentual}deg")
        angulo_atual += percentual
    
    legenda = ""
    for label, valor in dados.items():
        percentual = (valor / total) * 100
        cor = cores.get(label, "#ccc")
        legenda += f"""
        <div style='display:flex; align-items:center; margin-bottom:8px;'>
            <div style='width:12px; height:12px; background:{cor}; border-radius:2px; margin-right:8px;'></div>
            <span style='flex:1; font-size:12px;'>{label}</span>
            <span style='font-weight:600;'>{valor} ({percentual:.1f}%)</span>
        </div>
        """
    
    return f"""
    <div class='chart-card'>
        <div class='chart-title'>{titulo}</div>
        <div style='display: flex; align-items: center; gap: 20px; flex-wrap: wrap;'>
            <div style='position: relative; width: 150px; height: 150px;'>
                <div style='position: absolute; width: 100%; height: 100%; border-radius: 50%; background: conic-gradient({', '.join(gradiente)});'></div>
                <div style='position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 70px; height: 70px; background: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-direction: column;'>
                    <div style='font-size: 20px; font-weight: 700;'>{total}</div>
                    <div style='font-size: 10px; color: #666;'>Total</div>
                </div>
            </div>
            <div style='flex: 1; min-width: 150px;'>{legenda}</div>
        </div>
    </div>
    """

def mcard(num, lbl, cor):
    return f"<div class='mcard'><div class='mcard-num {cor}'>{num}</div><div class='mcard-lbl'>{lbl}</div></div>"

def sec(t):
    st.markdown(f"<div class='sec-title'>{t}</div>", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# INICIALIZAR SUPABASE
# ──────────────────────────────────────────────
supabase = init_supabase()

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
    
    hora_br = obter_hora_brasil()
    st.markdown(f"📅 {hora_br.strftime('%d/%m/%Y')}", unsafe_allow_html=True)
    st.markdown(f"🕐 {hora_br.strftime('%H:%M:%S')}", unsafe_allow_html=True)
    st.markdown("<hr class='sb-div'>", unsafe_allow_html=True)
    
    if st.button("🚪 Sair", use_container_width=True):
        fazer_logout()

# ──────────────────────────────────────────────
# CABEÇALHO
# ──────────────────────────────────────────────
hora_br = obter_hora_brasil()
st.markdown(f"""
<div class='page-title'>SecureOps - Gestão de Segurança</div>
<div class='page-sub'>PDCA + Análise de Risco · {hora_br.strftime('%d/%m/%Y %H:%M')}</div>
""", unsafe_allow_html=True)

# Carregar dados
if supabase:
    dados_risco_carregado = carregar_riscos_supabase(supabase)
    dados_eq_carregado = carregar_equipamentos_supabase(supabase)
    dados_pdca_carregado = carregar_pdca_supabase(supabase)
else:
    dados_risco_carregado = None
    dados_eq_carregado = None
    dados_pdca_carregado = {}

if dados_risco_carregado is not None and not dados_risco_carregado.empty:
    edited_risco = dados_risco_carregado
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

# Abas
tab_dados, tab_graficos, tab_pdca, tab_historico = st.tabs(["📋 Dados", "📊 Gráficos", "🔄 PDCA", "📜 Histórico"])

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
            "Status": st.column_config.SelectboxColumn(options=["Ativo", "Inativo", "Em Manutenção", "Reserva"]),
        }, hide_index=True,
    )

    st.markdown("---")
    st.markdown("### 💾 Salvar no Supabase")
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        if st.button("☁️ Salvar Dados", use_container_width=True):
            if supabase:
                ok1 = salvar_riscos_supabase(supabase, edited_risco, st.session_state.usuario)
                ok2 = salvar_equipamentos_supabase(supabase, edited_eq, st.session_state.usuario)
                if ok1 and ok2:
                    st.success("✅ Dados salvos na nuvem!")
                else:
                    st.error("❌ Erro ao salvar")
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
    st.markdown("### 📊 Dashboard de Gráficos")
    
    # Filtro por localidade
    st.markdown("#### 🔍 Filtros")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        localidades_risco = ["Todas"] + sorted(edited_risco["Localidade"].unique().tolist())
        filtro_local_risco = st.selectbox("Filtrar Riscos por Localidade:", localidades_risco)
    
    with col_f2:
        localidades_eq = ["Todas"] + sorted(edited_eq["Localidade"].unique().tolist())
        filtro_local_eq = st.selectbox("Filtrar Equipamentos por Localidade:", localidades_eq)
    
    # Aplicar filtros
    risco_filtrado = edited_risco if filtro_local_risco == "Todas" else edited_risco[edited_risco["Localidade"] == filtro_local_risco]
    eq_filtrado = edited_eq if filtro_local_eq == "Todas" else edited_eq[edited_eq["Localidade"] == filtro_local_eq]
    
    st.markdown("---")
    
    # Métricas
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(mcard(len(risco_filtrado), "Total Riscos", "c-blue"), unsafe_allow_html=True)
    with col2:
        st.markdown(mcard(len(risco_filtrado[risco_filtrado["Nível do Risco"] == "🔴 Alto"]), "Riscos Altos", "c-red"), unsafe_allow_html=True)
    with col3:
        st.markdown(mcard(len(eq_filtrado), "Equipamentos", "c-green"), unsafe_allow_html=True)
    with col4:
        st.markdown(mcard(len(eq_filtrado[eq_filtrado["Status"] == "Ativo"]), "Equipamentos Ativos", "c-green"), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Gráficos em rosca
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        # Gráfico de riscos por nível
        risco_nivel = risco_filtrado["Nível do Risco"].value_counts().to_dict()
        cores_risco = {"🔴 Alto": "#dc2626", "🟡 Médio": "#d97706", "🟢 Baixo": "#16a34a"}
        st.markdown(grafico_rosca(risco_nivel, "Distribuição de Riscos", cores_risco), unsafe_allow_html=True)
    
    with col_g2:
        # Gráfico de status dos equipamentos
        status_eq = eq_filtrado["Status"].value_counts().to_dict()
        cores_status = {"Ativo": "#16a34a", "Inativo": "#dc2626", "Em Manutenção": "#d97706", "Reserva": "#64748b"}
        st.markdown(grafico_rosca(status_eq, "Status dos Equipamentos", cores_status), unsafe_allow_html=True)
    
    col_g3, col_g4 = st.columns(2)
    
    with col_g3:
        # Gráfico de riscos por localidade (top 5)
        risco_local = risco_filtrado["Localidade"].value_counts().head(5).to_dict()
        if risco_local:
            st.markdown(grafico_rosca(risco_local, "Top Localidades com Riscos", {"default": "#2563eb"}), unsafe_allow_html=True)
    
    with col_g4:
        # Gráfico de equipamentos por tipo
        tipo_eq = eq_filtrado["Tipo"].value_counts().to_dict()
        cores_tipo = {"Segurança": "#2563eb", "Rede": "#7c3aed", "Servidor": "#0891b2", "Storage": "#059669", "Infraestrutura": "#d97706"}
        st.markdown(grafico_rosca(tipo_eq, "Equipamentos por Tipo", cores_tipo), unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB PDCA (COMPLETO)
# ══════════════════════════════════════════════
with tab_pdca:
    st.markdown("### 🔄 PDCA de Controle de Acesso")
    st.markdown("Preencha as 7 fases do ciclo PDCA para gestão de segurança")
    
    fases = [
        {"nome": "1. Contexto", "fase": "PLAN", "cor": "#2563eb", "desc": "Análise do ambiente"},
        {"nome": "2. Liderança", "fase": "PLAN", "cor": "#2563eb", "desc": "Comprometimento"},
        {"nome": "3. Planejamento", "fase": "PLAN", "cor": "#2563eb", "desc": "Objetivos e riscos"},
        {"nome": "4. Suporte", "fase": "DO", "cor": "#d97706", "desc": "Recursos e treinamento"},
        {"nome": "5. Operação", "fase": "DO", "cor": "#d97706", "desc": "Controles operacionais"},
        {"nome": "6. Avaliação", "fase": "CHECK", "cor": "#16a34a", "desc": "Monitoramento"},
        {"nome": "7. Melhoria", "fase": "ACT", "cor": "#7c3aed", "desc": "Ações corretivas"},
    ]
    
    linhas_pdca = [
        "🎯 Objetivo Estratégico",
        "⚙️ Ação Técnica (TI/OT)",
        "📊 Indicador (KPI)",
        "🚩 Evidência / Status",
    ]
    
    cols = st.columns(len(fases), gap="small")
    dados_pdca = {}
    
    # Carregar dados salvos
    if dados_pdca_carregado:
        st.info("📀 PDCA carregado do Supabase")
        dados_pdca = dados_pdca_carregado
    
    for i, (col, fase) in enumerate(zip(cols, fases)):
        with col:
            st.markdown(f"""
            <div class='pdca-header' style='background:{fase["cor"]}10; border:1px solid {fase["cor"]}30;'>
                <div style='font-size:10px; font-weight:700; color:{fase["cor"]}; text-transform:uppercase;'>{fase["fase"]}</div>
                <div style='font-size:13px; font-weight:700; color:{fase["cor"]};'>{fase["nome"]}</div>
                <div style='font-size:9px; color:#64748b;'>{fase["desc"]}</div>
            </div>
            """, unsafe_allow_html=True)
            
            for j, linha in enumerate(linhas_pdca):
                if i == 0:
                    st.markdown(f"<div class='pdca-row-lbl'>{linha}</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='height:34px;'></div>", unsafe_allow_html=True)
                
                key = f"pdca_{i}_{j}"
                valor_padrao = dados_pdca.get((i, j), "")
                dados_pdca[(i, j)] = st.text_area(
                    label="", key=key,
                    placeholder=f"Digite o {linha.lower()}...",
                    label_visibility="collapsed",
                    height=85,
                    value=valor_padrao
                )
    
    st.markdown("---")
    col_p1, col_p2, col_p3 = st.columns([1, 1, 2])
    
    with col_p1:
        if st.button("💾 Salvar PDCA", use_container_width=True):
            if supabase:
                if salvar_pdca_supabase(supabase, dados_pdca, st.session_state.usuario):
                    st.success("✅ PDCA salvo na nuvem!")
                else:
                    st.error("❌ Erro ao salvar PDCA")
            else:
                st.error("❌ Supabase não conectado")
    
    with col_p2:
        if st.button("📋 Gerar Relatório PDCA", use_container_width=True):
            # Gerar HTML do PDCA
            pdca_html = "<div style='font-family: Arial; padding: 20px;'>"
            pdca_html += "<h2 style='color:#2563eb'>Relatório PDCA - Controle de Acesso</h2>"
            pdca_html += f"<p>Data: {hora_br.strftime('%d/%m/%Y %H:%M')}</p><hr>"
            
            for i, fase in enumerate(fases):
                pdca_html += f"<div style='margin-bottom: 30px;'>"
                pdca_html += f"<h3 style='color:{fase['cor']}; border-left: 4px solid {fase['cor']}; padding-left: 10px;'>{fase['nome']} ({fase['fase']})</h3>"
                for j, linha in enumerate(linhas_pdca):
                    conteudo = dados_pdca.get((i, j), "")
                    pdca_html += f"<div style='margin-bottom: 15px;'>"
                    pdca_html += f"<strong>{linha}:</strong><br>"
                    pdca_html += f"<div style='background:#f8fafc; padding: 10px; border-radius: 8px; margin-top: 5px;'>{conteudo if conteudo else '—'}</div>"
                    pdca_html += f"</div>"
                pdca_html += "</div><hr>"
            pdca_html += "</div>"
            
            st.download_button(
                label="📥 Baixar Relatório PDCA (HTML)",
                data=pdca_html,
                file_name=f"relatorio_pdca_{hora_br.strftime('%Y%m%d_%H%M%S')}.html",
                mime="text/html",
                use_container_width=True
            )

# ══════════════════════════════════════════════
# TAB HISTÓRICO
# ══════════════════════════════════════════════
with tab_historico:
    st.markdown("### 📜 Histórico de Alterações")
    
    tipo_filtro = st.selectbox("Filtrar:", ["Todos", "analise_risco", "equipamentos", "pdca"])
    
    if supabase:
        df_hist = carregar_historico_supabase(supabase, tipo_filtro)
        if not df_hist.empty:
            st.dataframe(df_hist, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum registro no histórico. Clique em 'Salvar' para começar.")
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
