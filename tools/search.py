import requests
from typing import Dict, Any
from config import settings

class SearchTool:
    """Performs web searches using DuckDuckGo or SerpApi."""
    
    def __init__(self):
        self.api_key = settings.SERPAPI_API_KEY

    async def run(self, query: str) -> Dict[str, Any]:
        """Executes a search query."""
        if self.api_key:
            return self._serp_search(query)
        else:
            return self._ddg_search(query)

    def _serp_search(self, query: str) -> Dict[str, Any]:
        # Implementation for SerpApi
        return {"source": "SerpApi", "results": [f"Result for {query}"]}

    def _ddg_search(self, query: str) -> Dict[str, Any]:
        # Implementation for DuckDuckGo
        return {"source": "DuckDuckGo", "results": [f"Result for {query}"]}
