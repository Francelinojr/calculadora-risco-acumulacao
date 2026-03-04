import streamlit as st
from datetime import datetime
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# =====================================================
# CONFIGURAÇÃO DA PÁGINA
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
    h2 { font-size: 26px !important; color: #1E3A8A !important; }
    div[data-testid="stWidgetLabel"] p {
        font-size: 20px !important;
        font-weight: bold !important;
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
# CONEXÃO GOOGLE SHEETS
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
        "titulo": "🔹 RISCO ESTRUTURAL",
        "descricao": [
            "0 – Estrutura íntegra",
            "1 – Trincas leves",
            "2 – Infiltração moderada/ 1 cômodo inseguro",
            "3 – Instalações elétricas expostas/ risco de incêndio",
            "4 – Risco iminente de desabamento/ incêndio"
        ]
    },
    "sanitario": {
        "titulo": "🔹 RISCO SANITÁRIO / HIGIÊNICO",
        "descricao": [
            "0 – Ambiente limpo/ desorganizado",
            "1 – Lixo leve",
            "2 – Lixo moderado/ ratos, baratas e etc., ocasionais",
            "3 – Lixo putrefato/ fezes/ odor forte. Vetores frequentes.",
            "4 – Infestação grave (ratos/baratas/escorpiões). Risco para vizinhos."
        ]
    },
    "animais": {
        "titulo": "🔹 ACÚMULO DE ANIMAIS",
        "descricao": [
            "0 – Nenhum animal/ quantidade adequada e cuidados presentes.",
            "1 – Leve desorganização e cuidados presentes.",
            "2 – Número acima do suportado higiene ruim e ausência de cuidados veterinários.",
            "3 – Maus-tratos evidentes, animais magros/doentes.",
            "4 – Acumulação severa(>15-20 animais / cadáveres / zoonoses)"
        ]
    },
    "obstrucao": {
        "titulo": "🔹 USO DO ESPAÇO / OBSTRUÇÃO",
        "descricao": [
            "0 – Todos os cômodosfuncionais",
            "1 – Bagunça leve",
            "2 – 1–2 cômodos inutilizados",
            "3 – Mais da metade da casa inacessível",
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
            "4 – Incapacidade grave de autocuidado, agressividade, surto e etc."
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
        return "🟡 RISCO ALTO (NÍVEL 3)", "yellow", "Visitas mensais."
    elif 8 <= total <= 12:
        return "🟢 RISCO MODERADO (NÍVEL 2)", "green", "Visitas bimestrais."
    return "🟠 RISCO BAIXO (NÍVEL 1)", "orange", "Monitoramento trimestral."


def salvar_avaliacao(nome, endereco, respostas, total, status, intervencao):
    row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nome_morador": nome,
        "endereco": endereco,
        **respostas,
        "total_pontos": total,
        "status_risco": status,
        "intervencao": intervencao
    }

    df_existente = carregar_dados()
    df_final = pd.concat([df_existente, pd.DataFrame([row])], ignore_index=True)
    gs_conn.update(worksheet=WORKSHEET_NAME, data=df_final)
    st.cache_data.clear()


def resetar_campos():
    for key in list(st.session_state.keys()):
        if key.startswith("r_") or key in ["nome", "end"]:
            del st.session_state[key]

# =====================================================
# INTERFACE
# =====================================================
st.title(" FORMULÁRIO DE AVALIAÇÃO DE RISCO")
st.markdown("---")

# Identificação
st.subheader("Identificação")
nome = st.text_input("Nome do usuário:", key="nome")
endereco = st.text_input("Endereço:", key="end")

st.markdown("---")

# Perguntas
respostas = {}
for key, config in CATEGORIAS.items():
    st.markdown(
        f'<div class="cat-header"><h2>{config["titulo"]}</h2></div>',
        unsafe_allow_html=True
    )

    respostas[key] = st.radio(
        "Selecione uma opção:",
        options=range(5),
        format_func=lambda x, desc=config["descricao"]: desc[x],
        key=f"r_{key}"
    )

# Cálculo
total_pontos = sum(respostas.values())
tem_item_4 = any(v == 4 for v in respostas.values())

status, cor, intervencao = classificar_risco(total_pontos, tem_item_4)

# Resultado
st.markdown("---")
st.subheader(f"Pontuação Total: {total_pontos}")
st.markdown(f"### Classificação Final: :{cor}[{status}]")
st.info(f"Intervenção Recomendada: {intervencao}")

# =====================================================
# BOTÃO SALVAR
# =====================================================
if st.button("SALVAR AVALIAÇÃO"):
    if nome.strip():
        with st.spinner("Salvando..."):
            try:
                salvar_avaliacao(
                    nome,
                    endereco,
                    respostas,
                    total_pontos,
                    status,
                    intervencao
                )
                resetar_campos()
                st.success("✅ Avaliação salva com sucesso!")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao salvar: {e}")
    else:
        st.warning("⚠️ Preencha o nome antes de salvar.")

