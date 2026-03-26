import pandas as pd

class LookupEngine:
    """
    Motor de Consulta Inteligente (v0.6.3).
    Substitui lógicas de PROCV/XLOOKUP via Joins eficientes.
    """
    def __init__(self):
        pass

    def find_common_columns(self, df_src, df_tgt):
        """Identifica colunas que existem em ambos os datasets (Match exato)."""
        src_cols = set(df_src.columns)
        tgt_cols = set(df_tgt.columns)
        return list(src_cols & tgt_cols)

    def suggest_key_pair(self, df_src, df_tgt):
        """Sugerir par de chaves baseado em nome e unicidade simples."""
        # TODO: Evoluir para Fuzzy no Patch 3. No Patch 1 é match exato.
        common = self.find_common_columns(df_src, df_tgt)
        if common:
            # Pega a primeira coluna comum que tenha alta taxa de unicidade
            for col in common:
                u_src = df_src[col].nunique() / len(df_src) if len(df_src) > 0 else 0
                u_tgt = df_tgt[col].nunique() / len(df_tgt) if len(df_tgt) > 0 else 0
                if u_src > 0.8 and u_tgt > 0.8:
                    return col, col
        return None, None
