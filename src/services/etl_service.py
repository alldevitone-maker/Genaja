import pandas as pd
import numpy as np

def filter_dataframe_by_columns(df, cols):
    unique = list(dict.fromkeys(cols)) # remove duplicatas preservando ordem
    return df[unique].copy()

def apply_numeric_filter(df, col):
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    return df[df[col] > 0]

def clean_empty_quantities_multi(df, cols):
    """ Filtra as linhas mantendo-as se PELO MENOS UMA das colunas informadas
    tiver um valor preenchido/maior que 0 (se numérico) ou texto não vazio.
    Remove a linha APENAS se TODAS as colunas informadas forem zero/nulas/vazias. """
    if not cols:
        return df.copy()
        
    mask = pd.Series(False, index=df.index)
    for col in cols:
        if col not in df.columns:
            continue
        series = df[col]
        not_null = series.notna()
        s_str = series.astype(str).str.strip().str.lower()
        valid_str = (s_str != '') & (s_str != 'nan') & (s_str != '<na>')
        
        # Considera ZERO tanto literais exatos como numericos = 0
        num_vals = pd.to_numeric(series.astype(str).str.replace(',', '.'), errors='coerce')
        is_num_zero = (num_vals == 0)
        is_str_zero = s_str.isin(['0', '0.0', '0,0', '0.00'])
        
        not_zero = ~(is_num_zero | is_str_zero)
        
        col_has_value = not_null & valid_str & not_zero
        mask = mask | col_has_value
        
    return df[mask].copy()

def process_data_synchronization(df_src, df_tgt, key_src, key_tgt, mapping):
    df_final = df_tgt.copy()
    
    # Tratamento de Tipos: Garante que chaves numéricas ou char conversem como string limpa
    df_src[key_src] = df_src[key_src].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
    df_final[key_tgt] = df_final[key_tgt].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
    
    # Prepara dados de atualização (Origem)
    update_data = (
        df_src.set_index(key_src)
        .groupby(level=0).last() # remove duplicatas na chave
        .rename(columns=mapping)
    )
    
    df_final.set_index(key_tgt, inplace=True)
    
    # 1. Atualiza as colunas que JÁ existem no SAP
    df_final.update(update_data)
    
    # 2. Identifica colunas novas que NÃO existem no SAP
    novas_cols = [col for col in update_data.columns if col not in df_final.columns]
    
    # 3. Adiciona colunas novas fazendo um LEFT JOIN no index
    if novas_cols:
        df_final = df_final.join(update_data[novas_cols], how='left')
        
    df_final.reset_index(inplace=True)
    
    matches = df_final[key_tgt].isin(df_src[key_src]).sum()
    return df_final, matches
