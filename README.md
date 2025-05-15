# Tech Challenge Fase 4

Este projeto implementa um modelo LSTM para prever preços de fechamento de ações, com uma API RESTful para servir as previsões.

## Estrutura do Projeto

fiap-posmlops-fase4-deeplearning/
├── src/
│   ├── data_collection.py        # Script para coletar dados
│   ├── data_preprocessing.py     # Script para pré-processamento
│   ├── model_training.py         # Script para treinamento do modelo LSTM
│   ├── model_evaluation.py       # Script para avaliação do modelo
│   ├── api.py                    # API RESTful com FastAPI
├── main.py                       # Script principal que orquestra a execução
├── Dockerfile                    # Arquivo para contêiner Docker
├── README.md                     # Documentação do projeto
├── requirements.txt              # Dependências do projeto
├── models/                       # Pasta para salvar o modelo treinado
├── data/                         # Pasta para salvar dados brutos e processados
└── reports/                      # Pasta para relatórios de desempenho

## Como Executar
1. Instale as dependências:
   ```bash
   pip install -r src/requirements.txt