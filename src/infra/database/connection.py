import aiosqlite

# O caminho do nosso banco de dados.
# Se preferir, em projetos reais, pegamos isso de variáveis de ambiente (.env)
DB_FILE = "./banco-dados.sqlite"


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
                data TEXT
            )
        """)
        await db.commit()
