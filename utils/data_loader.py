import pandas as pd
import streamlit as st

@st.cache_data
def carregar_dados():
    return pd.read_excel('data/pesquisa.xlsx')