from difflib import SequenceMatcher
from core.adapters.rust_omni_adapter import RustOmniAdapter

class FuzzyMatcher:
    """
    Camada de Similaridade Probabilística.
    Resolve erros de digitação (typos) via distância de caracteres.
    """
    def __init__(self, taxonomy, weights, min_score=0.78):
        self.taxonomy = taxonomy
        self.weights = weights
        self.min_score = min_score
        
        # 🔗 Pré-processamento de Performance v0.7.2
        self._taxonomy_map = {}
        for entry in self.taxonomy:
            code = entry.get("code")
            candidates = (
                entry.get("canonical_terms", []) + 
                entry.get("business_synonyms", []) + 
                entry.get("abbreviations", [])
            )
            self._taxonomy_map[code] = [c.lower().strip() for c in candidates]

    def collect_evidences(self, norm_val):
        """
        Calcula a similaridade contra todos os termos pré-processados.
        Prioriza aceleração via Rust se disponível.
        """
        hits = []
        multiplier = self.weights.get("fuzzy_multiplier", 0.75)

        # 1. TENTATIVA DE ACELERAÇÃO VIA RUST (Bulk Matching)
        rust_results = RustOmniAdapter.fuzzy_compare(norm_val, self._taxonomy_map)
        
        if rust_results and isinstance(rust_results, dict):
            # O Rust deve retornar: { "CODE": score_float }
            for code, sim in rust_results.items():
                if sim >= self.min_score:
                    final_score = sim * multiplier
                    hits.append((code, final_score, f"RUST_FUZZY({int(sim*100)}%)"))
            return hits

        # 2. FALLBACK PYTHON (Resiliência)
        for code, candidates in self._taxonomy_map.items():
            best_local_score = 0
            for cand_clean in candidates:
                sim = SequenceMatcher(None, norm_val, cand_clean).ratio()
                if sim > best_local_score:
                    best_local_score = sim
            
            if best_local_score >= self.min_score:
                final_score = best_local_score * multiplier
                hits.append((code, final_score, f"PY_FUZZY({int(best_local_score*100)}%)"))
                
        return hits

# --- Declaração de Versão do Módulo (Genaja Version Hook) ---
from version_hook import declare as _vdeclare
from version import __version__
_vdeclare(__name__, __version__, "Motor de busca difusa otimizado com cache de candidatos e bridge nativa")
