# Lógica de previsão usando modelo salvo
import numpy as np
import joblib
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

def predict_next_value(last_sequence):
    """
    Faz a predição do próximo valor a partir da última sequência de fechamento normalizada.
    last_sequence deve ser um array numpy com shape (window_size, 1)
    ALEX
    """
    model = load_model("models/lstm_model.h5")
    scaler = joblib.load("data/scaler.pkl")

    # Verificar e ajustar a forma da sequência
    if len(last_sequence.shape) == 2:
        last_sequence = np.expand_dims(last_sequence, axis=0)  # (1, window_size, 1)

    prediction = model.predict(last_sequence)
    predicted_price = scaler.inverse_transform(prediction)

    return predicted_price[0][0]

if __name__ == "__main__":
    # Exemplo de uso
    dummy_sequence = np.random.rand(60, 1)  # Sequência fictícia
    valor_previsto = predict_next_value(dummy_sequence)
    print(f"Valor previsto: {valor_previsto:.2f}")

