from typing import List, Dict, Any
import logging

class ActionExecutor:
    """Handles the execution of planned actions and tool calls."""
    
    def __init__(self, tool_registry: Any):
        self.registry = tool_registry
        self.logger = logging.getLogger("nexus.executor")

    async def execute_step(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """Executes a single step of a plan."""
        tool_name = step.get("action")
        tool_input = step.get("input")
        
        self.logger.info(f"Executing {tool_name} with input: {tool_input}")
        
        try:
            tool = self.registry.get_tool(tool_name)
            if not tool:
                return {"status": "error", "message": f"Tool {tool_name} not found"}
            
            result = await tool.run(tool_input)
            return {"status": "success", "tool": tool_name, "result": result}
            
        except Exception as e:
            self.logger.error(f"Error executing {tool_name}: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def execute_plan(self, plan: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Executes a sequence of steps."""
        results = []
        for step in plan:
            result = await self.execute_step(step)
            results.append(result)
            if result["status"] == "error":
                break
        return results
