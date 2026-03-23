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


def process_data_comparison(df_src, df_tgt, key_src, key_tgt, comp_tipo, clean_output, mapping):
    df_src_cmp = df_src.copy()
    df_tgt_cmp = df_tgt.copy()
    
    df_src_cmp[key_src] = df_src_cmp[key_src].astype(str).str.replace(r'\\.0$', '', regex=True).str.strip()
    df_tgt_cmp[key_tgt] = df_tgt_cmp[key_tgt].astype(str).str.replace(r'\\.0$', '', regex=True).str.strip()
    
    if comp_tipo == 'falta_destino':
        missing_keys = set(df_src_cmp[key_src]) - set(df_tgt_cmp[key_tgt])
        df_result = df_src_cmp[df_src_cmp[key_src].isin(missing_keys)].copy()
        
        if clean_output:
            cols = [key_src] + list(mapping.keys())
            cols = [c for c in dict.fromkeys(cols) if c in df_result.columns]
            df_result = df_result[cols]
            
    else: # falta_origem
        missing_keys = set(df_tgt_cmp[key_tgt]) - set(df_src_cmp[key_src])
        df_result = df_tgt_cmp[df_tgt_cmp[key_tgt].isin(missing_keys)].copy()
        
        if clean_output:
            cols = [key_tgt] + list(mapping.values())
            cols = [c for c in dict.fromkeys(cols) if c in df_result.columns]
            df_result = df_result[cols]

    return df_result, len(df_result)


def suggest_primary_keys(df_src, df_tgt):
    best_src = None
    best_tgt = None
    max_score = 0
    
    # Samples para extrema velocidade
    src_sample = df_src.head(10000)
    tgt_sample = df_tgt.head(10000)
    
    tgt_sets = {}
    for t_col in tgt_sample.columns:
        s = tgt_sample[t_col].astype(str).str.replace(r'\\.0$', '', regex=True).str.strip()
        s = s[s != 'nan']
        s = s[s != '']
        tgt_sets[t_col] = set(s)
        
    for s_col in src_sample.columns:
        s = src_sample[s_col].astype(str).str.replace(r'\\.0$', '', regex=True).str.strip()
        s = s[s != 'nan']
        s = s[s != '']
        s_set = set(s)
        
        if not s_set: continue
            
        for t_col, t_set in tgt_sets.items():
            if not t_set: continue    
            intersection = len(s_set & t_set)
            
            if intersection > max_score:
                max_score = intersection
                best_src = s_col
                best_tgt = t_col
                
    return best_src, best_tgt, max_score
