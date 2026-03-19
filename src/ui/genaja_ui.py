import tkinter as tk
import logging
from tkinter import ttk, scrolledtext

class GenajaUI:
    def __init__(self, root, product_name, version, on_start, on_exit):
        self.root = root
        self.root.title(f"{product_name} {version}")
        self.root.geometry("800x600")
        style = ttk.Style(); style.theme_use('clam')

        main = tk.Frame(root); main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        tk.Label(main, text=f"{product_name}: JGDA Engine", font=("Helvetica", 16, "bold")).pack(pady=(0, 10))

        self.log_area = scrolledtext.ScrolledText(main, state='disabled', height=20, font=("Consolas", 10))
        self.log_area.pack(fill=tk.BOTH, expand=True, pady=5)
        self.log_area.tag_config("error", foreground="red"); self.log_area.tag_config("success", foreground="green"); self.log_area.tag_config("warning", foreground="orange")

        self.progress = ttk.Progressbar(main, orient='horizontal', length=100, mode='determinate')
        self.progress.pack(fill=tk.X, pady=10)

        # Feature: Checkbox para limpar saída
        self.clean_output_var = tk.BooleanVar(value=False)
        tk.Checkbutton(main, text="Manter apenas colunas selecionadas no arquivo final", variable=self.clean_output_var).pack(pady=5)

        btns = tk.Frame(main); btns.pack(fill=tk.X, pady=5)
        self.btn_iniciar = tk.Button(btns, text="Iniciar", command=on_start, bg="#007bff", fg="white", font=("Helvetica", 12, "bold"), height=2)
        self.btn_iniciar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        tk.Button(btns, text="Sair", command=on_exit, font=("Helvetica", 12)).pack(side=tk.RIGHT, padx=5)

    def toggle_controls(self, enable=True):
        self.btn_iniciar.config(state='normal' if enable else 'disabled')
        if not enable:
            self.log_area.config(state='normal'); self.log_area.delete(1.0, tk.END); self.log_area.config(state='disabled')

    def append_log(self, msg, level="INFO"):
        self.log_area.config(state='normal')
        tag = "error" if level == "ERROR" else "success" if level == "SUCCESS" else "warning" if level == "WARNING" else None
        icon = "❌" if level == "ERROR" else "✅" if level == "SUCCESS" else "⚠️" if level == "WARNING" else "ℹ️"
        self.log_area.insert(tk.END, f"{icon} {msg}\n", tag)
        self.log_area.see(tk.END); self.log_area.config(state='disabled')
        self.root.update()
        
        if level == "ERROR": logging.error(msg)
        elif level == "WARNING": logging.warning(msg)
        else: logging.info(msg)

    def set_progress(self, val, total):
        self.progress['maximum'] = total; self.progress['value'] = val; self.root.update()
