import pandas as pd
import numpy as np
import re

def filter_dataframe_by_columns(df, cols_to_keep, msg_prefix, log_callback):
    if len(cols_to_keep) == 0:
        return df
    
    missing_cols = [c for c in cols_to_keep if c not in df.columns]
    if missing_cols:
        log_callback(f"{msg_prefix} Coluna(s) ignorada(s) pois não existem no arquivo: {', '.join(missing_cols)}", "WARNING")
        
    valid_cols = [c for c in cols_to_keep if c in df.columns]
    return df[valid_cols].copy()


def clean_empty_quantities_multi(df, target_cols, num_cols):
    df_clean = df.copy()
    
    # Fill NAs
    df_clean[target_cols] = df_clean[target_cols].fillna('')
    try:
        df_clean[num_cols] = df_clean[num_cols].fillna(0).astype(float)
    except ValueError:
        pass
        
    # Check
    for i, row in df_clean.iterrows():
        try:
            val_num = float(row[num_cols[0]])
        except:
            continue
            
        is_empty_target = all(str(row[c]).strip() == '' for c in target_cols)
        if val_num == 0.0 and is_empty_target:
            df_clean = df_clean.drop(i)
            
    return df_clean


def apply_numeric_filter(df, cols_to_filter):
    df_clean = df.copy()
    initial_count = len(df_clean)
    for col in cols_to_filter:
        s = df_clean[col]
        # Converte para numerico se puder
        s_num = pd.to_numeric(s, errors='coerce')
        # Zeros literais ou NaNs nos numericos
        mask_zero = (s_num == 0.0)
        mask_empty_str = (s.astype(str).str.strip() == '')
        mask_nan = s.isna()
        mask_to_drop = mask_zero | mask_empty_str | mask_nan
        df_clean = df_clean[~mask_to_drop]
        
    final_count = len(df_clean)
    # log if needed
    return df_clean


def process_data_synchronization(df_src, df_tgt, key_src, key_tgt, key_tgt_final, mapping, clean_output=True):
    df_src[key_src] = df_src[key_src].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
    df_tgt[key_tgt] = df_tgt[key_tgt].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
    
    df_tgt_no_dup = df_tgt.drop_duplicates(subset=[key_tgt], keep='first')
    df_result = pd.merge(df_src, df_tgt_no_dup, left_on=key_src, right_on=key_tgt, how='left', suffixes=('', '_DROP_ME'))
    
    # Remove colunas do destino que colidiram com nomes da origem
    df_result = df_result[[c for c in df_result.columns if not c.endswith('_DROP_ME')]]
    
    for col_src, col_tgt in mapping.items():
        if col_src in df_result.columns and col_src != col_tgt:
            df_result[col_tgt] = df_result[col_src]
            
    if clean_output:
        # Remove as colunas temporarias e injeta a 3º Chave na posição Zero (0)
        cols_to_keep = list(mapping.values())
        if key_tgt_final in cols_to_keep:
            cols_to_keep.remove(key_tgt_final)
        cols_to_keep.insert(0, key_tgt_final)
        cols_to_keep = [c for c in dict.fromkeys(cols_to_keep) if c in df_result.columns]
        df_final = df_result[cols_to_keep].copy()
    else:
        # Mantem todas as colunas da origem nativas + as colunas sincronizadas do destino
        # Injeta a chave principal no começo
        cols_to_keep = list(df_result.columns)
        if key_tgt_final in cols_to_keep:
            cols_to_keep.remove(key_tgt_final)
        cols_to_keep.insert(0, key_tgt_final)
        df_final = df_result[cols_to_keep].copy()
    
    return df_final


def process_data_comparison(df_src, df_tgt, key_src, key_tgt, comp_tipo, clean_output, mapping, key_tgt_final):
    df_src_cmp = df_src.copy()
    df_tgt_cmp = df_tgt.copy()
    
    df_src_cmp[key_src] = df_src_cmp[key_src].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
    df_tgt_cmp[key_tgt] = df_tgt_cmp[key_tgt].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
    
    if comp_tipo == 'falta_destino':
        missing_keys = set(df_src_cmp[key_src]) - set(df_tgt_cmp[key_tgt])
        df_result = df_src_cmp[df_src_cmp[key_src].isin(missing_keys)].copy()
        
        if clean_output:
            cols = list(mapping.keys())
            if key_tgt_final in cols: cols.remove(key_tgt_final)
            cols.insert(0, key_tgt_final)
            cols = [c for c in dict.fromkeys(cols) if c in df_result.columns]
            df_result = df_result[cols]
            
    else: # falta_origem
        missing_keys = set(df_tgt_cmp[key_tgt]) - set(df_src_cmp[key_src])
        df_result = df_tgt_cmp[df_tgt_cmp[key_tgt].isin(missing_keys)].copy()
        
        if clean_output:
            cols = list(mapping.values())
            if key_tgt_final in cols: cols.remove(key_tgt_final)
            cols.insert(0, key_tgt_final)
            cols = [c for c in dict.fromkeys(cols) if c in df_result.columns]
            df_result = df_result[cols]

    return df_result, len(df_result)


def suggest_primary_keys(df_src, df_tgt):
    matches = []
    
    src_sample = df_src.head(10000)
    tgt_sample = df_tgt.head(10000)
    
    tgt_sets = {}
    for t_col in tgt_sample.columns:
        s = tgt_sample[t_col].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
        s = s[s != 'nan']
        s = s[s != '']
        tgt_sets[t_col] = set(s)
        
    for s_col in src_sample.columns:
        s = src_sample[s_col].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
        s = s[s != 'nan']
        s = s[s != '']
        s_set = set(s)
        
        if not s_set: continue
            
        for t_col, t_set in tgt_sets.items():
            if not t_set: continue    
            intersection = len(s_set & t_set)
            
            if intersection > 0:
                matches.append({'src': s_col, 'tgt': t_col, 'score': intersection})
                
    matches.sort(key=lambda x: x['score'], reverse=True)
    return matches[:3]
