import pandas as pd
from tkinter import simpledialog, messagebox, filedialog

def select_file_dialog(title, root, log_callback):
    f = filedialog.askopenfilename(title=title, filetypes=[("Excel", "*.xlsx *.xls")], parent=root)
    if f: log_callback(f"Arquivo: {f}")
    return f

def load_excel_data_with_adjustment(path, system_name, root, log_callback):
    log_callback(f"📂 Lendo {system_name}...", "INFO")
    try: pd.read_excel(path, nrows=5) # teste
    except Exception as e: log_callback(f"Erro leitura: {e}", "ERROR"); return None

    skip = simpledialog.askinteger("Cabeçalho", f"Linha do cabeçalho de {system_name}:", parent=root, minvalue=0)
    if skip is None: log_callback("Cancelado.", "WARNING"); return None

    try:
        df = pd.read_excel(path, skiprows=skip)
        df.columns = [str(c).strip() for c in df.columns]
        df = df.loc[:, ~df.columns.str.contains('^Unnamed|^nan', case=False)]
        if df.empty: raise ValueError("Arquivo vazio")
        log_callback(f"Carregado: {len(df)} linhas.", "SUCCESS")
        return df
    except Exception as e:
        log_callback(f"Erro carga: {e}", "ERROR"); return None
