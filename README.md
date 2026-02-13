📋 Calculadora Multidimensional de Risco de Acumulação
Este projeto é uma ferramenta de apoio à decisão para avaliação de casos de acumulação severa (objetos e animais). Ele permite que técnicos e pesquisadores realizem uma avaliação estruturada em cinco dimensões, gerando automaticamente uma classificação de risco e recomendações de intervenção.

O projeto foi desenvolvido como parte dos meus estudos em Ciência de Dados e Inteligência Artificial na UFPB.

🚀 Demonstração
O sistema está publicado e pode ser acessado pelo link:
calculadora-risco-acumulacao.streamlit.app

🛠️ Tecnologias Utilizadas
Python: Linguagem principal para lógica de dados.

Streamlit: Framework para a interface web interativa.

Pandas: Manipulação e estruturação dos dados coletados.

Google Sheets API: Persistência de dados em nuvem via conta de serviço.

GitHub Actions/Streamlit Cloud: Deploy e integração contínua.

📊 Metodologia de Avaliação
O sistema pontua cinco categorias críticas (0 a 4 pontos cada):

Risco Estrutural: Condições físicas do imóvel.

Risco Sanitário: Presença de vetores (ratos, baratas) e higiene.

Acúmulo de Animais: Quantidade, bem-estar e zoonoses.

Uso do Espaço: Nível de obstrução e acessibilidade.

Vulnerabilidade Psicossocial: Capacidade de autocuidado e rede de apoio.

Classificação de Risco
🟢 0–7 Pontos: Risco Baixo.

🟡 8–12 Pontos: Risco Moderado.

🟠 13–20 Pontos: Risco Alto.

🔴 ≥21 Pontos ou Item Nível 4: Risco Grave (Prioridade Assistencial).

📂 Estrutura do Projeto
site.py: Código-fonte da aplicação Streamlit.

requirements.txt: Dependências do ambiente.

.streamlit/secrets.toml: (Protegido) Configurações de autenticação segura para conexão com a API do Google.
