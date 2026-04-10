import os
import pandas as pd
import json
from version import __version__

class ExportService:
    def __init__(self):
        pass

    def export(self, df, filepath_or_format, format_type=None):
        """
        Exporta o DataFrame para o formato desejado.
        Pode receber um filepath completo ou um tipo de formato (ex: '.xlsx').
        """
        if format_type and not filepath_or_format.endswith(format_type):
            filepath = filepath_or_format + format_type
        else:
            filepath = filepath_or_format
            
        ext = os.path.splitext(filepath)[1].lower()
        
        if ext == '.csv':
            df.to_csv(filepath, index=False, sep=';', encoding='utf-8-sig')
            return True
        
        elif ext == '.sql':
            # Nome da tabela dinâmico baseado na versão (ex: genaja_export_v071)
            v_suffix = __version__.replace('.', '')
            table_name = f"genaja_export_v{v_suffix}"
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"-- Genaja Enterprise SQL Export\n")
                f.write(f"-- Generated on: {pd.Timestamp.now()}\n\n")
                cols = df.columns.tolist()
                cols_str = ", ".join([f"`{c}`" for c in cols])
                
                for row in df.itertuples(index=False):
                    vals = []
                    for v in row:
                        if pd.isna(v): vals.append("NULL")
                        elif isinstance(v, (str, bytes)): 
                            clean_v = str(v).replace("'", "''")
                            vals.append(f"'{clean_v}'")
                        else: vals.append(str(v))
                    vals_str = ", ".join(vals)
                    f.write(f"INSERT INTO {table_name} ({cols_str}) VALUES ({vals_str});\n")
            return True

        elif ext == '.json':
            df.to_json(filepath, orient='records', force_ascii=False, indent=4)
            return True
        
        elif ext == '.xlsx':
            df.to_excel(filepath, index=False)
            return True
            
        return False


# --- Declaração de Versão do Módulo (Genaja Version Hook) ---
from version_hook import declare as _vdeclare
_vdeclare(__name__, __version__, "Serviço de exportação multi-formato (Excel, CSV, JSON, SQL) com suporte a LGPD")
