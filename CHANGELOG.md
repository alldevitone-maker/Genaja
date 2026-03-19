# Changelog

## [v0.3.5] - 19/03/2026 (Git Preparation)
### Adicionado
- Arquivo `.gitignore` para exclusão de arquivos temporários, logs e backups do controle de versão.
- Preparação do ambiente para inicialização do repositório Git/GitHub.

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
