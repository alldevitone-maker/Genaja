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
    """
    Remove linhas onde TODAS as colunas especificadas são zero, nulas ou vazias.
    Preserva valores como '0123' (códigos com zero à esquerda) pois não avaliam como zero absoluto.
    """
    if not cols_to_filter:
        return df
        
    df_clean = df.copy()
    valid_cols = [c for c in cols_to_filter if c in df_clean.columns]
    
    if not valid_cols:
        return df_clean

    # Começamos assumindo que todas são "candidatas a deletar" (True)
    # E usamos a operação AND (&) para garantir que SÓ continue True se TODAS forem zero/nulas
    mask_to_drop = pd.Series(True, index=df_clean.index)
    
    for col in valid_cols:
        s = df_clean[col].astype(str).str.strip()
        # Converte para numérico mas mantém NaN para o que não for número (como strings vazias)
        s_num = pd.to_numeric(s, errors='coerce')
        
        # Uma célula é considerada "vazia/zero" se:
        # 1. O valor numérico é exatamente 0.0
        # 2. A string original é vazia ou 'nan'
        # 3. O valor original é NaN real
        is_zero = (s_num == 0.0) | (s_num == 0)
        is_empty = (s == '') | (s.str.lower() == 'nan')
        is_nan = df_clean[col].isna()
        
        mask_to_drop &= (is_zero | is_empty | is_nan)
        
    return df_clean[~mask_to_drop]

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

def apply_text_transformations(df, trim=True, upper=True):
    """Aplica transformações de texto (Trim e Upper Case) em colunas do tipo objeto."""
    df_clean = df.copy()
    if trim:
        df_clean = df_clean.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    if upper:
        df_clean = df_clean.apply(lambda x: x.str.upper() if x.dtype == "object" else x)
    return df_clean
