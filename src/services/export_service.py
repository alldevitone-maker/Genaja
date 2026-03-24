import os
import pandas as pd
import json

def export_data(df, filepath, export_fmt, log_callback=None):
    """
    Centraliza a exportação de dados em diversos formatos (Excel, CSV, SQL, JSON).
    """
    ext = os.path.splitext(filepath)[1].lower()
    
    if ext == '.csv':
        df.to_csv(filepath, index=False, sep=';', encoding='utf-8-sig')
        return True
    
    elif ext == '.sql':
        # Tabela padrão para exportação Genaja
        table_name = "genaja_export_v049"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"-- Genaja Universal SQL Export\n")
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
