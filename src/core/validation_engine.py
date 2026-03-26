import pandas as pd

class ValidationEngine:
    """
    Motor de Validação Estruturada (v0.6.3).
    Detecta problemas de qualidade e integridade nos dados.
    """
    def __init__(self):
        pass

    def audit_dataframe(self, df):
        """Realiza auditoria de integridade para o dialog de pré-análise."""
        if df is None: return {}
        
        report = {
            "col_count": len(df.columns),
            "row_count": len(df),
            "null_cells": int(df.isna().sum().sum()),
            "critical_columns": [] # Colunas com muitos nulos
        }
        
        # Identificar colunas com mais de 50% de nulos
        for col in df.columns:
            null_ratio = df[col].isna().mean()
            if null_ratio > 0.5:
                report["critical_columns"].append({
                    "name": col,
                    "null_ratio": float(null_ratio)
                })
        
        return report
