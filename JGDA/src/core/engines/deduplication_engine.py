import pandas as pd
import re
from rapidfuzz import fuzz, process
from core.services.logger_service import LoggerService
from core.math.phonetic_engine import PhoneticEngine

class DeduplicationEngine:
    """
    Motor de Consolidação Universal.
    Arquitetura Matemática Pura (Zero Hardcoding).
    Usa segmentação estrutural e Clustering Hierárquico via RapidFuzz.
    """
    def __init__(self, threshold=80):
        self.threshold = threshold
        self.ls = LoggerService()

    def _calculate_signal_score(self, text):
        """
        Calcula a 'Pureza do Sinal' de uma string.
        Pontua positivamente caracteres alfanuméricos e negativamente ruídos.
        """
        if not text or not isinstance(text, str): return 0
        
        # Sinal: Letras e Números
        signal = len(re.findall(r'[a-zA-Z0-9]', text))
        # Ruído: Pontuação repetida, espaços excessivos, caracteres especiais soltos
        noise = len(re.findall(r'[-_*|!@#$%^&()]', text))
        spaces = text.count(" ")
        
        # Penaliza ruído mas valoriza o sinal real
        score = signal - (noise * 1.5) - (spaces * 0.5)
        return max(score, 0)


    def _get_segments(self, text):
        """
        Segmentador ESTRUTURAL agnóstico. 
        Divide a string em Nó Central e Metadados (parênteses, traços, etc).
        """
        if not text or not isinstance(text, str):
            return {"base": "", "meta": ""}
            
        # 1. Isolar conteúdo entre parênteses como Metadado
        meta_match = re.search(r'\((.*?)\)', text)
        meta = meta_match.group(1).strip().upper() if meta_match else ""
        
        # 2. Limpar o nome base (Remover tudo que não é identidade central)
        base = re.sub(r'\(.*?\)', '', text) # Remove parênteses
        base = re.sub(r'[-:|]', ' ', base)  # Trata delimitadores como espaços
        base = ' '.join(base.split()).upper() # Normaliza espaços e case
        
        return {"base": base, "meta": meta}

    def consolidate(self, df, dynamic_threshold=None, col_mapping=None):
        """
        Consolidação Universal via Power Query Matemático.
        Suporta Recalibração Dinâmica e Mapeamento de Colunas Injetado.
        """
        threshold = dynamic_threshold if dynamic_threshold is not None else self.threshold
        cm = col_mapping if col_mapping else {"name": "Name", "mail": "E_Mail", "phone": "Phone"}
        
        if df is None or df.empty:
            return df, []

        df_work = df.copy()
        
        # 1. Segmentação Prévia (O(N))
        df_work['_segments'] = df_work[cm.get('name', 'Name')].apply(self._get_segments)
        
        groups = df_work.groupby('ParentKey')
        final_rows = []
        dedup_log = []

        for pk, group in groups:
            if len(group) == 1:
                final_rows.append(group.iloc[0].to_dict())
                continue

            processed_idxs = set()
            
            for i in range(len(group)):
                idx = group.index[i]
                if idx in processed_idxs:
                    continue
                
                # Inicia Cluster
                cluster_idxs = [idx]
                processed_idxs.add(idx)
                
                seg_a = group.loc[idx, '_segments']
                
                # Compara com o restante do grupo
                for j in range(i + 1, len(group)):
                    other_idx = group.index[j]
                    if other_idx in processed_idxs:
                        continue
                        
                    seg_b = group.loc[other_idx, '_segments']
                    
                    # --- ALGORITMO HÍBRIDO (CIÊNCIA DE DADOS) ---
                    # Se as identidades sonoras forem totalmente discrepantes, ignoramos o Fuzz caro
                    phon_a = PhoneticEngine.get_phonetic_code(seg_a['base'])
                    phon_b = PhoneticEngine.get_phonetic_code(seg_b['base'])
                    
                    # WRatio é caro (O(N*M)). Só rodamos se houver proximidade estrutural ou fonética.
                    sim_base = 0
                    if phon_a == phon_b or (len(seg_a['base']) > 3 and seg_a['base'][0] == seg_b['base'][0]):
                        sim_base = fuzz.WRatio(seg_a['base'], seg_b['base'])
                    else:
                        # Fallback seguro para strings curtas ou incertas
                        sim_base = fuzz.QRatio(seg_a['base'], seg_b['base'])
                    is_phonetic_match = (phon_a == phon_b and len(phon_a) > 2)
                    
                    # Decisão Adaptativa
                    is_match = False
                    if sim_base >= threshold: 
                        is_match = True
                    elif is_phonetic_match and sim_base >= (threshold - 10):
                        # Fonética idêntica permite threshold menor
                        is_match = True
                    elif sim_base >= (threshold - 5) and (seg_a['meta'] == seg_b['meta'] and seg_a['meta'] != ""):
                        is_match = True

                    if is_match:
                        cluster_idxs.append(other_idx)
                        processed_idxs.add(other_idx)
                        # Injeta score de similaridade para o HUD visual (Platinum UX)
                        # Salva também se foi fonético para o Raio-X
                        group.at[other_idx, '_similarity_score'] = sim_base
                        group.at[other_idx, '_is_phonetic'] = is_phonetic_match

                # 3. Merge de Atributos por Cluster
                cluster_df = df_work.loc[cluster_idxs]
                if len(cluster_df) == 1:
                    final_rows.append(cluster_df.iloc[0].to_dict())
                else:
                    # Usa o metadado do nó A como rótulo ou o próprio nome limpo
                    label = seg_a['meta'] if seg_a['meta'] else "CONSOLIDADO"
                    master_record = self._merge_records(cluster_df, label, cm)
                    final_rows.append(master_record)
                    dedup_log.append({
                        "pk": pk,
                        "role": label,
                        "merged_count": len(cluster_idxs),
                        "details": f"Unificação Universal: {seg_a['base']} (Confiança: {sim_base}%)"
                    })

        df_result = pd.DataFrame(final_rows)
        # Limpeza de colunas temporárias
        cols_to_drop = [c for c in df_result.columns if c.startswith('_')]
        df_result = df_result.drop(columns=cols_to_drop)
            
        return df_result, dedup_log

    def _merge_records(self, cluster_df, role_name, cm):
        """
        Cria um registro mestre consolidando o melhor de cada campo (Zero Hardcode).
        """
        name_col = cm.get('name', 'Name')
        mail_col = cm.get('mail', 'E_Mail')
        phone_col = cm.get('phone', 'Phone')
        
        # CRITÉRIO DE ELITE: Signal-to-Noise Score.
        # Prioriza o nome com a melhor relação de caracteres válidos vs. ruído.
        # O comprimento (len) agora é apenas o critério de desempate.
        scores = cluster_df[name_col].apply(self._calculate_signal_score)
        lengths = cluster_df[name_col].str.len()
        
        # Combina scores (Signal como peso principal, Length como secundário)
        best_idx = (scores * 100 + lengths).idxmax()
        base_record = cluster_df.loc[best_idx].to_dict()
        
        # Consolidar E-mail e Telefone (Não perder dados!)
        all_emails = [str(x).strip() for x in cluster_df[mail_col].unique() if x and str(x).lower() not in ['nan', 'none', '']]
        all_phones = [str(x).strip() for x in cluster_df if phone_col in cluster_df.columns and cluster_df[phone_col].unique()] # Safe check
        
        # Corrigindo lógica de telefones
        all_phones = []
        if phone_col in cluster_df.columns:
            all_phones = [str(x).strip() for x in cluster_df[phone_col].unique() if x and str(x).lower() not in ['nan', 'none', '']]

        base_record[mail_col] = "; ".join(all_emails) if all_emails else ""
        if phone_col in base_record:
            base_record[phone_col] = "; ".join(all_phones) if all_phones else ""
            
        base_record['MDM_Status'] = "CONSOLIDATED"
        base_record['MDM_Reason'] = f"Unificação Fuzzy RapidFuzz (Role: {role_name})"
        
        # Rastro de Auditoria
        base_record['_dedup_origin_count'] = len(cluster_df)
        
        return base_record

    def get_pair_analysis(self, text_a, text_b):
        """
        Gera métricas profundas para o Raio-X do HUD.
        """
        from rapidfuzz import distance
        seg_a = self._get_segments(text_a)
        seg_b = self._get_segments(text_b)
        
        return {
            "w_ratio": fuzz.WRatio(seg_a['base'], seg_b['base']),
            "levenshtein": distance.Levenshtein.distance(seg_a['base'], seg_b['base']),
            "is_phonetic": PhoneticEngine.get_phonetic_code(seg_a['base']) == PhoneticEngine.get_phonetic_code(seg_b['base']),
            "seg_a": seg_a,
            "seg_b": seg_b
        }

# --- Declaração de Versão do Módulo (Genaja Version Hook) ---
from version import __version__
from version_hook import declare as _vdeclare
_vdeclare(__name__, __version__, "Motor de Consolidação Power Query com RapidFuzz")
