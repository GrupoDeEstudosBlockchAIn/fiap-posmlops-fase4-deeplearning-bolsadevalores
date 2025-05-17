# Dockerfile

# Imagem base leve com Python 3.12
FROM python:3.12-slim

# Variáveis de ambiente para evitar arquivos .pyc e saída não bufferizada
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Atualização do sistema e instalação de dependências necessárias
RUN apt-get update && apt-get install -y build-essential

# Criação e definição do diretório de trabalho
WORKDIR /app

# Copia os arquivos de dependência
COPY requirements.txt .

# Instala as dependências do projeto
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia todos os arquivos do projeto para o container
COPY . .

# Expor a porta da API
EXPOSE 8000

# Iniciar API com caminho explícito dos arquivos
CMD ["uvicorn", "src.api:create_app('models/lstm_model.keras','data/processed_data.npz')", "--factory", "--host", "0.0.0.0", "--port", "8000"]