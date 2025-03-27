# criar conteção com mysql

import mysql.connector
from mysql.connector import Error

def criar_conexao():
    try:
        # Estabelecer conexão com o MySQL
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root"
        )
        
        if conexao.is_connected():
            print("Conexão com MySQL estabelecida com sucesso!")
            return conexao
            
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

def criar_banco_se_nao_existe(conexao, nome_banco="demonstrativos"):
    try:
        if conexao and conexao.is_connected():
            cursor = conexao.cursor()
            
            # Criar banco de dados se não existir
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {nome_banco}")
            print(f"Banco de dados '{nome_banco}' criado/verificado com sucesso!")
            
            # Usar o banco de dados
            cursor.execute(f"USE {nome_banco}")
            print(f"Usando banco de dados: {nome_banco}")
            
            conexao.commit()
            return True
            
    except Error as e:
        print(f"Erro ao criar/verificar banco de dados: {e}")
        return False

def fechar_conexao(conexao):
    if conexao and conexao.is_connected():
        conexao.close()
        print("Conexão com MySQL fechada.")

# Exemplo de uso
if __name__ == "__main__":
    # Criar conexão
    conexao = criar_conexao()
    
    if conexao:
        # Criar banco de dados
        criar_banco_se_nao_existe(conexao)
        
        # Fechar conexão
        fechar_conexao(conexao)
