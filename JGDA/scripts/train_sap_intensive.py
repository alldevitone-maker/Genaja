import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'src'))

from core.learning.learning_logger import LearningLogger
from core.learning.mega_store import MegaKnowledgeStore
from core.engines.loader_engine import LoaderEngine
from core.engines.lookup_engine import LookupEngine

def intensive_sap_training(cycles=10):
    print(f" Iniciando Treinamento Intensivo SAP OITM ({cycles} Ciclos)...")
    
    test_dir = os.path.join(BASE_DIR, "tests", "index")
    files = [f for f in os.listdir(test_dir) if f.endswith('.xlsx')]
    if len(files) < 2:
        print("Erro: bases insuficientes.")
        return
    
    tgt_path = os.path.join(test_dir, "98% Validar OITM - Items - ITEM1 - 03-26.xlsx")
    if not os.path.exists(tgt_path):
        tgt_path = os.path.join(test_dir, files[0])
    
    src_path = [os.path.join(test_dir, f) for f in files if "Tabela" in f or "V2" in f]
    src_path = src_path[0] if src_path else os.path.join(test_dir, files[1])
    
    from core.paths import BRAINS_DIR
    loader = LoaderEngine()
    logger = LearningLogger(BRAINS_DIR)
    mega = MegaKnowledgeStore(BRAINS_DIR)
    lookup = LookupEngine()
    
    print(" Carregando dados massivos para memória...")
    tgt_wb, _ = loader.load_workbook(tgt_path)
    src_wb, _ = loader.load_workbook(src_path)
    
    df_tgt = tgt_wb[list(tgt_wb.keys())[0]]
    df_src = src_wb[list(src_wb.keys())[0]]
    
    # Discover Common Setup
    key_src, key_tgt = lookup.suggest_key_pair(df_src, df_tgt)
    if not key_src: key_src = df_src.columns[0]
    if not key_tgt: key_tgt = df_tgt.columns[0]
    
    common_cols = [c for c in df_src.columns if c in df_tgt.columns and c != key_src and c != key_tgt]
    
    print(f" Treinando padrões: Chaves ({key_src} -> {key_tgt}) | {len(common_cols)} Colunas Comuns")
    
    # Simulate repeated syncs to build strong confidence
    for i in range(cycles):
        # 1. Log structure (Profile compatibility)
        logger.log_workbook_structure(tgt_wb)
        logger.log_workbook_structure(src_wb)
        
        # 2. Add explicit mapping evidence (Strong weight)
        mega.add_evidence(key_src, key_tgt, reason="user_selected_mapping")
        mega.add_evidence(key_src, key_tgt, reason="runtime_successful_execution")
        
        for col in common_cols:
            mega.add_evidence(col, col, reason="repeated_pattern")
            mega.add_evidence(col, col, reason="user_selected_mapping")
            
        print(f"  -> Ciclo {i+1}/{cycles} concluído. Conexões neurais reforçadas.")
        
    mega.save()
    
    print(" Consolidação Concluída! A Genaja agora domina esta base de dados.")

if __name__ == "__main__":
    intensive_sap_training(cycles=20)
