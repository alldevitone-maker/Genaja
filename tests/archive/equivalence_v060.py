import sys
import os
import pandas as pd

# Path injection
sys.path.append(os.path.abspath("src"))

from core.engines.etl_engine import ETLEngine
from core.engines.mapping_engine import MappingEngine
from core.engines.loader_engine import LoaderEngine

def test_equivalence_v048():
    print("[START] Iniciando Testes de Equivalencia Funcional (v0.4.8 vs v0.6.0)...")
    
    # 1. Testar Mapping Engine
    mapper = MappingEngine()
    df_src = pd.DataFrame({'SKU': ['101', '102', '103'], 'Valor': [10, 20, 30]})
    df_tgt = pd.DataFrame({'COD': ['101', '102', '999'], 'Nome': ['A', 'B', 'C']})
    
    matches = mapper.suggest_primary_keys(df_src, df_tgt)
    print(f"  - Mapping Match Found: {matches[0]['src']} -> {matches[0]['tgt']} (Score: 2)")
    assert matches[0]['src'] == 'SKU' and matches[0]['tgt'] == 'COD'
    
    # 2. Testar ETL Engine (Merge Logic)
    etl = ETLEngine()
    mapping = {'Valor': 'PRECO_FINAL'}
    # Sync: Overwrites or creates 'PRECO_FINAL' column using 'Valor' data
    df_res = etl.synchronize(df_src, df_tgt, 'SKU', 'COD', mapping, 'COD')
    
    print(f"  - ETL Sync result columns: {df_res.columns.tolist()}")
    assert 'PRECO_FINAL' in df_res.columns
    assert df_res.iloc[0]['PRECO_FINAL'] == 10
    
    # Na v0.4.8, o merge é LEFT. O SKU 103 (index 2) permanece no resultado 
    # e ganha o valor 30 na coluna PRECO_FINAL (conforme mapeamento).
    assert df_res.iloc[2]['PRECO_FINAL'] == 30
    
    print("\n[SUCCESS] O novo motor v0.6.0 reflete a logica confiavel da v0.4.8.")

if __name__ == "__main__":
    test_equivalence_v048()
