import pandas as pd
import sys
import os

# Setup path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'src'))

from core.engines.etl_engine import ETLEngine

def test_v048_logic():
    print("Testing v0.4.8 Logic Parity...")
    engine = ETLEngine()
    
    # 1. Mock Data
    df_src = pd.DataFrame({
        'ID': ['01', '02', '03'],
        'NOME': ['Alice', 'Bob', 'Charlie'],
        'VALOR': [100, 200, 300]
    })
    
    df_tgt = pd.DataFrame({
        'KEY': ['01', '02', '04'],
        'NAME_TGT': ['ALICE_OLD', '', 'DELTA'],
        'DATA': ['OldInfo', 'Existing', 'KeepMe']
    })
    
    mapping = {'NOME': 'NAME_TGT', 'VALOR': 'DATA'}
    
    # 2. Test Shielding (Don't overwrite if target has data)
    print("- Testing Shielding...")
    res_shield = engine.synchronize(
        df_src, df_tgt, 'ID', 'KEY', mapping, 
        protected_a1=False, shielding=True
    )
    
    # ID 1 in src matches KEY 01 in tgt. 
    # NAME_TGT in tgt is 'ALICE_OLD'. Shielding should KEEP 'ALICE_OLD'.
    alice_row = res_shield[res_shield['KEY'] == '01'].iloc[0]
    if alice_row['NAME_TGT'] != 'ALICE_OLD':
        print(f"FAILED Shielding: Expected 'ALICE_OLD', got '{alice_row['NAME_TGT']}'")
        return False
        
    # ID 2 in src matches KEY 02 in tgt. 
    # NAME_TGT in tgt is empty. Shielding should FILL 'Bob'.
    bob_row = res_shield[res_shield['KEY'] == '02'].iloc[0]
    if bob_row['NAME_TGT'] != 'Bob':
        print(f"FAILED Shielding: Expected 'Bob', got '{bob_row['NAME_TGT']}'")
        return False

    # 3. Test Protected A1
    print("- Testing Protected A1...")
    res_a1 = engine.synchronize(
        df_src, df_tgt, 'ID', 'KEY', mapping, 
        protected_a1=True, shielding=False
    )
    
    # The first column of df_tgt is 'KEY'. So KEY must stay at index 0.
    if res_a1.columns[0] != 'KEY':
        print(f"FAILED Protected A1: First column should be 'KEY', got '{res_a1.columns[0]}'")
        return False
    
    print("SUCCESS: v0.4.8 Logic Parity Verified.")
    return True

if __name__ == "__main__":
    if test_v048_logic():
        sys.exit(0)
    else:
        sys.exit(1)
