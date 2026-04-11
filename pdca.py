import streamlit as st

# Configuração da página para largura total
st.set_page_config(layout="wide", page_title="PDCA Controle de Acesso")

st.title("🔄 PDCA de Controle de Acesso - Segurança Corporativa")
st.subheader("Governança e Melhoria Contínua dos Sistemas de Segurança (HID / LPR / CFTV)")
st.markdown("---")

# Criando as 7 colunas baseadas na imagem da ISO 27001
cols = st.columns(7)

# Títulos ajustados para o seu contexto de Controle de Acesso
titulos = [
    "1. Contexto (P)",
    "2. Liderança (P)",
    "3. Planejamento (P)",
    "4. Suporte (D)",
    "5. Operação (D)",
    "6. Avaliação (C)",
    "7. Melhoria (A)"
]

# Conteúdo técnico focado na Usina e nos Meios Eletrônicos
conteudos = [
    "**Escopo:** Definição das áreas críticas (Pimental, P7, Salas Técnicas) e perímetros monitorados.",
    "**Diretrizes:** Apoio da Superintendência para política de acesso e conformidade normativa.",
    "**Riscos:** Mapeamento de tentativas de invasão, falhas nos leitores HID e placas não lidas pela LPR.",
    "**Recursos:** Infraestrutura de fibra óptica, servidores de segurança e equipe técnica de campo.",
    "**Implementação:** Instalação física dos leitores, configuração das câmeras LPR e barreiras virtuais.",
    "**Monitoramento:** Análise de logs via Power BI e auditoria de acessos fora do horário permitido.",
    "**Ações:** Correção de falhas técnicas e revisão periódica das permissões de crachás inativos."
]

# Estilização visual para o tabuleiro
for i in range(7):
    with cols[i]:
        # Cores para identificar as fases: Plan (Azul), Do (Amarelo), Check (Verde), Act (Laranja)
        if i < 3: color = "#D6EAF8" # Azul claro (Plan)
        elif i < 5: color = "#FCF3CF" # Amarelo claro (Do)
        elif i == 5: color = "#D5F5E3" # Verde claro (Check)
        else: color = "#FADBD8" # Vermelho/Laranja claro (Act)
        
        st.markdown(f"""
            <div style="background-color: {color}; padding: 15px; border-radius: 8px; border: 2px solid #2E4053; min-height: 280px;">
                <h4 style="color: #1B2631; text-align: center; font-size: 16px;">{titulos[i]}</h4>
                <hr style="border: 0.5px solid #2E4053;">
                <p style="color: #2C3E50; font-size: 14px; line-height: 1.4;">{conteudos[i]}</p>
            </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.caption("Desenvolvido para Gestão de Segurança Corporativa - Norte Energia")
