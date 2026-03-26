from typing import List, Dict, Any, Optional
from core.learning.learning_store import LearningStore
from migration.schema_mapper import SchemaMapper
from core.lookup_engine import LookupEngine

class HistoricalSuggestionEngine:
    """
    Motor de Sugestão Contextual (v0.6.3 - Patch 4).
    Prioridade (Patch 4): 1. Histórico, 2. Fuzzy, 3. Exato.
    """
    def __init__(self, root_dir: str):
        self.store = LearningStore(root_dir)
        self.fuzzy = SchemaMapper()
        self.exact = LookupEngine()

    def get_smart_suggestions(self, src_cols: List[str], tgt_cols: List[str]) -> Dict[str, Any]:
        """
        Gera sugestões orquestradas por prioridade.
        Retorno: {
           "mapping": {col: target},
           "confidence": float,
           "source": "history" | "fuzzy" | "exact"
        }
        """
        # 1. Tentar Histórico (Prioridade 1)
        history_suggestion = self._get_from_history(src_cols, tgt_cols)
        if history_suggestion:
            return {
                "mapping": history_suggestion["mapping"],
                "confidence": history_suggestion["confidence"],
                "source": "history"
            }
            
        # 2. Tentar Fuzzy (Prioridade 2)
        fuzzy_matches = self.fuzzy.suggest_matches(src_cols, tgt_cols)
        if fuzzy_matches:
            # Converte formato {src: {target, score}} para {src: target}
            mapping = {s: v["target"] for s, v in fuzzy_matches.items()}
            return {
                "mapping": mapping,
                "confidence": 0.7,
                "source": "fuzzy"
            }
            
        # 3. Tentar Exato (Prioridade 3)
        common = self.exact.find_common_columns_mock(src_cols, tgt_cols) # Assumindo list match
        if common:
            return {
                "mapping": {c: c for c in common},
                "confidence": 1.0,
                "source": "exact"
            }
            
        return {"mapping": {}, "confidence": 0.0, "source": "none"}

    def _get_from_history(self, src_cols: List[str], tgt_cols: List[str]) -> Optional[Dict]:
        """Busca no log por assinaturas semelhantes."""
        log = self.store.load_log()
        sig_src = self.store.generate_signature(src_cols)
        sig_tgt = self.store.generate_signature(tgt_cols)
        
        candidates = []
        for ex in log["executions"]:
            if ex.get("source_signature") == sig_src and ex.get("target_signature") == sig_tgt:
                candidates.append(ex)
                
        if not candidates:
            return None
            
        # Priorizar a que tem maior usage_count (mais frequente)
        best = max(candidates, key=lambda x: x.get("usage_count", 1))
        
        return {
            "mapping": best["mapping_applied"],
            "confidence": 0.9,
            "keys": (best["selected_key_src"], best["selected_key_tgt"])
        }
