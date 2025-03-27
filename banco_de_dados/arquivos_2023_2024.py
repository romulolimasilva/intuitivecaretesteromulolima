import pandas as pd
import os
import requests
import zipfile
from urllib.parse import urljoin

# Diretórios de origem
url_2023 = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2023/"
url_2024 = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2024/"

# Criar o diretório se não existir
output_dir = "C:\\ADS Desenvolve\\Teste Seleção\\caredemo\\banco_de_dados"
temp_dir = os.path.join(output_dir, "temp")
os.makedirs(output_dir, exist_ok=True)
os.makedirs(temp_dir, exist_ok=True)

def ler_csv_com_encoding(arquivo):
    """Tenta ler um arquivo CSV com diferentes encodings e separadores"""
    for encoding in ['utf-8', 'latin1', 'cp1252']:
        try:
            for sep in [';', ',']:
                try:
                    df = pd.read_csv(arquivo, encoding=encoding, sep=sep)
                    print(f"Sucesso! Usando encoding={encoding} e separador={sep}")
                    return df
                except:
                    continue
        except:
            continue
    return None

def baixar_e_extrair_zip(url, trimestre, ano):
    try:
        print(f"Baixando dados do {trimestre}º trimestre de {ano}...")
        response = requests.get(url)
        response.raise_for_status()
        
        zip_path = os.path.join(temp_dir, f"{trimestre}T{ano}.zip")
        with open(zip_path, 'wb') as f:
            f.write(response.content)
        
        dataframes = []
        with zipfile.ZipFile(zip_path) as zip_ref:
            csv_files = [f for f in zip_ref.namelist() if f.lower().endswith('.csv')]
            
            for csv_file in csv_files:
                try:
                    print(f"Processando arquivo: {csv_file}")
                    with zip_ref.open(csv_file) as f:
                        # Salvar temporariamente o arquivo CSV para poder usar o ler_csv_com_encoding
                        temp_csv = os.path.join(temp_dir, "temp.csv")
                        with open(temp_csv, 'wb') as temp_f:
                            temp_f.write(f.read())
                        
                        df = ler_csv_com_encoding(temp_csv)
                        if df is not None:
                            # Adicionar colunas de identificação
                            df['Ano'] = ano
                            df['Trimestre'] = trimestre
                            dataframes.append(df)
                        
                        os.remove(temp_csv)
                            
                except Exception as e:
                    print(f"Erro ao processar arquivo {csv_file}: {str(e)}")
                    continue
        
        os.remove(zip_path)
        return dataframes
        
    except Exception as e:
        print(f"Erro ao processar {trimestre}T{ano}: {str(e)}")
        if os.path.exists(zip_path):
            os.remove(zip_path)
        return []

def processar_ano(url_base, ano):
    print(f"\nProcessando dados de {ano}...")
    dados_ano = []
    
    for trimestre in range(1, 5):
        zip_url = urljoin(url_base, f"{trimestre}T{ano}.zip")
        dfs_trimestre = baixar_e_extrair_zip(zip_url, trimestre, ano)
        dados_ano.extend(dfs_trimestre)
    
    return dados_ano

try:
    print("Iniciando download e extração dos arquivos...")
    
    # Processar dados de cada ano
    dfs_2023 = processar_ano(url_2023, 2023)
    dfs_2024 = processar_ano(url_2024, 2024)
    
    # Juntar todos os DataFrames
    todos_dfs = dfs_2023 + dfs_2024
    
    if todos_dfs:
        # Concatenar todos os dados
        df_completo = pd.concat(todos_dfs, ignore_index=True)
        
        # Remover duplicatas se houver
        df_completo = df_completo.drop_duplicates()
        
        # Salvar arquivo final
        output_file = os.path.join(output_dir, "demonstracoes_contabeis.csv")
        df_completo.to_csv(output_file, index=False)
        print(f"\nArquivo CSV criado com sucesso em: {output_file}")
        print("\nPrimeiras linhas do arquivo:")
        print(df_completo.head())
        print(f"\nDimensões do arquivo: {df_completo.shape[0]} linhas x {df_completo.shape[1]} colunas")
    else:
        print("\nNão foi possível extrair dados de nenhum dos anos.")

except Exception as e:
    print(f"\nErro durante o processamento: {str(e)}")

finally:
    # Limpar arquivos temporários
    if os.path.exists(temp_dir):
        for file in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, file))
        os.rmdir(temp_dir)