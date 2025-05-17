import numpy as np
from tensorflow.keras.models import load_model
from sklearn.metrics import mean_absolute_error, mean_squared_error
import pandas as pd
import tensorflow as tf
import os
from .metric_report import generate_html_report

def evaluate_model(model_path, data_path, metric_path):
    """
    Avalia o modelo treinado e gera um relatório de desempenho.
    
    Args:
        model_path (str): Caminho do modelo treinado
        data_path (str): Caminho dos dados processados
        metric_path (str): Caminho para salvar o relatório
    """
    try:
        # Verificar se os arquivos existem
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Arquivo do modelo não encontrado: {model_path}")
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Arquivo de dados não encontrado: {data_path}")

        # Carregar modelo
        try:
            model = load_model(model_path)
        except Exception as e:
            raise ValueError(f"Erro ao carregar o modelo: {e}. Verifique se o arquivo {model_path} contém um modelo válido.")

        # Carregar dados
        data = np.load(data_path, allow_pickle=True)
        X_test, y_test, scaler = data['X_test'], data['y_test'], data['scaler'].item()
        
        # Fazer previsões
        predictions = model.predict(X_test)
        
        # Desnormalizar dados
        predictions = scaler.inverse_transform(predictions)
        y_test = scaler.inverse_transform(y_test)
        
        # Calcular métricas
        mae = mean_absolute_error(y_test, predictions)
        rmse = np.sqrt(mean_squared_error(y_test, predictions))
        mape = np.mean(np.abs((y_test - predictions) / y_test)) * 100
        
        # Criar relatório de métricas
        metric = {
            'MAE': mae,
            'RMSE': rmse,
            'MAPE': mape
        }
        
        # Salvar relatório de métricas
        os.makedirs(os.path.dirname(metric_path), exist_ok=True)
        generate_html_report(metric, output_path=os.path.join(os.path.dirname(metric_path), "metric_report.html"))
        print(f"Relatório de métricas salvo em {metric_path}")
        
        return metric
    except Exception as e:
        print(f"Erro na avaliação: {e}")
        return None