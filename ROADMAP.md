# 🛣️ Genaja Roadmap (PT-BR / ENG)

## 📌 Status Atual: v0.4.7
Foco estabelecido em **Robustez, UI Premium Responsiva e Exportação Multi-formato (CSV/SQL/JSON)**.

---

## ✔️ Realizado / Done (Até 0.4.7)
- **Restauro do Módulo Iterativo**: O HUD suporta dois módulos integrados ("ETL de Limpeza" e "Comparador de GAPS/Auditor") na mesma tela.
- **Cruzamento Semântico I.A**: Placar O(1) de sugestão nativa das três chaves primárias ideais por varredura de dados `head(10000)`.
- **Global Tooltips & Toggles**: Dicas customizadas escuras em hover com master switch global liga/desliga.
- **Dynamic Responsiveness (Canvas Scroll)**: Infraestrutura adaptada para rodar uniformemente em laptops < 900px sem cortar a altura.
- **Exportadores O(1) Experimentais**: Lançada exportações em `.csv`, `.json` e `.sql`.
- **Reinício Automático Nativo**: Reinício via chamada ao SO da própria interface gráfica (OS Reboot).

---

## 🚀 Próximos Passos (v0.5.0 - The Logic Rewrite Pipeline)
### 🇧🇷 Brasileiro
- [ ] **Desacoplamento Completo Backend-Frontend**: Separar 100% da inteligência da GUI pro `etl_service`.
- [ ] **Módulo O(1) Definitivo**: Retirar o selo experimental do `SQL` e `CSV` ao aprofundar os testes com bases contendo +5 Milhões de Linhas.
- [ ] **Dark Mode Nativo Exato**: Trocar ou implementar um Theme-Switcher completo (Toggle de Interface Clara/Escura).
- [ ] **Histórico de Logs**: Criação de `log.txt` na pasta para registro de todos os carregamentos e limpezas automáticas aplicadas pelo sistema.

### 🇺🇸 English
- [ ] **Full Frontend-Backend Decoupling**: Completely abstract away all dataframe modifications into `etl_service`.
- [ ] **Definitive O(1) Exporter Module**: Remove the "Experimental" tags from `CSV` and `SQL` generators by running +5 Million Rows edge-case scaling benchmarks.
- [ ] **Native Dark Mode Toggler**: Implement an interactive, real-time Theme-Switcher between Light and Premium Dark.
- [ ] **Log Exporting Engine**: Compile history inside a local `log.txt` noting every cleanup rule applied by the I.A and output size differences.
