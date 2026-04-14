import os
import sys
import pandas as pd
import json
import time
import random

# Adicionar src ao path
sys.path.append(os.path.abspath("src"))

from core.learning.mega_store import MegaKnowledgeStore
from core.engines.loader_engine import LoaderEngine

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    source_dir = os.path.join(root_dir, "data", "marathon_source")
    bigdata_dir = os.path.join(root_dir, "data", "bigdata")
    
    # Garantir que os diretórios existam para evitar crash de IO
    os.makedirs(source_dir, exist_ok=True)
    os.makedirs(bigdata_dir, exist_ok=True)
    
    # 1. Inicializar
    mega_store = MegaKnowledgeStore(root_dir)
    loader = LoaderEngine()
    
    print(f"--- Iniciando MEGA-MARATONA FASE 2 (1.000.000 Ciclos) ---")
    
    # 2. Re-aprender do BigData (1000 relatórios anteriores)
    print(f"Buscando relatórios legados em {bigdata_dir}...")
    report_files = [os.path.join(bigdata_dir, f) for f in os.listdir(bigdata_dir) 
                    if (f.startswith("report_") or f.startswith("marathon_report_")) and f.endswith(".json")]
    
    ingested = 0
    for rf in report_files:
        try:
            with open(rf, 'r', encoding='utf-8') as f:
                data = json.load(f)
                mapping = data.get("learned_mapping", {})
                for src, tgt in mapping.items():
                    mega_store.add_evidence(src, tgt, weight=2) # Peso dobrado para dados validados
                ingested += 1
        except:
            continue
    print(f"DONE Ingestao completa: {ingested} relatorios incorporados ao cerebro.")

    # 3. Cache total de datasets para simulação
    files = [os.path.join(source_dir, f) for f in os.listdir(source_dir) if f.endswith(('.xlsx', '.xls', '.csv'))]
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
    print(f"Base de dados para simulação: {num_sheets} abas disponíveis.")
    
    # 4. Mega Ciclo (1.000.000)
    total_cycles = 1000000
    batch_size = 100000
    start_time = time.time()
    
    print(f"Executando {total_cycles} ciclos de aprendizado cruzado...")
    
    for i in range(1, total_cycles + 1):
        s1, s2 = random.sample(all_sheets, 2)
        
        # Subsampling de colunas (estocástico)
        k1 = random.randint(1, len(s1["cols"]))
        k2 = random.randint(1, len(s2["cols"]))
        cols1 = random.sample(s1["cols"], k=k1)
        cols2 = random.sample(s2["cols"], k=k2)
        
        # Simulação de Reforço de Mapeamento
        for c1 in cols1:
            for c2 in cols2:
                # Lógica simplificada de "verdade" para aprendizado de pesos
                if c1.lower() == c2.lower() or c1.lower() in c2.lower() or c2.lower() in c1.lower():
                    mega_store.add_evidence(c1, c2, weight=1)

        if i % batch_size == 0:
            elapsed = time.time() - start_time
            print(f"BATERIA {i}/{total_cycles} completa... ({elapsed:.1f}s)")
            mega_store.save()

    mega_store.save()
    total_time = time.time() - start_time
    
    # 5. Relatório Ultimato no Desktop
    report = {
        "status": "Genaja v0.6.7 ULTIMATE MARATHON COMPLETE",
        "total_cycles": total_cycles + ingested,
        "phase2_simulations": total_cycles,
        "legacy_ingested": ingested,
        "total_time_seconds": total_time,
        "knowledge_density": len(mega_store.data['associations']),
        "brain_location": mega_store.storage_path
    }
    report_path = os.path.join(root_dir, "data", "ULTIMATE_BRAIN_REPORT.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=4)

    print(f"--- MEGA-MARATONA FASE 2 FINALIZADA EM {total_time:.1f}s ---")

if __name__ == "__main__":
    main()
