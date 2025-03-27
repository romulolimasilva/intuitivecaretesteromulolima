import pandas as pd
from tabulate import tabulate
import os

def executar_consulta():
    try:
        # Caminho para o arquivo CSV
        caminho_csv = os.path.join(os.path.dirname(__file__), 'demonstracoes_contabeis.csv')
        
        # Primeiro, vamos ler o CSV diretamente com pandas
        df = pd.read_csv(caminho_csv)
        
        print("\nPrimeiras linhas do arquivo:")
        print(df.head())
        
        print("\nAnos disponíveis no arquivo:")
        print(sorted(df['Ano'].unique()))
        
        print("\nDescrições disponíveis:")
        print(df['DESCRICAO'].unique())
        
        # Filtrar registros de 2024
        df_2024 = df[
            (df['Ano'] == 2024) & 
            (df['DESCRICAO'].str.contains('EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR', na=False))
        ]
        
        # Converter VL_SALDO_FINAL para numérico
        df_2024['VL_SALDO_FINAL'] = pd.to_numeric(df_2024['VL_SALDO_FINAL'].str.replace(',', '.'), errors='coerce')
        
        # Agrupar e calcular os resultados
        resultado = df_2024.groupby('REG_ANS').agg({
            'VL_SALDO_FINAL': 'sum',
            'Trimestre': lambda x: ', '.join(sorted(x.astype(str).unique()))
        }).reset_index()
        
        # Renomear as colunas
        resultado.columns = ['REG_ANS', 'TOTAL_SINISTROS', 'TRIMESTRES_ANALISADOS']
        
        # Ordenar por TOTAL_SINISTROS e pegar os top 10
        resultado = resultado.sort_values('TOTAL_SINISTROS', ascending=False).head(10)
        
        # Criar uma cópia do DataFrame antes de formatar para salvar em CSV
        resultado_csv = resultado.copy()
        
        # Salvar em CSV antes da formatação para manter os valores numéricos
        caminho_csv = os.path.join(os.path.dirname(__file__), 'resultado_consulta.csv')
        resultado_csv.to_csv(caminho_csv, index=False)
        print(f"\nResultado salvo em: {caminho_csv}\n")
        
        # Formatar o TOTAL_SINISTROS como moeda para exibição
        resultado['TOTAL_SINISTROS'] = resultado['TOTAL_SINISTROS'].apply(
            lambda x: f'R$ {x:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.')
        )
        
        # Imprimir o resultado usando tabulate para melhor formatação
        print("\n=== TOP 10 OPERADORAS COM MAIORES SINISTROS EM 2024 ===\n")
        print(tabulate(resultado, headers='keys', tablefmt='grid', showindex=False))
        
    except Exception as e:
        print(f"Erro ao executar a consulta: {str(e)}")

if __name__ == "__main__":
    executar_consulta()
