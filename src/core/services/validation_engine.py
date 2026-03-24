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

    def suggest_primary_keys(self, df_src, df_tgt):
        """Portado da v0.4.9: Sugestão inteligente de chaves primárias"""
        common_names = ['ID', 'CODIGO', 'SKU', 'EAN', 'CPF', 'CNPJ', 'MATRICULA', 'CHAVE']
        
        def find_best(df):
            for name in common_names:
                for col in df.columns:
                    if name in col.upper():
                        return col
            return df.columns[0]
            
        best_src = find_best(df_src)
        best_tgt = find_best(df_tgt)
        return best_src, best_tgt, 0.85
