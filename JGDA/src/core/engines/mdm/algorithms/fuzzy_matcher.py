from rapidfuzz import fuzz, process
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

        # 2. RAPIDFUZZ ACCELERATION (Primary Elite Layer)
        # Otimização: Buscamos em todos os candidatos usando process.extractOne (C++ Engine)
        for code, candidates in self._taxonomy_map.items():
            best_match = process.extractOne(
                norm_val, 
                candidates, 
                scorer=fuzz.WRatio,
                score_cutoff=self.min_score * 100
            )

            if best_match:
                cand, score_100, _ = best_match
                sim = score_100 / 100.0
                
                # --- GOVERNANÇA DE PARIDADE (Anti-Suicídio Técnico) ---
                # Validamos com difflib apenas na "Zona Cinzenta" para garantir compatibilidade legacy
                if 0.75 <= sim <= 0.85:
                    from difflib import SequenceMatcher
                    legacy_sim = SequenceMatcher(None, norm_val, cand).ratio()
                    sim = max(sim, legacy_sim)

                final_score = sim * multiplier
                hits.append((code, final_score, f"RAPID_FUZZ({int(sim*100)}%)"))
                
        return hits

# --- Declaração de Versão do Módulo (Genaja Version Hook) ---
from version_hook import declare as _vdeclare
from version import __version__
_vdeclare(__name__, __version__, "Motor de busca difusa otimizado com cache de candidatos e bridge nativa")
