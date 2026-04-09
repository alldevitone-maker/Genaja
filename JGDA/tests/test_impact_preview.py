import pandas as pd
from src.core.impact_preview import ImpactSimulator

def test_impact_simulator_base_logic():
    # Setup 'before' state
    df_before = pd.DataFrame({
        "codigo": ["100", "101", "102"],
        "preco": [10.5, 20.0, 30.0],
        "estoque": [5, 10, 15]
    })
    
    # Setup 'after' state:
    # 100 -> price changed
    # 101 -> stock changed
    # 102 -> NO change
    # 103 -> NEW row
    df_after = pd.DataFrame({
        "codigo": ["100", "101", "102", "103"],
        "preco": [15.0, 20.0, 30.0, 40.0],
        "estoque": [5, 12, 15, 20]
    })
    
    report = ImpactSimulator.generate_impact_report(df_before, df_after, primary_key="codigo")
    
    assert report["status"] == "success"
    assert report["total_analyzed"] == 4
    assert report["lines_new"] == 1
    assert report["lines_changed"] == 2 # 100 and 101 both had cell changes
    
    # Expected changed columns: 'preco' = 1 change (row 100), 'estoque' = 1 change (row 101)
    # The new row (103) is excluded from the cell mutation diff calculation because it's NEW
    assert "preco" in report["columns_affected"]
    assert report["columns_affected"]["preco"] == 1
    
    assert "estoque" in report["columns_affected"]
    assert report["columns_affected"]["estoque"] == 1

def test_impact_simulator_no_changes():
    df_before = pd.DataFrame({
        "codigo": ["1"],
        "preco": [10.0]
    })
    
    report = ImpactSimulator.generate_impact_report(df_before, df_before.copy(), primary_key="codigo")
    
    assert report["status"] == "success"
    assert report["total_analyzed"] == 1
    assert report["lines_new"] == 0
    assert report["lines_changed"] == 0
    assert len(report["columns_affected"]) == 0

if __name__ == "__main__":
    test_impact_simulator_base_logic()
    test_impact_simulator_no_changes()
    print("🟢 IMPACT PREVIEW MVP TESTS PASSED SUCCESSFULLY!")
