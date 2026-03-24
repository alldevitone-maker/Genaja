# Changelog

## [v0.5.3] - 24/03/2026 (Modern UI & Premium Design)
- **Custom Title Bar**: Substituição da barra nativa do Windows por uma barra integrada ao tema (estilo VS Code/Slack).
- **Frameless Architecture**: Janela limpa, integrada e 100% controlada pelo motor gráfico do Genaja.
- **Theme Engine 2.0**: Introdução de **Presets Oficiais** (Zinc Studio, Phoenix Dark, Light Grey SaaS).
- **Phoenix Customizer 2.0**: HUD redesenhado com agrupamento visual, seletores de cores amigáveis e live preview aprimorado.
- **Desacoplamento Visual**: `MainWindow` agora é visualmente cega, consumindo 100% da identidade via tokens do `ThemeService`.
- **Governança v0.5.3**: Pipeline de validação atualizada para certificar a nova arquitetura frameless.

## [v0.5.1] - 24/03/2026 (The Next Frontier - v0.5.1 Bugfix)
- **Correção de Janela Branca**: Ajuste técnico na inicialização do Tkinter para evitar instanciamento duplo do Root.
- **Sincronização de Metadados**: Padronização global das etiquetas de versão em conformidade com o Protocolo de Governança.
- **Estabilização de Bootstrap**: Refinamento na lógica de seleção de UI (Qt como default).

## [v0.5.0] - 24/03/2026 (The Next Frontier - Gold Release)
- **Arquitetura Híbrida Real**: Migração completa para um ambiente dual PySide6 e Tkinter com motores desacoplados.
- **v0.5.0 Wizard (Qt)**: Implementação de fluxo de 4 passos funcional com injeção de serviços enterprise.
- **Phoenix Qt (Design System)**: Motor de temas dinâmico QSS com editor flutuante e live preview no PySide6.
- **Status Dashboard Area**: Novo módulo de monitoramento em tempo real com barra de progresso e log de auditoria.
- **Micro-Animações**: Transições de opacidade cinematográficas no Wizard para uma experiência de usuário premium.
- **Coração Service-Oriented (SOA)**: Lógica de negócio isolada em `core/services`, garantindo 100% de paridade entre frontends.
- **Governance Safe-Check**: Integração de fumaça (smoke tests) para ambas as interfaces no pipeline de release.

## [v0.4.9] - 24/03/2026 (The Phoenix Absolute Edition)
- **Phoenix Customizer**: Introdução de editor de temas em tempo real via Janela Flutuante (Toplevel).
- **Controle de Tema Absoluto**: Reatividade total (100%) para bordas, fundos, telas e botões.
- **Arquitetura Zero-XP**: Reconstrução dos botões nativos em Flat Design puro com motor de hover dinâmico.
- **Precisão Hexadecimal**: Suporte a entrada direta de códigos de cor com sincronização instantânea.
- **Menu Bar Institucional**: Acesso formal às configurações via barra de menu "Settings" no topo da janela.
- **Estética Vibrant Hybrid**: Equilíbrio entre a arquitetura flat moderna e a paleta de alto contraste v0.4.8.
- **Transparência I.A**: Melhoria no feedback visual do scanner léxico (ícones de status e alertas).

## [v0.4.8] - 24/03/2026 (The Architectural Refactoring & Governance Update)
- **Refatoração Arquitetural**: Modularização do `etl_service.py` em motores especializados (`mapping_engine.py`, `validation_engine.py`).
- **Governança Ativa**: Implementação de Git Hooks (pre-commit) para validação automática de versão e testes.
- **Orquestrador Unificado**: Criação do `automate.py` integrando validação, backup, e release interativa.
- **Limpeza de Legado**: Remoção de scripts obsoletos (`reset_structure.py`, `release.py`, `gerar_massa_teste.py`).
- **Organização de Dados**: Movimentação de arquivos de teste para a pasta `data/`.
- **Log Histórico**: Implementação de sistema de logs persistentes em `logs/genaja.log`.
- **Dependências**: Criação do `requirements.txt` para padronização do ambiente.

## [v0.4.7] - 24/03/2026 (The Premium Update & Big Data O(1))
- **Interface Premium:** Implementado motor de Tooltips Flutuantes e Global Canvas Scroll para telas menores.
- **Big Data Experimental:** Suporte a exportações brutas em JSON, CSV e SQL.
- **Segurança de Dados:** Refatoração do motor de junção (Safe-Merge) contra corrupção de nomes duplicados.
- **Gestão de Memória:** Botão de Reiniciar App nativo para limpeza imediata de RAM.

## [v0.4.6] - 23/03/2026 (Genaja Wizard & IA API)
- Nova interface baseada em Wizard (1, 2, 3) com navegacao superprotegida.
- Inteligencia Nativa que sugere Chaves lendo planilhas de forma semantica.
- Motor de Exportacao liberado para gerar CSV ou codigos remotos SQL Insert.

## [v0.4.5] - 23/03/2026 (Arquitetura de Pastas Enterprise)
- Pastas raiz purificadas. Scripts de automacao (CI) e Qualidade foram isolados (scripts/ e tests/).
- Exclusao de arquivos mortos e scripts legados de prototipagem.

[🇺🇸 English](CHANGELOG.en.md) | [🇧🇷 Português](CHANGELOG.md)

## [v0.4.4] - 23/03/2026 (Internationalization & i18n)
- **Globalização:** Introduzido suporte multi-idiomas nas documentações (`.en.md`) e cross-links navegáveis para expansão e contribuição open-source mundial.

## [v0.4.2] - 23/03/2026 (Comparador Pro & Hub de Módulos)
- **Transformação** do Passo 3 em um Hub de Módulos expansível, permitindo navegar entre telas em um clique.
- **Novo Módulo Comparador** para cruzar e encontrar registros faltantes entre dois mundos diferentes sem precisar gastar horas em Excel.
- **Libertação de Nomenclaturas:** Tchau Sap e Simplesweb, de agora em diante tudo suporta conexões genéricas e chamadas flexíveis para Origem e Destino com foco em Integrações Absolutas.
- **Cabeçalho Inteligente** reconstruiu sua IA, varrendo relatórios complexos com decorações inúteis de títulos e agrupamentos no topo focando e identificando a tabela original instantaneamente.

## [v0.4.1] - 23/03/2026 (Ajustes e Estabilidade Numérica)
- **Blindagem de Textos Frios** garantindo que células preenchidas majoritariamente com Zeros nas bases do cliente não sumissem na eliminação diária de vazios sem querer (Segurança à Códigos Descritivos e de Produto).
- **Polimentos Reativos** impedindo colapsos de acentos nos logs exportados.

## [v0.4.0] - 20/03/2026 (Patch Pro UX & Advanced ETL)
- **Reestruturação Interativa** aposentando as chaves digitadas de colunas para cliques com ListBoxes bidirecionais de Mapeamentos. A ferramenta te avisa com o nome exato.
- **Combos Protegidos:** Proteções das chaves principais engatilhou a defesa Absoluta as travando como Read-Only da hora que localizadas em diante.
- **Cruzado Booleano Inteligente:** Regras generalizadas de remoção checam multiplas colunas, limpando em condicional OR para exclusões se e somente se cruzar total ausência de informações na matriz completa.

## [v0.3.9] - 20/03/2026 (Dark Mode Padrão & Inception Smart Headers)
- **Elegância Embutida:** Tema corporativo noturno assumido como Standard visual.
- **Radares ativados:** Em relatórios brutos que vieram faltando uma informação em algumas colunas o sistema preenche as vazias pra impedir anomalias e encontra dinamicamente de onde a planilha nasceu mesmo ignorando nulos.

## [v0.3.8] - 20/03/2026 (Motor Dinâmico de Captura Externa/Expansão)
- Genaja parou seu fluxo primitivo de apenas retocar colunas com os mesmos nomes e aprendeu com eficiência impressionista a roubar novas colunas das Bases recém adicionadas (A Base Antiga incorpora com a nova se tiver novas colunas adicionais e cruza no momento sem exigir intervenções analíticas prévias).

## [v0.3.7 ao Inicial] - A Fundação Corporativa de Manutenção (CI/CD Automático)
- Separações de Documentos Internos por Sigilo Empresarial (Trato e Compliance nas automações restritas ao cliente vs Repositório).
- Introduzido a varredura e cópias de Backup Transparente onde a ferramenta detecta se as ações na interface terminaram em validade garantindo proteção para se algo no Windows quebrar. 