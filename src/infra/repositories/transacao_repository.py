import aiosqlite
from typing import List

# Importamos a nossa entidade pura e a variável de conexão
from src.domain.entities.transacao import Transacao
from src.infra.database.connection import DB_FILE


class TransacaoRepository:

    async def buscar_todas(self) -> List[Transacao]:
        async with aiosqlite.connect(DB_FILE) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("SELECT * FROM transacoes") as cursor:
                rows = await cursor.fetchall()

                # Traduzimos as linhas do banco (dicionários) para a nossa Entidade
                return [
                    Transacao(
                        id=row["id"],
                        valor=row["valor"],
                        tipo=row["tipo"],
                        observacao=row["observacao"],
                        data=row["data"]
                    ) for row in rows
                ]

    async def salvar(self, transacao: Transacao) -> Transacao:
        async with aiosqlite.connect(DB_FILE) as db:
            cursor = await db.execute(
                "INSERT INTO transacoes (valor, tipo, observacao, data) VALUES (?, ?, ?, ?)",
                (transacao.valor, transacao.tipo,
                 transacao.observacao, transacao.data)
            )
            await db.commit()

            # O banco gerou um ID, então atualizamos a entidade antes de devolvê-la
            transacao.id = cursor.lastrowid
            return transacao

    async def limpar_todas(self) -> bool:
        async with aiosqlite.connect(DB_FILE) as db:
            await db.execute("DELETE FROM transacoes")
            await db.commit()
            return True
