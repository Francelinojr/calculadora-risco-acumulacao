import streamlit as st
from datetime import datetime
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# =====================================================
# CONFIGURAÇÃO
# =====================================================
st.set_page_config(
    page_title="Calculadora de Risco de Acumulação",
    page_icon="📋",
    layout="centered"
)

# =====================================================
# ESTILO
# =====================================================
st.markdown("""
    <style>
    .cat-header {
        padding: 10px;
        border-left: 10px solid #1E3A8A;
        background-color: #f0f2f6;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    div.stButton > button {
        width: 100%;
        height: 3.5em;
        font-size: 22px !important;
        font-weight: bold !important;
        background-color: #007bff !important;
        color: white !important;
        border-radius: 12px;
        border: none;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# =====================================================
# GOOGLE SHEETS
# =====================================================
gs_conn = st.connection("gsheets", type=GSheetsConnection)
WORKSHEET_NAME = "Avaliacoes_Acumulacao1"

@st.cache_data(ttl=300)
def carregar_dados():
    try:
        return gs_conn.read(worksheet=WORKSHEET_NAME)
    except:
        return pd.DataFrame()

# =====================================================
# CATEGORIAS
# =====================================================
CATEGORIAS = {
    "estrutural": {
        "titulo": "🔹 CONDIÇÃO ESTRUTURAL",
        "descricao": [
            "0 – Estrutura íntegra",
            "1 – Trincas leves",
            "2 – Infiltração moderada",
            "3 – Risco elétrico",
            "4 – Risco iminente"
        ]
    },
    "sanitario": {
        "titulo": "🔹 RISCO SANITÁRIO / HIGIÊNICO",
        "descricao": [
            "0 – Ambiente limpo",
            "1 – Lixo leve",
            "2 – Lixo moderado",
            "3 – Lixo putrefato",
            "4 – Infestação grave"
        ]
    },
    "animais": {
        "titulo": "🔹 ACÚMULO DE ANIMAIS",
        "descricao": [
            "0 – Quantidade adequada",
            "1 – Leve desorganização",
            "2 – Número acima do suportado",
            "3 – Maus-tratos",
            "4 – Acumulação severa"
        ]
    },
    "obstrucao": {
        "titulo": "🔹 USO DO ESPAÇO / OBSTRUÇÃO",
        "descricao": [
            "0 – Todos funcionais",
            "1 – Bagunça leve",
            "2 – 1–2 cômodos inutilizados",
            "3 – Casa inacessível",
            "4 – Saídas bloqueadas"
        ]
    },
    "psicossocial": {
        "titulo": "🔹 VULNERABILIDADE PSICOSSOCIAL",
        "descricao": [
            "0 – Autonomia preservada",
            "1 – Isolamento leve",
            "2 – Sem rede de apoio",
            "3 – Autoabandono",
            "4 – Incapacidade grave"
        ]
    }
}

# =====================================================
# FUNÇÕES
# =====================================================
def classificar_risco(total, tem_critico):
    if total >= 21 or tem_critico:
        return "🔴 RISCO GRAVE (NÍVEL 4)", "red", "Acompanhamento intensivo."
    elif 13 <= total <= 20:
        return "🟠 RISCO ALTO (NÍVEL 3)", "orange", "Visitas mensais."
    elif 8 <= total <= 12:
        return "🟡 RISCO MODERADO (NÍVEL 2)", "yellow", "Visitas bimestrais."
    return "🟢 RISCO BAIXO (NÍVEL 1)", "green", "Monitoramento trimestral."

def salvar_avaliacao(dados):
    df_existente = carregar_dados()
    df_final = pd.concat([df_existente, pd.DataFrame([dados])], ignore_index=True)
    gs_conn.update(worksheet=WORKSHEET_NAME, data=df_final)
    st.cache_data.clear()

# =====================================================
# INTERFACE
# =====================================================
st.title("📋 FORMULÁRIO DE AVALIAÇÃO DE RISCO")
st.markdown("---")

with st.form("form_avaliacao", clear_on_submit=True):

    st.subheader("Identificação do Morador")
    nome = st.text_input("Nome do(a) morador(a):")
    endereco = st.text_input("Endereço:")

    st.markdown("---")

    respostas = {}
    for key, config in CATEGORIAS.items():
        st.markdown(
            f'<div class="cat-header"><b>{config["titulo"]}</b></div>',
            unsafe_allow_html=True
        )

        respostas[key] = st.radio(
            "Selecione uma opção:",
            options=range(5),
            format_func=lambda x, desc=config["descricao"]: desc[x]
        )

    total_pontos = sum(respostas.values())
    tem_item_4 = any(v == 4 for v in respostas.values())
    status, cor, intervencao = classificar_risco(total_pontos, tem_item_4)

    st.markdown("---")
    st.subheader(f"Pontuação Total: {total_pontos}")
    st.markdown(f"### Classificação Final: :{cor}[{status}]")
    st.info(f"Intervenção Recomendada: {intervencao}")

    submitted = st.form_submit_button("SALVAR AVALIAÇÃO")

    if submitted:
        if nome.strip():
            with st.spinner("Salvando..."):
                dados = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "nome_morador": nome,
                    "endereco": endereco,
                    **respostas,
                    "total_pontos": total_pontos,
                    "status_risco": status,
                    "intervencao": intervencao
                }

                salvar_avaliacao(dados)
                st.success("✅ Avaliação salva com sucesso!")
        else:
            st.warning("⚠️ Preencha o nome antes de salvar.")
