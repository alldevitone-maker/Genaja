import pandas as pd
import numpy as np
from typing import Any, Optional

class TypeConverter:
    """
    Serviço de Conversão e Normalização de Tipos (v0.6.3).
    Focado em interoperabilidade de tipos (Java-like strictness).
    """
    def __init__(self):
        pass

    def parse_numeric(self, series: pd.Series) -> pd.Series:
        """
        Normaliza strings para Float/Int com foco em locales híbridos (BR/EN).
        Lida com ponto como milhar e vírgula como decimal (ou vice-versa).
        """
        if series.dtype in [np.float64, np.int64]:
            return series
            
        # Higienização: remove símbolos monetários e espaços
        s = series.astype(str).str.replace(r'[^\d,\.-]', '', regex=True)
        
        # Heurística PT-BR: Se houver vírgula e ponto, o ponto vira nada e a vírgula ponto.
        # Ex: 1.000,50 -> 1000.50
        mask_mixed = s.str.contains(r'\.', regex=True) & s.str.contains(r',', regex=True)
        s.loc[mask_mixed] = s.loc[mask_mixed].str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
        
        # Fallback vírgula simples: 10,50 -> 10.50
        s = s.str.replace(',', '.', regex=False)
        
        return pd.to_numeric(s, errors='coerce')

    def parse_date(self, series: pd.Series) -> pd.Series:
        """Converte para datetime ISO-8601 (Standard Table format)."""
        return pd.to_datetime(series, errors='coerce')

    def normalize_string(self, series: pd.Series, to_upper: bool = True) -> pd.Series:
        """Normalização de strings para chaves primárias e buscas."""
        s = series.astype(str).str.strip()
        if to_upper:
            s = s.str.upper()
        return s.replace(['NAN', 'NONE', 'NAT', ''], np.nan)
