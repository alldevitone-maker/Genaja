import pandas as pd
import numpy as np
import re

class ETLEngine:
    """
    Motor ETL Puro (v0.6.0) - Baseado na lógica estável da v0.4.8.
    Desacoplado de qualquer interface visual.
    """
    
    @staticmethod
    def sanitize_key(series):
        """Padronização de chaves para evitar erros de ponto flutuante e espaços."""
        return series.astype(str).str.replace(r'\.0$', '', regex=True).str.strip()

    def synchronize(self, df_src, df_tgt, key_src, key_tgt, mapping, key_tgt_final, clean_output=True):
        """
        Sincroniza dados da Origem para o Destino baseado em um mapeamento.
        Implementação fiel ao 'Rollback Lógico' da v0.4.8.
        """
        # 1. Higienização das chaves
        df_src_clean = df_src.copy()
        df_tgt_clean = df_tgt.copy()
        
        df_src_clean[key_src] = self.sanitize_key(df_src_clean[key_src])
        df_tgt_clean[key_tgt] = self.sanitize_key(df_tgt_clean[key_tgt])
        
        # 2. Remoção de duplicatas no destino para evitar explosão de merge
        df_tgt_unique = df_tgt_clean.drop_duplicates(subset=[key_tgt], keep='first')
        
        # 3. Merge (Left Join)
        df_merged = pd.merge(
            df_src_clean, 
            df_tgt_unique, 
            left_on=key_src, 
            right_on=key_tgt, 
            how='left', 
            suffixes=('', '_LEGACY_TGT')
        )
        
        # 4. Limpeza de colunas redundantes do destino
        df_merged = df_merged[[c for c in df_merged.columns if not c.endswith('_LEGACY_TGT')]]
        
        # 5. Aplicação do Mapeamento (Sobrescrever destino com origem)
        for col_src, col_tgt in mapping.items():
            if col_src in df_merged.columns:
                df_merged[col_tgt] = df_merged[col_src]
                
        # 6. Reordenação e Limpeza Final
        if clean_output:
            # Manter apenas colunas que mapeamos + Chave Final
            cols_to_keep = list(mapping.values())
            if key_tgt_final in cols_to_keep:
                cols_to_keep.remove(key_tgt_final)
            cols_to_keep.insert(0, key_tgt_final)
            
            # Garantir que as colunas existem no resultado
            cols_to_keep = [c for c in dict.fromkeys(cols_to_keep) if c in df_merged.columns]
            return df_merged[cols_to_keep].copy()
            
        return df_merged

    def compare(self, df_src, df_tgt, key_src, key_tgt, mode='missing_in_target'):
        """
        Compara lacunas entre as bases.
        mode: 'missing_in_target' (O que tem na src mas não na tgt) 
              ou 'missing_in_source' (O que tem na tgt mas não na src)
        """
        src_keys = set(self.sanitize_key(df_src[key_src]))
        tgt_keys = set(self.sanitize_key(df_tgt[key_tgt]))
        
        if mode == 'missing_in_target':
            diff_keys = src_keys - tgt_keys
            df_result = df_src[self.sanitize_key(df_src[key_src]).isin(diff_keys)].copy()
        else:
            diff_keys = tgt_keys - src_keys
            df_result = df_tgt[self.sanitize_key(df_tgt[key_tgt]).isin(diff_keys)].copy()
            
        return df_result
