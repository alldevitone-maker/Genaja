import os
import sys
import subprocess
import argparse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run_script(script_path, args=None):
    cmd = [sys.executable, script_path]
    if args: cmd.extend(args)
    print(f"Running: {os.path.basename(script_path)}...")
    result = subprocess.run(cmd, capture_output=False)
    return result.returncode == 0

def main():
    parser = argparse.ArgumentParser(description="Genaja Automation Orchestrator")
    parser.add_argument("--release", action="store_true", help="Run full release flow (validate + backup + git)")
    parser.add_argument("--quick", action="store_true", help="Run quick validation only")
    parser.add_argument("--fix", action="store_true", help="Attempt to fix common sync issues (Placeholder)")
    
    args = parser.parse_args()
    
    validate_path = os.path.join(BASE_DIR, 'scripts', 'validate.py')
    backup_path = os.path.join(BASE_DIR, 'scripts', 'make_backup.py')
    
    if not run_script(validate_path):
        print("Validation failed. Aborting.")
        sys.exit(1)
        
    if args.quick:
        print("Quick validation passed.")
        sys.exit(0)
        
    if args.release:
        print("\n--- Starting Release Flow ---")
        if not run_script(backup_path):
            print("Backup failed. Aborting.")
            sys.exit(1)
            
        print("\n--- Git Operations ---")
        # Logic for git push could be added here or kept manual as per user preference
        # For now, we just pass the validation and backup phases.
        print("Validation and Backup completed successfully.")
        print("You can now safely run: git add . && git commit -m 'Release vX.Y.Z' && git push")
        sys.exit(0)

if __name__ == "__main__":
    main()
