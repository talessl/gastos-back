import strawberry
from typing import List
from strawberry.types import Info

from src.api.graphql.types import TransacaoType, OportunidadeType, IndicadoresType

from src.infra.repositories.transacao_repository import TransacaoRepository
from src.domain.entities.transacao import Transacao

from src.infra.repositories.yahoo_finance_repository import YahooFinanceRepository
from src.infra.repositories.brapi_repository import BrapiRepository
from src.domain.usecases.analisar_acoes_usecase import AnalisarOportunidadesUseCase

transacao_repo = TransacaoRepository()

explorador_repo = BrapiRepository()
acao_repo = YahooFinanceRepository()
analisar_oportunidades_uc = AnalisarOportunidadesUseCase(
    explorador_repo, acao_repo)


@strawberry.type
class Query:
    @strawberry.field
    def buscar_oportunidades(self, preco_maximo: float = 10.0) -> List[OportunidadeType]:
        resultados = analisar_oportunidades_uc.executar(preco_maximo)

        lista_oportunidades = []
        for res in resultados:
            indicadores = IndicadoresType(
                rsi=res["indicadores"]["rsi"],
                estocastico=res["indicadores"]["estocastico"]
            )
            lista_oportunidades.append(
                OportunidadeType(
                    ativo=res["ativo"],
                    preco=res["preco"],
                    status=res["status"],
                    indicadores=indicadores
                )
            )

        return lista_oportunidades

    @strawberry.field
    async def buscar_transacoes(self, info: Info) -> List[TransacaoType]:

        transacoes_db = await transacao_repo.buscar_todas()

        return [
            TransacaoType(
                id=t.id,
                valor=t.valor,
                tipo=t.tipo,
                observacao=t.observacao,
                data=t.data
            ) for t in transacoes_db
        ]


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def adicionar_transacao(self, info: Info, valor: float, tipo: str, observacao: str, data: str) -> TransacaoType:

        transacao_salva = await transacao_repo.salvar(Transacao(
            valor=valor, tipo=tipo, observacao=observacao, data=data
        ))

        return TransacaoType(
            id=transacao_salva.id,
            valor=transacao_salva.valor,
            tipo=transacao_salva.tipo,
            observacao=transacao_salva.observacao,
            data=transacao_salva.data
        )

    @strawberry.mutation
    async def limpar_todas_transacoes(self, info: Info) -> bool:
        return await transacao_repo.limpar_todas()

    @strawberry.mutation
    async def remover_transacao(self, info: Info, id: int) -> bool:
        return await transacao_repo.deletar_por_id(id)


schema = strawberry.Schema(query=Query, mutation=Mutation)
