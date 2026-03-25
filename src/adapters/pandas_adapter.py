import pandas as pd
import os

class PandasAdapter:
    """
    Adapter para Pandas (v0.6.0). 
    Encapsula o uso de bibliotecas externas para proteger o Core Engine.
    """
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
