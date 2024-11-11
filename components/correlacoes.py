import streamlit as st
import altair as alt
import pandas as pd
import plotly.express as px

def mostrar_horas_idade(df):
    st.write('### Relação entre Média de Horas Diárias de Uso de Telas por Faixa Etária')
    media_horas = df.groupby('faixa_etaria')['horas_dia_num'].mean().apply(lambda x: round(x, 2)).reset_index()
    
    st.bar_chart(
        media_horas.set_index('faixa_etaria'), 
        y='horas_dia_num',
        y_label='Média de Horas Diárias',
        x_label= 'Faixa Etária',
        color='horas_dia_num', 
        height=400,
        use_container_width=True
    )
    sobre_grafico = st.expander("Sobre o gráfico", icon="💡")
    sobre_grafico.write('''
        Este gráfico de barras mostra a média de horas diárias de uso de telas para cada faixa etária.
    Ele ajuda a visualizar quais grupos de idade tendem a passar mais tempo em frente a dispositivos,
    fornecendo uma visão geral do comportamento de uso de telas por idade.
    ''')
    
    st.markdown("#### Tabela da Correlação: Média de Horas Diárias por Faixa Etária")
    media_horas_renomeada = media_horas.rename(columns={
        'faixa_etaria': 'Faixa Etária',
        'horas_dia_num': 'Média de Horas Diárias'
    })
    st.dataframe(media_horas_renomeada, use_container_width=True, hide_index=True)

def mostrar_qualidade_sono(df):
    st.write("### Relação entre a média da Qualidade do Sono e Nível de Estresse")
    # Mapeamento de qualidade do sono para valores numéricos
    quality_mapping = {
        '1 - Muito Ruim': 1,
        '2 - Ruim': 2,
        '3 - Regular': 3,
        '4 - Bom': 4,
        '5 - Excelente': 5
    }
    df['qualidade_sono_num'] = df['qualidade_sono_mes'].map(quality_mapping)

    # Mapeamento de estresse para valores numéricos
    stress_mapping = {
        'Baixo': 1,
        'Moderado': 2,
        'Alto': 3,
        'Muito alto': 4
    }
    df['estresse_mes_num'] = df['estresse_mes'].map(stress_mapping)

    # Verifica se há valores ausentes após o mapeamento
    if df['qualidade_sono_num'].isnull().any() or df['estresse_mes_num'].isnull().any():
        st.error("Existem valores ausentes após o mapeamento. Verifique os dados de entrada.")
        return

    # Agrupando os dados por nível de estresse e calculando a média da qualidade do sono
    df_grouped = df.groupby('estresse_mes').agg({'qualidade_sono_num': 'mean'}).reset_index()

    # Mapeando a média para as categorias de qualidade do sono
    def map_quality(num):
        if num <= 1.5:
            return '1 - Muito Ruim'
        elif num <= 2.5:
            return '2 - Ruim'
        elif num <= 3.5:
            return '3 - Regular'
        elif num <= 4.5:
            return '4 - Bom'
        else:
            return '5 - Excelente'

    # Aplicando a função de mapeamento
    df_grouped['qualidade_sono_str'] = df_grouped['qualidade_sono_num'].apply(map_quality)

    # Ordenando o DataFrame do maior índice para o menor
    df_grouped.sort_values(by='qualidade_sono_num', ascending=False, inplace=True)

    # Remover duplicatas nas categorias de qualidade do sono
    df_grouped = df_grouped.drop_duplicates(subset=['qualidade_sono_str'])

    # Criando o gráfico de barras
    fig_bar = px.bar(df_grouped, 
                     x='estresse_mes', 
                     y='qualidade_sono_num',
                     labels={'qualidade_sono_num': 'Qualidade do Sono', 'estresse_mes': 'Nível de Estresse'},
                     color='qualidade_sono_num',
                     color_continuous_scale=px.colors.sequential.YlGnBu)

    # Atualizando os rótulos do eixo y para mostrar as strings
    fig_bar.update_yaxes(tickvals=df_grouped['qualidade_sono_num'], 
                         ticktext=df_grouped['qualidade_sono_str'])

    # Formatação das médias no hover com duas casas decimais
    fig_bar.update_traces(hovertemplate='Nível de Estresse: %{x}<br>Média da Qualidade do Sono: %{y:.2f}')

    # Exibindo o gráfico
    st.plotly_chart(fig_bar)
    sobre_grafico = st.expander("Sobre o gráfico", icon="💡")
    sobre_grafico.write('''
        Este gráfico de barras mostra a média da qualidade do sono em relação ao nível de estresse.
        Ele permite observar como diferentes níveis de estresse podem impactar a qualidade do sono,
        oferecendo uma visão geral do bem-estar dos participantes em relação ao estresse mensal.
    ''')

    # st.write('### Relação entre Tempo de Tela e Qualidade do Sono')
    # media_sono = df.groupby('qualidade_sono_mes')['horas_dia_num'].mean().apply(lambda x: round(x, 2)).reset_index()
    
    # st.bar_chart(
    #     media_sono.set_index('qualidade_sono_mes'), 
    #     y='horas_dia_num',
    #     y_label='Média de Horas Diárias',
    #     x_label= 'Qualidade do Sono',
    #     color='horas_dia_num',
    #     height=400,
    #     use_container_width=True
    # )
    # sobre_grafico = st.expander("Sobre o gráfico", icon="💡")
    # sobre_grafico.write('''
    #     Este gráfico de barras demonstra como o tempo de tela diário se relaciona com a qualidade do sono dos respondentes.
    # Isso oferece insights sobre como o uso prolongado de telas pode afetar o descanso e o bem-estar geral.
    # ''')

def unificar_streaming(atividade):
    plataformas_streaming = ['Youtube', 'Netflix', 'Prime video', 'max', 'YouTube']
    return 'Streamings' if any(plataforma.lower() in atividade.lower() for plataforma in plataformas_streaming) else atividade

def filtrar_atividades(atividade):
    atividades_permitidas = ["Trabalho", "Estudo", "Redes Sociais", "Streamings", "Jogos"]
    return atividade in atividades_permitidas

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

def mostrar_atividades_efeitos(df):
    st.write("### Relação entre as Atividades em Telas e Efeitos Negativos")
    
    atividades_lista, efeitos_lista, responsaveis_lista = expandir_coluna(df['atividades'], df['efeitos_negativos'])

    df_correlacao = pd.DataFrame({
        'Atividade': atividades_lista,
        'Efeito_Negativo': efeitos_lista,
        'Responsavel': responsaveis_lista
    })

    df_correlacao = df_correlacao.drop_duplicates(subset=['Atividade', 'Efeito_Negativo', 'Responsavel'])
    df_correlacao = df_correlacao.groupby(['Atividade', 'Efeito_Negativo']).size().reset_index(name='Frequência')
    df_correlacao = df_correlacao[df_correlacao['Frequência'] > 0]
    
    chart = alt.Chart(df_correlacao).mark_bar().encode(
        x=alt.X('Atividade:N', title='Atividade'),
        y=alt.Y('Frequência:Q', title='Frequência', stack='zero'),
        color=alt.Color('Efeito_Negativo:N', title='Efeito Negativo', scale=alt.Scale(scheme='category20b')),
        tooltip=['Atividade', 'Efeito_Negativo', 'Frequência']
    ).properties(
        width="container",
        height=400,
    ).interactive()
    
    st.altair_chart(chart, use_container_width=True)

    sobre_grafico = st.expander("Sobre o gráfico", icon="💡")
    sobre_grafico.write('''
    Este gráfico de barras empilhadas mostra a correlação entre as atividades e os efeitos negativos.
    Cada barra representa uma atividade, e as seções coloridas dentro de cada barra representam os diferentes efeitos negativos.
    A altura de cada seção colorida indica a frequência com que esse efeito negativo foi associado à atividade.
    Você pode passar o mouse sobre as seções para ver detalhes específicos.
    ''')
    
    st.markdown("#### Tabela da Correlação: Atividades e Efeitos Negativos")
    st.dataframe(df_correlacao, use_container_width=True, hide_index=True)

def mostrar_correlacoes(df):
    opcao = st.selectbox('Selecione uma correlação:', [
        'Selecione uma correlação:',
        'Média de Horas x Idade',
        'Qualidade do Sono x Nível de Estresse',
        'Atividades x Efeitos Negativos'
    ], label_visibility='collapsed')

    if opcao == 'Média de Horas x Idade':
        mostrar_horas_idade(df)
    elif opcao == 'Qualidade do Sono x Nível de Estresse':
        mostrar_qualidade_sono(df)
    elif opcao == 'Atividades x Efeitos Negativos':
        mostrar_atividades_efeitos(df)