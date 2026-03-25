import pandas as pd
import re

class MappingEngine:
    """
    Motor de Mapeamento (v0.6.0) - Lógica resgatada da v0.4.8.
    Especializado em heurísticas de identificação de colunas.
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
                
        # Cruzamento combinatório
        for s_col in src_sample.columns:
            s_set = self._get_unique_set(src_sample[s_col])
            if not s_set: continue
            
            for t_col, t_set in tgt_sets.items():
                intersection = len(s_set & t_set)
                if intersection > 0:
                    matches.append({
                        'src': s_col, 
                        'tgt': t_col, 
                        'score': intersection,
                        'confidence': intersection / max(len(s_set), 1)
                    })
                    
        # Ordenar por maior interseção
        matches.sort(key=lambda x: x['score'], reverse=True)
        return matches[:5]

    def _get_unique_set(self, series):
        """Limpa e retorna set de valores únicos."""
        s = series.astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
        s = s[s != 'nan']
        s = s[s != '']
        return set(s) if not s.empty else None
