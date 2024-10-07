import streamlit as st
import pandas as pd
import altair as alt

# Logo 
st.logo('icon.svg')

### Importando os Dados ###
@st.cache_data
def carregar_dados():
    return pd.read_excel('data/pesquisa.xlsx')

df = carregar_dados()

### Visualização dos Dados ###
st.sidebar.title('Menu')
pagina_dashboard = st.sidebar.selectbox('Selecione uma opção:', ['Dashboards'])

if pagina_dashboard == 'Dashboards':
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

    media_sono = df.groupby('qualidade_sono_mes')['horas_dia_num'].mean().apply(lambda x: round(x, 2)).reset_index()

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

    ### Correlação Faixa etaria, horas e estresse ###

    # Filtrar colunas relevantes
    df_filtered = df[['faixa_etaria', 'horas_dia', 'estresse_mes']]

    # Excluir dados faltantes
    df_filtered = df_filtered.dropna()

    # Converter a coluna 'estresse_mes' para numérica (se os níveis de estresse forem categóricos, pode ser necessário mapeá-los)
    stress_mapping = {
        'Baixo': 1,
        'Moderado': 2,
        'Alto': 3,
        'Muito Alto': 4
    }

    df_filtered['estresse_numerico'] = df_filtered['estresse_mes'].map(stress_mapping)

    # Converter 'horas_dia' em números para o gráfico (mapeando as categorias em números)
    horas_mapping = {
        'Menos de 1 hora': 0.5,
        '1 - 2 horas': 1.5,
        '3 - 4 horas': 3.5,
        '5 - 6 horas': 5.5,
        'Mais de 6 horas': 7
    }

    df_filtered['horas_numerico'] = df_filtered['horas_dia'].map(horas_mapping)

    ######### Exibição dos gráficos #########
    opcao = st.selectbox('Escolha uma opção:', ['Ocultar Gráfico', 'Média de Horas x Idade', 'Tempo de Tela x Qualidade do Sono', 'Gráfico de Correlação', 'Faixa Etária x Horas de Tela x Estresse'])

    if opcao == 'Média de Horas x Idade':
        st.write('### Média de Horas Diárias de Uso de Telas por Faixa Etária')
        st.bar_chart(media_horas.set_index('faixa_etaria'), y='horas_dia_num')

    elif opcao == 'Tempo de Tela x Qualidade do Sono':
        st.write('Relação entre Tempo de Tela e Qualidade do Sono')
        st.bar_chart(media_sono.set_index('qualidade_sono_mes'), y='horas_dia_num')

    elif opcao == 'Gráfico de Correlação':
        st.title("Gráfico de Correlação: Atividades vs Efeitos Negativos")
        
        # Criar o gráfico de barras empilhadas usando Altair
        chart = alt.Chart(df_correlacao).mark_bar().encode(
            x=alt.X('Atividade:N', title='Atividade'),
            y=alt.Y('Frequência:Q', title='Frequência', stack='zero'),
            color=alt.Color('Efeito_Negativo:N', title='Efeito Negativo', scale=alt.Scale(scheme='category20b')),
            tooltip=['Atividade', 'Efeito_Negativo', 'Frequência']
        ).properties(
            width=600,
            height=400,
            title='Correlação entre Atividades e Efeitos Negativos'
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

    elif opcao == 'Faixa Etária x Horas de Tela x Estresse':
        # Criação do gráfico de dispersão com Streamlit
        st.write("Correlação entre Faixa Etária, Horas de Uso de Tela e Estresse")

        # Usar scatter_chart com as colunas numéricas
        st.scatter_chart(data=df_filtered, x='horas_numerico', y='estresse_numerico', color='faixa_etaria')
        
        # Criar os dados para a tabela de Nível de Estresse
        estresse_data = {
            'Nível de Estresse': ['Baixo', 'Moderado', 'Alto', 'Muito Alto'],
            'Código': ['1', '2', '3', '4']
        }
        estresse_df = pd.DataFrame(estresse_data)

        # Criar os dados para a tabela de Horas de Tela
        horas_data = {
            'Horas de Tela': ['Menos de 1 hora', '1 - 2 horas', '3 - 4 horas', '5 - 6 horas', 'Mais de 6 horas'],
            'Código': ['0.5', '1.5', '3.5', '5.5', '7']
        }
        horas_df = pd.DataFrame(horas_data)

        # Criar um espaço em branco para centralizar as colunas
        st.write("Legendas") 
        col1, col2 = st.columns(2)

        # Tabela para Nível de Estresse na primeira coluna
        with col1:
            st.dataframe(estresse_df, hide_index=True, use_container_width=True)

        # Tabela para Horas de Tela na segunda coluna
        with col2:
            st.dataframe(horas_df, hide_index=True, use_container_width=True)

        st.write("")  # Espaço abaixo 