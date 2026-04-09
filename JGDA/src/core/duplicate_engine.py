import pandas as pd
from typing import List, Dict, Tuple, Optional

class DuplicateEngine:
    """
    Motor de Detecção de Identidade e Duplicidade.
    Arquiteto para portabilidade Java: Focado em Entidades e Relatórios Estruturados.
    """
    def __init__(self):
        pass

    def scan_for_duplicates(self, df: pd.DataFrame, subset: List[str] = None) -> Tuple[Dict, pd.DataFrame]:
        """
        Analisa o dataframe em busca de duplicatas.
        Equivalente a um 'IdentityScanService' em Java.
        """
        if subset is None:
            subset = list(df.columns)
            
        # Identificar todas as ocorrências de duplicatas (inclusive a primeira se necessário, mas seguimos 'first' como base)
        is_duplicate = df.duplicated(subset=subset, keep='first')
        df_duplicates = df[is_duplicate].copy()
        
        summary = {
            "total_records": len(df),
            "duplicate_count": len(df_duplicates),
            "integrity_score": (1 - (len(df_duplicates) / len(df))) if len(df) > 0 else 1.0,
            "fields_scanned": subset
        }
        
        return summary, df_duplicates

    def get_frequency_map(self, df: pd.DataFrame, column: str) -> List[Dict]:
        """Gera um mapa de frequências para identificar 'heavy hitters' de duplicidade."""
        if column not in df.columns:
            return []
            
        counts = df[column].value_counts()
        heavy_hitters = counts[counts > 1]
        
        report = []
        for value, count in heavy_hitters.items():
            report.append({
                "value": str(value),
                "count": int(count)
            })
            
        return sorted(report, key=lambda x: x["count"], reverse=True)


# --- Declaração de Versão do Módulo (Genaja Version Hook) ---
from version_hook import declare as _vdeclare
_vdeclare(__name__, "0.7.1", "Motor de detecção de duplicidade tática para validação Shift-Left")
