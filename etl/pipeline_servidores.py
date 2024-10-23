import pandas as pd
import streamlit as st
import os


# 1 - ADD O NOME DO SERVIDOR NA TABELA
# Defina o caminho da pasta onde os arquivos .csv estão localizados
pasta = r'./data/raw/documentos_producao_gecomp'

# Lista todos os arquivos na pasta que terminam com .csv
arquivos_csv = [f for f in os.listdir(pasta) if f.endswith('.csv')]

# Itera sobre cada arquivo .csv
for arquivo in arquivos_csv:
    caminho_arquivo = os.path.join(pasta, arquivo)
    
    # Lê o arquivo .csv
    df = pd.read_csv(caminho_arquivo)
    
    # Extrai o nome do arquivo sem a extensão .csv
    nome_arquivo = os.path.splitext(arquivo)[0]
    
    # Adiciona a nova coluna "Nome" com o valor do nome do arquivo
    df['Nome'] = nome_arquivo
    
    # Salva o arquivo novamente, substituindo o original
    df.to_csv(caminho_arquivo, index=False)


# 2 - UNIR OS ARQUIVOS
# Definir o diretório onde os arquivos CSV estão armazenados
download_dir = r'./data/raw/documentos_producao_gecomp'
combined_csv_path = os.path.join(r'./data/raw', 'producao_gecomp.csv')

# Inicializar uma lista vazia para armazenar todos os DataFrames
lista_dfs = []

# Percorrer o diretório de downloads e carregar todos os arquivos CSV em DataFrames
for file_name in os.listdir(download_dir):
    if file_name.endswith('.csv'):
        file_path = os.path.join(download_dir, file_name)
        df = pd.read_csv(file_path)
        lista_dfs.append(df)

# Concatenar todos os DataFrames em um único DataFrame
df = pd.concat(lista_dfs, ignore_index=True)

# Salvar o DataFrame consolidado em um arquivo CSV
df.to_csv(combined_csv_path, index=False, encoding='utf-8')
print(f"Arquivo consolidado salvo em: {combined_csv_path}")

# ----------------------------------

# 1 - ADD O NOME DO SERVIDOR NA TABELA
# Defina o caminho da pasta onde os arquivos .csv estão localizados
pasta = r'./data/raw/documentos_producao_gad'

# Lista todos os arquivos na pasta que terminam com .csv
arquivos_csv = [f for f in os.listdir(pasta) if f.endswith('.csv')]

# Itera sobre cada arquivo .csv
for arquivo in arquivos_csv:
    caminho_arquivo = os.path.join(pasta, arquivo)
    
    # Lê o arquivo .csv
    df = pd.read_csv(caminho_arquivo)
    
    # Extrai o nome do arquivo sem a extensão .csv
    nome_arquivo = os.path.splitext(arquivo)[0]
    
    # Adiciona a nova coluna "Nome" com o valor do nome do arquivo
    df['Nome'] = nome_arquivo
    
    # Salva o arquivo novamente, substituindo o original
    df.to_csv(caminho_arquivo, index=False)


# 2 - UNIR OS ARQUIVOS
# Definir o diretório onde os arquivos CSV estão armazenados
download_dir = r'./data/raw/documentos_producao_gad'
combined_csv_path = os.path.join(r'./data/raw', 'producao_gad.csv')

# Inicializar uma lista vazia para armazenar todos os DataFrames
lista_dfs = []

# Percorrer o diretório de downloads e carregar todos os arquivos CSV em DataFrames
for file_name in os.listdir(download_dir):
    if file_name.endswith('.csv'):
        file_path = os.path.join(download_dir, file_name)
        df = pd.read_csv(file_path)
        lista_dfs.append(df)

# Concatenar todos os DataFrames em um único DataFrame
df = pd.concat(lista_dfs, ignore_index=True)

# Salvar o DataFrame consolidado em um arquivo CSV
df.to_csv(combined_csv_path, index=False, encoding='utf-8')
print(f"Arquivo consolidado salvo em: {combined_csv_path}")

# ----------------------------------------

# 1 - ADD O NOME DO SERVIDOR NA TABELA
# Defina o caminho da pasta onde os arquivos .csv estão localizados
pasta = r'./data/raw/documentos_producao_sc'

# Lista todos os arquivos na pasta que terminam com .csv
arquivos_csv = [f for f in os.listdir(pasta) if f.endswith('.csv')]

# Itera sobre cada arquivo .csv
for arquivo in arquivos_csv:
    caminho_arquivo = os.path.join(pasta, arquivo)
    
    # Lê o arquivo .csv
    df = pd.read_csv(caminho_arquivo)
    
    # Extrai o nome do arquivo sem a extensão .csv
    nome_arquivo = os.path.splitext(arquivo)[0]
    
    # Adiciona a nova coluna "Nome" com o valor do nome do arquivo
    df['Nome'] = nome_arquivo
    
    # Salva o arquivo novamente, substituindo o original
    df.to_csv(caminho_arquivo, index=False)


# 2 - UNIR OS ARQUIVOS
# Definir o diretório onde os arquivos CSV estão armazenados
download_dir = r'./data/raw/documentos_producao_sc'
combined_csv_path = os.path.join(r'./data/raw', 'producao_sc.csv')

# Inicializar uma lista vazia para armazenar todos os DataFrames
lista_dfs = []

# Percorrer o diretório de downloads e carregar todos os arquivos CSV em DataFrames
for file_name in os.listdir(download_dir):
    if file_name.endswith('.csv'):
        file_path = os.path.join(download_dir, file_name)
        df = pd.read_csv(file_path)
        lista_dfs.append(df)

# Concatenar todos os DataFrames em um único DataFrame
df = pd.concat(lista_dfs, ignore_index=True)

# Salvar o DataFrame consolidado em um arquivo CSV
df.to_csv(combined_csv_path, index=False, encoding='utf-8')
print(f"Arquivo consolidado salvo em: {combined_csv_path}")