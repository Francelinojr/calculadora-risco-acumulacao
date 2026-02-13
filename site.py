import streamlit as st 
from datetime import datetime
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# 1. Configuração da Página
st.set_page_config(page_title="Calculadora de Risco de Acumulação", page_icon="📋", layout="centered")

# 2. Estilização para Acessibilidade e Cores nas Categorias
st.markdown(
    """
    <style>
    .cat-header {
        padding: 10px;
        border-left: 10px solid #1E3A8A;
        background-color: #f0f2f6;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    h2 { font-size: 28px !important; color: #1E3A8A !important; margin-bottom: 0px; }
    div[data-testid="stWidgetLabel"] p { font-size: 22px !important; font-weight: bold !important; }
    div[data-testid="stMarkdownContainer"] p { font-size: 20px !important; line-height: 1.6 !important; }
    [data-testid="stSelectionControlValue"] { transform: scale(1.5); margin-right: 10px; }
    div.stButton > button {
        width: 100%;
        height: 3.5em;
        font-size: 24px !important;
        font-weight: bold !important;
        background-color: #007bff !important;
        color: white !important;
        border-radius: 12px;
        border: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📋 FORMULÁRIO DE AVALIAÇÃO DE RISCO")
st.markdown("---")

# ------------------ CONEXÃO ------------------
gs_conn = st.connection("gsheets", type=GSheetsConnection)
WORKSHEET_NAME = "Avaliacoes_Acumulacao1"

# ------------------ CATEGORIAS ------------------
CATEGORIAS = {
    "cat1_estrutural": {
        "titulo": "🔹 CONDIÇÃO ESTRUTURAL",
        "descricao": ["0 – Estrutura íntegra", "1 – Trincas leves", "2 – Infiltração moderada / 1 cômodo inseguro", "3 – Instalações elétricas expostas / risco de incêndio", "4 – Risco iminente de desabamento/incêndio"]
    },
    "cat2_sanitario": {
        "titulo": "🔹 RISCO SANITÁRIO / HIGIÊNICO",
        "descricao": ["0 – Ambiente limpo / desorganizado", "1 – Lixo leve", "2 – Lixo moderado / vetores ocasionais", "3 – Lixo putrefato / odor forte / vetores frequentes", "4 – Infestação grave"]
    },
    "cat3_animais": {
        "titulo": "🔹 ACÚMULO DE ANIMAIS",
        "descricao": ["0 – Quantidade adequada", "1 – Leve desorganização", "2 – Número acima do suportado", "3 – Maus-tratos evidentes", "4 – Acumulação severa"]
    },
    "cat4_obstrucao": {
        "titulo": "🔹 USO DO ESPAÇO / OBSTRUÇÃO",
        "descricao": ["0 – Todos os cômodos funcionais", "1 – Bagunça leve", "2 – 1–2 cômodos inutilizados", "3 – Casa majoritariamente inacessível", "4 – Saídas bloqueadas"]
    },
    "cat5_psicossocial": {
        "titulo": "🔹 VULNERABILIDADE PSICOSSOCIAL",
        "descricao": ["0 – Autonomia preservada", "1 – Isolamento leve", "2 – Sem rede de apoio", "3 – Autoabandono", "4 – Incapacidade grave"]
    }
}

# ------------------ FORMULÁRIO ------------------
with st.form("avaliacao_form", clear_on_submit=True):
    st.subheader("Identificação do Morador")
    nome_morador = st.text_input("Nome do(a) morador(a):")
    endereco = st.text_input("Endereço:")
    
    st.markdown("---")
    
    respostas = {}
    for key, config in CATEGORIAS.items():
        st.markdown(f'<div class="cat-header"><h2>{config["titulo"]}</h2></div>', unsafe_allow_html=True)
        respostas[key] = st.radio(
            "Selecione uma opção:",
            options=list(range(5)),
            format_func=lambda x: config["descricao"][x],
            key=f"radio_{key}"
        )
        st.markdown("<br>", unsafe_allow_html=True)

    submit_button = st.form_submit_button("SALVAR AVALIAÇÃO")

# ------------------ LÓGICA DE EXIBIÇÃO E SALVAMENTO ------------------
if submit_button:
    if nome_morador.strip():
        with st.spinner("🚀 Salvando e calculando..."):
            # Cálculos de Risco
            total_pontos = sum(respostas.values())
            tem_item_4 = any(valor == 4 for valor in respostas.values())

            def classificar_risco(total, tem_critico):
                if total >= 21 or tem_critico:
                    return ("🔴 RISCO GRAVE (NÍVEL 4)", "red", "Acompanhamento multiprofissional intensivo e contínuo.")
                elif 13 <= total <= 20:
                    return ("🟠 RISCO ALTO (NÍVEL 3)", "orange", "Acompanhamento intensivo e visitas mensais.")
                elif 8 <= total <= 12:
                    return ("🟡 RISCO MODERADO (NÍVEL 2)", "yellow", "Elaboração de PTS e visitas bimestrais.")
                else:
                    return ("🟢 RISCO BAIXO (NÍVEL 1)", "green", "Monitoramento periódico e visitas trimestrais.")

            status, cor, intervencao = classificar_risco(total_pontos, tem_item_4)

            # Preparação dos dados para o Google Sheets
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
                # Salva no Google Sheets
                df_existing = gs_conn.read(worksheet=WORKSHEET_NAME)
                df_final = pd.concat([df_existing, pd.DataFrame([row])], ignore_index=True)
                gs_conn.update(worksheet=WORKSHEET_NAME, data=df_final)
                st.cache_data.clear()
                
                # MANTÉM OS DADOS NA TELA IGUAL À SUA IMAGEM
                st.success(f"✅ Dados de {nome_morador} registrados!")
                st.markdown("---")
                st.markdown(f"## Pontuação Total: {total_pontos}")
                st.markdown(f"## Classificação Final: {status}")
                st.info(f"Intervenção Recomendada: {intervencao}")
                
            except Exception as e:
                st.error(f"❌ Erro ao salvar: {e}")
    else:
        st.warning("⚠️ Preencha o nome para calcular e salvar.")