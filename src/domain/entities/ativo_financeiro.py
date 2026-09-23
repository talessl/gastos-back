# arquivo: src/domain/entities/analise_acao.py
import math


class AnaliseAcao:
    def __init__(self, ticker: str, preco_atual: float, rsi: float, estocastico_lento: float):
        # Garante que sempre fique maiúsculo (ex: petr4 vira PETR4)
        self.ticker = ticker.upper()
        self.preco_atual = preco_atual
        self.rsi = rsi
        self.estocastico_lento = estocastico_lento

        # Assim que a entidade nasce, ela se auto-valida
        self.validar()

    def validar(self):
        if not self.ticker:
            raise ValueError("O Ticker da ação é obrigatório.")

        # None e NaN primeiro, antes de qualquer comparação
        for nome, valor in (("RSI", self.rsi), ("Estocástico", self.estocastico_lento)):
            if valor is None or math.isnan(valor):
                raise ValueError(
                    f"Dados insuficientes no Yahoo Finance para {self.ticker} ({nome})")

        if not 0 <= self.rsi <= 100:
            raise ValueError(
                f"O IFR (RSI) deve estar entre 0 e 100. Valor recebido: {self.rsi}")
        if not 0 <= self.estocastico_lento <= 100:
            raise ValueError(
                f"O Estocástico Lento deve estar entre 0 e 100. Valor recebido: {self.estocastico_lento}")
    # A nossa Regra de Negócio Pura!

    def is_oportunidade_de_compra(self) -> bool:
        # A regra de ouro: RSI abaixo de 30 e Estocástico abaixo de 20
        is_rsi_sobrevendido = self.rsi < 30
        is_estocastico_sobrevendido = self.estocastico_lento < 20

        return is_rsi_sobrevendido and is_estocastico_sobrevendido

    def obter_resumo(self) -> dict:
        return {
            "ativo": self.ticker,
            "preco": f"R$ {self.preco_atual:.2f}",
            "status": "COMPRA FORTE" if self.is_oportunidade_de_compra() else "AGUARDAR",
            "indicadores": {
                "rsi": round(self.rsi, 2),
                "estocastico": round(self.estocastico_lento, 2)
            }
        }
