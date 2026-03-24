import pandas as pd
import numpy as np

def filter_dataframe_by_columns(df, cols_to_keep, msg_prefix, log_callback):
    """Filtra colunas do DataFrame com logging de erro."""
    if len(cols_to_keep) == 0:
        return df
    
    missing_cols = [c for c in cols_to_keep if c not in df.columns]
    if missing_cols:
        log_callback(f"{msg_prefix} Coluna(s) ignorada(s) pois não existem no arquivo: {', '.join(missing_cols)}", "WARNING")
        
    valid_cols = [c for c in cols_to_keep if c in df.columns]
    return df[valid_cols].copy()

def apply_numeric_filter(df, cols_to_filter):
    """Aplica filtro para remover zeros, strings vazias e NaNs em colunas numéricas."""
    df_clean = df.copy()
    for col in cols_to_filter:
        s = df_clean[col]
        s_num = pd.to_numeric(s, errors='coerce')
        mask_zero = (s_num == 0.0)
        mask_empty_str = (s.astype(str).str.strip() == '')
        mask_nan = s.isna()
        mask_to_drop = mask_zero | mask_empty_str | mask_nan
        df_clean = df_clean[~mask_to_drop]
    return df_clean

def clean_empty_quantities_multi(df, target_cols, num_cols):
    """Limpeza avançada de linhas onde as colunas alvo estão vazias e o valor numérico é zero."""
    df_clean = df.copy()
    df_clean[target_cols] = df_clean[target_cols].fillna('')
    try:
        df_clean[num_cols] = df_clean[num_cols].fillna(0).astype(float)
    except ValueError:
        pass
        
    for i, row in df_clean.iterrows():
        try:
            val_num = float(row[num_cols[0]])
        except:
            continue
            
        is_empty_target = all(str(row[c]).strip() == '' for c in target_cols)
        if val_num == 0.0 and is_empty_target:
            df_clean = df_clean.drop(i)
            
    return df_clean
