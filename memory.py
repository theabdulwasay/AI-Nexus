"""
Memory module for storing and retrieving conversation history and context.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import os


class Memory:
    """Manages conversation memory and context."""
    
    def __init__(self, max_history: int = 100):
        """
        Initialize memory.
        
        Args:
            max_history: Maximum number of interactions to store
        """
        self.max_history = max_history
        self.conversation_history = []
        self.context = {}
    
    def add_interaction(self, role: str, content: str, metadata: Dict[str, Any] = None):
        """
        Add an interaction to memory.
        
        Args:
            role: 'user' or 'assistant'
            content: Message content
            metadata: Optional metadata dictionary
        """
        interaction = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        self.conversation_history.append(interaction)
        
        # Limit history size
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]
            
        # Auto-save
        self._save_to_disk()
            
    def _save_to_disk(self):
        """Save memory to disk."""
        try:
             with open("memory.json", "w", encoding="utf-8") as f:
                json.dump({
                    "history": self.conversation_history,
                    "context": self.context
                }, f, indent=2, ensure_ascii=False)
        except Exception:
            pass # Fail silently for now to avoid interrupting flow

    def load_from_disk(self):
        """Load memory from disk if exists."""
        if os.path.exists("memory.json"):
            try:
                with open("memory.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.conversation_history = data.get("history", [])
                    self.context = data.get("context", {})
            except Exception:
                pass
    
    def get_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get conversation history.
        
        Args:
            limit: Maximum number of interactions to return
            
        Returns:
            List of interaction dictionaries
        """
        if limit:
            return self.conversation_history[-limit:]
        return self.conversation_history.copy()
    
    def get_recent_context(self, n: int = 5) -> List[Dict[str, Any]]:
        """
        Get recent conversation context.
        
        Args:
            n: Number of recent interactions to return
            
        Returns:
            List of recent interactions
        """
        return self.get_history(limit=n)
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get memory statistics.
        
        Returns:
            Dictionary with statistics
        """
        history = self.conversation_history
        total_interactions = len(history)
        
        if not history:
            return {
                "total_interactions": 0,
                "first_interaction": None,
                "last_interaction": None,
                "role_distribution": {}
            }
            
        role_Distribution = {}
        for h in history:
            role = h.get("role", "unknown")
            role_Distribution[role] = role_Distribution.get(role, 0) + 1
            
        return {
            "total_interactions": total_interactions,
            "first_interaction": history[0].get("timestamp"),
            "last_interaction": history[-1].get("timestamp"),
            "role_distribution": role_Distribution,
            "context_keys": list(self.context.keys())
        }

    def search_memory(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Advanced search in memory.
        
        Args:
            query: Text to search for
            limit: Max results
            
        Returns:
            List of matching interaction items
        """
        matches = []
        query_lower = query.lower()
        
        for item in reversed(self.conversation_history):
            content = item.get("content", "").lower()
            if query_lower in content:
                matches.append(item)
                if len(matches) >= limit:
                    break
        
        return matches

    def clear(self):
        """Clear all conversation history and context."""
        self.conversation_history = []
        self.context = {}
        self._save_to_disk()
    
    def export_history(self, filepath: str):
        """
        Export conversation history to a JSON file.
        
        Args:
            filepath: Path to output file
        """
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump({
                "history": self.conversation_history,
                "context": self.context,
                "stats": self.get_stats()
            }, f, indent=2, ensure_ascii=False)
    
    def import_history(self, filepath: str):
        """
        Import conversation history from a JSON file.
        
        Args:
            filepath: Path to input file
        """
        if not os.path.exists(filepath):
            return 
            
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.conversation_history = data.get("history", [])
            self.context = data.get("context", {})

