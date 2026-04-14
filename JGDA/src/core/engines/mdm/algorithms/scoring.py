class ConfidenceScorer:
    """
    Consolidador de Evidências.
    Calcula o score final baseado em múltiplos hits de camadas.
    """
    
    @staticmethod
    def consolidate(evidences):
        """
        Agrupa evidências por categoria e acumula os scores.
        evidences: lista de (code, score, type)
        Retorna: { "CODE": { "score": float, "traces": [] } }
        """
        results = {}
        for code, score, ev_type in evidences:
            if code not in results:
                results[code] = {"score": 0.0, "traces": []}
            
            # Acúmulo de Score com teto de 1.0 (100% de confiança)
            results[code]["score"] = min(1.0, results[code]["score"] + score)
            results[code]["traces"].append({
                "layer": ev_type,
                "score": round(score, 3)
            })
            
        # Ordenar por maior score
        sorted_keys = sorted(results, key=lambda x: results[x]["score"], reverse=True)
        return {k: results[k] for k in sorted_keys}

    @staticmethod
    def top_candidates(consolidated_results, limit=2):
        """Retorna os top N candidatos."""
        return list(consolidated_results.items())[:limit]
