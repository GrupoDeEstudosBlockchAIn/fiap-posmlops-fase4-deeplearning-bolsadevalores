import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import os
import tensorflow as tf

def build_and_train_model(X_train, y_train, model_path, epochs=50, batch_size=32):
    """
    Constrói e treina o modelo LSTM.
    
    Args:
        X_train (np.array): Dados de treinamento
        y_train (np.array): Rótulos de treinamento
        model_path (str): Caminho para salvar o modelo
        epochs (int): Número de épocas
        batch_size (int): Tamanho do lote
    """
    try:
        # Construir o modelo
        model = Sequential()
        model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
        model.add(Dropout(0.2))
        model.add(LSTM(units=50, return_sequences=False))
        model.add(Dropout(0.2))
        model.add(Dense(units=25))
        model.add(Dense(units=1))
        
        # Compilar o modelo
        model.compile(optimizer='adam', loss='mean_squared_error')
        
        # Treinar o modelo
        model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=1)
        
        # Salvar o modelo
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        model.save(model_path)
        print(f"Modelo salvo em {model_path}")
        
        return model
    except Exception as e:
        print(f"Erro no treinamento: {e}")
        return None