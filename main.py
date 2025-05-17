import argparse
import numpy as np
import os
from src.data_collection import collect_stock_data
from src.data_preprocessing import preprocess_data
from src.model_training import build_and_train_model
from src.model_evaluation import evaluate_model
from src.api import create_app
import uvicorn
from datetime import datetime

def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def main():
    parser = argparse.ArgumentParser(description="Tech Challenge Fase 4: Previsão de preços de ações com LSTM")
    parser.add_argument('--mode', type=str, default='all', 
                        choices=['collect', 'preprocess', 'train', 'evaluate', 'api', 'all'],
                        help="Modo de execução: collect, preprocess, train, evaluate, api ou all")
    parser.add_argument('--ticker', type=str, default='AAPL', help="Símbolo da ação (ex: AAPL)")
    parser.add_argument('--start_date', type=str, default='2020-01-01', help="Data inicial (YYYY-MM-DD)")
    parser.add_argument('--end_date', type=str, default='2025-05-11', help="Data final (YYYY-MM-DD)")
    parser.add_argument('--epochs', type=int, default=50, help="Número de épocas para treinamento")
    parser.add_argument('--batch_size', type=int, default=32, help="Tamanho do lote para treinamento")
    parser.add_argument('--port', type=int, default=8000, help="Porta para a API")
    
    args = parser.parse_args()
    
    # Definir caminhos absolutos com base no diretório do main.py
    base_dir = os.path.dirname(os.path.abspath(__file__))
    raw_data_path = os.path.join(base_dir, "data", "raw_stock_data.csv")
    processed_data_path = os.path.join(base_dir, "data", "processed_data.npz")
    model_path = os.path.join(base_dir, "models", "lstm_model.keras")
    metric_path = os.path.join(base_dir, "metrics", "evaluation_metric.csv")
    
    try:
        # Executar conforme o modo
        if args.mode in ['collect', 'all']:
            log("Coletando dados...")
            collect_stock_data(args.ticker, args.start_date, args.end_date, raw_data_path)
        
        if args.mode in ['preprocess', 'all']:
            log("Pré-processando dados...")
            preprocess_data(raw_data_path, processed_data_path)
        
        if args.mode in ['train', 'all']:
            log("Treinando modelo...")
            data = np.load(processed_data_path)
            X_train, y_train = data['X_train'], data['y_train']
            build_and_train_model(X_train, y_train, model_path, epochs=args.epochs, batch_size=args.batch_size)
        
        if args.mode in ['evaluate', 'all']:
            log("Avaliando modelo...")
            evaluate_model(model_path, processed_data_path, metric_path)
        
        if args.mode in ['api', 'all']:
            log("Iniciando API...")
            app = create_app(model_path, processed_data_path)
            uvicorn.run(app, host="127.0.0.1", port=args.port)
    
    except Exception as e:
        log(f"Erro durante a execução: {e}")
        raise

if __name__ == "__main__":
    main()