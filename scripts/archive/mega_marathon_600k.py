import os
import sys
import pandas as pd
import json
import time
import random

# Adicionar src ao path
sys.path.append(os.path.abspath("src"))

from core.learning.mega_store import MegaKnowledgeStore
from core.learning.suggestion_engine import HistoricalSuggestionEngine
from core.engines.loader_engine import LoaderEngine

def main():
    root_dir = os.getcwd()
    source_dir = r"C:\Users\ti01\Desktop\learn manchine"
    
    # 1. Inicializar
    mega_store = MegaKnowledgeStore(root_dir)
    loader = LoaderEngine()
    engine = HistoricalSuggestionEngine(root_dir)
    
    files = [os.path.join(source_dir, f) for f in os.listdir(source_dir) if f.endswith(('.xlsx', '.xls', '.csv'))]
    
    print(f"--- Iniciando MEGA-MARATONA (600.000 Ciclos) ---")
    
    # 2. Cache total de datasets
    all_sheets = []
    for f in files:
        try:
            if f.endswith('.csv'):
                df = pd.read_csv(f)
                all_sheets.append({"name": os.path.basename(f), "cols": list(df.columns)})
            else:
                workbook, _ = loader.load_workbook(f)
                for name, df in workbook.items():
                    all_sheets.append({"name": f"{os.path.basename(f)}[{name}]", "cols": list(df.columns)})
        except:
            continue
            
    num_sheets = len(all_sheets)
    if num_sheets < 2:
        print("Dados insuficientes para maratona.")
        return

    print(f"Base de dados carregada: {num_sheets} abas disponíveis.")
    
    # 3. Ciclo de Aprendizado Massivo
    total_cycles = 600000
    batch_size = 50000
    start_time = time.time()
    
    print(f"Processando {total_cycles} combinações estocásticas...")
    
    for i in range(1, total_cycles + 1):
        # Seleção estocástica de duas abas
        s1, s2 = random.sample(all_sheets, 2)
        
        # Subsampling de colunas (simula usuário escolhendo subconjunto)
        cols1 = random.sample(s1["cols"], k=random.randint(1, len(s1["cols"])))
        cols2 = random.sample(s2["cols"], k=random.randint(1, len(s2["cols"])))
        
        # Simular motor de sugestão (usando fuzzy/exact para gerar "verdade")
        # Nota: Estamos ensinando ao MegaKnowledge o que o motor fuzzy/exato descobre
        for c1 in cols1:
            # Match exato ou fuzzy simulado
            for c2 in cols2:
                if c1.lower() == c2.lower():
                    mega_store.add_evidence(c1, c2, weight=1)
                elif c1.lower() in c2.lower() or c2.lower() in c1.lower():
                    # Peso menor para matches parciais
                    mega_store.add_evidence(c1, c2, weight=1)

        if i % batch_size == 0:
            elapsed = time.time() - start_time
            print(f"BATERIA {i}/{total_cycles} concluida... ({elapsed:.1f}s)")
            mega_store.save() # Persistência incremental para segurança

    mega_store.save()
    total_time = time.time() - start_time
    
    print(f"--- MEGA-MARATONA FINALIZADA ---")
    print(f"Tempo total: {total_time:.1f}s")
    print(f"Densidade de conhecimento: {len(mega_store.data['associations'])} colunas primárias mapeadas.")
    
    # Gerar relatório final no Desktop
    report = {
        "status": "Genaja v0.6.7 MEGA-MARATHON COMPLETE",
        "cycles": total_cycles,
        "total_time_seconds": total_time,
        "knowledge_density": len(mega_store.data['associations']),
        "storage_path": mega_store.storage_path
    }
    with open(r"C:\Users\ti01\Desktop\MEGA_INSIGHTS_v0.6.7.json", "w") as f:
        json.dump(report, f, indent=4)

if __name__ == "__main__":
    main()
