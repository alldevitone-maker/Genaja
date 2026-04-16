# 🛡️ PROTOCOLO DE ENGENHARIA E GOVERNANÇA GENAJA (v0.7.1 Platinum)

Este documento estabelece as diretrizes invioláveis para o desenvolvimento, manutenção e lançamento do ecossistema **Genaja (JGDA)**. Ele garante que qualquer agente (IA ou Humano) mantenha a integridade estrutural do sistema em um release consistente.

## 1. Fonte Única de Verdade (Single Source of Truth)
- **Versão:** Definida EXCLUSIVAMENTE em `src/version.py`. Nenhuma outra string de versão deve ser escrita manualmente no código ou na documentação.
- **Título de Release:** Definido em `src/version.py` (ex: `__title__ = "Stable Governance"`).

## 2. Declaração de Módulos (Metadata Hooks)
- Todo módulo funcional dentro de `src/` deve obrigatoriamente incluir o `version_hook.py`.
- **Sintaxe Obrigatória:** 
  ```python
  from version_hook import declare as _vdeclare
  from version import __version__
  _vdeclare(__name__, __version__, "Breve descrição da função do módulo")
  ```

## 3. Ritual de Release - "Manutenibilidade em um Clique"
Para qualquer alteração de versão ou saneamento de documentação:
1. **Sync Automático**: Execute `python scripts/automate.py --fix`. Isso atualizará READMEs, Compliance, Baseline, CHANGELOGs, Cargo.toml e JSON Registry.
2. **Validação Rápida**: Execute `python scripts/automate.py --quick`. Este comando certifica que o sistema de boot e os motores principais não foram corrompidos.
3. **Registry Audit**: Verifique `data/module_versions.json` para garantir que novos módulos foram registrados.

## 4. Política de Remoção de Resíduos (Zombie Purge)
- Módulos órfãos (sem imports ativos em `src/`) devem ser deletados ou movidos para `archive/`. 
- Testes que referenciam módulos deletados devem ser purgados imediatamente.
- Dependências em `requirements.txt` devem ser auditadas trimestralmente para remover bibliotecas de stacks obsoletas (ex: PySide6/Qt).

## 5. Isolamento de Dados e Privacidade (LGPD)
- **Produção vs Código**: É terminantemente PROIBIDO versionar dados reais de clientes (`.xlsx`, `.csv`, `.zip`) no repositório. Use o `.gitignore` para blindar pastas de `backups/` e `tests/index/`.
- **Relativização de Caminhos**: Ninguém deve expor caminhos locais de hardware (ex: `C:\Users\nomedousuario\`). Utilize a âncora `src/core/paths.py` para resolver caminhos de forma dinâmica e agnóstica ao sistema operacional.
- **Limpeza de Cache**: Ambientes virtuais (`.venv`) e caches (`__pycache__`) devem ser excluídos do rastreamento Git para manter o repositório leve e focado apenas em código-fonte.

---
*Assinado: Motor de Governança Genaja (v0.7.3 Platinum Certified).*
