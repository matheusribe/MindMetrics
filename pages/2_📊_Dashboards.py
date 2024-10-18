import streamlit as st
from utils.data_loader import carregar_dados
from utils.data_processing import processar_dados_correlacao
from components.pesquisa import mostrar_pesquisa
from components.correlacoes import mostrar_correlacoes

def main():
    st.set_page_config(layout="wide", page_title="MindMetric's")
    st.logo('./assets/icon.svg')

    # Carregando e processando dados
    df = carregar_dados()
    df = processar_dados_correlacao(df)

    # Sidebar e Menu
    st.sidebar.title('Menu')
    pagina_dashboard = st.sidebar.selectbox('Selecione uma opção:', ['Pesquisa', 'Correlações'])

    if pagina_dashboard == 'Pesquisa':
        mostrar_pesquisa(df)
    elif pagina_dashboard == 'Correlações':
        mostrar_correlacoes(df)

if __name__ == "__main__":
    main()