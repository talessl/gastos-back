import strawberry
from typing import List
from strawberry.types import Info

from src.api.graphql.types import TransacaoType, OportunidadeType, IndicadoresType

from src.infra.repositories.transacao_repository import TransacaoRepository
from src.domain.usecases.gerenciar_transacao_usecase import GerenciarTransacoesUseCase

from src.infra.repositories.yahoo_finance_repository import YahooFinanceRepository
from src.infra.repositories.brapi_repository import BrapiRepository
from src.domain.usecases.analisar_acoes_usecase import AnalisarOportunidadesUseCase

transacao_repo = TransacaoRepository()
gerenciar_transacoes_uc = GerenciarTransacoesUseCase(transacao_repo)

explorador_repo = BrapiRepository()
acao_repo = YahooFinanceRepository()
analisar_oportunidades_uc = AnalisarOportunidadesUseCase(
    explorador_repo, acao_repo)


@strawberry.type
class Query:
    @strawberry.field
    async def buscar_transacoes(self, info: Info) -> List[TransacaoType]:

        transacoes_db = await gerenciar_transacoes_uc.listar_transacoes()

        return [
            TransacaoType(
                id=t.id,
                valor=t.valor,
                tipo=t.tipo,
                observacao=t.observacao,
                data=t.data
            ) for t in transacoes_db
        ]

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


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def adicionar_transacao(self, info: Info, valor: float, tipo: str, observacao: str, data: str) -> TransacaoType:

        transacao_salva = await gerenciar_transacoes_uc.criar_transacao(valor=valor, tipo=tipo, observacao=observacao, data=data)

        return TransacaoType(
            id=transacao_salva.id,
            valor=transacao_salva.valor,
            tipo=transacao_salva.tipo,
            observacao=transacao_salva.observacao,
            data=transacao_salva.data
        )

    @strawberry.mutation
    async def limpar_transacoes(self, info: Info) -> bool:
        return await gerenciar_transacoes_uc.limpar_transacoes()


schema = strawberry.Schema(query=Query, mutation=Mutation)
