import json
from typing import List, Dict, Any
from openai import OpenAI
from config import settings

class IntentRouter:
    """Routes user input to specific agent capabilities or tools."""
    
    def __init__(self, model: str = settings.DEFAULT_MODEL):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = model

    async def route(self, user_input: str, history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """Analyzes input to determine intent, mood, and required tools."""
        system_prompt = """
        You are the Intent Router for NEXUS. Your job is to analyze user messages and categorize them.
        Return a JSON object with:
        - intent: (e.g., "query", "action", "chat", "command")
        - mood: (e.g., "neutral", "excited", "frustrated")
        - needs_tools: boolean
        - suggested_tools: list of tool names if applicable
        - urgency: 1-5
        """
        
        messages = [{"role": "system", "content": system_prompt}]
        if history:
            messages.extend(history[-5:]) # Last 5 messages for context
        messages.append({"role": "user", "content": user_input})
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
