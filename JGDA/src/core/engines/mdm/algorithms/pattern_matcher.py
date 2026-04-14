import re

class PatternMatcher:
    """
    Camada de Inteligência de Padrão.
    Executa Regex contra o valor normalizado para capturar semântica estrutural.
    """
    def __init__(self, taxonomy, weights):
        self.taxonomy = taxonomy
        self.weights = weights
        
        # 🔗 Pré-compilação de Regex para Performance v0.7.2
        self._compiled_patterns = []
        for entry in self.taxonomy:
            code = entry.get("code")
            boost = entry.get("boost", 1.0)
            patterns = entry.get("patterns", [])
            compiled = []
            for p in patterns:
                try:
                    compiled.append(re.compile(p, re.IGNORECASE))
                except Exception:
                    continue # Ignora regex inválida
            
            if compiled:
                self._compiled_patterns.append({
                    "code": code,
                    "boost": boost,
                    "patterns": compiled
                })

    def collect_evidences(self, norm_val):
        """
        Executa todos os padrões pré-compilados contra o input.
        """
        hits = []
        weight_pattern = self.weights.get("pattern_hit", 0.72)
        
        for entry in self._compiled_patterns:
            code = entry["code"]
            boost = entry["boost"]
            
            for pat in entry["patterns"]:
                if pat.search(norm_val):
                    # Score ponderado pelo boost da categoria
                    score = weight_pattern * boost
                    hits.append((code, score, "PATTERN_HIT"))
                    break # Um hit de padrão por categoria é suficiente
                    
        return hits

# --- Declaração de Versão do Módulo (Genaja Version Hook) ---
from version_hook import declare as _vdeclare
from version import __version__
_vdeclare(__name__, __version__, "Motor de reconhecimento de padrões otimizado com pré-compilação regex")
