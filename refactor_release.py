import os
import re

# 1. FIX MAKE_BACKUP.PY
with open('make_backup.py', 'r', encoding='utf-8') as f:
    backup_code = f.read()

backup_code = backup_code.replace(
    "TITLE = version_vars.get('__title__', '').replace(' ', '_')",
    "TITLE = version_vars.get('__title__', '').replace(' ', '_')\nimport re\nTITLE = re.sub(r'[\\\\/*?:\"<>|]', '', TITLE)"
)

with open('make_backup.py', 'w', encoding='utf-8') as f:
    f.write(backup_code)


# 2. REWRITE RELEASE.PY
with open('release.py', 'r', encoding='utf-8') as f:
    rel_code = f.read()

# Replace file declarations
rel_code = rel_code.replace(
    "CHANGELOG_FILE = os.path.join(BASE_DIR, 'CHANGELOG.md')\nREADME_FILE = os.path.join(BASE_DIR, 'README.md')",
    "CHANGELOG_FILE = os.path.join(BASE_DIR, 'CHANGELOG.md')\nCHANGELOG_EN_FILE = os.path.join(BASE_DIR, 'CHANGELOG.en.md')\nREADME_FILE = os.path.join(BASE_DIR, 'README.md')\nREADME_EN_FILE = os.path.join(BASE_DIR, 'README.en.md')"
)

# Replace input logic
input_logic_old = """    print("\\n3. Digite as notas para o CHANGELOG (deixe em branco e pressione Enter para finalizar):")
    changelog_notes = []
    while True:
        note = input("   - ")
        if not note:
            break
        changelog_notes.append(note)

    if not changelog_notes:
        print("❌ Nenhuma nota de changelog fornecida. Abortando.")
        sys.exit(1)"""

input_logic_new = """    release_title_en = input(f"   Digite o título da release em INGLÊS (ex: Release Automation): ").strip()
    if not release_title_en:
        print("❌ Título em inglês não pode ser vazio.")
        sys.exit(1)

    print("\\n3. Digite as notas para o CHANGELOG PT-BR (deixe em branco e pressione Enter para finalizar):")
    changelog_notes = []
    while True:
        note = input("   - ")
        if not note:
            break
        changelog_notes.append(note)

    if not changelog_notes:
        print("❌ Nenhuma nota de changelog fornecida. Abortando.")
        sys.exit(1)

    print("\\n4. Digite as notas para o CHANGELOG EN (Inglês) (deixe em branco e pressione Enter para finalizar):")
    changelog_notes_en = []
    while True:
        note = input("   - ")
        if not note:
            break
        changelog_notes_en.append(note)

    if not changelog_notes_en:
        print("❌ Nenhuma nota de changelog em inglês fornecida. Abortando.")
        sys.exit(1)"""

rel_code = rel_code.replace(input_logic_old, input_logic_new)

# Modify Review block
rel_code = rel_code.replace(
    "    print(\"\\n--- REVISÃO ---\")\n    print(f\"Versão Atual:      {current_version}\")\n    print(f\"Nova Versão:       {new_version}\")\n    print(f\"Título da Release: {release_title}\")\n    print(\"Notas do Changelog:\")\n    for note in changelog_notes:\n        print(f\"  - {note}\")\n    print(\"---------------\")",
    "    print(\"\\n--- REVISÃO ---\")\n    print(f\"Versão Atual:      {current_version}\")\n    print(f\"Nova Versão:       {new_version}\")\n    print(f\"Título (PT):       {release_title}\")\n    print(f\"Título (EN):       {release_title_en}\")\n    print(\"Notas PT-BR:\")\n    for note in changelog_notes:\n        print(f\"  - {note}\")\n    print(\"Notas EN:\")\n    for note in changelog_notes_en:\n        print(f\"  - {note}\")\n    print(\"---------------\")"
)
rel_code = rel_code.replace("if input(\"Tudo certo?", "# 5. Confirmar\n    if input(\"Tudo certo?")

# Modify File Update block
update_logic_old = """    # Atualiza CHANGELOG.md
    print(f"🔄 Atualizando {os.path.relpath(CHANGELOG_FILE)}...")
    with open(CHANGELOG_FILE, 'r', encoding='utf-8') as f: old_changelog = f.read()
    today = datetime.date.today().strftime("%d/%m/%Y")
    new_entry = f"## [{new_version}] - {today} ({release_title})\\n" + '\\n'.join(f"- {note}" for note in changelog_notes)
    update_file(CHANGELOG_FILE, f"# Changelog\\n\\n{new_entry}\\n\\n{old_changelog.replace('# Changelog', '').strip()}")

    # Atualiza README.md
    print(f"🔄 Atualizando {os.path.relpath(README_FILE)}...")
    with open(README_FILE, 'r', encoding='utf-8') as f: readme_content = f.read()
    pattern = re.compile(r"(> \*\*Versão Atual:\*\* `)(" + re.escape(current_version) + r")(` \().*?(\))")
    new_readme_line = r"\\g<1>" + new_version + r"\\g<3>" + release_title + r"\\g<4>"
    update_file(README_FILE, pattern.sub(new_readme_line, readme_content))"""

update_logic_new = """    today = datetime.date.today().strftime("%d/%m/%Y")

    # ---- ATUALIZAÇÃO PT-BR ----
    print(f"🔄 Atualizando {os.path.relpath(CHANGELOG_FILE)}...")
    with open(CHANGELOG_FILE, 'r', encoding='utf-8') as f: old_changelog = f.read()
    new_entry = f"## [{new_version}] - {today} ({release_title})\\n" + '\\n'.join(f"- {note}" for note in changelog_notes)
    # Insert safely after the Badges
    pattern_cl = re.compile(r"(# Changelog.*?\\n\\n)(.*)", re.DOTALL)
    update_file(CHANGELOG_FILE, pattern_cl.sub(f"\\\\g<1>{new_entry}\\n\\n\\\\g<2>", old_changelog))

    print(f"🔄 Atualizando {os.path.relpath(README_FILE)}...")
    with open(README_FILE, 'r', encoding='utf-8') as f: readme_content = f.read()
    pattern = re.compile(r"(> \*\*Versão Atual:\*\* `)(" + re.escape(current_version) + r")(` \\().*?(\\))")
    new_readme_line = r"\\g<1>" + new_version + r"\\g<3>" + release_title + r"\\g<4>"
    update_file(README_FILE, pattern.sub(new_readme_line, readme_content))

    # ---- ATUALIZAÇÃO EN ----
    print(f"🔄 Atualizando {os.path.relpath(CHANGELOG_EN_FILE)}...")
    with open(CHANGELOG_EN_FILE, 'r', encoding='utf-8') as f: old_changelog_en = f.read()
    new_entry_en = f"## [{new_version}] - {today} ({release_title_en})\\n" + '\\n'.join(f"- {note}" for note in changelog_notes_en)
    update_file(CHANGELOG_EN_FILE, pattern_cl.sub(f"\\\\g<1>{new_entry_en}\\n\\n\\\\g<2>", old_changelog_en))

    print(f"🔄 Atualizando {os.path.relpath(README_EN_FILE)}...")
    with open(README_EN_FILE, 'r', encoding='utf-8') as f: readme_en_content = f.read()
    pattern_en = re.compile(r"(> \*\*Current Version:\*\* `)(" + re.escape(current_version) + r")(` \\().*?(\\))")
    new_readme_en_line = r"\\g<1>" + new_version + r"\\g<3>" + release_title_en + r"\\g<4>"
    update_file(README_EN_FILE, pattern_en.sub(new_readme_en_line, readme_en_content))"""

rel_code = rel_code.replace("6. Rodar smoke test", "6. Rodar smoke")
rel_code = rel_code.replace("7. Executar comandos", "7. Executar")
rel_code = rel_code.replace(update_logic_old, update_logic_new)

with open('release.py', 'w', encoding='utf-8') as f:
    f.write(rel_code)

print("Automatizadores nativos corrigidos com sucesso!")
