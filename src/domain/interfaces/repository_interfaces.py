from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.transacao import Transacao


class IExploradorMercadoRepository(ABC):
    @abstractmethod
    def buscar_tickers_por_preco_maximo(self, preco_maximo: float) -> list[str]:
        pass


class IAcaoRepository(ABC):
    @abstractmethod
    def buscar_historico(self, ticker: str) -> dict:
        pass


class ITransacaoRepository(ABC):
    @abstractmethod
    async def buscar_todas(self) -> List[Transacao]:
        pass

    @abstractmethod
    async def salvar(self, transacao: Transacao) -> Transacao:
        pass

    @abstractmethod
    async def limpar_todas(self) -> bool:
        pass
