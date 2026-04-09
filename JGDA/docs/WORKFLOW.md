# Guia de Workflow e Automação - Genaja

Este documento explica como utilizar o sistema de automação e governança do projeto.

## 🔄 O Ciclo de Desenvolvimento

O projeto utiliza **Git Hooks** para garantir que nenhuma versão inconsistente ou código quebrado suba para o repositório.

### 1. Commit Automático (pre-commit)
Sempre que você rodar `git commit`, o sistema executará automaticamente:
- Verificação de sincronia de versão (README vs version.py).
- Teste de fumaça (Smoke Test).
- Auditoria de nomes de arquivos.

Se algo estiver errado, o commit será **bloqueado**.

### 2. Orquestrador de Release (`automate.py`)
Para preparar uma entrega oficial:
```bash
python scripts/automate.py --release
```
Isso validará o projeto e gerará o **Backup ZIP** automaticamente na pasta `backups/`.

---

## ❄️ Cenários de Exceção ("Congelar" e "Retomar")

### Como Congelar a Automação
Se você estiver em um merge complexo ou fazendo ajustes rápidos e **precisa** commitar algo mesmo com erro de validação:
```bash
git commit -m "ajuste temporário" --no-verify
```
> [!CAUTION]
> Use isso apenas para salvar o estado. Nunca dê push com `--no-verify` sem uma revalidação completa.

### Como Retomar e Corrigir
Após os ajustes manuais, para garantir que o projeto voltou aos trilhos:
1. Rode a validação manual: `python scripts/automate.py --quick`
2. Corrija o que o script apontar (ex: sincronizar versão).
3. Faça o commit final normalmente (sem `--no-verify`).

---

## 🔒 Arquivos Privados
O arquivo `ROADMAP.md` e a pasta `backups/` estão no `.gitignore`.
- **Eles continuam existindo no seu PC.**
- **Eles NUNCA serão enviados para o GitHub.**
Isso mantém a estratégia e os backups protegidos localmente.
