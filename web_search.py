"""
Web search tool for searching the internet.
"""

from typing import Dict, Any, Optional
import requests
from urllib.parse import quote


class WebSearch:
    """Tool for performing web searches."""
    
    def __init__(self, api_key: Optional[str] = None, search_engine: str = "duckduckgo"):
        """
        Initialize web search tool.
        
        Args:
            api_key: Optional API key for search services
            search_engine: Search engine to use ('duckduckgo' or 'google')
        """
        self.api_key = api_key
        self.search_engine = search_engine
    
    def execute(self, query: str, max_results: int = 5) -> str:
        """
        Execute a web search.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            
        Returns:
            Search results as formatted string
        """
        try:
            if self.search_engine == "duckduckgo":
                return self._search_duckduckgo(query, max_results)
            elif self.search_engine == "google":
                return self._search_google(query, max_results)
            else:
                return self._search_simple(query, max_results)
        except Exception as e:
            return f"Error performing web search: {str(e)}"
    
    def _search_duckduckgo(self, query: str, max_results: int) -> str:
        """Search using DuckDuckGo (no API key required)."""
        try:
            # DuckDuckGo Instant Answer API
            url = f"https://api.duckduckgo.com/?q={quote(query)}&format=json&no_html=1&skip_disambig=1"
            response = requests.get(url, timeout=5)
            data = response.json()
            
            results = []
            
            # Get abstract/answer
            if data.get("AbstractText"):
                results.append(f"Answer: {data['AbstractText']}")
            
            # Get related topics
            if data.get("RelatedTopics"):
                for topic in data["RelatedTopics"][:max_results]:
                    if isinstance(topic, dict) and "Text" in topic:
                        results.append(f"- {topic['Text']}")
            
            if results:
                return "\n".join(results)
            else:
                return f"Search completed for '{query}'. No instant answers found. Consider using a search API for more detailed results."
                
        except Exception as e:
            return f"DuckDuckGo search error: {str(e)}. Note: For production use, consider integrating a proper search API."
    
    def _search_google(self, query: str, max_results: int) -> str:
        """Search using Google (requires API key)."""
        if not self.api_key:
            return "Google search requires an API key. Please set it in the WebSearch initialization."
        
        try:
            # Google Custom Search API
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                "key": self.api_key,
                "cx": "YOUR_SEARCH_ENGINE_ID",  # Replace with actual search engine ID
                "q": query,
                "num": max_results
            }
            response = requests.get(url, params=params, timeout=5)
            data = response.json()
            
            results = []
            if "items" in data:
                for item in data["items"]:
                    results.append(f"Title: {item.get('title', 'N/A')}")
                    results.append(f"Link: {item.get('link', 'N/A')}")
                    results.append(f"Snippet: {item.get('snippet', 'N/A')}")
                    results.append("")
            
            return "\n".join(results) if results else f"No results found for '{query}'"
            
        except Exception as e:
            return f"Google search error: {str(e)}"
    
    def _search_simple(self, query: str, max_results: int) -> str:
        """Simple search fallback (simulated)."""
        return f"Search query: '{query}'\nNote: This is a simulated search. For real results, configure a search API (DuckDuckGo, Google, Bing, etc.)"


if __name__ == "__main__":
    # Test the web search tool
    search = WebSearch()
    result = search.execute("Python programming")
    print(result)

