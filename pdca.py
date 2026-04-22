import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta
from supabase import create_client, Client
import json
import hashlib

st.set_page_config(
    layout="wide",
    page_title="SecureOps — Gestão de Segurança",
    page_icon="🛡️",
    initial_sidebar_state="expanded"
)

# Remove header, toolbar, footer e deploy button do Streamlit
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
.viewerBadge_link__1S137 { display: none !important; }
#stDecoration { display: none !important; }
.styles_viewerBadge__CvC9N { display: none !important; }
[class*="viewerBadge"] { display: none !important; }
[class*="ActionButton"] { display: none !important; }
[data-testid="baseButton-headerNoPadding"] { display: none !important; }
.block-container { padding-top: 0.5rem !important; }
</style>
""", unsafe_allow_html=True)

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
# FUNÇÕES DO SUPABASE - CÓDIGO DE CONDUTA
# ──────────────────────────────────────────────
def salvar_codigo_conduta_supabase(supabase, df_codigo, usuario):
    if not supabase:
        return False
    try:
        supabase.table("codigo_conduta").delete().neq("id", 0).execute()
        for _, row in df_codigo.iterrows():
            supabase.table("codigo_conduta").insert({
                "principio": row["Princípio"],
                "categoria": row["Categoria"],
                "descricao": row["Descrição"],
                "aplicavel_a": row["Aplicável a"],
                "consequencias": row["Consequências"],
                "status": row["Status"],
                "data_revisao": row.get("Data Revisão", ""),
                "versao": row.get("Versão", "1.0"),
                "usuario": usuario
            }).execute()
        supabase.table("historico_seguranca").insert({
            "tipo": "codigo_conduta",
            "dados": json.dumps(df_codigo.to_dict('records')),
            "usuario": usuario
        }).execute()
        return True
    except Exception as e:
        st.error(f"Erro ao salvar código de conduta: {e}")
        return False

def carregar_codigo_conduta_supabase(supabase):
    if not supabase:
        return None
    try:
        response = supabase.table("codigo_conduta").select("*").execute()
        if response.data:
            df = pd.DataFrame(response.data)
            df = df.rename(columns={
                "principio": "Princípio",
                "categoria": "Categoria",
                "descricao": "Descrição",
                "aplicavel_a": "Aplicável a",
                "consequencias": "Consequências",
                "status": "Status",
                "data_revisao": "Data Revisão",
                "versao": "Versão"
            })
            return df[["Princípio", "Categoria", "Descrição", "Aplicável a", "Consequências", "Status", "Data Revisão", "Versão"]]
        return None
    except:
        return None

# ──────────────────────────────────────────────
# FUNÇÕES DO SUPABASE - CLASSIFICAÇÃO DA INFORMAÇÃO
# ──────────────────────────────────────────────
def salvar_classificacao_supabase(supabase, df_classificacao, usuario):
    if not supabase:
        return False
    try:
        supabase.table("classificacao_informacao").delete().neq("id", 0).execute()
        for _, row in df_classificacao.iterrows():
            supabase.table("classificacao_informacao").insert({
                "ativo_informacao": row["Ativo de Informação"],
                "proprietario": row["Proprietário"],
                "classificacao": row["Classificação"],
                "nivel_sigilo": row["Nível de Sigilo"],
                "justificativa": row["Justificativa"],
                "tempo_retencao": row["Tempo de Retenção"],
                "controles_necessarios": row["Controles Necessários"],
                "data_classificacao": row.get("Data Classificação", ""),
                "revisado_por": row.get("Revisado por", ""),
                "usuario": usuario
            }).execute()
        supabase.table("historico_seguranca").insert({
            "tipo": "classificacao_informacao",
            "dados": json.dumps(df_classificacao.to_dict('records')),
            "usuario": usuario
        }).execute()
        return True
    except Exception as e:
        st.error(f"Erro ao salvar classificação: {e}")
        return False

def carregar_classificacao_supabase(supabase):
    if not supabase:
        return None
    try:
        response = supabase.table("classificacao_informacao").select("*").execute()
        if response.data:
            df = pd.DataFrame(response.data)
            df = df.rename(columns={
                "ativo_informacao": "Ativo de Informação",
                "proprietario": "Proprietário",
                "classificacao": "Classificação",
                "nivel_sigilo": "Nível de Sigilo",
                "justificativa": "Justificativa",
                "tempo_retencao": "Tempo de Retenção",
                "controles_necessarios": "Controles Necessários",
                "data_classificacao": "Data Classificação",
                "revisado_por": "Revisado por"
            })
            return df[["Ativo de Informação", "Proprietário", "Classificação", "Nível de Sigilo", "Justificativa", "Tempo de Retenção", "Controles Necessários", "Data Classificação", "Revisado por"]]
        return None
    except:
        return None

# ──────────────────────────────────────────────
# FUNÇÕES DO SUPABASE - OUTRAS TABELAS
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
    if not supabase:
        return False
    try:
        supabase.table("pdca").delete().neq("id", 0).execute()
        for key, value in dados_pdca.items():
            fase_idx, linha_idx = key
            fases = ["1. Contexto", "2. Liderança", "3. Planejamento", "4. Suporte", "5. Operação", "6. Avaliação", "7. Melhoria"]
            linhas = ["Objetivo Estratégico", "Ação Técnica", "Indicador KPI", "Evidência Status"]
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
    if not supabase:
        return {}
    try:
        response = supabase.table("pdca").select("*").execute()
        if response.data:
            dados_pdca = {}
            for item in response.data:
                fase = item["fase"]
                linha = item["linha"]
                fases = ["1. Contexto", "2. Liderança", "3. Planejamento", "4. Suporte", "5. Operação", "6. Avaliação", "7. Melhoria"]
                linhas = ["Objetivo Estratégico", "Ação Técnica", "Indicador KPI", "Evidência Status"]
                if fase in fases and linha in linhas:
                    i = fases.index(fase)
                    j = linhas.index(linha)
                    dados_pdca[(i, j)] = item["conteudo"]
            return dados_pdca
        return {}
    except:
        return {}

def salvar_controles_supabase(supabase, df_controles, usuario):
    if not supabase:
        return False
    try:
        supabase.table("controles_seguranca").delete().neq("id", 0).execute()
        for _, row in df_controles.iterrows():
            supabase.table("controles_seguranca").insert({
                "controle": row["Controle"],
                "categoria": row["Categoria"],
                "descricao": row["Descrição"],
                "tipo_controle": row["Tipo de Controle"],
                "status": row["Status"],
                "data_implementacao": row.get("Data Implementação", ""),
                "responsavel": row.get("Responsável", ""),
                "efetividade": row.get("Efetividade", ""),
                "usuario": usuario
            }).execute()
        supabase.table("historico_seguranca").insert({
            "tipo": "controles",
            "dados": json.dumps(df_controles.to_dict('records')),
            "usuario": usuario
        }).execute()
        return True
    except:
        return False

def carregar_controles_supabase(supabase):
    if not supabase:
        return None
    try:
        response = supabase.table("controles_seguranca").select("*").execute()
        if response.data:
            df = pd.DataFrame(response.data)
            df = df.rename(columns={
                "controle": "Controle",
                "categoria": "Categoria",
                "descricao": "Descrição",
                "tipo_controle": "Tipo de Controle",
                "status": "Status",
                "data_implementacao": "Data Implementação",
                "responsavel": "Responsável",
                "efetividade": "Efetividade"
            })
            return df[["Controle", "Categoria", "Descrição", "Tipo de Controle", "Status", "Data Implementação", "Responsável", "Efetividade"]]
        return None
    except:
        return None

def salvar_ameacas_supabase(supabase, df_ameacas, usuario):
    if not supabase:
        return False
    try:
        supabase.table("inteligencia_ameacas").delete().neq("id", 0).execute()
        for _, row in df_ameacas.iterrows():
            supabase.table("inteligencia_ameacas").insert({
                "ameaca": row["Ameaça"],
                "categoria": row["Categoria"],
                "nivel_criticidade": row["Nível Criticidade"],
                "descoberta_em": row["Descoberta em"],
                "descricao": row["Descrição"],
                "tecnicas_ataque": row["Técnicas de Ataque"],
                "medidas_mitigacao": row["Medidas de Mitigação"],
                "status": row["Status"],
                "usuario": usuario
            }).execute()
        supabase.table("historico_seguranca").insert({
            "tipo": "inteligencia_ameacas",
            "dados": json.dumps(df_ameacas.to_dict('records')),
            "usuario": usuario
        }).execute()
        return True
    except:
        return False

def carregar_ameacas_supabase(supabase):
    if not supabase:
        return None
    try:
        response = supabase.table("inteligencia_ameacas").select("*").execute()
        if response.data:
            df = pd.DataFrame(response.data)
            df = df.rename(columns={
                "ameaca": "Ameaça",
                "categoria": "Categoria",
                "nivel_criticidade": "Nível Criticidade",
                "descoberta_em": "Descoberta em",
                "descricao": "Descrição",
                "tecnicas_ataque": "Técnicas de Ataque",
                "medidas_mitigacao": "Medidas de Mitigação",
                "status": "Status"
            })
            return df[["Ameaça", "Categoria", "Nível Criticidade", "Descoberta em", "Descrição", "Técnicas de Ataque", "Medidas de Mitigação", "Status"]]
        return None
    except:
        return None

def salvar_segregacao_supabase(supabase, df_segregacao, usuario):
    if not supabase:
        return False
    try:
        supabase.table("segregacao_funcoes").delete().neq("id", 0).execute()
        for _, row in df_segregacao.iterrows():
            supabase.table("segregacao_funcoes").insert({
                "cargo": row["Cargo"],
                "nivel": row["Nível"],
                "responsabilidades": row["Responsabilidades"],
                "acessos_autorizados": row["Acessos Autorizados"],
                "principio_need_to_know": row["Need to Know"],
                "segregacao_aplicada": row["Segregação Aplicada"],
                "aprovador": row.get("Aprovador", ""),
                "data_revisao": row.get("Data Revisão", ""),
                "usuario": usuario
            }).execute()
        supabase.table("historico_seguranca").insert({
            "tipo": "segregacao_funcoes",
            "dados": json.dumps(df_segregacao.to_dict('records')),
            "usuario": usuario
        }).execute()
        return True
    except:
        return False

def carregar_segregacao_supabase(supabase):
    if not supabase:
        return None
    try:
        response = supabase.table("segregacao_funcoes").select("*").execute()
        if response.data:
            df = pd.DataFrame(response.data)
            df = df.rename(columns={
                "cargo": "Cargo",
                "nivel": "Nível",
                "responsabilidades": "Responsabilidades",
                "acessos_autorizados": "Acessos Autorizados",
                "principio_need_to_know": "Need to Know",
                "segregacao_aplicada": "Segregação Aplicada",
                "aprovador": "Aprovador",
                "data_revisao": "Data Revisão"
            })
            return df[["Cargo", "Nível", "Responsabilidades", "Acessos Autorizados", "Need to Know", "Segregação Aplicada", "Aprovador", "Data Revisão"]]
        return None
    except:
        return None

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

def obter_hora_brasil():
    utc_now = datetime.now(timezone.utc)
    brasilia_offset = timedelta(hours=-3)
    brasilia_time = utc_now + brasilia_offset
    return brasilia_time

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
.sb-blue { background: #dbeafe; color: #2563eb; }
.sb-purple { background: #ede9fe; color: #7c3aed; }
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
.c-purple { color: #7c3aed; }
.classificacao-publica { background: #dcfce7; color: #166534; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; display: inline-block; }
.classificacao-interna { background: #dbeafe; color: #1e40af; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; display: inline-block; }
.classificacao-restrita { background: #fed7aa; color: #9a3412; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; display: inline-block; }
.classificacao-confidencial { background: #fee2e2; color: #991b1b; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; display: inline-block; }
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
<div class='page-sub'>PDCA + Análise de Risco + Controles + Classificação · {hora_br.strftime('%d/%m/%Y %H:%M')}</div>
""", unsafe_allow_html=True)

# ── Carregar dados do Supabase ──
if supabase:
    dados_risco_carregado = carregar_riscos_supabase(supabase)
    dados_eq_carregado = carregar_equipamentos_supabase(supabase)
    dados_pdca_carregado = carregar_pdca_supabase(supabase)
    dados_controles_carregado = carregar_controles_supabase(supabase)
    dados_codigo_carregado = carregar_codigo_conduta_supabase(supabase)
    dados_classificacao_carregado = carregar_classificacao_supabase(supabase)
    dados_ameacas_carregado = carregar_ameacas_supabase(supabase)
    dados_segregacao_carregado = carregar_segregacao_supabase(supabase)
else:
    dados_risco_carregado = None
    dados_eq_carregado = None
    dados_pdca_carregado = {}
    dados_controles_carregado = None
    dados_codigo_carregado = None
    dados_classificacao_carregado = None
    dados_ameacas_carregado = None
    dados_segregacao_carregado = None

# ── Dados Riscos ──
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

# ── Dados Equipamentos ──
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

# ── Dados Controles ──
if dados_controles_carregado is not None and not dados_controles_carregado.empty:
    edited_controles = dados_controles_carregado
else:
    edited_controles = pd.DataFrame({
        "Controle": ["Controle de Acesso", "Antivírus Centralizado", "Backup Automatizado", "Firewall de Rede", "Monitoramento 24/7", "Política de Senhas", "DLP", "SIEM"],
        "Categoria": ["Acesso", "Malware", "Backup", "Rede", "Monitoramento", "Governança", "Data Loss", "SIEM"],
        "Descrição": ["Controle de acesso baseado em RBAC", "Antivírus com atualização automática", "Backup diário com retenção de 30 dias", "Firewall com inspeção de pacotes", "Monitoramento contínuo de ativos", "Política de senhas fortes e troca mensal", "Prevenção contra vazamento de dados", "Correlação de eventos de segurança"],
        "Tipo de Controle": ["Preventivo", "Detectivo", "Corretivo", "Preventivo", "Detectivo", "Preventivo", "Preventivo", "Detectivo"],
        "Status": ["Implantado", "Implantado", "Implantado", "Implantado", "Parcial", "Pendente", "Planejado", "Planejado"],
        "Data Implementação": ["2024-01-15", "2024-01-10", "2024-01-20", "2024-02-01", "2024-03-10", "", "", ""],
        "Responsável": ["TI", "TI", "DBA", "Rede", "SecOps", "Governança", "SecOps", "SecOps"],
        "Efetividade": ["95%", "90%", "100%", "85%", "60%", "", "", ""],
    })

# ── Dados Código de Conduta ──
if dados_codigo_carregado is not None and not dados_codigo_carregado.empty:
    edited_codigo = dados_codigo_carregado
else:
    edited_codigo = pd.DataFrame({
        "Princípio": ["Integridade", "Confidencialidade", "Conformidade", "Respeito", "Responsabilidade", "Transparência"],
        "Categoria": ["Ética", "Segurança", "Legal", "Comportamental", "Gestão", "Governança"],
        "Descrição": ["Agir com honestidade em todas as atividades", "Proteger informações confidenciais da organização", "Cumprir leis e regulamentos aplicáveis", "Tratar todos com respeito e dignidade", "Assumir responsabilidade por ações e decisões", "Manter comunicação clara e aberta"],
        "Aplicável a": ["Todos", "Todos", "Todos", "Todos", "Gestores", "Lideranças"],
        "Consequências": ["Advertência e demissão", "Medidas disciplinares", "Sanções legais", "Advertência", "Revisão de função", "Avaliação de desempenho"],
        "Status": ["Ativo", "Ativo", "Ativo", "Ativo", "Ativo", "Ativo"],
        "Data Revisão": ["2024-01-01", "2024-01-01", "2024-01-01", "2024-01-01", "2024-01-01", "2024-01-01"],
        "Versão": ["1.0", "1.0", "1.0", "1.0", "1.0", "1.0"],
    })

# ── Dados Classificação da Informação ──
if dados_classificacao_carregado is not None and not dados_classificacao_carregado.empty:
    edited_classificacao = dados_classificacao_carregado
else:
    edited_classificacao = pd.DataFrame({
        "Ativo de Informação": ["Relatório Financeiro", "Dados de Clientes", "Políticas Internas", "Manuais Técnicos", "Estratégia de Negócio", "Comunicados", "Código Fonte", "Contratos"],
        "Proprietário": ["CFO", "DPO", "RH", "TI", "CEO", "Marketing", "CTO", "Jurídico"],
        "Classificação": ["Restrita", "Confidencial", "Interna", "Interna", "Confidencial", "Pública", "Restrita", "Confidencial"],
        "Nível de Sigilo": ["Alto", "Máximo", "Médio", "Médio", "Máximo", "Baixo", "Alto", "Alto"],
        "Justificativa": ["Informações financeiras sensíveis", "Dados pessoais LGPD", "Diretrizes internas", "Conhecimento técnico", "Planejamento estratégico", "Comunicação externa", "Propriedade intelectual", "Cláusulas contratuais"],
        "Tempo de Retenção": ["5 anos", "Indeterminado", "2 anos", "3 anos", "3 anos", "1 ano", "Indeterminado", "10 anos"],
        "Controles Necessários": ["Criptografia, Auditoria", "LGPD, Acesso restrito", "Intranet, Autenticação", "Controle de versão", "Sala cofre, NDA", "Aprovação de marketing", "Repositório privado", "Assinatura digital"],
        "Data Classificação": ["2024-01-15", "2024-01-10", "2024-01-05", "2024-01-20", "2024-01-25", "2024-01-30", "2024-02-01", "2024-02-05"],
        "Revisado por": ["Comitê", "DPO", "RH", "TI", "Diretoria", "Marketing", "TI", "Jurídico"],
    })

# ── Dados Ameaças ──
if dados_ameacas_carregado is not None and not dados_ameacas_carregado.empty:
    edited_ameacas = dados_ameacas_carregado
else:
    edited_ameacas = pd.DataFrame({
        "Ameaça": ["Ransomware", "Phishing", "DDoS", "Insider Threat", "Zero-Day", "Man-in-the-Middle"],
        "Categoria": ["Malware", "Engenharia Social", "Disponibilidade", "Pessoal", "Vulnerabilidade", "Rede"],
        "Nível Criticidade": ["Crítico", "Alto", "Alto", "Médio", "Crítico", "Médio"],
        "Descoberta em": ["2024-01-15", "2024-01-10", "2024-01-05", "2024-01-20", "2024-02-01", "2024-01-25"],
        "Descrição": ["Criptografia de dados mediante resgate", "Tentativas de obter informações sensíveis", "Sobrecarga de tráfego", "Ameaças internas maliciosas", "Vulnerabilidade desconhecida", "Interceptação de comunicação"],
        "Técnicas de Ataque": ["Phishing, Exploits", "E-mails fraudulentos", "Botnets, Amplificação", "Abuso de privilégios", "Exploração não patched", "ARP Spoofing, SSL Strip"],
        "Medidas de Mitigação": ["Backup, Antivírus", "Treinamento, Filtros", "WAF, Rate limiting", "Monitoramento, Segregação", "Patch management, EDR", "Criptografia, Certificados"],
        "Status": ["Monitorando", "Mitigado", "Monitorando", "Controlado", "Investigando", "Mitigado"],
    })

# ── Dados Segregação ──
if dados_segregacao_carregado is not None and not dados_segregacao_carregado.empty:
    edited_segregacao = dados_segregacao_carregado
else:
    edited_segregacao = pd.DataFrame({
        "Cargo": ["Diretor de TI", "Gerente de Segurança", "Analista de Rede", "Administrador DB", "Operador Suporte", "Auditor Interno"],
        "Nível": ["Estratégico", "Tático", "Operacional", "Técnico", "Operacional", "Controle"],
        "Responsabilidades": ["Aprovações, Orçamento", "Políticas, Riscos", "Configuração rede", "Backup, Permissões", "Atendimento usuários", "Auditoria, Conformidade"],
        "Acessos Autorizados": ["Todos leitura", "SIEM, Firewall", "Roteadores, Switches", "Bancos dados", "Ferramentas suporte", "Logs, Relatórios"],
        "Need to Know": ["Informações estratégicas", "Dados de segurança", "Configurações rede", "Dados sensíveis", "Ticket usuários", "Evidências auditoria"],
        "Segregação Aplicada": ["Não executa tarefas técnicas", "Não acessa dados financeiros", "Não aprova políticas", "Não gerencia rede", "Não altera configurações", "Não opera sistemas"],
        "Aprovador": ["CEO", "Diretor", "Gerente", "Gerente", "Coordenador", "Diretoria"],
        "Data Revisão": ["2024-01-15", "2024-01-15", "2024-01-20", "2024-01-20", "2024-01-25", "2024-01-25"],
    })

# ──────────────────────────────────────────────
# ABAS COMPLETAS
# ──────────────────────────────────────────────
tab_dados, tab_graficos, tab_controles, tab_classificacao, tab_codigo, tab_ameacas, tab_segregacao, tab_pdca, tab_historico = st.tabs([
    "📋 Dados", "📊 Gráficos", "🔒 Controles", "🔐 Classificação", "📜 Código Conduta", "🕵️ Ameaças", "👥 Segregação", "🔄 PDCA", "📜 Histórico"
])

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
                edited_controles.to_excel(writer, sheet_name="Controles", index=False)
                edited_codigo.to_excel(writer, sheet_name="CodigoConduta", index=False)
                edited_classificacao.to_excel(writer, sheet_name="Classificacao", index=False)
                edited_ameacas.to_excel(writer, sheet_name="Ameacas", index=False)
                edited_segregacao.to_excel(writer, sheet_name="Segregacao", index=False)
            st.success("Excel exportado!")

# ══════════════════════════════════════════════
# TAB GRÁFICOS
# ══════════════════════════════════════════════
with tab_graficos:
    st.markdown("### 📊 Dashboard de Gráficos")
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(mcard(len(edited_risco), "Total Riscos", "c-blue"), unsafe_allow_html=True)
    with col2:
        alto = len(edited_risco[edited_risco["Nível do Risco"] == "🔴 Alto"])
        st.markdown(mcard(alto, "Riscos Altos", "c-red"), unsafe_allow_html=True)
    with col3:
        st.markdown(mcard(len(edited_controles[edited_controles["Status"] == "Implantado"]), "Controles Implantados", "c-green"), unsafe_allow_html=True)
    with col4:
        confidencial = len(edited_classificacao[edited_classificacao["Classificação"] == "Confidencial"])
        st.markdown(mcard(confidencial, "Info Confidencial", "c-purple"), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Gráficos de Classificação
    st.markdown("##### 🔐 Distribuição por Classificação da Informação")
    col_c1, col_c2 = st.columns(2)
    
    with col_c1:
        classificacao_counts = edited_classificacao["Classificação"].value_counts().to_dict()
        cores_class = {
            "Pública": "#16a34a",
            "Interna": "#2563eb", 
            "Restrita": "#d97706",
            "Confidencial": "#dc2626"
        }
        
        if classificacao_counts:
            total = sum(classificacao_counts.values())
            pie_data = ""
            for label, valor in classificacao_counts.items():
                pct = (valor / total) * 100
                cor = cores_class.get(label, "#94a3b8")
                pie_data += f"""
                <div style='display:flex; justify-content:space-between; margin-bottom:8px;'>
                    <span>{get_classificacao_badge(label)}</span>
                    <span><strong>{valor}</strong> ({pct:.0f}%)</span>
                </div>
                """
            st.markdown(f"""
            <div class='chart-card'>
                <div class='chart-title'>Classificação dos Ativos</div>
                {pie_data}
            </div>
            """, unsafe_allow_html=True)
    
    with col_c2:
        # Níveis de Sigilo
        sigilo_counts = edited_classificacao["Nível de Sigilo"].value_counts().to_dict()
        if sigilo_counts:
            sigilo_html = ""
            for nivel, count in sigilo_counts.items():
                cor = {"Máximo": "#dc2626", "Alto": "#ea580c", "Médio": "#d97706", "Baixo": "#16a34a"}.get(nivel, "#64748b")
                sigilo_html += f"""
                <div style='display:flex; justify-content:space-between; margin-bottom:8px;'>
                    <span style='color:{cor}; font-weight:600;'>🎯 {nivel}</span>
                    <span><strong>{count}</strong></span>
                </div>
                """
            st.markdown(f"""
            <div class='chart-card'>
                <div class='chart-title'>Nível de Sigilo</div>
                {sigilo_html}
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB CONTROLES DE SEGURANÇA
# ══════════════════════════════════════════════
with tab_controles:
    sec("🔒 Controles de Segurança")
    
    st.markdown("""
    <div style="background:#eef2ff; padding:12px 16px; border-radius:10px; margin-bottom:16px; border-left:4px solid #2563eb;">
        <span style="font-size:13px; color:#1e40af;">📌 Os controles de segurança são medidas ou ações para evitar, 
        combater ou minimizar a perda ou indisponibilidade de ativos de informação.</span>
    </div>
    """, unsafe_allow_html=True)
    
    edited_controles = st.data_editor(
        edited_controles, 
        use_container_width=True, 
        num_rows="dynamic",
        column_config={
            "Categoria": st.column_config.SelectboxColumn(
                options=["Acesso", "Malware", "Backup", "Rede", "Monitoramento", "Governança", "Data Loss", "SIEM", "Física", "Criptografia"]
            ),
            "Tipo de Controle": st.column_config.SelectboxColumn(
                options=["Preventivo", "Detectivo", "Corretivo", "Compensatório", "Deterrente"]
            ),
            "Status": st.column_config.SelectboxColumn(
                options=["Implantado", "Parcial", "Pendente", "Planejado", "Cancelado"]
            ),
        },
        hide_index=True,
    )
    
    col_sv1, col_sv2 = st.columns(2)
    with col_sv1:
        if st.button("💾 Salvar Controles", use_container_width=True):
            if supabase:
                if salvar_controles_supabase(supabase, edited_controles, st.session_state.usuario):
                    st.success("✅ Controles salvos!")
                else:
                    st.error("❌ Erro ao salvar")

# ══════════════════════════════════════════════
# TAB CLASSIFICAÇÃO DA INFORMAÇÃO (NOVA)
# ══════════════════════════════════════════════
with tab_classificacao:
    sec("🔐 Classificação da Informação")
    
    st.markdown("""
    <div style="background:#fef3c7; padding:12px 16px; border-radius:10px; margin-bottom:16px; border-left:4px solid #d97706;">
        <span style="font-size:13px; color:#92400e;">
        📌 A classificação da informação segue os níveis: 
        <strong>Pública</strong> (acesso livre), 
        <strong>Interna</strong> (uso interno), 
        <strong>Restrita</strong> (acesso limitado), 
        <strong>Confidencial</strong> (alto sigilo).
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Matriz de Classificação
    st.markdown("#### 📊 Matriz de Classificação")
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    
    with col_m1:
        st.markdown(f"""
        <div style="background:#dcfce7; padding:15px; border-radius:10px; text-align:center;">
            <div style="font-size:28px;">🌍</div>
            <div style="font-weight:700;">Pública</div>
            <div style="font-size:11px; color:#166534;">Acesso irrestrito</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_m2:
        st.markdown(f"""
        <div style="background:#dbeafe; padding:15px; border-radius:10px; text-align:center;">
            <div style="font-size:28px;">🏢</div>
            <div style="font-weight:700;">Interna</div>
            <div style="font-size:11px; color:#1e40af;">Uso interno apenas</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_m3:
        st.markdown(f"""
        <div style="background:#fed7aa; padding:15px; border-radius:10px; text-align:center;">
            <div style="font-size:28px;">🔒</div>
            <div style="font-weight:700;">Restrita</div>
            <div style="font-size:11px; color:#9a3412;">Acesso limitado</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_m4:
        st.markdown(f"""
        <div style="background:#fee2e2; padding:15px; border-radius:10px; text-align:center;">
            <div style="font-size:28px;">🔐</div>
            <div style="font-weight:700;">Confidencial</div>
            <div style="font-size:11px; color:#991b1b;">Alto sigilo</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tabela de Classificação
    edited_classificacao = st.data_editor(
        edited_classificacao,
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            "Classificação": st.column_config.SelectboxColumn(
                options=["Pública", "Interna", "Restrita", "Confidencial"]
            ),
            "Nível de Sigilo": st.column_config.SelectboxColumn(
                options=["Baixo", "Médio", "Alto", "Máximo"]
            ),
        },
        hide_index=True,
    )
    
    # Botão Salvar
    if st.button("💾 Salvar Classificação da Informação", use_container_width=True):
        if supabase:
            if salvar_classificacao_supabase(supabase, edited_classificacao, st.session_state.usuario):
                st.success("✅ Classificação salva!")
            else:
                st.error("❌ Erro ao salvar")
        else:
            st.error("❌ Supabase não conectado")

# ══════════════════════════════════════════════
# TAB CÓDIGO DE CONDUTA (NOVA)
# ══════════════════════════════════════════════
with tab_codigo:
    sec("📜 Código de Conduta")
    
    st.markdown("""
    <div style="background:#e0e7ff; padding:12px 16px; border-radius:10px; margin-bottom:16px; border-left:4px solid #4338ca;">
        <span style="font-size:13px; color:#3730a3;">
        📌 O Código de Conduta estabelece os princípios éticos e comportamentais que todos os colaboradores 
        devem seguir, garantindo integridade, confidencialidade e conformidade com as políticas da organização.
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Termo de Aceite
    with st.expander("📋 Termo de Compromisso - Clique para ler e assinar"):
        st.markdown("""
        ### DECLARAÇÃO DE COMPROMISSO COM O CÓDIGO DE CONDUTA
        
        Eu, _________________________________, portador do CPF: _________________, 
        declaro que li, compreendi e concordo em cumprir integralmente o Código de Conduta 
        da organização SecureOps.
        
        Estou ciente de que:
        - Devo agir com integridade e honestidade em todas as atividades profissionais
        - Devo proteger as informações confidenciais da organização
        - Devo cumprir todas as leis e regulamentos aplicáveis
        - Devo reportar qualquer violação às autoridades competentes
        - Estou sujeito a medidas disciplinares em caso de descumprimento
        
        **Data:** ___/___/______
        **Assinatura:** _________________________
        """)
        
        nome_colaborador = st.text_input("Nome do Colaborador")
        if st.button("📝 Assinar Termo"):
            if nome_colaborador:
                st.success(f"✅ Termo assinado por {nome_colaborador} em {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            else:
                st.warning("Digite seu nome para assinar")
    
    st.markdown("---")
    
    # Tabela do Código de Conduta
    edited_codigo = st.data_editor(
        edited_codigo,
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            "Categoria": st.column_config.SelectboxColumn(
                options=["Ética", "Segurança", "Legal", "Comportamental", "Gestão", "Governança", "Tecnologia"]
            ),
            "Status": st.column_config.SelectboxColumn(
                options=["Ativo", "Revisão", "Descontinuado"]
            ),
        },
        hide_index=True,
    )
    
    # Botão Salvar
    if st.button("💾 Salvar Código de Conduta", use_container_width=True):
        if supabase:
            if salvar_codigo_conduta_supabase(supabase, edited_codigo, st.session_state.usuario):
                st.success("✅ Código de Conduta salvo!")
            else:
                st.error("❌ Erro ao salvar")
        else:
            st.error("❌ Supabase não conectado")

# ══════════════════════════════════════════════
# TAB INTELIGÊNCIA DE AMEAÇAS
# ══════════════════════════════════════════════
with tab_ameacas:
    sec("🕵️ Inteligência de Ameaças")
    
    st.markdown("""
    <div style="background:#fce7f3; padding:12px 16px; border-radius:10px; margin-bottom:16px; border-left:4px solid #db2777;">
        <span style="font-size:13px; color:#9d174d;">
        📌 A inteligência de ameaças envolve a investigação proativa de novas vulnerabilidades, 
        técnicas de ataque e medidas de proteção, aumentando a resiliência da organização.
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Threat Intelligence Lifecycle
    st.markdown("#### 🔄 Threat Intelligence Lifecycle")
    st.markdown("""
    <div class='threat-cycle'>
        <div class='threat-stage'><div class='threat-stage-num'>1</div><div class='threat-stage-name'>Definir Objetivos</div></div>
        <div class='threat-stage'><div class='threat-stage-num'>2</div><div class='threat-stage-name'>Coletar Dados</div></div>
        <div class='threat-stage'><div class='threat-stage-num'>3</div><div class='threat-stage-name'>Processar Dados</div></div>
        <div class='threat-stage'><div class='threat-stage-num'>4</div><div class='threat-stage-name'>Analisar Dados</div></div>
        <div class='threat-stage'><div class='threat-stage-num'>5</div><div class='threat-stage-name'>Reportar</div></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tabela de Ameaças
    edited_ameacas = st.data_editor(
        edited_ameacas,
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            "Categoria": st.column_config.SelectboxColumn(
                options=["Malware", "Engenharia Social", "Disponibilidade", "Pessoal", "Vulnerabilidade", "Rede", "Física"]
            ),
            "Nível Criticidade": st.column_config.SelectboxColumn(
                options=["Crítico", "Alto", "Médio", "Baixo"]
            ),
            "Status": st.column_config.SelectboxColumn(
                options=["Monitorando", "Mitigado", "Investigando", "Controlado", "Crítico"]
            ),
        },
        hide_index=True,
    )
    
    col_sva1, col_sva2 = st.columns(2)
    with col_sva1:
        if st.button("💾 Salvar Inteligência de Ameaças", use_container_width=True):
            if supabase:
                if salvar_ameacas_supabase(supabase, edited_ameacas, st.session_state.usuario):
                    st.success("✅ Ameaças salvas!")
                else:
                    st.error("❌ Erro ao salvar")

# ══════════════════════════════════════════════
# TAB SEGREGAÇÃO DE FUNÇÕES
# ══════════════════════════════════════════════
with tab_segregacao:
    sec("👥 Segregação de Funções")
    
    st.markdown("""
    <div style="background:#e6f7e6; padding:12px 16px; border-radius:10px; margin-bottom:16px; border-left:4px solid #059669;">
        <span style="font-size:13px; color:#065f46;">
        📌 A segregação de funções evita conflitos de interesse e reduz o risco de ações não autorizadas, 
        garantindo que nenhum indivíduo tenha acesso ou controle excessivo sobre processos críticos.
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Pirâmide de Segregação
    st.markdown("#### 🏛️ Pirâmide de Segregação")
    st.markdown("""
    <div class='segregation-pyramid'>
        <div class='pyramid-level pyramid-director'>🎯 Diretor - Aprova Estratégias</div>
        <div class='pyramid-level pyramid-manager'>📋 Gerente - Define Políticas</div>
        <div class='pyramid-level pyramid-operator'>⚙️ Operador - Executa Tarefas</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tabela de Segregação
    edited_segregacao = st.data_editor(
        edited_segregacao,
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            "Nível": st.column_config.SelectboxColumn(
                options=["Estratégico", "Tático", "Operacional", "Técnico", "Controle"]
            ),
        },
        hide_index=True,
    )
    
    col_svs1, col_svs2 = st.columns(2)
    with col_svs1:
        if st.button("💾 Salvar Segregação de Funções", use_container_width=True):
            if supabase:
                if salvar_segregacao_supabase(supabase, edited_segregacao, st.session_state.usuario):
                    st.success("✅ Segregação salva!")
                else:
                    st.error("❌ Erro ao salvar")

# ══════════════════════════════════════════════
# TAB PDCA
# ══════════════════════════════════════════════
with tab_pdca:
    st.markdown("### 🔄 PDCA de Gestão de Segurança")

    fases = [
        {"nome": "1. Contexto",      "fase": "PLAN",  "cor": "#2563eb"},
        {"nome": "2. Liderança",     "fase": "PLAN",  "cor": "#2563eb"},
        {"nome": "3. Planejamento",  "fase": "PLAN",  "cor": "#2563eb"},
        {"nome": "4. Suporte",       "fase": "DO",    "cor": "#d97706"},
        {"nome": "5. Operação",      "fase": "DO",    "cor": "#d97706"},
        {"nome": "6. Avaliação",     "fase": "CHECK", "cor": "#16a34a"},
        {"nome": "7. Melhoria",      "fase": "ACT",   "cor": "#7c3aed"},
    ]

    linhas_pdca = [
        ("🎯", "Objetivo Estratégico"),
        ("⚙️", "Ação Técnica"),
        ("📊", "Indicador KPI"),
        ("🚩", "Evidência Status"),
    ]

    dados_pdca = {}
    if dados_pdca_carregado:
        st.info("📀 PDCA carregado do Supabase")
        dados_pdca = dados_pdca_carregado

    fase_cols = st.columns(7, gap="small")

    for i, (col, fase) in enumerate(zip(fase_cols, fases)):
        with col:
            st.markdown(f"""
            <div style='background:{fase["cor"]}15; border:2px solid {fase["cor"]}40;
                        border-radius:10px; padding:12px 6px; text-align:center;
                        margin-bottom:10px;'>
                <div style='font-size:11px; font-weight:800; color:{fase["cor"]};
                            letter-spacing:0.3px;'>{fase["nome"]}</div>
                <div style='font-size:9px; font-weight:600; color:#94a3b8;
                            margin-top:3px; text-transform:uppercase;
                            letter-spacing:1px;'>{fase["fase"]}</div>
            </div>
            """, unsafe_allow_html=True)

            for j, (icone, nome_linha) in enumerate(linhas_pdca):
                st.markdown(
                    f"<div style='font-size:10px; font-weight:600; color:#64748b; "
                    f"margin-bottom:2px;'>{icone} {nome_linha}</div>",
                    unsafe_allow_html=True
                )
                key = f"pdca_{i}_{j}"
                valor_padrao = dados_pdca.get((i, j), "")
                dados_pdca[(i, j)] = st.text_area(
                    label="",
                    key=key,
                    placeholder="Digite...",
                    label_visibility="collapsed",
                    height=90,
                    value=valor_padrao,
                )

    st.markdown("---")

    if st.button("💾 Salvar PDCA", use_container_width=True):
        if supabase:
            if salvar_pdca_supabase(supabase, dados_pdca, st.session_state.usuario):
                st.success("✅ PDCA salvo na nuvem!")
            else:
                st.error("❌ Erro ao salvar PDCA")
        else:
            st.error("❌ Supabase não conectado")

# ══════════════════════════════════════════════
# TAB HISTÓRICO
# ══════════════════════════════════════════════
with tab_historico:
    st.markdown("### 📜 Histórico de Alterações")
    tipo_filtro = st.selectbox("Filtrar:", ["Todos", "analise_risco", "equipamentos", "pdca", "controles", "codigo_conduta", "classificacao_informacao", "inteligencia_ameacas", "segregacao_funcoes"])
    if supabase:
        tipo_valor = None if tipo_filtro == "Todos" else tipo_filtro
        df_hist = carregar_historico_supabase(supabase, tipo_valor)
        if not df_hist.empty:
            st.dataframe(df_hist, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum registro no histórico")
    else:
        st.warning("Conecte ao Supabase para ver o histórico")

# ──────────────────────────────────────────────
# SIDEBAR — RESUMO ATUALIZADO
# ──────────────────────────────────────────────
with sidebar_ph:
    alto = len(edited_risco[edited_risco["Nível do Risco"] == "🔴 Alto"])
    medio = len(edited_risco[edited_risco["Nível do Risco"] == "🟡 Médio"])
    baixo = len(edited_risco[edited_risco["Nível do Risco"] == "🟢 Baixo"])
    controles_total = len(edited_controles)
    controles_implantados = len(edited_controles[edited_controles["Status"] == "Implantado"])
    confid
