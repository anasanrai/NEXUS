"""
Task Executor for NEXUS
Executes plans and subtasks with error handling and retry logic.
"""

import logging
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime

from agent.planner import Subtask
from tools.registry import tool_registry

logger = logging.getLogger(__name__)


class TaskExecutor:
    """Executes tasks and subtasks with resilience."""
    
    def __init__(self, max_retries: int = 3):
        """
        Initialize executor.
        
        Args:
            max_retries: Max retry attempts per task
        """
        self.max_retries = max_retries
        self.execution_history = []
    
    async def execute_plan(self, plan: dict) -> Dict[str, Any]:
        """
        Execute a task plan.
        
        Args:
            plan: Plan from TaskPlanner
            
        Returns:
            dict: {success, results, errors}
        """
        try:
            if not plan.get("requires_planning"):
                # Simple task - execute directly
                return {
                    "success": True,
                    "results": {"task": plan["task"], "status": "ready"},
                    "errors": [],
                }
            
            subtasks = plan.get("subtasks", [])
            if not subtasks:
                return {
                    "success": True,
                    "results": {},
                    "errors": [],
                }
            
            results = {}
            errors = []
            
            # Execute subtasks respecting dependencies
            completed = set()
            pending = {st["id"]: st for st in subtasks}
            
            while pending:
                # Find subtasks with met dependencies
                ready = [
                    st_id for st_id, st in pending.items()
                    if all(dep in completed for dep in st.get("dependencies", []))
                ]
                
                if not ready:
                    logger.error("Circular dependency detected in plan")
                    errors.append("Circular dependency in execution plan")
                    break
                
                # Execute ready subtasks
                for st_id in ready:
                    subtask = pending.pop(st_id)
                    result = await self._execute_subtask(subtask, results)
                    
                    if result["success"]:
                        completed.add(st_id)
                        results[st_id] = result["result"]
                    else:
                        errors.append(f"Subtask {st_id} failed: {result['error']}")
                        # Don't continue if critical subtask fails
                        if subtask.get("critical", False):
                            break
            
            success = len(errors) == 0
            logger.info(f"Plan execution: {len(completed)}/{len(subtasks)} subtasks completed")
            
            return {
                "success": success,
                "results": results,
                "errors": errors,
                "completion_rate": len(completed) / len(subtasks) if subtasks else 0,
            }
            
        except Exception as e:
            logger.error(f"Plan execution failed: {str(e)}")
            return {
                "success": False,
                "results": None,
                "errors": [str(e)],
            }
    
    async def _execute_subtask(
        self,
        subtask: dict,
        context: dict = None,
    ) -> Dict[str, Any]:
        """
        Execute a single subtask with retry logic.
        
        Args:
            subtask: Subtask definition
            context: Results from previous subtasks
            
        Returns:
            dict: {success, result, error}
        """
        context = context or {}
        retry_count = 0
        
        while retry_count <= self.max_retries:
            try:
                logger.info(f"Executing subtask: {subtask['title']} (attempt {retry_count + 1})")
                
                tool_name = subtask.get("tool")
                if not tool_name:
                    return {
                        "success": False,
                        "result": None,
                        "error": "No tool specified",
                    }
                
                # Call the tool
                result = await tool_registry.call_tool(
                    tool_name,
                    description=subtask.get("description", ""),
                    context=context,
                )
                
                if result["success"]:
                    self._log_execution(subtask, True, result["result"])
                    return result
                else:
                    raise Exception(result.get("error", "Tool execution failed"))
                    
            except asyncio.TimeoutError:
                logger.warning(f"Subtask timeout: {subtask['title']}")
                retry_count += 1
                if retry_count <= self.max_retries:
                    await asyncio.sleep(2 ** retry_count)  # Exponential backoff
                    continue
                else:
                    return {
                        "success": False,
                        "result": None,
                        "error": "Subtask timeout after retries",
                    }
                    
            except Exception as e:
                logger.warning(f"Subtask error: {str(e)} (attempt {retry_count + 1})")
                retry_count += 1
                
                if retry_count <= self.max_retries:
                    await asyncio.sleep(2 ** retry_count)
                    continue
                else:
                    # Final attempt failed, return error
                    self._log_execution(subtask, False, str(e))
                    return {
                        "success": False,
                        "result": None,
                        "error": f"{str(e)} (after {retry_count} retries)",
                    }
        
        return {
            "success": False,
            "result": None,
            "error": "Max retries exceeded",
        }
    
    async def execute_tool(
        self,
        tool_name: str,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Execute a single tool directly.
        
        Args:
            tool_name: Tool name
            **kwargs: Tool arguments
            
        Returns:
            dict: {success, result, error}
        """
        try:
            result = await tool_registry.call_tool(tool_name, **kwargs)
            return result
        except Exception as e:
            logger.error(f"Tool execution failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    def _log_execution(
        self,
        subtask: dict,
        success: bool,
        result: Any,
    ) -> None:
        """Log subtask execution."""
        self.execution_history.append({
            "timestamp": datetime.now().isoformat(),
            "subtask_id": subtask.get("id"),
            "title": subtask.get("title"),
            "success": success,
            "result": str(result)[:100],  # Truncate for logging
        })
    
    def get_execution_summary(self) -> Dict[str, Any]:
        """Get execution history summary."""
        if not self.execution_history:
            return {
                "total_tasks": 0,
                "successful": 0,
                "failed": 0,
                "success_rate": 0,
            }
        
        total = len(self.execution_history)
        successful = sum(1 for h in self.execution_history if h["success"])
        
        return {
            "total_tasks": total,
            "successful": successful,
            "failed": total - successful,
            "success_rate": successful / total if total > 0 else 0,
            "recent": self.execution_history[-10:],
        }


# Global instance
task_executor = TaskExecutor()
