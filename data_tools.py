import pandas as pd
import os
from typing import Dict, Any, List

class DataTool:
    """Tools for data analysis and manipulation."""
    
    def execute(self, operation: str, **kwargs) -> Any:
        if operation == "summarize_csv":
            return self.summarize_csv(kwargs.get("path"))
        elif operation == "stats":
            return self.get_stats(kwargs.get("path"))
        else:
            return f"Data operation '{operation}' not supported"

    def summarize_csv(self, path: str) -> str:
        """Summarize a CSV file."""
        if not path or not os.path.exists(path):
            return f"Error: File '{path}' not found"
        
        try:
            df = pd.read_csv(path)
            summary = [
                f"Summary of {path}:",
                f"Rows: {len(df)}",
                f"Columns: {', '.join(df.columns)}",
                "\nFirst 5 rows:",
                df.head().to_string()
            ]
            return "\n".join(summary)
        except Exception as e:
            return f"Error reading CSV: {str(e)}"

    def get_stats(self, path: str) -> str:
        """Get descriptive statistics for numerical columns."""
        if not path or not os.path.exists(path):
            return f"Error: File '{path}' not found"
        
        try:
            df = pd.read_csv(path)
            stats = df.describe().to_string()
            return f"Statistics for {path}:\n{stats}"
        except Exception as e:
            return f"Error calculating stats: {str(e)}"
