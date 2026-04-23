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
.block-container { padding: 1rem 1.5rem 1.5rem !important; }

/* Sidebar */
.sb-logo { font-size: 20px; font-weight: 700; color: #0f172a; }
.sb-sub { font-size: 11px; color: #64748b; }
.sb-div { border-top: 1px solid #e2e8f0; margin: 0.6rem 0; }
.sb-lbl { font-size: 10px; font-weight: 600; text-transform: uppercase; color: #64748b; letter-spacing: 0.5px; }

/* Menu lateral - Todas as abas */
.sb-menu-item { display: flex; align-items: center; gap: 10px; padding: 8px 12px; border-radius: 8px; margin-bottom: 4px; cursor: pointer; transition: all 0.2s; color: #475569; font-size: 13px; }
.sb-menu-item:hover { background: #e2e8f0; }
.sb-menu-active { background: #e2e8f0; color: #0f172a; font-weight: 500; border-left: 3px solid #2563eb; }

/* Header */
.page-title { font-size: 22px; font-weight: 700; color: #0f172a; }
.page-sub { font-size: 12px; color: #64748b; margin-bottom: 1rem; }
.sec-title { font-size: 11px; font-weight: 600; text-transform: uppercase; color: #94a3b8; border-bottom: 1px solid #e2e8f0; margin: 1.2rem 0 0.6rem; padding-bottom: 4px; }

/* Cards */
.mcard { background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 14px; text-align: center; box-shadow: 0 1px 2px rgba(0,0,0,0.03); }
.mcard-num { font-size: 28px; font-weight: 700; }
.mcard-lbl { font-size: 11px; color: #64748b; margin-top: 4px; }
.c-blue { color: #3b82f6; }
.c-red { color: #ef4444; }
.c-green { color: #10b981; }
.c-yellow { color: #f59e0b; }
.c-purple { color: #8b5cf6; }
.c-orange { color: #f97316; }
.c-indigo { color: #6366f1; }

/* Badges */
.classificacao-publica { background: #e8f5e9; color: #2e7d32; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; display: inline-block; }
.classificacao-interna { background: #e3f2fd; color: #1565c0; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; display: inline-block; }
.classificacao-restrita { background: #fff3e0; color: #e65100; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; display: inline-block; }
.classificacao-confidencial { background: #ffebee; color: #c62828; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; display: inline-block; }

/* NDA Badge */
.nda-assinado { background: #e8f5e9; color: #2e7d32; padding: 2px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; display: inline-block; }
.nda-pendente { background: #ffebee; color: #c62828; padding: 2px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; display: inline-block; }
.nda-expirado { background: #fff3e0; color: #e65100; padding: 2px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; display: inline-block; }

/* Matriz de Classificação */
.matriz-card { border-radius: 12px; padding: 18px 12px; text-align: center; transition: all 0.2s ease; cursor: pointer; height: 100%; }
.matriz-card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
.matriz-card-active { border-width: 2px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
.matriz-icon { font-size: 32px; margin-bottom: 8px; }
.matriz-title { font-size: 14px; font-weight: 700; margin-bottom: 6px; }
.matriz-desc { font-size: 10px; opacity: 0.75; margin-bottom: 8px; }

/* Gráficos */
.chart-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px; margin-bottom: 16px; height: 100%; }
.chart-title { font-size: 13px; font-weight: 600; border-left: 3px solid #3b82f6; padding-left: 10px; margin-bottom: 14px; }

/* Threat lifecycle */
.threat-cycle { display: flex; justify-content: space-between; gap: 8px; margin: 16px 0; flex-wrap: wrap; }
.threat-stage { flex: 1; text-align: center; padding: 12px 6px; border-radius: 10px; color: white; min-width: 90px; }

/* Info box */
.info-box { padding: 10px 14px; border-radius: 10px; margin-bottom: 16px; border-left: 4px solid; font-size: 12px; }

/* Botões */
.stButton > button { background: #1e293b !important; color: #fff !important; border-radius: 8px !important; font-size: 13px !important; padding: 0.4rem 0.8rem !important; }
.stButton > button:hover { background: #334155 !important; }

/* NDA Card */
.nda-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px; margin-bottom: 12px; transition: all 0.2s; }
.nda-card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
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
# FUNÇÕES SUPABASE - NDA
# ──────────────────────────────────────────────
def salvar_ndas_supabase(supabase, df, usuario):
    if not supabase: return False
    try:
        supabase.table("acordos_nda").delete().neq("id", 0).execute()
        for _, row in df.iterrows():
            supabase.table("acordos_nda").insert({
                "colaborador": row["Colaborador"], "cargo": row["Cargo"],
                "data_assinatura": row.get("Data Assinatura", ""), "data_validade": row.get("Data Validade", ""),
                "status": row["Status"], "termos_principais": row.get("Termos Principais", ""),
                "anexo": row.get("Anexo", ""), "usuario": usuario
            }).execute()
        supabase.table("historico_seguranca").insert({
            "tipo": "acordos_nda", "dados": json.dumps(df.to_dict('records')), "usuario": usuario
        }).execute()
        return True
    except: return False

def carregar_ndas_supabase(supabase):
    if not supabase: return None
    try:
        r = supabase.table("acordos_nda").select("*").execute()
        if r.data:
            df = pd.DataFrame(r.data).rename(columns={
                "colaborador":"Colaborador","cargo":"Cargo","data_assinatura":"Data Assinatura",
                "data_validade":"Data Validade","status":"Status","termos_principais":"Termos Principais","anexo":"Anexo"
            })
            return df[["Colaborador","Cargo","Data Assinatura","Data Validade","Status","Termos Principais","Anexo"]]
        return None
    except: return None

# ──────────────────────────────────────────────
# FUNÇÕES SUPABASE - OUTRAS
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
    st.stop()

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
supabase = init_supabase()

if supabase:
    dados_risco_db = carregar_riscos_supabase(supabase)
    dados_eq_db = carregar_equipamentos_supabase(supabase)
    dados_pdca_db = carregar_pdca_supabase(supabase)
    dados_controles_db = carregar_controles_supabase(supabase)
    dados_codigo_db = carregar_codigo_conduta_supabase(supabase)
    dados_classificacao_db = carregar_classificacao_supabase(supabase)
    dados_ameacas_db = carregar_ameacas_supabase(supabase)
    dados_segregacao_db = carregar_segregacao_supabase(supabase)
    dados_ndas_db = carregar_ndas_supabase(supabase)
else:
    dados_risco_db = dados_eq_db = dados_controles_db = dados_codigo_db = dados_classificacao_db = dados_ameacas_db = dados_ndas_db = None
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
        "Cumprir todas as leis, regulamentos e normas aplicáveis.",
        "Tratar todos os colegas, clientes e parceiros com respeito e dignidade.",
        "Assumir responsabilidade pelas próprias ações e decisões.",
        "Manter comunicação clara, aberta e honesta.",
        "Demonstrar comprometimento com os objetivos da organização.",
        "Utilizar tecnologia de forma ética e responsável.",
    ],
    "Aplicável a": ["Todos", "Todos", "Todos", "Todos", "Gestores", "Lideranças", "Todos", "TI"],
    "Consequências": ["Advertência e demissão", "Medidas disciplinares", "Sanções legais", "Advertência", "Revisão de função", "Avaliação", "Aviso", "Advertência"],
    "Status": ["Ativo", "Ativo", "Ativo", "Ativo", "Ativo", "Ativo", "Ativo", "Ativo"],
    "Data Revisão": ["2024-01-01"] * 8,
    "Versão": ["2.0"] * 8,
})

edited_classificacao = dados_classificacao_db if (dados_classificacao_db is not None and not dados_classificacao_db.empty) else pd.DataFrame({
    "Ativo de Informação": ["Relatório Financeiro", "Dados de Clientes", "Políticas Internas", "Manuais Técnicos", "Estratégia", "Comunicados", "Código Fonte", "Contratos"],
    "Proprietário": ["CFO", "DPO", "RH", "TI", "CEO", "Marketing", "CTO", "Jurídico"],
    "Classificação": ["Restrita", "Confidencial", "Interna", "Interna", "Confidencial", "Pública", "Restrita", "Confidencial"],
    "Nível de Sigilo": ["Alto", "Máximo", "Médio", "Médio", "Máximo", "Baixo", "Alto", "Alto"],
    "Justificativa": ["Financeiro", "LGPD", "Interno", "Técnico", "Estratégico", "Externo", "IP", "Legal"],
    "Tempo de Retenção": ["5 anos", "Indeterminado", "2 anos", "3 anos", "3 anos", "1 ano", "Indeterminado", "10 anos"],
    "Controles Necessários": ["Criptografia", "LGPD", "Intranet", "Versão", "Sala cofre", "Aprovação", "Repositório", "Digital"],
    "Data Classificação": ["2024-01-15"] * 8,
    "Revisado por": ["Comitê"] * 8,
})

edited_ameacas = dados_ameacas_db if (dados_ameacas_db is not None and not dados_ameacas_db.empty) else pd.DataFrame({
    "Ameaça": ["Ransomware", "Phishing", "DDoS", "Insider Threat", "Zero-Day", "MITM"],
    "Categoria": ["Malware", "Social", "Disponibilidade", "Pessoal", "Vulnerabilidade", "Rede"],
    "Nível Criticidade": ["Crítico", "Alto", "Alto", "Médio", "Crítico", "Médio"],
    "Descoberta em": ["2024-01-15", "2024-01-10", "2024-01-05", "2024-01-20", "2024-02-01", "2024-01-25"],
    "Descrição": ["Criptografia e resgate", "Falsos e-mails", "Sobrecarga de tráfego", "Ameaças internas", "Vulnerabilidade 0-day", "Interceptação"],
    "Técnicas de Ataque": ["Phishing", "E-mails falsos", "Botnets", "Abuso de acesso", "Exploração", "ARP Spoofing"],
    "Medidas de Mitigação": ["Backup, EDR", "Treinamento, MFA", "WAF", "Monitoramento", "Patch", "TLS"],
    "Status": ["Monitorando", "Mitigado", "Monitorando", "Controlado", "Investigando", "Mitigado"],
})

edited_ndas = dados_ndas_db if (dados_ndas_db is not None and not dados_ndas_db.empty) else pd.DataFrame({
    "Colaborador": ["João Silva", "Maria Santos", "Carlos Lima", "Ana Oliveira", "Pedro Costa", "Fernanda Souza"],
    "Cargo": ["Analista de Segurança", "Gerente de TI", "Desenvolvedor", "Coordenador", "Arquiteto", "Estagiário"],
    "Data Assinatura": ["2024-01-10", "2024-01-15", "2024-01-20", "2024-02-01", "2024-02-10", "2024-03-01"],
    "Data Validade": ["2027-01-10", "2027-01-15", "2027-01-20", "2027-02-01", "2027-02-10", "2027-03-01"],
    "Status": ["Assinado", "Assinado", "Assinado", "Assinado", "Pendente", "Assinado"],
    "Termos Principais": ["Confidencialidade total", "Proteção de dados", "Código fonte", "Estratégia", "Dados sensíveis", "Confidencialidade"],
    "Anexo": ["nda_joao.pdf", "nda_maria.pdf", "", "", "", ""],
})

# Corrigir Nível do Risco
edited_risco["Nível do Risco"] = edited_risco.apply(lambda r: nivel_risco(r["Probabilidade"], r["Impacto"]), axis=1)

# ──────────────────────────────────────────────
# SIDEBAR COM MENU
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div class='sb-logo'>🛡️ SecureOps</div>", unsafe_allow_html=True)
    st.markdown("<div class='sb-sub'>Gestão de Segurança</div>", unsafe_allow_html=True)
    st.markdown("<hr class='sb-div'>", unsafe_allow_html=True)
    st.markdown(f"**{st.session_state.usuario}**")
    st.markdown("<div style='font-size:11px;color:#64748b;'>Administrador</div>", unsafe_allow_html=True)
    st.markdown("<hr class='sb-div'>", unsafe_allow_html=True)
    
    # Menu de navegação
    st.markdown("<div class='sb-lbl'>Navegação</div>", unsafe_allow_html=True)
    
    # Abas do sistema
    MENU_ITENS = [
        ("📋 Dados", "dados"),
        ("📊 Gráficos", "graficos"),
        ("🔒 Controles", "controles"),
        ("🔐 Classificação", "classificacao"),
        ("📜 Código Conduta", "codigo"),
        ("🕵️ Ameaças", "ameacas"),
        ("👥 Segregação", "segregacao"),
        ("📄 Acordos NDA", "nda"),
        ("🔄 PDCA", "pdca"),
        ("📜 Histórico", "historico"),
    ]
    
    if 'menu_selecionado' not in st.session_state:
        st.session_state.menu_selecionado = "dados"
    
    for nome, id_item in MENU_ITENS:
        is_active = st.session_state.menu_selecionado == id_item
        st.markdown(f"""
        <div class='sb-menu-item {"sb-menu-active" if is_active else ""}' 
             onclick="parent.postMessage({{type:'set_menu', value:'{id_item}'}}, '*')">
            {nome}
        </div>
        """, unsafe_allow_html=True)
        if st.button(nome, key=f"menu_{id_item}", use_container_width=True):
            st.session_state.menu_selecionado = id_item
            st.rerun()
    
    st.markdown("<hr class='sb-div'>", unsafe_allow_html=True)
    
    # Resumo rápido
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
<div class='page-sub'>PDCA · Análise de Risco · Controles · Classificação · NDA · {hora_br.strftime('%d/%m/%Y %H:%M')}</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# FUNÇÃO PARA RENDERIZAR ABA SELECIONADA
# ──────────────────────────────────────────────
def render_dados():
    sec("📋 Análise de Risco")
    df_risco = st.data_editor(
        edited_risco, use_container_width=True, num_rows="dynamic",
        column_config={
            "Probabilidade": st.column_config.SelectboxColumn(options=["Baixa","Média","Alta"]),
            "Impacto": st.column_config.SelectboxColumn(options=["Baixo","Médio","Alto"]),
            "Nível do Risco": st.column_config.TextColumn(disabled=True),
        }, hide_index=True, key="risco_editor"
    )
    df_risco["Nível do Risco"] = df_risco.apply(lambda r: nivel_risco(r["Probabilidade"], r["Impacto"]), axis=1)
    
    sec("📡 Inventário de Equipamentos")
    df_eq = st.data_editor(
        edited_eq, use_container_width=True, num_rows="dynamic",
        column_config={
            "Tipo": st.column_config.SelectboxColumn(options=["Segurança","Rede","Servidor","Storage","Infraestrutura"]),
            "Status": st.column_config.SelectboxColumn(options=["Ativo","Inativo","Em Manutenção","Reserva"]),
        }, hide_index=True, key="equip_editor"
    )
    
    st.markdown("---")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        if st.button("☁️ Salvar Dados", use_container_width=True):
            if supabase:
                ok1 = salvar_riscos_supabase(supabase, df_risco, st.session_state.usuario)
                ok2 = salvar_equipamentos_supabase(supabase, df_eq, st.session_state.usuario)
                st.success("✅ Dados salvos!") if (ok1 and ok2) else st.error("❌ Erro ao salvar")
            else:
                st.error("❌ Supabase não conectado")
    with col_s2:
        if st.button("📥 Exportar Excel", use_container_width=True):
            with pd.ExcelWriter(f"secureops_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx") as writer:
                df_risco.to_excel(writer, sheet_name="Riscos", index=False)
                df_eq.to_excel(writer, sheet_name="Equipamentos", index=False)
            st.success("✅ Exportado!")

def render_graficos():
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
        assinados = len(edited_ndas[edited_ndas["Status"] == "Assinado"]) if not edited_ndas.empty else 0
        st.markdown(mcard(assinados, "NDA Assinados", "c-indigo"), unsafe_allow_html=True)

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
        cores_s = {"Máximo":"#ef4444","Alto":"#f97316","Médio":"#f59e0b","Baixo":"#10b981"}
        html2 = "".join([f"<div style='display:flex;justify-content:space-between;margin-bottom:10px;'><span style='color:{cores_s.get(k,'#64748b')};font-weight:600;'>● {k}</span><span><b>{v}</b></span></div>" for k, v in sigilo.items()])
        st.markdown(f"<div class='chart-card'>{html2}</div>", unsafe_allow_html=True)

def render_controles():
    sec("🔒 Controles de Segurança")
    st.markdown("""<div class='info-box' style='background:#eef2ff;border-color:#3b82f6;color:#1e40af;'>
    📌 Controles de segurança são medidas para evitar, combater ou minimizar perdas de ativos de informação.
    </div>""", unsafe_allow_html=True)

    df_controles = st.data_editor(
        edited_controles, use_container_width=True, num_rows="dynamic",
        column_config={
            "Categoria": st.column_config.SelectboxColumn(options=["Acesso","Malware","Backup","Rede","Monitoramento","Governança","Data Loss","SIEM","Física","Criptografia"]),
            "Tipo de Controle": st.column_config.SelectboxColumn(options=["Preventivo","Detectivo","Corretivo","Compensatório","Deterrente"]),
            "Status": st.column_config.SelectboxColumn(options=["Implantado","Parcial","Pendente","Planejado","Cancelado"]),
        }, hide_index=True, key="controles_editor"
    )

    if st.button("💾 Salvar Controles", use_container_width=True):
        if supabase and salvar_controles_supabase(supabase, df_controles, st.session_state.usuario):
            st.success("✅ Controles salvos!")

def render_classificacao():
    sec("🔐 Classificação da Informação")

    NIVEIS = [
        {"nome": "Pública", "emoji": "🌍", "bg": "#e8f5e9", "cor": "#2e7d32", "desc": "Acesso irrestrito", "exemplos": "Site, Comunicados"},
        {"nome": "Interna", "emoji": "🏢", "bg": "#e3f2fd", "cor": "#1565c0", "desc": "Uso interno", "exemplos": "Políticas, Manuais"},
        {"nome": "Restrita", "emoji": "🔒", "bg": "#fff3e0", "cor": "#e65100", "desc": "Acesso limitado", "exemplos": "Financeiro, Código"},
        {"nome": "Confidencial", "emoji": "🔐", "bg": "#ffebee", "cor": "#c62828", "desc": "Alto sigilo", "exemplos": "Clientes, Estratégia"},
    ]

    cols = st.columns(4)
    for i, nivel in enumerate(NIVEIS):
        with cols[i]:
            is_ativo = (st.session_state.matriz_ativa == nivel["nome"])
            st.markdown(f"""
            <div class='matriz-card' style='background:{nivel["bg"]}; border:2px solid {nivel["cor"] if is_ativo else nivel["cor"]}40;'>
                <div class='matriz-icon'>{nivel["emoji"]}</div>
                <div class='matriz-title' style='color:{nivel["cor"]};'>{nivel["nome"]}</div>
                <div class='matriz-desc'>{nivel["desc"]}</div>
                <div style='font-size:9px; color:#64748b;'>{nivel["exemplos"]}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Filtrar {nivel['nome']}", key=f"filtro_{nivel['nome']}", use_container_width=True):
                st.session_state.matriz_ativa = nivel["nome"] if not is_ativo else None
                st.rerun()

    if st.session_state.matriz_ativa:
        df_filtrado = edited_classificacao[edited_classificacao["Classificação"] == st.session_state.matriz_ativa]
        st.info(f"🔍 Filtrando: **{st.session_state.matriz_ativa}** — {len(df_filtrado)} ativo(s)")
        df_edit = df_filtrado
    else:
        df_edit = edited_classificacao

    st.markdown("---")
    st.markdown("#### 📋 Ativos de Informação")

    df_result = st.data_editor(
        df_edit, use_container_width=True, num_rows="dynamic",
        column_config={
            "Classificação": st.column_config.SelectboxColumn(options=["Pública","Interna","Restrita","Confidencial"]),
            "Nível de Sigilo": st.column_config.SelectboxColumn(options=["Baixo","Médio","Alto","Máximo"]),
        }, hide_index=True, key="classif_editor"
    )

    if st.button("💾 Salvar Classificação", use_container_width=True):
        if supabase and salvar_classificacao_supabase(supabase, df_result, st.session_state.usuario):
            st.success("✅ Classificação salva!")
            st.rerun()

def render_codigo():
    sec("📜 Código de Conduta")
    st.markdown("""<div class='info-box' style='background:#e0e7ff;border-color:#6366f1;color:#3730a3;'>
    📌 Princípios éticos e comportamentais que todos os colaboradores devem seguir.
    </div>""", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(mcard(len(edited_codigo), "Princípios", "c-blue"), unsafe_allow_html=True)
    with col2:
        ativos = len(edited_codigo[edited_codigo["Status"] == "Ativo"])
        st.markdown(mcard(ativos, "Ativos", "c-green"), unsafe_allow_html=True)
    with col3:
        st.markdown(mcard(edited_codigo["Categoria"].nunique(), "Categorias", "c-purple"), unsafe_allow_html=True)
    with col4:
        todos = len(edited_codigo[edited_codigo["Aplicável a"] == "Todos"])
        st.markdown(mcard(todos, "Aplicável a Todos", "c-yellow"), unsafe_allow_html=True)

    st.markdown("---")
    
    df_codigo = st.data_editor(
        edited_codigo, use_container_width=True, num_rows="dynamic",
        column_config={
            "Categoria": st.column_config.SelectboxColumn(options=["Ética","Segurança","Legal","Comportamental","Gestão","Governança","Tecnologia","Compromisso"]),
            "Status": st.column_config.SelectboxColumn(options=["Ativo","Revisão","Descontinuado"]),
            "Aplicável a": st.column_config.SelectboxColumn(options=["Todos","Gestores","Lideranças","TI","Colaboradores"]),
        }, hide_index=True, key="codigo_editor"
    )

    st.markdown("---")
    with st.expander("📋 Termo de Compromisso"):
        st.markdown("**DECLARAÇÃO DE COMPROMISSO**\n\nEu, _________________, declaro que li e concordo com o Código de Conduta.")
        nome = st.text_input("Nome completo")
        if st.button("📝 Assinar"):
            if nome:
                st.success(f"✅ Termo assinado por {nome}")

    if st.button("💾 Salvar Código", use_container_width=True):
        if supabase and salvar_codigo_conduta_supabase(supabase, df_codigo, st.session_state.usuario):
            st.success("✅ Código salvo!")

def render_ameacas():
    sec("🕵️ Inteligência de Ameaças")
    st.markdown("""<div class='info-box' style='background:#fce7f3;border-color:#db2777;color:#9d174d;'>
    📌 Investigação proativa de vulnerabilidades e técnicas de ataque.
    </div>""", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(mcard(len(edited_ameacas), "Total Ameaças", "c-blue"), unsafe_allow_html=True)
    with col2:
        criticas = len(edited_ameacas[edited_ameacas["Nível Criticidade"] == "Crítico"])
        st.markdown(mcard(criticas, "Críticas", "c-red"), unsafe_allow_html=True)
    with col3:
        monitorando = len(edited_ameacas[edited_ameacas["Status"] == "Monitorando"])
        st.markdown(mcard(monitorando, "Monitorando", "c-yellow"), unsafe_allow_html=True)
    with col4:
        mitigadas = len(edited_ameacas[edited_ameacas["Status"] == "Mitigado"])
        st.markdown(mcard(mitigadas, "Mitigadas", "c-green"), unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 🔄 Threat Intelligence Lifecycle")
    
    etapas = [("1", "Definir"), ("2", "Coletar"), ("3", "Processar"), ("4", "Analisar"), ("5", "Reportar")]
    cores = ["#3b82f6", "#8b5cf6", "#db2777", "#f59e0b", "#10b981"]
    cols = st.columns(5)
    for i, (num, titulo) in enumerate(etapas):
        with cols[i]:
            st.markdown(f"<div class='threat-stage' style='background:{cores[i]};'><div style='font-size:20px;font-weight:700;'>{num}</div><div>{titulo}</div></div>", unsafe_allow_html=True)

    st.markdown("---")
    
    df_ameacas = st.data_editor(
        edited_ameacas, use_container_width=True, num_rows="dynamic",
        column_config={
            "Categoria": st.column_config.SelectboxColumn(options=["Malware","Social","Disponibilidade","Pessoal","Vulnerabilidade","Rede"]),
            "Nível Criticidade": st.column_config.SelectboxColumn(options=["Crítico","Alto","Médio","Baixo"]),
            "Status": st.column_config.SelectboxColumn(options=["Monitorando","Mitigado","Investigando","Controlado"]),
        }, hide_index=True, key="ameacas_editor"
    )

    if st.button("💾 Salvar Ameaças", use_container_width=True):
        if supabase and salvar_ameacas_supabase(supabase, df_ameacas, st.session_state.usuario):
            st.success("✅ Ameaças salvas!")

def render_segregacao():
    sec("👥 Segregação de Funções")
    st.markdown("""<div class='info-box' style='background:#e6f7e6;border-color:#10b981;color:#065f46;'>
    📌 Evita conflitos de interesse e reduz risco de ações não autorizadas.
    </div>""", unsafe_allow_html=True)

    st.markdown("#### 🏛️ Pirâmide Hierárquica")
    
    niveis = st.session_state.piramide_niveis
    for nivel in niveis:
        largura = nivel.get("largura", 50)
        cor = nivel.get("cor", "#3b82f6")
        st.markdown(f"""
        <div style='width:{largura}%; background:{cor}; border-radius:10px; padding:10px 16px; margin:0 auto 6px auto; color:white; text-align:center;'>
            <div style='font-size:16px;'>{nivel.get('emoji', '🔹')}</div>
            <div style='font-size:12px; font-weight:700;'>{nivel.get('titulo', '')}</div>
            <div style='font-size:9px; opacity:0.85;'>{nivel.get('responsabilidades', '')[:50]}...</div>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("✏️ Editar níveis da pirâmide"):
        for i, nivel in enumerate(niveis):
            st.markdown(f"**Nível {i+1}**")
            col1, col2 = st.columns(2)
            with col1:
                nivel["titulo"] = st.text_input("Título", nivel.get("titulo", ""), key=f"tit_{i}")
                nivel["emoji"] = st.text_input("Emoji", nivel.get("emoji", "🔹"), key=f"emo_{i}")
            with col2:
                nivel["cor"] = st.color_picker("Cor", nivel.get("cor", "#3b82f6"), key=f"cor_{i}")
                nivel["largura"] = st.slider("Largura", 15, 100, nivel.get("largura", 50), key=f"larg_{i}")
            nivel["responsabilidades"] = st.text_area("Responsabilidades", nivel.get("responsabilidades", ""), key=f"resp_{i}", height=60)
            if st.button(f"🗑️ Remover", key=f"rem_{i}"):
                st.session_state.piramide_niveis.pop(i)
                st.rerun()
            st.markdown("---")
        
        if st.button("➕ Adicionar nível"):
            st.session_state.piramide_niveis.append({"emoji": "🔹", "titulo": "Novo Nível", "responsabilidades": "", "cor": "#3b82f6", "largura": 50})
            st.rerun()

    if st.button("💾 Salvar Pirâmide", use_container_width=True):
        if supabase and salvar_segregacao_supabase(supabase, st.session_state.piramide_niveis, st.session_state.usuario):
            st.success("✅ Pirâmide salva!")

def render_nda():
    sec("📄 Acordos de Confidencialidade (NDA)")
    st.markdown("""<div class='info-box' style='background:#f3e8ff;border-color:#a855f7;color:#6b21a5;'>
    📌 Acordos de não divulgação (NDA) protegem informações confidenciais da organização.
    </div>""", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(mcard(len(edited_ndas), "Total NDAs", "c-blue"), unsafe_allow_html=True)
    with col2:
        assinados = len(edited_ndas[edited_ndas["Status"] == "Assinado"]) if not edited_ndas.empty else 0
        st.markdown(mcard(assinados, "Assinados", "c-green"), unsafe_allow_html=True)
    with col3:
        pendentes = len(edited_ndas[edited_ndas["Status"] == "Pendente"]) if not edited_ndas.empty else 0
        st.markdown(mcard(pendentes, "Pendentes", "c-red"), unsafe_allow_html=True)
    with col4:
        expirados = len(edited_ndas[edited_ndas["Status"] == "Expirado"]) if not edited_ndas.empty else 0
        st.markdown(mcard(expirados, "Expirados", "c-yellow"), unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 📋 Lista de Acordos NDA")

    df_ndas = st.data_editor(
        edited_ndas, use_container_width=True, num_rows="dynamic",
        column_config={
            "Status": st.column_config.SelectboxColumn(options=["Assinado", "Pendente", "Expirado", "Cancelado"]),
        }, hide_index=True, key="nda_editor"
    )

    st.markdown("---")
    st.markdown("#### 📝 Modelo de NDA")
    
    with st.expander("Ver modelo do Acordo de Confidencialidade"):
        st.markdown("""
        **ACORDO DE CONFIDENCIALIDADE E NÃO DIVULGAÇÃO (NDA)**
        
        **CLÁUSULA 1 - DEFINIÇÃO**
        Consideram-se Informações Confidenciais todos os dados, documentos, projetos, códigos, estratégias, 
        listas de clientes, propriedade intelectual e demais informações não públicas da empresa.
        
        **CLÁUSULA 2 - OBRIGAÇÕES DO SIGNATÁRIO**
        O signatário compromete-se a:
        - Não divulgar as Informações Confidenciais a terceiros
        - Utilizar as informações apenas para fins profissionais
        - Proteger os documentos contra acesso não autorizado
        - Reportar imediatamente qualquer violação
        
        **CLÁUSULA 3 - VIGÊNCIA**
        Este acordo vigorará durante o período de vínculo com a empresa e por 5 (cinco) anos após seu término.
        
        **CLÁUSULA 4 - PENALIDADES**
        O descumprimento deste acordo sujeitará o infrator a medidas disciplinares, incluindo demissão por 
        justa causa e ações legais cabíveis.
        
        **Data: ___/___/______**
        **Assinatura: _________________________**
        """)
        
        nome_nda = st.text_input("Nome do colaborador", placeholder="Nome completo")
        cargo_nda = st.text_input("Cargo", placeholder="Cargo do colaborador")
        if st.button("📝 Gerar NDA"):
            if nome_nda and cargo_nda:
                st.success(f"✅ NDA gerado para {nome_nda} ({cargo_nda}) - Aguardando assinatura")
            else:
                st.warning("Preencha nome e cargo")

    if st.button("💾 Salvar Acordos NDA", use_container_width=True):
        if supabase and salvar_ndas_supabase(supabase, df_ndas, st.session_state.usuario):
            st.success("✅ NDAs salvos!")

def render_pdca():
    st.markdown("### 🔄 PDCA de Gestão de Segurança")

    fases = [
        {"nome": "1. Contexto", "cor": "#3b82f6"}, {"nome": "2. Liderança", "cor": "#3b82f6"},
        {"nome": "3. Planejamento", "cor": "#3b82f6"}, {"nome": "4. Suporte", "cor": "#f59e0b"},
        {"nome": "5. Operação", "cor": "#f59e0b"}, {"nome": "6. Avaliação", "cor": "#10b981"},
        {"nome": "7. Melhoria", "cor": "#8b5cf6"},
    ]
    linhas = ["🎯 Objetivo Estratégico", "⚙️ Ação Técnica", "📊 Indicador KPI", "🚩 Evidência Status"]
    
    pdca_data = dados_pdca_db if dados_pdca_db else {}
    
    cols = st.columns(7, gap="small")
    for i, (col, fase) in enumerate(zip(cols, fases)):
        with col:
            st.markdown(f"""
            <div style='background:{fase["cor"]}15; border:2px solid {fase["cor"]}40; border-radius:10px; padding:10px; text-align:center; margin-bottom:10px;'>
                <div style='font-size:11px; font-weight:800; color:{fase["cor"]};'>{fase["nome"]}</div>
            </div>
            """, unsafe_allow_html=True)
            for j, linha in enumerate(linhas):
                st.markdown(f"<div style='font-size:9px; font-weight:600; color:#64748b; margin-bottom:2px;'>{linha}</div>", unsafe_allow_html=True)
                pdca_data[(i, j)] = st.text_area("", value=pdca_data.get((i, j), ""), placeholder="...", label_visibility="collapsed", height=70, key=f"pdca_{i}_{j}")

    if st.button("💾 Salvar PDCA", use_container_width=True):
        if supabase and salvar_pdca_supabase(supabase, pdca_data, st.session_state.usuario):
            st.success("✅ PDCA salvo!")

def render_historico():
    st.markdown("### 📜 Histórico de Alterações")
    tipo = st.selectbox("Filtrar:", ["Todos", "analise_risco", "equipamentos", "controles", "codigo_conduta", "classificacao_informacao", "inteligencia_ameacas", "segregacao_funcoes", "acordos_nda", "pdca"])
    if supabase:
        df_hist = carregar_historico_supabase(supabase, None if tipo == "Todos" else tipo)
        if not df_hist.empty:
            st.dataframe(df_hist, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum registro no histórico.")

# ──────────────────────────────────────────────
# RENDERIZAR ABA SELECIONADA
# ──────────────────────────────────────────────
menu = st.session_state.menu_selecionado

if menu == "dados":
    render_dados()
elif menu == "graficos":
    render_graficos()
elif menu == "controles":
    render_controles()
elif menu == "classificacao":
    render_classificacao()
elif menu == "codigo":
    render_codigo()
elif menu == "ameacas":
    render_ameacas()
elif menu == "segregacao":
    render_segregacao()
elif menu == "nda":
    render_nda()
elif menu == "pdca":
    render_pdca()
elif menu == "historico":
    render_historico()

# ──────────────────────────────────────────────
# SIDEBAR RESUMO
# ──────────────────────────────────────────────
with sidebar_ph:
    alto_s = len(edited_risco[edited_risco["Nível do Risco"] == "🔴 Alto"])
    medio_s = len(edited_risco[edited_risco["Nível do Risco"] == "🟡 Médio"])
    baixo_s = len(edited_risco[edited_risco["Nível do Risco"] == "🟢 Baixo"])
    ctrl_impl = len(edited_controles[edited_controles["Status"] == "Implantado"])
    ameacas_crit = len(edited_ameacas[edited_ameacas["Nível Criticidade"] == "Crítico"]) if not edited_ameacas.empty else 0
    nda_assinados = len(edited_ndas[edited_ndas["Status"] == "Assinado"]) if not edited_ndas.empty else 0

    st.markdown(f"""
    <div style='background:#fee2e2; color:#dc2626; display:flex; justify-content:space-between; padding:8px 12px; border-radius:10px; margin-bottom:6px;'>
        <span>🔴 Riscos Altos</span><span style='font-size:18px; font-weight:700;'>{alto_s}</span>
    </div>
    <div style='background:#fef3c7; color:#d97706; display:flex; justify-content:space-between; padding:8px 12px; border-radius:10px; margin-bottom:6px;'>
        <span>🟡 Riscos Médios</span><span style='font-size:18px; font-weight:700;'>{medio_s}</span>
    </div>
    <div style='background:#dcfce7; color:#16a34a; display:flex; justify-content:space-between; padding:8px 12px; border-radius:10px; margin-bottom:6px;'>
        <span>🟢 Riscos Baixos</span><span style='font-size:18px; font-weight:700;'>{baixo_s}</span>
    </div>
    <div style='background:#dbeafe; color:#2563eb; display:flex; justify-content:space-between; padding:8px 12px; border-radius:10px; margin-bottom:6px;'>
        <span>✅ Controles OK</span><span style='font-size:18px; font-weight:700;'>{ctrl_impl}</span>
    </div>
    <div style='background:#fee2e2; color:#dc2626; display:flex; justify-content:space-between; padding:8px 12px; border-radius:10px; margin-bottom:6px;'>
        <span>🚨 Ameaças Críticas</span><span style='font-size:18px; font-weight:700;'>{ameacas_crit}</span>
    </div>
    <div style='background:#f3e8ff; color:#9333ea; display:flex; justify-content:space-between; padding:8px 12px; border-radius:10px; margin-bottom:6px;'>
        <span>📄 NDAs Assinados</span><span style='font-size:18px; font-weight:700;'>{nda_assinados}</span>
    </div>
    """, unsafe_allow_html=True)
