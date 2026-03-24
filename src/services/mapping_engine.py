import pandas as pd
import re

def suggest_primary_keys(df_src, df_tgt):
    """
    Analisa as primeiras 10.000 linhas de dois DataFrames e sugere as 
    chaves primárias com maior taxa de intersecção.
    """
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
