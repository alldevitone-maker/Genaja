import sys
import os

# --- ENVIRONMENT CONFIGURATION ---
BASE_DIR = r"c:\Users\ti01\Documents\Genaja\JGDA"
SRC_DIR = os.path.join(BASE_DIR, 'src')
sys.path.insert(0, SRC_DIR)

from ui_flet.theme import PlatinumTheme

def debug_theme():
    try:
        val = PlatinumTheme.PRIMARY()
        print(f"VAL: '{val}'")
        print(f"LOWER: '{val.lower()}'")
        print(f"MATCH: {val.lower() == '#3b82f6'}")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    debug_theme()
