from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import os
from datetime import datetime
import logging

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

def carregar_resultados():
    """Carrega os resultados do arquivo CSV"""
    try:
        caminho_csv = os.path.abspath(os.path.join(os.path.dirname(__file__), 
                                                   '..', 'banco_de_dados', 'resultado_consulta.csv'))
        return pd.read_csv(caminho_csv)
    except Exception as e:
        logger.error(f"Erro ao carregar resultados: {str(e)}")
        raise

def carregar_resultados_trimestre():
    """Carrega os resultados do arquivo CSV do último trimestre"""
    try:
        caminho_csv = os.path.abspath(os.path.join(os.path.dirname(__file__), 
                                                   '..', 'banco_de_dados', 'resultado_consulta_trimestre.csv'))
        return pd.read_csv(caminho_csv)
    except Exception as e:
        logger.error(f"Erro ao carregar resultados do trimestre: {str(e)}")
        raise

@app.route('/api/top-operadoras/ano', methods=['GET'])
def consulta_ano():
    """Endpoint para consulta anual"""
    try:
        # Carregar resultados do CSV
        resultado = carregar_resultados()
        
        # Formatar o TOTAL_SINISTROS como moeda
        resultado['TOTAL_SINISTROS_FORMATADO'] = resultado['TOTAL_SINISTROS'].apply(
            lambda x: f'R$ {x:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.')
        )
        
        # Converter para o formato da API
        dados = []
        for _, row in resultado.iterrows():
            dados.append({
                'reg_ans': str(row['REG_ANS']),
                'total_sinistros': float(row['TOTAL_SINISTROS']),
                'total_sinistros_formatado': row['TOTAL_SINISTROS_FORMATADO'],
                'trimestres': row['TRIMESTRES_ANALISADOS'].split(', ')
            })
        
        return jsonify({
            'ano': 2024,
            'data': dados,
            'atualizado_em': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erro em consulta_ano: {str(e)}")
        return jsonify({'erro': 'Ocorreu um erro ao processar a requisição'}), 500

@app.route('/api/top-operadoras/trimestre', methods=['GET'])
def consulta_trimestre():
    """Endpoint para consulta do último trimestre"""
    try:
        # Carregar resultados do CSV
        resultado = carregar_resultados_trimestre()
        
        # Formatar o TOTAL_SINISTROS como moeda
        resultado['TOTAL_SINISTROS_FORMATADO'] = resultado['TOTAL_SINISTROS'].apply(
            lambda x: f'R$ {x:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.')
        )
        
        # Converter para o formato da API
        dados = []
        for _, row in resultado.iterrows():
            dados.append({
                'reg_ans': str(row['REG_ANS']),
                'total_sinistros': float(row['TOTAL_SINISTROS']),
                'total_sinistros_formatado': row['TOTAL_SINISTROS_FORMATADO'],
                'meses': row['MESES_ANALISADOS'].split(', ')
            })
        
        return jsonify({
            'ano': 2024,
            'trimestre': 4,
            'data': dados,
            'atualizado_em': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erro em consulta_trimestre: {str(e)}")
        return jsonify({'erro': 'Ocorreu um erro ao processar a requisição'}), 500

if __name__ == '__main__':
    app.run(debug=True)
