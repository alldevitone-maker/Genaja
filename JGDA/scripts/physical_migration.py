import os
import shutil

# Root path of the Genaja project
GENAJA_ROOT = r'C:\Users\ti01\Documents\Genaja'
DOCUMENTS_ROOT = r'C:\Users\ti01\Documents'
JGDA_ROOT = os.path.join(GENAJA_ROOT, 'JGDA')

def ensure_dirs():
    dirs = [
        os.path.join(GENAJA_ROOT, 'brains'),
        os.path.join(GENAJA_ROOT, 'shared', 'results'),
        os.path.join(GENAJA_ROOT, 'shared', 'logs'),
        os.path.join(GENAJA_ROOT, 'workspace'),
        os.path.join(GENAJA_ROOT, 'docs'),
        os.path.join(GENAJA_ROOT, 'scripts')
    ]
    for d in dirs:
        if not os.path.exists(d):
            print(f"Creating directory: {d}")
            os.makedirs(d, exist_ok=True)

def safe_move(src, dst):
    if not os.path.exists(src):
        print(f"Source not found, skipping: {src}")
        return
    
    if os.path.exists(dst):
        print(f"Target already exists: {dst}. Merging contents...")
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)
        shutil.rmtree(src)
    else:
        print(f"Moving: {src} -> {dst}")
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.move(src, dst)

def migrate():
    ensure_dirs()
    
    # 1. External brain folders
    safe_move(os.path.join(DOCUMENTS_ROOT, 'genaja_engineering'), 
              os.path.join(GENAJA_ROOT, 'brains', 'engineering'))
    
    safe_move(os.path.join(DOCUMENTS_ROOT, 'genaja_market_intelligence'), 
              os.path.join(GENAJA_ROOT, 'brains', 'market_intelligence'))
    
    # 2. Learning data (Merge external and JGDA internal)
    # External learn folder first
    safe_move(os.path.join(DOCUMENTS_ROOT, 'learn'), 
              os.path.join(GENAJA_ROOT, 'brains', 'learn'))
    
    # JGDA learn folder second (merging)
    safe_move(os.path.join(JGDA_ROOT, 'learn'), 
              os.path.join(GENAJA_ROOT, 'brains', 'learn'))
    
    # 3. Audit, Results, Logs
    safe_move(os.path.join(JGDA_ROOT, 'audit'), 
              os.path.join(GENAJA_ROOT, 'brains', 'audit'))
    
    safe_move(os.path.join(JGDA_ROOT, 'results'), 
              os.path.join(GENAJA_ROOT, 'shared', 'results'))
    
    safe_move(os.path.join(JGDA_ROOT, 'logs'), 
              os.path.join(GENAJA_ROOT, 'shared', 'logs'))
    
    print("\nPhysical migration completed successfully.")

if __name__ == "__main__":
    migrate()
