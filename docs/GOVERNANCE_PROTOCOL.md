# 🛡️ PROTOCOLO DE ENGENHARIA E GOVERNANÇA GENAJA (v0.5.3)

Este documento resume como o desenvolvimento do Genaja é blindado contra falhas e como mantemos a paridade entre código, design e documentação.

## 1. 🎛️ Automação e CLI de Liderança
Todo o ciclo de vida é gerido pelo script `scripts/automate.py`. 
- **Modo `--quick`**: Roda apenas validações de consistência (Regex).
- **Modo `--release`**: Executa o fluxo completo:
    - **Validação de Versão**: Garante que `src/version.py` = `CHANGELOG.md` = `README.md`.
    - **Backup Automático**: Gera um ZIP versionado na pasta `backups/`.
    - **Documentação Sync**: Sincroniza labels e títulos entre as versões PT e EN.

## 2. 🛡️ Governança de Código (Git Hooks)
Implementamos um **Git Pre-commit Hook** (.git/hooks/pre-commit) que:
1. Impede o commit se houver divergência de versão.
2. Impede o commit se o **Smoke Test** falhar.
3. Garante que nenhum arquivo "lixo" (tmp, bak, copy of) seja enviado ao repositório.

## 🧪 3. Protocolos de Teste (The Smoke Test)
- **Localização**: `tests/smoke_test.py`.
- **Ação**: Instancia a `GenajaApp`, inicia a interface gráfica (Tkinter) em modo headless/temporário e a fecha após 2 segundos.
- **Objetivo**: Garantir que alterações na UI (como o Phoenix Customizer) não causem erros de inicialização ou conflitos de variáveis de tema.

## 🎨 4. Sistema de Design: Zinc Studio & Phoenix Engine
- **Arquitetura**: Light-Grey Layering (SaaS Style).
- **Theme Engine**: Centralizado no `services/theme_service.py` (`theme.json`).
- **Phoenix Customizer**: Uma janela flutuante (`Toplevel`) que injeta cores em tempo real em todos os widgets através de um motor recursivo de atualização reativa em `genaja_ui.py`.
- **Flat Buttons**: Todos os botões são `tk.Button` customizados com bordas de highlight e estados de hover via código, eliminando o estilo clássico do Windows.

## 📂 5. Documentação Bilíngue (i18n)
Mantemos paridade absoluta:
- `README.md` / `README.en.md`
- `CHANGELOG.md` / `CHANGELOG.en.md`
- `DEVELOPER_GUIDE.md` / `DEVELOPER_GUIDE.en.md`

## 🏁 Fluxo para o Novo Roadmap (v0.5.0)
Para evoluir a UX/UI:
1. **Alterar no Customizer**: Testar cores e contrastes em tempo real.
2. **Commit**: Passar pela barreira de pre-commit.
3. **Release**: Rodar `automate.py --release` para consolidar o estado estável.

**Assinado:** Antigravity AI (Genaja Lead Agent)
