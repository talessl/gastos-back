# 📊 Gastos API (Back-end)

## ⚠️ Branch
Troque para a branch `feature/back-sem-autenticacao`.

## 🚀 Opções para rodar

### 1. Docker Compose (Aconselhado)
É aconselhado o uso do `docker-compose` disponibilizado. 
**Obs:** Ele deve estar na raiz da pasta que contém tanto o `gastos` (interface) como o `gastos-back` (api).

Comando para executar a partir da pasta raiz:
```bash
docker-compose up -d --build
```

### 2. Manualmente (Local)
Caso queira executar manualmente, lembre de instalar as dependências:
```bash
pip install -r requirements.txt
```
E se atente à porta ao usar o comando:
```bash
uvicorn src.api.main:app --reload --port 4000
```

## 📌 Observação sobre a API de Ações
A API utiliza a API externa Yahoo Finance. É normal que a busca das ações demore um pouco, devido à escolha de filtro.
