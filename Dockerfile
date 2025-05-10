# Dockerfile para servir o modelo LSTM via FastAPI
FROM python:3.10-slim

WORKDIR /app

# Copiar os arquivos necessários
COPY . /app

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta da API
EXPOSE 8000

# Comando para iniciar a API
CMD ["uvicorn", "interface.api:app", "--host", "0.0.0.0", "--port", "8000"]
