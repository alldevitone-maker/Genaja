import os
import sys
import json

# Adicionar src ao path
sys.path.append(os.path.abspath("src"))

from core.learning.suggestion_engine import HistoricalSuggestionEngine
from core.learning.curated_store import CuratedStore
from core.learning.mega_store import MegaKnowledgeStore

def run_test():
    root = os.getcwd()
    engine = HistoricalSuggestionEngine(root)
    
    # Limpar qualquer rastro de teste anterior
    try:
        os.remove(os.path.join(root, "learn", "curated", "master_rules.json"))
        os.remove(os.path.join(root, "learn", "consolidated", "mega_knowledge.json"))
    except:
        pass
        
    mega = MegaKnowledgeStore(root)
    curated = CuratedStore(root)
    
    src_cols = ["ID_PRODUTO"]
    tgt_cols = ["ItemCode", "ItemName"]
    
    print("--- Teste de Prioridade Genaja v0.6.9 ---")
    
    # 1. Sem nada (None)
    res1 = engine.get_smart_suggestions(src_cols, tgt_cols)
    print(f"1. Sem regras: {res1['mapping']} (Source: {res1['source']})")
    
    # 2. Com MegaBrain (Estatístico)
    mega.add_evidence("id_produto", "ItemName", reason="runtime_successful_execution")
    mega.save()
    
    # Reload engine to pick up new files
    engine = HistoricalSuggestionEngine(root)
    res2 = engine.get_smart_suggestions(src_cols, tgt_cols)
    print(f"2. Com MegaBrain: {res2['mapping']} (Source: {res2['source']})")
    
    # 3. Com Master Rule (Priority 0)
    # Deve SOBREPOR o MegaBrain
    curated.promote_mapping("id_produto", "ItemCode", reason="Manual Curation")
    curated.save()
    
    engine = HistoricalSuggestionEngine(root)
    res3 = engine.get_smart_suggestions(src_cols, tgt_cols)
    print(f"3. Com Master Rule: {res3['mapping']} (Source: {res3['source']})")
    
    if res3['source'] == 'curated' and res3['mapping']['ID_PRODUTO'] == 'ItemCode':
        print("\n✅ SUCESSO: Prioridade 0 (Curated) validada!")
    else:
        print("\n❌ FALHA: Prioridade incorreta.")

if __name__ == "__main__":
    run_test()
