import pandas as pd
import re

class MappingEngine:
    """
    Motor de Mapeamento — Especializado em heurísticas de identificação de colunas.
    """
    
    def suggest_primary_keys(self, df_src, df_tgt, sample_size=10000):
        """
        Analisa a interseção de dados para sugerir as melhores chaves de cruzamento.
        """
        matches = []
        
        # Amostragem para performance
        src_sample = df_src.head(sample_size)
        tgt_sample = df_tgt.head(sample_size)
        
        # Cache de sets do destino para otimização
        tgt_sets = {}
        for t_col in tgt_sample.columns:
            s_set = self._get_unique_set(tgt_sample[t_col])
            if s_set:
                tgt_sets[t_col] = s_set
                
        # 2. Cruzamento combinatório por dados
        for s_col in src_sample.columns:
            s_set = self._get_unique_set(src_sample[s_col])
            if not s_set: continue
            
            for t_col, t_set in tgt_sets.items():
                intersection = len(s_set & t_set)
                
                # Heurística de Nome
                name_similarity = self._calc_similarity(s_col, t_col)
                
                if intersection > 0 or name_similarity > 0.8:
                    score = intersection + (name_similarity * 10)
                    matches.append({
                        'src': s_col, 
                        'tgt': t_col, 
                        'score': score,
                        'confidence': intersection / max(len(s_set), 1)
                    })
                    
        # Ordenar por maior pontuação composta
        matches.sort(key=lambda x: x['score'], reverse=True)
        return matches[:5]

    def _calc_similarity(self, a, b):
        """Heurística simples de similaridade de nomes."""
        a, b = a.lower(), b.lower()
        if a == b: return 1.0
        if a in b or b in a: return 0.8
        return 0.0

    def _get_unique_set(self, series):
        """Limpa e retorna set de valores únicos."""
        s = series.astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
        s = s[s != 'nan']
        s = s[s != '']
        return set(s) if not s.empty else None


# --- Declaração de Versão do Módulo (Genaja Version Hook) ---
from version_hook import declare as _vdeclare
_vdeclare(__name__, "0.7.1", "Motor de mapeamento por intersecção de dados e heurística de nome")
