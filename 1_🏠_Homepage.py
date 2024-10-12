import streamlit as st
st.set_page_config(layout="centered")


# Título do aplicativo

st.title("MindMetric's ")
st.logo('icon.svg')

# Seção sobre
st.subheader('Sobre o aplicativo', divider='gray')
st.html("<div style='text-align: justify;'>O MindMetric's é uma plataforma de Dashboards que tem como foco, entregar um ambiente de visualização de dados acerca do tempo de tela em dispositivos eletrônicos e como isso pode afetar sua saúde mental.</div>")

# Link para visualizar dados na página de dashboards
st.page_link('./pages/2_📊_dashboards.py', label='Visualizar dados', icon='📊')

st.subheader('Sobre a Pesquisa', divider='gray')
st.html("<div style='text-align: justify;'>O MindMetric's é uma plataforma de Dashboards que tem como foco, entregar um ambiente de visualização de dados acerca do tempo de tela em dispositivos eletrônicos e como isso pode afetar sua saúde mental.</div>")