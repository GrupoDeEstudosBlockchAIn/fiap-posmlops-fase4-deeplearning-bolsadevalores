import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def preprocess_data(input_path, output_path, sequence_length=60):
    """
    Pré-processa os dados para treinamento do modelo LSTM.
    
    Args:
        input_path (str): Caminho do arquivo CSV com dados brutos
        output_path (str): Caminho para salvar os dados processados
        sequence_length (int): Tamanho da sequência para o LSTM
    """
    try:
        # Carregar dados
        df = pd.read_csv(input_path)
        
        # Usar apenas a coluna 'Close' para previsão
        data = df[['Close']].values
        
        # Normalizar os dados
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(data)
        
        # Criar sequências para o LSTM
        X, y = [], []
        for i in range(sequence_length, len(scaled_data)):
            X.append(scaled_data[i-sequence_length:i])
            y.append(scaled_data[i])
        
        X, y = np.array(X), np.array(y)
        
        # Dividir em treino e teste (80% treino, 20% teste)
        train_size = int(len(X) * 0.8)
        X_train, X_test = X[:train_size], X[train_size:]
        y_train, y_test = y[:train_size], y[train_size:]
        
        # Salvar dados processados com o scaler como objeto
        np.savez_compressed(output_path, 
            X_train=X_train, y_train=y_train, 
            X_test=X_test, y_test=y_test, 
            scaler=scaler)
        
        print(f"Dados processados salvos em {output_path}")
        return X_train, y_train, X_test, y_test, scaler
    except Exception as e:
        print(f"Erro no pré-processamento: {e}")
        return None
