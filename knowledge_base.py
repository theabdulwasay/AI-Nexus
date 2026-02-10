import os
import json
from typing import List, Dict, Any

class KnowledgeBase:
    """Manages local knowledge and learned information."""
    
    def __init__(self, kb_path: str = "knowledge_base.json"):
        self.kb_path = kb_path
        self.knowledge = {}
        self.load()

    def load(self):
        if os.path.exists(self.kb_path):
            try:
                with open(self.kb_path, "r", encoding="utf-8") as f:
                    self.knowledge = json.load(f)
            except Exception:
                self.knowledge = {}

    def save(self):
        try:
            with open(self.kb_path, "w", encoding="utf-8") as f:
                json.dump(self.knowledge, f, indent=2)
        except Exception:
            pass

    def learn(self, source: str, content: str):
        """Add new information to the knowledge base."""
        self.knowledge[source] = {
            "content": content[:1000] + ("..." if len(content) > 1000 else ""),
            "timestamp": os.path.getmtime(source) if os.path.exists(source) else 0
        }
        self.save()

    def search(self, query: str) -> List[Dict[str, Any]]:
        """Simple keyword search in knowledge."""
        results = []
        query = query.lower()
        for source, info in self.knowledge.items():
            if query in source.lower() or query in info["content"].lower():
                results.append({"source": source, "content": info["content"]})
        return results

    def get_all(self) -> Dict[str, Any]:
        return self.knowledge
