## [0.7.0] - 02/04/2026 (Universal Connector Strategy)
- **Universal Connector Foundation**: Implementação do `BaseConnector` e desacoplamento do motor ETL.
- **SQL Database Connector**: Suporte nativo a SQLAlchemy 2.0 com streaming de dados (Memory-Safe).
- **Registry Pattern Factory**: Refatoração da `ConnectorFactory` para registro dinâmico de novos adaptadores.
- **Wizard UI SQL Sprint**: Novo Passo 1 com seletor de origem, descoberta de schema/tabela e preview seguro.
- **Arquitetura v0.7 Patch**: Consolidação da inteligência de arquitetura no diretório `.agent/`.

## [0.6.9-Master] - 27/03/2026 (Master Curated Strategy)
- **Master Curated Layer**: Introdução do `CuratedStore` para persistência de 'Regras de Ouro' (Nível 0).
- **Priority Orchestration**: Reformulação do motor de sugestão (Curated > MegaBrain > History > Fuzzy).
- **Auto-Promotion Logic**: O `brain_feed.py` agora promove automaticamente mapeamentos maduros (Score >= 20).
- **Master Rules Persistence**: Nova base determinística em `learn/curated/master_rules.json`.

## [0.6.8-Master] - 27/03/2026 (Master Agent Execution Protocol)
- **Master Agent Protocol**: Implementação do protocolo de saneamento profundo e orquestração de aprendizado.
- **Probabilistic Brain v2**: Sistema de pesos dinâmicos e classificação de estados (OBSERVED a CONFIRMED).
- **Brain Inbox (Sanitation Pipeline)**: Criação do fluxo `learn/inbox` para ingestão segura de datasets externos.
- **Pollution Filter**: Mecanismo de quarentena automática para padrões de mapeamento genéricos ou suspeitos.
- **Automation Toolkit**: Lançamento do `brain_feed.py` (Orquestrador) e `sanitation_hook.py` (Limpador).

## [0.6.7-Ultimate] - 27/03/2026 (Marathon Analysis Release)
- **Big Data Marathon Phase 2**: Consolidação massiva de **1.001.675 associações** aprendidas.
- **Brain Migration**: Centralização do "Cérebro" do Genaja na pasta visível `learn/` do repositório.
- **Statistical Mapping Inference**: Motor de inferência refinado com densidade de 315 colunas primárias.
- **Performance de Elite**: Execução de 1 milhão de ciclos estocásticos em 74 segundos.
- **Governança Unificada**: Sincronização completa de tags `v0.6.5`, `v0.6.6` e `v0.6.7` com auditoria final.

## [0.6.6] - 27/03/2026 (Multi-Sheet Processing)
- **Multi-Sheet Loader**: Suporte nativo para leitura de todas as abas de Workbooks Excel (`sheet_name=None`).
- **Sheet Intelligence**: Detecção automática de cabeçalhos e tipos por aba individual.
- **UI Sheet Selection**: Integração de dropdowns dinâmicos na Step 1 para alternância de abas ativas.
- **Aprendizado por Aba**: Metadados estruturais agora incluem o contexto da planilha de origem.

## [0.6.5] - 27/03/2026 (Profiling Engine)
- **Data Profiling Layer**: Implementação de motor de análise de conteúdo (`dtype`, `unique_ratio`, `avg_len`).
- **Deep Suggestion**: Priorização de sugestões baseada no perfil do dado quando o nome da coluna diverge.
- **Redução de Falsos Positivos**: Filtragem inteligente de colunas técnicas ruidosas via heurística estatística.
- **Performance**: Algoritmo de profiling otimizado para execuções O(n) em datasets corporativos.

## [0.6.4] - 26/03/2026 (Evolution Memory Release)
- **Evolution Memory Layer**: Introdução de persistência local de aprendizado.
- **Learning Store**: Armazenamento seguro de metadados em `learning_log.json`.
- **Signature Matching**: Identificação de contextos via assinaturas de colunas.
- **Usage Tracking**: Priorização de sugestões por frequência de uso.
- **I.A. Local**: Sugestões inteligentes baseadas em execuções passadas.

## [0.6.3] - 26/03/2026 (Data Intelligence Layer)
- **Engines Core**: Implementação de `ValidationEngine`, `LookupEngine` e `SchemaMapper`.
- **Inteligência de UI**: Criação do `FileIntelligenceDialog` e `CompatibilityDialog`.
- **Fuzzy Mapping**: Suporte a similaridade editorial (Levenshtein).

## [0.6.2] - 26/03/2026 (Cleanup)
- **Purga de Legado**: Remoção definitiva do diretório `src/legacy/ui_qt/`.
- **Theme Optimization**: Purgado `get_qss()` do `ThemeService`.
- **Reorganização**: Criação de `/scripts/tools/` para utilitários de desenvolvimento.
- **QA Archive**: Arquivamento de testes de paridade obsoletos em `/tests/archive/`.
- **Documentação**: Baseline de Engenharia atualizada para stack Flet Stateless.

## [0.6.1] - 26/03/2026 (Alfa v2)
- **Congelamento Arquitetural**: Estabilização final da ponte dinâmica de temas.
- **Auditoria de Release**: Limpeza de resíduos de desenvolvimento e documentos privados.
- **Governança**: Padronização de metadados e versionamento rigoroso.
- **UX**: Refino de contraste e reatividade no Platinum Shell.

## [0.6.0] - 25/03/2026 (Alpha Platinum - Flet Migration & v0.4.x Parity)
- **Flet Migration**: Arquitetura 100% Flet (v0.82.2+) com Router Lifecycle-Safe.
- **Paridade v0.4.6/0.4.7**: Restauração do Dual-List Transfer, Regras de Linha e Regras Estruturais.
- **Motor v0.4.8**: Integração de `ValidationEngine` e Filtro Numérico robusto.
- **Módulo Comparador**: Restauração do modo de comparação pura (origem vs destino).
- **Export Multi-Formato**: Suporte a Excel, CSV, JSON e SQL integrado.
- **UI UX**: Tooltips v0.4.7 e Estabilização visual Platinum.

## [0.5.9] - 2026-03-24 (Governance & History Synchronization)
- **Histórico Consolidado**: Reconstrução completa da trilha de auditoria v0.5.x e v0.4.x no README (PT/EN).
- **Audit Build**: Sincronização de metadados e certificação de pre-commit hooks.
- **Paridade Documental**: Alinhamento das notas de release em ambos os idiomas.

## [0.5.8] - 2026-03-24 (Professional Settings Suite)
- **Settings HUD 2026**: Nova interface de configurações globais com navegação lateral (Sidebar).
- **Config Engine v2.0**: Refatoração do `ConfigService` com suporte a Schema e Defaults.
- **Controle de Motor**: Toggles para Auto-Trim, Auto-Upper e Case-Sensitivity.

## [0.5.6] - 24/03/2026 (Premium Customizer 2026)
- **Phoenix Customizer 2.0**: Redesign estilo SaaS Pro com abas e Preview em tempo real.
- **User-Friendly Naming**: Nomes amigáveis para ajustes de cores.

## [v0.5.5] - 24/03/2026 (Pure Qt Architecture Stabilization)
- **Refino v0.5.4**: Estabilização pós-purge do Tkinter.

## [v0.5.4] - 24/03/2026 (Pure Qt Transition)
- **Decomissionamento Tkinter**: Remoção total da pasta `ui_tk`.
- **Pure Entrypoint**: `main.py` agora é 100% PySide6.

## [v0.5.3] - 24/03/2026 (Modern UI & Premium Design)
- **Custom Title Bar**: Barra integrada ao tema estilo Slack.
- **Frameless Architecture**: Experiência visual imersiva.

## [v0.5.2] - 24/03/2026 (Engine Stability Patch)
- **Mapping Fixes**: Correções heurísticas no motor de sugestão de chaves.

## [v0.5.1] - 24/03/2026 (Startup Bugfix & Governance)
- **White Window Fix**: Correção de inicialização dupla de janela.

## [v0.5.0] - 23/03/2026 (The Next Frontier - Gold Release)
- **Hybrid Infrastructure**: Implementação de arquitetura dual (PySide6/Tkinter).
- **Enterprise Engines**: Desacoplamento da lógica ETL da camada Visual.

## [0.4.9] - 20/03/2026 (The Phoenix Absolute Edition)
- **Live Theme Customizer**: Edição visual de temas em tempo real.

## [0.4.7] - 18/03/2026 (The Premium Update)
- **Premium UX**: Tooltips flutuantes e Global Canvas Scroll.
- **Big Data Experimental**: Suporte bruto a JSON/SQL.

## [0.4.3] - 15/03/2026 (Docs & i18n)
- **Bilingual Focus**: Sincronização completa de manuais em Inglês e Português.
- **Doc Layering**: Divisão em Manual do Analista vs Guia do Dev.