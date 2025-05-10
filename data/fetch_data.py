# Funções de coleta e preparação de dados
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import os
import joblib
from core import config

def fetch_and_prepare_data(symbol=config.symbol, start_date=config.start_date, end_date=config.end_date, window_size=config.window_size):
    # Baixar os dados do Yahoo Finance
    df = yf.download(symbol, start=start_date, end=end_date)

    if df.empty:
        raise ValueError("Nenhum dado foi retornado. Verifique o símbolo ou datas fornecidas.")

    # Selecionar apenas a coluna 'Close'
    close_prices = df['Close'].values.reshape(-1, 1)

    # Normalizar os dados
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(close_prices)

    # Salvar o scaler para uso futuro
    os.makedirs('data', exist_ok=True)
    joblib.dump(scaler, 'data/scaler.pkl')

    # Criar sequências para LSTM
    X, y = [], []
    for i in range(window_size, len(scaled_data)):
        X.append(scaled_data[i - window_size:i, 0])
        y.append(scaled_data[i, 0])

    X, y = np.array(X), np.array(y)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))

    return X, y, df

if __name__ == "__main__":
    X, y, df = fetch_and_prepare_data()
    print(f"Dados prontos: X shape = {X.shape}, y shape = {y.shape}")
