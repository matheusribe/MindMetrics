import streamlit as st
import altair as alt
import pandas as pd

def mostrar_horas_idade(df):
    st.write('### Média de Horas Diárias de Uso de Telas por Faixa Etária')
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

def mostrar_tela_sono(df):
    st.write('### Relação entre Tempo de Tela e Qualidade do Sono')
    media_sono = df.groupby('qualidade_sono_mes')['horas_dia_num'].mean().apply(lambda x: round(x, 2)).reset_index()
    
    st.bar_chart(
        media_sono.set_index('qualidade_sono_mes'), 
        y='horas_dia_num',
        y_label='Média de Horas Diárias',
        x_label= 'Qualidade do Sono',
        color='horas_dia_num',
        height=400,
        use_container_width=True
    )
    sobre_grafico = st.expander("Sobre o gráfico", icon="💡")
    sobre_grafico.write('''
        Este gráfico de barras demonstra como o tempo de tela diário se relaciona com a qualidade do sono dos respondentes.
    Isso oferece insights sobre como o uso prolongado de telas pode afetar o descanso e o bem-estar geral.
    ''')

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
    st.write("### Atividades em Telas e Efeitos Negativos")
    
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
        'Tempo de Tela x Qualidade do Sono',
        'Atividades x Efeitos Negativos'
    ], label_visibility='collapsed')

    if opcao == 'Média de Horas x Idade':
        mostrar_horas_idade(df)
    elif opcao == 'Tempo de Tela x Qualidade do Sono':
        mostrar_tela_sono(df)
    elif opcao == 'Atividades x Efeitos Negativos':
        mostrar_atividades_efeitos(df)