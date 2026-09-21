# 📊 Gastos API (Back-end)

Descrição: O projeto foi desenvolvido com o intuito de facilitar o controle financeiro por meio de uma interface de calendário, oferecendo uma interatividade prática para adição e gerenciamento de lucros e gastos durante o mês. Além disso, há a utilização de APIs externas (Brapi e YahooFinance) para a checagem de oportunidades no mercado da B3, seguindo uma estratégia de ações em estado de sobrevenda (Índices: RSI abaixo de 30 e Estocástico abaixo de 20). A plataforma também permite a consulta rápida de ações do mercado.

## 🚀 Opções para rodar

### 1. Docker Compose (Aconselhado)
É aconselhado o uso do `docker-compose` disponibilizado na interface (Front-end). 
**Obs:** Ele deve estar na raiz da pasta que contém tanto o `gastos` (interface) como o `gastos-back` (api).

Comando para executar a partir da pasta raiz:
```bash
docker-compose up -d --build
```

### 2. Manualmente (Local)
Caso queira executar manualmente, lembre de configurar o ambiente e instalar as dependências:

```bash
python -m venv venv
```

```bash
pip install -r requirements.txt
```
E se atente à porta ao usar o comando:
```bash
uvicorn src.api.main:app --reload --port 4000
```

## 📌 Observação sobre a API de Ações
A API utiliza a API externa Yahoo Finance. É normal que a busca das ações demore um pouco, devido à escolha de filtro.
