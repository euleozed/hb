import smtplib
from datetime import datetime
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders


# Carregar arquivos
df = pd.read_csv(r'./data/processed/df_andamento.csv',
                 dtype={'Usuário': str,
                        'Protocolo': str},
                 parse_dates=['Data/Hora'])

df_objeto = pd.read_excel(r'./data/database/objetos.xlsx')

# Ordenando o DataFrame pelo número do processo e pela data
df = df.sort_values(by=['Processo', 'Data/Hora']).reset_index(drop=True)

# Converter a coluna 'Data/Hora' para datetime
df['Data/Hora'] = pd.to_datetime(df['Data/Hora'])

# Mesclar df e df_objeto com base na coluna 'Processo'
df_combinado = pd.merge(df, df_objeto, on='Processo', how='inner')
df_combinado.info()

# Para encontrar o registro mais recente de cada processo
df_atrasados = df_combinado.loc[df_combinado.groupby('Processo')['Data/Hora'].idxmax()]

# Selecionar apenas as colunas necessárias
df_atrasados = df_atrasados[['Processo', 'objeto', 'Data/Hora', 'Documento']].reset_index(drop=True)
df_atrasados = df_atrasados.rename(columns={'Data/Hora': 'Data da Última Movimentação'})

# Converter a coluna 'Data da Última Movimentação' para datetime
df_atrasados['Data da Última Movimentação'] = pd.to_datetime(df_atrasados['Data da Última Movimentação'], format='%Y-%m-%d')

# Obter a data de hoje
data_hoje = datetime.now()

# Calcular a diferença de dias entre 'Data da Última Movimentação' e a data de hoje
df_atrasados['Dias desde a Última Movimentação'] = (data_hoje - df_atrasados['Data da Última Movimentação']).dt.days

# Formatar a data no formato dd-mm-aaaa
df_atrasados['Data da Última Movimentação'] = df_atrasados['Data da Última Movimentação'].dt.strftime('%d-%m-%Y')

# Ordenando os processos pelo número de dias desde a última movimentação
df_atrasados = df_atrasados.sort_values(by='Dias desde a Última Movimentação', ascending=False)

# tabela andamento de processos com +15 e -50 dias
df_andamento = df_atrasados[(df_atrasados['Dias desde a Última Movimentação'] <= 50) & (df_atrasados['Dias desde a Última Movimentação'] > 15)]


# Criar filtros para os diferentes grupos de processos
mais_300_dias = df_atrasados[(df_atrasados['Dias desde a Última Movimentação'] >= 300)].shape[0]
mais_200_dias = df_atrasados[(df_atrasados['Dias desde a Última Movimentação'] >= 200) & (df_atrasados['Dias desde a Última Movimentação'] < 300)].shape[0]
mais_100_dias = df_atrasados[(df_atrasados['Dias desde a Última Movimentação'] >= 100)  & (df_atrasados['Dias desde a Última Movimentação'] < 200)].shape[0]
mais_50_dias = df_atrasados[(df_atrasados['Dias desde a Última Movimentação'] >= 50)  & (df_atrasados['Dias desde a Última Movimentação'] < 100)].shape[0]

print(f"Processos com +300: {mais_300_dias}")
print(f"Processos com +200: {mais_300_dias}")
print(f"Processos com +100: {mais_300_dias}")
print(f"Processos com +500: {mais_300_dias}")

print("Tabela de processos")
print(df_atrasados)



# Configurações do email
email_de = 'fenix.gadsesau@gmail.com'
email_para = 'leozed92@gmail.com'
senha = 'dgma rgoh ghis mbav'


# Criando a mensagem do email
msg = MIMEMultipart()
msg['From'] = email_de
msg['To'] = email_para
msg['Subject'] = 'Notificação GECOMP - Processos +15d'

# Corpo do email com as métricas
corpo = f'''Bom dia, Gestores! 

Abaixo o quantitativo de processos sem movimentação:

- Processos com +300 dias: {mais_300_dias}
- Processos com +200 dias: {mais_200_dias}
- Processos com +100 dias: {mais_100_dias}
- Processos com +50 dias: {mais_50_dias}

Na tabela abaixo, são apresentados os processos que não são movimentados entre 15 e 50 dias.

Respeitosamente, 
GECOMP-SESAU'''

# Converte o DataFrame para uma tabela HTML
# tabela_html = df_atrasados.to_html(index=False)
tabela_html_andamento = df_andamento.to_html(index=False)

# Anexa o corpo do email e a tabela ao email
msg.attach(MIMEText(corpo, 'plain'))
msg.attach(MIMEText(tabela_html_andamento, 'html'))

# Enviando o email
try:
    with smtplib.SMTP('smtp.gmail.com', 587) as servidor:
        servidor.starttls()
        servidor.login(email_de, senha)
        servidor.sendmail(email_de, email_para, msg.as_string())
    print('Email enviado com sucesso!')
except Exception as e:
    print(f'Erro ao enviar email: {e}')