import os
import sys
import json
import pandas as pd
from datetime import datetime
import shutil

# Adicionar src ao path
sys.path.append(os.path.abspath("src"))

from core.learning.learning_logger import LearningLogger
from core.engines.loader_engine import LoaderEngine
from core.learning.suggestion_engine import HistoricalSuggestionEngine
from core.learning.curated_store import CuratedStore
from core.paths import LEARN_DIR, BRAINS_DIR

INBOX = os.path.join(LEARN_DIR, "inbox")
RAW = os.path.join(LEARN_DIR, "raw")
REPORTS = os.path.join(LEARN_DIR, "reports")
CONSOLIDATED = os.path.join(LEARN_DIR, "consolidated")

def scan_files():
    files = []
    if not os.path.exists(INBOX):
        os.makedirs(INBOX)
    for f in os.listdir(INBOX):
        if f.lower().endswith((".xlsx", ".csv", ".json", ".xls")):
            files.append(f)
    return files

def process_file(file_name, loader, logger, engine):
    file_path = os.path.join(INBOX, file_name)
    print(f"Ingerindo: {file_name}...")
    
    try:
        # 1. Carregar Dados
        if file_name.endswith('.csv'):
            try:
                df = pd.read_csv(file_path, encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(file_path, encoding='cp1252')
            workbook = {file_name: df}
        else:
            workbook, _ = loader.load_workbook(file_path)
            
        # 2. Aprendizado Passivo (Discovery)
        logger.log_workbook_structure(workbook)
        
        # 3. Cruzamento de Inteligência (Auto-Mapping Simulation)
        curated_store = CuratedStore(BRAINS_DIR)
        all_cols = []
        for sheet_name, df in workbook.items():
            cols = list(df.columns)
            all_cols.append((sheet_name, cols))
            
        for name, cols in all_cols:
            # Simular sugestões contra o próprio histórico para reforçar pesos
            suggestions = engine.get_smart_suggestions(cols, cols)
            if suggestions["mapping"]:
                for src, tgt in suggestions["mapping"].items():
                    if src.lower() == tgt.lower():
                        logger.mega.add_evidence(src, tgt, reason="repeated_pattern")
                        
                        # Promoção Automática (v0.6.9)
                        # Se o mapeamento alcançou maturidade (ex: score 20), vira Regra Master
                        entry = logger.mega.data["associations"].get(src.lower(), {}).get(tgt.lower(), {})
                        if isinstance(entry, dict) and entry.get("score", 0) >= 20:
                            curated_store.promote_mapping(src, tgt, reason="Auto-promotion: High Confidence Score")
        
        logger.mega.save()
        curated_store.save()
        
        # 4. Mover para RAW (Arquivo de Processados)
        os.makedirs(RAW, exist_ok=True)
        shutil.move(file_path, os.path.join(RAW, file_name))
        return True
    except Exception as e:
        print(f"Erro ao processar {file_name}: {e}")
        return False

def generate_report(processed_count, total_files):
    report = {
        "timestamp": str(datetime.now()),
        "status": "SUCCESS" if processed_count == total_files else "PARTIAL",
        "files_processed": processed_count,
        "total_files": total_files,
        "brain_version": "0.6.9",
        "protocol": "Master Agent v0.6.9"
    }

    os.makedirs(REPORTS, exist_ok=True)
    report_path = os.path.join(REPORTS, "brain_feed_report.json")
    
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
        
    # Cópia para o Desktop (Seção 8)
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    desktop_report = os.path.join(desktop, "Genaja_Brain_Feed_Report.json")
    try:
        with open(desktop_report, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
    except:
        pass

def main():
    loader = LoaderEngine()
    logger = LearningLogger(BRAINS_DIR)
    engine = HistoricalSuggestionEngine(BRAINS_DIR)
    
    files = scan_files()
    processed = 0
    
    if not files:
        print("Inbox vazio. Aguardando novos datasets dirty.")
    else:
        for f in files:
            if process_file(f, loader, logger, engine):
                processed += 1
                
    generate_report(processed, len(files))
    print(f"Relatório gerado em {REPORTS}/brain_feed_report.json")
    print("Brain feed completed")

if __name__ == "__main__":
    main()
