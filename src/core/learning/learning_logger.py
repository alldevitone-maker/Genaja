from typing import List, Dict, Optional
from core.learning.learning_store import LearningStore

class LearningLogger:
    """
    Serviço de Registro de Aprendizado (v0.6.3 - Patch 4).
    Orquestra a captura de metadados ao final do fluxo ETL.
    """
    def __init__(self, root_dir: str):
        self.store = LearningStore(root_dir)

    def log_execution(self, 
                      source_columns: List[str], 
                      target_columns: List[str], 
                      mapping: Dict[str, str], 
                      keys: tuple, 
                      row_count: int):
        """
        Registra uma execução bem-sucedida se houver dados válidos.
        keys = (src_key, tgt_key)
        """
        # 1. Proteção contra registros inválidos (Ajuste Patch 4)
        if not mapping or not keys or not all(keys):
            return False
            
        # 2. Montar Dados de Execução
        execution = {
            "source_columns": source_columns,
            "target_columns": target_columns,
            "source_signature": self.store.generate_signature(source_columns),
            "target_signature": self.store.generate_signature(target_columns),
            "selected_key_src": keys[0],
            "selected_key_tgt": keys[1],
            "mapping_applied": mapping,
            "row_count": row_count
        }
        
        # 3. Persistir
        self.store.save_execution(execution)
        return True
