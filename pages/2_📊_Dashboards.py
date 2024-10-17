import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

# Título do aplicativo
st.set_page_config(layout="wide", page_title="MindMetric's")

# Logo 
st.logo('icon.svg')

### Importando os Dados ###
@st.cache_data
def carregar_dados():
    return pd.read_excel('data/pesquisa.xlsx')

df = carregar_dados()

### Sidebar e Menu ###
st.sidebar.title('Menu')
pagina_dashboard = st.sidebar.selectbox('Selecione uma opção:', ['Pesquisa', 'Correlações'])

### Pesquisa ###
col1, col2 = st.columns([3,2],gap='large',vertical_alignment='top')
if pagina_dashboard == 'Pesquisa':
    with col1:
        st.metric(label="Respostas", value="104", help="Quantidade de respostas que a pesquisa obteve")
        st.write("##### Quadro geral de respostas")
        st.dataframe(df)
    with col2:
        fig = px.pie(df, names='faixa_etaria', color_discrete_sequence=px.colors.sequential.RdBu,title="Faixa Etária")
        st.plotly_chart(fig)

### Correlações ###
elif pagina_dashboard == 'Correlações':
    ### Média de horas x Idade ###
    ### Convertendo os valores da coluna 'horas_dia'
    def converter_horas(valor):
        if pd.isna(valor):
            return None
        
        mapeamento = {
            'Menos de 1 hora': 0.5,
            '1 - 2 horas': 1.5,
            '3 - 4 horas': 3.5,
            '5 - 6 horas': 5.5,
            'Mais de 6 horas': 7
        }
        
        return mapeamento.get(valor, None)

    df['horas_dia_num'] = df['horas_dia'].apply(converter_horas)
    media_horas = df.groupby('faixa_etaria')['horas_dia_num'].mean().apply(lambda x: round(x, 2)).reset_index()

    ### Média de Horas x Qualidade do Sono ###
    media_sono = df.groupby('qualidade_sono_mes')['horas_dia_num'].mean().apply(lambda x: round(x, 2)).reset_index()

    ### Atividades vs Efeitos Negativos ###
    # Função para unificar as plataformas de streaming em uma única categoria "Streamings"
    def unificar_streaming(atividade):
        plataformas_streaming = ['Youtube', 'Netflix', 'Prime video', 'max', 'YouTube']
        return 'Streamings' if any(plataforma.lower() in atividade.lower() for plataforma in plataformas_streaming) else atividade

    # Filtrar atividades relevantes
    def filtrar_atividades(atividade):
        atividades_permitidas = ["Trabalho", "Estudo", "Redes Sociais", "Streamings", "Jogos"]
        return atividade in atividades_permitidas

    # Filtrar efeitos negativos relevantes
    def filtrar_efeitos(efeito):
        efeitos_permitidos = [
            "Insônia ou distúrbios do sono", 
            "Ansiedade", 
            "Depressão", 
            "Estresse", 
            "Isolamento social", 
            "Dificuldade de concentração"
        ]
        return efeito in efeitos_permitidos

    # Expandir as colunas de atividades e efeitos negativos
    def expandir_coluna(coluna_atividades, coluna_efeitos):
        atividades_lista = []
        efeitos_lista = []
        responsaveis_lista = []
        
        for i, (atividades, efeitos) in enumerate(zip(coluna_atividades, coluna_efeitos)):
            if pd.isna(atividades) or pd.isna(efeitos):
                continue
            lista_atividades = [unificar_streaming(atividade.strip()) for atividade in str(atividades).split(',')]
            lista_efeitos = [efeito.strip() for efeito in str(efeitos).split(',')]
            
            for atividade in lista_atividades:
                if filtrar_atividades(atividade):
                    for efeito in lista_efeitos:
                        if filtrar_efeitos(efeito):
                            atividades_lista.append(atividade)
                            efeitos_lista.append(efeito)
                            responsaveis_lista.append(i + 1)
                            
        return atividades_lista, efeitos_lista, responsaveis_lista

    # Expandir as colunas de atividades e efeitos negativos
    atividades_lista, efeitos_lista, responsaveis_lista = expandir_coluna(df['atividades'], df['efeitos_negativos'])

    # Criar um DataFrame com atividades e seus efeitos correspondentes
    df_correlacao = pd.DataFrame({
        'Atividade': atividades_lista,
        'Efeito_Negativo': efeitos_lista,
        'Responsavel': responsaveis_lista
    })

    # Remover duplicatas para contar cada combinação uma única vez por respondente
    df_correlacao = df_correlacao.drop_duplicates(subset=['Atividade', 'Efeito_Negativo', 'Responsavel'])

    # Contar as combinações de atividades e efeitos
    df_correlacao = df_correlacao.groupby(['Atividade', 'Efeito_Negativo']).size().reset_index(name='Frequência')

    # Filtrar para manter apenas os efeitos negativos que têm atividades associadas
    df_correlacao = df_correlacao[df_correlacao['Frequência'] > 0]

    ######### Exibição dos gráficos #########
    opcao = st.selectbox('Escolha uma opção:', ['Selecione uma correlação:', 'Média de Horas x Idade', 'Tempo de Tela x Qualidade do Sono', 'Atividades vs Efeitos Negativos'])

    if opcao == 'Média de Horas x Idade':
        st.write('### Média de Horas Diárias de Uso de Telas por Faixa Etária')
        st.bar_chart(media_horas.set_index('faixa_etaria'), y='horas_dia_num', color='horas_dia_num', height=400, x_label='Faixa Etária', y_label='Média de Horas Diárias')

    elif opcao == 'Tempo de Tela x Qualidade do Sono':
        st.write('### Relação entre Tempo de Tela e Qualidade do Sono')
        st.bar_chart(media_sono.set_index('qualidade_sono_mes'), y='horas_dia_num', color='horas_dia_num' , height=400, horizontal=True,x_label='Média de Horas Diárias', y_label='Qualidade do Sono')

    elif opcao == 'Atividades vs Efeitos Negativos':
        st.write("### Atividades em Telas e Efeitos Negativos")
        
        # Criar o gráfico de barras empilhadas usando Altair
        chart = alt.Chart(df_correlacao).mark_bar().encode(
            x=alt.X('Atividade:N', title='Atividade'),
            y=alt.Y('Frequência:Q', title='Frequência', stack='zero'),
            color=alt.Color('Efeito_Negativo:N', title='Efeito Negativo', scale=alt.Scale(scheme='category20b')),
            tooltip=['Atividade', 'Efeito_Negativo', 'Frequência']
        ).properties(
            width=600,
            height=400,
        ).interactive()
        
        # Exibir o gráfico
        st.altair_chart(chart, use_container_width=True)

        # Adicionar uma legenda explicativa
        st.write("""
        Este gráfico de barras empilhadas mostra a correlação entre as atividades e os efeitos negativos.
        Cada barra representa uma atividade, e as seções coloridas dentro de cada barra representam os diferentes efeitos negativos.
        A altura de cada seção colorida indica a frequência com que esse efeito negativo foi associado à atividade.
        Você pode passar o mouse sobre as seções para ver detalhes específicos.
        """)
        st.markdown("#### Tabela de Correlação: Atividades vs Efeitos Negativos")
        st.dataframe(df_correlacao, use_container_width=True)