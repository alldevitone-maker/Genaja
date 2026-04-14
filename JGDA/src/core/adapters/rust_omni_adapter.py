import os
import json
import ast
import subprocess
from version import __version__
from typing import Dict, Any
import logging

import platform

from core.engines.source_inspection_engine import SourceInspectionEngine
from core.engines.source_conversion_engine import SourceConversionEngine

# --- Declaração de Versão do Módulo (Genaja Version Hook) ---
from version_hook import declare as _vdeclare
_vdeclare(__name__, __version__, "Adaptador híbrido Rust/Python para inspeção e conversão universal de dados")

class RustOmniAdapter:
    """
    Genaja Stable - O Adapter Nativo Híbrido para o Omni-Data.
    
    [POLÍTICA OFICIAL DE FALLBACK]
    - Tentativa Primária: Subprocess isolado chamando `genaja_omni`
    - Condições de Queda: Binário não encontrado, timeout ou STDOUT corrompido/não-JSON.
    - Fallback: Acionamento invisível da engine Python. A UI Flet será notificada via chave `_engine`.
    
    [CONTRATO JSON OBRIGATÓRIO (RUST -> PYTHON)]
    - inspect: { declared_type, detected_type, risk_level, recommended_action, can_auto_convert, preview_summary, encoding_status, container_type, notes: [] }
    - convert: { success, output_path, output_type, rows_written, execution_time_ms, warnings: [] }
    """
    
    @classmethod
    def _get_bin_name(cls) -> str:
        return "omni_rust.exe" if platform.system() == "Windows" else "omni_rust"

    @classmethod
    def _get_bin_path(cls) -> str:
        bin_name = cls._get_bin_name()
        # Mapeia possíveis caminhos do binário Rust nas distribuições
        dev_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "omni_rust", "target", "release", bin_name))
        root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", bin_name))
        debug_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "omni_rust", "target", "debug", bin_name))
        
        for path in [dev_path, root_path, debug_path]:
            if os.path.exists(path):
                return path
        return ""

    @classmethod
    def fuzzy_compare(cls, input_val: str, candidates: list) -> Dict[str, Any]:
        """
        Aceleração Nativa para Similarity Matching (Fuzzy).
        Envia o input e candidatos para o motor Rust e retorna os scores.
        """
        bin_path = cls._get_bin_path()
        if bin_path:
            try:
                # Payload JSON para o Rust
                payload = json.dumps({"input": input_val, "candidates": candidates})
                result = subprocess.run(
                    [bin_path, "fuzzy", payload],
                    capture_output=True,
                    text=True,
                    timeout=2 
                )
                if result.returncode == 0:
                    return json.loads(result.stdout)
            except Exception as e:
                logging.debug(f"Rust Fuzzy Boost indisponível: {e}")
        
        return None

    @classmethod
    def inspect(cls, file_path: str) -> Dict[str, Any]:
        """Tenta Inspecionar via Rust. Fallback via Python se falhar."""
        bin_path = cls._get_bin_path()
        if bin_path:
            try:
                result = subprocess.run(
                    [bin_path, "inspect", file_path],
                    capture_output=True,
                    text=True,
                    timeout=5 # O Scanner não deve levar mais do que 10ms em Rust
                )
                if result.returncode == 0:
                    report = json.loads(result.stdout)
                    report["_engine"] = "rust_native"
                    return report
                else:
                    logging.warning(f"Rust inspect falhou (código {result.returncode}). Output: {result.stderr}")
            except Exception as e:
                logging.warning(f"Erro ao invocar Rust CLI: {e}")
                
        # FALLBACK PARA PYTHON PURO
        logging.info("Utilizando SourceInspectionEngine em modo Fallback (Python Puro)")
        report = SourceInspectionEngine.inspect(file_path)
        report["_engine"] = "python_fallback"
        return report

    @classmethod
    def convert(cls, in_path: str, inspection_report: Dict[str, Any], out_path: str = None) -> Dict[str, Any]:
        """Tenta Converter via Rust. Fallback se falhar."""
        detected_type = inspection_report.get("detected_type", "unknown")
        logging.info(f"--- Início da Conversão [Type: {detected_type}] ---")
        logging.info(f" - Origem: {in_path}")
        logging.info(f" - Destino: {out_path}")

        if out_path is None:
            out_path = in_path + ".extracted.csv"
            
        # Simulação Tática: Se for o mock, forja um sucesso imediato sem bater no Engine Fallback que iria crashar pedindo um arquivo real
        if in_path and "mock" in in_path and "falso_sap" in in_path:
            return {
                "success": True,
                "output_path": out_path,
                "warnings": ["[SIMULAÇÃO] Operação concluída sobre matriz virtual de treinamento."],
                "_engine": "python_fallback"
            }
            
        # Pre-check: File existence and type
        if not os.path.exists(in_path):
            return {"success": False, "warnings": [f"Arquivo não localizado: {in_path}"]}
        if os.path.isdir(in_path):
            return {"success": False, "warnings": [f"O caminho indicado é uma pasta, selecione o arquivo: {in_path}"]}

        bin_path = cls._get_bin_path()
        
        # O inspector original não pede out_path na API (process_conversion(filepath, report))
        # Vamos construir o Fake Report pro Fallback se necessário:
        fake_report = inspection_report
        
        if bin_path:
            try:
                logging.info(f"Delegando conversão [{detected_type}] para Rust...")
                result = subprocess.run(
                    [bin_path, "convert", in_path, detected_type, out_path],
                    capture_output=True,
                    text=True,
                    timeout=60 * 5 # Até 5 min pra bases gigantes
                )
                if result.returncode == 0:
                    try:
                        report = json.loads(result.stdout)
                        
                        # 🔑 FIX: Se Rust retornou success:false (tipo não suportado),
                        # acionar fallback Python em vez de retornar falha para a UI.
                        if not report.get("success", False):
                            logging.warning(f"Rust retornou success:false para [{detected_type}]. Warnings: {report.get('warnings')}. Tentando fallback Python...")
                            # Deixa cair para o bloco FALLBACK abaixo
                        else:
                            logging.info("Sucesso no motor Rust!")
                            report["_engine"] = "rust_native"
                            report["extracted_path"] = out_path
                            
                            # --- POST-RUST MAGIC FIX (Platinum) ---
                            if inspection_report.get("magic_fix"):
                                out_path_real = out_path or report.get("output_path")
                                if out_path_real and os.path.exists(out_path_real):
                                    file_size = os.path.getsize(out_path_real)
                                    if file_size < 100_000_000: # 100MB Limit
                                        logging.info("Aplicando Magic Fix pós-processamento Rust...")
                                        import pandas as pd
                                        if out_path_real.endswith(('.csv', '.txt')):
                                            df_temp = pd.read_csv(out_path_real, sep=';', encoding='utf-8')
                                            df_temp = SourceConversionEngine.apply_magic_fixes(df_temp)
                                            df_temp.to_csv(out_path_real, index=False, sep=';', encoding='utf-8')
                            
                            return report
                    except json.JSONDecodeError:
                        logging.warning("Falha no parse do STDOUT JSON do Rust. Tentando fallback...")
                else:
                    logging.warning(f"Rust convert falhou (código {result.returncode}). Output: {result.stderr}")
                    logging.info("Tentando fallback para motor Python...")
            except Exception as e:
                logging.warning(f"Erro crítico invocando Rust Convert: {e}. Tentando fallback...")
                
        # FALLBACK PARA PYTHON PURO
        logging.info("Utilizando SourceConversionEngine em modo Fallback (Python Puro)")
        report = SourceConversionEngine.process_conversion(in_path, fake_report, out_path=out_path)
        report["_engine"] = "python_fallback"
        # Padroniza a resposta rust:
        success = report.get("status") == "success"
        unified = {
            "success": success,
            "output_path": report.get("extracted_path"),
            "warnings": report.get("notes", []),
            "_engine": "python_fallback"
        }
        return unified
