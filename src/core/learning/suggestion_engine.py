from typing import List, Dict, Any, Optional
from core.learning.learning_store import LearningStore
from core.learning.curated_store import CuratedStore
from core.learning.mega_store import MegaKnowledgeStore
from migration.schema_mapper import SchemaMapper
from core.services.lookup_engine import LookupEngine

class HistoricalSuggestionEngine:
    """
    Motor de Sugestão Contextual (v0.6.3 - Patch 4).
    Prioridade (Patch 4): 1. Histórico, 2. Fuzzy, 3. Exato.
    """
    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        self.store = LearningStore(root_dir)
        self.mega = MegaKnowledgeStore(root_dir)
        self.curated = CuratedStore(root_dir)
        self.fuzzy = SchemaMapper()
        self.exact = LookupEngine()

    def get_smart_suggestions(self, src_cols: List[str], tgt_cols: List[str], src_profiles: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Gera sugestões orquestradas por prioridade (Histórico > Fuzzy > Perfil > Exato).
        """
        # 0. Tentar Curadoria 'Iron-Clad' (v0.6.9 - Prioridade Master)
        curated_mapping = {}
        for src in src_cols:
            match = self.curated.get_curated_match(src, tgt_cols)
            if match:
                curated_mapping[src] = match
        
        if curated_mapping:
            return {
                "mapping": curated_mapping,
                "confidence": 1.0,
                "source": "curated"
            }

        # 1. Tentar Histórico Estatístico (v0.6.8+ - Prioridade 1)
        # Primeiro tenta match global via MegaKnowledgeStore
        mega_mapping = {}
        for src in src_cols:
            match = self.mega.get_best_match(src, tgt_cols)
            if match:
                mega_mapping[src] = match
                
        if mega_mapping:
            return {
                "mapping": mega_mapping,
                "confidence": 0.95,
                "source": "mega_brain"
            }

        # 1.1 Tentar Histórico Linear (Backwards Compatibility)
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

        # 3. Tentar Profiling (v0.6.5 - Prioridade 3)
        if src_profiles:
            profile_suggestion = self._get_from_profiles(src_profiles, tgt_cols)
            if profile_suggestion:
                return {
                    "mapping": profile_suggestion,
                    "confidence": 0.6,
                    "source": "profiling"
                }
            
        # 4. Tentar Exato (Prioridade 4)
        common = [c for c in src_cols if c in tgt_cols]
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

    def _get_from_profiles(self, current_profiles: Dict[str, Any], tgt_cols: List[str]) -> Optional[Dict]:
        """Compara perfis atuais com o histórico para encontrar matches de conteúdo."""
        log = self.store.load_log()
        matches = {}
        
        for src_col, current_p in current_profiles.items():
            best_target = None
            max_match_score = 0
            
            for ex in log["executions"]:
                hist_profiles = ex.get("column_profiles", {})
                hist_mapping = ex.get("mapping_applied", {})
                
                for h_src, h_p in hist_profiles.items():
                    # Critério de similaridade de perfil (Tipo e Comprimento Médio)
                    if h_p.get("dtype") == current_p.get("dtype") and abs(h_p.get("avg_len", 0) - current_p.get("avg_len", 0)) < 2:
                        target = hist_mapping.get(h_src)
                        if target in tgt_cols:
                            matches[src_col] = target
                            break
        
        return matches if matches else None
