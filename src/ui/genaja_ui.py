import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class GenajaUI:
    def __init__(self, root, title, version, callbacks):
        self.root = root
        self.root.title(f"{title} - Inteligência de Sincronização e ETL (v{version}) - WIZARD")
        self.root.geometry("850x700")
        
        # Tema Escuro Elegante
        self.style = ttk.Style(self.root)
        if "clam" in self.style.theme_names():
            self.style.theme_use("clam")
        
        bg_col = "#2B2D30"
        fg_col = "#DFE1E5"
        self.root.configure(bg=bg_col)
        self.style.configure(".", background=bg_col, foreground=fg_col, font=("Segoe UI", 10))
        self.style.configure("TFrame", background=bg_col)
        self.style.configure("TLabel", background=bg_col, foreground=fg_col)
        self.style.configure("TButton", padding=6, relief="flat", background="#3A3D41", foreground=fg_col, font=("Segoe UI", 10, "bold"))
        self.style.map("TButton", background=[("active", "#4A4D51")])
        self.style.configure("Action.TButton", background="#007BFF", foreground="white")
        self.style.map("Action.TButton", background=[("active", "#0056b3")])
        self.style.configure("Success.TButton", background="#28A745", foreground="white")
        self.style.map("Success.TButton", background=[("active", "#218838")])
        
        self.callbacks = callbacks # dict with: 'on_files_selected', 'on_process', 'on_cancel'
        
        # State Storage
        self.file_src = tk.StringVar()
        self.file_tgt = tk.StringVar()
        self.key_src = tk.StringVar()
        self.key_tgt = tk.StringVar()
        
        # Step 3 Data Data
        self.cols_src = []
        self.cols_tgt = []
        
        self.main_container = ttk.Frame(self.root, padding=20)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Dictionaries for views
        self.views = {}
        self.current_view = None
        
        self.build_step1()
        self.build_step2()
        self.build_step3()
        
        self.show_view("step1")
        
    def show_view(self, name):
        if self.current_view:
            self.views[self.current_view].pack_forget()
        self.views[name].pack(fill=tk.BOTH, expand=True)
        self.current_view = name
        
    def _ask_file(self, var):
        f = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if f: var.set(f)

    # --- STEP 1: UPLOAD ---
    def build_step1(self):
        f = ttk.Frame(self.main_container)
        self.views["step1"] = f
        
        ttk.Label(f, text="Passo 1: Conexão de Arquivos", font=("Segoe UI", 16, "bold"), foreground="#007BFF").pack(pady=20)
        ttk.Label(f, text="Selecione as planilhas para iniciação da análise de I.A.").pack(pady=(0, 20))
        
        # Card Origem
        c1 = ttk.LabelFrame(f, text=" [1] Arquivo de Origem (Novos Dados) ")
        c1.pack(fill=tk.X, pady=10)
        ttk.Entry(c1, textvariable=self.file_src, state="readonly", width=80).pack(side=tk.LEFT, padx=10, pady=15, expand=True, fill=tk.X)
        ttk.Button(c1, text="Buscar", command=lambda: self._ask_file(self.file_src)).pack(side=tk.RIGHT, padx=10, pady=15)
        
        # Card Destino
        c2 = ttk.LabelFrame(f, text=" [2] Arquivo de Destino (Base Atual a ser Mapeada/Limpa) ")
        c2.pack(fill=tk.X, pady=10)
        ttk.Entry(c2, textvariable=self.file_tgt, state="readonly", width=80).pack(side=tk.LEFT, padx=10, pady=15, expand=True, fill=tk.X)
        ttk.Button(c2, text="Buscar", command=lambda: self._ask_file(self.file_tgt)).pack(side=tk.RIGHT, padx=10, pady=15)
        
        # Navigation
        nav = ttk.Frame(f)
        nav.pack(fill=tk.X, pady=30)
        ttk.Button(nav, text="Avançar (I.A Analysis) ➔", style="Action.TButton", command=self.on_step1_next).pack(side=tk.RIGHT)

    def on_step1_next(self):
        if not self.file_src.get() or not self.file_tgt.get():
            messagebox.showwarning("Aviso", "Selecione os dois arquivos para prosseguir.")
            return
        # Transitioning... Let the controller do the heavy lifting
        self.callbacks['on_files_selected'](self.file_src.get(), self.file_tgt.get())

    # --- STEP 2: AI MATCH ---
    def build_step2(self):
        f = ttk.Frame(self.main_container)
        self.views["step2"] = f
        
        ttk.Label(f, text="Passo 2: I.A Auto-Mapping", font=("Segoe UI", 16, "bold"), foreground="#007BFF").pack(pady=20)
        
        self.ai_status_lbl = ttk.Label(f, text="Mapeamento sugerido pela Inteligência:", font=("Segoe UI", 11))
        self.ai_status_lbl.pack(pady=(0, 20))
        
        # Combos
        row = ttk.Frame(f)
        row.pack(fill=tk.X, pady=10)
        
        ttk.Label(row, text="Chave Primária da Origem:").pack(side=tk.LEFT, padx=(0,5))
        self.combo_src = ttk.Combobox(row, textvariable=self.key_src, state="readonly", width=30)
        self.combo_src.pack(side=tk.LEFT, padx=(0,20))
        
        ttk.Label(row, text="🔗 cruza com 🔗", foreground="#007BFF").pack(side=tk.LEFT, padx=10)
        
        ttk.Label(row, text="Chave Primária do Destino:").pack(side=tk.LEFT, padx=(20,5))
        self.combo_tgt = ttk.Combobox(row, textvariable=self.key_tgt, state="readonly", width=30)
        self.combo_tgt.pack(side=tk.LEFT)
        
        # Navigation
        nav = ttk.Frame(f)
        nav.pack(fill=tk.X, pady=50)
        ttk.Button(nav, text="⬅️ Voltar", command=lambda: self.show_view('step1')).pack(side=tk.LEFT)
        ttk.Button(nav, text="Confirmar Chaves ➔", style="Action.TButton", command=self.on_step2_next).pack(side=tk.RIGHT)

    def set_step2_data(self, cols_src, cols_tgt, best_s, best_t, score):
        self.cols_src = cols_src
        self.cols_tgt = cols_tgt
        self.combo_src['values'] = cols_src
        self.combo_tgt['values'] = cols_tgt
        
        if best_s and best_t and score > 0:
            self.key_src.set(best_s)
            self.key_tgt.set(best_t)
            self.ai_status_lbl.config(text=f"A I.A encontrou {score} valores em comum! Sugestão aplicada.", foreground="#28A745")
        else:
            self.ai_status_lbl.config(text="A I.A não encontrou cruzamentos evidentes. Selecione manualmente.", foreground="#DC3545")
        self.show_view('step2')

    def on_step2_next(self):
        if not self.key_src.get() or not self.key_tgt.get():
            messagebox.showwarning("Aviso", "Selecione as chaves primárias ou volte para alterar o arquivo.")
            return
        
        # Feed Step 3 Listboxes
        self.lb_src.delete(0, tk.END)
        for c in self.cols_src: self.lb_src.insert(tk.END, c)
        self.lb_tgt.delete(0, tk.END)
        for c in self.cols_tgt: self.lb_tgt.insert(tk.END, c)
        
        self.show_view('step3')

    # --- STEP 3: HUB ---
    def build_step3(self):
        f = ttk.Frame(self.main_container)
        self.views["step3"] = f
        
        # Top
        top = ttk.Frame(f)
        top.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(top, text="Passo 3: Mapeamento de Colunas & Hub", font=("Segoe UI", 16, "bold"), foreground="#007BFF").pack(side=tk.LEFT)
        ttk.Button(top, text="🔄 Recomeçar do Zero", command=lambda: self.show_view('step1')).pack(side=tk.RIGHT)
        
        # Mapeamento
        map_frame = ttk.LabelFrame(f, text=" Colunas para Transferir (Duplo Clique) ")
        map_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        cols_container = ttk.Frame(map_frame)
        cols_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # lists
        f_left = ttk.Frame(cols_container)
        f_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        ttk.Label(f_left, text="Disponíveis (Origem)").pack(anchor=tk.W)
        self.lb_src = tk.Listbox(f_left, selectmode=tk.MULTIPLE, bg="#333", fg="white")
        self.lb_src.pack(fill=tk.BOTH, expand=True)
        self.lb_src.bind('<Double-Button-1>', self._move_to_tgt)
        
        f_cent = ttk.Frame(cols_container)
        f_cent.pack(side=tk.LEFT, padx=10)
        ttk.Button(f_cent, text="Traspôr ➔", command=self._move_to_tgt).pack(pady=5)
        ttk.Button(f_cent, text="⬅️ Remover", command=self._remove_from_tgt).pack(pady=5)
        
        f_right = ttk.Frame(cols_container)
        f_right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        ttk.Label(f_right, text="Colunas Escolhidas (Sincronizar)").pack(anchor=tk.W)
        self.lb_tgt = tk.Listbox(f_right, selectmode=tk.MULTIPLE, bg="#1E3E26", fg="white")
        self.lb_tgt.pack(fill=tk.BOTH, expand=True)
        self.lb_tgt.bind('<Double-Button-1>', self._remove_from_tgt)
        
        # Checkboxes 
        ch_frame = ttk.LabelFrame(f, text=" Regras Globais de Faxina ")
        ch_frame.pack(fill=tk.X, pady=10)
        
        self.chk_upper = tk.BooleanVar(value=True)
        self.chk_trim = tk.BooleanVar(value=True)
        self.chk_zeros = tk.BooleanVar(value=False)
        self.action_module = tk.StringVar(value="Limpar")
        
        ttk.Checkbutton(ch_frame, text="Forçar MAIÚSCULAS", variable=self.chk_upper).pack(side=tk.LEFT, padx=10, pady=10)
        ttk.Checkbutton(ch_frame, text="Remover micro-espaços falsos", variable=self.chk_trim).pack(side=tk.LEFT, padx=10)
        ttk.Checkbutton(ch_frame, text="Remover Falsos Registros Zerados", variable=self.chk_zeros).pack(side=tk.LEFT, padx=10)
        
        # Hub Buttons
        hub_frame = ttk.Frame(f)
        hub_frame.pack(fill=tk.X, pady=15)
        
        ttk.Label(hub_frame, text="Módulo de Execução:").pack(side=tk.LEFT)
        ttk.Radiobutton(hub_frame, text="Sincronizar & Faxinar", variable=self.action_module, value="Limpar").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(hub_frame, text="Comparador Anti-Join (Falta no Destino)", variable=self.action_module, value="Falta no Destino").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(hub_frame, text="Comparador (Falta na Origem)", variable=self.action_module, value="Falta na Origem").pack(side=tk.LEFT, padx=10)
        
        # Bottom
        nav = ttk.Frame(f)
        nav.pack(fill=tk.X, pady=10)
        ttk.Button(nav, text="⬅️ Alterar Chaves Primárias", command=lambda: self.show_view('step2')).pack(side=tk.LEFT)
        self.btn_run = ttk.Button(nav, text="🚀 Executar Módulo & Exportar", style="Success.TButton", command=self.on_process)
        self.btn_run.pack(side=tk.RIGHT)

    def _move_to_tgt(self, event=None):
        sel = self.lb_src.curselection()
        for i in reversed(sel):
            val = self.lb_src.get(i)
            self.lb_tgt.insert(tk.END, val)
            self.lb_src.delete(i)
            
    def _remove_from_tgt(self, event=None):
        sel = self.lb_tgt.curselection()
        for i in reversed(sel):
            val = self.lb_tgt.get(i)
            self.lb_src.insert(tk.END, val)
            self.lb_tgt.delete(i)

    def get_final_inputs(self):
        return {
            "cols_mapped": list(self.lb_tgt.get(0, tk.END)),
            "chk_upper": self.chk_upper.get(),
            "chk_trim": self.chk_trim.get(),
            "chk_zeros": self.chk_zeros.get(),
            "module": self.action_module.get(),
            "key_src": self.key_src.get(),
            "key_tgt": self.key_tgt.get(),
            "file_src": self.file_src.get(),
            "file_tgt": self.file_tgt.get()
        }

    def on_process(self):
        inputs = self.get_final_inputs()
        if not inputs["cols_mapped"]:
            messagebox.showwarning("Aviso", "A lista de colunas a processar está vazia.")
            return
            
        # State lock
        self.btn_run.config(state="disabled")
        self.callbacks['on_process'](inputs)
        
    def unlock_ui(self):
        self.btn_run.config(state="normal")
