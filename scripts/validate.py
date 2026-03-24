import os
import sys
import re
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_version_info():
    version_vars = {}
    v_path = os.path.join(BASE_DIR, 'src', 'version.py')
    with open(v_path, 'r', encoding='utf-8') as f:
        exec(f.read(), version_vars)
    return version_vars.get('__version__'), version_vars.get('__title__')

def validate_version_sync():
    version, title = get_version_info()
    print(f"Checking version sync for: {version} ({title})")
    
    files_to_check = [
        ('README.md', r'> \*\*Versão Atual:\*\* `v' + re.escape(version) + r'` \(' + re.escape(title) + r'\)'),
        ('README.en.md', r'> \*\*Current Version:\*\* `v' + re.escape(version) + r'` \(' + re.escape(title) + r'\)'),
        ('CHANGELOG.md', r'## \[v?' + re.escape(version) + r'\]'),
        ('CHANGELOG.en.md', r'## \[v?' + re.escape(version) + r'\]'),
    ]
    
    errors = []
    for filename, pattern in files_to_check:
        path = os.path.join(BASE_DIR, filename)
        if not os.path.exists(path):
            errors.append(f"Missing file: {filename}")
            continue
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            if not re.search(pattern, content):
                errors.append(f"Version/Title mismatch in {filename}")
    
    return errors

def check_naming_conventions():
    errors = []
    # Simplified check for snake_case in src
    src_dir = os.path.join(BASE_DIR, 'src')
    for root, dirs, files in os.walk(src_dir):
        if '__pycache__' in root: continue
        for name in files + dirs:
            if name.startswith('__'): continue
            if not re.match(r'^[a-z0-9_.]+$', name):
                errors.append(f"Naming violation: {os.path.join(root, name)} (use snake_case)")
    return errors

def check_junk_files():
    errors = []
    junk_patterns = [r'copy of', r'copia de', r'tmp', r'\.bak$', r'~']
    for root, dirs, files in os.walk(BASE_DIR):
        if any(d in root for d in ['.git', 'backups', 'venv', '__pycache__']): continue
        for name in files:
            for pattern in junk_patterns:
                if re.search(pattern, name, re.IGNORECASE):
                    errors.append(f"Junk file detected: {os.path.join(root, name)}")
    return errors

def run_tests():
    print("Running Smoke Test...")
    smoke_path = os.path.join(BASE_DIR, 'tests', 'smoke_test.py')
    try:
        subprocess.run([sys.executable, smoke_path], check=True, capture_output=True, text=True)
        return []
    except subprocess.CalledProcessError as e:
        return [f"Smoke test failed: {e.stdout}\n{e.stderr}"]

def main():
    all_errors = []
    all_errors.extend(validate_version_sync())
    all_errors.extend(check_naming_conventions())
    all_errors.extend(check_junk_files())
    all_errors.extend(run_tests())
    
    if all_errors:
        print("\n--- VALIDATION FAILED ---")
        for err in all_errors:
            print(f"FAILED: {err}")
        sys.exit(1)
    else:
        print("\n--- VALIDATION PASSED ---")
        sys.exit(0)

if __name__ == "__main__":
    main()
