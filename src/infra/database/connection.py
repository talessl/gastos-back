import aiosqlite
from src.infra.config import DB_FILE


async def init_db():
    """
    Função responsável por inicializar o banco de dados.
    Garante que a tabela 'transacoes' exista antes de qualquer requisição.
    """
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS transacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                valor REAL,
                tipo TEXT,
                observacao TEXT,
                data TEXT,
                usuario_id INTEGER NOT NULL
            )
        """)
        await db.commit()
