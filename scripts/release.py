import os
import sys
import re
import subprocess
import datetime

def run_command(command, capture=False):
    """Executa um comando no shell, lida com erros e retorna o sucesso."""
    print(f"🚀 Executando: {' '.join(command)}")
    try:
        result = subprocess.run(
            command, 
            check=True, 
            text=True, 
            capture_output=capture, 
            encoding='utf-8'
        )
        if capture:
            return result.stdout.strip()
        print("✅ Comando executado com sucesso.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ ERRO ao executar comando: {' '.join(command)}")
        print(f"   Saída do erro:\n{e.stderr}")
        return False
    except FileNotFoundError:
        print(f"❌ ERRO: Comando '{command[0]}' não encontrado. O Git está instalado e no PATH do sistema?")
        return False

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERSION_FILE = os.path.join(BASE_DIR, 'src', 'version.py')
CHANGELOG_FILE = os.path.join(BASE_DIR, 'CHANGELOG.md')
CHANGELOG_EN_FILE = os.path.join(BASE_DIR, 'CHANGELOG.en.md')
README_FILE = os.path.join(BASE_DIR, 'README.md')
README_EN_FILE = os.path.join(BASE_DIR, 'README.en.md')

def get_current_version():
    """Lê a versão atual do arquivo src/version.py."""
    version_vars = {}
    with open(VERSION_FILE, 'r', encoding='utf-8') as f:
        exec(f.read(), version_vars)
    return version_vars['__version__']

def update_file(path, content):
    """Escreve o novo conteúdo em um arquivo."""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    print("--- 🚀 Script de Automação de Release Genaja ---")

    # 1. Verificar se o repositório está limpo
    print("\n1. Verificando status do Git...")
    if run_command(['git', 'status', '--porcelain'], capture=True):
        print("❌ ERRO: Seu repositório Git tem alterações não commitadas.")
        print("   Por favor, commite ou descarte suas alterações antes de criar uma release.")
        sys.exit(1)
    print("✅ Repositório Git está limpo.")

    # 2. Obter informações da nova versão
    current_version = get_current_version()
    print(f"\n2. Versão atual detectada: {current_version}")
    
    new_version = input(f"   Digite a nova versão (ex: v0.3.6): ").strip()
    if not re.match(r'^v\d+\.\d+\.\d+$', new_version):
        print("❌ Formato de versão inválido. Use o formato 'vX.Y.Z'.")
        sys.exit(1)

    release_title = input(f"   Digite o título da release (ex: Release Automation): ").strip()
    if not release_title:
        print("❌ Título da release não pode ser vazio.")
        sys.exit(1)

    release_title_en = input(f"   Digite o título da release em INGLÊS (ex: Release Automation): ").strip()
    if not release_title_en:
        print("❌ Título em inglês não pode ser vazio.")
        sys.exit(1)

    print("\n3. Digite as notas para o CHANGELOG PT-BR (deixe em branco e pressione Enter para finalizar):")
    changelog_notes = []
    while True:
        note = input("   - ")
        if not note:
            break
        changelog_notes.append(note)

    if not changelog_notes:
        print("❌ Nenhuma nota de changelog fornecida. Abortando.")
        sys.exit(1)

    print("\n4. Digite as notas para o CHANGELOG EN (Inglês) (deixe em branco e pressione Enter para finalizar):")
    changelog_notes_en = []
    while True:
        note = input("   - ")
        if not note:
            break
        changelog_notes_en.append(note)

    if not changelog_notes_en:
        print("❌ Nenhuma nota de changelog em inglês fornecida. Abortando.")
        sys.exit(1)

    # 4. Confirmar antes de executar
    print("\n--- REVISÃO ---")
    print(f"Versão Atual:      {current_version}")
    print(f"Nova Versão:       {new_version}")
    print(f"Título (PT):       {release_title}")
    print(f"Título (EN):       {release_title_en}")
    print("Notas PT-BR:")
    for note in changelog_notes:
        print(f"  - {note}")
    print("Notas EN:")
    for note in changelog_notes_en:
        print(f"  - {note}")
    print("---------------")
    
    # 5. Confirmar
    if input("Tudo certo? Posso iniciar o processo de release? (s/n): ").lower() != 's':
        print("Abortado pelo usuário."); sys.exit(0)

    # 5. Executar as atualizações nos arquivos
    print("\n--- 🚀 INICIANDO PROCESSO DE RELEASE ---")
    
    # Atualiza version.py
    print(f"🔄 Atualizando {os.path.relpath(VERSION_FILE)}...")
    update_file(VERSION_FILE, f'__version__ = "{new_version}"\n__title__ = "{release_title}"\n')

    today = datetime.date.today().strftime("%d/%m/%Y")

    # ---- ATUALIZAÇÃO PT-BR ----
    print(f"🔄 Atualizando {os.path.relpath(CHANGELOG_FILE)}...")
    with open(CHANGELOG_FILE, 'r', encoding='utf-8') as f: old_changelog = f.read()
    new_entry = f"## [{new_version}] - {today} ({release_title})\n" + '\n'.join(f"- {note}" for note in changelog_notes)
    # Insert safely after the Badges
    pattern_cl = re.compile(r"(# Changelog.*?\n\n)(.*)", re.DOTALL)
    update_file(CHANGELOG_FILE, pattern_cl.sub(f"\\g<1>{new_entry}\n\n\\g<2>", old_changelog))

    print(f"🔄 Atualizando {os.path.relpath(README_FILE)}...")
    with open(README_FILE, 'r', encoding='utf-8') as f: readme_content = f.read()
    pattern = re.compile(r"(> \*\*Versão Atual:\*\* `)(" + re.escape(current_version) + r")(` \().*?(\))")
    new_readme_line = r"\g<1>" + new_version + r"\g<3>" + release_title + r"\g<4>"
    update_file(README_FILE, pattern.sub(new_readme_line, readme_content))

    # ---- ATUALIZAÇÃO EN ----
    print(f"🔄 Atualizando {os.path.relpath(CHANGELOG_EN_FILE)}...")
    with open(CHANGELOG_EN_FILE, 'r', encoding='utf-8') as f: old_changelog_en = f.read()
    new_entry_en = f"## [{new_version}] - {today} ({release_title_en})\n" + '\n'.join(f"- {note}" for note in changelog_notes_en)
    update_file(CHANGELOG_EN_FILE, pattern_cl.sub(f"\\g<1>{new_entry_en}\n\n\\g<2>", old_changelog_en))

    print(f"🔄 Atualizando {os.path.relpath(README_EN_FILE)}...")
    with open(README_EN_FILE, 'r', encoding='utf-8') as f: readme_en_content = f.read()
    pattern_en = re.compile(r"(> \*\*Current Version:\*\* `)(" + re.escape(current_version) + r")(` \().*?(\))")
    new_readme_en_line = r"\g<1>" + new_version + r"\g<3>" + release_title_en + r"\g<4>"
    update_file(README_EN_FILE, pattern_en.sub(new_readme_en_line, readme_en_content))

    # 6. Rodar smoke para validação
    print("\n6. Executando smoke_test.py para validação...")
    if not run_command([sys.executable, os.path.join(BASE_DIR, 'tests', 'smoke_test.py')]):
        print("❌ Smoke test falhou! Revertendo alterações nos arquivos...")
        run_command(['git', 'checkout', VERSION_FILE, CHANGELOG_FILE, README_FILE])
        print("   Alterações revertidas. A release foi cancelada.")
        sys.exit(1)
    print("✅ Smoke test passou com sucesso.")

    # 7. Executar Git
    print("\n7. Executando comandos Git...")
    commit_message = f"Release {new_version}: {release_title}"
    if not run_command(['git', 'add', '.']): sys.exit(1)
    if not run_command(['git', 'commit', '-m', commit_message]): sys.exit(1)
    if not run_command(['git', 'tag', new_version]): sys.exit(1)
    
    print("\n--- ✨ RELEASE CONCLUÍDA COM SUCESSO! ✨ ---")
    print(f"Versão {new_version} foi criada e taggeada localmente.")
    print("Para publicar no servidor remoto, execute os seguintes comandos:")
    print(f"  git push")
    print(f"  git push origin {new_version}")

if __name__ == "__main__":
    main()