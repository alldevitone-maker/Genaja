import pandas as pd

class LookupEngine:
    """
    Motor de Consulta Inteligente — Substitui lógicas de PROCV/XLOOKUP via Joins eficientes.
    """
    def __init__(self):
        pass

    def find_common_columns(self, df_src, df_tgt):
        """Identifica colunas comuns preservando a ordem da origem (Hardening Patch 2)."""
        if df_src is None or df_tgt is None: return []
        tgt_cols = set(df_tgt.columns)
        return [col for col in df_src.columns if col in tgt_cols]

    def suggest_key_pair(self, df_src, df_tgt):
        """Sugerir par de chaves com guarda contra NaN e Zero Division (Hardening Patch 2)."""
        if df_src is None or df_tgt is None: return None, None
        common = self.find_common_columns(df_src, df_tgt)
        if not common or len(df_src) == 0 or len(df_tgt) == 0:
            return None, None
            
        for col in common:
            try:
                # Ignorar NaN no cálculo de unicidade
                u_src = len(df_src[col].dropna().unique()) / len(df_src)
                u_tgt = len(df_tgt[col].dropna().unique()) / len(df_tgt)
                
                if u_src > 0.8 and u_tgt > 0.8:
                    return col, col
            except:
                continue
        return None, None

    def multi_key_sync(self, df_orig, df_dest, pares_chave, col_valor, col_preencher,
                       sanitizar_monetario=True):
        """
        v0.7.1 - Sincronização em cascata multi-chave (substitui PROCX do Excel).
        Cada par de chave é tentado em sequência apenas para as linhas ainda sem match.

        Args:
            df_orig: DataFrame da tabela de preços (origem)
            df_dest: DataFrame do arquivo destino
            pares_chave: lista de tuplas [(col_destino, col_origem), ...]
            col_valor: coluna do preço na origem
            col_preencher: coluna do destino que receberá o valor
            sanitizar_monetario: se True, aplica fix IEEE 754 (Decimal 2 casas)

        Returns:
            { success, df_resultado, passes: [{chave_dest, chave_orig, matches}], matched_total, unmatched }
        """
        from core.engines.etl_engine import ETLEngine
        from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

        etl = ETLEngine()
        df_dest = df_dest.copy()
        df_dest[col_preencher] = None
        report = {"passes": [], "matched_total": 0, "unmatched": 0, "success": True}

        for (col_d, col_o) in pares_chave:
            if col_d not in df_dest.columns or col_o not in df_orig.columns:
                report["passes"].append({
                    "chave_dest": col_d, "chave_orig": col_o,
                    "matches": 0, "aviso": "Coluna não encontrada"
                })
                continue

            mask = df_dest[col_preencher].isna()
            if mask.sum() == 0:
                break  # Todos os itens já resolvidos

            # Normalização via ETLEngine (único padrão, sem duplicação)
            norm_orig = etl.sanitize_series(df_orig[col_o], trim=True, upper=True,
                                            preserve_zeros=True)
            norm_dest = etl.sanitize_series(df_dest.loc[mask, col_d], trim=True, upper=True,
                                            preserve_zeros=True)

            # Remove pontuação extra para replicar SUBSTITUIR(. , - /) do Excel
            import re
            norm_orig = norm_orig.str.replace(r'[.,\-/]', '', regex=True)
            norm_dest = norm_dest.str.replace(r'[.,\-/]', '', regex=True)

            # Lookup dict: chave_normalizada → valor
            lookup = (
                df_orig.assign(__k=norm_orig.values)
                .drop_duplicates("__k")
                .set_index("__k")[col_valor]
                .to_dict()
            )

            matched_vals = norm_dest.map(lookup)
            df_dest.loc[mask, col_preencher] = matched_vals.values

            n_matched = int(matched_vals.notna().sum())
            report["passes"].append({"chave_dest": col_d, "chave_orig": col_o, "matches": n_matched})
            report["matched_total"] += n_matched

        report["unmatched"] = int(df_dest[col_preencher].isna().sum())

        # IEEE 754 Fix: 351.27000000000004 → 351.27
        if sanitizar_monetario:
            def _sanitizar(v):
                if v is None or str(v).strip() in ("", "nan", "None"):
                    return None
                try:
                    return float(Decimal(str(v)).quantize(Decimal("0.01"),
                                                          rounding=ROUND_HALF_UP))
                except (InvalidOperation, ValueError):
                    return None
            df_dest[col_preencher] = df_dest[col_preencher].apply(_sanitizar)

        report["df_resultado"] = df_dest
        return report


# --- Declaração de Versão do Módulo (Genaja Version Hook) ---
from version_hook import declare as _vdeclare
_vdeclare(__name__, "0.7.1", "Adicionado multi_key_sync() — substitui PROCV/XLOOKUP com cascata multi-chave e IEEE 754 fix")
