from abc import ABC, abstractmethod
from typing import Dict, Any


class IExploradorMercadoRepository(ABC):
    @abstractmethod
    def buscar_tickers_por_preco_maximo(self, preco_maximo: float) -> list[str]:
        pass


class IAcaoRepository(ABC):
    @abstractmethod
    def buscar_historico(self, ticker: str) -> dict:
        pass
