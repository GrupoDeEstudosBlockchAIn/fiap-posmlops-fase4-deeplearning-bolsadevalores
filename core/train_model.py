# Lógica de treino do modelo
import os
from domain.model import create_lstm_model
from data.fetch_data import fetch_and_prepare_data
from core import config
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
import numpy as np
import joblib
from tensorflow.keras.callbacks import ModelCheckpoint

def train():
    X, y, df = fetch_and_prepare_data()

    model = create_lstm_model((X.shape[1], 1))

    # Salvar o melhor modelo automaticamente
    os.makedirs("models", exist_ok=True)
    checkpoint = ModelCheckpoint("models/lstm_model.h5", monitor="loss", save_best_only=True, verbose=1)

    history = model.fit(X, y, epochs=20, batch_size=32, callbacks=[checkpoint])

    # Avaliação
    predictions = model.predict(X)
    scaler = joblib.load("data/scaler.pkl")
    y_true = scaler.inverse_transform(y.reshape(-1, 1))
    y_pred = scaler.inverse_transform(predictions)

    print("MAE:", mean_absolute_error(y_true, y_pred))
    print("RMSE:", mean_squared_error(y_true, y_pred, squared=False))
    print("MAPE:", mean_absolute_percentage_error(y_true, y_pred))

if __name__ == "__main__":
    train()
