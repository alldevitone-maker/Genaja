import logging
from typing import Dict, Any, List, Tuple, Optional


class TransformEngine:
    """
    v0.7.1 - Orquestrador de Transformação (Facade Pattern).
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

        Args:
            path_origem: Caminho da tabela de preços
            path_destino: Caminho do arquivo destino
            col_chave_origem: Coluna chave principal na tabela de preços
            col_valor_origem: Coluna de preço na tabela de preços
            col_chave_destino: Coluna chave principal no destino
            col_destino_preencher: Coluna do destino que receberá o valor
            chaves_alternativas: Pares extras [(col_dest, col_orig)] para cascata
            sheet_origem: Aba do Excel na origem (nome ou índice)
            sheet_destino: Aba do Excel no destino (nome ou índice)
            out_path: Caminho de saída. Se None, usa pasta do destino.
            operator: Nome do operador para log de auditoria.

        Returns:
            { success, output_path, matched_total, unmatched, passes, warnings }
        """
        from core.engines.loader_engine import LoaderEngine
        from core.engines.lookup_engine import LookupEngine
        from core.services.export_service import ExportService
        from core.services.audit_service import AuditService
        import os

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
            # ── CARREGAR via LoaderEngine (robusto, multi-encoding, multi-aba) ──
            logging.info(f"[TransformEngine] Carregando origem: {path_origem}")
            wb_orig, _ = loader.load_workbook(path_origem)
            sheet_orig_key = sheet_origem if isinstance(sheet_origem, str) else list(wb_orig.keys())[sheet_origem]
            df_orig = wb_orig.get(sheet_orig_key)
            if df_orig is None:
                result["warnings"].append(f"Aba '{sheet_orig_key}' não encontrada na origem. Abas: {list(wb_orig.keys())}")
                return result

            logging.info(f"[TransformEngine] Carregando destino: {path_destino}")
            wb_dest, _ = loader.load_workbook(path_destino)
            sheet_dest_key = sheet_destino if isinstance(sheet_destino, str) else list(wb_dest.keys())[sheet_destino]
            df_dest = wb_dest.get(sheet_dest_key)
            if df_dest is None:
                result["warnings"].append(f"Aba '{sheet_dest_key}' não encontrada no destino. Abas: {list(wb_dest.keys())}")
                return result

            logging.info(f"[TransformEngine] Origem: {len(df_orig)} linhas | Destino: {len(df_dest)} linhas")

            # ── VALIDAR COLUNAS ──
            for col in [col_chave_origem, col_valor_origem]:
                if col not in df_orig.columns:
                    result["warnings"].append(f"Coluna '{col}' não encontrada na origem. Disponíveis: {list(df_orig.columns)}")
                    return result
            if col_chave_destino not in df_dest.columns:
                result["warnings"].append(f"Coluna '{col_chave_destino}' não encontrada no destino. Disponíveis: {list(df_dest.columns)}")
                return result

            # ── MONTAR CASCATA DE CHAVES ──
            # Chave primária sempre primeiro, alternativas em sequência
            pares = [(col_chave_destino, col_chave_origem)]
            if chaves_alternativas:
                pares.extend(chaves_alternativas)

            # ── SINCRONIZAR via LookupEngine (dono canônico do PROCV/XLOOKUP) ──
            logging.info(f"[TransformEngine] Executando multi_key_sync com {len(pares)} par(es) de chave...")
            sync_result = lookup.multi_key_sync(
                df_orig=df_orig,
                df_dest=df_dest,
                pares_chave=pares,
                col_valor=col_valor_origem,
                col_preencher=col_destino_preencher,
                sanitizar_monetario=True  # IEEE 754 fix automático
            )

            df_final = sync_result["df_resultado"]
            result["matched_total"] = sync_result["matched_total"]
            result["unmatched"] = sync_result["unmatched"]
            result["passes"] = sync_result["passes"]

            # ── EXPORTAR via ExportService (único exportador do projeto) ──
            if out_path is None:
                base = os.path.splitext(path_destino)[0]
                out_path = base + "_SYNC.xlsx"
                result["output_path"] = out_path

            exporter.export(df_final, out_path, format_type=None)
            logging.info(f"[TransformEngine] Exportado: {out_path}")

            # ── AUDITORIA LGPD (Art. 37 — rastreabilidade) ──
            auditor.record_sync(
                src_file=path_origem,
                tgt_file=path_destino,
                rows_affected=result["matched_total"]
            )

            result["success"] = True

            if result["unmatched"] > 0:
                result["warnings"].append(
                    f"{result['unmatched']} linhas sem correspondência de preço."
                )

        except Exception as e:
            logging.error(f"[TransformEngine] Erro crítico: {e}")
            result["warnings"].append(f"Erro interno: {str(e)}")

        return result

    @classmethod
    def apply_pipeline(cls, df_source: Any, transform_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Stub para pipeline de transformações futuras."""
        return {
            "status": "pending",
            "dataframe_final": None,
            "dropped_columns": [],
            "notes": ["Pipeline de transformação planejado para versão futura"]
        }
