"""
NEXUS Core Agent - Main Agent Loop
Coordinates all agent operations: receiving messages, routing, planning, executing.
"""

import logging
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime

from config import config
from agent.router import ModelRouter, TaskType
from agent.planner import task_planner
from agent.executor import task_executor
from agent.persona import get_system_prompt, get_persona_context
from memory.short_term import ShortTermMemory
from memory.long_term import LongTermMemory
from tools.registry import tool_registry

logger = logging.getLogger(__name__)


class NEXUSCore:
    """Core NEXUS agent coordinator."""
    
    def __init__(self):
        """Initialize NEXUS core."""
        self.router = ModelRouter()
        self.short_term_memory = ShortTermMemory()
        self.long_term_memory = LongTermMemory()
        self.system_prompt = get_system_prompt()
        self.persona = get_persona_context()
        self.session_id = None
        self.current_task = None
        self.execution_context = {}
    
    async def process_message(
        self,
        message: str,
        session_id: str = None,
        user_context: dict = None,
    ) -> Dict[str, Any]:
        """
        Main entry point for processing user messages.
        
        Args:
            message: User message/task
            session_id: Session ID for continuity
            user_context: Additional context
            
        Returns:
            dict: {success, response, action_summary, cost}
        """
        try:
            self.session_id = session_id or f"session_{datetime.now().timestamp()}"
            self.execution_context = user_context or {}
            
            logger.info(f"Processing message: {message[:100]}")
            
            # Step 1: Load memory context
            memory_context = await self._load_memory_context()
            
            # Step 2: Detect task type
            task_type = self.router.detect_task_type(message)
            logger.info(f"Task type detected: {task_type.value}")
            
            # Step 3: Select model
            model = self.router.select_model(task_type)
            logger.info(f"Selected model: {model}")
            
            # Step 4: Plan if complex
            plan = None
            if task_type in [TaskType.COMPLEX, TaskType.CODE]:
                plan_result = await task_planner.create_plan(message, memory_context)
                if plan_result["success"]:
                    plan = plan_result["plan"]
                    logger.info(f"Plan created with {len(plan.get('subtasks', []))} subtasks")
            
            # Step 5: Call model or execute plan
            if plan and plan.get("requires_planning"):
                # Execute the plan
                execution_result = await task_executor.execute_plan(plan)
                response = self._format_plan_result(execution_result, plan)
            else:
                # Call model directly for simple tasks
                response = await self._call_model_for_task(
                    model,
                    message,
                    memory_context,
                )
            
            # Step 6: Save to memory
            await self._save_to_memory(message, response, memory_context)
            
            # Step 7: Format response
            cost_summary = self.router.get_cost_summary()
            
            return {
                "success": True,
                "response": response,
                "session_id": self.session_id,
                "task_type": task_type.value,
                "model_used": model,
                "action_summary": {
                    "task_type": task_type.value,
                    "completed": True,
                    "timestamp": datetime.now().isoformat(),
                },
                "cost": cost_summary.get("total", 0),
            }
            
        except Exception as e:
            logger.error(f"Message processing failed: {str(e)}")
            return {
                "success": False,
                "response": f"Error processing request: {str(e)}",
                "error": str(e),
                "session_id": self.session_id,
            }
    
    async def _load_memory_context(self) -> Dict[str, Any]:
        """Load relevant context from memory."""
        try:
            recent_history = await self.short_term_memory.get_history(
                self.session_id,
                limit=10,
            )
            
            return {
                "recent_messages": recent_history,
                "persona": self.persona,
            }
        except Exception as e:
            logger.warning(f"Failed to load memory context: {str(e)}")
            return {"persona": self.persona}
    
    async def _call_model_for_task(
        self,
        model: str,
        task: str,
        context: dict,
    ) -> str:
        """Call model for task completion."""
        try:
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": task},
            ]
            
            result = await self.router.call_model(
                model,
                messages,
                temperature=0.7,
                max_tokens=2000,
            )
            
            if result["success"]:
                content = result["result"].get("choices", [{}])[0].get("message", {})
                return content.get("content", "Task completed but no response generated.")
            else:
                return f"Error: {result['error']}"
                
        except Exception as e:
            logger.error(f"Model call failed: {str(e)}")
            return f"Error calling model: {str(e)}"
    
    def _format_plan_result(self, execution_result: dict, plan: dict) -> str:
        """Format plan execution results into response."""
        if not execution_result["success"]:
            return f"Task execution failed: {execution_result.get('errors')}"
        
        results = execution_result.get("results", {})
        completion_rate = execution_result.get("completion_rate", 0)
        
        summary = f"Task execution complete ({completion_rate*100:.0f}% success rate)\n\n"
        
        for subtask in plan.get("subtasks", []):
            st_id = subtask["id"]
            result = results.get(st_id, "Not executed")
            summary += f"- {subtask['title']}: {result}\n"
        
        return summary
    
    async def _save_to_memory(
        self,
        input_message: str,
        response: str,
        context: dict,
    ) -> None:
        """Save to both short and long term memory."""
        try:
            # Short-term memory
            await self.short_term_memory.add_message(
                self.session_id,
                "user",
                input_message,
            )
            await self.short_term_memory.add_message(
                self.session_id,
                "assistant",
                response,
            )
            
            # Long-term memory
            await self.long_term_memory.store(
                response,
                {
                    "type": "task_result",
                    "session_id": self.session_id,
                    "timestamp": datetime.now().isoformat(),
                    "task": input_message[:100],
                },
            )
            
            logger.info("Saved to memory")
        except Exception as e:
            logger.warning(f"Failed to save to memory: {str(e)}")
    
    async def get_status(self) -> Dict[str, Any]:
        """Get agent status."""
        return {
            "name": "NEXUS",
            "status": "operational",
            "version": "1.0",
            "uptime": "continuous",
            "session_id": self.session_id,
            "tools_available": len(tool_registry.list_tools()),
            "cost_summary": self.router.get_cost_summary(),
            "execution_summary": task_executor.get_execution_summary(),
        }
    
    async def register_tools(self) -> None:
        """Register all available tools in the registry."""
        try:
            from tools.registry import initialize_tool_registry
            global tool_registry
            tool_registry = await initialize_tool_registry()
            logger.info(f"Registered {len(tool_registry.list_tools())} tools")
        except Exception as e:
            logger.error(f"Failed to register tools: {str(e)}")


# Global instance
nexus_core = NEXUSCore()
