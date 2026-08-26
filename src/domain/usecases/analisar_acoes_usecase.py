import pandas as pd
import pandas_ta as ta
from src.domain.interfaces.repository_interfaces import IExploradorMercadoRepository, IAcaoRepository
from src.domain.entities.ativo_financeiro import AnaliseAcao


class AnalisarOportunidadesUseCase:
    def __init__(
        self,
        explorador_repo: IExploradorMercadoRepository,
        acao_repo: IAcaoRepository
    ):
        self.explorador_repo = explorador_repo
        self.acao_repo = acao_repo

    def executar(self, preco_maximo: float) -> list[dict]:
        oportunidades = []
        tickers_filtrados = self.explorador_repo.buscar_tickers_por_preco_maximo(
            preco_maximo)

        for ticker in tickers_filtrados:
            try:
                dados = self.acao_repo.buscar_historico(ticker)

                rsi = self._calcular_rsi(dados['close'])
                estocastico = self._calcular_estocastico(
                    dados['high'], dados['low'], dados['close'])
                analise = AnaliseAcao(
                    ticker=ticker,
                    preco_atual=dados['preco_atual'],
                    rsi=rsi,
                    estocastico_lento=estocastico
                )

                if analise.is_oportunidade_de_compra():
                    oportunidades.append(analise.obter_resumo())
            except Exception as e:
                print(
                    f"Alerta: Erro ao processar o ticker {ticker} - {str(e)}")
                continue

        return oportunidades

    def _calcular_rsi(self, close: list) -> float:
        serie_close = pd.Series(close)
        rsi_calculado = ta.rsi(serie_close, length=14)

        # Pega o último valor calculado (o dia de hoje)
        return float(rsi_calculado.iloc[-1]) if rsi_calculado is not None else None

    def _calcular_estocastico(self, high: list, low: list, close: list) -> float:
        df = pd.DataFrame({'high': high, 'low': low, 'close': close})

        # k=14 (período), d=3 (média), smooth_k=3 (suavização para o Estocástico Lento)
        stoch_calculado = ta.stoch(
            df['high'], df['low'], df['close'], k=14, d=3, smooth_k=3)

        if stoch_calculado is not None:
            # A coluna STOCHk_14_3_3 representa a linha K do Estocástico Lento
            return float(stoch_calculado['STOCHk_14_3_3'].iloc[-1])
        return None
