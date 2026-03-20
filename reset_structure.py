import os
import shutil

# --- DEFINIÇÃO DO CONTEÚDO DOS ARQUIVOS (O CÓDIGO CORRETO) ---

CODE_MAIN = r'''import sys
import os
import tkinter as tk
from tkinter import messagebox

# Garante que o python encontre os pacotes dentro de src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importações da Arquitetura Modular
from ui.genaja_ui import GenajaUI
from utils.logger_setup import configure_logging
from version import __version__
from services.config_service import save_config_service, load_config_service
from services.excel_loader import load_excel_data_with_adjustment, select_file_dialog
from services.column_mapper import resolve_column_name_interactive
from services.etl_service import filter_dataframe_by_columns, apply_numeric_filter, process_data_synchronization

class GenajaApp:
    ENGINE_NAME = "JGDA Engine"
    PRODUCT_NAME = "Genaja"

    def __init__(self): 
        self.root = tk.Tk()
        # Inicializa a UI e passa os callbacks
        self.ui = GenajaUI(self.root, self.PRODUCT_NAME, __version__, self.on_start_process_click, self.root.quit)
        configure_logging()

    def log_message(self, mensagem, nivel="INFO"):
        """Centraliza logs para UI e Arquivo"""
        self.ui.append_log(mensagem, nivel)

    def run(self):
        self.root.mainloop()

    def on_start_process_click(self):
        self.ui.toggle_controls(enable=False)
        self.root.after(100, self.run_etl_engine_logic)

    def run_etl_engine_logic(self):
        try:
            self.log_message(f"--- Iniciando Engine {self.ENGINE_NAME} ---", "INFO")
            total_etapas = 6
            etapa = 1
            self.ui.set_progress(etapa, total_etapas)

            # Configuração
            config = None
            if messagebox.askyesno("Configuração", "Deseja carregar uma configuração salva?", parent=self.root):
                config = load_config_service(self.root, self.log_message)
            
            # 1. Carregamento
            arq1 = config.get('arq1') if config else select_file_dialog("Selecionar Origem (Simplesweb)", self.root, self.log_message)
            if not arq1: 
                self.ui.toggle_controls(True); return
            
            df_simples = load_excel_data_with_adjustment(arq1, "SIMPLESWEB", self.root, self.log_message)
            if df_simples is None: 
                self.ui.toggle_controls(True); return

            etapa += 1; self.ui.set_progress(etapa, total_etapas)
            
            arq2 = config.get('arq2') if config else select_file_dialog("Selecionar Destino (SAP)", self.root, self.log_message)
            if not arq2: 
                self.ui.toggle_controls(True); return
            
            df_sap = load_excel_data_with_adjustment(arq2, "SAP", self.root, self.log_message)
            if df_sap is None: 
                self.ui.toggle_controls(True); return

            etapa += 1; self.ui.set_progress(etapa, total_etapas)

            # 2. Chaves e Colunas
            col_chave = config.get('col_chave_simples') if config else resolve_column_name_interactive(df_simples, "Nome da coluna de CÓDIGO na Simplesweb", self.root, self.log_message)
            if not col_chave: 
                self.ui.toggle_controls(True); return

            etapa += 1; self.ui.set_progress(etapa, total_etapas)

            cols_origem = config.get('colunas_origem')
            if not cols_origem:
                from tkinter import simpledialog
                qtd = simpledialog.askinteger("Colunas", "Quantas colunas atualizar?", parent=self.root, minvalue=1)
                if not qtd: 
                    self.ui.toggle_controls(True); return
                cols_origem = []
                for i in range(qtd):
                    c = resolve_column_name_interactive(df_simples, f"Nome da {i+1}ª coluna", self.root, self.log_message)
                    if not c: self.ui.toggle_controls(True); return
                    cols_origem.append(c)

            etapa += 1; self.ui.set_progress(etapa, total_etapas)

            # Salvar Config
            if messagebox.askyesno("Salvar", "Salvar configuração?", parent=self.root):
                save_config_service({'arq1': arq1, 'arq2': arq2, 'col_chave_simples': col_chave, 'colunas_origem': cols_origem}, self.root, self.log_message)

            # 3. Processamento
            try:
                df_origem_final = filter_dataframe_by_columns(df_simples, [col_chave] + cols_origem)
            except Exception as e:
                self.log_message(f"Erro ao filtrar: {e}", "ERROR"); self.ui.toggle_controls(True); return

            for col in cols_origem:
                if messagebox.askyesno("Filtro", f"Filtrar > 0 para '{col}'?", parent=self.root):
                    df_origem_final = apply_numeric_filter(df_origem_final, col)

            # Mapeamento Destino
            col_chave_sap = resolve_column_name_interactive(df_sap, f"No SAP, qual é a chave para '{col_chave}'?", self.root, self.log_message)
            if not col_chave_sap: self.ui.toggle_controls(True); return

            de_para = {}
            for col in cols_origem:
                dest = resolve_column_name_interactive(df_sap, f"No SAP, '{col}' vai para onde?", self.root, self.log_message)
                if not dest: self.ui.toggle_controls(True); return
                de_para[col] = dest

            # Engine Run
            self.log_message("🚀 Sincronizando...", "INFO")
            df_final, count = process_data_synchronization(df_origem_final, df_sap, col_chave, col_chave_sap, de_para)

            # Feature: Checkbox Limpeza (v0.3.5)
            if self.ui.clean_output_var.get():
                # Mantém apenas a chave do SAP e as colunas que receberam dados
                cols_final = [col_chave_sap] + list(de_para.values())
                cols_final = list(dict.fromkeys(cols_final)) # Remove duplicatas
                df_final = df_final[cols_final]
                self.log_message("ℹ️ Saída filtrada: mantendo apenas colunas mapeadas.", "INFO")

            # Salvar
            from tkinter import filedialog
            salvar = filedialog.asksaveasfilename(defaultextension=".xlsx", title="Salvar Resultado", parent=self.root)
            if salvar:
                df_final.to_excel(salvar, index=False)
                self.log_message(f"✅ Concluído! Itens atualizados: {count}", "SUCCESS")
                messagebox.showinfo("Sucesso", "Finalizado com sucesso!", parent=self.root)

        except Exception as e:
            self.log_message(f"Erro crítico: {e}", "ERROR")
        finally:
            self.ui.toggle_controls(True)

if __name__ == "__main__":
    app = GenajaApp()
    app.run()
'''

CODE_UI = r'''import tkinter as tk
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

        # Controls Area
        controls = tk.Frame(main); controls.pack(fill=tk.X, pady=5)
        
        # Checkbox Feature v0.3.5
        self.clean_output_var = tk.BooleanVar(value=False)
        self.chk_clean = tk.Checkbutton(controls, text="Manter apenas colunas mapeadas no destino (Limpeza)", var=self.clean_output_var, font=("Helvetica", 10))
        self.chk_clean.pack(side=tk.TOP, anchor='w', pady=(0, 5))

        btns = tk.Frame(controls); btns.pack(fill=tk.X)
        self.btn_iniciar = tk.Button(btns, text="Iniciar", command=on_start, bg="#007bff", fg="white", font=("Helvetica", 12, "bold"), height=2)
        self.btn_iniciar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        tk.Button(btns, text="Sair", command=on_exit, font=("Helvetica", 12)).pack(side=tk.RIGHT, padx=5)

    def toggle_controls(self, enable=True):
        self.btn_iniciar.config(state='normal' if enable else 'disabled')
        self.chk_clean.config(state='normal' if enable else 'disabled')
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
'''

CODE_LOGGER = r'''import logging
import os

def configure_logging():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) # volta de src/utils para JGDA
    log_dir = os.path.join(base_dir, 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    logging.basicConfig(
        filename=os.path.join(log_dir, 'genaja.log'),
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        encoding='utf-8'
    )
'''

CODE_CONFIG = r'''import json, os
from tkinter import messagebox

def get_config_path(filename):
    return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), filename)

def save_config_service(config, root, log_callback, filename='genaja_config.json'):
    try:
        path = get_config_path(filename)
        with open(path, 'w', encoding='utf-8') as f: json.dump(config, f, indent=4)
        log_callback(f"Configuração salva: {path}", "SUCCESS")
    except Exception as e:
        log_callback(f"Erro ao salvar: {e}", "ERROR")

def load_config_service(root, log_callback, filename='genaja_config.json'):
    try:
        path = get_config_path(filename)
        if not os.path.exists(path): return None
        with open(path, 'r', encoding='utf-8') as f:
            log_callback(f"Configuração carregada: {path}", "SUCCESS")
            return json.load(f)
    except Exception as e:
        log_callback(f"Erro ao carregar: {e}", "ERROR"); return None
'''

CODE_EXCEL = r'''import pandas as pd
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
'''

CODE_MAPPER = r'''import difflib
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
'''

CODE_ETL = r'''import pandas as pd

def filter_dataframe_by_columns(df, cols):
    unique = list(dict.fromkeys(cols)) # remove duplicatas preservando ordem
    return df[unique].copy()

def apply_numeric_filter(df, col):
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    return df[df[col] > 0]

def process_data_synchronization(df_src, df_tgt, key_src, key_tgt, mapping):
    df_final = df_tgt.copy()
    
    # Prepara dados de atualização (Origem)
    update_data = (
        df_src.set_index(key_src)
        .groupby(level=0).last() # remove duplicatas na chave
        .rename(columns=mapping)
    )
    
    df_final.set_index(key_tgt, inplace=True)
    df_final.update(update_data)
    df_final.reset_index(inplace=True)
    
    matches = df_tgt[key_tgt].isin(df_src[key_src]).sum()
    return df_final, matches
'''

CODE_VERSION = r'''__version__ = "v0.3.5"
'''

# --- LOGICA DE CRIAÇÃO ---

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, 'src')
FILES_TO_KILL = [
    # Arquivos que não deveriam estar na raiz do projeto JGDA
    "main.py",
    "config_service.py",
    "excel_loader.py",
    "column_mapper.py",
    "etl_service.py",
    "genaja_ui.py",
    "cleanup.py", # Não será mais necessário
    # Pastas de cache
    "__pycache__"
]

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Criado: {os.path.relpath(path, BASE_DIR)}")

def run_reset():
    print("🚧 INICIANDO REESTRUTURAÇÃO COMPLETA (HARD RESET) 🚧")
    
    # 0. Matar arquivos soltos na raiz (Limpeza Agressiva)
    print("🔪 Removendo arquivos soltos incorretos na raiz...")
    for fname in FILES_TO_KILL:
        fpath = os.path.join(BASE_DIR, fname)
        if os.path.exists(fpath):
            if os.path.isdir(fpath):
                shutil.rmtree(fpath)
            else:
                os.remove(fpath)
            print(f"   ❌ Deletado: {fname}")

    # 1. Limpar pasta src antiga se existir
    if os.path.exists(SRC_DIR):
        print("🗑️  Removendo pasta src antiga e bagunçada...")
        shutil.rmtree(SRC_DIR)
    
    # 2. Recriar estrutura
    print("🏗️  Recriando estrutura limpa...")
    
    structure = {
        os.path.join(SRC_DIR, 'main.py'): CODE_MAIN,
        os.path.join(SRC_DIR, 'version.py'): CODE_VERSION,
        os.path.join(SRC_DIR, 'ui', 'genaja_ui.py'): CODE_UI,
        os.path.join(SRC_DIR, 'ui', '__init__.py'): "",
        os.path.join(SRC_DIR, 'utils', 'logger_setup.py'): CODE_LOGGER,
        os.path.join(SRC_DIR, 'utils', '__init__.py'): "",
        os.path.join(SRC_DIR, 'services', 'config_service.py'): CODE_CONFIG,
        os.path.join(SRC_DIR, 'services', 'excel_loader.py'): CODE_EXCEL,
        os.path.join(SRC_DIR, 'services', 'column_mapper.py'): CODE_MAPPER,
        os.path.join(SRC_DIR, 'services', 'etl_service.py'): CODE_ETL,
        os.path.join(SRC_DIR, 'services', '__init__.py'): ""
    }

    for path, content in structure.items():
        create_file(path, content)

    print("-" * 40)
    print("✨ REESTRUTURAÇÃO CONCLUÍDA COM SUCESSO! ✨")
    print("Agora você tem uma estrutura Canon (Padrão) limpa.")
    print("Execute: python src/main.py")

if __name__ == "__main__":
    run_reset()