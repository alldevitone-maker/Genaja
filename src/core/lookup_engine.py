import pandas as pd

class LookupEngine:
    """
    Motor de Consulta Inteligente (v0.6.3).
    Substitui lógicas de PROCV/XLOOKUP via Joins eficientes.
    """
    def __init__(self):
        pass

    def find_common_columns(self, df_src, df_tgt):
        """Identifica colunas comuns preservando a ordem da origem (Hardening Patch 2)."""
        if df_src is None or df_tgt is None: return []
        tgt_cols = set(df_tgt.columns)
        return [col for col in df_src.columns if col in tgt_cols]

    def suggest_key_pair(self, df_src, df_tgt):
        """Sugerir par de chaves com guarda contra NaN e Zero Division (Hardening Patch 2)."""
        common = self.find_common_columns(df_src, df_tgt)
        if not common or len(df_src) == 0 or len(df_tgt) == 0:
            return None, None
            
        for col in common:
            # Ignorar NaN no cálculo de unicidade
            u_src = len(df_src[col].dropna().unique()) / len(df_src)
            u_tgt = len(df_tgt[col].dropna().unique()) / len(df_tgt)
            
            if u_src > 0.8 and u_tgt > 0.8:
                return col, col
        return None, None
