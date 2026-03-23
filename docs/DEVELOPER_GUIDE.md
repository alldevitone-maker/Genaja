# Genaja Developer & Architecture Guide

[🇺🇸 English](DEVELOPER_GUIDE.en.md) | [🇧🇷 Português](DEVELOPER_GUIDE.md)

Este documento contém o registro avançado da infraestrutura sob o capô do Genaja (JGDA).

## 🏗️ Arquitetura do Software (O Motor JGDA)

A ferramenta foi projetada separando as lógicas pesadas de Banco de Dados da Visualização Gráfica do Usuário (inspirada em MVC).

1. **`ui/genaja_ui.py` (Visão Tátil):** Toda a aplicação roda desenhada por blocos gerenciados pelo pacote embutido `tkinter` com o empacotador de estilização `ttk`. Um `Hub` controla dinamicamente quais Frames devem carregar (`pack(fill=tk.BOTH)` e `pack_forget()`) dependendo de qual "state" ou "modulo ativo" foi engatilhado pelas setas e callbacks.  
2. **`services/etl_service.py` (Controlador ETL):** Trabalha fortemente fundado na vetorização atrelada ao `Pandas`. As exclusões são feitas mediante o instanciamento de matrizes Booleanas simultâneas de comparação paralela bit-wise (`not_zero & valid_str % not_null`) evitando o loop de linha catastrófico (iterating `iterrows()`). 
3. **`services/excel_loader.py` (Leitor Heurístico):** Utiliza técnica de identificação avançada (`isinstance(str)`) correndo as 20 primeiras camadas para localizar "True Headers", contornando o erro nativo do Pandas em ler blocos mesclados (`Unnamed: N`). Extração se baseia na contagem estrita de volume de strings textuais por linha.
4. **`Main.py`**: Desvio e instanciador de classes. Recebe as ordens empacotadas num dicionário da UI (`get_inputs()`) para evitar espaguete de argumentos e desvia o switch/if-else para ramificar a execução dos serviços correspondentes aos módulos instanciados do UI Container.

## CI/CD Workflow Local
Como o projeto não possui Github Actions nativas na nuvem (ainda), o versionamento corre numa esteira manual protegida:
- O Teste unitário cego: Desenvolvedores testam as injeções com o script `smoke_test.py`. Esse código avaliza Imports comutativos, sintaxe não detectável ao salvar em cache e Encoding do SO.
- Ao acenar `sys.exit(0)`, o `make_backup.py` é evocado nos bastidores gerando snapshots físicos baseados no diretório limpo para `backups/v_titulo.zip`
- Lançamento: A criação da release é automatizada rodando `python release.py` interativo no terminal. Esse script fará Regex na Landing Page, varreduras no File Tree injetando `git commit/tag/push` autonomamente impedindo assincronias e quebras na arvore Branch-Tag.

---

## 🛠️ Log de Commits da Engenharia (Technical Version History)

### v0.4.4 - Internationalization & i18n
- **Localization:** Duplicação limpa de `README`, `CHANGELOG` e `DEVELOPER_GUIDE` criados sob extensão paramétrica `.en.md` possuindo Badges dinâmicas injetadas na UI do Github Render.

### v0.4.3 - Refatoração Arquitetônica de Documentação (UX/Docs)
- **Docs:** Bifurcação das linguagens: criação explícita do `DEVELOPER_GUIDE.md` (Neste documento o qual você lê agora), extraído os jargões lógicos puros do `README.md` raiz. O objetivo foi limpar o Changelog para torná-lo um registro de release corporativa, isolando a documentação crua da stack em ambiente contido.

### v0.4.2 - Comparador Pro & Auto-Hub 
- **Refactoring:** Interface `genaja_ui.py` modificada com Views dinâmicas modulares em containers reusáveis `f3_container` possuindo transições de estados de botão com `hasattr`.
- **Feature:** Implementado wrapper `process_data_comparison` dentro do motor Pandas em `etl_service`, resolvendo disparidades inter-dataframe utilizando logica puramente via sets iteráveis: `missing_keys = set(df_src_cmp[key_src]) - set(df_tgt_cmp[key_tgt])` (Anti-Join em C genérico nativo do set CPython para máxima eficiência algorítmica).
- **Bugfix (Heuristic Header Loader):** Alteração radical no `find_best_header()`. Antigamente regrado via "max cols dropna()", gerando falso-positivo se uma linha de dados possuísse mais números informados do que a row mesclada do cabeçalho. Alterado para "sum of `isinstance(string)` cells" somado de verificação de estrutura bottom-header (>= score) para priorizar a linha final de cabeçalho duplo (ex: ignorar sub-titulos sobrejacentes como em relatórios SAP nativos).
- **Refatoração UI API:** SAP/Simplesweb renomeados paramétricamente nos text vars e dicionários `.get()` de `main.py` para agnósticos Origem (`df_origem`) e Destino (`df_destino`).

### v0.4.1 - Fix de Filtragem de ETL & Enconding 
- **Bugfix (Engine):** A rotina responsável por obliterar os lixos iteráveis preenchidos com null (`clean_empty_quantities_multi`), não alocava validação numéricos nativos por ser checado numa array bit array em Strings hardcoded `(s != '0.0')`. Corrigido castando via proxy method `pd.to_numeric()`, avaliando 0 estritos nativos e estendendo proteção para não-intencionais falsos zeros lidos como texto no Excel, preservando `000100` e outras PKs na base.
- **Bugfix (Console):** Resolvidos os encoding prints falhos `cp1252` e emojis travando pipes do Popen/Stdout do `release.py` no Windows, garantindo UTF-8 forçado no process host.

### v0.4.0 - Mapeamento O(1) e Multibox
- **UI Rewrite:** Subtraída a mecânica pesada e perigosa dos Entry Textos onde o User devia colar colunas e implementado o modelo `tk.Listbox` dinâmico atrealado ao payload auto-detectado no `read_excel`. Busca responsiva via binding `trace_add()`.
- **Motor Lógico Expansível:** O filtro de linhas aceitava check rígido 1x1. Através de um loop dinâmico bit a bit ele passou a ser acumulável. O delete da tabela é cruzado por uma matriz Condicional OR.

### v0.3.9 - Inception do Smart Headers
- Criada a funcionalidade pre-wrapper de Auto Detecção. Introduzido o método iterável de 20 rows para calcular `non_nulls > max_non_nulls` expurgando Unnamed nan's corrompidos comuns em exportações web diretas. 
- Inclusão do Theme "VSCode Dark", sobrescrevendo os frames TK.

### v0.3.8 - Sincronização Expandida
- Arquitetura principal (`process_data_synchronization`) reescrita, evoluindo do modelo in-place Update para o Left Join (`.join()`) capturando colunas dinâmicas desdobradas do dataframe 2 para o DF1.

### v0.3.1 à v0.3.7 - Compliance e Transição Py
- Versões em que a estabilidade principal foi isolada dos scripts originais para proteção contra os dados e a engine foi modularizada dos espaguetes legacy criados fora da IDE. Nascimento dos backups com base em títulos SemVer para CI. Conformidade aplicada no ignore e tree map isolado.
