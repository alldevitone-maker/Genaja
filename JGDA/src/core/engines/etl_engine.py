from core.services.logger_service import LoggerService
from version import __version__
import pandas as pd
import numpy as np
import os

class ETLEngine:
    """
    Motor ETL Puro — Restauração Completa do padrão original.
    Implementa Escudo de Dados (Shielding) e Chave A1 Protegida.
    """
    
    def sanitize_series(self, series, trim=True, upper=False, preserve_zeros=True):
        """Padronização de chaves e dados."""
        if preserve_zeros:
            # Converte para string e limpa apenas o .0 se existir no final
            s = series.astype(str).str.replace(r'\.0$', '', regex=True)
        else:
            # Comportamento agressivo: tenta converter para numerico e volta (remove zeros a esquerda)
            s = pd.to_numeric(series, errors='coerce').fillna(series).astype(str).str.replace(r'\.0$', '', regex=True)
            
        if trim: s = s.str.strip()
        if upper: s = s.str.upper()
        return s.replace('nan', '')

    def synchronize(self, df_src, df_tgt, key_src, key_tgt, mapping, 
                    protected_a1=True, shielding=False, 
                    auto_trim=True, auto_upper=False, preserve_zeros=True,
                    a1_col_name=None):
        """
        Sincroniza dados com proteção de integridade.
        """
        # 1. Backups e Preparação
        df_src_work = df_src.copy()
        df_tgt_work = df_tgt.copy()
        
        # Identificar a Coluna A1 (Prioriza escolha do usuario ou primeira do destino) para proteção
        if a1_col_name is None:
            a1_col_name = df_tgt.columns[0]
        
        # 2. Higienização das chaves de cruzamento
        key_src_clean = self.sanitize_series(df_src_work[key_src], trim=auto_trim, upper=auto_upper, preserve_zeros=preserve_zeros)
        key_tgt_clean = self.sanitize_series(df_tgt_work[key_tgt], trim=auto_trim, upper=auto_upper, preserve_zeros=preserve_zeros)
        
        df_src_work['_JOIN_KEY'] = key_src_clean
        df_tgt_work['_JOIN_KEY'] = key_tgt_clean
        
        # Marker to identify which rows successfully joined
        df_src_work['_MATCHED'] = True
        
        # 3. Safe-Merge (Prevenção de duplicatas no destino)
        df_tgt_unique = df_tgt_work.drop_duplicates(subset=['_JOIN_KEY'], keep='first')
        
        # 4. Cruzamento (Left Join)
        # Queremos preservar a estrutura do DESTINO (Target)
        df_result = pd.merge(
            df_tgt_work, 
            df_src_work, 
            on='_JOIN_KEY', 
            how='left', 
            suffixes=('', '_SRC_VAL')
        )
        
        # 5. Aplicação do Escudo (Shielding) e Mapeamento
        for col_src_raw, col_tgt in mapping.items():
            # Tenta encontrar a coluna da origem (pode estar com sufixo se houver colisão)
            col_src = f"{col_src_raw}_SRC_VAL"
            if col_src not in df_result.columns:
                col_src = col_src_raw # Não houve colisão
                
            if col_src not in df_result.columns: continue
            mask_matched = df_result['_MATCHED'] == True
            
            if shielding:
                # Shielding: Só preenche se o destino estiver vazio E houver correspondência
                # Consideramos 'vazio' os valores: '', 'nan', None ou NaN
                val_tgt_clean = df_result[col_tgt].astype(str).str.strip()
                mask_empty = (val_tgt_clean.isin(['', 'nan', 'None'])) | (df_result[col_tgt].isna())
                mask_to_update = mask_empty & mask_matched
                df_result.loc[mask_to_update, col_tgt] = df_result.loc[mask_to_update, col_src]
            else:
                # Sobrescrever (Padrão) - MAS apena onde houve match! 
                # (Previne "apagar" dados de linhas que só existem no destino)
                df_result.loc[mask_matched, col_tgt] = df_result.loc[mask_matched, col_src]
        
        # Cleanup
        if '_MATCHED' in df_result.columns:
            df_result = df_result.drop(columns=['_MATCHED'])
        
        # 6. Proteção de Coluna A1
        # Se a A1 estiver protegida, garantimos que ela permaneça a primeira coluna
        # e que seus valores originais (do target) sejam preservados.
        if protected_a1:
            # Já está preservada pois fizemos join no df_tgt_work
            # Mas vamos garantir que ela seja a primeira na saída
            cols = [a1_col_name] + [c for c in df_result.columns if c != a1_col_name and not c.endswith('_SRC_VAL') and c != '_JOIN_KEY']
        else:
            cols = [c for c in df_result.columns if not c.endswith('_SRC_VAL') and c != '_JOIN_KEY']
            
        return df_result[cols].copy()

    def compare(self, df_src, df_tgt, key_src, key_tgt, mode='falta_destino',
                auto_trim=True, auto_upper=False):
        """
        Modulo Comparador Puro.
        mode='falta_destino': itens na origem que NAO existem no destino.
        mode='falta_origem': itens no destino que NAO existem na origem.
        """
        src_keys = set(self.sanitize_series(df_src[key_src], trim=auto_trim, upper=auto_upper))
        tgt_keys = set(self.sanitize_series(df_tgt[key_tgt], trim=auto_trim, upper=auto_upper))
        
        if mode == 'falta_destino':
            missing = src_keys - tgt_keys
            clean_src = df_src.copy()
            clean_src['_CMP_KEY'] = self.sanitize_series(clean_src[key_src], trim=auto_trim, upper=auto_upper)
            result = clean_src[clean_src['_CMP_KEY'].isin(missing)].drop(columns=['_CMP_KEY'])
        else:
            missing = tgt_keys - src_keys
            clean_tgt = df_tgt.copy()
            clean_tgt['_CMP_KEY'] = self.sanitize_series(clean_tgt[key_tgt], trim=auto_trim, upper=auto_upper)
            result = clean_tgt[clean_tgt['_CMP_KEY'].isin(missing)].drop(columns=['_CMP_KEY'])
        
        return result, len(result)


# --- Declaração de Versão do Módulo (Genaja Version Hook) ---
from version_hook import declare as _vdeclare
_vdeclare(__name__, __version__, "Motor ETL puro estabilizado — padrão de sanitização e sync com shielding")
