import difflib
from tkinter import simpledialog, messagebox

def resolve_column_name_interactive(df, msg, root, log_callback):
    cols = list(df.columns)
    while True:
        val = simpledialog.askstring("Coluna", f"Disponíveis:\n{cols}\n\n{msg}:", parent=root)
        if not val: log_callback("Cancelado.", "WARNING"); return None
        val = val.strip()
        if val in cols: 
            log_callback(f"Selecionado: {val}")
            return val
        
        match = difflib.get_close_matches(val, cols, n=1)
        if match and messagebox.askyesno("Sugestão", f"Quis dizer '{match[0]}'?", parent=root):
            log_callback(f"Aceito sugestão: {match[0]}")
            return match[0]
        messagebox.showerror("Erro", "Coluna não encontrada.")
