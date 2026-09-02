import pandas as pd
import requests
from src.domain.interfaces.repository_interfaces import IExploradorMercadoRepository
import requests


class BrapiRepository(IExploradorMercadoRepository):
    def buscar_tickers_por_preco_maximo(self, preco_maximo: float) -> list[str]:
        url = "https://brapi.dev/api/quote/list"
        response = requests.get(url, params={"type": "stock"})
        data = response.json()

        tickers_filtrados = []

        for item in data.get("stocks", []):
            preco_atual = item.get("close")
            ticker = item.get("stock")

            # 1. Verifica se tem preço válido e está abaixo do máximo
            if preco_atual is not None and preco_atual <= preco_maximo:
                # 2. Ignora os fracionários (terminados em F)
                if not ticker.endswith('F'):
                    tickers_filtrados.append(f"{ticker}.SA")

        return tickers_filtrados
