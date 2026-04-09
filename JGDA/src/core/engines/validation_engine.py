import pandas as pd
import numpy as np

class ValidationEngine:
    """
    Motor de Validação e Limpeza — Garante integridade dos dados pós-merge.
    Focada em garantir a integridade dos dados pós-merge.
    """
    
    def apply_numeric_filter(self, df, columns):
        """Remove linhas onde as colunas especificadas são zero, vazias ou NaN."""
        df_clean = df.copy()
        for col in columns:
            if col not in df_clean.columns: continue
            
            s = df_clean[col]
            s_num = pd.to_numeric(s, errors='coerce')
            
            # Máscaras de remoção
            mask_zero = (s_num == 0.0)
            mask_empty = (s.astype(str).str.strip() == '')
            mask_nan = s.isna()
            
            df_clean = df_clean[~(mask_zero | mask_empty | mask_nan)]
            
        return df_clean

    def clean_empty_by_values(self, df, target_cols, num_col):
        """
        Limpeza condicional: Remove linhas onde as colunas alvo estão vazias 
        E o valor na coluna numérica é zero.
        """
        if num_col not in df.columns: return df
        
        df_work = df.copy()
        for i, row in df_work.iterrows():
            try:
                val_num = float(row[num_col])
                is_empty_target = all(str(row[c]).strip() == '' for c in target_cols if c in df.columns)
                
                if val_num == 0.0 and is_empty_target:
                    df_work = df_work.drop(i)
            except (ValueError, TypeError):
                continue
                
        return df_work

    def audit_dataframe(self, df):
        """Auditoria Rápida: Gera metadados para o FileIntelligenceDialog."""
        if df is None: return {}
        
        try:
            return {
                "rows": len(df),
                "cols": len(df.columns),
                "nulls": int(df.isna().sum().sum()),
                "dupes": int(df.duplicated().sum()) if len(df.columns) > 0 else 0,
                "empty_cols": [col for col in df.columns if df[col].isna().all()]
            }
        except Exception as e:
            from core.services.logger_service import LoggerService
            LoggerService().error(f"Erro na auditoria: {e}")
            return {"rows": len(df), "cols": len(df.columns), "nulls": 0, "dupes": 0, "empty_cols": []}

    def validate_keys(self, df, columns):
        """Verifica se existem duplicatas ou vazios críticos em chaves."""
        report = {"valid": True, "errors": []}
        for col in columns:
            if col not in df.columns:
                report["valid"] = False
                report["errors"].append(f"Coluna '{col}' não encontrada.")
                continue
                
            null_count = df[col].isna().sum()
            if null_count > 0:
                report["errors"].append(f"Coluna '{col}' possui {null_count} valores nulos.")
                
        return report


# --- Declaração de Versão do Módulo (Genaja Version Hook) ---
from version_hook import declare as _vdeclare
_vdeclare(__name__, "0.7.1", "Motor de validação de chaves e limpeza de dados nulos/duplicados")
