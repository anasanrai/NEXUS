import json
from typing import List, Dict, Any
from openai import OpenAI
from config import settings

class TaskPlanner:
    """Breaks down complex requests into a sequence of executable steps."""
    
    def __init__(self, model: str = settings.DEFAULT_MODEL):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = model

    async def create_plan(self, objective: str, available_tools: List[str]) -> List[Dict[str, Any]]:
        """Generates a step-by-step execution plan."""
        system_prompt = f"""
        You are the NEXUS Strategic Planner.
        Given an objective and a list of available tools: {available_tools}
        Create a detailed step-by-step plan.
        Return a JSON array of steps:
        [
          {{"step": 1, "action": "tool_name", "input": "input_parameters", "reason": "why this step"}},
          ...
        ]
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Objective: {objective}"}
            ],
            response_format={"type": "json_object"} # Planner often returns nested JSON
        )
        
        # Note: The output might need parsing if it's wrapped in a 'plan' key
        raw_data = json.loads(response.choices[0].message.content)
        if "plan" in raw_data:
            return raw_data["plan"]
        if isinstance(raw_data, list):
            return raw_data
        return [raw_data] # If it returns a single step object
