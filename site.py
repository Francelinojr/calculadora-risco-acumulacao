import streamlit as st
from datetime import datetime
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Calculadora de Risco de Acumulação", page_icon="📋")

st.title("📋 Avaliação Multidimensional de Acumulação")
st.markdown("---")

# --- CONEXÃO COM GOOGLE SHEETS ---
gs_conn = st.connection("gsheets", type=GSheetsConnection)
WORKSHEET_NAME = "Avaliacoes_Acumulacao1"

# --- CATEGORIA: IDENTIFICAÇÃO ---
st.subheader("Identificação do Morador")
nome_morador = st.text_input("Nome do(a) morador(a):")
endereco = st.text_input("Endereço:")

# --- CATEGORIAS DE AVALIAÇÃO ---
st.header("🔹 Categoria 1 – CONDIÇÃO ESTRUTURAL")
cat1 = st.radio("Selecione a condição estrutural:", options=[0, 1, 2, 3, 4],
                format_func=lambda x: ["0 – Estrutura íntegra", "1 – Trincas leves", "2 – Infiltração moderada / 1 cômodo inseguro", "3 – Instalações elétricas expostas / risco de incêndio", "4 – Risco iminente de desabamento/incêndio"][x])

st.header("🔹 Categoria 2 – RISCO SANITÁRIO / HIGIÊNICO")
cat2 = st.radio("Selecione a condição sanitária:", options=[0, 1, 2, 3, 4],
                format_func=lambda x: ["0 – Ambiente limpo / desorganizado.", "1 – Lixo leve", "2 – Lixo moderado / ratos, baratas e etc., ocasionais", "3 – Lixo putrefato / fezes / odor forte. Vetores frequentes.", "4 – Infestação grave (ratos/baratas/escorpiões). Risco para vizinhos."][x])

st.header("🔹 Categoria 3 – ACÚMULO DE ANIMAIS")
cat3 = st.radio("Selecione a condição dos animais:", options=[0, 1, 2, 3, 4],
                format_func=lambda x: ["0 – Nenhum animal / quantidade adequada e cuidados presentes.", "1 – Leve desorganização e cuidados presentes.", "2 – Número acima do suportado higiene ruim e ausência de cuidados veterinários.", "3 – Maus-tratos evidentes, animais magros/doentes.", "4 – Acumulação severa (>15–20 animais / cadáveres / zoonoses)"][x])

st.header("🔹 Categoria 4 – USO DO ESPAÇO / OBSTRUÇÃO")
cat4 = st.radio("Selecione o nível de obstrução:", options=[0, 1, 2, 3, 4],
                format_func=lambda x: ["0 – Todos os cômodos funcionais", "1 – Bagunça leve", "2 – 1–2 cômodos inutilizados", "3 – Mais da metade da casa inacessível", "4 – Saídas bloqueadas"][x])

st.header("🔹 Categoria 5 – Vulnerabilidade Psicossocial")
cat5 = st.radio("Selecione a vulnerabilidade:", options=[0, 1, 2, 3, 4],
                format_func=lambda x: ["0 – Autonomia preservada", "1 – Isolamento leve", "2 – Sem rede de apoio", "3 – Autoabandono", "4 – Incapacidade grave de autocuidado, agressividade, surto e etc."][x])

# --- CÁLCULO FINAL ---
total_pontos = cat1 + cat2 + cat3 + cat4 + cat5
tem_item_4 = any([cat1==4, cat2==4, cat3==4, cat4==4, cat5==4])

if total_pontos >= 21 or tem_item_4:
    status, cor, intervencao = "🔴 RISCO GRAVE (NÍVEL 4)", "red", "Acompanhamento multiprofissional intensivo e contínuo. Prioridade assistencial. Articulação com Defesa Civil e EMLURB."
elif 13 <= total_pontos <= 20:
    status, cor, intervencao = "🟠 RISCO ALTO (NÍVEL 3)", "orange", "Acompanhamento intensivo pela eSF, eMulti e CAPS. Visitas mensais por ACS/ASACE."
elif 8 <= total_pontos <= 12:
    status, cor, intervencao = "🟡 RISCO MODERADO (NÍVEL 2)", "yellow", "Elaboração de PTS (Projeto Terapêutico Singular). Visitas bimestrais e articulação intersetorial."
else:
    status, cor, intervencao = "🟢 RISCO BAIXO (NÍVEL 1)", "green", "Monitoramento periódico. Visitas domiciliares trimestrais. Apoio matricial."

st.markdown("---")
st.subheader(f"Pontuação Total: {total_pontos}")
st.markdown(f"### Classificação Final: :{cor}[{status}]")
st.info(f"**Intervenção Recomendada:** {intervencao}")

# --- FUNÇÃO PARA SALVAR ---
def salvar_dados():
    row = {
        "timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "nome_morador": [nome_morador],
        "endereco": [endereco],
        "cat1_estrutural": [int(cat1)],
        "cat2_sanitario": [int(cat2)],
        "cat3_animais": [int(cat3)],
        "cat4_obstrucao": [int(cat4)],
        "cat5_psicossocial": [int(cat5)],
        "total_pontos": [int(total_pontos)],
        "status_risco": [status],
        "intervencao": [intervencao]
    }
    try:
        df_existing = gs_conn.read(worksheet=WORKSHEET_NAME, ttl=0)
        df_new = pd.DataFrame(row)
        df_final = pd.concat([df_existing, df_new], ignore_index=True)
        gs_conn.update(worksheet=WORKSHEET_NAME, data=df_final)
        st.success("Dados salvos com sucesso no Google Sheets!")
    except Exception as e:
        st.error(f"Erro ao salvar: {e}")

if st.button("Salvar Avaliação"):
    if nome_morador:
        salvar_dados()
    else:
        st.warning("Preencha o nome do morador para salvar.")