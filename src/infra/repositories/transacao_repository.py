import aiosqlite
from typing import List

from src.domain.entities.transacao import Transacao
from src.infra.config import DB_FILE


class TransacaoRepository:

    async def buscar_todas(self) -> List[Transacao]:
        async with aiosqlite.connect(DB_FILE) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM transacoes"
            ) as cursor:
                rows = await cursor.fetchall()

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

            # O banco gerou um ID, atualizamos a entidade antes de devolvê-la
            transacao.id = cursor.lastrowid
            return transacao

    async def atualizar(self, transacao: Transacao) -> Transacao:
        if transacao.id is None:
            raise ValueError("Não é possível atualizar uma transação sem ID.")

        async with aiosqlite.connect(DB_FILE) as db:
            cursor = await db.execute(
                "UPDATE transacoes SET valor = ?, tipo = ?, observacao = ?, data = ? WHERE id = ?",
                (transacao.valor, transacao.tipo,
                 transacao.observacao, transacao.data, transacao.id)
            )
            await db.commit()

            if cursor.rowcount == 0:
                raise ValueError(
                    f"Transação com id={transacao.id} não encontrada.")

            return transacao

    async def deletar_por_id(self, transacao_id: int) -> bool:
        async with aiosqlite.connect(DB_FILE) as db:
            cursor = await db.execute("DELETE FROM transacoes WHERE id = ?", (transacao_id,))
            await db.commit()

            return cursor.rowcount > 0

    async def limpar_todas(self) -> bool:
        async with aiosqlite.connect(DB_FILE) as db:
            await db.execute("DELETE FROM transacoes ")
            await db.commit()
            return True
