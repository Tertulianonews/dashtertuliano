import pandas as pd
import pandas_datareader.data as web
import datetime as dt
import streamlit as st
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

st.set_page_config(page_title="Dashboard Financeiro",layout="wide")
st.title('Dashboard Financeiro para a família de Deus')
st.title('Tertuliano')

end_date = dt.datetime.today()
start_date = dt.datetime(end_date.year-1,end_date.month,end_date.day)

with st.container():
    st.header('Insira as informações solicitadas abaixo:')

    col1, col2, col3 = st.columns(3)

    with col1:
        ativo = st.selectbox('Selecione o ativo desejado:', options=['PETR4.SA','VALE3.SA','BOVA11.SA','ITSA4.SA','BTC-USD'])
    with col2:
        data_inicial = st.date_input('Selecione a data inicial:',start_date)
    with col3:
        data_final = st.date_input('Selecione a data final:', end_date)

#Retornar as informações da API
df = web.DataReader(name=ativo, data_source='yahoo',start=data_inicial, end=data_final)
df.index = df.index.date

#Criar métricas

ult_atualizacao = df.index.max()
ult_cotacao = round(df.loc[df.index.max(),'Adj Close'],2)#Última cotação encontrada
menor_cotacao = round(df['Adj Close'].min(),2) #Menor cotação do período.
maior_cotacao = round(df['Adj Close'].max(),2) #Maior cotação do período.
prim_cotacao = round(df.loc[df.index.min(),'Adj Close'],2)#Última cotação encontrada
delta = round(((ult_cotacao-prim_cotacao)/prim_cotacao)*100,2)#Variação da cotação no período.

with st.container():
    with col1:
        st.metric(f"Última atualização - {ult_atualizacao}","R$ {:,.2f}".format(ult_cotacao),f"{delta}%")
    with col2:
        st.metric(f"Menor cotação do período - {ult_atualizacao}","R$ {:,.2f}".format(menor_cotacao))
    with col3:
        st.metric(f"Maior cotação do período - {ult_atualizacao}","R$ {:,.2f}".format(maior_cotacao))

# As linhas abaixo irão apresentar o dataframe na tela da página web
with st.container():
   st.area_chart(df[['Adj Close']])
   st.line_chart(df[['Low','Adj Close','High']])

if __name__ == '__main__':
    app.run_server(debug=True)
#print(dt.head(5))

