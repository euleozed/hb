import pandas as pd
import streamlit as st
import os
from streamlit_extras.metric_cards import style_metric_cards
import plotly.express as px
import plotly.graph_objects as go

# Carregar arquivos
df_gecomp = pd.read_csv(r'./data/raw/producao_gecomp.csv',
                 usecols=['id_unidade', 'Documento1', 'protocolo_formatado', 'Nome', 'Ano', 'Mes'],
                 dtype={'protocolo_formatado': str})

df_gad = pd.read_csv(r'./data/raw/producao_gad.csv',
                 usecols=['id_unidade', 'Documento1', 'protocolo_formatado', 'Nome', 'Ano', 'Mes'],
                 dtype={'protocolo_formatado': str})

df_sc = pd.read_csv(r'./data/raw/producao_sc.csv',
                 usecols=['id_unidade', 'Documento1', 'protocolo_formatado', 'Nome', 'Ano', 'Mes'],
                 dtype={'protocolo_formatado': str})

# Concatenar arquivos

df = pd.concat([df_gecomp, df_gad, df_sc], ignore_index=True)

# Layout
st.set_page_config(page_title="Produção", layout='wide')
st.markdown("""<h1 style="text-align: center;">PRODUÇÃO DE DOCUMENTOS 2024📄</h1>""", unsafe_allow_html=True)
st.markdown("""<h6 style="text-align: center;">DADOS ATUALIZADOS DE JANEIRO A SETEMBRO</h6>""", unsafe_allow_html=True)
st.divider()

# Selecionar o setor
setor_selecionado = st.selectbox('Selecione o setor:', options=df['id_unidade'].unique().tolist())

# Filtro de Mês usando st.slider
mes_selecionado = st.slider('Selecione o intervalo de meses:', min_value=1, max_value=12, value=(1, 12))

# Filtrar os nomes com base no setor selecionado
nomes_filtrados = df[df['id_unidade'] == setor_selecionado]['Nome'].unique().tolist()

# Filtro de Nome usando st.multiselect, atualizando conforme o setor selecionado
df_nome_selecionado = st.multiselect('Selecione o Nome:', ['Tudo'] + sorted(nomes_filtrados), default='Tudo')

# Filtro por Mês
df_filtrado = df[(df['Mes'] >= mes_selecionado[0]) & (df['Mes'] <= mes_selecionado[1]) & (df['id_unidade'] == setor_selecionado)]

# Filtro por Nome
if 'Tudo' in df_nome_selecionado or not df_nome_selecionado:
    df_filtrado = df_filtrado  # Mostra todos os dados se "Tudo" estiver selecionado ou se nenhum nome for selecionado
else:
    df_filtrado = df_filtrado[df_filtrado['Nome'].isin(df_nome_selecionado)]



          
# MÉTRICAS
c1, c2, c3, c4 = st.columns(4)
style_metric_cards(background_color= 'rainbow')

qtd_documentos = df_filtrado['protocolo_formatado'].nunique()
qtd_servidores = df_filtrado['Nome'].nunique()
qtd_meses = df_filtrado['Mes'].nunique()

# Verifica se qtd_servidores é maior que 0 antes de dividir
if qtd_servidores > 0:
    media_docs_servidor = round(qtd_documentos / qtd_servidores, 2)
else:
    media_docs_servidor = 0  # Define como 0 ou outro valor padrão

# Média de documentos por mês para todos os nomes
df_mes = df_filtrado.groupby('Mes').agg(Media=('protocolo_formatado', 'count')).reset_index()
media_documentos_por_mes = qtd_documentos / qtd_meses

# Média de documentos por servidor
media_documentos_por_servidor = round(qtd_documentos / qtd_meses, 0)

# Média de documentos por servidor por mês
media_documentos_por_servidor_por_mes = round(media_documentos_por_mes / qtd_servidores, 0)


# Cards
c1.metric('Quantidade de Documentos:', qtd_documentos)
c2.metric('Quantidade de Servidores:', qtd_servidores)

if 'Tudo' in df_nome_selecionado:
    c3.metric(label='Média de Documentos por Mês:', value=round(media_documentos_por_mes, 0))
else:
    c3.metric(label='Média de Documentos do Servidor por Mês:', value=round(media_documentos_por_servidor, 0))

c4.metric(label='Média de Documentos por Servidor por Mês:', value=round(media_documentos_por_servidor_por_mes, 2))

# GRAFICO POR MÊS
df_mes = df_filtrado.groupby('Mes').agg(Quantidade=('protocolo_formatado', 'count')).reset_index()
fig2 = px.line(df_mes, x='Mes', y='Quantidade', text='Quantidade')
fig2.update_xaxes(tickformat='d')
fig2.update_traces(textposition="top center")
# st.markdown("""<h5 style="text-align: center;">Produção de Documentos por Mês</h5>""", unsafe_allow_html=True)
# st.plotly_chart(fig2)
st.divider()

# GRÁFICO POR TIPO DO DOCUMENTO
df_agrupado = df_filtrado.groupby(['Mes', 'Documento1']).agg(Quantidade=('protocolo_formatado', 'count')).sort_values(by='Quantidade', ascending=False).reset_index()
df_total_mes = df_agrupado.groupby('Mes').agg(Total_Quantidade=('Quantidade', 'sum')).reset_index()
fig3 = px.bar(df_agrupado, x='Mes', y='Quantidade', color='Documento1', barmode='group', text_auto=True)
fig3.update_layout(xaxis_title='Mês',
                   yaxis_title='Quantidade',
                   showlegend=True)
fig3.add_trace(go.Scatter(
    x=df_total_mes['Mes'], 
    y=df_total_mes['Total_Quantidade'], 
    mode='lines+markers+text',  # Adiciona a linha, marcadores e rótulos
    name='Total por Mês',
    line=dict(color='orange', width=3),
    marker=dict(size=8),
    text=df_total_mes['Total_Quantidade'].round(0),  # Rótulos com valores arredondados
    textposition='top center'  # Posição dos rótulos
))
fig3.update_xaxes(
    tickvals=df_total_mes['Mes'],  # Definir os valores do eixo x
    ticktext=df_total_mes['Mes']  # Formatar os meses
)
st.markdown("""<h5 style="text-align: center;">Comparativo de Documentos por Mês</h5>""",
    unsafe_allow_html=True
)
st.plotly_chart(fig3)
st.divider()


df_qtd_nome = df_filtrado.groupby('Nome').agg(Quantidade=('protocolo_formatado', 'count')).sort_values(by='Quantidade', ascending=False).reset_index()
st.markdown("""<h5 style="text-align: center;">Tabela de Quantidade de Tipos de Documentos por Mês</h5>""",
    unsafe_allow_html=True
)
# st.dataframe(df_agrupado, hide_index=True, width=1750)
# st.divider()

df_agrupado_nome = df_filtrado.groupby(['Documento1', 'Mes']).agg(Quantidade=('protocolo_formatado', 'count')).sort_values(by='Quantidade', ascending=False).reset_index()
# Usando pivot para transformar os meses em colunas
df_pivot = df_agrupado_nome.pivot(index='Documento1', columns='Mes', values='Quantidade').fillna(0)

# Convertendo os meses de volta para colunas
df_pivot.columns.name = None  # Remove o nome da coluna (Mes)
df_pivot = df_pivot.reset_index()


# Exibindo o DataFrame no Streamlit
st.dataframe(df_pivot, hide_index=True, width=1750)