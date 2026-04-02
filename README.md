# Genaja — ETL e Sincronização de Dados

[🇺🇸 View in English](README.en.md) | [🇧🇷 Visualizar em Português](README.md)

> **Versão Atual:** `v0.7.0` (Universal Connector Strategy)
> **Status:** Estável — Python / Flet / SQLAlchemy

---

## Sobre o Projeto

Genaja é uma ferramenta de integração e sincronização de dados desenvolvida em Python com interface Flet.
Destinada a analistas corporativos, permite mapear, transformar e exportar dados entre planilhas Excel e bancos relacionais sem escrita de código.

O motor ETL é completamente desacoplado da interface. A UI opera via `WizardState` → `ConnectorFactory` → adaptadores, garantindo que o ETLEngine receba apenas DataFrames, independente da fonte original.

---

## Capacidades

- Mapeamento de colunas com similaridade Levenshtein (fuzzy matching)
- Detecção automática de chaves primárias por entropia (ID, SKU, CPF, CNPJ)
- Sugestões baseadas em histórico de execuções anteriores (local, offline)
- Suporte a planilhas Excel com múltiplas abas (workbook completo)
- Profiling estatístico para redução de falsos positivos no mapeamento
- Conexão com bancos relacionais via SQLAlchemy 2.0 (PostgreSQL, MySQL, SQLite)
- Exportação para Excel, CSV, JSON e SQL
- Interface Wizard de 4 passos com preview em tempo real

---

## Governança e Pipeline de Release

```bash
# Validação rápida antes de qualquer commit
python scripts/automate.py --quick

# Release completo: versão + changelog + backup + push
python scripts/automate.py --release --push
```

O pipeline executa:
1. Sincronia de versão — `version.py` ↔ `README` ↔ `CHANGELOG` (PT/EN)
2. Smoke Test — importação e inicialização dos módulos críticos
3. Auditoria de arquivos — naming conventions e detecção de temporários
4. Backup automático — snapshot ZIP versionado em `backups/`
5. Git commit e push — executado apenas após validação verde

> **Pre-commit hook ativo:** commits são bloqueados se a validação falhar.

---

## Histórico de Versões

### v0.7.0 — Conectores Universais (02/04/2026)

Introdução da camada de conectores extensíveis via Registry Pattern.

- `DatabaseConnector`: suporte a PostgreSQL, MySQL, SQLite via SQLAlchemy 2.0
- `ConnectorFactory`: registro dinâmico de adaptadores sem acoplamento à UI
- Wizard Step 1: seletor de fonte (arquivo local vs banco SQL) com descoberta de schema
- Preview limitado a 100 linhas na etapa de seleção (proteção de memória)
- Credenciais efêmeras: senha nunca persistida em estado serializado ou logs

### v0.6.9-Master — Curadoria Determinística (27/03/2026)

- `CuratedStore`: camada de regras com prioridade absoluta sobre sugestões probabilísticas
- Auto-promoção de mapeamentos com score >= 20 para regras permanentes

### v0.6.8-Master — Agent Protocol (27/03/2026)

- Pipeline de ingestão segura via `learn/inbox/`
- Script de saneamento automático do repositório (`sanitation_hook.py`)

### v0.6.7 — Marathon Analysis (27/03/2026)

- Consolidação de 1.001.675 associações aprendidas com pesos estatísticos
- Migração do histórico de aprendizado para `learn/` (visível no repositório)

### v0.6.6 — Multi-Sheet Support (27/03/2026)

- Leitura de workbooks Excel completos (`sheet_name=None`)
- Seleção dinâmica de abas na interface Step 1

### v0.6.5 — Profiling Engine (27/03/2026)

- Análise estatística de `dtype`, `unique_ratio` e `avg_len` por coluna
- Filtragem de colunas ruidosas antes da sugestão de mapeamento

### v0.6.4 — Evolution Memory (26/03/2026)

- Persistência local de histórico de mapeamentos em `learning_log.json`
- Identificação de contextos via assinaturas de coluna (MD5)

### v0.6.3 — Data Intelligence Layer (26/03/2026)

- `ValidationEngine`, `LookupEngine` e `SchemaMapper` implementados
- `FileIntelligenceDialog` e `CompatibilityDialog` na UI
- Fuzzy matching via distância de Levenshtein

### v0.6.2 — Cleanup (26/03/2026)

- Remoção da camada legada `src/legacy/ui_qt/`
- Reorganização de scripts e arquivamento de testes obsoletos

### v0.6.1 — Estabilização Alfa v2 (26/03/2026)

- Migração para `PlatinumTheme`: tokens dinâmicos de cor e contraste
- Cálculo automático de luminância para ajuste de `ThemeMode`
- Auditoria de release: remoção de documentos privados antes da publicação

---

### Versões Anteriores

**v0.6.0** — Migração para Flet (Python Flutter). Paridade funcional com a série v0.4.x. Restauração do Módulo Comparador e Dual-List Transfer.

**v0.5.9** — Sincronização de histórico e hooks de pre-commit.

**v0.5.8** — Painel de configurações globais (Trim/Case, exportação, segurança).

**v0.5.6** — Phoenix Customizer 2.0: editor de temas com preview em tempo real.

**v0.5.5** — Estabilização após remoção do Tkinter.

**v0.5.4** — Remoção definitiva do suporte ao Tkinter. Aplicação Pure PySide6.

**v0.5.3** — Custom Title Bar (estilo VS Code), motor de temas visual.

**v0.5.2** — Correções no motor de mapeamento heurístico.

**v0.5.1** — Correção de bug de inicialização dupla de janela.

**v0.5.0** — Arquitetura híbrida PySide6/Tkinter, Wizard de 4 passos, dashboard em tempo real.

**v0.4.9** — Live Theme Customizer.

**v0.4.7** — Tooltips flutuantes, scroll global, suporte experimental a Big Data (JSON, CSV, SQL).

**v0.4.6** — Hub único com Chave A1 Protegida via checkbox.

**v0.4.3** — Documentação em dupla camada (Analista / TI) com paridade bilíngue.

**v0.4.0** — Filtro cruzado inteligente e seleções de transferência nativas.

**v0.3.5** — Refatoração completa para arquitetura desacoplada.

---

*Documentação técnica detalhada disponível em `docs/`.*
