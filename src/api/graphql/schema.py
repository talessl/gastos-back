import strawberry
from typing import List
from strawberry.types import Info

from src.api.graphql.types import TransacaoType, OportunidadeType, IndicadoresType, AcaoBuscadaType

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
    def buscar_acao(self, ticker: str) -> AcaoBuscadaType:
        # Como é uma leitura simples, instanciamos o repositório direto
        repo = YahooFinanceRepository()

        try:
            dados = repo.buscar_historico(ticker)
            return AcaoBuscadaType(
                ticker=dados["ticker"],
                preco_atual=dados["preco_atual"]
            )
        except Exception as e:
            raise ValueError(f"Ação não encontrada ou erro na busca: {str(e)}")

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
    async def atualizar_transacao(self, info: Info, id: int, valor: float, tipo: str, observacao: str, data: str) -> TransacaoType:

        transacao_atualizada = await transacao_repo.atualizar(Transacao(
            id=id, valor=valor, tipo=tipo, observacao=observacao, data=data
        ))

        return TransacaoType(
            id=transacao_atualizada.id,
            valor=transacao_atualizada.valor,
            tipo=transacao_atualizada.tipo,
            observacao=transacao_atualizada.observacao,
            data=transacao_atualizada.data
        )

    @strawberry.mutation
    async def limpar_todas_transacoes(self, info: Info) -> bool:
        return await transacao_repo.limpar_todas()

    @strawberry.mutation
    async def remover_transacao(self, info: Info, id: int) -> bool:
        return await transacao_repo.deletar_por_id(id)


schema = strawberry.Schema(query=Query, mutation=Mutation)
