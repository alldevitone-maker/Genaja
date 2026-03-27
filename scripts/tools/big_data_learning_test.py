import os
import sys
import pandas as pd
import json
import time

# Adicionar src ao path
sys.path.append(os.path.abspath("src"))

from core.learning.learning_logger import LearningLogger
from core.learning.suggestion_engine import HistoricalSuggestionEngine
from core.engines.loader_engine import LoaderEngine
from services.logger_service import LoggerService

def main():
    LoggerService.setup()
    source_dir = r"C:\Users\ti01\Desktop\learn manchine"
    target_dir = r"C:\Users\ti01\Desktop\BigData"
    os.makedirs(target_dir, exist_ok=True)

    loader = LoaderEngine()
    logger = LearningLogger(os.getcwd())
    engine = HistoricalSuggestionEngine(os.getcwd())

    files = [os.path.join(source_dir, f) for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]
    
    print(f"--- Iniciando Super Maratona (1000+ Testes) ---")

    # 1. Carregar TODOS os Workbooks e coletar TODAS as abas
    all_sheets = []
    for f in files:
        try:
            workbook, _ = loader.load_workbook(f)
            for sheet_name, df in workbook.items():
                all_sheets.append({
                    "file_path": f,
                    "file_name": os.path.basename(f),
                    "sheet_name": sheet_name,
                    "df": df,
                    "cols": list(df.columns)
                })
        except Exception as e:
            print(f"Erro ao carregar {f}: {e}")

    total_sheets = len(all_sheets)
    print(f"Detectadas {total_sheets} abas úteis em {len(files)} arquivos.")
    
    total_cycles = 0
    max_tests = 1000
    
    # 2. Cruzamento Massivo Sheet-to-Sheet
    for i in range(total_sheets):
        if total_cycles >= max_tests: break
        
        for j in range(total_sheets):
            if i == j: continue  
            if total_cycles >= max_tests: break
            
            s1 = all_sheets[i]
            s2 = all_sheets[j]
            
            # 1. Sugestão Contextual
            src_profiles = logger._profile_dataframe(s1["df"].head(2000), s1["cols"])
            suggestions = engine.get_smart_suggestions(s1["cols"], s2["cols"], src_profiles=src_profiles)
            
            mapping = suggestions["mapping"]
            if not mapping:
                mapping = {c: c for c in s1["cols"] if c in s2["cols"]}

            if mapping:
                # 2. Log de Aprendizado (Multi-Sheet)
                logger.log_execution(
                    source_columns=s1["cols"],
                    target_columns=s2["cols"],
                    mapping=mapping,
                    keys=("ID", "ID"),
                    row_count=len(s1["df"]),
                    df_src=s1["df"],
                    sheet_name=s1["sheet_name"]
                )
                
                # 3. Gerar Relatório de Ciclo
                report = {
                    "cycle_id": total_cycles,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "source": f"{s1['file_name']} [{s1['sheet_name']}]",
                    "target": f"{s2['file_name']} [{s2['sheet_name']}]",
                    "learned_mapping": mapping,
                    "confidence": suggestions["confidence"],
                    "source_method": suggestions["source"],
                    "profiling_status": "active" if src_profiles else "none"
                }
                
                report_file = os.path.join(target_dir, f"marathon_report_{total_cycles:04d}.json")
                with open(report_file, 'w', encoding='utf-8') as rf:
                    json.dump(report, rf, indent=4, ensure_ascii=False)
                
                total_cycles += 1
                if total_cycles % 50 == 0:
                    print(f"✅ Processados {total_cycles}/1000 ciclos...")

    print(f"--- Maratona Finalizada! {total_cycles} novos relatórios gerados em BigData ---")

if __name__ == "__main__":
    main()
