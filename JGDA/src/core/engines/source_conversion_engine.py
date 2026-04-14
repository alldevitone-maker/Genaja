import os
from typing import Dict, Any, List
from version import __version__

class SourceConversionEngine:
    """
    Genaja Stable - Core de Desencriptação e Construção Secundária.
    Especializado em sanear fontes reprovadas pela inspeção nativa.
    """

    @classmethod
    def process_conversion(cls, file_path: str, inspection_report: Dict[str, Any], out_path: str = None) -> Dict[str, Any]:
        """
        Recebe a trilha diagnosticada pela Inspection e constroi a representação matricial real.
        """
        if out_path is None:
            out_path = file_path + ".extracted.csv"
            
        result = {
            "status": "pending",
            "extracted_path": out_path,
            "raw_dataframe_cache": None,
            "notes": []
        }
        
        detected = inspection_report.get("detected_type")
        
        if detected == "xml_spreadsheet_2003":
            return cls._convert_xml_spreadsheet(file_path, result, out_path, inspection_report)
            
        elif detected == "html_table":
            return cls._convert_html_table(file_path, result, out_path, inspection_report)
            
        elif detected in ["xlsx/zip", "xls_legacy", "csv_or_text", "tsv_tabulated"]:
            return cls._convert_standard(file_path, result, out_path, inspection_report)

        result["status"] = "skipped"
        result["notes"].append(f"Nenhuma conversão especial disparada para o tipo detectado: {detected}")
        return result

    @classmethod
    def _convert_xml_spreadsheet(cls, file_path: str, result: Dict[str, Any], out_path: str, inspection_report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Derrete as tags XML do SAP e condensa num arquivo CSV genérico para ingestão suave do Pandas.
        Utiliza ElementTree com iterparse para não estourar a memória (streaming parse).
        """
        import xml.etree.ElementTree as ET
        import csv
        import logging

        extracted_path = out_path
        
        try:
            with open(extracted_path, 'w', encoding='utf-8', newline='') as f_out:
                writer = csv.writer(f_out, delimiter=';')
                
                # Namespace do Excel XML Spreadsheet
                ns = {'ss': 'urn:schemas-microsoft-com:office:spreadsheet'}
                
                context = ET.iterparse(file_path, events=("start", "end"))
                
                current_row = []
                row_count = 0
                in_row = False
                in_cell = False
                
                for event, elem in context:
                    # Strip namespace for tag check
                    tag_base = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
                    
                    if event == "start" and tag_base == "Row":
                        in_row = True
                        current_row = []
                    elif event == "end" and tag_base == "Data" and in_row:
                        current_row.append(elem.text.strip() if elem.text else "")
                        
                    elif event == "end" and tag_base == "Row":
                        if current_row:
                            row_count += 1
                            writer.writerow(current_row)
                            if row_count % 1000 == 0:
                                logging.info(f" - [XML Parser] {row_count} linhas processadas...")
                        in_row = False
                        # Limpa memoria da arvore rastreada
                        elem.clear()

            logging.info(f"Fim da Desencriptação: {row_count} linhas salvas em CSV.")
            result["status"] = "success"
            result["extracted_path"] = extracted_path
            result["notes"].append("XML convertido recursivamente para formato tabular matricial (;).")
        
        except Exception as e:
            error_detail = f"{type(e).__name__}: {str(e)}"
            logging.error(f"Falha na Desencriptação XML: {error_detail}")
            result["status"] = "error"
            result["notes"].append(f"Erro na reconstrução da matriz primária: {error_detail}")
            
        return result
        
    @classmethod
    def _convert_html_table(cls, file_path: str, result: Dict[str, Any], out_path: str, inspection_report: Dict[str, Any]) -> Dict[str, Any]:
        """Placeholder para conversão de Falso XLS baseado em HTML via Python nativo."""
        result["status"] = "error"
        result["notes"].append(f"Extrator de HTML table mascarado ainda pendente na v{__version__}.")
        return result

    @classmethod
    def _convert_standard(cls, file_path: str, result: Dict[str, Any], out_path: str, inspection_report: Dict[str, Any]) -> Dict[str, Any]:
        """Conversão baseada em Pandas para formatos de planilha reais (XLSX, XLS, CSV)."""
        import pandas as pd
        import logging
        try:
            logging.info(f"Iniciando conversão padrão: {file_path} -> {out_path}")
            
            # Detecção de motor por extensão
            if file_path.lower().endswith(('.xlsx', '.xlsm')):
                 df = pd.read_excel(file_path, engine='openpyxl')
            elif file_path.lower().endswith('.xls'):
                 try:
                     df = pd.read_excel(file_path, engine='xlrd')
                 except Exception as e:
                     # 🚨 L2: Fallback MDM para XLS legado corrompido ou com bytes ERP (0x8D)
                     if "codec" in str(e).lower() or "charmap" in str(e).lower():
                         logging.warning("⚠️ Falha de charmap detectada. Acionando Fallback Universal (latin1)...")
                         import xlrd
                         # Latin1 nunca falha na decodificação pois mapeia todos os 256 bytes
                         book = xlrd.open_workbook(file_path, encoding_override='latin1')
                         sheet = book.sheet_by_index(0)
                         rows_data = []
                         for r in range(sheet.nrows):
                             rows_data.append([sheet.cell_value(r, c) for c in range(sheet.ncols)])
                         
                         if rows_data:
                             headers = rows_data[0]
                             data = rows_data[1:]
                             df = pd.DataFrame(data, columns=headers)
                         else:
                             raise e
                     else:
                         raise e
            elif file_path.lower().endswith(('.csv', '.txt')):
                 df = pd.read_csv(file_path, sep=None, engine='python')
            else:
                 df = pd.read_excel(file_path) # Tentativa genérica
            
            # --- MECANICA DE CORRECAO AUTOMATICA ---
            if inspection_report.get("magic_fix"):
                logging.info("Aplicando Correções Automáticas de Integridade...")
                df = cls.apply_magic_fixes(df)
            
            if out_path.lower().endswith('.csv'):
                df.to_csv(out_path, index=False, sep=';', encoding='utf-8')
            elif out_path.lower().endswith('.parquet'):
                # 🩹 MODO ENGENHARIA: Forçar reconhecimento do motor Parquet no ambiente Windows
                try:
                    import pyarrow
                except ImportError:
                    import sys, os
                    # Busca agressiva na venv local
                    venv_site = os.path.abspath(os.path.join(os.getcwd(), ".venv", "Lib", "site-packages"))
                    if os.path.exists(venv_site):
                        if venv_site not in sys.path:
                            sys.path.append(venv_site)
                
                df.to_parquet(out_path, index=False)
            elif out_path.lower().endswith('.json'):
                df.to_json(out_path, orient='records', force_ascii=False)
            
            result["status"] = "success"
            result["extracted_path"] = out_path
            result["notes"].append(f"Conversão concluída ({len(df)} linhas extraídas).")
            return result
        except Exception as e:
            logging.error(f"Erro na Conversão Universal: {e}")
            result["status"] = "error"
            result["notes"].append(f"Falha na conversão universal: {str(e)}")
            return result

    @classmethod
    def apply_magic_fixes(cls, df: Any) -> Any:
        """
        Aplica limpeza automática: trim em strings e remoção de linhas 100% nulas.
        """
        import pandas as pd
        import numpy as np
        
        # 1. Trim em todas as colunas de texto
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
        
        # 2. Remover linhas 100% vazias
        df.dropna(how='all', inplace=True)
        
        # 3. Converter strings 'None', 'NaN', 'null' para nulo real do pandas
        df.replace(['None', 'NaN', 'null', 'nan'], np.nan, inplace=True)
        
        return df

    @classmethod
    def get_sample_rows(cls, file_path: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Lê uma amostra do arquivo de forma performática para o "Forensic Preview".
        Suporta CSV, XLSX, XLS e o XML do SAP (via partial parse).
        """
        import pandas as pd
        import logging

        try:
            ext = file_path.lower()

            if ext.endswith(('.csv', '.txt', '.tsv')):
                df = pd.read_csv(file_path, sep=None, engine='python', nrows=limit)
                return df.head(limit).to_dict('records')

            elif ext.endswith(('.xlsx', '.xlsm')):
                df = pd.read_excel(file_path, engine='openpyxl', nrows=limit)
                return df.head(limit).to_dict('records')

            elif ext.endswith('.xls'):
                # Pode ser falso XLS (XML SAP) — tenta smart-detect
                try:
                    with open(file_path, 'rb') as f:
                        header = f.read(512)
                    if b'<?xml' in header or b'<Workbook' in header:
                        # É um XML mascarado — usar o parser XML direto
                        return cls._sample_xml_spreadsheet(file_path, limit)
                    else:
                        try:
                            df = pd.read_excel(file_path, engine='xlrd', nrows=limit)
                            return df.head(limit).to_dict('records')
                        except Exception as e:
                            # 🚨 L2: Fallback Forense para XLS legado 'sujo'
                            if "codec" in str(e).lower() or "charmap" in str(e).lower():
                                import xlrd
                                book = xlrd.open_workbook(file_path, encoding_override='latin1')
                                sheet = book.sheet_by_index(0)
                                headers = [str(sheet.cell_value(0, c)) for c in range(sheet.ncols)]
                                rows = []
                                for r in range(1, min(sheet.nrows, limit + 1)):
                                    row_dict = {headers[c]: sheet.cell_value(r, c) for c in range(sheet.ncols)}
                                    rows.append(row_dict)
                                return rows
                            else:
                                raise e
                except Exception:
                    return cls._sample_xml_spreadsheet(file_path, limit)

            else:
                # Tentativa genérica com Pandas
                try:
                    df = pd.read_csv(file_path, sep=None, engine='python', nrows=limit)
                    return df.head(limit).to_dict('records')
                except Exception:
                    return []

        except Exception as e:
            logging.error(f"Erro ao capturar amostra: {e}")
            return []

    @classmethod
    def _sample_xml_spreadsheet(cls, file_path: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Parser parcial do XML Spreadsheet 2003 (SAP B1).
        Extrai as primeiras `limit` linhas sem carregar o arquivo inteiro.
        """
        import xml.etree.ElementTree as ET
        import logging

        try:
            context = ET.iterparse(file_path, events=("start", "end"))
            rows = []
            headers = []
            current_row = []
            in_row = False
            row_count = 0

            for event, elem in context:
                tag_base = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag

                if event == "start" and tag_base == "Row":
                    in_row = True
                    current_row = []
                elif event == "end" and tag_base == "Data" and in_row:
                    current_row.append(elem.text.strip() if elem.text else "")
                elif event == "end" and tag_base == "Row":
                    if current_row:
                        if not headers:
                            headers = current_row  # Primeira linha = cabeçalho
                        else:
                            row_dict = {headers[i]: current_row[i] if i < len(current_row) else "" for i in range(len(headers))}
                            rows.append(row_dict)
                            row_count += 1
                    in_row = False
                    elem.clear()

                    if row_count >= limit:
                        break

            return rows

        except Exception as e:
            logging.error(f"Erro ao fazer amostra XML SAP: {e}")
            return []

# --- Declaração de Versão do Módulo (Genaja Version Hook) ---
from version_hook import declare as _vdeclare
_vdeclare(__name__, __version__, "Core de conversão multi-formato (SAP XML, HTML, CSV) com correção automática")
