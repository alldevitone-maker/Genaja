import tkinter as tk
from tkinter import ttk, colorchooser
from services.theme_service import ThemeService

class SettingsWindow:
    def __init__(self, parent, theme_service, on_update_callback):
        self.parent = parent
        self.theme_service = theme_service
        self.on_update = on_update_callback
        self.window = None
        
    def toggle(self):
        if self.window and self.window.winfo_exists():
            self.window.destroy()
            self.window = None
        else:
            self.show()

    def show(self):
        self.window = tk.Toplevel(self.parent)
        self.window.title("⚙️ Phoenix Customizer")
        self.window.geometry("350x650")
        self.window.attributes("-topmost", True)
        self.window.configure(bg="#F3F4F6")
        
        # O Customizer agora é uma janela flutuante
        self._build_content()

    def _build_content(self):
        # Header (VSCode Style)
        header = tk.Frame(self.window, bg="#1E293B", height=40)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="🎨 EDITOR DE TEMA ABSOLUTO", bg="#1E293B", fg="white", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=10)
        
        # Content Container (Scrollable)
        container = tk.Frame(self.window, bg="#F3F4F6", padx=15, pady=15)
        container.pack(fill=tk.BOTH, expand=True)

        # Seções de Cores
        self._add_section(container, "ESTRUTURA GLOBAL", [
            ("Fundo Principal", "bg_col"),
            ("Janelas de Sessão (Cards)", "surface_col"),
            ("Contornos/Bordas", "border_col"),
            ("Texto Global", "fg_col")
        ])

        self._add_section(container, "BOTÕES FUNCIONAIS", [
            ("Motor (Azul)", "action_bg"),
            ("Sinc (Verde)", "success_bg"),
            ("Dados (Ciano)", "warning_bg"),
            ("Chave PK", "pk_bg")
        ])

        # Footer Actions
        footer = tk.Frame(self.window, bg="#F3F4F6", pady=20)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        
        save_btn = tk.Button(footer, text="💾 SALVAR COMO PADRÃO", bg="#0D6EFD", fg="white", relief="flat", bd=0, 
                             font=("Segoe UI", 9, "bold"), pady=10, command=self._save_theme)
        save_btn.pack(fill=tk.X, padx=15)
        
        reset_btn = tk.Button(footer, text="🔄 RESETAR TEMA", bg="#6C757D", fg="white", relief="flat", bd=0,
                              font=("Segoe UI", 9), pady=5, command=self._reset_theme)
        reset_btn.pack(fill=tk.X, padx=15, pady=(5, 0))

    def _add_section(self, parent, title, fields):
        tk.Label(parent, text=title, bg="#F3F4F6", fg="#6B7280", font=("Segoe UI", 8, "bold")).pack(anchor=tk.W, pady=(15, 5))
        
        for label, key in fields:
            row = tk.Frame(parent, bg="#F3F4F6")
            row.pack(fill=tk.X, pady=4)
            tk.Label(row, text=label, bg="#F3F4F6", font=("Segoe UI", 9)).pack(side=tk.LEFT)
            
            # Botão de visualização/click de cor
            current_color = self.theme_service.current_theme.get(key, "#FFFFFF")
            btn = tk.Button(row, bg=current_color, width=3, relief="solid", bd=1, command=lambda k=key: self._pick_color(k))
            btn.pack(side=tk.RIGHT)
            
            # Entry para digitar o HEX diretamente
            hex_var = tk.StringVar(value=current_color)
            ent = tk.Entry(row, textvariable=hex_var, bg="white", font=("Consolas", 8), width=9, relief="solid", borderwidth=1)
            ent.pack(side=tk.RIGHT, padx=5)
            
            # Vincular digitação em tempo real
            ent.bind("<KeyRelease>", lambda e, k=key, v=hex_var: self._on_hex_typing(k, v))
            
            # Armazenar referência para atualizar visualmente
            if not hasattr(self, '_color_widgets'): self._color_widgets = {}
            self._color_widgets[key] = (btn, hex_var, ent)

    def _on_hex_typing(self, key, var):
        hex_val = var.get().strip()
        # Validação básica de HEX (format #RRGGBB)
        if len(hex_val) == 7 and hex_val.startswith("#"):
            try:
                # Se for uma cor válida para o Tkinter, aplica
                btn, _, _ = self._color_widgets[key]
                btn.config(bg=hex_val)
                self.theme_service.current_theme[key] = hex_val
                self.on_update(self.theme_service.current_theme)
            except:
                pass

    def _pick_color(self, key):
        initial = self.theme_service.current_theme.get(key, "#FFFFFF")
        color = colorchooser.askcolor(initialcolor=initial, title=f"Escolher Cor: {key}")
        if color[1]:
            self._update_local_color(key, color[1])

    def _update_local_color(self, key, hex_color):
        # Atualiza a memória e a UI do Customizer
        self.theme_service.current_theme[key] = hex_color
        btn, hex_var, _ = self._color_widgets[key]
        btn.config(bg=hex_color)
        hex_var.set(hex_color)
        
        # Dispara atualização em tempo real no app
        self.on_update(self.theme_service.current_theme)

    def _save_theme(self):
        self.theme_service.save_theme()
        tk.messagebox.showinfo("Customizer", "Tema salvo com sucesso como padrão! ✅")

    def _reset_theme(self):
        default = self.theme_service.DEFAULT_THEME.copy()
        self.theme_service.current_theme = default
        for key in self._color_widgets:
            col = default.get(key, "#FFFFFF")
            btn, hex_var, _ = self._color_widgets[key]
            btn.config(bg=col)
            hex_var.set(col)
        self.on_update(default)
