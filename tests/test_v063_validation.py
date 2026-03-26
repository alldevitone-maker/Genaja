import os
import sys
import pandas as pd
import unittest

# Setup paths
sys.path.append(os.path.join(os.getcwd(), "src"))

from core.validation_engine import ValidationEngine

class TestV063Validation(unittest.TestCase):
    def test_audit_dataframe(self):
        df = pd.DataFrame({
            "A": [1, 2, None, None],
            "B": [1, 2, 3, 4]
        })
        engine = ValidationEngine()
        report = engine.audit_dataframe(df)
        
        self.assertEqual(report["col_count"], 2)
        self.assertEqual(report["row_count"], 4)
        self.assertEqual(report["null_cells"], 2)
        # Coluna A tem 50% nulos, deve estar em critical
        self.assertEqual(len(report["critical_columns"]), 0) # Threshold é > 0.5 no meu código, vamos testar com 0.51
        
        df_bad = pd.DataFrame({"C": [None, None, None, 1]})
        report_bad = engine.audit_dataframe(df_bad)
        self.assertEqual(len(report_bad["critical_columns"]), 1)
        self.assertEqual(report_bad["critical_columns"][0]["name"], "C")

if __name__ == "__main__":
    unittest.main()
