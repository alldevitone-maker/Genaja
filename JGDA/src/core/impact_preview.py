import logging
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

class ImpactSimulator:
    """
    Isolated simulator that compares two DataFrames (before and after ETL execution)
    to generate safety statistics without touching the destination file or the ETLEngine.
    """
    
    @staticmethod
    def generate_impact_report(df_before: pd.DataFrame, df_after: pd.DataFrame, primary_key: str) -> dict:
        """
        Compares original target DataFrame and the ETL-processed DataFrame in memory.
        
        Args:
            df_before: The initial state of the target file.
            df_after: The resulting state after ETLEngine (in memory).
            primary_key: The column used to identify unique rows.
            
        Returns:
            Dictionary with statistical impact data.
        """
        try:
            # Drop purely empty rows to avoid noise in statistics
            df_before_clean = df_before.dropna(how='all').copy()
            df_after_clean = df_after.dropna(how='all').copy()
            
            total_analyzed = len(df_after_clean)
            
            # 1. Identify new lines
            keys_before = set(df_before_clean[primary_key].dropna().astype(str))
            keys_after = set(df_after_clean[primary_key].dropna().astype(str))
            
            new_keys = keys_after - keys_before
            new_lines = len(new_keys)
            
            # 2. Align existing lines for cell-by-cell comparison
            # We only compare keys that existed before AND are still present
            existing_keys = list(keys_before.intersection(keys_after))
            
            df_old_aligned = df_before_clean[df_before_clean[primary_key].astype(str).isin(existing_keys)].set_index(primary_key)
            df_new_aligned = df_after_clean[df_after_clean[primary_key].astype(str).isin(existing_keys)].set_index(primary_key)
            
            # Ensure both dataframes have the same columns for comparison
            common_cols = list(set(df_old_aligned.columns).intersection(df_new_aligned.columns))
            df_old_aligned = df_old_aligned[common_cols].sort_index()
            df_new_aligned = df_new_aligned[common_cols].sort_index()
            
            # 3. Calculate changes
            # We replace NaNs to allow safe equality checks
            df_old_filled = df_old_aligned.fillna('')
            df_new_filled = df_new_aligned.fillna('')
            
            # Boolean mask of differences
            diff_mask = (df_old_filled != df_new_filled)
            
            # Lines with at least one changed cell
            changed_lines = int(diff_mask.any(axis=1).sum())
            
            # Changed cells per column
            cells_changed_per_col = diff_mask.sum(axis=0).to_dict()
            
            # Filter out columns with 0 changes
            affected_columns = {k: int(v) for k, v in cells_changed_per_col.items() if v > 0}
            
            return {
                "total_analyzed": total_analyzed,
                "lines_new": new_lines,
                "lines_changed": changed_lines,
                "columns_affected": affected_columns,
                "status": "success"
            }
            
        except Exception as e:
            logger.error("Impact simulator crashed during comparison: %s", e, exc_info=True)
            return {
                "status": "error",
                "error_message": str(e)
            }
