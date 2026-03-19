import pandas as pd

def filter_dataframe_by_columns(df, cols):
    unique = list(dict.fromkeys(cols)) # remove duplicatas preservando ordem
    return df[unique].copy()

def apply_numeric_filter(df, col):
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    return df[df[col] > 0]

def process_data_synchronization(df_src, df_tgt, key_src, key_tgt, mapping):
    df_final = df_tgt.copy()
    
    # Prepara dados de atualização (Origem)
    update_data = (
        df_src.set_index(key_src)
        .groupby(level=0).last() # remove duplicatas na chave
        .rename(columns=mapping)
    )
    
    df_final.set_index(key_tgt, inplace=True)
    df_final.update(update_data)
    df_final.reset_index(inplace=True)
    
    matches = df_tgt[key_tgt].isin(df_src[key_src]).sum()
    return df_final, matches
