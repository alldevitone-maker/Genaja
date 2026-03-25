import pandas as pd
import numpy as np

class ValidationEngine:
    def __init__(self):
        pass

    def validate_keys(self, df_src, df_tgt, key_src, key_tgt):
        if key_src not in df_src.columns:
            return False, f"Chave '{key_src}' não encontrada na Origem"
        if key_tgt not in df_tgt.columns:
            return False, f"Chave '{key_tgt}' não encontrada no Destino"
        return True, "Chaves válidas"

    def apply_numeric_filter(self, df, column):
        """Remove linhas onde a coluna não possui valor numérico válido"""
        if column in df.columns:
            return df[pd.to_numeric(df[column], errors='coerce').notnull()]
        return df

    def suggest_primary_keys(self, src_data, tgt_data):
        """Portado da v0.4.9: Sugestão inteligente de chaves primárias (Aceita DF ou List)"""
        common_names = ['ID', 'CODIGO', 'SKU', 'EAN', 'CPF', 'CNPJ', 'MATRICULA', 'CHAVE']
        
        def find_best(data):
            # Se for DataFrame, pega as colunas. Se for lista, usa direto.
            cols = data.columns if hasattr(data, 'columns') else data
            if len(cols) == 0: return ""
            
            # Prioridade 1: Match exato (case insensitive)
            for name in common_names:
                for col in cols:
                    if str(col).upper() == name:
                        return col
            
            # Prioridade 2: Substring
            for name in common_names:
                for col in cols:
                    if name in str(col).upper():
                        return col
            return cols[0] if len(cols) > 0 else ""
            
        best_src = find_best(src_data)
        best_tgt = find_best(tgt_data)
        return best_src, best_tgt, 0.85
