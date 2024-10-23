import pandas as pd
import re
import streamlit as st
import numpy as np
from datetime import datetime
from unidecode import unidecode

# Configurações da página
st.set_page_config(page_title='Pipeline', layout='wide', page_icon='⚒️')

# Carregar os dados do CSV ou DataFrame existente
df = pd.read_csv(r"C:\Users\00840207255\OneDrive - Minha Empresa\Aplicativos\BANCO DADOS HB\raw\tabela_historico.csv")
df_usuarios = pd.read_csv(r"C:\Users\00840207255\OneDrive - Minha Empresa\Aplicativos\BANCO DADOS HB\raw\tabela_servidores.csv")
df_objetos = pd.read_excel(r"C:\Users\00840207255\OneDrive - Minha Empresa\Aplicativos\App Timeline HB\data\objetos.xlsx")

# Definir tipo string
df['Usuário'] = df['Usuário'].astype(str)
df_usuarios['CPF1'] = df_usuarios['CPF1'].astype(str)

# Renomear colunas

df.rename(columns={'numero_processo': 'Processo',
                   'Usuário': 'CPF'}, inplace=True)
df_usuarios.rename(columns={'CPF1': 'CPF',
                            'nome1': 'Nome'}, inplace=True)

# Substituir '/' por '-' na coluna 'Data/Hora'
df['Data/Hora'] = df['Data/Hora'].str.replace('/', '-')

# # Separar a data e a hora, mantendo apenas a data
# df['Data/Hora'] = df['Data/Hora'].str.split(' ').str[0]

# Converter a coluna 'Data/Hora' para formato datetime
df['Data/Hora'] = pd.to_datetime(df['Data/Hora'], format='%d-%m-%Y %H:%M')

# Função para extrair o Protocolo e o nome do documento
def extrair_texto(descricao):
    # Expressão regular para extrair o protocolo (sequência de dígitos)
    protocolo = re.search(r'Documento (\d+)', descricao)
    
    # Expressão regular para extrair o nome do documento (conteúdo entre parênteses)
    documento = re.search(r'\((.*?)\)', descricao)
    
    # Expressão regular para identificar a movimentação e capturar a descrição completa
    movimentacao = re.search(r'\b(remetido)\b(.*?)(?=\s*\Z)', descricao)  # Captura tudo após "remetido" até o fim da linha
    
    # Se movimentação for encontrada, usamos ela
    if movimentacao:
        # Captura o texto completo da movimentação
        movimentacao_texto = movimentacao.group(0)
        return (protocolo.group(1) if protocolo else None, movimentacao_texto.strip())
    
    # Caso contrário, retornamos o nome do documento normal
    elif protocolo and documento:
        return protocolo.group(1), documento.group(1)
    
    return None, None

# Supondo que você tenha um DataFrame 'df' com a coluna 'Descrição'
df['Protocolo'], df['Documento'] = zip(*df['Descrição'].apply(extrair_texto))


# Merge através do cpf do usuário
df = pd.merge(df, df_usuarios, on='CPF', how='left')


# ------------------------------

# Filtrar o DataFrame para manter as linhas que contém "homologação"
df_tabela_homologados = df[df['Descrição'].str.contains(r'homologação', case=False, na=False)]

# Filtrar o DataFrame para manter as linhas que contém "encerramento"
df_encerrados = df[df['Descrição'].str.contains(r'encerramento', case=False, na=False)]

# definir a lista de processos que serão retirados da tabela histórico
lista_homologados = df_tabela_homologados['Processo'].unique()
lista_encerrados = df_encerrados['Processo'].unique()

# ANDAMENTO
# Filtrar o DataFrame excluindo processos que estão em 'lista_homologados' e 'lista_encerrados'
df_andamento = df[~df['Processo'].isin(lista_homologados) & ~df['Processo'].isin(lista_encerrados)]


# Filtrar o DataFrame para manter as linhas que contêm "remetido" ou "assinado"
df_andamento = df_andamento[df_andamento['Descrição'].str.contains(r'remetido|assinado', case=False, na=False)]
df_andamento.drop(columns=['Órgao', 'data', 'id_nivel'], inplace=True)

# Exclui todas as linhas onde a coluna 'Documento' contém valores vazios
df_andamento = df_andamento.dropna(subset=['Documento'])

# Salvar o DataFrame atualizado em um novo arquivo CSV
df_andamento.to_csv(r'C:\Users\00840207255\OneDrive - Minha Empresa\Aplicativos\App Timeline HB\data\df_andamento.csv', index=False)
df_andamento