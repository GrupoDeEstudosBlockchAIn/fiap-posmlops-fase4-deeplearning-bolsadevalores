import requests
import pandas as pd
import os
from datetime import datetime

# Você pode mover esta chave para uma variável de ambiente em produção
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

def collect_stock_data(ticker, start_date, end_date, output_path):
    """
    Coleta dados históricos de ações usando a API Alpha Vantage e salva em CSV.
    
    Args:
        ticker (str): Símbolo da ação (ex: 'AAPL')
        start_date (str): Data inicial (formato 'YYYY-MM-DD')
        end_date (str): Data final (formato 'YYYY-MM-DD')
        output_path (str): Caminho para salvar o arquivo CSV
    """
    try:
        print(f"Solicitando dados de {ticker} via Alpha Vantage...")
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": ticker,
            "apikey": ALPHA_VANTAGE_API_KEY,
            "outputsize": "full",
            "datatype": "json"
        }

        response = requests.get(url, params=params)
        data = response.json()

        print("Resposta da API:", list(data.keys()))

        if "Time Series (Daily)" not in data:
            raise ValueError(f"Erro na resposta da API Alpha Vantage: {data.get('Note') or data.get('Error Message') or 'Resposta inesperada.'}")

        # Organiza os dados em DataFrame
        daily_data = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient="index")
        daily_data = daily_data.rename(columns={
            "1. open": "Open",
            "2. high": "High",
            "3. low": "Low",
            "4. close": "Close",
            "5. volume": "Volume"
        })

        daily_data.index = pd.to_datetime(daily_data.index)
        daily_data = daily_data.sort_index()

        # Garante que as colunas necessárias existam antes de prosseguir
        expected_cols = ["Open", "High", "Low", "Close", "Volume"]
        missing_cols = [col for col in expected_cols if col not in daily_data.columns]
        if missing_cols:
            raise ValueError(f"Colunas ausentes nos dados retornados: {missing_cols}")

        daily_data = daily_data[expected_cols].astype(float)

        # Filtra intervalo de datas
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        filtered_data = daily_data[(daily_data.index >= start) & (daily_data.index <= end)]

        if filtered_data.empty:
            raise ValueError("Nenhum dado disponível no intervalo fornecido.")

        # Salva como CSV
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        filtered_data.to_csv(output_path)
        print(f"Dados salvos com sucesso em: {output_path}")
        return filtered_data

    except Exception as e:
        print(f"Erro ao coletar dados de {ticker}: {e}")
        return None
