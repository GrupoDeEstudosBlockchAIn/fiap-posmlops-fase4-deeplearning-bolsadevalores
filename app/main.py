from fastapi import FastAPI
from app.routes import router

app = FastAPI(title='Stock Price Predictor API')
app.include_router(router)
