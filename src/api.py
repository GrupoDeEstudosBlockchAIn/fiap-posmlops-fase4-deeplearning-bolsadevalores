from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

def create_app(model_path, data_path):
    """
    Cria a aplicação FastAPI para servir o modelo.
    
    Args:
        model_path (str): Caminho do modelo treinado
        data_path (str): Caminho dos dados processados
    """
    app = FastAPI()
    
    # Carregar modelo e scaler
    model = load_model(model_path)
    data = np.load(data_path, allow_pickle=True)
    scaler = data['scaler'].item()  # <- essencial!
    
    class StockData(BaseModel):
        prices: list[float]
    
    @app.get("/")
    async def root():
        return {"message": "API de previsão de ações com LSTM. Use POST /predict"}

    @app.post("/predict")
    async def predict(data: StockData):
        try:
            # Validar entrada
            if len(data.prices) < 60:
                raise HTTPException(status_code=400, detail="É necessário fornecer pelo menos 60 preços históricos")
            
            # Preparar dados
            input_data = np.array(data.prices[-60:]).reshape(-1, 1)
            scaled_data = scaler.transform(input_data)
            X = scaled_data.reshape(1, 60, 1)
            
            # Fazer previsão
            prediction = model.predict(X)
            predicted_price = scaler.inverse_transform(prediction)[0][0]
            
            return {"predicted_price": float(predicted_price)}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    return app
