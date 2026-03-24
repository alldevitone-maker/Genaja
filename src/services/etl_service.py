import pandas as pd
import numpy as np
import re

import pandas as pd
import numpy as np
import re

# Import modularized engines
from .mapping_engine import suggest_primary_keys
from .validation_engine import filter_dataframe_by_columns, apply_numeric_filter, clean_empty_quantities_multi

def process_data_synchronization(df_src, df_tgt, key_src, key_tgt, key_tgt_final, mapping, clean_output=True):
    """Core Engine: Sincronização de dados entre Origem e Destino."""
    df_src[key_src] = df_src[key_src].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
    df_tgt[key_tgt] = df_tgt[key_tgt].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
    
    df_tgt_no_dup = df_tgt.drop_duplicates(subset=[key_tgt], keep='first')
    df_result = pd.merge(df_src, df_tgt_no_dup, left_on=key_src, right_on=key_tgt, how='left', suffixes=('', '_DROP_ME'))
    
    df_result = df_result[[c for c in df_result.columns if not c.endswith('_DROP_ME')]]
    
    for col_src, col_tgt in mapping.items():
        if col_src in df_result.columns and col_src != col_tgt:
            df_result[col_tgt] = df_result[col_src]
            
    if clean_output:
        cols_to_keep = list(mapping.values())
        if key_tgt_final in cols_to_keep:
            cols_to_keep.remove(key_tgt_final)
        cols_to_keep.insert(0, key_tgt_final)
        cols_to_keep = [c for c in dict.fromkeys(cols_to_keep) if c in df_result.columns]
        df_final = df_result[cols_to_keep].copy()
    else:
        cols_to_keep = list(df_result.columns)
        if key_tgt_final in cols_to_keep:
            cols_to_keep.remove(key_tgt_final)
        cols_to_keep.insert(0, key_tgt_final)
        df_final = df_result[cols_to_keep].copy()
    
    return df_final


def process_data_comparison(df_src, df_tgt, key_src, key_tgt, comp_tipo, clean_output, mapping, key_tgt_final):
    """Core Engine: Comparação de lacunas entre bases (Faltas no Destino ou Origem)."""
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
