# Dockerfile para servir o modelo LSTM via FastAPI
FROM python:3.10-slim

WORKDIR /app

# Copiar os arquivos necessários
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .
COPY models/ ./models/
COPY data/ ./data/

# Expor a porta da API
EXPOSE 8000

# Comando para iniciar a API
CMD ["uvicorn", "api:app", "--host", "127.0.0.1", "--port", "8000"]