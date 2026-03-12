"""
Model Routing Logic for NEXUS
Routes tasks to the most appropriate AI model based on task type and complexity.
"""

import json
import logging
from typing import Type, Optional
from enum import Enum
import httpx

from config import config

logger = logging.getLogger(__name__)


class TaskType(Enum):
    """Task classification types."""
    BROWSER = "browser"
    RESEARCH = "research"
    SIMPLE = "simple"
    COMPLEX = "complex"
    CODE = "code"
    UNKNOWN = "unknown"


class ModelRouter:
    """Routes tasks to appropriate AI models via OpenRouter."""
    
    def __init__(self):
        """Initialize the router with model configurations."""
        self.openrouter_api_key = config.llm.openrouter_api_key
        self.base_url = "https://openrouter.ai/api/v1"
        self.cost_tracking = {}
        
        self.models = {
            "primary": config.llm.primary_model,      # minimax-m2.5
            "browser": config.llm.browser_model,      # glm-5
            "fast": config.llm.fast_model,            # gemini-2.5-flash
            "fallback": config.llm.fallback_model,    # claude-sonnet-4-5
        }
    
    def detect_task_type(self, content: str) -> TaskType:
        """
        Detect task type from content.
        
        Args:
            content: Task description or message
            
        Returns:
            TaskType: Classified task type
        """
        content_lower = content.lower()
        
        browser_keywords = ["click", "visit", "navigate", "scrape", "screenshot", 
                           "fill form", "browser", "website", "webpage", "url"]
        research_keywords = ["search", "research", "find information", "lookup", 
                            "news", "trending", "latest"]
        code_keywords = ["code", "write", "function", "debug", "fix", "git", 
                        "repository", "deploy", "python", "javascript"]
        
        if any(keyword in content_lower for keyword in browser_keywords):
            return TaskType.BROWSER
        if any(keyword in content_lower for keyword in research_keywords):
            return TaskType.RESEARCH
        if any(keyword in content_lower for keyword in code_keywords):
            return TaskType.CODE
        if len(content) < 100 and content.count(" ") < 20:
            return TaskType.SIMPLE
        if "," in content or ";" in content or any(word in content_lower 
                                                     for word in ["multiple", "several", "complex"]):
            return TaskType.COMPLEX
        
        return TaskType.UNKNOWN
    
    def select_model(self, task_type: TaskType) -> str:
        """
        Select model based on task type.
        
        Args:
            task_type: Type of task
            
        Returns:
            str: Model name from OpenRouter
        """
        routing_map = {
            TaskType.BROWSER: self.models["browser"],
            TaskType.RESEARCH: self.models["browser"],
            TaskType.SIMPLE: self.models["fast"],
            TaskType.CODE: self.models["primary"],
            TaskType.COMPLEX: self.models["primary"],
            TaskType.UNKNOWN: self.models["fallback"],
        }
        return routing_map.get(task_type, self.models["fallback"])
    
    async def call_model(
        self,
        model: str,
        messages: list,
        tools: Optional[list] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> dict:
        """
        Call the selected model via OpenRouter.
        
        Args:
            model: Model name
            messages: List of message dicts with role and content
            tools: Optional list of tool definitions
            temperature: Sampling temperature
            max_tokens: Maximum output tokens
            
        Returns:
            dict: {success, result, error, cost}
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.openrouter_api_key}",
                "Content-Type": "application/json",
            }
            
            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
            }
            
            if tools:
                payload["tools"] = tools
                payload["tool_choice"] = "auto"
            
            async with httpx.AsyncClient(timeout=60) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                )
            
            if response.status_code != 200:
                logger.error(f"OpenRouter error: {response.status_code} {response.text}")
                return {
                    "success": False,
                    "result": None,
                    "error": f"API error: {response.status_code}",
                    "cost": 0,
                }
            
            result = response.json()
            cost = self._calculate_cost(model, result)
            self._track_cost(model, cost)
            
            return {
                "success": True,
                "result": result,
                "error": None,
                "cost": cost,
            }
            
        except Exception as e:
            logger.error(f"Model call failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
                "cost": 0,
            }
    
    def _calculate_cost(self, model: str, result: dict) -> float:
        """
        Calculate API cost from response.
        
        Args:
            model: Model used
            result: API response
            
        Returns:
            float: Estimated cost in USD
        """
        usage = result.get("usage", {})
        input_tokens = usage.get("prompt_tokens", 0)
        output_tokens = usage.get("completion_tokens", 0)
        
        # Estimated costs per 1M tokens (updated 2024)
        cost_map = {
            "minimax/minimax-m2.5": {"input": 0.04, "output": 0.12},
            "z-ai/glm-5": {"input": 0.1, "output": 0.3},
            "google/gemini-2.5-flash": {"input": 0.075, "output": 0.3},
            "anthropic/claude-sonnet-4-5": {"input": 3, "output": 15},
        }
        
        rates = cost_map.get(model, {"input": 0.1, "output": 0.3})
        cost = (input_tokens * rates["input"] + output_tokens * rates["output"]) / 1_000_000
        return round(cost, 6)
    
    def _track_cost(self, model: str, cost: float) -> None:
        """
        Track cumulative cost per model.
        
        Args:
            model: Model name
            cost: Cost amount
        """
        if model not in self.cost_tracking:
            self.cost_tracking[model] = 0
        self.cost_tracking[model] += cost
    
    def get_cost_summary(self) -> dict:
        """
        Get cost tracking summary.
        
        Returns:
            dict: Cost per model and total
        """
        total = sum(self.cost_tracking.values())
        return {
            "by_model": self.cost_tracking,
            "total": round(total, 6),
        }
