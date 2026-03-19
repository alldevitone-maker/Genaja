# Genaja: Java Generic Data Access (JGDA)

> **Versão Atual:** `v0.3.5` (Feature Added)  
> **Status do Roadmap:** [6/8] - Feature Checkbox Implemented

## Visão Geral

**Genaja** é uma aplicação desktop para automação de ETL (Extração, Transformação e Carga) entre planilhas (ex: Simplesweb -> SAP). Utiliza a engine interna **JGDA**.
Esta versão (`v0.3.1`) marca o congelamento da base de código Python reorganizada, servindo como ponto estável para futuras features e eventual migração para Java.

## Estrutura do Projeto

```
Genaja/JGDA/
├── src/                  # Código-fonte (main.py)
├── logs/                 # Arquivos de log (genaja.log)
├── backups/              # Versões legadas (ScriptsGe/Pre-Genaja)
├── docs/                 # Documentação técnica e Roadmap
├── CHANGELOG.md          # Histórico de versões
└── README.md             # Este arquivo
```

## Roadmap e Progresso

- [x] **1/8** - Congelar base legado (v0.3.0).
- [x] **2/8** - Organizar estrutura de pastas e atualizar versão (v0.3.1).
- [x] **3/8** - Validar execução na nova estrutura (Testes de Fumaça).
- [x] **4/8** - Limpeza final para GitHub.
- [x] **5/8** - Publicação no GitHub (Preparação .gitignore concluída).
- [x] **6/8** - Feature: Checkbox "Manter apenas colunas selecionadas".
- [ ] **7/8** - Validação da Feature.
- [ ] **8/8** - Planejamento de Modularização Avançada.

## Como Executar

1. Certifique-se de ter Python 3.x e as libs instaladas:
   ```bash
   pip install pandas openpyxl
   ```
2. Navegue até a pasta raiz `Genaja/JGDA`.
3. Para rodar a aplicação:
   ```bash
   python src/main.py
   ```
4. Para rodar o teste de validação:
   ```bash
   python smoke_test.py   # Executa teste e gera backup automático se sucesso
   ```

## Notas de Versão (v0.3.5)
- Inclusão de `.gitignore` para ignorar `backups/`, `logs/` e arquivos de config locais.
- Projeto pronto para `git init`.
- Implementação da lógica de limpeza de colunas no arquivo final (Checkbox na UI).
- Correção de bugs críticos de seleção de colunas.
- Refatoração de nomes para Inglês Técnico.
- Separação física entre código (`src`) e artefatos.