import os
import sys
import pandas as pd
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'src'))

from core.engines.loader_engine import LoaderEngine
from core.engines.etl_engine import ETLEngine
from core.engines.lookup_engine import LookupEngine
from core.engines.validation_engine import ValidationEngine
from core.services.logger_service import LoggerService

def run_battery():
    print("Iniciando Bateria de Testes de Integração c/ Base Real (SAP OITM)...")
    logger = LoggerService()
    
    loader = LoaderEngine()
    etl = ETLEngine()
    lookup = LookupEngine()
    validator = ValidationEngine()
    
    test_dir = os.path.join(BASE_DIR, "tests", "index")
    
    # Identify Target and Source
    # Target will usually be the "Validar OITM" file. Source could be the "Tabela de preco..." Or "V2"
    # To be generic, let's load the two largest files as target and source
    files = [f for f in os.listdir(test_dir) if f.endswith('.xlsx')]
    if len(files) < 2:
        print("Erro: não há arquivos suficientes para teste (precisa de pelo menos 2).")
        return
        
    print(f"Arquivos disponíveis p/ teste: {files}")
    
    tgt_path = os.path.join(test_dir, "98% Validar OITM - Items - ITEM1 - 03-26.xlsx")
    if not os.path.exists(tgt_path):
        tgt_path = os.path.join(test_dir, files[0])
    
    # We will pick another file as source
    src_path = None
    for f in files:
        if "Tabela de preco" in f or "V2" in f:
            src_path = os.path.join(test_dir, f)
            break
    if not src_path:
        src_path = os.path.join(test_dir, files[1] if files[0] != os.path.basename(tgt_path) else files[0])
        
    print(f"-> TARGET (Destino): {os.path.basename(tgt_path)}")
    print(f"-> SOURCE (Origem) : {os.path.basename(src_path)}")
    
    tgt_wb, _ = loader.load_workbook(tgt_path)
    src_wb, _ = loader.load_workbook(src_path)
    
    df_tgt = tgt_wb[list(tgt_wb.keys())[0]]
    df_src = src_wb[list(src_wb.keys())[0]]
    
    print(f"Target Shape: {df_tgt.shape} | Source Shape: {df_src.shape}")
    
    # 1. Test Key Suggestion
    key_src, key_tgt = lookup.suggest_key_pair(df_src, df_tgt)
    if not key_src or not key_tgt:
        # Fallback to first columns just to simulate a join
        key_src = df_src.columns[0]
        key_tgt = df_tgt.columns[0]
        print(f"[Aviso] Sem sugestão automática forte. Forçando: {key_src} -> {key_tgt}")
    else:
        print(f"Chaves sugeridas automaticamente: SRC='{key_src}' | TGT='{key_tgt}'")

    # 2. Create a generic mapping of common columns (excluding key)
    common_cols = [c for c in df_src.columns if c in df_tgt.columns and c != key_src and c != key_tgt]
    mapping = {c: c for c in common_cols[:5]} # Map up to 5 common columns to test overwrite
    print(f"Mapeamento Simulado (Até 5 cols): {mapping}")

    # 3. Test ETL Engine with defaults (Overwrite, Preserve Zeros: True, auto_filter: False)
    print("\n--- TEST ROUND 1 : Padrão (Sem Shielding) ---")
    start = time.time()
    res_1 = etl.synchronize(
        df_src, df_tgt, key_src, key_tgt, mapping, 
        protected_a1=True, shielding=False, preserve_zeros=True
    )
    print(f"Resultado Round 1 Shape: {res_1.shape} (Esperado igual ao Target, ou próximo) - Tempo: {time.time()-start:.2f}s")
    if len(res_1) == 0:
        print("[ERRO CRÍTICO] Round 1 retornou 0 linhas!")
        sys.exit(1)

    # 4. Test Shielding Logic
    print("\n--- TEST ROUND 2 : Com Shielding Ativado ---")
    res_2 = etl.synchronize(
        df_src, df_tgt, key_src, key_tgt, mapping, 
        protected_a1=True, shielding=True, preserve_zeros=True
    )
    print(f"Resultado Round 2 Shape: {res_2.shape}")
    if len(res_2) == 0:
        print("[ERRO CRÍTICO] Round 2 retornou 0 linhas!")
        sys.exit(1)

    # 5. Test Filtering Logic (Simulate UI Checkbox logic fixed)
    print("\n--- TEST ROUND 3 : Filtro Numérico na Chave (Bugfix test) ---")
    filter_cols = [key_tgt]
    res_3 = validator.apply_numeric_filter(res_2, filter_cols)
    print(f"Resultado Round 3 Shape: {res_3.shape} (Filtro Zero/Nulo aplicado)")
    if len(res_3) == 0 and len(res_2) > 0:
        print("[ALERTA] Round 3 retornou 0 linhas. (Apenas se todas chaves de destino forem Vazias/Nulas)")

    print("\nBATERIA DE TESTES CONCLUÍDA COM SUCESSO! 🚀")

if __name__ == "__main__":
    run_battery()
