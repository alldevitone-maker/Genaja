import os
from version import __version__
import glob
from core.services.logger_service import LoggerService

class SuggestionEngine:
    """
    Motor de Sugestão de Arquivos — Heurística de busca por arquivos recentes e relevantes.
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
        
        # Upgrade MDM: Classificação Inteligente de Arquivos
        from core.engines.mdm.mdm_engine import MDMEngine
        mdm = MDMEngine()
        
        for f in all_files[:15]: # Analisar os 15 mais recentes
            res = mdm.resolve(f['name'])
            
            if res["category_code"] == "SRC_FILE" and res["status"] == "AUTO_CLASSIFIED":
                if not src_best: src_best = f['path']
            elif res["category_code"] == "TGT_FILE" and res["status"] == "AUTO_CLASSIFIED":
                if not tgt_best: tgt_best = f['path']
                
        # Caso não encontre via MDM direto, tenta fallback nas chaves de negócio
        if not src_best or not tgt_best:
            for f in all_files[:10]:
                res = mdm.resolve(f['name'])
                # Se for financeiro ou fiscal, provavelmente é origem
                if res["category_code"] in ["FIN", "FISC"] and not src_best:
                    src_best = f['path']
        
        # Fallback Final: Os dois mais recentes se não encontrar por inteligência
        if not src_best and all_files: src_best = all_files[0]['path']
        if not tgt_best and len(all_files) > 1: tgt_best = all_files[1]['path']
        
        return src_best, tgt_best


# --- Declaração de Versão do Módulo (Genaja Version Hook) ---
from version_hook import declare as _vdeclare
_vdeclare(__name__, __version__, "Motor de sugestão de arquivos recentes por heurística de nome")
