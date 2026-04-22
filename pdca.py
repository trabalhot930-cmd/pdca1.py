import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta
from supabase import create_client, Client
import json

st.set_page_config(
    layout="wide",
    page_title="SecureOps — Gestão de Segurança",
    page_icon="🛡️",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
#MainMenu { visibility: hidden !important; }
header[data-testid="stHeader"] { display: none !important; height: 0 !important; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
[data-testid="stStatusWidget"] { display: none !important; }
footer { visibility: hidden !important; height: 0 !important; }
footer:after { display: none !important; }
.viewerBadge_container__1QSob { display: none !important; }
.block-container { padding-top: 0.5rem !important; }

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif !important; }

[data-testid="stSidebar"] { background: #f1f5f9 !important; border-right: 1px solid #e2e8f0 !important; }
.block-container { padding: 1.5rem 2rem 2rem !important; }

.sb-logo { font-size: 20px; font-weight: 700; color: #0f172a; }
.sb-sub { font-size: 11px; color: #64748b; }
.sb-div { border-top: 1px solid #e2e8f0; margin: 0.8rem 0; }
.sb-lbl { font-size: 10px; font-weight: 600; text-transform: uppercase; color: #64748b; }

.page-title { font-size: 24px; font-weight: 700; color: #0f172a; }
.page-sub { font-size: 13px; color: #64748b; margin-bottom: 1.2rem; }
.sec-title { font-size: 11px; font-weight: 600; text-transform: uppercase; color: #94a3b8; border-bottom: 1px solid #e2e8f0; margin: 1.5rem 0 0.8rem; padding-bottom: 4px; }

.mcard { background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px; text-align: center; }
.mcard-num { font-size: 32px; font-weight: 700; }
.mcard-lbl { font-size: 12px; color: #64748b; }
.c-blue { color: #2563eb; }
.c-red { color: #dc2626; }
.c-green { color: #16a34a; }
.c-yellow { color: #d97706; }
.c-purple { color: #7c3aed; }
.c-orange { color: #ea580c; }

.classificacao-publica { background: #dcfce7; color: #166534; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; display: inline-block; }
.classificacao-interna { background: #dbeafe; color: #1e40af; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; display: inline-block; }
.classificacao-restrita { background: #fed7aa; color: #9a3412; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; display: inline-block; }
.classificacao-confidencial { background: #fee2e2; color: #991b1b; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; display: inline-block; }

.matriz-container { display: flex; gap: 12px; margin-bottom: 20px; flex-wrap: wrap; }
.matriz-col { flex: 1; border-radius: 12px; padding: 20px 16px; cursor: pointer; transition: all 0.3s ease; border: 2px solid transparent; text-align: center; min-width: 180px; }
.matriz-col:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(0,0,0,0.12); }
.matriz-col.active { border-width: 3px; transform: translateY(-4px); box-shadow: 0 12px 32px rgba(0,0,0,0.18); }
.matriz-icon { font-size: 36px; margin-bottom: 10px; }
.matriz-title { font-size: 16px; font-weight: 700; margin-bottom: 6px; }
.matriz-desc { font-size: 11px; opacity: 0.8; }

.piramide-container { display: flex; flex-direction: column; align-items: center; gap: 0; margin: 20px auto; width: 100%; }
.piramide-level { display: flex; align-items: center; justify-content: center; gap: 12px; border-radius: 8px; margin-bottom: 4px; cursor: pointer; transition: all 0.25s; position: relative; }
.piramide-level:hover { filter: brightness(1.08); }
.piramide-level-content { font-weight: 600; text-align: center; }
.piramide-level-title { font-size: 13px; font-weight: 700; }
.piramide-level-sub { font-size: 11px; opacity: 0.8; }

.ameaca-card { border-radius: 12px; padding: 16px; margin-bottom: 10px; border-left: 4px solid; }
.ameaca-critica { background: #fef2f2; border-color: #dc2626; }
.ameaca-alta { background: #fff7ed; border-color: #ea580c; }
.ameaca-media { background: #fefce8; border-color: #ca8a04; }
.ameaca-baixa { background: #f0fdf4; border-color: #16a34a; }

.principio-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 16px; margin-bottom: 10px; border-left: 4px solid; transition: box-shadow 0.2s; }
.principio-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.08); }

.stButton > button { background: #0f172a !important; color: #fff !important; border-radius: 8px !important; }
.stButton > button:hover { background: #1e293b !important; }

.info-box { padding: 12px 16px; border-radius: 10px; margin-bottom: 16px; border-left: 4px solid; font-size: 13px; }

/* Grid para métricas */
.metrics-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }
@media (max-width: 768px) { .metrics-grid { grid-template-columns: repeat(2, 1fr); } }

/* Cards de gráficos */
.chart-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 18px; margin-bottom: 16px; height: 100%; }
.chart-title { font-size: 14px; font-weight: 600; border-left: 3px solid #2563eb; padding-left: 10px; margin-bottom: 16px; }

/* Threat lifecycle */
.threat-cycle { display: flex; justify-content: space-between; margin: 20px 0; flex-wrap: wrap; gap: 10px; }
.threat-stage { flex: 1; text-align: center; padding: 15px 8px; border-radius: 12px; color: white; min-width: 100px; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# SUPABASE CONFIG
# ──────────────────────────────────────────────
SUPABASE_URL = "https://bhwqrfolkusuzvwavanc.supabase.co"
SUPABASE_KEY = "sb_publishable_J_z2LmOOVT0cmJuYhqW0qg_9iAEHt4u"

def init_supabase():
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except:
        return None

# ──────────────────────────────────────────────
# SUPABASE - FUNÇÕES
# ──────────────────────────────────────────────
def salvar_riscos_supabase(supabase, df, usuario):
    if not supabase: return False
    try:
        supabase.table("riscos_atuais").delete().neq("id", 0).execute()
        for _, row in df.iterrows():
            supabase.table("riscos_atuais").insert({
                "ativo": row["Ativo"], "localidade": row["Localidade"],
                "ameaca": row["Ameaça"], "vulnerabilidade": row["Vulnerabilidade"],
                "probabilidade": row["Probabilidade"], "impacto": row["Impacto"],
                "nivel_risco": row["Nível do Risco"], "usuario": usuario
            }).execute()
        supabase.table("historico_seguranca").insert({
            "tipo": "analise_risco", "dados": json.dumps(df.to_dict('records')), "usuario": usuario
        }).execute()
        return True
    except: return False

def carregar_riscos_supabase(supabase):
    if not supabase: return None
    try:
        r = supabase.table("riscos_atuais").select("*").execute()
        if r.data:
            df = pd.DataFrame(r.data).rename(columns={
                "ativo":"Ativo","localidade":"Localidade","ameaca":"Ameaça",
                "vulnerabilidade":"Vulnerabilidade","probabilidade":"Probabilidade",
                "impacto":"Impacto","nivel_risco":"Nível do Risco"
            })
            return df[["Ativo","Localidade","Ameaça","Vulnerabilidade","Probabilidade","Impacto","Nível do Risco"]]
        return None
    except: return None

def salvar_equipamentos_supabase(supabase, df, usuario):
    if not supabase: return False
    try:
        supabase.table("equipamentos").delete().neq("id", 0).execute()
        for _, row in df.iterrows():
            supabase.table("equipamentos").insert({
                "equipamento": row["Equipamento"], "tipo": row["Tipo"], "localidade": row["Localidade"],
                "fabricante": row["Fabricante"], "modelo": row["Modelo"], "status": row["Status"],
                "motivo": row.get("Motivo", ""), "usuario": usuario
            }).execute()
        supabase.table("historico_seguranca").insert({
            "tipo": "equipamentos", "dados": json.dumps(df.to_dict('records')), "usuario": usuario
        }).execute()
        return True
    except: return False

def carregar_equipamentos_supabase(supabase):
    if not supabase: return None
    try:
        r = supabase.table("equipamentos").select("*").execute()
        if r.data:
            df = pd.DataFrame(r.data).rename(columns={
                "equipamento":"Equipamento","tipo":"Tipo","localidade":"Localidade",
                "fabricante":"Fabricante","modelo":"Modelo","status":"Status","motivo":"Motivo"
            })
            return df[["Equipamento","Tipo","Localidade","Fabricante","Modelo","Status","Motivo"]]
        return None
    except: return None

def salvar_controles_supabase(supabase, df, usuario):
    if not supabase: return False
    try:
        supabase.table("controles_seguranca").delete().neq("id", 0).execute()
        for _, row in df.iterrows():
            supabase.table("controles_seguranca").insert({
                "controle": row["Controle"], "categoria": row["Categoria"],
                "descricao": row["Descrição"], "tipo_controle": row["Tipo de Controle"],
                "status": row["Status"], "data_implementacao": row.get("Data Implementação", ""),
                "responsavel": row.get("Responsável", ""), "efetividade": row.get("Efetividade", ""),
                "usuario": usuario
            }).execute()
        supabase.table("historico_seguranca").insert({
            "tipo": "controles", "dados": json.dumps(df.to_dict('records')), "usuario": usuario
        }).execute()
        return True
    except: return False

def carregar_controles_supabase(supabase):
    if not supabase: return None
    try:
        r = supabase.table("controles_seguranca").select("*").execute()
        if r.data:
            df = pd.DataFrame(r.data).rename(columns={
                "controle":"Controle","categoria":"Categoria","descricao":"Descrição",
                "tipo_controle":"Tipo de Controle","status":"Status",
                "data_implementacao":"Data Implementação","responsavel":"Responsável","efetividade":"Efetividade"
            })
            return df[["Controle","Categoria","Descrição","Tipo de Controle","Status","Data Implementação","Responsável","Efetividade"]]
        return None
    except: return None

def salvar_codigo_conduta_supabase(supabase, df, usuario):
    if not supabase: return False
    try:
        supabase.table("codigo_conduta").delete().neq("id", 0).execute()
        for _, row in df.iterrows():
            supabase.table("codigo_conduta").insert({
                "principio": row["Princípio"], "categoria": row["Categoria"],
                "descricao": row["Descrição"], "aplicavel_a": row["Aplicável a"],
                "consequencias": row["Consequências"], "status": row["Status"],
                "data_revisao": row.get("Data Revisão", ""), "versao": row.get("Versão", "1.0"),
                "usuario": usuario
            }).execute()
        supabase.table("historico_seguranca").insert({
            "tipo": "codigo_conduta", "dados": json.dumps(df.to_dict('records')), "usuario": usuario
        }).execute()
        return True
    except: return False

def carregar_codigo_conduta_supabase(supabase):
    if not supabase: return None
    try:
        r = supabase.table("codigo_conduta").select("*").execute()
        if r.data:
            df = pd.DataFrame(r.data).rename(columns={
                "principio":"Princípio","categoria":"Categoria","descricao":"Descrição",
                "aplicavel_a":"Aplicável a","consequencias":"Consequências","status":"Status",
                "data_revisao":"Data Revisão","versao":"Versão"
            })
            return df[["Princípio","Categoria","Descrição","Aplicável a","Consequências","Status","Data Revisão","Versão"]]
        return None
    except: return None

def salvar_classificacao_supabase(supabase, df, usuario):
    if not supabase: return False
    try:
        supabase.table("classificacao_informacao").delete().neq("id", 0).execute()
        for _, row in df.iterrows():
            supabase.table("classificacao_informacao").insert({
                "ativo_informacao": row["Ativo de Informação"], "proprietario": row["Proprietário"],
                "classificacao": row["Classificação"], "nivel_sigilo": row["Nível de Sigilo"],
                "justificativa": row["Justificativa"], "tempo_retencao": row["Tempo de Retenção"],
                "controles_necessarios": row["Controles Necessários"],
                "data_classificacao": row.get("Data Classificação", ""),
                "revisado_por": row.get("Revisado por", ""), "usuario": usuario
            }).execute()
        supabase.table("historico_seguranca").insert({
            "tipo": "classificacao_informacao", "dados": json.dumps(df.to_dict('records')), "usuario": usuario
        }).execute()
        return True
    except: return False

def carregar_classificacao_supabase(supabase):
    if not supabase: return None
    try:
        r = supabase.table("classificacao_informacao").select("*").execute()
        if r.data:
            df = pd.DataFrame(r.data).rename(columns={
                "ativo_informacao":"Ativo de Informação","proprietario":"Proprietário",
                "classificacao":"Classificação","nivel_sigilo":"Nível de Sigilo",
                "justificativa":"Justificativa","tempo_retencao":"Tempo de Retenção",
                "controles_necessarios":"Controles Necessários","data_classificacao":"Data Classificação",
                "revisado_por":"Revisado por"
            })
            return df[["Ativo de Informação","Proprietário","Classificação","Nível de Sigilo","Justificativa","Tempo de Retenção","Controles Necessários","Data Classificação","Revisado por"]]
        return None
    except: return None

def salvar_ameacas_supabase(supabase, df, usuario):
    if not supabase: return False
    try:
        supabase.table("inteligencia_ameacas").delete().neq("id", 0).execute()
        for _, row in df.iterrows():
            supabase.table("inteligencia_ameacas").insert({
                "ameaca": row["Ameaça"], "categoria": row["Categoria"],
                "nivel_criticidade": row["Nível Criticidade"], "descoberta_em": row["Descoberta em"],
                "descricao": row["Descrição"], "tecnicas_ataque": row["Técnicas de Ataque"],
                "medidas_mitigacao": row["Medidas de Mitigação"], "status": row["Status"],
                "usuario": usuario
            }).execute()
        supabase.table("historico_seguranca").insert({
            "tipo": "inteligencia_ameacas", "dados": json.dumps(df.to_dict('records')), "usuario": usuario
        }).execute()
        return True
    except: return False

def carregar_ameacas_supabase(supabase):
    if not supabase: return None
    try:
        r = supabase.table("inteligencia_ameacas").select("*").execute()
        if r.data:
            df = pd.DataFrame(r.data).rename(columns={
                "ameaca":"Ameaça","categoria":"Categoria","nivel_criticidade":"Nível Criticidade",
                "descoberta_em":"Descoberta em","descricao":"Descrição","tecnicas_ataque":"Técnicas de Ataque",
                "medidas_mitigacao":"Medidas de Mitigação","status":"Status"
            })
            return df[["Ameaça","Categoria","Nível Criticidade","Descoberta em","Descrição","Técnicas de Ataque","Medidas de Mitigação","Status"]]
        return None
    except: return None

def salvar_segregacao_supabase(supabase, dados, usuario):
    if not supabase: return False
    try:
        supabase.table("segregacao_funcoes").delete().neq("id", 0).execute()
        supabase.table("segregacao_funcoes").insert({
            "cargo": "_piramide_dados_", "nivel": "_json_", "responsabilidades": json.dumps(dados),
            "acessos_autorizados": "", "principio_need_to_know": "", "segregacao_aplicada": "",
            "aprovador": "", "data_revisao": "", "usuario": usuario
        }).execute()
        supabase.table("historico_seguranca").insert({
            "tipo": "segregacao_funcoes", "dados": json.dumps(dados), "usuario": usuario
        }).execute()
        return True
    except: return False

def carregar_segregacao_supabase(supabase):
    if not supabase: return None
    try:
        r = supabase.table("segregacao_funcoes").select("*").execute()
        if r.data:
            for item in r.data:
                if item.get("cargo") == "_piramide_dados_":
                    return json.loads(item["responsabilidades"])
        return None
    except: return None

def salvar_pdca_supabase(supabase, dados_pdca, usuario):
    if not supabase: return False
    try:
        supabase.table("pdca").delete().neq("id", 0).execute()
        fases = ["1. Contexto","2. Liderança","3. Planejamento","4. Suporte","5. Operação","6. Avaliação","7. Melhoria"]
        linhas = ["Objetivo Estratégico","Ação Técnica","Indicador KPI","Evidência Status"]
        for key, value in dados_pdca.items():
            fi, li = key
            supabase.table("pdca").insert({
                "fase": fases[fi], "linha": linhas[li], "conteudo": value, "usuario": usuario
            }).execute()
        supabase.table("historico_seguranca").insert({
            "tipo": "pdca", "dados": json.dumps({str(k): v for k, v in dados_pdca.items()}), "usuario": usuario
        }).execute()
        return True
    except: return False

def carregar_pdca_supabase(supabase):
    if not supabase: return {}
    try:
        r = supabase.table("pdca").select("*").execute()
        if r.data:
            fases = ["1. Contexto","2. Liderança","3. Planejamento","4. Suporte","5. Operação","6. Avaliação","7. Melhoria"]
            linhas = ["Objetivo Estratégico","Ação Técnica","Indicador KPI","Evidência Status"]
            dados = {}
            for item in r.data:
                if item["fase"] in fases and item["linha"] in linhas:
                    dados[(fases.index(item["fase"]), linhas.index(item["linha"]))] = item["conteudo"]
            return dados
        return {}
    except: return {}

def carregar_historico_supabase(supabase, tipo=None):
    if not supabase: return pd.DataFrame()
    try:
        q = supabase.table("historico_seguranca").select("id,tipo,usuario,data").order("id", desc=True).limit(50)
        if tipo and tipo != "Todos":
            q = q.eq("tipo", tipo)
        r = q.execute()
        return pd.DataFrame(r.data) if r.data else pd.DataFrame()
    except: return pd.DataFrame()

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

def obter_hora_brasil():
    return datetime.now(timezone.utc) + timedelta(hours=-3)

# ──────────────────────────────────────────────
# HELPERS
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

def mcard(num, lbl, cor):
    return f"<div class='mcard'><div class='mcard-num {cor}'>{num}</div><div class='mcard-lbl'>{lbl}</div></div>"

def sec(t):
    st.markdown(f"<div class='sec-title'>{t}</div>", unsafe_allow_html=True)

def get_classificacao_badge(nivel):
    badges = {
        "Pública": '<span class="classificacao-publica">🌍 Pública</span>',
        "Interna": '<span class="classificacao-interna">🏢 Interna</span>',
        "Restrita": '<span class="classificacao-restrita">🔒 Restrita</span>',
        "Confidencial": '<span class="classificacao-confidencial">🔐 Confidencial</span>'
    }
    return badges.get(nivel, f'<span class="classificacao-interna">{nivel}</span>')

# ──────────────────────────────────────────────
# LOGIN PAGE
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
    st.stop()

# ──────────────────────────────────────────────
# INICIALIZAR SUPABASE
# ──────────────────────────────────────────────
supabase = init_supabase()

# ──────────────────────────────────────────────
# SESSION STATE
# ──────────────────────────────────────────────
if 'matriz_ativa' not in st.session_state:
    st.session_state.matriz_ativa = None

if 'piramide_niveis' not in st.session_state:
    st.session_state.piramide_niveis = [
        {"emoji": "👑", "titulo": "Diretoria / C-Level", "responsabilidades": "Aprovação de estratégias, Orçamento, Governança", "acesso": "Visão executiva completa", "cor": "#7c3aed", "largura": 20},
        {"emoji": "🎯", "titulo": "Gerência de Segurança", "responsabilidades": "Políticas, Análise de riscos, Supervisão de controles", "acesso": "SIEM, Firewall, Relatórios", "cor": "#2563eb", "largura": 35},
        {"emoji": "🔧", "titulo": "Analista / Técnico", "responsabilidades": "Configuração de sistemas, Monitoramento, Resposta a incidentes", "acesso": "Ferramentas técnicas, Logs", "cor": "#0891b2", "largura": 52},
        {"emoji": "💼", "titulo": "Operador de Suporte", "responsabilidades": "Atendimento a usuários, Tickets, Primeiro nível", "acesso": "Sistema de chamados, Base de conhecimento", "cor": "#059669", "largura": 68},
        {"emoji": "👥", "titulo": "Colaboradores Gerais", "responsabilidades": "Uso dos sistemas, Cumprimento das políticas", "acesso": "Sistemas de uso geral, Intranet", "cor": "#64748b", "largura": 85},
    ]

# Carregar dados do Supabase
if supabase:
    dados_risco_db = carregar_riscos_supabase(supabase)
    dados_eq_db = carregar_equipamentos_supabase(supabase)
    dados_pdca_db = carregar_pdca_supabase(supabase)
    dados_controles_db = carregar_controles_supabase(supabase)
    dados_codigo_db = carregar_codigo_conduta_supabase(supabase)
    dados_classificacao_db = carregar_classificacao_supabase(supabase)
    dados_ameacas_db = carregar_ameacas_supabase(supabase)
    dados_segregacao_db = carregar_segregacao_supabase(supabase)
else:
    dados_risco_db = dados_eq_db = dados_controles_db = dados_codigo_db = dados_classificacao_db = dados_ameacas_db = None
    dados_pdca_db = {}
    dados_segregacao_db = None

if dados_segregacao_db is not None:
    st.session_state.piramide_niveis = dados_segregacao_db

# ── DADOS PADRÃO ──
edited_risco = dados_risco_db if (dados_risco_db is not None and not dados_risco_db.empty) else pd.DataFrame({
    "Ativo": ["Cabos sala", "Pen drive", "Servidor internet", "Switch", "Firewall", "Router"],
    "Localidade": ["Sala A", "TI Sala 210", "DC Rack 05", "Sala rede", "DC Rack 02", "DC Rack 01"],
    "Ameaça": ["Rompimento", "Vírus", "Invasão", "Desligamento", "DDoS", "Configuração"],
    "Vulnerabilidade": ["Cabos soltos", "Antivírus antigo", "Rede interna", "Sem trava", "Firmware", "Senha fraca"],
    "Probabilidade": ["Baixa", "Alta", "Média", "Média", "Baixa", "Média"],
    "Impacto": ["Alto", "Alto", "Alto", "Médio", "Alto", "Alto"],
    "Nível do Risco": ["🔴 Alto", "🔴 Alto", "🔴 Alto", "🟡 Médio", "🔴 Alto", "🔴 Alto"],
})

edited_eq = dados_eq_db if (dados_eq_db is not None and not dados_eq_db.empty) else pd.DataFrame({
    "Equipamento": ["Firewall Fortinet", "Switch Core Huawei", "Router Cisco", "Servidor Dell", "Storage EMC", "Access Point", "Patch Panel"],
    "Tipo": ["Segurança", "Rede", "Rede", "Servidor", "Storage", "Rede", "Infraestrutura"],
    "Localidade": ["DC Rack 02", "DC Rack 01", "DC Rack 01", "DC Rack 03", "DC Rack 04", "Sala 210", "Sala servidores"],
    "Fabricante": ["Fortinet", "Huawei", "Cisco", "Dell", "EMC", "Ubiquiti", "Intelbras"],
    "Modelo": ["FG-100F", "S12700", "ISR4321", "R750", "XT380", "U6-LR", "CAT6"],
    "Status": ["Ativo", "Ativo", "Ativo", "Ativo", "Ativo", "Ativo", "Ativo"],
    "Motivo": ["", "", "", "", "", "", ""],
})

edited_controles = dados_controles_db if (dados_controles_db is not None and not dados_controles_db.empty) else pd.DataFrame({
    "Controle": ["Controle de Acesso", "Antivírus Centralizado", "Backup Automatizado", "Firewall de Rede", "Monitoramento 24/7", "Política de Senhas", "DLP", "SIEM"],
    "Categoria": ["Acesso", "Malware", "Backup", "Rede", "Monitoramento", "Governança", "Data Loss", "SIEM"],
    "Descrição": ["Controle de acesso RBAC", "Antivírus com atualização automática", "Backup diário 30 dias", "Firewall com inspeção de pacotes", "Monitoramento contínuo", "Política de senhas fortes", "Prevenção vazamento de dados", "Correlação de eventos"],
    "Tipo de Controle": ["Preventivo", "Detectivo", "Corretivo", "Preventivo", "Detectivo", "Preventivo", "Preventivo", "Detectivo"],
    "Status": ["Implantado", "Implantado", "Implantado", "Implantado", "Parcial", "Pendente", "Planejado", "Planejado"],
    "Data Implementação": ["2024-01-15", "2024-01-10", "2024-01-20", "2024-02-01", "2024-03-10", "", "", ""],
    "Responsável": ["TI", "TI", "DBA", "Rede", "SecOps", "Governança", "SecOps", "SecOps"],
    "Efetividade": ["95%", "90%", "100%", "85%", "60%", "", "", ""],
})

edited_codigo = dados_codigo_db if (dados_codigo_db is not None and not dados_codigo_db.empty) else pd.DataFrame({
    "Princípio": ["Integridade", "Confidencialidade", "Conformidade", "Respeito", "Responsabilidade", "Transparência", "Lealdade", "Inovação Ética"],
    "Categoria": ["Ética", "Segurança", "Legal", "Comportamental", "Gestão", "Governança", "Compromisso", "Tecnologia"],
    "Descrição": [
        "Agir com honestidade e retidão em todas as atividades profissionais.",
        "Proteger informações confidenciais da organização, não divulgando dados sensíveis.",
        "Cumprir todas as leis, regulamentos e normas aplicáveis, incluindo LGPD e ISO 27001.",
        "Tratar todos os colegas, clientes e parceiros com respeito e dignidade.",
        "Assumir responsabilidade pelas próprias ações e decisões.",
        "Manter comunicação clara, aberta e honesta.",
        "Demonstrar comprometimento com os objetivos e valores da organização.",
        "Utilizar tecnologia de forma ética e responsável.",
    ],
    "Aplicável a": ["Todos", "Todos", "Todos", "Todos", "Gestores", "Lideranças", "Todos", "TI e Usuários"],
    "Consequências": ["Advertência e possível demissão", "Medidas disciplinares", "Sanções legais e demissão", "Advertência e mediação", "Revisão de função", "Avaliação de desempenho", "Aviso e desligamento", "Advertência e restrição"],
    "Status": ["Ativo", "Ativo", "Ativo", "Ativo", "Ativo", "Ativo", "Ativo", "Ativo"],
    "Data Revisão": ["2024-01-01", "2024-01-01", "2024-01-01", "2024-01-01", "2024-01-01", "2024-01-01", "2024-01-01", "2024-01-01"],
    "Versão": ["2.0", "2.0", "2.0", "2.0", "2.0", "2.0", "2.0", "2.0"],
})

edited_classificacao = dados_classificacao_db if (dados_classificacao_db is not None and not dados_classificacao_db.empty) else pd.DataFrame({
    "Ativo de Informação": ["Relatório Financeiro", "Dados de Clientes", "Políticas Internas", "Manuais Técnicos", "Estratégia de Negócio", "Comunicados", "Código Fonte", "Contratos"],
    "Proprietário": ["CFO", "DPO", "RH", "TI", "CEO", "Marketing", "CTO", "Jurídico"],
    "Classificação": ["Restrita", "Confidencial", "Interna", "Interna", "Confidencial", "Pública", "Restrita", "Confidencial"],
    "Nível de Sigilo": ["Alto", "Máximo", "Médio", "Médio", "Máximo", "Baixo", "Alto", "Alto"],
    "Justificativa": ["Informações financeiras sensíveis", "Dados pessoais LGPD", "Diretrizes internas", "Conhecimento técnico", "Planejamento estratégico", "Comunicação externa", "Propriedade intelectual", "Cláusulas contratuais"],
    "Tempo de Retenção": ["5 anos", "Indeterminado", "2 anos", "3 anos", "3 anos", "1 ano", "Indeterminado", "10 anos"],
    "Controles Necessários": ["Criptografia, Auditoria", "LGPD, Acesso restrito", "Intranet, Autenticação", "Controle de versão", "Sala cofre, NDA", "Aprovação marketing", "Repositório privado", "Assinatura digital"],
    "Data Classificação": ["2024-01-15", "2024-01-10", "2024-01-05", "2024-01-20", "2024-01-25", "2024-01-30", "2024-02-01", "2024-02-05"],
    "Revisado por": ["Comitê", "DPO", "RH", "TI", "Diretoria", "Marketing", "TI", "Jurídico"],
})

edited_ameacas = dados_ameacas_db if (dados_ameacas_db is not None and not dados_ameacas_db.empty) else pd.DataFrame({
    "Ameaça": ["Ransomware", "Phishing", "DDoS", "Insider Threat", "Zero-Day", "Man-in-the-Middle"],
    "Categoria": ["Malware", "Engenharia Social", "Disponibilidade", "Pessoal", "Vulnerabilidade", "Rede"],
    "Nível Criticidade": ["Crítico", "Alto", "Alto", "Médio", "Crítico", "Médio"],
    "Descoberta em": ["2024-01-15", "2024-01-10", "2024-01-05", "2024-01-20", "2024-02-01", "2024-01-25"],
    "Descrição": ["Criptografia de dados e pedido de resgate", "Tentativas de obter credenciais por e-mail fraudulento", "Sobrecarga de tráfego para derrubar serviços", "Ameaças originadas por usuários internos", "Exploração de vulnerabilidade ainda desconhecida", "Interceptação e alteração de comunicações"],
    "Técnicas de Ataque": ["Phishing, Exploits", "E-mails fraudulentos", "Botnets, Amplificação", "Abuso de privilégios", "Exploração 0-day", "ARP Spoofing"],
    "Medidas de Mitigação": ["Backup offline, EDR", "Treinamento, MFA", "WAF, Rate limiting", "Monitoramento UBA", "Patch management", "TLS, Certificados"],
    "Status": ["Monitorando", "Mitigado", "Monitorando", "Controlado", "Investigando", "Mitigado"],
})

# ──────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div class='sb-logo'>🛡️ SecureOps</div>", unsafe_allow_html=True)
    st.markdown("<div class='sb-sub'>Gestão de Segurança</div>", unsafe_allow_html=True)
    st.markdown("<hr class='sb-div'>", unsafe_allow_html=True)
    st.markdown(f"**{st.session_state.usuario}**")
    st.markdown("<div style='font-size:11px;color:#64748b;'>Administrador</div>", unsafe_allow_html=True)
    st.markdown("<hr class='sb-div'>", unsafe_allow_html=True)
    st.markdown("<div class='sb-lbl'>Resumo Rápido</div>", unsafe_allow_html=True)
    sidebar_ph = st.empty()
    st.markdown("<hr class='sb-div'>", unsafe_allow_html=True)
    hora_br = obter_hora_brasil()
    st.markdown(f"📅 {hora_br.strftime('%d/%m/%Y')}")
    st.markdown(f"🕐 {hora_br.strftime('%H:%M:%S')}")
    st.markdown("<hr class='sb-div'>", unsafe_allow_html=True)
    if st.button("🚪 Sair", use_container_width=True):
        fazer_logout()

# ──────────────────────────────────────────────
# CABEÇALHO
# ──────────────────────────────────────────────
hora_br = obter_hora_brasil()
st.markdown(f"""
<div class='page-title'>🛡️ SecureOps — Gestão de Segurança</div>
<div class='page-sub'>PDCA · Análise de Risco · Controles · Classificação · {hora_br.strftime('%d/%m/%Y %H:%M')}</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# ABAS
# ──────────────────────────────────────────────
tab_dados, tab_graficos, tab_controles, tab_classificacao, tab_codigo, tab_ameacas, tab_segregacao, tab_pdca, tab_historico = st.tabs([
    "📋 Dados", "📊 Gráficos", "🔒 Controles", "🔐 Classificação", "📜 Código Conduta", "🕵️ Ameaças", "👥 Segregação", "🔄 PDCA", "📜 Histórico"
])

# ═══════════════════════════════════════════════════════════════
# TAB DADOS
# ═══════════════════════════════════════════════════════════════
with tab_dados:
    sec("Análise de Risco")
    edited_risco = st.data_editor(
        edited_risco, use_container_width=True, num_rows="dynamic",
        column_config={
            "Probabilidade": st.column_config.SelectboxColumn(options=["Baixa","Média","Alta"]),
            "Impacto": st.column_config.SelectboxColumn(options=["Baixo","Médio","Alto"]),
            "Nível do Risco": st.column_config.TextColumn(disabled=True),
        }, hide_index=True,
    )
    edited_risco["Nível do Risco"] = edited_risco.apply(lambda r: nivel_risco(r["Probabilidade"], r["Impacto"]), axis=1)

    sec("Inventário de Equipamentos")
    edited_eq = st.data_editor(
        edited_eq, use_container_width=True, num_rows="dynamic",
        column_config={
            "Tipo": st.column_config.SelectboxColumn(options=["Segurança","Rede","Servidor","Storage","Infraestrutura"]),
            "Status": st.column_config.SelectboxColumn(options=["Ativo","Inativo","Em Manutenção","Reserva"]),
        }, hide_index=True,
    )

    st.markdown("---")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        if st.button("☁️ Salvar Dados na Nuvem", use_container_width=True):
            if supabase:
                ok1 = salvar_riscos_supabase(supabase, edited_risco, st.session_state.usuario)
                ok2 = salvar_equipamentos_supabase(supabase, edited_eq, st.session_state.usuario)
                st.success("✅ Dados salvos!") if (ok1 and ok2) else st.error("❌ Erro ao salvar")
            else:
                st.error("❌ Supabase não conectado")
    with col_s2:
        if st.button("📥 Exportar Excel", use_container_width=True):
            with pd.ExcelWriter(f"secureops_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx") as writer:
                edited_risco.to_excel(writer, sheet_name="Riscos", index=False)
                edited_eq.to_excel(writer, sheet_name="Equipamentos", index=False)
                edited_controles.to_excel(writer, sheet_name="Controles", index=False)
                edited_codigo.to_excel(writer, sheet_name="CodigoConduta", index=False)
                edited_classificacao.to_excel(writer, sheet_name="Classificacao", index=False)
                edited_ameacas.to_excel(writer, sheet_name="Ameacas", index=False)
            st.success("✅ Excel exportado!")

# ═══════════════════════════════════════════════════════════════
# TAB GRÁFICOS
# ═══════════════════════════════════════════════════════════════
with tab_graficos:
    st.markdown("### 📊 Dashboard de Segurança")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(mcard(len(edited_risco), "Total Riscos", "c-blue"), unsafe_allow_html=True)
    with col2:
        alto = len(edited_risco[edited_risco["Nível do Risco"] == "🔴 Alto"])
        st.markdown(mcard(alto, "Riscos Altos", "c-red"), unsafe_allow_html=True)
    with col3:
        impl = len(edited_controles[edited_controles["Status"] == "Implantado"])
        st.markdown(mcard(impl, "Controles OK", "c-green"), unsafe_allow_html=True)
    with col4:
        conf = len(edited_classificacao[edited_classificacao["Classificação"] == "Confidencial"])
        st.markdown(mcard(conf, "Info Confidencial", "c-purple"), unsafe_allow_html=True)

    st.markdown("---")
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown("##### 🔐 Classificação da Informação")
        counts = edited_classificacao["Classificação"].value_counts().to_dict()
        total = sum(counts.values()) if counts else 1
        html = "".join([f"<div style='display:flex;justify-content:space-between;margin-bottom:10px;'><span>{get_classificacao_badge(k)}</span><span><b>{v}</b> ({v/total*100:.0f}%)</span></div>" for k, v in counts.items()])
        st.markdown(f"<div class='chart-card'>{html}</div>", unsafe_allow_html=True)
    
    with col_c2:
        st.markdown("##### 🎯 Nível de Sigilo")
        sigilo = edited_classificacao["Nível de Sigilo"].value_counts().to_dict()
        cores_s = {"Máximo":"#dc2626","Alto":"#ea580c","Médio":"#d97706","Baixo":"#16a34a"}
        html2 = "".join([f"<div style='display:flex;justify-content:space-between;margin-bottom:10px;'><span style='color:{cores_s.get(k,'#64748b')};font-weight:600;'>● {k}</span><span><b>{v}</b></span></div>" for k, v in sigilo.items()])
        st.markdown(f"<div class='chart-card'>{html2}</div>", unsafe_allow_html=True)

    st.markdown("---")
    
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.markdown("##### ⚠️ Distribuição de Riscos")
        risco_counts = edited_risco["Nível do Risco"].value_counts().to_dict()
        cores_risco = {"🔴 Alto":"#dc2626","🟡 Médio":"#d97706","🟢 Baixo":"#16a34a"}
        html3 = "".join([f"<div style='display:flex;justify-content:space-between;margin-bottom:10px;'><span style='color:{cores_risco.get(k,"#64748b")};font-weight:600;'>{k}</span><span><b>{v}</b></span></div>" for k, v in risco_counts.items()])
        st.markdown(f"<div class='chart-card'>{html3}</div>", unsafe_allow_html=True)
    
    with col_r2:
        st.markdown("##### 🔒 Status dos Controles")
        ctrl_counts = edited_controles["Status"].value_counts().to_dict()
        cores_ctrl = {"Implantado":"#16a34a","Parcial":"#d97706","Pendente":"#dc2626","Planejado":"#2563eb"}
        html4 = "".join([f"<div style='display:flex;justify-content:space-between;margin-bottom:10px;'><span style='color:{cores_ctrl.get(k,"#64748b")};font-weight:600;'>● {k}</span><span><b>{v}</b></span></div>" for k, v in ctrl_counts.items()])
        st.markdown(f"<div class='chart-card'>{html4}</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# TAB CONTROLES
# ═══════════════════════════════════════════════════════════════
with tab_controles:
    sec("🔒 Controles de Segurança")
    st.markdown("""<div class='info-box' style='background:#eef2ff;border-color:#2563eb;color:#1e40af;'>
    📌 Controles de segurança são medidas para evitar, combater ou minimizar perdas de ativos de informação.
    </div>""", unsafe_allow_html=True)

    edited_controles = st.data_editor(
        edited_controles, use_container_width=True, num_rows="dynamic",
        column_config={
            "Categoria": st.column_config.SelectboxColumn(options=["Acesso","Malware","Backup","Rede","Monitoramento","Governança","Data Loss","SIEM","Física","Criptografia"]),
            "Tipo de Controle": st.column_config.SelectboxColumn(options=["Preventivo","Detectivo","Corretivo","Compensatório","Deterrente"]),
            "Status": st.column_config.SelectboxColumn(options=["Implantado","Parcial","Pendente","Planejado","Cancelado"]),
        }, hide_index=True,
    )

    if st.button("💾 Salvar Controles", use_container_width=True):
        if supabase:
            if salvar_controles_supabase(supabase, edited_controles, st.session_state.usuario):
                st.success("✅ Controles salvos!")
            else:
                st.error("❌ Erro ao salvar")
        else:
            st.error("❌ Supabase não conectado")

# ═══════════════════════════════════════════════════════════════
# TAB CLASSIFICAÇÃO
# ═══════════════════════════════════════════════════════════════
with tab_classificacao:
    sec("🔐 Classificação da Informação")

    NIVEIS_CLASSIFICACAO = [
        {"nome": "Pública", "emoji": "🌍", "bg": "#dcfce7", "cor": "#16a34a", "desc": "Acesso irrestrito ao público", "exemplos": ["Site institucional", "Comunicados"]},
        {"nome": "Interna", "emoji": "🏢", "bg": "#dbeafe", "cor": "#2563eb", "desc": "Uso exclusivo interno", "exemplos": ["Políticas internas", "Manuais técnicos"]},
        {"nome": "Restrita", "emoji": "🔒", "bg": "#fed7aa", "cor": "#ea580c", "desc": "Acesso limitado a grupos específicos", "exemplos": ["Relatórios financeiros", "Código-fonte"]},
        {"nome": "Confidencial", "emoji": "🔐", "bg": "#fee2e2", "cor": "#dc2626", "desc": "Alto sigilo", "exemplos": ["Dados clientes LGPD", "Estratégia"]},
    ]

    cols_matriz = st.columns(4, gap="small")
    for i, nivel in enumerate(NIVEIS_CLASSIFICACAO):
        with cols_matriz[i]:
            is_ativo = (st.session_state.matriz_ativa == nivel["nome"])
            st.markdown(f"""
            <div style='background:{nivel["bg"]}; border:2px solid {nivel["cor"]}40; border-radius:12px; padding:16px; text-align:center; {"border-width:3px; border-color:"+nivel["cor"] if is_ativo else ""}'>
                <div style='font-size:32px;'>{nivel["emoji"]}</div>
                <div style='font-size:14px; font-weight:700; color:{nivel["cor"]};'>{nivel["nome"]}</div>
                <div style='font-size:10px; color:#64748b; margin:6px 0;'>{nivel["desc"]}</div>
                <div style='font-size:10px; color:{nivel["cor"]};'>{', '.join(nivel["exemplos"])}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"{'✅ ' if is_ativo else ''}Filtrar {nivel['nome']}", key=f"btn_matriz_{nivel['nome']}", use_container_width=True):
                if is_ativo:
                    st.session_state.matriz_ativa = None
                else:
                    st.session_state.matriz_ativa = nivel["nome"]
                st.rerun()

    if st.session_state.matriz_ativa:
        df_filtrado = edited_classificacao[edited_classificacao["Classificação"] == st.session_state.matriz_ativa]
        st.info(f"🔍 Filtrando: **{st.session_state.matriz_ativa}** — {len(df_filtrado)} ativo(s) encontrado(s)")
        df_para_editar = df_filtrado
    else:
        df_para_editar = edited_classificacao

    st.markdown("---")
    st.markdown("#### 📋 Ativos de Informação")

    df_editado = st.data_editor(
        df_para_editar.copy(),
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            "Classificação": st.column_config.SelectboxColumn(options=["Pública","Interna","Restrita","Confidencial"]),
            "Nível de Sigilo": st.column_config.SelectboxColumn(options=["Baixo","Médio","Alto","Máximo"]),
        },
        hide_index=True,
        key="classificacao_editor"
    )

    if st.button("💾 Salvar Classificação", use_container_width=True):
        if supabase:
            if salvar_classificacao_supabase(supabase, df_editado, st.session_state.usuario):
                st.success("✅ Classificação salva!")
                st.rerun()
            else:
                st.error("❌ Erro ao salvar")
        else:
            st.error("❌ Supabase não conectado")

# ═══════════════════════════════════════════════════════════════
# TAB CÓDIGO DE CONDUTA
# ═══════════════════════════════════════════════════════════════
with tab_codigo:
    sec("📜 Código de Conduta")

    st.markdown("""<div class='info-box' style='background:#e0e7ff;border-color:#4338ca;color:#3730a3;'>
    📌 O Código de Conduta define os princípios éticos e comportamentais que todos os colaboradores devem seguir.
    </div>""", unsafe_allow_html=True)

    col_cc1, col_cc2, col_cc3, col_cc4 = st.columns(4)
    with col_cc1:
        st.markdown(mcard(len(edited_codigo), "Total Princípios", "c-blue"), unsafe_allow_html=True)
    with col_cc2:
        ativos_cod = len(edited_codigo[edited_codigo["Status"] == "Ativo"]) if not edited_codigo.empty else 0
        st.markdown(mcard(ativos_cod, "Ativos", "c-green"), unsafe_allow_html=True)
    with col_cc3:
        st.markdown(mcard(edited_codigo["Categoria"].nunique() if not edited_codigo.empty else 0, "Categorias", "c-purple"), unsafe_allow_html=True)
    with col_cc4:
        todos_aplica = len(edited_codigo[edited_codigo["Aplicável a"] == "Todos"]) if not edited_codigo.empty else 0
        st.markdown(mcard(todos_aplica, "Aplicável a Todos", "c-yellow"), unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### ✏️ Editar Código de Conduta")

    edited_codigo = st.data_editor(
        edited_codigo,
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            "Categoria": st.column_config.SelectboxColumn(options=["Ética","Segurança","Legal","Comportamental","Gestão","Governança","Tecnologia","Compromisso"]),
            "Status": st.column_config.SelectboxColumn(options=["Ativo","Revisão","Descontinuado"]),
            "Aplicável a": st.column_config.SelectboxColumn(options=["Todos","Gestores","Lideranças","TI e Usuários","Colaboradores","Diretoria"]),
        },
        hide_index=True,
    )

    st.markdown("---")
    with st.expander("📋 Termo de Compromisso - Clique para assinar"):
        st.markdown("""
        **DECLARAÇÃO DE COMPROMISSO COM O CÓDIGO DE CONDUTA — SecureOps**
        
        Eu, _________________________________, declaro que li, compreendi e concordo em cumprir integralmente 
        o Código de Conduta da organização SecureOps.
        """)
        nome_colab = st.text_input("Nome completo", placeholder="Digite seu nome completo")
        if st.button("📝 Assinar Termo"):
            if nome_colab:
                st.success(f"✅ Termo assinado por {nome_colab} em {hora_br.strftime('%d/%m/%Y %H:%M')}")
            else:
                st.warning("Preencha seu nome para assinar")

    if st.button("💾 Salvar Código de Conduta", use_container_width=True):
        if supabase:
            if salvar_codigo_conduta_supabase(supabase, edited_codigo, st.session_state.usuario):
                st.success("✅ Código salvo!")
            else:
                st.error("❌ Erro ao salvar")
        else:
            st.error("❌ Supabase não conectado")

# ═══════════════════════════════════════════════════════════════
# TAB AMEAÇAS
# ═══════════════════════════════════════════════════════════════
with tab_ameacas:
    sec("🕵️ Inteligência de Ameaças")

    st.markdown("""<div class='info-box' style='background:#fce7f3;border-color:#db2777;color:#9d174d;'>
    📌 Inteligência de ameaças: investigação proativa de vulnerabilidades e técnicas de ataque.
    </div>""", unsafe_allow_html=True)

    col_a1, col_a2, col_a3, col_a4 = st.columns(4)
    with col_a1:
        st.markdown(mcard(len(edited_ameacas), "Total Ameaças", "c-blue"), unsafe_allow_html=True)
    with col_a2:
        criticas = len(edited_ameacas[edited_ameacas["Nível Criticidade"] == "Crítico"]) if not edited_ameacas.empty else 0
        st.markdown(mcard(criticas, "Críticas", "c-red"), unsafe_allow_html=True)
    with col_a3:
        monitorando = len(edited_ameacas[edited_ameacas["Status"] == "Monitorando"]) if not edited_ameacas.empty else 0
        st.markdown(mcard(monitorando, "Monitorando", "c-yellow"), unsafe_allow_html=True)
    with col_a4:
        mitigadas = len(edited_ameacas[edited_ameacas["Status"] == "Mitigado"]) if not edited_ameacas.empty else 0
        st.markdown(mcard(mitigadas, "Mitigadas", "c-green"), unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 🔄 Threat Intelligence Lifecycle")
    
    etapas_ti = [
        ("1", "Definir Objetivos", "#2563eb"),
        ("2", "Coletar Dados", "#7c3aed"),
        ("3", "Processar", "#db2777"),
        ("4", "Analisar", "#d97706"),
        ("5", "Reportar", "#059669"),
    ]
    cols_ti = st.columns(5)
    for i, (num, titulo, cor) in enumerate(etapas_ti):
        with cols_ti[i]:
            st.markdown(f"""
            <div class='threat-stage' style='background:{cor};'>
                <div style='font-size:24px;font-weight:700;'>{num}</div>
                <div style='font-size:11px;font-weight:600;'>{titulo}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### ✏️ Gerenciar Ameaças")

    edited_ameacas = st.data_editor(
        edited_ameacas, use_container_width=True, num_rows="dynamic",
        column_config={
            "Categoria": st.column_config.SelectboxColumn(options=["Malware","Engenharia Social","Disponibilidade","Pessoal","Vulnerabilidade","Rede"]),
            "Nível Criticidade": st.column_config.SelectboxColumn(options=["Crítico","Alto","Médio","Baixo"]),
            "Status": st.column_config.SelectboxColumn(options=["Monitorando","Mitigado","Investigando","Controlado","Crítico"]),
        }, hide_index=True,
    )

    if st.button("💾 Salvar Ameaças", use_container_width=True):
        if supabase:
            if salvar_ameacas_supabase(supabase, edited_ameacas, st.session_state.usuario):
                st.success("✅ Ameaças salvas!")
            else:
                st.error("❌ Erro ao salvar")
        else:
            st.error("❌ Supabase não conectado")

# ═══════════════════════════════════════════════════════════════
# TAB SEGREGAÇÃO
# ═══════════════════════════════════════════════════════════════
with tab_segregacao:
    sec("👥 Segregação de Funções")

    st.markdown("""<div class='info-box' style='background:#e6f7e6;border-color:#059669;color:#065f46;'>
    📌 A segregação de funções evita conflitos de interesse e reduz o risco de ações não autorizadas.
    </div>""", unsafe_allow_html=True)

    st.markdown("#### 🏛️ Pirâmide Hierárquica")
    
    niveis = st.session_state.piramide_niveis
    piramide_html = "<div style='display:flex;flex-direction:column;align-items:center;gap:8px;padding:20px 0;'>"
    for nivel in niveis:
        largura = nivel.get("largura", 50)
        cor = nivel.get("cor", "#2563eb")
        piramide_html += f"""
        <div style='width:{largura}%; background:{cor}; border-radius:10px; padding:12px 16px; text-align:center; color:white;'>
            <div style='font-size:18px;'>{nivel.get('emoji', '🔹')}</div>
            <div style='font-size:13px; font-weight:700;'>{nivel.get('titulo', '')}</div>
            <div style='font-size:10px; opacity:0.85;'>{nivel.get('responsabilidades', '')[:60]}...</div>
        </div>
        """
    piramide_html += "</div>"
    st.markdown(piramide_html, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### ✏️ Editar Níveis")
    
    with st.expander("Gerenciar níveis da pirâmide"):
        for i, nivel in enumerate(niveis):
            st.markdown(f"**Nível {i+1}**")
            col_e1, col_e2 = st.columns(2)
            with col_e1:
                nivel["titulo"] = st.text_input("Título", value=nivel.get("titulo", ""), key=f"tit_{i}")
                nivel["emoji"] = st.text_input("Emoji", value=nivel.get("emoji", "🔹"), key=f"emo_{i}")
                nivel["cor"] = st.color_picker("Cor", value=nivel.get("cor", "#2563eb"), key=f"cor_{i}")
            with col_e2:
                nivel["responsabilidades"] = st.text_area("Responsabilidades", value=nivel.get("responsabilidades", ""), key=f"resp_{i}", height=80)
                nivel["largura"] = st.slider("Largura (%)", 15, 100, nivel.get("largura", 50), key=f"larg_{i}")
            if st.button(f"🗑️ Remover nível {i+1}", key=f"rem_{i}"):
                st.session_state.piramide_niveis.pop(i)
                st.rerun()
            st.markdown("---")
        
        if st.button("➕ Adicionar novo nível"):
            st.session_state.piramide_niveis.append({
                "emoji": "🔹", "titulo": "Novo Nível", "responsabilidades": "", "cor": "#0891b2", "largura": 50
            })
            st.rerun()

    if st.button("💾 Salvar Pirâmide", use_container_width=True):
        if supabase:
            if salvar_segregacao_supabase(supabase, st.session_state.piramide_niveis, st.session_state.usuario):
                st.success("✅ Pirâmide salva!")
            else:
                st.error("❌ Erro ao salvar")
        else:
            st.error("❌ Supabase não conectado")

# ═══════════════════════════════════════════════════════════════
# TAB PDCA
# ═══════════════════════════════════════════════════════════════
with tab_pdca:
    st.markdown("### 🔄 PDCA de Gestão de Segurança")

    fases = [
        {"nome": "1. Contexto", "cor": "#2563eb"}, {"nome": "2. Liderança", "cor": "#2563eb"},
        {"nome": "3. Planejamento", "cor": "#2563eb"}, {"nome": "4. Suporte", "cor": "#d97706"},
        {"nome": "5. Operação", "cor": "#d97706"}, {"nome": "6. Avaliação", "cor": "#16a34a"},
        {"nome": "7. Melhoria", "cor": "#7c3aed"},
    ]
    linhas_pdca = ["🎯 Objetivo Estratégico", "⚙️ Ação Técnica", "📊 Indicador KPI", "🚩 Evidência Status"]
    
    pdca_data = dados_pdca_db if dados_pdca_db else {}
    
    fase_cols = st.columns(7, gap="small")
    for i, (col, fase) in enumerate(zip(fase_cols, fases)):
        with col:
            st.markdown(f"""
            <div style='background:{fase["cor"]}15; border:2px solid {fase["cor"]}40; border-radius:10px; padding:12px; text-align:center; margin-bottom:10px;'>
                <div style='font-size:11px; font-weight:800; color:{fase["cor"]};'>{fase["nome"]}</div>
            </div>
            """, unsafe_allow_html=True)
            for j, linha in enumerate(linhas_pdca):
                st.markdown(f"<div style='font-size:10px; font-weight:600; color:#64748b; margin-bottom:2px;'>{linha}</div>", unsafe_allow_html=True)
                key_val = pdca_data.get((i, j), "")
                pdca_data[(i, j)] = st.text_area("", value=key_val, placeholder="Digite...", label_visibility="collapsed", height=80, key=f"pdca_{i}_{j}")

    st.markdown("---")
    if st.button("💾 Salvar PDCA", use_container_width=True):
        if supabase:
            if salvar_pdca_supabase(supabase, pdca_data, st.session_state.usuario):
                st.success("✅ PDCA salvo!")
            else:
                st.error("❌ Erro ao salvar")
        else:
            st.error("❌ Supabase não conectado")

# ═══════════════════════════════════════════════════════════════
# TAB HISTÓRICO
# ═══════════════════════════════════════════════════════════════
with tab_historico:
    st.markdown("### 📜 Histórico de Alterações")
    tipo_filtro = st.selectbox("Filtrar:", ["Todos", "analise_risco", "equipamentos", "controles", "codigo_conduta", "classificacao_informacao", "inteligencia_ameacas", "segregacao_funcoes", "pdca"])
    if supabase:
        df_hist = carregar_historico_supabase(supabase, None if tipo_filtro == "Todos" else tipo_filtro)
        if not df_hist.empty:
            st.dataframe(df_hist, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum registro no histórico.")
    else:
        st.warning("Conecte ao Supabase para ver o histórico.")

# ──────────────────────────────────────────────
# SIDEBAR RESUMO
# ──────────────────────────────────────────────
with sidebar_ph:
    alto_s = len(edited_risco[edited_risco["Nível do Risco"] == "🔴 Alto"])
    medio_s = len(edited_risco[edited_risco["Nível do Risco"] == "🟡 Médio"])
    baixo_s = len(edited_risco[edited_risco["Nível do Risco"] == "🟢 Baixo"])
    ctrl_impl = len(edited_controles[edited_controles["Status"] == "Implantado"])
    ameacas_crit = len(edited_ameacas[edited_ameacas["Nível Criticidade"] == "Crítico"]) if not edited_ameacas.empty else 0

    st.markdown(f"""
    <div style='background:#fee2e2; color:#dc2626; display:flex; justify-content:space-between; padding:10px 14px; border-radius:10px; margin-bottom:8px;'>
        <span>🔴 Riscos Altos</span><span style='font-size:20px; font-weight:700;'>{alto_s}</span>
    </div>
    <div style='background:#fef3c7; color:#d97706; display:flex; justify-content:space-between; padding:10px 14px; border-radius:10px; margin-bottom:8px;'>
        <span>🟡 Riscos Médios</span><span style='font-size:20px; font-weight:700;'>{medio_s}</span>
    </div>
    <div style='background:#dcfce7; color:#16a34a; display:flex; justify-content:space-between; padding:10px 14px; border-radius:10px; margin-bottom:8px;'>
        <span>🟢 Riscos Baixos</span><span style='font-size:20px; font-weight:700;'>{baixo_s}</span>
    </div>
    <div style='background:#dbeafe; color:#2563eb; display:flex; justify-content:space-between; padding:10px 14px; border-radius:10px; margin-bottom:8px;'>
        <span>✅ Controles OK</span><span style='font-size:20px; font-weight:700;'>{ctrl_impl}</span>
    </div>
    <div style='background:#fee2e2; color:#dc2626; display:flex; justify-content:space-between; padding:10px 14px; border-radius:10px; margin-bottom:8px;'>
        <span>🚨 Ameaças Críticas</span><span style='font-size:20px; font-weight:700;'>{ameacas_crit}</span>
    </div>
    """, unsafe_allow_html=True)
