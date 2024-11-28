import streamlit as st

def main():
    st.set_page_config(layout="centered", page_title="MindMetric's")
    st.logo('./assets/icon.svg')

    st.header("MindMetric's", divider='gray')
    st.html("<div style='text-align: justify;'> É uma plataforma de Dashboards que tem como foco, entregar um ambiente de visualização de dados acerca do tempo de tela em dispositivos eletrônicos e como isso pode afetar sua saúde mental.</div>")
    st.page_link('./pages/Dashboards.py', label='Visualizar dados', icon='📊')
    
    tab1, tab2 = st.tabs(["Pesquisa", "Dados"])
    with tab1:
        st.subheader('Sobre a Pesquisa')
        st.html("<div style='text-align: justify;'>A ascensão exponencial da tecnologia digital trouxe consigo uma profunda integração das telas em diversos âmbitos da vida cotidiana. Desde o uso extensivo de smartphones e computadores até a imersão em redes sociais e entretenimento digital, as telas se tornaram uma parte integral da experiência humana. A partir disso, o aumento no tempo de tela e na conectividade constante também levanta preocupações significativas sobre os impactos na saúde mental. Nesse contexto, a pesquisa que originou o MindMetric's tem como objetivo investigar o impacto do uso de telas na saúde mental e no bem-estar das pessoas.</div>")

    with tab2:
        st.subheader('Como arrecadamos os dados')
        col1, col2 = st.columns([4, 1], gap='large', vertical_alignment='center')
        with col1:
            st.html("<div style='text-align: justify;'>Os dados foram arrecados por meio de uma pesquisa quantitativa, seguindo a práticas da lei geral de proteção de dados (LGPD), tratando as informações de maneira confidencial, usadas apenas para fins academicas, com 105 respondentes de faixa etária e gêneros variados. A coleta de dados se consentrou na identificação de comportamento de uso de dispositivos eletrônico e autoavaliações por parte dos respondentes. Dessa forma, é possível entender de maneira abrangente como os respondentes se relacionam com os impactos do uso de telas na saúde mental e no bem-estar.</div>")
        with col2:
            st.metric(label="Demográficos", value="", help="Faixa Etária | Gênero")
            st.metric(label="Uso de telas", value="", help="Frequência do uso de eletronicos | Quantidade de horas | Pricipais atividades")
            st.metric(label="Bem-estar", value="",help= "Estresse | Qualidade do sono | Avaliação no impacto das telas | Principais efeitos negativos")

if __name__ == "__main__":
    main()