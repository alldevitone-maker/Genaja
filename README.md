# Genaja: Java Generic Data Access (JGDA)

> **Versão Atual:** `v0.4.2` (Comparador Pro & Hub de Módulos)  
> **Status do Roadmap:** [Ativo] - Pro UI & Advanced ETL Features

## Visão Geral

**Genaja** é uma aplicação desktop para automação de ETL (Extração, Transformação e Carga) entre planilhas (ex: Simplesweb -> SAP). Utiliza a engine interna **JGDA**.
Esta versão marca a conclusão do primeiro ciclo de desenvolvimento, com uma base de código estável, features funcionais e um fluxo de trabalho automatizado para futuras releases.

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
- [x] **7/8** - Validação da Feature.
- [x] **8/8** - Automação de Release e Melhoria de Backup.

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

## Notas de Versão (v0.4.0)
- **Pro UI Mapeamento Dinâmico:** Seleção de colunas com Listboxes interativas (Disponíveis vs Selecionadas) em substituição à digitação manual.
- **Proteção Absoluta de Chaves:** Caixas de chaves primárias agora são *Read-Only* e populadas automaticamente.
- **Auto-Anchoring de Interface:** Geometria da tela recalculada e layouts empacotados com ancoragem absoluta.
- **Divisão Lógica Passo 3:** Separação visual clara em "Regras de Linhas" e "Regras de Estrutura Estruturais".
- **Exclusão Avançada por Lógica Booleana:** A engine ETL cruza o teste com uma matriz *OR*, deletando linhas inválidas.