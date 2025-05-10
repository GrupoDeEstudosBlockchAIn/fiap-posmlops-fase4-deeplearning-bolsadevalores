from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
from core import predict

app = FastAPI(title="Stock Price Predictor API")

class PriceSequence(BaseModel):
    sequence: list[float]  # Lista com os últimos 60 preços normalizados

@app.post("/predict")
def get_prediction(data: PriceSequence):
    if len(data.sequence) != 60:
        raise HTTPException(status_code=400, detail="A sequência deve conter exatamente 60 valores.")

    try:
        sequence_array = np.array(data.sequence).reshape((60, 1))
        predicted_price = predict.predict_next_value(sequence_array)
        return {"predicted_price": round(predicted_price, 2)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
