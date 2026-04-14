class ExactMatcher:
    """
    Camada de Lookup Determinístico.
    Tenta encontrar o dado nas tabelas de taxonomia (Synonyms/Typos/Abbreviations).
    """
    
    def __init__(self, taxonomy, weights):
        self.taxonomy = taxonomy
        self.weights = weights
        
        # 🔗 Pré-processamento de Performance v0.7.2
        self._precomputed = []
        for entry in self.taxonomy:
            self._precomputed.append({
                "code": entry.get("code"),
                "canonical": [t.lower() for t in entry.get("canonical_terms", [])],
                "synonyms": [t.lower() for t in entry.get("business_synonyms", [])],
                "abbrevs": [t.lower() for t in entry.get("abbreviations", [])],
                "typos": [t.lower() for t in entry.get("known_typos", [])]
            })

    def collect_evidences(self, norm_val):
        """
        Varre a taxonomia em busca de hits exatos.
        """
        hits = []
        for entry in self._precomputed:
            code = entry["code"]
            
            # 1. Canonical Match (1.0)
            if norm_val in entry["canonical"]:
                hits.append((code, self.weights.get("canonical_exact", 1.0), "CANONICAL_EXACT"))
                continue
                
            # 2. Business Synonym Match (0.95)
            if norm_val in entry["synonyms"]:
                hits.append((code, self.weights.get("business_synonym", 0.95), "BUSINESS_SYNONYM"))
                
            # 3. Abbreviation Match (0.90)
            if norm_val in entry["abbrevs"]:
                hits.append((code, self.weights.get("abbreviation", 0.90), "ABBREVIATION"))
                
            # 4. Known Typo Match (0.88)
            if norm_val in entry["typos"]:
                hits.append((code, self.weights.get("known_typo", 0.88), "KNOWN_TYPO"))
                
        return hits

# --- Declaração de Versão do Módulo (Genaja Version Hook) ---
from version_hook import declare as _vdeclare
from version import __version__
_vdeclare(__name__, __version__, "Motor de busca exata otimizado com pré-indexação de taxonomia")
