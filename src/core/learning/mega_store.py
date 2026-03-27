import os
import json
from typing import List, Dict, Any, Optional

class MegaKnowledgeStore:
    """
    Motor de Conhecimento de Alta Densidade (v0.6.7).
    Otimizado para armazenar centenas de milhares de associações estatísticas.
    """
    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        self.storage_path = os.path.join(root_dir, "learn", "mega_knowledge.json")
        self.data = self._load()

    def _load(self) -> Dict[str, Any]:
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass
        return {"associations": {}, "metadata": {"total_cycles": 0, "last_update": ""}}

    def add_evidence(self, src_col: str, tgt_col: str, weight: int = 1):
        """Adiciona uma evidência de mapeamento ao mapa de calor estatístico."""
        key = src_col.strip().lower()
        tgt_key = tgt_col.strip().lower()
        
        if key not in self.data["associations"]:
            self.data["associations"][key] = {}
        
        counts = self.data["associations"][key]
        counts[tgt_key] = counts.get(tgt_key, 0) + weight
        self.data["metadata"]["total_cycles"] += 1

    def get_best_match(self, src_col: str, possible_targets: List[str]) -> Optional[str]:
        """Retorna o alvo estatisticamente mais provável para uma coluna."""
        key = src_col.strip().lower()
        if key not in self.data["associations"]:
            return None
            
        candidates = self.data["associations"][key]
        # Filtrar apenas alvos presentes no dataset atual
        valid_candidates = {t: c for t, c in candidates.items() if t in [pt.lower() for pt in possible_targets]}
        
        if not valid_candidates:
            return None
            
        # Retorna o alvo com maior contagem (maior probabilidade histórica)
        best_lower = max(valid_candidates, key=valid_candidates.get)
        
        # Encontrar o case original do target
        for pt in possible_targets:
            if pt.lower() == best_lower:
                return pt
        return None

    def save(self):
        """Persistência atômica do conhecimento consolidado."""
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
