import os
from jinja2 import Template

def generate_html_report(metric_dict, output_path="metrics/report.html"):
    """
    Gera um relatório HTML formatado com base nas métricas fornecidas.

    Args:
        metric_dict (dict): Dicionário contendo métricas (MAE, RMSE, MAPE).
        output_path (str): Caminho para salvar o relatório HTML.
    """
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        html_template = """
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <title>Relatório de Avaliação do Modelo</title>
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background-color: #f4f6f8;
                    padding: 40px;
                    color: #333;
                }
                h1 {
                    color: #2c3e50;
                    text-align: center;
                }
                .container {
                    background-color: white;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }
                th, td {
                    padding: 15px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }
                th {
                    background-color: #3498db;
                    color: white;
                }
                .footer {
                    text-align: center;
                    font-size: 0.9em;
                    margin-top: 30px;
                    color: #aaa;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Relatório de Avaliação do Modelo</h1>
                <table>
                    <tr>
                        <th>Métrica</th>
                        <th>Valor</th>
                    </tr>
                    {% for key, value in metric.items() %}
                    <tr>
                        <td>{{ key }}</td>
                        <td>{{ "%.4f"|format(value) }}</td>
                    </tr>
                    {% endfor %}
                </table>
                <div class="footer">
                    Projeto Tech Challenge - Fase 4 • Previsão de Preços de Ações com LSTM
                </div>
            </div>
        </body>
        </html>
        """

        template = Template(html_template)
        html_content = template.render(metric=metric_dict)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"Relatório HTML salvo com sucesso em: {output_path}")
    except Exception as e:
        print(f"Erro ao gerar relatório HTML: {e}")
