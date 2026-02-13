# 📋 Calculadora Multidimensional de Risco de Acumulação

Este projeto é uma ferramenta de apoio à decisão para avaliação de casos de acumulação (objetos e animais), desenvolvida para auxiliar equipes técnicas na classificação de riscos e definição de intervenções.

O sistema permite a coleta estruturada de dados em campo e automatiza a análise com base em critérios multidimensionais, salvando os resultados em tempo real em uma base de dados na nuvem.

## 🚀 Demonstração
O aplicativo está publicado e pode ser acessado em:
👉 **[calculadora-risco-acumulacao.streamlit.app](https://calculadora-risco-acumulacao.streamlit.app/)**

## 🛠️ Tecnologias Utilizadas
* **Python**: Linguagem base para o desenvolvimento da lógica.
* **Streamlit**: Framework utilizado para a criação da interface web interativa.
* **Pandas**: Biblioteca para estruturação e manipulação dos dados das avaliações.
* **Google Sheets API**: Integração para persistência de dados via Service Account.
* **GitHub**: Controle de versão e hospedagem do código-fonte.

## 📊 Metodologia de Avaliação
A calculadora avalia cinco categorias críticas, com pontuações de 0 a 4 para cada uma:

1. **Risco Estrutural**: Avaliação da integridade física do imóvel.
2. **Risco Sanitário**: Verificação de higiene e presença de vetores como ratos e baratas.
3. **Acúmulo de Animais**: Diagnóstico da quantidade e bem-estar dos animais presentes.
4. **Uso do Espaço**: Medição do nível de obstrução de cômodos e saídas.
5. **Vulnerabilidade Psicossocial**: Análise da autonomia e rede de apoio do morador.



### Classificação Final
O sistema calcula a soma total e gera automaticamente a classificação:
* 🟢 **0–7 pontos**: Risco Baixo.
* 🟡 **8–12 pontos**: Risco Moderado.
* 🟠 **13–20 pontos**: Risco Alto.
* 🔴 **≥21 pontos (ou qualquer item nível 4)**: Risco Grave.

## 📂 Estrutura de Arquivos
* `site.py`: Script principal com a interface e lógica de cálculo.
* `requirements.txt`: Lista de bibliotecas necessárias para rodar o projeto.
* `.streamlit/secrets.toml`: Arquivo de configuração de chaves de API (não incluído no repositório por segurança).

## 👤 Autor
Desenvolvido por um estudante de **Ciência de Dados e Inteligência Artificial** da **UFPB** (Universidade Federal da Paraíba).
