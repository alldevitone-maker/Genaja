import pandas as pd
from tkinter import simpledialog, messagebox, filedialog

def find_best_header(path):
    try:
        df_temp = pd.read_excel(path, nrows=20, header=None)
        best_row = 0
        max_non_nulls = 0
        for i, row in df_temp.iterrows():
            non_nulls = row.dropna().shape[0]
            if non_nulls > max_non_nulls:
                max_non_nulls = non_nulls
                best_row = i
        return best_row
    except Exception:
        return 0

def select_file_dialog(title, root, log_callback):
    f = filedialog.askopenfilename(title=title, filetypes=[("Excel", "*.xlsx *.xls")], parent=root)
    if f: log_callback(f"Arquivo: {f}")
    return f

def load_excel_data_with_adjustment(path, system_name, root, log_callback):
    log_callback(f"📂 Lendo {system_name} e Auto-detectando cabeçalho...", "INFO")
    
    skip = find_best_header(path)

    try:
        df = pd.read_excel(path, skiprows=skip)
        df.columns = [str(c).strip() for c in df.columns]
        df = df.loc[:, ~df.columns.str.contains('^Unnamed|^nan', case=False)]
        if df.empty: raise ValueError("Arquivo vazio")
        log_callback(f"✅ Carregado: {len(df)} linhas (detectado cabeçalho na linha {skip}).", "SUCCESS")
        return df
    except Exception as e:
        log_callback(f"Erro carga {system_name}: {e}", "ERROR"); return None
