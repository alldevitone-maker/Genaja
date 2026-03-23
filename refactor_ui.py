import os
import re

with open('src/ui/genaja_ui.py', 'r', encoding='utf-8') as f:
    code = f.read()

new_f3_code = """        f3_card, f3 = create_card(main, "3. Hub de Módulos (Ações)")
        
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
        self.root.after(50, self.show_view_menu) # Inicia no Menu na proxima UI tick"""

code = re.sub(r'        f3_card, f3 = create_card\(main, "3\. Conferência Final e Regras de Limpeza"\).*?# =========================================================\n        # Rodapé com Botões de Ação Principais e Log', new_f3_code + '\n\n        # =========================================================\n        # Rodapé com Botões de Ação Principais e Log', code, flags=re.DOTALL)


methods_code = """
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

    # --- Lógica do Motor Visual ---"""

code = code.replace("    # --- Lógica do Motor Visual ---", methods_code)


old_get_inputs = """    def get_inputs(self):
        return {
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
        }"""
new_get_inputs = """    def get_inputs(self):
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
        }"""

code = code.replace(old_get_inputs, new_get_inputs)

with open('src/ui/genaja_ui.py', 'w', encoding='utf-8') as f:
    f.write(code)
    
print("UI Refactored!")
