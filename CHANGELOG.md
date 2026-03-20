# Changelog

## [v0.4.0] - 20/03/2026 (Patch Pro UX & Advanced ETL)
### Adicionado / Modificado
- **Pro UI Mapeamento Dinâmico (Dual Listbox):** Seleção de colunas com Listboxes interativas (Disponíveis vs Selecionadas) em substituição à digitação manual, zerando taxa de erros (Typos).
- **Proteção Absoluta de Chaves (Combobox):** Caixas de chaves primárias agora são *Read-Only* e populadas automaticamente no load dos arquivos (SimplesWeb e SAP).
- **Auto-Anchoring de Interface:** Geometria da tela recalculada e layouts empacotados com ancoragem absoluta no Rodapé, impedindo sumiço dos botões de ação em monitores de baixa resolução (Notebooks).
- **Divisão Lógica Passo 3 (Side-by-Side):** Separação visual clara em "Regras de Linhas" (que alteram quantidade de registros finais) e "Regras de Estrutura Estruturais" (que limpam colunas/textos mantendo a linha).
- **Exclusão Avançada por Lógica Booleana (OR Array):** A regra de "Dropar linhas com Qtd Nula/Zerada" foi generalizada. Agora permite selecionar Multi-Colunas pelo Listbox. A engine ETL cruza o teste com uma matriz *OR*, deletando a linha do arquivo gerado *apenas* se TODAS as colunas selecionadas forem simultaneamente invalidas. Textos literais (ex. 'parede') agora são preservados.

## [v0.3.9] - 20/03/2026 (VSCode Theme e Smart Autocomplete)
### Adicionado
- **Tema VSCode Dark:** A interface agora segue as paletas de cores do Visual Studio Code.
- **Smart Headers:** O `excel_loader` agora escaneia ativamente as primeiras 20 linhas do Excel em busca de metadados, pulando linhas vazias ou de título que geravam colunas `Unnamed`.
- **Auto-complete nos Combobox:** Barra de pesquisa em tempo real que filtra as colunas enquanto o usuário digita.
- **Novos Filtros de Regra de Negócio:** Checkboxes adicionados para realizar formatação Trim (remover espaços) e UpperCase (maiúsculas) nas colunas de texto importadas.

## [v0.3.8] - 20/03/2026 (Mega Patch UI e ETL)
### Modificado
- **Refatoração Completa da UI:** Substituição de pop-ups interativos por um painel HUD fixo com campos de texto para chaves e colunas.
- **Evolução do Filtro ETL:** O processo de sincronização Pandas agora adiciona (JOIN) novas colunas ao SAP se elas existirem na Origem e não no Destino, parando de se limitar apenas a atualizar colunas pré-existentes.

## [v0.3.7] - 20/03/2026 (Aplicação compliance)
### Modificado
- Aplicação de regras de compliance de projeto, isolando documentos e estratégias internas do repositório final.
- Atualização do arquivo README com escopo 9/9 concluído.

## [v0.3.6] - 19/03/2026 (Automated Workflow)
### Adicionado
- Script `release.py` para automação completa do ciclo de lançamento (versionamento, changelog, git tagging).
- Backup automático agora inclui o **Nome da Release** no nome do arquivo gerado (ex: `..._AutoBackup_Automated_Workflow.zip`).
- Variável `__title__` adicionada ao `src/version.py`.

## [v0.3.5] - 19/03/2026 (Git & Feature Checkbox)
### Adicionado
- Arquivo `.gitignore` para exclusão de arquivos temporários, logs e backups do controle de versão.
- Preparação do ambiente para inicialização do repositório Git/GitHub.
- **Feature:** Checkbox "Manter apenas colunas selecionadas". Permite filtrar o arquivo de saída mantendo apenas as colunas mapeadas e a chave.

## [v0.3.4] - 19/03/2026 (Stability & Path Fixes)
### Corrigido
- Ajustes na detecção de caminhos relativos (`os.getcwd` vs `__file__`) no `smoke_test.py` para execução via terminal.
- Melhoria na importação de módulos ao executar scripts fora da raiz.

## [v0.3.3] - 19/03/2026 (Versioning Automation)
### Regra de Versionamento
- **X.Y.Z**:
    - **X** (Major): Mudança de ciclo (ex: após v0.9.9).
    - **Y** (Minor): Novas funcionalidades/features.
    - **Z** (Patch): Correções de bugs, ajustes e refatorações de arquitetura.

### Adicionado
- Arquivo `src/version.py` para centralizar o controle de versão.
- Automação de backup integrada ao `smoke_test.py`. Toda execução de teste bem-sucedida gera um backup da versão atual.
- Interface gráfica agora exibe a versão dinâmica lida de `src/version.py`.

## [v0.3.1-dev] - 19/03/2026 (Versão Congelada / Ready for Java)
### Adicionado
- Estrutura inicial do projeto Genaja (JGDA).
- Logging configurado com encoding UTF-8.
- `src/main.py` como ponto de entrada principal.
- Documentação de Roadmap e README oficial.
- Snapshot de segurança (Backup) criado em `backups/v0.3.1-dev/`.

### Alterado
- Renomeação da classe principal para `GenajaApp`.
- Identidade visual e textos atualizados para "Genaja: Java Generic Data Access".
- Métodos refatorados para inglês técnico (ex: `load_excel_data_with_adjustment`).
- Base de código congelada para futura migração/modularização.

### Corrigido
- Bug na seleção de colunas duplicadas (chave vs colunas de atualização) que causava erro no Pandas.
