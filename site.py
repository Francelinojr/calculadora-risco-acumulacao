import streamlit as st
from datetime import datetime
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Calculadora de Risco de Acumulação", page_icon="📋")
st.title("📋 FORMULÁRIO DE AVALIAÇÃO DE RISCO")
st.markdown("---")

# ------------------ CONEXÃO ------------------
gs_conn = st.connection("gsheets", type=GSheetsConnection)
WORKSHEET_NAME = "Avaliacoes_Acumulacao1"

# ------------------ IDENTIFICAÇÃO ------------------
st.subheader("Identificação do Morador")
nome_morador = st.text_input("Nome do(a) morador(a):")
endereco = st.text_input("Endereço:")

# ------------------ CONFIGURAÇÃO DAS CATEGORIAS ------------------
CATEGORIAS = {
    "cat1_estrutural": {
        "titulo": "🔹 Categoria 1 – CONDIÇÃO ESTRUTURAL",
        "descricao": [
            "0 – Estrutura íntegra",
            "1 – Trincas leves",
            "2 – Infiltração moderada / 1 cômodo inseguro",
            "3 – Instalações elétricas expostas / risco de incêndio",
            "4 – Risco iminente de desabamento/incêndio"
        ]
    },
    "cat2_sanitario": {
        "titulo": "🔹 Categoria 2 – RISCO SANITÁRIO / HIGIÊNICO",
        "descricao": [
            "0 – Ambiente limpo / desorganizado",
            "1 – Lixo leve",
            "2 – Lixo moderado / vetores ocasionais",
            "3 – Lixo putrefato / odor forte / vetores frequentes",
            "4 – Infestação grave"
        ]
    },
    "cat3_animais": {
        "titulo": "🔹 Categoria 3 – ACÚMULO DE ANIMAIS",
        "descricao": [
            "0 – Quantidade adequada",
            "1 – Leve desorganização",
            "2 – Número acima do suportado",
            "3 – Maus-tratos evidentes",
            "4 – Acumulação severa"
        ]
    },
    "cat4_obstrucao": {
        "titulo": "🔹 Categoria 4 – USO DO ESPAÇO / OBSTRUÇÃO",
        "descricao": [
            "0 – Todos os cômodos funcionais",
            "1 – Bagunça leve",
            "2 – 1–2 cômodos inutilizados",
            "3 – Casa majoritariamente inacessível",
            "4 – Saídas bloqueadas"
        ]
    },
    "cat5_psicossocial": {
        "titulo": "🔹 Categoria 5 – Vulnerabilidade Psicossocial",
        "descricao": [
            "0 – Autonomia preservada",
            "1 – Isolamento leve",
            "2 – Sem rede de apoio",
            "3 – Autoabandono",
            "4 – Incapacidade grave"
        ]
    }
}

def render_categoria(key, config):
    st.header(config["titulo"])
    return st.radio(
        "Selecione:",
        options=list(range(5)),
        format_func=lambda x: config["descricao"][x],
        key=key
    )

# ------------------ RENDERIZAÇÃO DINÂMICA ------------------
respostas = {}
for key, config in CATEGORIAS.items():
    respostas[key] = render_categoria(key, config)

# ------------------ CÁLCULO ------------------
total_pontos = sum(respostas.values())
tem_item_4 = any(valor == 4 for valor in respostas.values())

def classificar_risco(total, tem_critico):
    if total >= 21 or tem_critico:
        return (
            "🔴 RISCO GRAVE (NÍVEL 4)",
            "red",
            "Acompanhamento multiprofissional intensivo e contínuo."
        )
    elif 13 <= total <= 20:
        return (
            "🟠 RISCO ALTO (NÍVEL 3)",
            "orange",
            "Acompanhamento intensivo e visitas mensais."
        )
    elif 8 <= total <= 12:
        return (
            "🟡 RISCO MODERADO (NÍVEL 2)",
            "yellow",
            "Elaboração de PTS e visitas bimestrais."
        )
    else:
        return (
            "🟢 RISCO BAIXO (NÍVEL 1)",
            "green",
            "Monitoramento periódico e visitas trimestrais."
        )

status, cor, intervencao = classificar_risco(total_pontos, tem_item_4)

st.markdown("---")
st.subheader(f"Pontuação Total: {total_pontos}")
st.markdown(f"### Classificação Final: :{cor}[{status}]")
st.info(f"Intervenção Recomendada: {intervencao}")

# ------------------ SALVAR ------------------
def salvar_dados():
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
        df_existing = gs_conn.read(worksheet=WORKSHEET_NAME, ttl=0)
        df_final = pd.concat([df_existing, pd.DataFrame([row])], ignore_index=True)
        gs_conn.update(worksheet=WORKSHEET_NAME, data=df_final)
        st.success("Dados salvos com sucesso!")
    except Exception as e:
        st.error(f"Erro ao salvar: {e}")

if st.button("Salvar Avaliação"):
    if nome_morador.strip():
        salvar_dados()
    else:
        st.warning("Preencha o nome do morador para salvar.")
