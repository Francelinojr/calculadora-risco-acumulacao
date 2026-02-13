import streamlit as st
from datetime import datetime
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Calculadora de Risco de Acumulação", page_icon="📋")

st.title("📋 Avaliação Multidimensional de Acumulação")
st.markdown("---")

gs_conn = st.connection("gsheets", type=GSheetsConnection)
WORKSHEET_NAME = "Avaliacoes_Acumulacao1"

# --- CATEGORIA 1: RISCO ESTRUTURAL ---
st.header("🔹 Categoria 1 – Risco Estrutural")
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
st.header("🔹 Categoria 2 – Risco Sanitário / Higiênico")
cat2 = st.radio("Selecione a condição sanitária:",
                options=[0, 1, 2, 3, 4],
                format_func=lambda x: [
                    "0 – Ambiente limpo",
                    "1 – Lixo leve",
                    "2 – Lixo moderado / insetos ocasionais",
                    "3 – Lixo putrefato / fezes / odor forte",
                    "4 – Infestação grave (ratos/baratas/escorpiões)"
                ][x])
st.subheader("Vetores identificados")
col_v1, col_v2, col_v3, col_v4 = st.columns(4)
with col_v1:
    v_baratas = st.checkbox("Baratas")
with col_v2:
    v_ratos = st.checkbox("Ratos")
with col_v3:
    v_escorpioes = st.checkbox("Escorpiões")
with col_v4:
    v_moscas = st.checkbox("Moscas")
v_outros = st.text_input("Outros (descrição)")

# --- CATEGORIA 3: ACÚMULO DE ANIMAIS ---
st.header("🔹 Categoria 3 – Acúmulo de Animais")

qtd_animais = st.number_input("Quantidade de animais", min_value=0, step=1, value=0)
especies = st.text_input("Espécies")

cat3 = st.radio("Selecione a condição dos animais:",
                options=[0, 1, 2, 3, 4],
                format_func=lambda x: [
                    "0 – Quantidade adequada e cuidados presentes",
                    "1 – Leve desorganização",
                    "2 – Número acima do suportado",
                    "3 – Maus-tratos evidentes",
                    "4 – Acumulação severa (>15–20 animais / cadáveres / zoonoses)"
                ][x])

cond_animais = st.radio("Condição corporal dos animais:", 
                        options=["Adequada", "Magros", "Doentes", "Feridos"])

obs_vet = st.text_area("Digite as observações veterinárias/sanitárias aqui...")


# --- CATEGORIA 4: USO DO ESPAÇO ---
st.header("🔹 Categoria 4 – Uso do Espaço / Obstrução")
cat4 = st.radio("Selecione o nível de obstrução:",
                options=[0, 1, 2, 3, 4],
                format_func=lambda x: [
                    "0 – Todos os cômodos funcionais",
                    "1 – Bagunça leve",
                    "2 – 1–2 cômodos inutilizados",
                    "3 – Mais da metade da casa inacessível",
                    "4 – Saídas bloqueadas"
                ][x])

comodos_inutilizados = st.text_input("Cômodos inutilizados")

# --- CATEGORIA 5: VULNERABILIDADE PSICOSSOCIAL ---
st.header("🔹 Categoria 5 – Vulnerabilidade Psicossocial")
cat5 = st.radio("Selecione a vulnerabilidade:",
                options=[0, 1, 2, 3, 4],
                format_func=lambda x: [
                    "0 – Autonomia preservada",
                    "1 – Isolamento leve",
                    "2 – Sem rede de apoio",
                    "3 – Autoabandono",
                    "4 – Incapacidade grave de autocuidado"
                ][x])

mora_sozinho = st.radio("Morador mora sozinho?", options=["Sim", "Não"], index=1)
acomp_saude = st.radio("Recebe acompanhamento de saúde?", options=["Sim", "Não"], index=1)

aps = st.text_area("Digite as observações sociais/APS aqui...")


# --- CÁLCULO FINAL ---
total_pontos = cat1 + cat2 + cat3 + cat4 + cat5
tem_item_4 = any([cat1==4, cat2==4, cat3==4, cat4==4, cat5==4])

st.markdown("---")
st.subheader(f"Pontuação Total: {total_pontos}")

# Lógica de Classificação conforme sua imagem
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

st.markdown(f"### Classificação Final: :{cor}[{status}]")
st.info(f"**Intervenção Recomendada:** {intervencao}")

st.subheader("Cálculo do Risco Global")
col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    st.metric("Estrutural", cat1)
with col2:
    st.metric("Sanitário", cat2)
with col3:
    st.metric("Animais", cat3)
with col4:
    st.metric("Uso do espaço", cat4)
with col5:
    st.metric("Psicossocial", cat5)
with col6:
    st.metric("Total geral", total_pontos)

st.markdown("#### Critérios de Classificação")
st.markdown("- 0–7 → 🟢 RISCO BAIXO")
st.markdown("- 8–12 → 🟡 RISCO MODERADO")
st.markdown("- 13–20 → 🟠 RISCO ALTO")
st.markdown("- ≥21 ou qualquer item 4 → 🔴 RISCO GRAVE")

def salvar_avaliacao():
    row = {
        "timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "qtd_animais": [int(qtd_animais)],
        "especies": [especies],
        "v_baratas": [int(v_baratas)],
        "v_ratos": [int(v_ratos)],
        "v_escorpioes": [int(v_escorpioes)],
        "v_moscas": [int(v_moscas)],
        "v_outros": [v_outros],
        "cat1": [int(cat1)],
        "cat2": [int(cat2)],
        "cat3": [int(cat3)],
        "cat4": [int(cat4)],
        "cat5": [int(cat5)],
        "cond_animais": [cond_animais],
        "comodos_inutilizados": [comodos_inutilizados],
        "mora_sozinho": [mora_sozinho],
        "acomp_saude": [acomp_saude],
        "obs_vet": [obs_vet],
        "aps": [aps],
        "total_pontos": [int(total_pontos)],
        "tem_item_4": [int(tem_item_4)],
        "status": [status],
        "intervencao": [intervencao],
    }
    try:
        df_existing = gs_conn.read(worksheet=WORKSHEET_NAME, ttl=0)
        df_final = pd.concat([df_existing, pd.DataFrame(row)], ignore_index=True)
        gs_conn.update(worksheet=WORKSHEET_NAME, data=df_final)
        return True
    except Exception as e:
        st.error(f"Falha ao salvar na planilha: {e}")
        return False

def conn_gsheets_read():
    try:
        return gs_conn.read(worksheet=WORKSHEET_NAME, ttl=0)
    except Exception:
        return None

def has_service_account():
    try:
        t = st.secrets.get("connections", {}).get("gsheets", {}).get("type", "")
        return str(t).lower() == "service_account"
    except Exception:
        return False

def verificar_cabecalhos():
    esperado = [
        "timestamp","qtd_animais","especies","v_baratas","v_ratos","v_escorpioes","v_moscas","v_outros",
        "cat1","cat2","cat3","cat4","cat5","cond_animais","comodos_inutilizados","mora_sozinho","acomp_saude",
        "obs_vet","aps","total_pontos","tem_item_4","status","intervencao"
    ]
    df = conn_gsheets_read()
    if df is None:
        st.error(f"Não foi possível ler a aba '{WORKSHEET_NAME}'. Verifique secrets e permissões.")
        return
    cols = list(df.columns)
    faltando = [c for c in esperado if c not in cols]
    extras = [c for c in cols if c not in esperado]
    if not faltando and not extras:
        st.success("Cabeçalhos conferem com o esperado.")
    else:
        if faltando:
            st.error(f"Faltando na planilha: {', '.join(faltando)}")
        if extras:
            st.warning(f"Colunas extras na planilha: {', '.join(extras)}")

if st.button("Salvar avaliação"):
    ok_sheet = salvar_avaliacao()
    if ok_sheet:
        st.success(f"Avaliação salva na planilha Google ({WORKSHEET_NAME}).")
        
col_t1, col_t2 = st.columns(2)
with col_t1:
    if st.button("Testar conexão"):
        if has_service_account():
            df = conn_gsheets_read()
            if df is None:
                st.error(f"Falha ao ler '{WORKSHEET_NAME}'. Cheque compartilhamento com a service account.")
            else:
                st.success(f"Conexão OK. Linhas atuais: {len(df)}")
        else:
            st.error("Secrets ausentes ou sem 'type = service_account'. Configure para habilitar escrita.")
with col_t2:
    if st.button("Verificar cabeçalhos"):
        verificar_cabecalhos()
