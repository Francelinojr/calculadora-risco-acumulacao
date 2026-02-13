import streamlit as st 
from datetime import datetime
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# 1. Configuração da Página
st.set_page_config(page_title="Calculadora de Risco de Acumulação", page_icon="📋", layout="centered")

# 2. Estilização para Acessibilidade e Estética
st.markdown(
    """
    <style>
    h2 { font-size: 28px !important; color: #1E3A8A !important; padding-top: 20px; }
    div[data-testid="stWidgetLabel"] p { font-size: 22px !important; font-weight: bold !important; }
    div[data-testid="stMarkdownContainer"] p { font-size: 20px !important; line-height: 1.6 !important; }
    [data-testid="stSelectionControlValue"] { transform: scale(1.5); margin-right: 10px; }
    
    /* Botão Salvar mais robusto */
    div.stButton > button:first-child {
        width: 100%;
        height: 3.5em;
        font-size: 24px !important;
        font-weight: bold !important;
        background-color: #007bff !important;
        color: white !important;
        border-radius: 12px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }
    input { font-size: 20px !important; }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📋 FORMULÁRIO DE AVALIAÇÃO DE RISCO")
st.info("Preencha todos os campos abaixo e clique em SALVAR no final da página.")

# ------------------ CONEXÃO ------------------
gs_conn = st.connection("gsheets", type=GSheetsConnection)
WORKSHEET_NAME = "Avaliacoes_Acumulacao1"

@st.cache_data(ttl=120)
def carregar_dados():
    return gs_conn.read(worksheet=WORKSHEET_NAME)

# ------------------ FORMULÁRIO ------------------
# Usar um formulário do Streamlit ajuda a organizar o envio
with st.form("meu_formulario", clear_on_submit=True):
    st.subheader("📍 Identificação do Morador")
    nome_morador = st.text_input("Nome do(a) morador(a):")
    endereco = st.text_input("Endereço:")
    
    st.markdown("---")

    CATEGORIAS = {
        "cat1_estrutural": {
            "titulo": "🔹 Categoria 1 – CONDIÇÃO ESTRUTURAL",
            "descricao": ["0 – Estrutura íntegra", "1 – Trincas leves", "2 – Infiltração moderada / 1 cômodo inseguro", "3 – Instalações elétricas expostas / risco de incêndio", "4 – Risco iminente de desabamento/incêndio"]
        },
        "cat2_sanitario": {
            "titulo": "🔹 Categoria 2 – RISCO SANITÁRIO / HIGIÊNICO",
            "descricao": ["0 – Ambiente limpo / desorganizado", "1 – Lixo leve", "2 – Lixo moderado / vetores ocasionais", "3 – Lixo putrefato / odor forte / vetores frequentes", "4 – Infestação grave"]
        },
        "cat3_animais": {
            "titulo": "🔹 Categoria 3 – ACÚMULO DE ANIMAIS",
            "descricao": ["0 – Quantidade adequada", "1 – Leve desorganização", "2 – Número acima do suportado", "3 – Maus-tratos evidentes", "4 – Acumulação severa"]
        },
        "cat4_obstrucao": {
            "titulo": "🔹 Categoria 4 – USO DO ESPAÇO / OBSTRUÇÃO",
            "descricao": ["0 – Todos os cômodos funcionais", "1 – Bagunça leve", "2 – 1–2 cômodos inutilizados", "3 – Casa majoritariamente inacessível", "4 – Saídas bloqueadas"]
        },
        "cat5_psicossocial": {
            "titulo": "🔹 Categoria 5 – Vulnerabilidade Psicossocial",
            "descricao": ["0 – Autonomia preservada", "1 – Isolamento leve", "2 – Sem rede de apoio", "3 – Autoabandono", "4 – Incapacidade grave"]
        }
    }

    respostas = {}
    for key, config in CATEGORIAS.items():
        st.header(config["titulo"])
        respostas[key] = st.radio("Selecione:", options=list(range(5)), format_func=lambda x: config["descricao"][x], key=key)
        st.markdown(" ")

    submit_button = st.form_submit_button("SALVAR AVALIAÇÃO")

# ------------------ LÓGICA APÓS CLIQUE ------------------
if submit_button:
    if not nome_morador.strip():
        st.error("⚠️ ERRO: O Nome do Morador é obrigatório!")
    else:
        with st.spinner("Salvando dados na planilha... aguarde."):
            # Cálculos
            total_pontos = sum(respostas.values())
            tem_item_4 = any(valor == 4 for valor in respostas.values())
            
            if total_pontos >= 21 or tem_item_4:
                status, cor, intervencao = ("🔴 RISCO GRAVE (NÍVEL 4)", "red", "Acompanhamento multiprofissional intensivo.")
            elif 13 <= total_pontos <= 20:
                status, cor, intervencao = ("🟠 RISCO ALTO (NÍVEL 3)", "orange", "Acompanhamento intensivo e visitas mensais.")
            elif 8 <= total_pontos <= 12:
                status, cor, intervencao = ("🟡 RISCO MODERADO (NÍVEL 2)", "yellow", "Elaboração de PTS e visitas bimestrais.")
            else:
                status, cor, intervencao = ("🟢 RISCO BAIXO (NÍVEL 1)", "green", "Monitoramento periódico.")

            # Preparar Linha
            row = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "nome_morador": nome_morador,
                "endereco": endereco,
                **respostas,
                "total_pontos": total_pontos,
                "status_risco": status,
                "intervencao": intervencao
            }

            try:
                df_existing = gs_conn.read(worksheet=WORKSHEET_NAME)
                df_final = pd.concat([df_existing, pd.DataFrame([row])], ignore_index=True)
                gs_conn.update(worksheet=WORKSHEET_NAME, data=df_final)
                
                st.balloons() # Efeito visual de sucesso
                st.success(f"✅ AVALIAÇÃO SALVA COM SUCESSO!\n\nResultado: {status}")
                st.info(f"Recomendação: {intervencao}")
                
            except Exception as e:
                st.error(f"❌ Erro ao salvar: {e}")