from typing import Dict, Any, List, Optional
import logging

class ToolRegistry:
    """Manages the lifecycle and discovery of available tools."""
    
    def __init__(self):
        self.tools: Dict[str, Any] = {}
        self.logger = logging.getLogger("nexus.tools")
        self._register_builtins()

    def _register_builtins(self):
        """Initializes internal tools."""
        # This will be populated as tools are created
        pass

    def register(self, name: str, tool_instance: Any):
        """Adds a new tool to the registry."""
        self.tools[name] = tool_instance
        self.logger.info(f"Registered tool: {name}")

    def get_tool(self, name: str) -> Optional[Any]:
        """Retrieves a tool by name."""
        return self.tools.get(name)

    def list_tools(self) -> List[str]:
        """Returns a list of all registered tool names."""
        return list(self.tools.keys())
