"""
Logger utility for Nexus AI.
"""

import logging
import os
from datetime import datetime

class Logger:
    """Standardized logger."""
    
    def __init__(self, name: str = "NexusAI", log_file: str = "nexus_ai.log"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Create handlers
        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler(log_file)
        c_handler.setLevel(logging.INFO)
        f_handler.setLevel(logging.INFO)
        
        # Create formatters and add it to handlers
        c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)
        
        # Add handlers to the logger
        if not self.logger.handlers:
            self.logger.addHandler(c_handler)
            self.logger.addHandler(f_handler)
            
    def info(self, msg: str):
        self.logger.info(msg)
        
    def error(self, msg: str):
        self.logger.error(msg)
        
    def warning(self, msg: str):
        self.logger.warning(msg)
