import pandas as pd
import os
from core.connectors.base_connector import BaseConnector

class PandasAdapter(BaseConnector):
    """
    Adapter para Pandas. 
    Implementa BaseConnector para suportar o novo core agnóstico.
    """
    
    def validate_connection(self) -> bool:
        path = self.config.get("path")
        return os.path.exists(path) if path else False

    def fetch_metadata(self) -> list:
        df = self.preview(limit=1)
        return list(df.columns)

    def preview(self, limit: int = 10) -> pd.DataFrame:
        path = self.config.get("path")
        return pd.read_excel(path, nrows=limit)

    def fetch_all(self) -> pd.DataFrame:
        path = self.config.get("path")
        return pd.read_excel(path)

    # --- METODOS LEGACY PARA COMPATIBILIDADE ---
    @staticmethod
    def read_excel(path, **kwargs):
        return pd.read_excel(path, **kwargs)

    @staticmethod
    def write_excel(df, path, index=False):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        df.to_excel(path, index=index)
        return path

    @staticmethod
    def get_columns(df):
        return [str(c) for c in df.columns]

    @staticmethod
    def filter_by_key(df, key_col, keys_set):
        return df[df[key_col].isin(keys_set)].copy()


# --- Declaração de Versão do Módulo (Genaja Version Hook) ---
from version_hook import declare as _vdeclare
from version import __version__
_vdeclare(__name__, __version__, "Adapter para Pandas com suporte a excel e filtragem multi-chave")
