import requests
import os
import zipfile
import shutil  # Para verificar se o RAR está instalado

# URL da página onde os anexos estão localizados
capturar_anexos = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

# 01 - Download dos Anexos I e II em formato PDF
print("\n01 - Download dos Anexos I e II em formato PDF:")

# Lista de anexos para download
anexos = {
    "Anexo_I.pdf": "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf",
    "Anexo_II.pdf": "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_II_DUT_2021_RN_465.2021_RN628.2025_RN629.2025.pdf"
}

# Cria diretório para os downloads se não existir
os.makedirs("anexos", exist_ok=True)

# Faz o download de cada anexo
for nome_arquivo, url in anexos.items():
    print(f"Baixando {nome_arquivo}...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        caminho_arquivo = os.path.join("anexos", nome_arquivo)
        with open(caminho_arquivo, "wb") as f:
            f.write(response.content)
        print(f"{nome_arquivo} baixado com sucesso!")
    except Exception as e:
        print(f"Erro ao baixar {nome_arquivo}: {e}")

# 02 - Compactação de todos os anexos
print("\n02 - Compactação de todos os anexos:")

# Compactação em ZIP
zip_filename = "anexos_compactados.zip"
try:
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk("anexos"):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, "anexos"))
    print(f"Arquivo {zip_filename} criado com sucesso!")
except Exception as e:
    print(f"Erro ao criar arquivo ZIP: {e}")

# Compactação em RAR (se o WinRAR estiver instalado)
rar_filename = "anexos_compactados.rar"
if shutil.which("rar"):
    try:
        os.system(f'rar a "{rar_filename}" "anexos\\*"')
        print(f"Arquivo {rar_filename} criado com sucesso!")
    except Exception as e:
        print(f"Erro ao criar arquivo RAR: {e}")
else:
    print("WinRAR não encontrado. A compactação em RAR não foi realizada.")

print("\nProcesso concluído!")