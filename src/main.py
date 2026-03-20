import sys
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
