from fabric import task
import pandas as pd
import os

@task
def collect_data(c):
    """Coleta dados e junta os arquivos CSV em um único."""
    # Execute seu script de web scraping aqui ou chame uma função
    os.system('python webscraping.py')

    # Junte todos os arquivos CSV
    csv_files = [f for f in os.listdir() if f.endswith('.csv')]
    df = pd.concat([pd.read_csv(f) for f in csv_files])
    df.to_csv('dados_juntos.csv', index=False)

@task
def process_data(c):
    """Tratamento dos dados."""
    # Execute seu script de tratamento de dados aqui ou chame uma função
    os.system('python pipeline.py')

@task
def deploy_streamlit(c):
    """Faz o deploy do app no Streamlit."""
    # Faça o git commit e push
    os.system('git add .')
    os.system('git commit -m "Atualizando o app Streamlit"')
    os.system('git push origin main')  # Altere para seu branch principal se necessário

    # Aqui você pode usar a API do Streamlit para fazer o deploy, se aplicável
    # Ou apenas abrir o Streamlit localmente
    c.run('streamlit run Home.py')  # Ou o caminho do seu app Streamlit

