# Genaja Suite — Inteligência Analítica e Sincronização de Dados

[🇺🇸 View in English](README.en.md) | [🇧🇷 Visualizar em Português](README.md)

> **Versão Atual:** `v0.6.9-Master` (Master Curated Strategy)
> **Status do Projeto:** Estável - Camada de Curadoria Determinística ⭐

---

## 🚀 Genaja Suite — A Revolução da Inteligência de Dados

**Genaja Suite** evoluiu de uma ferramenta ETL para uma plataforma de **Data Learning** projetada para analistas corporativos que buscam automação inteligente sem código. Através de sua nova **Evolution Memory Layer**, o sistema aprende com cada mapeamento, transformando execuções passadas em conhecimento vivo para o futuro.

Seu motor **JGDA Engine** entrega:
- 🚀 **Memória Evolutiva Local** — Reconhecimento de contextos e mapeamentos históricos (Zero Cloud/Offline)
- 📊 **Ultimate Marathon (v0.6.7)** — Base de conhecimento consolidada com **1.000.000+ ciclos** de aprendizado
- 🏛️ **Knowledge Brain** — Repositório visível de aprendizado na pasta `learn/` do projeto
- 📑 **Multi-Sheet Support (v0.6.6)** — Processamento completo de Workbooks Excel com seleção dinâmica de abas
- 🔍 **Data Profiling (v0.6.5)** — Análise estatística de conteúdo para redução de falsos positivos
- 🔑 **Detecção de Chaves Primárias** — Identificação automática via entropia (ID, SKU, CPF, CNPJ...)
- 🔗 **Mapeamento via Fuzzy Logic** — Heurísticas de similaridade editorial Levenshtein (AI Estrutural)
- 🛡️ **Safe-Merge com Shielding** — Evita duplicatas, fantasmas e cruzamentos errôneos
- 📦 **Exportação Multi-Formato Native** — Excel, CSV, JSON, SQL (Motor High-Performance O(1))
- 🎨 **UI Platinum 2026** — Interface Frameless, Custom TitleBar e Live Theme Studio

---

## 🛡️ Governança & Pipeline de Release

Todo commit e release passam por um pipeline automatizado de validação:

```bash
# Validação rápida (antes de qualquer commit)
python scripts/automate.py --quick

# Release completo (interativo: versão + changelog + backup + push)
python scripts/automate.py --release --push
```

O pipeline executa automaticamente:
1. ✅ **Sincronia de versão** — `version.py` ↔ `README` ↔ `CHANGELOG` em paridade PT/EN
2. ✅ **Smoke Test** — valida inicialização dos widgets críticos
3. ✅ **Auditoria de arquivos** — naming conventions + detecção de lixo
4. ✅ **Backup automático** — snapshot ZIP versionado em `backups/`
5. ✅ **Git commit & push** — executado apenas após validação 100% verde

> ⚠️ **Pre-commit hook ativo**: commits são bloqueados automaticamente se a validação falhar.

---

## 📖 Histórico de Atualizações (Audit Trail 2026)

<div id="latest-release">

### **v0.6.9-Master (Master Curated Strategy)**
**Decisão Absoluta.** Camada de Curadoria Mestre (Prioridade 0).
- ⭐ **Master Rules**: Regras determinísticas em `learn/curated/master_rules.json`.
- 📊 **Auto-Promotion**: Promoção automática de mapeamentos com Score >= 20.

### **v0.6.8-Master (Master Agent Protocol)**
**Orquestração e Saneamento.** Protocolo de limpeza e estruturação do cérebro.
- 🧹 **Sanitation Hook**: Script de limpeza automática do repositório.
- 🍱 **Brain Inbox**: Fluxo de ingestão segura de dados via `learn/inbox/`.

### **v0.6.7 (Marathon Analysis Release - ULTIMATE)**
**O cérebro definitivo.** Consolidação de 1 milhão de simulações e integração de dados legados do BigData.
- 🏃 **Ultimate Marathon**: 1.001.675 associações aprendidas com pesos estatísticos.
- 🏛️ **Brain Consolidation**: Migração do cérebro técnico para a pasta visível `learn/`.
- 📈 **Statistical Inference**: Sugestões ultra-precisas com densidade de 315 colunas primárias.

### **v0.6.6 (Multi-Sheet Release)**
**O fim da limitação de aba única.** O Genaja agora entende arquivos Excel como entidades completas.
- 📑 **Multi-Sheet Loader**: Leitura simultânea de todas as abas (`sheet_name=None`).
- 🔘 **Tab Selector UI**: Dropdowns para seleção de origem/destino na interface Step 1.

### **v0.6.5 (Profiling Release)**
**O motor de análise profunda.** Redução drástica de falsos positivos no mapeamento.
- 🔍 **Data Profiling**: Análise de `dtype`, unicidade e comprimento médio dos dados.
- 🛡️ **Noise Reduction**: Filtragem de colunas técnicas ruidosas baseada em perfil estatístico.

### **v0.6.4 (Evolution Memory Release)**
**O sistema que aprende.** Introdução da Camada de Memória Evolutiva que automatiza o mapeamento baseado no histórico de uso real do analista.
- 🧠 **Learning Store**: Registro seguro e atômico de metadados estruturais em `learning_log.json`.
- 🏷️ **Signature Matching**: Identificação instantânea de colunas recorrentes via assinaturas de contexto (MD5).
- 📈 **Usage Tracking**: Priorização inteligente de sugestões baseada na frequência de execuções anteriores.

### **v0.6.3 (Data Intelligence Layer)**
**A inteligência local.** Implementação dos motores de auditoria e mapeamento avançado.
- 🔍 **Schema Mapping Fuzzy**: Motor de similaridade Levenshtein para sugerir colunas com nomes aproximados.
- 🤖 **Data Assistance**: Novos diálogos de interceptação e compatibilidade assistida (`CompatibilityDialog`).
- 🛡️ **Hardening v0.6.x**: Correções de estabilidade de UI e segurança de overlay no Flet.

---

### **v0.6.2 (Cleanup)**

---

### **v0.6.1 (Alfa v2)**
**O Marco de Estabilização.** Esta versão consolidou a transição para a nova arquitetura reativa, eliminando bugs de contraste e garantindo governança absoluta do repositório.
- 🎨 **Estabilização de Temas**: Migração para a ponte dinâmica `PlatinumTheme`, garantindo legibilidade perfeita no tema Light.
- 🌓 **Reatividade Inteligente**: Cálculo automático de luminância para ajuste nativo do `ThemeMode` (SO Context).
- 🧼 **Auditoria de Release**: Purga de resíduos técnicos e documentos privados para publicação pública segura.
- ⚖️ **Governança 2026**: Sincronia rigorosa de metadados entre UI, Version e Docs.

> [!TIP]
> **Download do Client:** [Link indisponível nesta fase de Alpha] <!-- Futuro link aqui -->

</div>

---

**v0.6.0 (Alpha Platinum - Flet Migration)**
Transição tecnológica massiva trocando o motor gráfico PySide6 por **Flet (Pure Python Flutter)**, mantendo paridade funcional com a série v0.4.x. Restauração do Módulo Comparador e Dual-List Transfer.

**v0.5.9 (Governance & History Synchronization)**
Versão de auditoria focada na integridade do histórico do projeto. Sincronizamos todos os marcos da série v0.5.x nas documentações bilíngues e certificamos o funcionamento dos hooks de pre-commit.

**v0.5.8 (Professional Settings Suite)**
Unificamos o controle do Genaja. O novo painel de **Global Preferences** permite gerenciar desde o comportamento do motor de dados (Trim/Case) até detalhes de exportação e segurança, tudo em uma interface Sidebar style com acabamento 2026 High-Fidelity.

**v0.5.6 (Premium Customizer 2026)**
Atingimos o estado da arte em customização UI. O novo **Phoenix Customizer 2.0** traz uma interface categorizada com Preview em tempo real, permitindo ajustes finos com nomes amigáveis. A engine QSS v2.2 oferece acabamento premium (16px radius).

**v0.5.5 (Pure Qt Architecture Stabilization)**
Marco de estabilização obrigatório. Validamos a integridade do sistema após o "Purge" do Tkinter, garantindo uma build limpa e performática para a nova stack PySide6.

**v0.5.4 (Pure Qt Transition)**
A consolidação da arquitetura moderna. Removemos definitivamente o suporte ao Tkinter (Legado) e o argumento `--ui`, tornando o Genaja uma aplicação Pure PySide6. Redução massiva de dívida técnica.

**v0.5.3 (Modern UI & Premium Design)**
A revolução estética. Implementamos a **Custom Title Bar** (estilo VS Code), removendo as decorações nativas do Windows para uma experiência imersiva e frameless, além do novo motor de temas visual.

**v0.5.2 (Engine Stability Patch)**
Ajustes finos no motor de mapeamento heurístico e correção de pequenos glitches visuais na barra de título em modo maximizado.

**v0.5.1 (Bugfix de Inicialização & Governança)**
Post-Gold stage focado em estabilidade. Corrigimos o bug de inicialização dupla de janela e sincronizamos os primeiros protocolos de governança para o ciclo v0.5.x.

**v0.5.0 (The Next Frontier - Gold Release)**
A maior evolução tecnológica do Genaja. Implementamos uma arquitetura híbrida completa (PySide6/Tkinter) com motores enterprise desacoplados, interface Wizard de 4 passos, dashboard de monitoramento em tempo real e o estúdio de temas Phoenix Qt.

**v0.4.9 (The Phoenix Absolute Edition)**
Introdução do **Live Theme Customizer**. Controle absoluto de cores e estilos via interface gráfica em tempo real para Tkinter/PySide6.

**v0.4.7 (The Premium Update & Big Data O(1))**
A interface corporativa alcançou o nível Premium. O sistema agora conta com um motor de **Tooltips Flutuantes** (Dicas visuais) detalhando funções complexas de negócio. Toda a tela recebeu um **Global Canvas Scroll**. Introduzimos os quadros "Experimentais" vermelhos com suporte a Big Data (`JSON`, `CSV`, `SQL`).

**v0.4.6 (Unified Hub Flex)**
Refatoração de arquitetura reunindo o Genaja em uma super-tela (Hub Único) sem perder funcionalidades clássicas. O botão de **Chave A1 Protegida** tornou-se ativável por Checkbox.

**v0.4.3 (Experiência do Usuário & Docs)**
A "vitrine" do aplicativo foi reformulada. Adicionada a estruturação em dupla camada (Manual do Analista e Documentação Técnica de TI) com paridade bilíngue.

**v0.4.0 (A Era do Auto-Clique)**
Retirada manual das caixas de anotação na ferramenta para seleções de transferência nativas e inteligentes na tela. Inserido o filtro cruzado inteligente.

**v0.3.5 (Core Clean Architecture)**
O marco zero da nova era. Refatoração completa para arquitetura desacoplada e foco em performance de processamento de dados.

---
*(A documentação de arquitetura detalhada para analistas e TI localiza-se na pasta isolada `docs/`)*
