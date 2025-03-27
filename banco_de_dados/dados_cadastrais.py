import pandas as pd
import os
import requests
from urllib.parse import urljoin

# URL base dos dados cadastrais
dados_cadastrais = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/"

# Criar o diretório se não existir
output_dir = "C:\\ADS Desenvolve\\Teste Seleção\\caredemo\\banco_de_dados"
temp_dir = os.path.join(output_dir, "temp")
os.makedirs(output_dir, exist_ok=True)
os.makedirs(temp_dir, exist_ok=True)

def baixar_dados_cadastrais():
    try:
        print("Baixando dados cadastrais...")
        
        # Montar URL completa do arquivo
        url_arquivo = urljoin(dados_cadastrais, "Relatorio_cadop.csv")
        
        # Baixar o arquivo
        response = requests.get(url_arquivo)
        response.raise_for_status()
        
        # Salvar temporariamente
        temp_file = os.path.join(temp_dir, "Relatorio_cadop.csv")
        with open(temp_file, 'wb') as f:
            f.write(response.content)
        
        # Ler o CSV
        df = pd.read_csv(temp_file, encoding='latin1', sep=';')
        
        # Selecionar e renomear colunas relevantes
        colunas_desejadas = {
            'Registro_ANS': 'Registro_ANS',
            'CNPJ': 'CNPJ',
            'Razao_Social': 'Razao_Social',
            'Nome_Fantasia': 'Nome_Fantasia',
            'Modalidade': 'Modalidade',
            'Logradouro': 'Logradouro',
            'Numero': 'Numero',
            'Complemento': 'Complemento',
            'Bairro': 'Bairro',
            'Cidade': 'Cidade',
            'UF': 'UF',
            'CEP': 'CEP',
            'DDD': 'DDD',
            'Telefone': 'Telefone',
            'Email': 'Email',
            'Data_Registro_ANS': 'Data_Registro_ANS'
        }
        
        # Verificar quais colunas existem no DataFrame
        colunas_existentes = {k: v for k, v in colunas_desejadas.items() if k in df.columns}
        
        # Selecionar apenas as colunas existentes
        df_final = df[list(colunas_existentes.keys())].copy()
        
        # Renomear as colunas
        df_final.rename(columns=colunas_existentes, inplace=True)
        
        # Formatar CNPJ (adicionar zeros à esquerda se necessário)
        if 'CNPJ' in df_final.columns:
            df_final['CNPJ'] = df_final['CNPJ'].astype(str).str.zfill(14)
            df_final['CNPJ'] = df_final['CNPJ'].str.replace(r'(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})', r'\1.\2.\3/\4-\5')
        
        # Formatar CEP
        if 'CEP' in df_final.columns:
            df_final['CEP'] = df_final['CEP'].astype(str).str.zfill(8)
            df_final['CEP'] = df_final['CEP'].str.replace(r'(\d{5})(\d{3})', r'\1-\2')
        
        # Formatar telefone
        if 'Telefone' in df_final.columns and 'DDD' in df_final.columns:
            df_final['Telefone'] = '(' + df_final['DDD'].astype(str) + ') ' + df_final['Telefone'].astype(str)
            df_final.drop('DDD', axis=1, inplace=True)
        
        # Salvar arquivo final
        output_file = os.path.join(output_dir, "dados_cadastrais.csv")
        df_final.to_csv(output_file, index=False)
        
        print(f"\nArquivo CSV criado com sucesso em: {output_file}")
        print("\nPrimeiras linhas do arquivo:")
        print(df_final.head())
        print(f"\nDimensões do arquivo: {df_final.shape[0]} linhas x {df_final.shape[1]} colunas")
        
        return df_final
        
    except Exception as e:
        print(f"\nErro durante o processamento: {str(e)}")
        return None
    
    finally:
        # Limpar arquivos temporários
        if os.path.exists(temp_dir):
            for file in os.listdir(temp_dir):
                os.remove(os.path.join(temp_dir, file))
            os.rmdir(temp_dir)

if __name__ == "__main__":
    df = baixar_dados_cadastrais()