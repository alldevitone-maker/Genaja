from typing import List, Dict, Optional, Any
import pandas as pd
import numpy as np
from core.learning.learning_store import LearningStore

class LearningLogger:
    """
    Serviço de Registro de Aprendizado (v0.6.3 - Patch 4).
    Orquestra a captura de metadados ao final do fluxo ETL.
    """
    def __init__(self, root_dir: str):
        self.store = LearningStore(root_dir)

    def log_execution(self, 
                      source_columns: List[str], 
                      target_columns: List[str], 
                      mapping: Dict[str, str], 
                      keys: tuple, 
                      row_count: int,
                      df_src: Optional[pd.DataFrame] = None,
                      sheet_name: Optional[str] = None):
        """
        Registra uma execução bem-sucedida se houver dados válidos.
        p_sheet_name (v0.6.6): Nome da aba utilizada no ETL.
        """
        if not mapping or not keys or not all(keys):
            return False
            
        # 1. Gerar Perfis de Dados (v0.6.5 Profiling)
        profiles = {}
        if df_src is not None:
            profiles = self._profile_dataframe(df_src, list(mapping.keys()))

        # 2. Montar Dados de Execução
        execution = {
            "sheet": sheet_name, # v0.6.6
            "source_columns": source_columns,
            "target_columns": target_columns,
            "source_signature": self.store.generate_signature(source_columns),
            "target_signature": self.store.generate_signature(target_columns),
            "selected_key_src": keys[0],
            "selected_key_tgt": keys[1],
            "mapping_applied": mapping,
            "row_count": row_count,
            "column_profiles": profiles
        }
        
        # 3. Persistir
        self.store.save_execution(execution)
        return True

    def log_workbook_structure(self, workbook: Dict[str, pd.DataFrame]):
        """Aprende a estrutura de todas as abas sem necessariamente executar um ETL (v0.6.6)."""
        for sheet_name, df in workbook.items():
            # Limitar profiling às primeiras 2000 linhas (v0.6.6 Performance)
            df_sampled = df.head(2000)
            
            # Registra como uma execução de "treinamento passivo"
            execution = {
                "sheet": sheet_name,
                "source_columns": list(df.columns),
                "source_signature": self.store.generate_signature(list(df.columns)),
                "row_count": len(df),
                "column_profiles": self._profile_dataframe(df_sampled, list(df.columns)),
                "is_passive_learning": True # Flag para distinguir de execuções reais
            }
            self.store.save_execution(execution)

    def _profile_dataframe(self, df: pd.DataFrame, columns: List[str]) -> Dict[str, Any]:
        """Gera um resumo estatístico e de tipo para cada coluna mapeada."""
        profiles = {}
        for col in columns:
            if col not in df.columns: continue
            
            series = df[col].dropna()
            if series.empty: continue
            
            # Amostra de tipos e comprimentos
            sample = series.head(100)
            is_numeric = pd.to_numeric(sample, errors='coerce').notnull().all()
            
            profiles[col] = {
                "dtype": str(df[col].dtype),
                "is_numeric": bool(is_numeric),
                "avg_len": float(sample.astype(str).str.len().mean()),
                "unique_ratio": float(len(series.unique()) / len(series)) if len(series) > 0 else 0
            }
        return profiles
