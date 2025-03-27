import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys

def carregar_dados():
    """Carrega os dados do CSV e processa conforme necessário."""
    try:
        # Caminho absoluto para o arquivo CSV
        caminho_csv = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'banco_de_dados', 'demonstracoes_contabeis.csv'))
        st.write(f"Tentando carregar arquivo de: {caminho_csv}")
        
        if not os.path.exists(caminho_csv):
            st.error(f"Arquivo não encontrado: {caminho_csv}")
            return None, None
            
        st.write("Arquivo encontrado! Tentando ler as primeiras linhas...")
        
        # Primeiro, vamos ler apenas algumas linhas para ver a estrutura
        df_sample = pd.read_csv(caminho_csv, nrows=5)
        st.write("Colunas disponíveis:")
        st.write(df_sample.columns.tolist())
        
        st.write("Amostra dos dados:")
        st.dataframe(df_sample)
        
        st.write("Carregando o arquivo completo...")
        # Agora vamos ler o arquivo completo
        df = pd.read_csv(caminho_csv)
        st.write(f"DataFrame carregado com sucesso! Dimensões: {df.shape}")
        
        # Verificar valores únicos em colunas importantes
        st.write("Anos disponíveis:", sorted(df['Ano'].unique()))
        st.write("Trimestres disponíveis:", sorted(df['Trimestre'].unique()))
        
        # Processar dados anuais
        st.write("Processando dados anuais...")
        df_anual = df[
            (df['Ano'] == 2024) & 
            (df['DESCRICAO'].str.contains('EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR', na=False))
        ].copy()
        
        st.write(f"Registros anuais encontrados: {len(df_anual)}")
        if len(df_anual) > 0:
            st.write("Exemplo de registro anual:")
            st.dataframe(df_anual.head(1))
        
        df_anual['VL_SALDO_FINAL'] = pd.to_numeric(df_anual['VL_SALDO_FINAL'].str.replace(',', '.'), errors='coerce')
        df_anual['REG_ANS'] = pd.to_numeric(df_anual['REG_ANS'], errors='coerce').astype('Int64')
        dados_anuais = df_anual.groupby('REG_ANS').agg({
            'VL_SALDO_FINAL': 'sum',
            'Trimestre': lambda x: sorted(list(x.unique()))
        }).reset_index()
        
        # Processar dados trimestrais
        st.write("Processando dados trimestrais...")
        df_trimestral = df[
            (df['Ano'] == 2024) & 
            (df['Trimestre'].isin([4])) & 
            (df['DESCRICAO'].str.contains('EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR', na=False))
        ].copy()
        
        st.write(f"Registros trimestrais encontrados: {len(df_trimestral)}")
        if len(df_trimestral) > 0:
            st.write("Exemplo de registro trimestral:")
            st.dataframe(df_trimestral.head(1))
        
        df_trimestral['VL_SALDO_FINAL'] = pd.to_numeric(df_trimestral['VL_SALDO_FINAL'].str.replace(',', '.'), errors='coerce')
        df_trimestral['REG_ANS'] = pd.to_numeric(df_trimestral['REG_ANS'], errors='coerce').astype('Int64')
        dados_trimestrais = df_trimestral.groupby('REG_ANS').agg({
            'VL_SALDO_FINAL': 'sum',
            'DATA': lambda x: sorted(list(x.unique()))
        }).reset_index()
        
        return dados_anuais, dados_trimestrais
        
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        import traceback
        st.error(f"Detalhes do erro:\n{traceback.format_exc()}")
        return None, None

def main():
    st.set_page_config(
        page_title="Dashboard ANS - Análise de Sinistros",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("Dashboard ANS - Análise de Sinistros")
    
    # Carregar dados
    dados_anuais, dados_trimestrais = carregar_dados()
    
    if dados_anuais is None or dados_trimestrais is None:
        st.error("Não foi possível carregar os dados. Verifique os logs acima.")
        return
    
    if len(dados_anuais) == 0:
        st.warning("Nenhum dado anual encontrado para o ano de 2024")
        return
        
    if len(dados_trimestrais) == 0:
        st.warning("Nenhum dado trimestral encontrado para o último trimestre de 2024")
        return
    
    # Criar duas colunas
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Análise Anual 2024")
        
        # Gráfico de barras para dados anuais
        fig_anual = px.bar(
            dados_anuais.sort_values('VL_SALDO_FINAL', ascending=False).head(10),
            x='REG_ANS',
            y='VL_SALDO_FINAL',
            title='Top 10 Operadoras por Valor Total de Sinistros (2024)',
            labels={'REG_ANS': 'Registro ANS', 'VL_SALDO_FINAL': 'Valor Total de Sinistros'}
        )
        # Formatando os valores no gráfico
        fig_anual.update_traces(
            text=dados_anuais.sort_values('VL_SALDO_FINAL', ascending=False).head(10)['VL_SALDO_FINAL'].apply(lambda x: f'R$ {x:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.')),
            textposition='auto'
        )
        fig_anual.update_layout(
            xaxis_title="Registro ANS",
            yaxis_title="Valor Total de Sinistros (R$)",
            yaxis_tickformat=',.2f'
        )
        st.plotly_chart(fig_anual, use_container_width=True)
        
        # Tabela de dados anuais
        st.subheader("Detalhes dos Dados Anuais")
        dados_anuais_formatados = dados_anuais.copy()
        dados_anuais_formatados['VL_SALDO_FINAL'] = dados_anuais_formatados['VL_SALDO_FINAL'].apply(
            lambda x: f'R$ {x:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.')
        )
        st.dataframe(
            dados_anuais_formatados.sort_values('VL_SALDO_FINAL', ascending=False)
            .head(10)
            .rename(columns={
                'REG_ANS': 'Registro ANS',
                'VL_SALDO_FINAL': 'Valor Total',
                'Trimestre': 'Trimestres Analisados'
            })
        )
    
    with col2:
        st.header("Análise do Último Trimestre 2024")
        
        # Gráfico de barras para dados trimestrais
        fig_trimestral = px.bar(
            dados_trimestrais.sort_values('VL_SALDO_FINAL', ascending=False).head(10),
            x='REG_ANS',
            y='VL_SALDO_FINAL',
            title='Top 10 Operadoras por Valor Total de Sinistros (Último Trimestre 2024)',
            labels={'REG_ANS': 'Registro ANS', 'VL_SALDO_FINAL': 'Valor Total de Sinistros'}
        )
        # Formatando os valores no gráfico
        fig_trimestral.update_traces(
            text=dados_trimestrais.sort_values('VL_SALDO_FINAL', ascending=False).head(10)['VL_SALDO_FINAL'].apply(lambda x: f'R$ {x:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.')),
            textposition='auto'
        )
        fig_trimestral.update_layout(
            xaxis_title="Registro ANS",
            yaxis_title="Valor Total de Sinistros (R$)",
            yaxis_tickformat=',.2f'
        )
        st.plotly_chart(fig_trimestral, use_container_width=True)
        
        # Tabela de dados trimestrais
        st.subheader("Detalhes dos Dados Trimestrais")
        dados_trimestrais_formatados = dados_trimestrais.copy()
        dados_trimestrais_formatados['VL_SALDO_FINAL'] = dados_trimestrais_formatados['VL_SALDO_FINAL'].apply(
            lambda x: f'R$ {x:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.')
        )
        st.dataframe(
            dados_trimestrais_formatados.sort_values('VL_SALDO_FINAL', ascending=False)
            .head(10)
            .rename(columns={
                'REG_ANS': 'Registro ANS',
                'VL_SALDO_FINAL': 'Valor Total',
                'DATA': 'Datas'
            })
        )

if __name__ == "__main__":
    main()