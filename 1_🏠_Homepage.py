import streamlit as st

def main():
    st.set_page_config(layout="centered", page_title="MindMetric's")
    st.title("MindMetric's")
    st.logo('./assets/icon.svg')

    st.subheader('Sobre o aplicativo', divider='gray')
    st.html("<div style='text-align: justify;'>O MindMetric's é uma plataforma de Dashboards que tem como foco, entregar um ambiente de visualização de dados acerca do tempo de tela em dispositivos eletrônicos e como isso pode afetar sua saúde mental.</div>")

    st.page_link('./pages/2_📊_dashboards.py', label='Visualizar dados', icon='📊')

    st.subheader('Sobre a Pesquisa', divider='gray')
    st.html("<div style='text-align: justify;'>A ascensão exponencial da tecnologia digital trouxe consigo uma profunda integração das telas em diversos âmbitos da vida cotidiana. Desde o uso extensivo de smartphones e computadores até a imersão em redes sociais e entretenimento digital, as telas se tornaram uma parte integral da experiência humana. A partir disso, o aumento no tempo de tela e na conectividade constante também levanta preocupações significativas sobre os impactos na saúde mental. Nesse contexto, a pesquisa que originou o MindMetric's tem como objetivo investigar o impacto do uso de telas na saúde mental e no bem-estar das pessoas.</div>")

if __name__ == "__main__":
    main()