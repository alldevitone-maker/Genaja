import logging
from typing import Dict, Any, List, Tuple, Optional
from version import __version__


class TransformEngine:
    """
    Genaja Stable - Orquestrador de Transformação (Facade Pattern).
    NÃO contém lógica de dados própria. Delega para os motores canônicos:
      - LoaderEngine   → carga de arquivos
      - LookupEngine   → join/sync multi-chave
      - ExportService  → exportação
      - AuditService   → rastreabilidade LGPD

    Delega 100% para os motores canônicos.
    """

    @classmethod
    def price_sync_join(
        cls,
        path_origem: str,
        path_destino: str,
        col_chave_origem: str,
        col_valor_origem: str,
        col_chave_destino: str,
        col_destino_preencher: str,
        chaves_alternativas: Optional[List[Tuple[str, str]]] = None,
        sheet_origem: str | int = 0,
        sheet_destino: str | int = 0,
        out_path: Optional[str] = None,
        operator: str = "Genaja",
    ) -> Dict[str, Any]:
        """
        Facade de sincronização de preços multi-chave.
        Delega 100% para LoaderEngine + LookupEngine + ExportService + AuditService.
        """
        from core.engines.loader_engine import LoaderEngine
        from core.engines.lookup_engine import LookupEngine
        from core.services.export_service import ExportService
        from core.services.audit_service import AuditService
        import os
        import pandas as pd

        result = {
            "success": False,
            "output_path": out_path,
            "matched_total": 0,
            "unmatched": 0,
            "passes": [],
            "warnings": []
        }

        loader = LoaderEngine()
        lookup = LookupEngine()
        exporter = ExportService()
        auditor = AuditService(operator=operator)

        try:
            # ── CARREGAR ──
            wb_orig, _ = loader.load_workbook(path_origem)
            sheet_orig_key = sheet_origem if isinstance(sheet_origem, str) else list(wb_orig.keys())[sheet_origem]
            df_orig = wb_orig.get(sheet_orig_key)

            wb_dest, _ = loader.load_workbook(path_destino)
            sheet_dest_key = sheet_destino if isinstance(sheet_destino, str) else list(wb_dest.keys())[sheet_destino]
            df_dest = wb_dest.get(sheet_dest_key)

            # ── MONTAR CASCATA DE CHAVES ──
            pares = [(col_chave_destino, col_chave_origem)]
            if chaves_alternativas:
                pares.extend(chaves_alternativas)

            # ── SINCRONIZAR via LookupEngine ──
            sync_result = lookup.multi_key_sync(
                df_orig=df_orig,
                df_dest=df_dest,
                pares_chave=pares,
                col_valor=col_valor_origem,
                col_preencher=col_destino_preencher,
                sanitizar_monetario=True
            )

            df_final = sync_result["df_resultado"]
            result["matched_total"] = sync_result["matched_total"]
            result["unmatched"] = sync_result["unmatched"]
            result["passes"] = sync_result["passes"]

            # ── EXPORTAR CIRÚRGICO (Preservação de Matriz e Fórmulas) ──
            if out_path is None:
                base = os.path.splitext(path_destino)[0]
                out_path = base + "_SYNC.xlsx"
            
            result["output_path"] = out_path

            # 1. Clonar o template original para preservar TUDO (Abas, Fórmulas, Estilos)
            import shutil
            if not os.path.exists(out_path):
                shutil.copy(path_destino, out_path)
            
            # 2. Injetar cirurgicamente apenas os valores cruzados
            exporter.export(
                df_final, 
                out_path, 
                sheet_name=sheet_dest_key, 
                key_col=col_chave_destino
            )

            # ── AUDITORIA LGPD ──
            auditor.record_sync(
                src_file=path_origem,
                tgt_file=path_destino,
                rows_affected=result["matched_total"]
            )

            result["success"] = True

        except Exception as e:
            logging.error(f"[TransformEngine] Erro crítico: {e}")
            result["warnings"].append(f"Erro interno: {str(e)}")

        return result


# --- Declaração de Versão do Módulo (Genaja Version Hook) ---
from version_hook import declare as _vdeclare
_vdeclare(__name__, __version__, "Restaurado price_sync_join() para compatibilidade com a UI e fix NameError pd")
