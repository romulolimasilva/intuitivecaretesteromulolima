import pandas as pd
import os
from tabula import read_pdf
import zipfile

print("Iniciando a extração de dados do PDF...")

# Transformar os dados em um arquivo CSV
transf_dados = "C:\\ADS Desenvolve\\Teste Seleção\\caredemo\\anexos\\Anexo_I.pdf"
output_dir = "C:\\ADS Desenvolve\\Teste Seleção\\caredemo\\transf_dados"

# Certifique-se de que o diretório de saída exista; caso contrário, crie-o
os.makedirs(output_dir, exist_ok=True)

print(f"Lendo o arquivo PDF: {transf_dados}")
try:
    # Extrair todas as tabelas do PDF
    tables = read_pdf(transf_dados, pages="all", lattice=True)
    print(f"Foram encontradas {len(tables)} tabelas no PDF")

    # Filtrar tabelas vazias e combinar todas as tabelas em um único DataFrame
    valid_tables = [table for table in tables if table.shape[0] > 0]
    print(f"Número de tabelas válidas: {len(valid_tables)}")
    
    if valid_tables:
        # Combinar todas as tabelas em um único DataFrame
        combined_table = pd.concat(valid_tables, ignore_index=True)
        
        # Salvar o DataFrame combinado em um único arquivo CSV
        output_file = os.path.join(output_dir, "anexo_I_completo.csv")
        combined_table.to_csv(output_file, index=False)
        print(f"\nArquivo CSV único criado com sucesso: {output_file}")
        print(f"Dimensões do arquivo final: {combined_table.shape[0]} linhas x {combined_table.shape[1]} colunas")

        # Compactação em ZIP
        zip_filename = os.path.join(output_dir, "romulo_lima.zip")
        try:
            with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
                # Adicionar apenas o arquivo CSV ao ZIP
                csv_name = "anexo_I_completo.csv"
                csv_path = os.path.join(output_dir, csv_name)
                zipf.write(csv_path, csv_name)
            print(f"Arquivo ZIP criado com sucesso em: {zip_filename}")
        except Exception as e:
            print(f"Erro ao criar arquivo ZIP: {e}")
    else:
        print("Nenhuma tabela válida encontrada no PDF")

    print("\nProcesso concluído com sucesso!")
    
except Exception as e:
    print(f"\nErro durante o processamento: {str(e)}")
