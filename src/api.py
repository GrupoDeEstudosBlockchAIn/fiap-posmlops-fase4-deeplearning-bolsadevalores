import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
from tensorflow.keras.models import load_model
from fastapi.responses import RedirectResponse 
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app(model_path, data_path):
    """
    Cria a aplicação FastAPI para servir o modelo.
    
    Args:
        model_path (str): Caminho do modelo treinado
        data_path (str): Caminho dos dados processados
    """
    model_path = os.getenv("MODEL_PATH", "models/lstm_model.keras")
    data_path = os.getenv("DATA_PATH", "data/processed_data.npz")

    app = FastAPI()
    
    # Carregar modelo e scaler
    model = load_model(model_path)
    data = np.load(data_path, allow_pickle=True)
    scaler = data['scaler'].item()
    
    class StockData(BaseModel):
        prices: list[float]
    
    @app.get("/", include_in_schema=False)
    async def root():
        return RedirectResponse(url="/docs") 

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
            logger.error(f"Erro interno na predição: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    return app
