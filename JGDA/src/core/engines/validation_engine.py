import pandas as pd
from version import __version__
import numpy as np
import re

class ValidationEngine:
    """
    Motor de Validação e Limpeza — Garante integridade dos dados pós-merge.
    Possui suporte a Normalização MDM de campos multi-valor (1:N).
    """
    
    def apply_numeric_filter(self, df, columns):
        """Remove linhas onde as colunas especificadas são zero, vazias ou NaN."""
        df_clean = df.copy()
        for col in columns:
            if col not in df_clean.columns: continue
            
            s = df_clean[col]
            s_num = pd.to_numeric(s, errors='coerce')
            
            # Máscaras de remoção
            mask_zero = (s_num == 0.0)
            mask_empty = (s.astype(str).str.strip() == '')
            mask_nan = s.isna()
            
            df_clean = df_clean[~(mask_zero | mask_empty | mask_nan)]
            
        return df_clean

    def normalize_multivalue_field(self, df, col_source, col_id, regex_pattern=None):
        """
        Normalização MDM: Transforma uma coluna multi-valor (ex: emails múltiplos) 
        em duas estruturas vinculadas (Matriz e Contatos).
        Retorna: {
            "entity_primary": pd.DataFrame (Header Node 1:1),
            "entity_contacts": pd.DataFrame (Detail Node 1:N)
        }
        """
        from core.services.logger_service import LoggerService
        ls = LoggerService()
        
        if df is None:
            ls.error("FALHA MDM: DataFrame de entrada é nulo (NoneType).")
            return None
            
        if col_source not in df.columns or col_id not in df.columns:
            ls.error(f"FALHA MDM: Colunas '{col_source}' ou '{col_id}' ausentes no DataFrame.")
            return None

        primary_data = [] # Memória para o Header Node (1:1)
        contacts_data = [] # Memória para o Detail Node (1:N)
        
        # --- REGRA DE OURO MDM v0.7.2 (Performance Platinum) ---
        from core.engines.mdm.mdm_engine import MDMEngine
        mdm = MDMEngine() # Instância única para o batch
        
        for _, row in df.iterrows():
            uid = row[col_id]
            raw_val = str(row[col_source]).strip()
            
            if not raw_val or raw_val.lower() in ['none', 'nan', 'null', '']:
                continue
                
            # Quebrar apenas por delimitadores fortes inicialmente (;, |)
            segments = re.split(r'[;|\n\r]+', str(raw_val))
            valid_tokens = []
            
            for seg in segments:
                # Se o segmento tem vírgula ou espaço, tratamos com cuidado
                parts = re.split(r'[,]', seg)
                for part in parts:
                    clean_part = part.strip().replace('"', '').replace("'", "")
                    if not clean_part: continue
                    
                    # Heurística: Se tem espaço, mas apenas um @, é um e-mail "sujo" (Ex: nome sobrenome @...)
                    if " " in clean_part and clean_part.count("@") == 1:
                        valid_tokens.append(clean_part)
                    elif " " in clean_part:
                        # Se tem múltiplos @ ou nenhum, tenta separar por espaços
                        sub_parts = clean_part.split(" ")
                        for sp in sub_parts:
                            if "@" in sp or (sp.isdigit() and len(sp) > 5):
                                valid_tokens.append(sp.strip())
                    else:
                        # Caso padrão
                        if "@" in clean_part or (clean_part.isdigit() and len(clean_part) > 5):
                            valid_tokens.append(clean_part)

            if not valid_tokens: continue

            # O primeiro valor válido fica como Primário (Header)
            primary_val = valid_tokens[0]
            overflow_values = valid_tokens[1:] if len(valid_tokens) > 1 else []
            
            # 1. Montagem do Registro Primário (Header)
            p_row = row.to_dict()
            p_row[col_source] = primary_val
            primary_data.append(p_row)
            
            # 2. Montagem dos Contatos Inteligentes (Detail via MDM Engine Compartilhado)
            for val in overflow_values:
                # Resolução de Domínio Enterprise
                res = mdm.resolve(val)
                
                contacts_data.append({
                    "ParentKey": uid,
                    "Name": res["category_label"] if res["status"] == "AUTO_CLASSIFIED" else res["input_normalized"].capitalize(),
                    "Position": res["position_default"],
                    "E_Mail": val if "@" in val else "",
                    "Phone": val if "@" not in val else "",
                    "MDM_Status": res["status"],
                    "MDM_Confidence": res["confidence"],
                    "MDM_Reason": res["reason"]
                })

        return {
            "entity_primary": pd.DataFrame(primary_data),
            "entity_contacts": pd.DataFrame(contacts_data)
        }

    def clean_empty_by_values(self, df, target_cols, num_col):
        """
        Limpeza condicional: Remove linhas onde as colunas alvo estão vazias 
        E o valor na coluna numérica é zero.
        """
        if num_col not in df.columns: return df
        
        df_work = df.copy()
        for i, row in df_work.iterrows():
            try:
                val_num = float(row[num_col])
                is_empty_target = all(str(row[c]).strip() == '' for c in target_cols if c in df.columns)
                
                if val_num == 0.0 and is_empty_target:
                    df_work = df_work.drop(i)
            except (ValueError, TypeError):
                continue
                
        return df_work

    def audit_dataframe(self, df):
        """Auditoria Rápida: Gera metadados para o FileIntelligenceDialog."""
        if df is None: return {}
        
        try:
            return {
                "rows": len(df),
                "cols": len(df.columns),
                "nulls": int(df.isna().sum().sum()),
                "dupes": int(df.duplicated().sum()) if len(df.columns) > 0 else 0,
                "empty_cols": [col for col in df.columns if df[col].isna().all()]
            }
        except Exception as e:
            from core.services.logger_service import LoggerService
            LoggerService().error(f"Erro na auditoria: {e}")
            return {"rows": len(df), "cols": len(df.columns), "nulls": 0, "dupes": 0, "empty_cols": []}

    def validate_keys(self, df, columns):
        """Verifica se existem duplicatas ou vazios críticos em chaves."""
        report = {"valid": True, "errors": []}
        for col in columns:
            if col not in df.columns:
                report["valid"] = False
                report["errors"].append(f"Coluna '{col}' não encontrada.")
                continue
                
            null_count = df[col].isna().sum()
            if null_count > 0:
                report["errors"].append(f"Coluna '{col}' possui {null_count} valores nulos.")
                
        return report

    def analyze_value_drift(self, df, col_old, col_new, threshold=0.1):
        """
        Analisa a deriva de valor (preço) entre colunas.
        threshold: percentual de variação considerado 'Outlier' (0.1 = 10%).
        """
        if col_old not in df.columns or col_new not in df.columns:
            return {"avg_drift": 0, "max_drift": 0, "outliers": [], "outlier_count": 0}

        # Cópias seguras com numerização
        old_v = pd.to_numeric(df[col_old], errors='coerce').fillna(0)
        new_v = pd.to_numeric(df[col_new], errors='coerce').fillna(0)

        # Evitar divisão por zero (apenas itens que já tinham preço)
        mask_valid = (old_v > 0) & (new_v > 0)
        if not mask_valid.any():
            return {"avg_drift": 0, "max_drift": 0, "outliers": [], "outlier_count": 0}

        v_old = old_v[mask_valid]
        v_new = new_v[mask_valid]

        pct_change = (v_new - v_old) / v_old
        
        avg_drift = pct_change.mean()
        max_drift = pct_change.max()

        # Identificar Outliers
        mask_outlier = pct_change.abs() > threshold
        outliers_indices = pct_change[mask_outlier].index
        
        outliers_list = []
        for idx in outliers_indices[:10]: # Top 10 para o relatório
            row = df.loc[idx]
            outliers_list.append({
                "id": str(row.iloc[0]), # PK assumida como primeira coluna
                "old": float(row[col_old]),
                "new": float(row[col_new]),
                "drift_pct": float(pct_change.loc[idx] * 100)
            })

        return {
            "avg_drift": float(avg_drift * 100),
            "max_drift": float(max_drift * 100),
            "outliers": outliers_list,
            "outlier_count": int(mask_outlier.sum())
        }

# --- Declaração de Versão do Módulo (Genaja Version Hook) ---
from version_hook import declare as _vdeclare
_vdeclare(__name__, __version__, "Motor MDM: Validação de chaves e Smart MVF Normalizer (Split 1:N)")
