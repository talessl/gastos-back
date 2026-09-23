# src/infra/config.py
import os
from dotenv import load_dotenv

load_dotenv()

# --- Banco de dados ---
DB_FILE = os.getenv("DB_FILE", "./banco-dados.sqlite")

# --- Validação básica ---
if not DB_FILE:
    raise ValueError("DB_FILE não configurado. Verifique seu arquivo .env")
