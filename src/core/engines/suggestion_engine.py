import os
import glob
from core.services.logger_service import LoggerService

class SuggestionEngine:
    """
    Motor de Sugestão de Arquivos (v0.6.0).
    Heurística v0.4.8 para encontrar arquivos recentes e relevantes.
    """
    def __init__(self):
        self.logger = LoggerService()
        self.common_paths = [
            os.path.join(os.path.expanduser("~"), "Downloads"),
            os.path.join(os.path.expanduser("~"), "Documents"),
            os.getcwd()
        ]

    def suggest_files(self):
        """Busca os arquivos .xlsx mais recentes e os categoriza."""
        all_files = []
        for path in self.common_paths:
            if not os.path.exists(path): continue
            pattern = os.path.join(path, "*.xlsx")
            files = glob.glob(pattern)
            for f in files:
                all_files.append({
                    'path': f,
                    'mtime': os.path.getmtime(f),
                    'name': os.path.basename(f).lower()
                })
        
        # Ordenar por data de modificação (mais recente primeiro)
        all_files.sort(key=lambda x: x['mtime'], reverse=True)
        
        src_best = None
        tgt_best = None
        
        # Heurística: Nomes comuns
        for f in all_files[:10]: # Analisar apenas os 10 mais recentes
            if any(k in f['name'] for k in ['export', 'sap', 'origem', 'relatorio', 'report', 'src']):
                if not src_best: src_best = f['path']
            elif any(k in f['name'] for k in ['master', 'destino', 'final', 'tgt', 'base']):
                if not tgt_best: tgt_best = f['path']
                
        # Fallback: Os dois mais recentes se não encontrar por nome
        if not src_best and all_files: src_best = all_files[0]['path']
        if not tgt_best and len(all_files) > 1: tgt_best = all_files[1]['path']
        
        return src_best, tgt_best
