"""
Task Planner for NEXUS
Decomposes complex tasks into executable subtasks.
"""

import logging
from typing import List, Dict, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Subtask:
    """Represents a single subtask."""
    id: int
    title: str
    description: str
    tool_required: str
    dependencies: List[int]
    estimated_duration: int
    retry_count: int = 0
    status: str = "pending"
    result: Any = None


class TaskPlanner:
    """Plans and decomposes complex tasks."""
    
    def __init__(self):
        """Initialize planner."""
        self.subtask_id_counter = 0
    
    async def create_plan(self, task: str, context: dict = None) -> Dict[str, Any]:
        """
        Create execution plan for complex task.
        
        Args:
            task: Task description
            context: Additional context
            
        Returns:
            dict: {success, plan, error}
        """
        try:
            from agent.router import ModelRouter, TaskType
            
            router = ModelRouter()
            task_type = router.detect_task_type(task)
            
            if task_type == TaskType.SIMPLE:
                # Simple tasks don't need planning
                return {
                    "success": True,
                    "plan": {
                        "task": task,
                        "type": task_type.value,
                        "subtasks": [],
                        "requires_planning": False,
                    },
                    "error": None,
                }
            
            # For complex tasks, decompose
            subtasks = await self._decompose_task(task, context or {})
            
            plan = {
                "task": task,
                "type": task_type.value,
                "subtasks": [
                    {
                        "id": st.id,
                        "title": st.title,
                        "description": st.description,
                        "tool": st.tool_required,
                        "dependencies": st.dependencies,
                        "duration": st.estimated_duration,
                    }
                    for st in subtasks
                ],
                "requires_planning": True,
                "total_duration": sum(st.estimated_duration for st in subtasks),
            }
            
            logger.info(f"Plan created with {len(subtasks)} subtasks")
            return {
                "success": True,
                "plan": plan,
                "error": None,
            }
            
        except Exception as e:
            logger.error(f"Plan creation failed: {str(e)}")
            return {
                "success": False,
                "plan": None,
                "error": str(e),
            }
    
    async def _decompose_task(self, task: str, context: dict) -> List[Subtask]:
        """
        Decompose task into subtasks.
        
        Args:
            task: Task description
            context: Task context
            
        Returns:
            List[Subtask]: Subtasks
        """
        subtasks = []
        
        # Analyze task and determine subtasks
        task_lower = task.lower()
        
        # Web research tasks
        if any(kw in task_lower for kw in ["search", "research", "find", "lookup"]):
            subtasks.append(self._create_subtask(
                "Search Web",
                f"Search for: {task}",
                "web_search",
                [],
                5,
            ))
            subtasks.append(self._create_subtask(
                "Analyze Results",
                "Analyze and summarize search results",
                "analysis",
                [subtasks[-1].id] if subtasks else [],
                3,
            ))
        
        # Code tasks
        elif any(kw in task_lower for kw in ["code", "write", "debug", "fix"]):
            subtasks.append(self._create_subtask(
                "Code Analysis",
                "Analyze requirements",
                "code_analysis",
                [],
                5,
            ))
            subtasks.append(self._create_subtask(
                "Write Code",
                "Write implementation",
                "code_write",
                [subtasks[-1].id],
                15,
            ))
            subtasks.append(self._create_subtask(
                "Test Code",
                "Test and validate",
                "code_test",
                [subtasks[-1].id],
                10,
            ))
            if "push" in task_lower or "deploy" in task_lower:
                subtasks.append(self._create_subtask(
                    "Deploy",
                    "Push to git and deploy",
                    "git_push",
                    [subtasks[-1].id],
                    5,
                ))
        
        # Content tasks
        elif any(kw in task_lower for kw in ["post", "blog", "content", "article"]):
            subtasks.append(self._create_subtask(
                "Write Content",
                "Write blog post or content",
                "content_write",
                [],
                20,
            ))
            subtasks.append(self._create_subtask(
                "Format & Publish",
                "Format and publish post",
                "wordpress",
                [subtasks[-1].id],
                5,
            ))
        
        # Social media tasks
        elif any(kw in task_lower for kw in ["post", "twitter", "linkedin", "instagram"]):
            subtasks.append(self._create_subtask(
                "Prepare Content",
                "Prepare social media content",
                "content_prepare",
                [],
                5,
            ))
            subtasks.append(self._create_subtask(
                "Post to Social",
                f"Post to social media",
                "social_media",
                [subtasks[-1].id],
                3,
            ))
        
        # Default: single execution subtask
        if not subtasks:
            subtasks.append(self._create_subtask(
                "Execute Task",
                task,
                "general",
                [],
                10,
            ))
        
        return subtasks
    
    def _create_subtask(
        self,
        title: str,
        description: str,
        tool: str,
        dependencies: List[int],
        duration: int,
    ) -> Subtask:
        """Create a subtask."""
        self.subtask_id_counter += 1
        return Subtask(
            id=self.subtask_id_counter,
            title=title,
            description=description,
            tool_required=tool,
            dependencies=dependencies,
            estimated_duration=duration,
        )


# Global instance
task_planner = TaskPlanner()
