import pandas as pd
from typing import List, Dict, Optional, Tuple

class SchemaMapper:
    """
    Motor de Mapeamento de Schema Inteligente (v0.6.3).
    Utiliza similaridade fuzzy (Levenshtein) e análise de tipos.
    Arquiteto para Java: Focado em Heurísticas e Scores.
    """
    def __init__(self, threshold: float = 0.6):
        self.threshold = threshold

    def _levenshtein_distance(self, s1: str, s2: str) -> int:
        """Calcula a distância editorial entre duas strings."""
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    def get_similarity_score(self, a: str, b: str) -> float:
        """Retorna um score de 0.0 a 1.0 (1.0 = idêntico)."""
        a, b = a.lower().strip(), b.lower().strip()
        if a == b: return 1.0
        
        distance = self._levenshtein_distance(a, b)
        max_len = max(len(a), len(b))
        return (max_len - distance) / max_len if max_len > 0 else 0.0

    def suggest_matches(self, src_cols: List[str], tgt_cols: List[str]) -> Dict[str, Dict]:
        """
        Gera um dicionário de sugestões baseadas em similaridade de nome.
        Retorno Java-Ready: {col_origem: {target: col_destino, score: 0.9, reason: "fuzzy_name"}}
        """
        suggestions = {}
        for s_col in src_cols:
            best_match = None
            max_score = 0.0
            
            for t_col in tgt_cols:
                score = self.get_similarity_score(s_col, t_col)
                if score > max_score and score >= self.threshold:
                    max_score = score
                    best_match = t_col
            
            if best_match:
                suggestions[s_col] = {
                    "target": best_match,
                    "score": round(max_score, 2),
                    "reason": "Similaridade de nome"
                }
        
        return suggestions
