import logging
from typing import List, Dict, Any, Optional
from .router import IntentRouter
from .persona import AgentPersona
from .planner import TaskPlanner
from .executor import ActionExecutor
from tools.registry import ToolRegistry
from memory.short_term import ShortTermMemory

class NexusAgent:
    """The central orchestrator for the NEXUS framework."""
    
    def __init__(self):
        self.persona = AgentPersona()
        self.router = IntentRouter()
        self.planner = TaskPlanner()
        self.registry = ToolRegistry()
        self.executor = ActionExecutor(self.registry)
        self.memory = ShortTermMemory()
        
        self.logger = logging.getLogger("nexus.core")
        logging.basicConfig(level=logging.INFO)

    async def process_message(self, user_input: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Main entry point for processing user messages."""
        self.logger.info(f"Processing message: {user_input}")
        
        # 1. Route Intent
        history = self.memory.get_history()
        analysis = await self.router.route(user_input, history)
        
        # 2. Add to context
        if context:
            analysis.update(context)
            
        # 3. Decision Logic
        if analysis["needs_tools"]:
            # 3a. Plan
            tools = self.registry.list_tools()
            plan = await self.planner.create_plan(user_input, tools)
            
            # 3b. Execute
            results = await self.executor.execute_plan(plan)
            
            # 3c. Summarize
            summary = self._summarize_results(results)
            self.memory.add_interaction(user_input, summary)
            return summary
        else:
            # Simple interaction
            response = await self._chat(user_input)
            self.memory.add_interaction(user_input, response)
            return response

    async def _chat(self, user_input: str) -> str:
        """Fallback for simple chat without tool use."""
        # Implementation via OpenAI client...
        return f"NEXUS: (Chatting) I received: {user_input}"

    def _summarize_results(self, results: List[Dict[str, Any]]) -> str:
        """Translates tool results into natural language."""
        return f"Processed interaction with {len(results)} steps."
