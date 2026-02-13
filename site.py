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

# --- CATEGORIA 1: ESTRUTURAL ---
st.header("🔹 Categoria 1 – CONDIÇÃO ESTRUTURAL")
cat1 = st.radio("Selecione a condição estrutural:", 
                options=[0, 1, 2, 3, 4],
                format_func=lambda x: [
                    "0 – Estrutura íntegra",
                    "1 – Trincas leves",
                    "2 – Infiltração moderada / 1 cômodo inseguro",
                    "3 – Instalações elétricas expostas / risco de incêndio",
                    "4 – Risco iminente de desabamento/incêndio"
                ][x])

# --- CATEGORIA 2: RISCO SANITÁRIO ---
st.header("🔹 Categoria 2 – RISCO SANITÁRIO / HIGIÊNICO")
cat2 = st.radio("Selecione a condição sanitária:",
                options=[0, 1, 2, 3, 4],
                format_func=lambda x: [
                    "0 – Ambiente limpo / desorganizado.",
                    "1 – Lixo leve",
                    "2 – Lixo moderado / ratos, baratas e etc., ocasionais",
                    "3 – Lixo putrefato / fezes / odor forte. Vetores frequentes.",
                    "4 – Infestação grave (ratos/baratas/escorpiões). Risco para vizinhos."
                ][x])

# --- CATEGORIA 3: ACÚMULO DE ANIMAIS ---
st.header("🔹 Categoria 3 – ACÚMULO DE ANIMAIS")
cat3 = st.radio("Selecione a condição dos animais:",
                options=[0, 1, 2, 3, 4],
                format_func=lambda x: [
                    "0 – Nenhum animal / quantidade adequada e cuidados presentes.",
                    "1 – Leve desorganização e cuidados presentes.",
                    "2 – Número acima do suportado higiene ruim e ausência de cuidados veterinários.",
                    "3 – Maus-tratos evidentes, animais magros/doentes.",
                    "4 – Acumulação severa (>15–20 animais / cadáveres / zoonoses)"
                ][x])

# --- CATEGORIA 4: USO DO ESPAÇO ---
st.header("🔹 Categoria 4 – USO DO ESPAÇO / OBSTRUÇÃO")
cat4 = st.radio("Selecione o nível de obstrução:",
                options=[0, 1, 2, 3, 4],
                format_func=lambda x: [
                    "0 – Todos os cômodos funcionais",
                    "1 – Bagunça leve",
                    "2 – 1–2 cômodos inutilizados",
                    "3 – Mais da metade da casa inacessível",
                    "4 – Saídas bloqueadas"
                ][x])

# --- CATEGORIA 5: VULNERABILIDADE PSICOSSOCIAL ---
st.header("🔹 Categoria 5 – Vulnerabilidade Psicossocial")
cat5 = st.radio("Selecione a vulnerabilidade:",
                options=[0, 1, 2, 3, 4],
                format_func=lambda x: [
                    "0 – Autonomia preservada",
                    "1 – Isolamento leve",
                    "2 – Sem rede de apoio",
                    "3 – Autoabandono",
                    "4 – Incapacidade grave de autocuidado, agressividade, surto e etc."
                ][x])

# --- CÁLCULO FINAL ---
total_pontos = cat1 + cat2 + cat3 + cat4 + cat5
tem_item_4 = any([cat1==4, cat2==4, cat3==4, cat4==4, cat5==4])

if total_pontos >= 21 or tem_item_4:
    status = "🔴 RISCO GRAVE (NÍVEL 4)"
    cor = "red"
    intervencao = "Acompanhamento multiprofissional intensivo e contínuo. Prioridade assistencial. Articulação com Defesa Civil e EMLURB."
elif 13 <= total_pontos <= 20:
    status = "🟠 RISCO ALTO (NÍVEL 3)"
    cor = "orange"
    intervencao = "Acompanhamento intensivo pela eSF, eMulti e CAPS. Visitas mensais por ACS/ASACE."
elif 8 <= total_pontos <= 12:
    status = "🟡 RISCO MODERADO (NÍVEL 2)"
    cor = "yellow"
    intervencao = "Elaboração de PTS (Projeto Terapêutico Singular). Visitas bimestrais e articulação intersetorial."
else:
    status = "🟢 RISCO BAIXO (NÍVEL 1)"
    cor = "green"
    intervencao = "Monitoramento periódico. Visitas domiciliares trimestrais. Apoio matricial."

st.markdown("---")
st.subheader(f"Pontuação Total: {total_pontos}")
st.markdown(f"### Classificação Final: :{cor}[{status}]")
st.info(f"**Intervenção Recomendada:** {intervencao}")

# --- FUNÇÕES DE PERSISTÊNCIA ---

def salvar_avaliacao():
    # Dicionário atualizado apenas com os dados presentes no formulário
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
        # Lê os dados existentes para concatenar
        df_existing = gs_conn.read(worksheet=WORKSHEET_NAME, ttl=0)
        df_new = pd.DataFrame(row)
        df_final = pd.concat([df_existing, df_new], ignore_index=True)
        
        # Faz o update na planilha
        gs_conn.update(worksheet=WORKSHEET_NAME, data=df_final)
        return True
    except Exception as e:
        st.error(f"Erro ao salvar: {e}")
        return False

def verificar_cabecalhos():
    # Lista de colunas esperadas na planilha Google Sheets
    esperado = [
        "timestamp", "nome_morador", "endereco", "cat1_estrutural", 
        "cat2_sanitario", "cat3_animais", "cat4_obstrucao", 
        "cat5_psicossocial", "total_pontos", "status_risco", "intervencao"
    ]
    try:
        df = gs_conn.read(worksheet=WORKSHEET_NAME, ttl=0)
        cols = list(df.columns)
        faltando = [c for c in esperado if c not in cols]
        if not faltando:
            st.success("Cabeçalhos sincronizados com sucesso!")
        else:
            st.error(f"Faltam as colunas: {', '.join(faltando)}")
    except:
        st.error("Erro ao conectar com a planilha.")

# --- BOTÕES DE AÇÃO ---
if st.button("Salvar avaliação"):
    if nome_morador:
        if salvar_avaliacao():
            st.success("Dados salvos com sucesso!")
    else:
        st.warning("Por favor, preencha o nome do morador antes de salvar.")

st.sidebar.header("Painel Administrativo")
if st.sidebar.button("Validar Colunas"):
    verificar_cabecalhos()