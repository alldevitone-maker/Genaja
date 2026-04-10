import os
import sys
import pandas as pd
import unittest

# Setup paths
sys.path.append(os.path.join(os.getcwd(), "src"))

from core.duplicate_engine import DuplicateEngine
from migration.type_converter import TypeConverter

class TestV063Patch2(unittest.TestCase):
    def test_duplicate_detection(self):
        df = pd.DataFrame({"ID": [1, 1, 2], "V": ["A", "A", "B"]})
        engine = DuplicateEngine()
        summary, dups = engine.scan_for_duplicates(df, subset=["ID"])
        self.assertEqual(summary["duplicate_count"], 1)
        self.assertEqual(len(dups), 1)

    def test_type_conversion_br(self):
        conv = TypeConverter()
        s = pd.Series(["1.000,50", "500,00", "10.500"])
        numeric = conv.parse_numeric(s)
        self.assertEqual(numeric[0], 1000.5)
        self.assertEqual(numeric[1], 500.0)

if __name__ == "__main__":
    unittest.main()
