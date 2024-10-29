import streamlit as st
import plotly.express as px
import pandas as pd

def contar_atividades(df):
    atividades_permitidas = ["Trabalho", "Estudo", "Redes Sociais", "Streamings", "Jogos"]
    
    # Inicializa o dicionário para contar as atividades
    contagem_atividades = {atividade: 0 for atividade in atividades_permitidas}
    
    # Conta as ocorrências de cada atividade
    for atividades in df['atividades']:
        if pd.isna(atividades):
            continue
        
        lista_atividades = [ativ.strip() for ativ in str(atividades).split(',')]
        # Flag para controlar se já contamos streaming nesta resposta
        streaming_contado = False
        
        for atividade in lista_atividades:
            # Verifica se é streaming
            is_streaming = any(plataforma.lower() in atividade.lower() 
                             for plataforma in ['Youtube', 'Netflix', 'Prime video', 'max', 'YouTube'])
            
            if is_streaming and not streaming_contado:
                contagem_atividades["Streamings"] += 1
                streaming_contado = True  # Marca que já contamos streaming nesta resposta
            elif atividade in atividades_permitidas:
                contagem_atividades[atividade] += 1
    
    # Cria um DataFrame com a contagem
    df_contagem = pd.DataFrame(list(contagem_atividades.items()), 
                             columns=['Atividade', 'Quantidade'])
    return df_contagem

def mostrar_pesquisa(df):
    col1, col2 = st.columns([3, 2], gap='large', vertical_alignment='top')
    
    with col1:
        st.metric(label="Respostas", value="105", 
                 help="Quantidade de respostas que a pesquisa obteve")
        st.write("##### Quadro geral de respostas")
        df.index = df.index + 1
        colunas_desejadas = [
            'faixa_etaria', 'genero', 'frequencia_dia', 'horas_dia', 
            'atividades', 'estresse_mes', 'qualidade_sono_mes', 
            'avaliacao_impacto', 'efeitos_negativos'
        ]
        novos_nomes = {
            'faixa_etaria': 'Faixa etária',
            'genero': 'Gênero',
            'frequencia_dia': 'Frequência de uso diariamente',
            'horas_dia': 'Média de uso diariamente',
            'atividades': 'Atividades em telas',
            'estresse_mes': 'Nível de estresse no último mês',
            'qualidade_sono_mes': 'Qualidade do sono no último mês',
            'avaliacao_impacto': 'Avaliação no impacto das telas',
            'efeitos_negativos': 'Principais efeitos negativos'
        }
        df_visualizacao = df[colunas_desejadas].rename(columns=novos_nomes)  
        st.dataframe(df_visualizacao, use_container_width=True)
        
    with col2:
        opcao = st.selectbox('Escolha um filtro demográfico:', [
            'Faixa Etária', 'Gênero'
        ])
        if opcao == 'Faixa Etária':
            fig = px.pie(df, names='faixa_etaria', 
                        color_discrete_sequence=px.colors.sequential.RdBu)
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        elif opcao == 'Gênero':
            fig = px.pie(df, names='genero', 
                        color_discrete_sequence=px.colors.sequential.Viridis)
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        opcao2 = st.selectbox('Escolha uma sessão para os dados:', ['Uso de telas', 'Bem estar', 'Efeitos Negativos'])

    # Adiciona o gráfico de pizza separados
    if opcao2 == 'Uso de telas':
        st.markdown('### Informações acerca do uso de telas')
        col1, col2 = st.columns([2, 2], gap='large', vertical_alignment='top')
        with col1:
            fig = px.pie(df, names='frequencia_dia')
            fig.update_layout(height=350, title='Frequência de uso de telas no dia')
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.pie(df, names='horas_dia')
            fig.update_layout(height=350, title='Horas diárias de uso de telas')
            st.plotly_chart(fig, use_container_width=True)

        # Adiciona gráfico de contagem de atividades
        df_contagem = contar_atividades(df)

        # Cria o gráfico de barras horizontal
        fig = px.bar(df_contagem, 
                    x='Quantidade', 
                    y='Atividade',
                    orientation='h',  # Torna o gráfico horizontal
                    title='Frequência de Atividades',
                    color='Quantidade',  # Adiciona cor baseada na quantidade
                    color_continuous_scale=px.colors.sequential.RdBu,  # Escolhe a escala de cores
                    text='Quantidade')  # Mostra os valores nas barras
        
        # Personaliza o layout do gráfico
        fig.update_traces(textposition='outside')  # Coloca os números fora das barras
        fig.update_layout(
            yaxis={'categoryorder':'total ascending'},  # Ordena as barras por quantidade
            showlegend=False,  # Remove a legenda
            xaxis_title="Quantidade de Respostas",
            yaxis_title="Atividades",
            height=400  # Ajusta a altura do gráfico
        )
        
        # Exibe o gráfico
        st.plotly_chart(fig, use_container_width=True)
        sobre_grafico = st.expander("Sobre o gráfico", icon="💡")
        sobre_grafico.write('''
            O gráfico representa a frequência das principais atividades realizadas em telas pelos 105 participantes da pesquisa. As barras horizontais mostram quantas pessoas relataram realizar cada uma dessas atividades. O eixo X indica o número de respostas e o eixo Y lista as atividades. A cor e o tamanho das barras são proporcionais à quantidade de respostas, facilitando a identificação visual das atividades mais comuns entre os participantes.
        ''')

    elif opcao2 == 'Bem estar':
        st.markdown('### Informações acerca do bem-estar')
        col1, col2 = st.columns([2, 2], gap='large', vertical_alignment='top')
        with col1:
            fig = px.pie(df, names='qualidade_sono_mes', color_discrete_sequence=px.colors.sequential.Cividis)
            fig.update_layout(height=350, title='Avaliação da qualidade do sono no último mês')
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.pie(df, names='estresse_mes', color_discrete_sequence=px.colors.sequential.Cividis)
            fig.update_layout(height=350, title='Avaliacao de estresse no último mês')
            st.plotly_chart(fig, use_container_width=True)
        contagem = df['avaliacao_impacto'].value_counts().reset_index()
        contagem.columns = ['avaliacao_impacto', 'contagem']
        fig = px.bar(contagem, x='avaliacao_impacto', y='contagem', color='avaliacao_impacto',
            color_discrete_sequence=px.colors.sequential.RdBu, title='Avaliação se o uso de telas impactaram na saúde mental' ,labels={'avaliacao_impacto': 'Avaliação de Impacto', 'contagem': 'Quantidade'})
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)

    elif opcao2 == 'Efeitos Negativos':
        def contar_efeitos(df):
            efeitos_permitidos = [
                "Insônia ou distúrbios do sono", 
                "Ansiedade", 
                "Depressão", 
                "Estresse",
                "Isolamento social", 
                "Dificuldade de concentração"
            ]
            
            # Inicializa o dicionário para contar os efeitos
            contagem_efeitos = {efeito: 0 for efeito in efeitos_permitidos}
            
            # Conta as ocorrências de cada efeito
            for efeitos in df['efeitos_negativos']:
                if pd.isna(efeitos):
                    continue
                
                lista_efeitos = [efeito.strip() for efeito in str(efeitos).split(',')]
                
                for efeito in lista_efeitos:
                    if efeito in efeitos_permitidos:
                        contagem_efeitos[efeito] += 1
            
            # Cria um DataFrame com a contagem
            df_contagem = pd.DataFrame(list(contagem_efeitos.items()), 
                                    columns=['Efeito Negativo', 'Quantidade'])
            return df_contagem

        # Chama a função para contar os efeitos negativos
        df_contagem = contar_efeitos(df)

        # Cria o gráfico de barras horizontal
        fig = px.bar(
            df_contagem, 
            x='Quantidade', 
            y='Efeito Negativo',
            orientation='h',  # Torna o gráfico horizontal
            title='Frequência de Efeitos Negativos',
            color='Quantidade',  # Adiciona cor baseada na quantidade
            color_continuous_scale=px.colors.sequential.YlOrRd,  # Escolhe a escala de cores
            text='Quantidade'  # Mostra os valores nas barras
        )

        # Personaliza o layout do gráfico
        fig.update_traces(textposition='outside')  # Coloca os números fora das barras
        fig.update_layout(
            yaxis={'categoryorder':'total ascending'},  # Ordena as barras por quantidade
            showlegend=False,  # Remove a legenda
            xaxis_title="Quantidade de Respostas",
            yaxis_title="Efeitos Negativos",
            height=400  # Ajusta a altura do gráfico
        )

        # Exibir o gráfico no Streamlit
        st.plotly_chart(fig, use_container_width=True)