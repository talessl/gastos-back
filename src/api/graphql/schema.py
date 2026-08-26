import strawberry
from typing import List

# Importamos o Tipo do GraphQL (O formato que vai para a internet)
from src.api.graphql.types import TransacaoType, OportunidadeType, IndicadoresType

# Importamos a Entidade pura e o Repositório (O motor do banco)
from src.domain.entities.transacao import Transacao
from src.infra.repositories.transacao_repository import TransacaoRepository

from src.infra.repositories.yahoo_finance_repository import YahooFinanceRepository
from src.infra.repositories.brapi_repository import BrapiRepository
from src.domain.usecases.analisar_acoes_usecase import AnalisarOportunidadesUseCase

# Instanciamos o nosso repositório
repository = TransacaoRepository()
explorador_repo = BrapiRepository()
acao_repo = YahooFinanceRepository()
analisar_oportunidades_uc = AnalisarOportunidadesUseCase(
    explorador_repo, acao_repo)


@strawberry.type
class Query:
    @strawberry.field
    async def buscar_transacoes(self) -> List[TransacaoType]:
        # 1. Pede os dados puros (Entidades) para o Repositório
        transacoes_db = await repository.buscar_todas()

        # 2. Traduz a Entidade do Domínio para o Tipo do GraphQL
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
    async def adicionar_transacao(self, valor: float, tipo: str, observacao: str, data: str) -> TransacaoType:
        # 1. Cria a Entidade pura do Domínio com os dados do Front-end
        nova_transacao = Transacao(
            valor=valor, tipo=tipo, observacao=observacao, data=data)

        # 2. Manda o Repositório salvar e pegar o ID gerado
        transacao_salva = await repository.salvar(nova_transacao)

        # 3. Devolve para o Front-end no formato GraphQL
        return TransacaoType(
            id=transacao_salva.id,
            valor=transacao_salva.valor,
            tipo=transacao_salva.tipo,
            observacao=transacao_salva.observacao,
            data=transacao_salva.data
        )

    @strawberry.mutation
    async def limpar_transacoes(self) -> bool:
        return await repository.limpar_todas()


# Exportamos o esquema pronto para ser plugado no FastAPI
schema = strawberry.Schema(query=Query, mutation=Mutation)
