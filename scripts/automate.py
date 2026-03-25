import os
import sys
import subprocess
import argparse
import re
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FREEZE_FILE = os.path.join(BASE_DIR, "FREEZE.lock")

def is_frozen():
    return os.path.exists(FREEZE_FILE)

def set_freeze(reason=""):
    with open(FREEZE_FILE, 'w', encoding='utf-8') as f:
        f.write(f"FREEZE ATIVO\nMotivo: {reason}\nData: {datetime.date.today()}\n")
        f.write("\nPara retomar o desenvolvimento, execute: python scripts/automate.py --unfreeze\n")
    print(f"\n❄️  PROJETO CONGELADO em v{get_version_info()[0]}")
    print(f"   Motivo: {reason or 'Não informado'}")
    print(f"   Arquivo: {FREEZE_FILE}")
    print(f"   Release e Push estão BLOQUEADOS até o unfreeze.")
    print(f"   'automate.py --quick' continua funcionando.\n")

def remove_freeze():
    if os.path.exists(FREEZE_FILE):
        os.remove(FREEZE_FILE)
        print(f"\n✅ Projeto DESCONGELADO! Pipeline de release reativado.")
        print(f"   Você pode rodar: python scripts/automate.py --release --push\n")
    else:
        print("\nNenhum FREEZE.lock encontrado. O projeto já está ativo.\n")

def run_script(script_path, args=None):
    cmd = [sys.executable, script_path]
    if args: cmd.extend(args)
    print(f"Running: {os.path.basename(script_path)}...")
    result = subprocess.run(cmd, capture_output=False)
    return result.returncode == 0

def get_version_info():
    version_vars = {}
    v_path = os.path.join(BASE_DIR, 'src', 'version.py')
    with open(v_path, 'r', encoding='utf-8') as f:
        exec(f.read(), version_vars)
    return version_vars.get('__version__'), version_vars.get('__title__')

def _fix_sync():
    version, title = get_version_info()
    print(f"Fixing documentation sync for version {version}...")
    
    # Update READMEs
    readme_files = [
        ('README.md', r'(> \*\*Versão Atual:\*\* `v).*?(` \().*?(\))', r'\g<1>' + version + r'\g<2>' + title + r'\g<3>'),
        ('README.en.md', r'(> \*\*Current Version:\*\* `v).*?(` \().*?(\))', r'\g<1>' + version + r'\g<2>' + title + r'\g<3>')
    ]
    
    import re
    for filename, pattern, repl in readme_files:
        path = os.path.join(BASE_DIR, filename)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            new_content = re.sub(pattern, repl, content)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  -> Updated {filename}")

def _interactive_release():
    print("\n--- Modo Release Interativo ---")
    current_version, current_title = get_version_info()
    print(f"Versão atual: {current_version} ({current_title})")
    
    new_version = input(f"Nova versão (pressione Enter para manter {current_version}): ").strip() or current_version
    new_title = input(f"Novo título (PT): ").strip() or current_title
    new_title_en = input(f"Novo título (EN): ").strip() or new_title
    
    # Update version.py
    v_path = os.path.join(BASE_DIR, 'src', 'version.py')
    with open(v_path, 'w', encoding='utf-8') as f:
        f.write(f'__version__ = "{new_version}"\n__title__ = "{new_title}"\n')
    
    # Sync docs
    _fix_sync()
    
    print("\nNotas para o CHANGELOG (PT): (Deixe em branco para finalizar)")
    notes = []
    while True:
        note = input(" - ")
        if not note: break
        notes.append(note)
        
    if notes:
        # Simple changelog update logic
        cl_path = os.path.join(BASE_DIR, 'CHANGELOG.md')
        with open(cl_path, 'r', encoding='utf-8') as f: content = f.read()
        date = datetime.date.today().strftime("%d/%m/%Y")
        new_entry = f"## [{new_version}] - {date} ({new_title})\n" + "\n".join([f"- {n}" for n in notes])
        pattern = re.compile(r"(# Changelog.*?\n\n)(.*)", re.DOTALL)
        content = pattern.sub(f"\\g<1>{new_entry}\n\n\\g<2>", content)
        with open(cl_path, 'w', encoding='utf-8') as f: f.write(content)
        print(f"  -> Atualizado: {os.path.basename(cl_path)}")

def _run_git_push(version, title):
    """Executa git add, commit e push após release validado."""
    commit_msg = f"Release v{version} - {title}"
    print(f"\n--- Git Push Automatizado ---")
    print(f"Mensagem de commit: '{commit_msg}'")
    
    commands = [
        ["git", "add", "."],
        ["git", "commit", "-m", commit_msg],
        ["git", "push"],
    ]
    
    for cmd in commands:
        print(f"  -> Executando: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=False)
        if result.returncode != 0:
            print(f"ERRO ao executar: {' '.join(cmd)}")
            return False
    
    print(f"\n✅ Push concluído com sucesso! v{version} no ar.")
    return True


def main():
    parser = argparse.ArgumentParser(description="Genaja Automation Orchestrator")
    parser.add_argument("--freeze", action="store_true", help="Congela o projeto: bloqueia release e push")
    parser.add_argument("--unfreeze", action="store_true", help="Descongela o projeto e reativa o pipeline")
    parser.add_argument("--release", action="store_true", help="Run full release flow (validate + backup + git)")
    parser.add_argument("--quick", action="store_true", help="Run quick validation only")
    parser.add_argument("--fix", action="store_true", help="Attempt to fix common sync issues")
    parser.add_argument("--push", action="store_true", help="After release, auto git add + commit + push")
    
    args = parser.parse_args()

    # --- FREEZE / UNFREEZE ---
    if args.freeze:
        reason = input("Motivo do congelamento (opcional, Enter para pular): ").strip()
        set_freeze(reason)
        sys.exit(0)
    
    if args.unfreeze:
        remove_freeze()
        sys.exit(0)

    # --- BLOQUEIO SE FROZEN ---
    if is_frozen() and (args.release or args.push):
        print("\n❌ OPERAÇÃO BLOQUEADA: Projeto está CONGELADO.")
        with open(FREEZE_FILE, 'r', encoding='utf-8') as f:
            print(f.read())
        sys.exit(1)

    
    validate_path = os.path.join(BASE_DIR, 'scripts', 'validate.py')
    backup_path = os.path.join(BASE_DIR, 'scripts', 'make_backup.py')
    
    if args.fix:
        _fix_sync()
        print("Sync fix applied successfully.")
        sys.exit(0)

    if not run_script(validate_path):
        print("Validation failed. Aborting.")
        sys.exit(1)
        
    if args.quick:
        print("Quick validation passed.")
        sys.exit(0)
        
    if args.release:
        print("\n--- Starting Release Flow ---")
        _interactive_release()
        
        if not run_script(backup_path):
            print("Backup failed. Aborting.")
            sys.exit(1)
        
        if args.push:
            version, title = get_version_info()
            if not _run_git_push(version, title):
                print("\nGit push falhou. Verifique o estado do repositório.")
                sys.exit(1)
        else:
            print("\n--- Git Operations ---")
            version, title = get_version_info()
            print("Validation and Backup completed successfully.")
            print(f"You can now safely run: git add . && git commit -m 'Release v{version} - {title}' && git push")
            print("  (Ou use --push para automatizar esse passo na próxima vez)")
        
        sys.exit(0)

if __name__ == "__main__":
    main()
