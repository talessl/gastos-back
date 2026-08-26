import yfinance as yf
from src.domain.interfaces.repository_interfaces import IAcaoRepository


class YahooFinanceRepository(IAcaoRepository):
    def buscar_historico(self, ticker: str) -> dict:
        # O Fundamentus devolve "MGLU3", mas o Yahoo exige "MGLU3.SA". Adicionamos o sufixo.
        ticker_yahoo = f"{ticker}.SA" if not ticker.endswith(".SA") else ticker

        acao = yf.Ticker(ticker_yahoo)
        historico = acao.history(period="60d")

        if historico.empty:
            raise ValueError(f"Nenhum dado encontrado para {ticker_yahoo}")

        return {
            "ticker": ticker,
            "preco_atual": float(historico['Close'].iloc[-1]),
            "high": historico['High'].tolist(),
            "low": historico['Low'].tolist(),
            "close": historico['Close'].tolist()
        }
