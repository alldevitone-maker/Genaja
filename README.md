# Genaja Wizard & IA API (v0.4.7) 🇧🇷 🇺🇸

## 🇧🇷 Português
**O Genaja** é um Hub Unificado de Inteligência de Sincronização e Auditoria (ETL) construído com foco corporativo em Big Data. O sistema permite transpor, validar e auditar colunas enormes do Excel com rapidez O(1) combinando poder de Processamento Pandas com interfaces fluídas em Tkinter.

### 🌟 Novidades da Versão 0.4.7 (Atualização Premium)
* **Design "Premium Slate"**: Cores renovadas focando em leitura e interfaces não padronizadas que trazem um visual corporativo moderno ao ETL.
* **Smart Tooltips (Dicas)**: Um motor inteligente e customizável criado do zero gera popups visuais nas ferramentas caso você não saiba como operá-las, com suporte ativável e desativável na aba superior (`💡 Desativar Dicas`).
* **Caixa Experimental (Big Data O(1))**: Acesso beta a motores de exportações massivas de até 10 milhões de linhas usando `JSON`, `CSV` e Scripts `SQL`. 
* **Global Canvas Scrolling**: O Hub de sincronização agora é flexível! Com uma barra de rolagem inteligente por toda a janela, laptops e telas menores (abaixo de `720p`) abrem o aplicativo limpidamente sem cortar os botões finais.
* **Sincronização Segura**: O cruzamento nativo impede mutações silenciosas vindas das bibliotecas Pandas (`_x` prefixes), garantindo relatórios livres de colunas ignoradas e vazias na auditoria (GAPS).
* **Reset Seguro (Hard Restart)**: Fizeram bagunça no mapeamento?  O novo botão 🔄 *Reiniciar App* deleta a memória RAM associada e realiza um "Reboot" no próprio script de Python.

---

## 🇺🇸 English
**Genaja** is a Unified Hub for Synchronization Intelligence and ETL Auditing designed with an enterprise-level focus on Big Data. The system allows you to easily transpose, validate and audit heavily-layered Excel columns in O(1) time using Pandas Dataframes mixed with a smooth Tkinter UX.

### 🌟 What's New in Version 0.4.7 (The Premium Update)
* **Premium Slate Design**: Readability-focused revamped colors providing a sleek, modern corporate aesthetic.
* **Smart Tooltips**: A custom-built hover motor that gives detailed GUI cues over any complex tool. Fully reversible by clicking the `💡 Toggle Hints` top button.
* **Experimental Output Box (Big Data O(1))**: Beta access to high-performance parsing models targeting tens of millions of rows via `JSON`, `CSV` or automated `SQL` dump scripts.
* **Global Canvas Scrolling**: The entire Hub is fully vertically-responsive windowed under a Canvas wrapper, solving "invisible cut-off buttons" issues on smaller-res monitors (`720p`).
* **Bulletproof Safe-Merge**: The native inner merge completely ignores and drops silent Pandas injections (such as `_x` and `_y` prefixes), bypassing invisible empty-document exports inside the GAPS Auditor algorithm.
* **Safe OS Restart**: Spilled out wrong columns mapping? The new bottom 🔄 *Restart App* button safely flushes all running memory and completely restarts the executing OS python process.

## Requisitos / Requirements
- Python 3.9+
- `pandas`, `openpyxl`, `tkinterdnd2`

## Execução / Running
```bash
python src/main.py
```