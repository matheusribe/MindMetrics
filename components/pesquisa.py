import streamlit as st
import plotly.express as px

def mostrar_pesquisa(df):
    col1, col2 = st.columns([3,2], gap='large', vertical_alignment='top')
    with col1:
        st.metric(label="Respostas", value="104", help="Quantidade de respostas que a pesquisa obteve")
        st.write("##### Quadro geral de respostas")
        st.dataframe(df)
    with col2:
        fig = px.pie(df, names='faixa_etaria', color_discrete_sequence=px.colors.sequential.RdBu, title="Faixa Etária")
        st.plotly_chart(fig)