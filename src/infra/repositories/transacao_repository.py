import aiosqlite
from typing import List

from src.domain.entities.transacao import Transacao
from src.infra.config import DB_FILE


class TransacaoRepository:

    async def buscar_todas(self, usuario_id: int) -> List[Transacao]:
        async with aiosqlite.connect(DB_FILE) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM transacoes WHERE usuario_id = ?", (usuario_id,)
            ) as cursor:
                rows = await cursor.fetchall()

                return [
                    Transacao(
                        id=row["id"],
                        usuario_id=row["usuario_id"],
                        valor=row["valor"],
                        tipo=row["tipo"],
                        observacao=row["observacao"],
                        data=row["data"]
                    ) for row in rows
                ]

    async def salvar(self, transacao: Transacao) -> Transacao:
        async with aiosqlite.connect(DB_FILE) as db:
            cursor = await db.execute(
                "INSERT INTO transacoes (valor, tipo, observacao, data, usuario_id) VALUES (?, ?, ?, ?, ?)",
                (transacao.valor, transacao.tipo,
                 transacao.observacao, transacao.data, transacao.usuario_id)
            )
            await db.commit()

            # O banco gerou um ID, atualizamos a entidade antes de devolvê-la
            transacao.id = cursor.lastrowid
            return transacao

    async def limpar_todas(self, usuario_id: int) -> bool:
        async with aiosqlite.connect(DB_FILE) as db:
            await db.execute("DELETE FROM transacoes WHERE usuario_id = ?", (usuario_id,))
            await db.commit()
            return True
