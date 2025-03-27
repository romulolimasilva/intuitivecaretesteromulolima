import pandas as pd

print("Iniciando o processo de substituição...")

# Ler o arquivo CSV criado
input_file = "C:\\ADS Desenvolve\\Teste Seleção\\caredemo\\transf_dados\\anexo_I_completo.csv"
output_file = "C:\\ADS Desenvolve\\Teste Seleção\\caredemo\\transf_dados\\anexo_I_substituto.csv"

try:
    # Carregar o arquivo CSV
    print(f"\nLendo o arquivo: {input_file}")
    anexo_I = pd.read_csv(input_file)
    
    print("\nNomes das colunas:")
    print(anexo_I.columns.tolist())
    
    print("\nPrimeiras 5 linhas do arquivo original:")
    print(anexo_I.head())
    
    print("\nVerificando onde aparecem 'OD' e 'AMB' no arquivo...")
    for coluna in anexo_I.columns:
        valores_unicos = anexo_I[coluna].unique()
        if any('OD' in str(v) or 'AMB' in str(v) for v in valores_unicos):
            print(f"\nValores únicos na coluna {coluna}:")
            print(valores_unicos)
    
    print("\nRealizando substituições...")
    # Substitua as abreviações das colunas OD e AMB pelas descrições completas
    anexo_I = anexo_I.replace({
        "OD": "Seg. Odontológica",
        "AMB": "Seg. Ambulatorial"
    })
    
    # Salvar o arquivo CSV com o nome "anexo_I_substituto.csv"
    print(f"\nSalvando arquivo: {output_file}")
    anexo_I.to_csv(output_file, index=False)
    
    print(f"\nProcesso concluído com sucesso!")
    print(f"Arquivo salvo em: {output_file}")
    print(f"Dimensões do arquivo: {anexo_I.shape[0]} linhas x {anexo_I.shape[1]} colunas")

except Exception as e:
    print(f"\nErro durante o processamento: {str(e)}")
