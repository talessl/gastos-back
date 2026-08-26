import strawberry
from typing import Optional


@strawberry.type
class TransacaoType:
    id: Optional[int]
    valor: float
    tipo: str
    observacao: str
    data: str


@strawberry.type
class IndicadoresType:
    rsi: float
    estocastico: float


@strawberry.type
class OportunidadeType:
    ativo: str
    preco: str
    status: str
    indicadores: IndicadoresType
