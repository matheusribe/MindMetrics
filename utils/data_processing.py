import pandas as pd

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

def processar_dados_correlacao(df):
    df['horas_dia_num'] = df['horas_dia'].apply(converter_horas)
    return df