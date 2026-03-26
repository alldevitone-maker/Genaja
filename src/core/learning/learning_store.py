import os
import json
import hashlib
from datetime import datetime
from typing import List, Dict, Any, Optional

class LearningStore:
    """
    Motor de Persistência de Aprendizado (v0.6.3 - Patch 4).
    Armazena metadados de execução em .genaja/learning_log.json.
    """
    LOG_VERSION = "1.0"
    MAX_RECORDS = 500
    
    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        self.genaja_dir = os.path.join(root_dir, ".genaja")
        self.log_path = os.path.join(self.genaja_dir, "learning_log.json")
        
    def _ensure_dir(self):
        if not os.path.exists(self.genaja_dir):
            os.makedirs(self.genaja_dir)
            
    def generate_signature(self, columns: List[str]) -> str:
        """Gera um hash único baseado na lista ordenada de colunas."""
        if not columns: return ""
        ordered = sorted([str(c).strip().lower() for c in columns])
        content = "|".join(ordered)
        return hashlib.md5(content.encode()).hexdigest()

    def load_log(self) -> Dict[str, Any]:
        """Carrega o log local ou retorna estrutura inicial se não existir."""
        if not os.path.exists(self.log_path):
            return {"log_version": self.LOG_VERSION, "executions": []}
            
        try:
            with open(self.log_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data
        except (json.JSONDecodeError, IOError):
            return {"log_version": self.LOG_VERSION, "executions": []}

    def save_execution(self, execution_data: Dict[str, Any]):
        """Append seguro e inteligente de uma nova execução."""
        self._ensure_dir()
        log = self.load_log()
        
        # 1. Encontrar Duplicatas de Assinatura p/ incrementar usage_count
        new_sig_src = execution_data.get("source_signature")
        new_sig_tgt = execution_data.get("target_signature")
        new_mapping = execution_data.get("mapping_applied")
        new_keys = (execution_data.get("selected_key_src"), execution_data.get("selected_key_tgt"))
        
        found = False
        for ex in log["executions"]:
            if (ex.get("source_signature") == new_sig_src and 
                ex.get("target_signature") == new_sig_tgt and
                ex.get("mapping_applied") == new_mapping and
                ex.get("selected_key_src") == new_keys[0] and
                ex.get("selected_key_tgt") == new_keys[1]):
                
                ex["usage_count"] = ex.get("usage_count", 1) + 1
                ex["timestamp"] = datetime.now().isoformat()
                found = True
                break
        
        if not found:
            # 2. Add Novo Registro
            execution_data["usage_count"] = 1
            execution_data["timestamp"] = datetime.now().isoformat()
            log["executions"].insert(0, execution_data) # Mais recente primeiro
            
        # 3. Truncamento (Ajuste Patch 4)
        if len(log["executions"]) > self.MAX_RECORDS:
            log["executions"] = log["executions"][:self.MAX_RECORDS]
            
        # 4. Escrita Atômica (simplificada via dump foca em estabilidade local)
        with open(self.log_path, "w", encoding="utf-8") as f:
            json.dump(log, f, indent=2, ensure_ascii=False)
