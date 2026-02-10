"""
System tools for accessing system information and file system.
"""

import os
import datetime
import platform
from typing import Dict, Any, List

class SystemTool:
    """Tool for retrieving system information."""
    
    def execute(self, action: str = "time") -> str:
        """
        Execute system action.
        
        Args:
            action: 'time', 'date', 'os_info'
        """
        if action == "time":
            return datetime.datetime.now().strftime("%H:%M:%S")
        elif action == "date":
            return datetime.datetime.now().strftime("%Y-%m-%d")
        elif action == "os_info":
            return f"{platform.system()} {platform.release()} ({platform.machine()})"
        else:
            return f"Unknown system action: {action}"

class FileTool:
    """Tool for file system operations (safe mode)."""
    
    def __init__(self, root_dir: str = "."):
        self.root_dir = os.path.abspath(root_dir)
    
    def execute(self, operation: str, path: str = ".") -> str:
        """
        Execute file operation.
        
        Args:
            operation: 'list', 'read'
            path: Target path relative to root
        """
        try:
            target_path = os.path.abspath(os.path.join(self.root_dir, path))
            
            # Security check: Ensure path is within root_dir
            if not target_path.startswith(self.root_dir):
                return "Error: Access denied (outside root directory)"
            
            if operation == "list":
                if os.path.isdir(target_path):
                    items = os.listdir(target_path)
                    return "\n".join(items) if items else "(empty directory)"
                else:
                    return "Error: Not a directory"
            
            elif operation == "read":
                if os.path.isfile(target_path):
                    # Limit file size for safety
                    if os.path.getsize(target_path) > 10000:
                        return "Error: File too large to read directly"
                        
                    with open(target_path, 'r', encoding='utf-8', errors='replace') as f:
                        return f.read()
                else:
                    return "Error: File not found"
            
            else:
                return f"Unknown file operation: {operation}"
                
        except Exception as e:
            return f"File operation error: {str(e)}"
