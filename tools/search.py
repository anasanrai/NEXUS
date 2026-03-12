"""
Web Search Tool using Tavily API
Provides web search and news search capabilities.
"""

import logging
from typing import List, Dict, Any
import httpx

from config import config

logger = logging.getLogger(__name__)


class SearchTool:
    """Web search functionality using Tavily API."""
    
    def __init__(self):
        """Initialize search tool."""
        self.api_key = config.search.tavily_api_key
        self.base_url = "https://api.tavily.com"
    
    async def web_search(
        self,
        query: str,
        max_results: int = 5,
        include_answer: bool = True,
    ) -> Dict[str, Any]:
        """
        Perform web search.
        
        Args:
            query: Search query
            max_results: Maximum results to return
            include_answer: Include answer generation
            
        Returns:
            dict: {success, result, error}
        """
        try:
            payload = {
                "api_key": self.api_key,
                "query": query,
                "max_results": max_results,
                "include_answer": include_answer,
            }
            
            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.post(
                    f"{self.base_url}/search",
                    json=payload,
                )
            
            if response.status_code != 200:
                logger.error(f"Search API error: {response.status_code}")
                return {
                    "success": False,
                    "result": None,
                    "error": f"API error: {response.status_code}",
                }
            
            data = response.json()
            
            results = []
            for result in data.get("results", []):
                results.append({
                    "title": result.get("title"),
                    "url": result.get("url"),
                    "content": result.get("content"),
                    "score": result.get("score"),
                })
            
            return {
                "success": True,
                "result": {
                    "query": query,
                    "answer": data.get("answer"),
                    "results": results,
                    "response_time": data.get("response_time"),
                },
                "error": None,
            }
            
        except Exception as e:
            logger.error(f"Web search failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    async def news_search(
        self,
        query: str,
        days: int = 7,
        max_results: int = 5,
    ) -> Dict[str, Any]:
        """
        Search news articles.
        
        Args:
            query: Search query
            days: Days back to search
            max_results: Maximum results
            
        Returns:
            dict: {success, result, error}
        """
        try:
            payload = {
                "api_key": self.api_key,
                "query": query,
                "max_results": max_results,
                "topic": "news",
                "days": days,
            }
            
            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.post(
                    f"{self.base_url}/search",
                    json=payload,
                )
            
            if response.status_code != 200:
                return {
                    "success": False,
                    "result": None,
                    "error": f"API error: {response.status_code}",
                }
            
            data = response.json()
            results = []
            
            for result in data.get("results", []):
                results.append({
                    "title": result.get("title"),
                    "url": result.get("url"),
                    "content": result.get("content"),
                    "published": result.get("published_date"),
                    "source": result.get("source"),
                })
            
            return {
                "success": True,
                "result": {
                    "query": query,
                    "days": days,
                    "results": results,
                },
                "error": None,
            }
            
        except Exception as e:
            logger.error(f"News search failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }


# Global instance
search_tool = SearchTool()


async def web_search(query: str, max_results: int = 5) -> Dict[str, Any]:
    """Web search wrapper."""
    return await search_tool.web_search(query, max_results)


async def news_search(query: str, days: int = 7) -> Dict[str, Any]:
    """News search wrapper."""
    return await search_tool.news_search(query, days)
