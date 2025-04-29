import pandas as pd
from supabase import create_client, Client
import re
import streamlit as st
import numpy as np
from datetime import datetime
import uuid

# Carregar os dados do CSV ou DataFrame existente
df = pd.read_csv("tabela_historico.csv")

# Carregar objetos
df_objetos = pd.read_excel("./data/objetos.xlsx")

# Merge através do número do processo para trazer o objeto
df = pd.merge(df, df_objetos, on='Processo', how='left')

# Renomear colunas
df.rename(columns={'objeto': 'Objeto',
                   'Usuário': 'CPF'}, inplace=True)
# df_usuarios.rename(columns={'CPF1': 'CPF',
#                             'nome1': 'Nome'}, inplace=True)

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


# -----------------------------


# Filtrar o DataFrame para manter as linhas que contêm "remetido" ou "assinado"
df = df[df['Descrição'].str.contains(r'remetido|assinado', case=False, na=False)]
# df_andamento.drop(columns=['Órgao', 'data', 'id_nivel'], inplace=True)

# Exclui todas as linhas onde a coluna 'Documento' contém valores vazios
df = df.dropna(subset=['Documento'])

# Adiciona uma coluna id unica
df['id'] = [str(uuid.uuid4()) for _ in range(len(df))]

# Salvar o DataFrame atualizado em um novo arquivo CSV
df.to_csv(r'.\data\df.csv', index=False)
print(f"Arquivo atualizado salvo em: {r'./data/df.csv'}")
