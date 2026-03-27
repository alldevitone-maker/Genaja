import os
import json
from typing import List, Dict, Any, Optional
from datetime import datetime

class MegaKnowledgeStore:
    """
    Motor de Conhecimento de Alta Densidade Probabilístico (v0.6.8).
    Implementa estratificação de estados: REJECTED, OBSERVED, INFERRED, SUGGESTED, CONFIRMED.
    """
    WEIGHTS = {
        "mapping_candidate_detected": 1,
        "repeated_pattern": 2,
        "schema_similarity": 2,
        "profile_compatibility": 2,
        "user_selected_mapping": 3,
        "runtime_successful_execution": 5,
        "large_dataset_bonus": 2,
        "generic_placeholder_penalty": -5,
        "semantic_conflict_penalty": -4,
        "test_pattern_penalty": -4,
        "single_occurrence_penalty": -2
    }

    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        self.storage_path = os.path.join(root_dir, "learn", "consolidated", "mega_knowledge.json")
        self.quarantine_path = os.path.join(root_dir, "learn", "quarantine", "pollution_log.json")
        self.data = self._load()

    def _load(self) -> Dict[str, Any]:
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass
        return {"associations": {}, "metadata": {"total_cycles": 0, "last_update": "", "version": "0.6.8"}}

    def add_evidence(self, src_col: str, tgt_col: str, reason: str = "mapping_candidate_detected"):
        """Adiciona evidência com peso especializado do protocolo v0.6.8."""
        key = src_col.strip().lower()
        tgt_key = tgt_col.strip().lower()
        
        # Filtro de Poluição (Seção 4)
        if self._is_polluted(tgt_key):
            self._quarantine(src_col, tgt_col, "Pollution Filter: Generic Pattern")
            return

        weight = self.WEIGHTS.get(reason, 1)
        
        if key not in self.data["associations"]:
            self.data["associations"][key] = {}
        
        raw_entry = self.data["associations"][key].get(tgt_key, {"score": 0, "state": "OBSERVED"})
        
        # Adaptador para dados legados (v0.6.7 usava apenas int)
        if isinstance(raw_entry, int):
            entry = {"score": raw_entry, "state": self._classify_state(raw_entry)}
        else:
            entry = raw_entry
            
        entry["score"] += weight
        entry["state"] = self._classify_state(entry["score"])
        
        self.data["associations"][key][tgt_key] = entry
        self.data["metadata"]["total_cycles"] += 1

    def _classify_state(self, score: int) -> str:
        if score < 0: return "REJECTED"
        if score <= 2: return "OBSERVED"
        if score <= 5: return "INFERRED"
        if score <= 8: return "SUGGESTED"
        return "CONFIRMED"

    def _is_polluted(self, col_name: str) -> bool:
        """Detecta padrões genéricos (coluna1, valor, etc)."""
        generic_patterns = ["coluna", "column", "valor", "field", "campo", "unknown", "item"]
        name = col_name.lower()
        
        # Caso clássico: "coluna1", "colunaA"
        if any(p in name for p in ["coluna", "column"]) and any(c.isdigit() or len(name) <= 8 for c in name):
            return True
            
        # Nomes curtos genéricos
        if name in ["valor", "val", "data", "id", "x", "y"]:
            return False # ID e Data são úteis, mas "valor" sozinho é vago
            
        return False

    def _quarantine(self, src: str, tgt: str, reason: str):
        """Salva mapeamento suspeito na quarentena."""
        log = []
        if os.path.exists(self.quarantine_path):
            try:
                with open(self.quarantine_path, "r") as f: log = json.load(f)
            except: pass
        
        log.append({
            "timestamp": str(datetime.now()),
            "source": src,
            "target": tgt,
            "reason": reason
        })
        
        with open(self.quarantine_path, "w") as f:
            json.dump(log, f, indent=2)

    def get_best_match(self, src_col: str, possible_targets: List[str]) -> Optional[str]:
        """Retorna o alvo mais provável (maior score) que não seja REJECTED."""
        key = src_col.strip().lower()
        if key not in self.data["associations"]: return None
            
        candidates = self.data["associations"][key]
        valid_targets = [pt.lower() for pt in possible_targets]
        
        best_tgt = None
        max_score = -float('inf')
        
        for tgt, entry in candidates.items():
            if entry["state"] == "REJECTED": continue
            if tgt in valid_targets:
                if entry["score"] > max_score:
                    max_score = entry["score"]
                    best_tgt = tgt
        
        if not best_tgt: return None
        
        for pt in possible_targets:
            if pt.lower() == best_tgt: return pt
        return None

    def save(self):
        self.data["metadata"]["last_update"] = str(datetime.now())
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
