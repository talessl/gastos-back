from typing import List
from src.domain.entities.transacao import Transacao
from src.domain.interfaces.repository_interfaces import ITransacaoRepository

TIPOS_VALIDOS = {"LUCRO", "GASTO"}


class GerenciarTransacoesUseCase:
    def __init__(self, transacao_repo: ITransacaoRepository):
        self.transacao_repo = transacao_repo

    async def listar_transacoes(self) -> List[Transacao]:
        return await self.transacao_repo.buscar_todas()

    async def criar_transacao(self, valor: float, tipo: str, observacao: str, data: str) -> Transacao:
        self._validar(valor, tipo)

        nova_transacao = Transacao(
            valor=valor, tipo=tipo, observacao=observacao, data=data)

        return await self.transacao_repo.salvar(nova_transacao)

    async def limpar_transacoes(self) -> bool:
        return await self.transacao_repo.limpar_todas()

    def _validar(self, valor: float, tipo: str) -> None:
        if valor <= 0:
            raise ValueError("O valor da transação deve ser maior que zero.")
        if tipo not in TIPOS_VALIDOS:
            raise ValueError(
                f"Tipo inválido: '{tipo}'. Use um destes: {TIPOS_VALIDOS}")
