import sys
import os
import tkinter as tk
from tkinter import messagebox, filedialog

# Garante que o python encontre os pacotes dentro de src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.genaja_ui import GenajaUI
from utils.logger_setup import configure_logging
from version import __version__
from services.excel_loader import load_excel_data_with_adjustment
from services.etl_service import filter_dataframe_by_columns, apply_numeric_filter, process_data_synchronization, clean_empty_quantities_multi, process_data_comparison

class GenajaApp:
    ENGINE_NAME = "JGDA Engine"
    PRODUCT_NAME = "Genaja"

    def __init__(self): 
        self.root = tk.Tk()
        self.ui = GenajaUI(self.root, self.PRODUCT_NAME, __version__, self.on_start_process_click, self.root.quit)
        configure_logging()

    def log_message(self, mensagem, nivel="INFO"):
        self.ui.append_log(mensagem, nivel)

    def run(self):
        self.root.mainloop()

    def on_start_process_click(self):
        inputs = self.ui.get_inputs()
        
        if not inputs["arq_origem"] or not inputs["arq_destino"]:
            messagebox.showwarning("Aviso", "Selecione ambos os arquivos originais.", parent=self.root)
            return
        if not inputs["chave_origem"] or not inputs["chave_destino"]:
            messagebox.showwarning("Aviso", "Preencha as chaves principais.", parent=self.root)
            return
        if not inputs["colunas"]:
            messagebox.showwarning("Aviso", "Adicione pelo menos uma coluna para importar.", parent=self.root)
            return
        if inputs["filter_qty"] and not inputs.get("filter_qty_cols"):
            messagebox.showwarning("Aviso", "Filtro de quantidade ativo mas nenhuma coluna foi selecionada para a regra de linha.", parent=self.root)
            return

        self.ui.toggle_controls(enable=False)
        self.root.after(100, lambda: self.run_etl_engine_logic(inputs))

    def run_etl_engine_logic(self, inputs):
        try:
            self.log_message(f"--- Iniciando Engine {self.ENGINE_NAME} ---", "INFO")
            total_etapas = 4
            etapa = 1
            self.ui.set_progress(etapa, total_etapas)

            # 1. Carregamento auto-detectado (sem popups)
            df_origem = load_excel_data_with_adjustment(inputs["arq_origem"], "ORIGEM", self.root, self.log_message)
            if df_origem is None: 
                self.ui.toggle_controls(True); return

            etapa += 1; self.ui.set_progress(etapa, total_etapas)
            
            df_destino = load_excel_data_with_adjustment(inputs["arq_destino"], "DESTINO", self.root, self.log_message)
            if df_destino is None: 
                self.ui.toggle_controls(True); return

            etapa += 1; self.ui.set_progress(etapa, total_etapas)

            # 2. Configurações de Filtro e Colunas
            col_chave = inputs["chave_origem"]
            col_chave_destino = inputs["chave_destino"]
            cols_origem = inputs["colunas"]

            if col_chave not in df_origem.columns:
                self.log_message(f"Erro: Chave '{col_chave}' não encontrada na Origem.", "ERROR"); self.ui.toggle_controls(True); return
            if col_chave_destino not in df_destino.columns:
                self.log_message(f"Erro: Chave '{col_chave_destino}' não encontrada no Destino.", "ERROR"); self.ui.toggle_controls(True); return

            colunas_presentes_origem = [c for c in cols_origem if c in df_origem.columns]
            colunas_ausentes_origem = [c for c in cols_origem if c not in df_origem.columns]
            
            if colunas_ausentes_origem:
                self.log_message(f"Aviso: Ignorando colunas que não existem na Origem: {', '.join(colunas_ausentes_origem)}", "WARNING")
            if not colunas_presentes_origem:
                self.log_message("Erro Crítico: Nenhuma das colunas solicitadas existe.", "ERROR"); self.ui.toggle_controls(True); return

            # RAMIFICAÇÃO DE MÓDULOS (HUB)
            if inputs.get("active_module") == "COMPARADOR":
                self.log_message("🚀 Iniciando Módulo de Comparação (Anti-Join)...", "INFO")
                de_para = {c: c for c in colunas_presentes_origem}
                
                df_final, count = process_data_comparison(
                    df_origem, df_destino, col_chave, col_chave_destino, 
                    inputs["comp_tipo"], inputs["comp_clean"], de_para
                )
                
                if count == 0:
                    self.log_message("✅ Nenhuma diferença encontrada. As bases estão em sincronia perfeita no lado selecionado.", "SUCCESS")
                else:
                    self.log_message(f"⚠️ {count} registros faltantes encontrados na comparação.", "WARNING")
                    
                etapa += 1; self.ui.set_progress(etapa, total_etapas)

            else:
                self.log_message("🚀 Iniciando Módulo de Limpeza e Sincronização...", "INFO")
                # 3. Limpeza de DataFrame Origem (Filtro de Quantidade)
                df_origem_final = df_origem.copy()

                try:
                    df_origem_final = filter_dataframe_by_columns(df_origem_final, [col_chave] + colunas_presentes_origem)
                except Exception as e:
                    self.log_message(f"Erro ao filtrar colunas: {e}", "ERROR"); self.ui.toggle_controls(True); return

                # Sincroniza dados
                de_para = {col: col for col in colunas_presentes_origem}
                self.log_message("🚀 Injetando colunas (Join) e Sincronizando dados (Update)...", "INFO")
                df_final, count = process_data_synchronization(df_origem_final, df_destino, col_chave, col_chave_destino, de_para)
                etapa += 1; self.ui.set_progress(etapa, total_etapas)

                # Aplicação de Filtros de Formatação Avançados
                if inputs["trim"] or inputs["upper"]:
                    self.log_message("ℹ️ Aplicando formatação (Trim / UpperCase) nas colunas importadas.", "INFO")
                    for c in de_para.values():
                        if c in df_final.columns and df_final[c].dtype == object: # Se for texto
                            if inputs["trim"]:
                                df_final[c] = df_final[c].astype(str).str.strip()
                            if inputs["upper"]:
                                df_final[c] = df_final[c].astype(str).str.upper()

                # 4. Ordenação e Limpeza de Saída
                colunas_extras = inputs["col_extra"]
                
                if inputs["clean_output"]:
                    cols_final = colunas_extras + [col_chave_destino] + list(de_para.values())
                    cols_final = [c for c in dict.fromkeys(cols_final) if c in df_final.columns]
                    df_final = df_final[cols_final]
                    self.log_message("ℹ️ Saída filtrada: mantendo apenas chaves, campos extras e colunas importadas.", "INFO")
                else:
                    if colunas_extras:
                        all_cols = colunas_extras + [c for c in df_final.columns if c not in colunas_extras]
                        all_cols = [c for c in dict.fromkeys(all_cols) if c in df_final.columns]
                        df_final = df_final[all_cols]

                # 4.5. Regras de Linha na Tabela Final (Onde ocorre a expulsão física)
                if inputs["filter_qty"] and inputs.get("filter_qty_cols"):
                    cols_to_check = [c for c in inputs["filter_qty_cols"] if c in df_final.columns]
                    if cols_to_check:
                        antes = len(df_final)
                        df_final = clean_empty_quantities_multi(df_final, cols_to_check)
                        depois = len(df_final)
                        self.log_message(f"Expurgo de Linha: {antes - depois} registros excluídos (todas as colunas {cols_to_check} simultaneamente nulas/zeradas).", "INFO")
                    else:
                        self.log_message("Expurgo ignorado: Nenhuma das colunas selecionadas existe na saída.", "WARNING")

            # 5. Salvar
            salvar = filedialog.asksaveasfilename(defaultextension=".xlsx", title="Salvar Resultado", parent=self.root)
            if salvar:
                df_final.to_excel(salvar, index=False)
                self.log_message(f"✅ Concluído com sucesso! Registro afetados: {count}", "SUCCESS")
                messagebox.showinfo("Sucesso", "Importação e Sincronização finalizadas com sucesso!", parent=self.root)

        except Exception as e:
            self.log_message(f"Erro crítico: {e}", "ERROR")
        finally:
            self.ui.toggle_controls(True)
            self.ui.set_progress(total_etapas, total_etapas)

if __name__ == "__main__":
    app = GenajaApp()
    app.run()
