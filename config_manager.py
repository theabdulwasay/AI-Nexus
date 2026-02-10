"""
Configuration manager for Nexus AI.
"""

import json
import os
from typing import Dict, Any

class ConfigManager:
    """Manages application configuration."""
    
    DEFAULT_CONFIG = {
        "app_name": "Nexus AI",
        "version": "2.1.0",
        "max_history_items": 100,
        "theme": "dark",
        "log_level": "INFO",
        "features": {
            "web_search": True,
            "calculator": True,
            "system_tools": True
        }
    }
    
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or default."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    return json.load(f)
            except Exception:
                return self.DEFAULT_CONFIG.copy()
        return self.DEFAULT_CONFIG.copy()
        
    def save_config(self):
        """Save current configuration to file."""
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=4)
            
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self.config.get(key, default)
        
    def set(self, key: str, value: Any):
        """Set a configuration value."""
        self.config[key] = value
        self.save_config()
