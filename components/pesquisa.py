import streamlit as st
import plotly.express as px
import pandas as pd

def contar_atividades(df):
    """Conta a frequência de cada atividade permitida nas respostas"""
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
        st.dataframe(df)

    with col2:
        opcao = st.selectbox('Escolha um filtro demográfico:', [
            'Faixa Etária', 'Gênero'
        ])
        if opcao == 'Faixa Etária':
            fig = px.pie(df, names='faixa_etaria', 
                        color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(fig)
        elif opcao == 'Gênero':
            fig = px.pie(df, names='genero', 
                        color_discrete_sequence=px.colors.sequential.Viridis)
            st.plotly_chart(fig)
            
    # Adiciona a tabela e o gráfico de contagem de atividades
    df_contagem = contar_atividades(df)
    
    st.metric(label="Sobre o gráfico", value="", 
    help="O gráfico representa a frequência das principais atividades realizadas em telas pelos 105 participantes da pesquisa. As atividades são categorizadas em: Trabalho, Estudo, Redes Sociais, Streamings e Jogos. As barras horizontais mostram quantas pessoas relataram realizar cada uma dessas atividades, onde o eixo X indica o número de respostas e o eixo Y lista as atividades. A cor e o tamanho das barras são proporcionais à quantidade de respostas, facilitando a identificação visual das atividades mais comuns entre os participantes.")
    
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
