from dataclasses import dataclass
from typing import Optional


@dataclass
class Transacao:
    valor: float
    tipo: str
    observacao: str
    data: str
    # O ID é opcional pois uma transação nova não tem ID até ser salva
    id: Optional[int] = None
