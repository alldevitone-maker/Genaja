import tkinter as tk
import logging
import pandas as pd
from tkinter import ttk, scrolledtext, filedialog

class GenajaUI:
    def __init__(self, root, product_name, version, on_start, on_exit):
        self.root = root
        self.root.title(f"{product_name} {version}")
        self.root.geometry("1000x760")
        self.root.minsize(980, 700)
        
        # Tema Corporativo Moderno (Light)
        self.bg_color = "#f0f2f5"        # Cinza de fundo global
        self.card_bg = "#ffffff"         # Branco pros cards
        self.text_color = "#333333"      # Cinza chumbo/grafite
        self.title_color = "#1a365d"     # Azul escuro grafite
        self.accent_color = "#0062cc"    # Azul corporativo primario
        self.secondary_bg = "#e2e8f0"    # Cinza bordas e botoes secund.
        
        self.font_main = ("Segoe UI", 9)
        self.font_title = ("Segoe UI", 10, "bold")
        self.font_header = ("Segoe UI", 16, "bold")
        
        self.root.configure(bg=self.bg_color)
        
        style = ttk.Style()
        if 'clam' in style.theme_names():
            style.theme_use('clam')
        style.configure("TFrame", background=self.bg_color)
        style.configure("Card.TFrame", background=self.card_bg)
        style.configure("TLabel", background=self.card_bg, foreground=self.text_color, font=self.font_main)
        style.configure("TCheckbutton", background=self.card_bg, foreground=self.text_color, font=self.font_main)
        style.map("TCheckbutton", background=[("active", self.card_bg)])
        style.configure("Main.TButton", font=("Segoe UI", 11, "bold"), background=self.accent_color, foreground="white", borderwidth=0)
        style.map("Main.TButton", background=[("active", "#0056b3")])
        style.configure("Sec.TButton", font=self.font_main, background=self.secondary_bg, foreground=self.text_color, borderwidth=0)
        style.map("Sec.TButton", background=[("active", "#cbd5e1")])
        style.configure("Action.TButton", font=("Segoe UI", 10, "bold"), background="#64748b", foreground="white", borderwidth=0)
        style.map("Action.TButton", background=[("active", "#475569")])

        main = tk.Frame(root, bg=self.bg_color)
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Criação dos Elementos Isolada
        header_fr = tk.Frame(main, bg=self.bg_color)
        tk.Label(header_fr, text=f"{product_name}: Sincronizador de Dados", bg=self.bg_color, fg=self.title_color, font=self.font_header).pack(side=tk.LEFT)
        tk.Label(header_fr, text="Dashboard ETL", bg=self.bg_color, fg="#64748b", font=("Segoe UI", 10)).pack(side=tk.RIGHT, pady=5)

        self.arq_origem_var = tk.StringVar()
        self.arq_destino_var = tk.StringVar()

        def create_card(parent, title):
            card = tk.Frame(parent, bg=self.card_bg, highlightbackground="#cbd5e1", highlightthickness=1)
            tk.Label(card, text=title, font=self.font_title, fg=self.title_color, bg=self.card_bg).pack(anchor='w', padx=15, pady=(8, 2))
            content = tk.Frame(card, bg=self.card_bg)
            content.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 6))
            return card, content

        # =========================================================
        # BLOCO 1
        # =========================================================
        f1_card, f1 = create_card(main, "1. Bases de Dados e Chaves de Integração")

        fr_simples = tk.Frame(f1, bg=self.card_bg)
        fr_simples.pack(fill=tk.X, pady=2)
        tk.Label(fr_simples, text="Arquivo Origem:", width=18, anchor='e', bg=self.card_bg, fg=self.text_color).pack(side=tk.LEFT)
        e1 = tk.Entry(fr_simples, textvariable=self.arq_origem_var, bg="#f8fafc", fg=self.text_color, relief="solid", bd=1, font=self.font_main)
        e1.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=8, ipady=3)
        ttk.Button(fr_simples, text="Procurar...", style="Sec.TButton", command=self.browse_origem).pack(side=tk.RIGHT)

        fr_sap = tk.Frame(f1, bg=self.card_bg)
        fr_sap.pack(fill=tk.X, pady=2)
        tk.Label(fr_sap, text="Arquivo Destino:", width=18, anchor='e', bg=self.card_bg, fg=self.text_color).pack(side=tk.LEFT)
        e2 = tk.Entry(fr_sap, textvariable=self.arq_destino_var, bg="#f8fafc", fg=self.text_color, relief="solid", bd=1, font=self.font_main)
        e2.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=8, ipady=3)
        ttk.Button(fr_sap, text="Procurar...", style="Sec.TButton", command=self.browse_destino).pack(side=tk.RIGHT)

        fr_keys = tk.Frame(f1, bg=self.card_bg)
        fr_keys.pack(fill=tk.X, pady=(6,0))
        
        tk.Label(fr_keys, text="PK Origem:", bg=self.card_bg, fg=self.text_color).grid(row=0, column=0, sticky='e', padx=5, pady=2)
        self.combo_chave_origem = ttk.Combobox(fr_keys, state="readonly", width=25, font=self.font_main)
        self.combo_chave_origem.grid(row=0, column=1, sticky='w', padx=5, pady=2)

        tk.Label(fr_keys, text="PK Destino:", bg=self.card_bg, fg=self.text_color).grid(row=0, column=2, sticky='e', padx=15, pady=2)
        self.combo_chave_destino = ttk.Combobox(fr_keys, state="readonly", width=25, font=self.font_main)
        self.combo_chave_destino.grid(row=0, column=3, sticky='w', padx=5, pady=2)

        tk.Label(fr_keys, text="Coluna Extra Protegida do Destino (Ex: ID Interno do Alvo):", bg=self.card_bg, fg=self.title_color, font=("Segoe UI", 9, "bold")).grid(row=1, column=0, columnspan=2, sticky='e', padx=5, pady=(4,2))
        self.combo_col_extra = ttk.Combobox(fr_keys, state="readonly", width=25, font=self.font_main)
        self.combo_col_extra.grid(row=1, column=2, columnspan=2, sticky='w', padx=15, pady=(4,2))

        # =========================================================
        # BLOCO 2
        # =========================================================
        f2_card, f2 = create_card(main, "2. Seleção de Colunas a Sincronizar")
        self.list_avail_data = []

        search_fr = tk.Frame(f2, bg=self.card_bg)
        search_fr.pack(fill=tk.X, pady=(0,4))
        tk.Label(search_fr, text="🔍 Procurar Coluna:", bg=self.card_bg, fg=self.text_color).pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace_add('write', self.update_avail_listbox)
        tk.Entry(search_fr, textvariable=self.search_var, bg="#f8fafc", fg=self.text_color, relief="solid", bd=1, font=self.font_main, width=40).pack(side=tk.LEFT, padx=8, ipady=3)

        dual_fr = tk.Frame(f2, bg=self.card_bg)
        dual_fr.pack(fill=tk.BOTH, expand=True)

        tk.Label(dual_fr, text="Colunas Disponíveis:", bg=self.card_bg, fg="#64748b", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky='w', pady=2)
        tk.Label(dual_fr, text="Colunas Selecionadas:", bg=self.card_bg, fg="#64748b", font=("Segoe UI", 9, "bold")).grid(row=0, column=2, sticky='w', pady=2)

        self.list_avail = tk.Listbox(dual_fr, selectmode=tk.EXTENDED, bg="#f8fafc", fg=self.text_color, selectbackground=self.accent_color, relief="solid", bd=1, font=self.font_main, height=5)
        self.list_avail.grid(row=1, column=0, sticky='nsew')

        btn_fr = tk.Frame(dual_fr, bg=self.card_bg)
        btn_fr.grid(row=1, column=1, padx=15)
        ttk.Button(btn_fr, text="Adicionar  >", style="Action.TButton", command=self.add_cols).pack(pady=2, fill=tk.X)
        ttk.Button(btn_fr, text="<  Remover", style="Action.TButton", command=self.remove_cols).pack(pady=2, fill=tk.X)
        ttk.Button(btn_fr, text=">> Add Todos", style="Action.TButton", command=self.add_all_cols).pack(pady=2, fill=tk.X)
        ttk.Button(btn_fr, text="<< Limpar", style="Action.TButton", command=self.remove_all_cols).pack(pady=2, fill=tk.X)

        self.list_sel = tk.Listbox(dual_fr, selectmode=tk.EXTENDED, bg="#f8fafc", fg=self.text_color, selectbackground=self.accent_color, relief="solid", bd=1, font=self.font_main, height=5)
        self.list_sel.grid(row=1, column=2, sticky='nsew')
        
        dual_fr.grid_columnconfigure(0, weight=1)
        dual_fr.grid_columnconfigure(2, weight=1)

        # =========================================================
        # BLOCO 3
        # =========================================================
        f3_card, f3 = create_card(main, "3. Hub de Módulos (Ações)")
        
        self.f3_container = tk.Frame(f3, bg=self.card_bg)
        self.f3_container.pack(fill=tk.BOTH, expand=True)
        
        # --- MENU VIEW ---
        self.view_menu = tk.Frame(self.f3_container, bg=self.card_bg)
        tk.Label(self.view_menu, text="Escolha uma ação para realizar com os arquivos mapeados:", bg=self.card_bg, fg=self.text_color, font=self.font_title).pack(pady=(15, 10))
        
        btn_frame = tk.Frame(self.view_menu, bg=self.card_bg)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="🧹 Módulo de Limpeza e Atualização", style="Main.TButton", command=self.show_view_limpeza).pack(side=tk.LEFT, padx=10, ipady=12, ipadx=10)
        ttk.Button(btn_frame, text="🔍 Módulo Comparador de Arquivos", style="Main.TButton", command=self.show_view_comparador).pack(side=tk.LEFT, padx=10, ipady=12, ipadx=10)

        # --- VIEW LIMPEZA ---
        self.view_limpeza = tk.Frame(self.f3_container, bg=self.card_bg)
        
        header_limpeza = tk.Frame(self.view_limpeza, bg=self.card_bg)
        header_limpeza.pack(fill=tk.X)
        tk.Label(header_limpeza, text="Colunas Acumuladas Para Sincronização:", bg=self.card_bg, fg=self.title_color, font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, pady=(0,2))
        ttk.Button(header_limpeza, text="⬅️ Voltar ao Menu", style="Sec.TButton", command=self.show_view_menu).pack(side=tk.RIGHT)
        
        self.summary_text = scrolledtext.ScrolledText(self.view_limpeza, height=2, font=("Segoe UI", 10, "bold"), bg="#f1f5f9", fg=self.accent_color, relief="solid", borderwidth=1, wrap=tk.WORD)
        self.summary_text.pack(fill=tk.X, pady=(0,6))
        self.summary_text.insert(tk.END, "Nenhuma coluna selecionada no processo acima.")
        self.summary_text.config(state='disabled')
        
        rules_fr = tk.Frame(self.view_limpeza, bg=self.card_bg)
        rules_fr.pack(fill=tk.BOTH, expand=True)
        
        left_rule = tk.LabelFrame(rules_fr, text="Regras de Linha", bg=self.card_bg, fg=self.title_color, font=("Segoe UI", 9, "bold"), relief="solid", bd=1)
        left_rule.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5), pady=0)
        
        self.filter_qty_var = tk.BooleanVar(value=False)
        tk.Checkbutton(left_rule, text="Remover linhas com valor zero ou nulo nas colunas:", variable=self.filter_qty_var, command=self.toggle_qty_list).pack(anchor='w', padx=5, pady=(2,0))
        
        self.list_qty = tk.Listbox(left_rule, selectmode=tk.MULTIPLE, height=3, bg="#e2e8f0", fg=self.text_color, selectbackground=self.accent_color, relief="solid", bd=1, font=self.font_main, state='disabled')
        self.list_qty.pack(fill=tk.BOTH, expand=True, padx=10, pady=(2,6))

        right_rule = tk.LabelFrame(rules_fr, text="Regras de Estrutura Estruturais", bg=self.card_bg, fg=self.title_color, font=("Segoe UI", 9, "bold"), relief="solid", bd=1)
        right_rule.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0), pady=0)
        
        self.clean_output_var = tk.BooleanVar(value=False)
        self.trim_var = tk.BooleanVar(value=False)
        self.upper_var = tk.BooleanVar(value=False)
        tk.Checkbutton(right_rule, text="Manter APENAS as colunas selecionadas", variable=self.clean_output_var).pack(anchor='w', padx=5, pady=(5,2))
        tk.Checkbutton(right_rule, text="Trim (limpar espaços extras no início/fim)", variable=self.trim_var).pack(anchor='w', padx=5, pady=2)
        tk.Checkbutton(right_rule, text="Maiúsculas (converter para Capslock)", variable=self.upper_var).pack(anchor='w', padx=5, pady=2)

        # --- VIEW COMPARADOR ---
        self.view_comparador = tk.Frame(self.f3_container, bg=self.card_bg)
        header_comp = tk.Frame(self.view_comparador, bg=self.card_bg)
        header_comp.pack(fill=tk.X)
        tk.Label(header_comp, text="Opções de Comparação de Arquivos:", bg=self.card_bg, fg=self.title_color, font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, pady=(0,2))
        ttk.Button(header_comp, text="⬅️ Voltar ao Menu", style="Sec.TButton", command=self.show_view_menu).pack(side=tk.RIGHT)
        
        comp_fr = tk.LabelFrame(self.view_comparador, text="Sentido da Busca e Exportação", bg=self.card_bg, fg=self.title_color, font=("Segoe UI", 9, "bold"), relief="solid", bd=1)
        comp_fr.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.comp_tipo_var = tk.StringVar(value="falta_destino")
        tk.Radiobutton(comp_fr, text="Falta no Destino (O que existe na Origem mas não no Destino)", variable=self.comp_tipo_var, value="falta_destino", bg=self.card_bg, fg=self.text_color, font=self.font_main).pack(anchor='w', padx=10, pady=5)
        tk.Radiobutton(comp_fr, text="Falta na Origem (O que existe no Destino mas não  na Origem)", variable=self.comp_tipo_var, value="falta_origem", bg=self.card_bg, fg=self.text_color, font=self.font_main).pack(anchor='w', padx=10, pady=5)
        
        self.comp_clean_var = tk.BooleanVar(value=True)
        tk.Checkbutton(comp_fr, text="Exportar relatório mantendo apenas as chaves e colunas mapeadas", variable=self.comp_clean_var, bg=self.card_bg, fg=self.text_color, font=self.font_main).pack(anchor='w', padx=10, pady=(10, 5))

        self.active_module = None
        self.root.after(50, self.show_view_menu) # Inicia no Menu na proxima UI tick

        # =========================================================
        # Rodapé com Botões de Ação Principais e Log
        # =========================================================
        log_fr = tk.Frame(main, bg=self.bg_color)
        
        self.progress = ttk.Progressbar(log_fr, orient='horizontal', length=100, mode='determinate')
        self.progress.pack(fill=tk.X, pady=(0,2))
        
        self.log_area = scrolledtext.ScrolledText(log_fr, state='disabled', height=2, font=("Consolas", 8), bg="#ffffff", fg="#475569", relief="solid", borderwidth=1)
        self.log_area.pack(fill=tk.X)
        self.log_area.tag_config("error", foreground="#dc2626")
        self.log_area.tag_config("success", foreground="#16a34a")
        self.log_area.tag_config("warning", foreground="#ca8a04")

        btns = tk.Frame(main, bg=self.bg_color)
        self.btn_iniciar = ttk.Button(btns, text="Executar Sincronização", style="Main.TButton", command=on_start)
        self.btn_iniciar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, ipady=6)
        ttk.Button(btns, text="Resetar Tudo", style="Sec.TButton", command=self.clear_form).pack(side=tk.LEFT, padx=5, ipady=6, ipadx=10)
        ttk.Button(btns, text="Sair", style="Sec.TButton", command=on_exit).pack(side=tk.RIGHT, padx=5, ipady=6, ipadx=15)

        # =========================================================
        # EMPACOTAMENTO MASTER (A ordem de top vs bottom resolve cutoff bugs)
        # =========================================================
        header_fr.pack(side=tk.TOP, fill=tk.X, pady=(0, 5))
        f1_card.pack(side=tk.TOP, fill=tk.X, pady=4)
        
        # Pack Footer from BOTTOM to guarantee Button Visibility Uncut
        btns.pack(side=tk.BOTTOM, fill=tk.X, pady=(5, 0))
        log_fr.pack(side=tk.BOTTOM, fill=tk.X, pady=2)
        f3_card.pack(side=tk.BOTTOM, fill=tk.X, pady=4)
        
        # O F2 será espremido no centro de modo natural!
        f2_card.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=4)


    def show_view_menu(self):
        self.view_limpeza.pack_forget()
        self.view_comparador.pack_forget()
        self.view_menu.pack(fill=tk.BOTH, expand=True)
        self.btn_iniciar.config(text="Selecione um Módulo")
        self.btn_iniciar.state(['disabled'])
        self.active_module = None

    def show_view_limpeza(self):
        self.view_menu.pack_forget()
        self.view_comparador.pack_forget()
        self.view_limpeza.pack(fill=tk.BOTH, expand=True)
        self.btn_iniciar.config(text="Executar Sincronização")
        self.btn_iniciar.state(['!disabled'])
        self.active_module = 'LIMPEZA'

    def show_view_comparador(self):
        self.view_menu.pack_forget()
        self.view_limpeza.pack_forget()
        self.view_comparador.pack(fill=tk.BOTH, expand=True)
        self.btn_iniciar.config(text="Gerar Relatório de Diferenças")
        self.btn_iniciar.state(['!disabled'])
        self.active_module = 'COMPARADOR'

    # --- Lógica do Motor Visual ---
    def toggle_qty_list(self):
        if self.filter_qty_var.get():
            self.list_qty.config(state='normal', bg="#ffffff")
        else:
            self.list_qty.selection_clear(0, tk.END)
            self.list_qty.config(state='disabled', bg="#e2e8f0")

    def sync_step3_summary(self):
        sel_items = list(self.list_sel.get(0, tk.END))
        
        # Painel de Conferência
        self.summary_text.config(state='normal')
        self.summary_text.delete(1.0, tk.END)
        if sel_items:
            self.summary_text.insert(tk.END, "   |   ".join(sel_items))
        else:
            self.summary_text.insert(tk.END, "Nenhuma coluna selecionada no processo acima.")
        self.summary_text.config(state='disabled')

        was_disabled = self.list_qty['state'] == 'disabled'
        current_active = []
        if not was_disabled:
            current_active = [self.list_qty.get(i) for i in self.list_qty.curselection()]
            
        self.list_qty.config(state='normal')
        self.list_qty.delete(0, tk.END)
        for col in sel_items:
            self.list_qty.insert(tk.END, col)
            if col in current_active:
                self.list_qty.selection_set(tk.END)
                
        if was_disabled:
            self.list_qty.config(state='disabled')

    def browse_origem(self):
        filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if filepath:
            self.arq_origem_var.set(filepath)
            self.load_columns_from_file(filepath, "origem")

    def browse_destino(self):
        filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if filepath:
            self.arq_destino_var.set(filepath)
            self.load_columns_from_file(filepath, "destino")

    def load_columns_from_file(self, filepath, tipo):
        try:
            from services.excel_loader import find_best_header
            skip = find_best_header(filepath)
            df = pd.read_excel(filepath, skiprows=skip, nrows=0)
            cols = [str(c).strip() for c in df.columns if not str(c).lower().startswith('unnamed') and not str(c).lower().startswith('nan')]
            
            if tipo == "origem":
                self.combo_chave_origem['values'] = cols
                self.list_avail_data = cols
                self.search_var.set('')
                self.list_sel.delete(0, tk.END)
                self.update_avail_listbox()
                self.sync_step3_summary()
                self.append_log(f"[Origem] {len(cols)} colunas detectadas.", "SUCCESS")
                
                for c in cols:
                    if c.upper() == 'CODIGO':
                        self.combo_chave_origem.set(c)
                        break
            else:
                self.combo_chave_destino['values'] = cols
                self.combo_col_extra['values'] = [''] + cols
                self.append_log(f"[Destino] {len(cols)} colunas detectadas.", "SUCCESS")
                
                for c in cols:
                    if c.upper() == 'MATERIAL' or c.upper() == 'ITEMCODE':
                        self.combo_chave_destino.set(c)
                        break
                        
        except Exception as e:
            self.append_log(f"Aviso: Falha na leitura dinâmica da {tipo}: {e}", "WARNING")

    def update_avail_listbox(self, *args):
        search_term = self.search_var.get().lower()
        self.list_avail.delete(0, tk.END)
        sel_items = self.list_sel.get(0, tk.END)
        for col in self.list_avail_data:
            if search_term in col.lower() and col not in sel_items:
                self.list_avail.insert(tk.END, col)

    def add_cols(self):
        selected_indices = self.list_avail.curselection()
        for i in selected_indices:
            col = self.list_avail.get(i)
            self.list_sel.insert(tk.END, col)
        self.update_avail_listbox()
        self.sync_step3_summary()

    def remove_cols(self):
        selected_indices = self.list_sel.curselection()
        for i in reversed(selected_indices):
            self.list_sel.delete(i)
        self.update_avail_listbox()
        self.sync_step3_summary()

    def add_all_cols(self):
        for col in self.list_avail_data:
            if col not in self.list_sel.get(0, tk.END):
                self.list_sel.insert(tk.END, col)
        self.update_avail_listbox()
        self.sync_step3_summary()

    def remove_all_cols(self):
        self.list_sel.delete(0, tk.END)
        self.update_avail_listbox()
        self.sync_step3_summary()

    def clear_form(self):
        self.arq_origem_var.set("")
        self.arq_destino_var.set("")
        self.combo_chave_origem.set("")
        self.combo_chave_destino.set("")
        self.combo_col_extra.set("")
        self.clean_output_var.set(False)
        self.filter_qty_var.set(False)
        self.trim_var.set(False)
        self.upper_var.set(False)
        self.search_var.set("")
        self.list_avail_data = []
        self.list_avail.delete(0, tk.END)
        self.list_sel.delete(0, tk.END)
        self.combo_chave_origem['values'] = []
        self.combo_chave_destino['values'] = []
        self.combo_col_extra['values'] = []
        self.sync_step3_summary()
        self.toggle_qty_list() # resets qty multi-dropdown visually
        self.append_log("Formulário resetado.", "INFO")

    def get_inputs(self):
        return {
            "active_module": getattr(self, 'active_module', None),
            "comp_tipo": getattr(self, 'comp_tipo_var', tk.StringVar()).get() if hasattr(self, 'comp_tipo_var') else None,
            "comp_clean": getattr(self, 'comp_clean_var', tk.BooleanVar()).get() if hasattr(self, 'comp_clean_var') else False,
            "arq_origem": self.arq_origem_var.get().strip(),
            "arq_destino": self.arq_destino_var.get().strip(),
            "chave_origem": self.combo_chave_origem.get().strip(),
            "chave_destino": self.combo_chave_destino.get().strip(),
            "col_extra": [self.combo_col_extra.get().strip()] if self.combo_col_extra.get().strip() else [],
            "colunas": list(self.list_sel.get(0, tk.END)),
            "clean_output": self.clean_output_var.get(),
            "filter_qty": self.filter_qty_var.get(),
            "filter_qty_cols": [self.list_qty.get(i) for i in self.list_qty.curselection()] if self.filter_qty_var.get() else [],
            "trim": self.trim_var.get(),
            "upper": self.upper_var.get()
        }

    def toggle_controls(self, enable=True):
        if enable:
            self.btn_iniciar.state(['!disabled'])
        else:
            self.btn_iniciar.state(['disabled'])
            self.log_area.config(state='normal')
            self.log_area.delete(1.0, tk.END)
            self.log_area.config(state='disabled')

    def append_log(self, msg, level="INFO"):
        self.log_area.config(state='normal')
        tag = "error" if level == "ERROR" else "success" if level == "SUCCESS" else "warning" if level == "WARNING" else None
        icon = "❌" if level == "ERROR" else "✅" if level == "SUCCESS" else "⚠️" if level == "WARNING" else "ℹ️"
        self.log_area.insert(tk.END, f"{icon} {msg}\n", tag)
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')
        self.root.update()
        
        if level == "ERROR": logging.error(msg)
        elif level == "WARNING": logging.warning(msg)
        else: logging.info(msg)

    def set_progress(self, val, total):
        self.progress['maximum'] = total
        self.progress['value'] = val
        self.root.update()
