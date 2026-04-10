import os
from version import __version__
from typing import Dict, Any

class SourceInspectionEngine:
    """
    Genaja Stable - Core de Quarentena e Inspeção Direcionada.
    NÃO POSSUI ACOPLAMENTO COM A UI E NÃO IMPORTA PANDAS.
    Analisa os magic-bytes do arquivo e identifica mutações ou anomalias (Ex: Arquivo XLS que na verdade é XML do SAP B1).
    """

    @classmethod
    def inspect(cls, file_path: str) -> Dict[str, Any]:
        """
        Inspeciona a fonte primária garantindo leitura segura.
        """
        report = {
            "declared_type": "unknown",
            "detected_type": "unknown",
            "risk_level": "low",
            "recommended_action": "proceed",
            "can_auto_convert": False,
            "preview_summary": "",
            "encoding_status": "utf-8",
            "container_type": "flat",
            "notes": []
        }

        if not os.path.exists(file_path):
            report["risk_level"] = "high"
            report["notes"].append("Arquivo não encontrado no sistema operacional.")
            return report

        # Normalização da Extensão
        ext = os.path.splitext(file_path)[1].lower().strip('.')
        report["declared_type"] = ext

        try:
            # Inspection via Raw Byte Streaming 
            # (zero dependência de Pandas/Flet - Memória controlada)
            with open(file_path, 'rb') as f:
                header_bytes = f.read(2048)
            
            # --- MAGIC BYTES DICTIONARY ---
            # PK Zip (XLSX, DOCX, etc)
            if header_bytes.startswith(b'PK\x03\x04'):
                report["detected_type"] = "xlsx/zip"
                report["container_type"] = "zip"
                report["recommended_action"] = "proceed" if ext in ["xlsx", "zip"] else "warn_extension"
            
            # Old Office (OLE2)
            elif header_bytes.startswith(b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1'):
                report["detected_type"] = "xls_legacy"
                report["container_type"] = "ole2"
            
            # SQLite Format
            elif header_bytes.startswith(b'SQLite format 3\x00'):
                report["detected_type"] = "sqlite"
                report["container_type"] = "db"
                report["risk_level"] = "medium"
                report["recommended_action"] = "extract_db"
            
            # XML SPREADSHEET 2003 (MUTAÇÃO DO SAP B1)
            elif header_bytes.lstrip().startswith(b'<?xml') and (b'progid="Excel.Sheet"' in header_bytes or b'urn:schemas-microsoft-com:office:spreadsheet' in header_bytes):
                report["detected_type"] = "xml_spreadsheet_2003"
                report["container_type"] = "xml"
                report["risk_level"] = "high"
                report["can_auto_convert"] = True
                report["recommended_action"] = "auto_convert"
                report["notes"].append("Falso XLS detectado (Estrutura XML nativa do SAP Business One).")
            
            # HTML Table masqueraded as XLS
            elif b'<table' in header_bytes.lower() and b'<tr' in header_bytes.lower():
                report["detected_type"] = "html_table"
                report["container_type"] = "html"
                report["can_auto_convert"] = True
                report["recommended_action"] = "auto_convert"
                report["notes"].append("Falso XLS detectado (Tabela HTML).")

            # JSON Data
            elif header_bytes.strip().startswith((b'{', b'[')) and b'"' in header_bytes:
                report["detected_type"] = "json"
                report["container_type"] = "text/json"
                
            # Executables / Assembly Binaries
            elif header_bytes.startswith(b'MZ'):
                report["detected_type"] = "pe_executable_dll"
                report["container_type"] = "binary"
                report["risk_level"] = "critical"
                report["notes"].append("Alerta de Segurança: Arquivo executável/binário do Windows detectado!")
            elif header_bytes.startswith(b'\x7fELF'):
                report["detected_type"] = "elf_executable"
                report["container_type"] = "binary"
                report["risk_level"] = "critical"
                report["notes"].append("Alerta de Segurança: Arquivo executável/binário Linux detectado!")

            # Parquet (Big Data)
            elif header_bytes.startswith(b'PAR1'):
                report["detected_type"] = "parquet"
                report["container_type"] = "binary/columnar"
                report["notes"].append("Formato Columnar Big Data (Parquet) identificado.")
                
            # PDF Format
            elif header_bytes.startswith(b'%PDF-'):
                report["detected_type"] = "pdf"
                report["container_type"] = "document"
                report["notes"].append("Documento PDF identificado. A extração de dados pode requerer OCR ou parsers complexos.")

            # Generic XML
            elif header_bytes.strip().startswith(b'<?xml'):
                report["detected_type"] = "xml_generic"
                report["container_type"] = "xml"

            # Fallback for CSV / Plain Text / Tabulated
            else:
                report["detected_type"] = "csv_or_text"
                
                # Sniffing delimeters for Tabulated data
                if b'\t' in header_bytes and b'\n' in header_bytes:
                     report["detected_type"] = "tsv_tabulated"
                     report["notes"].append("Delimitador provável: TAB (Planilha Textual)")
                elif b';' in header_bytes:
                    report["notes"].append("Delimitador provável: Ponto e Vírgula (;)")
                elif b',' in header_bytes:
                    report["notes"].append("Delimitador provável: Vírgula (,)")

            # Avaliação de Risco Baseada no Tipo
            if report["detected_type"] != "csv_or_text" and report["declared_type"] in ["csv", "txt"]:
                report["risk_level"] = "high"
                report["notes"].append("Conflito severo de extensão: Arquivo binário mascarado como texto.")
            elif report["detected_type"] in ["xml_spreadsheet_2003", "html_table"] and report["declared_type"] == "xls":
                report["risk_level"] = "medium" # Clássico do SAP

        except Exception as e:
            report["risk_level"] = "critical"
            report["notes"].append(f"Erro de leitura de baixo nível: {str(e)}")

        return report

# --- Declaração de Versão do Módulo (Genaja Version Hook) ---
from version_hook import declare as _vdeclare
_vdeclare(__name__, __version__, "Goleiro forense de inspeção de arquivos (Detecção de Magic Bytes e Fraude de Extensão)")
