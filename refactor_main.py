import os
import re

with open('src/main.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Fix import
code = code.replace("clean_empty_quantities_multi", "clean_empty_quantities_multi, process_data_comparison")

# Replace block from '# 3. Limpeza de' down to '# 5. Salvar'
replacement_logic = """            # RAMIFICAÇÃO DE MÓDULOS (HUB)
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

            # 5. Salvar"""

# Perform replacement via regex chunk block
pattern = re.compile(r"            # 3\. Limpeza de DataFrame Origem \(Filtro de Quantidade\).*?# 5\. Salvar", re.DOTALL)
code = pattern.sub(replacement_logic, code)

with open('src/main.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("main.py Refactored!")
