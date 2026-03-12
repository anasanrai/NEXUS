"""
Dynamic Tool Registry for NEXUS
Manages registration, retrieval, and installation of tools.
"""

import logging
import importlib
from typing import Callable, Dict, Any, List, Optional

logger = logging.getLogger(__name__)


class ToolRegistry:
    """Registry for managing all available tools."""
    
    def __init__(self):
        """Initialize the tool registry."""
        self.tools: Dict[str, Dict[str, Any]] = {}
    
    def register_tool(
        self,
        name: str,
        function: Callable,
        description: str,
        parameters: Optional[Dict[str, Any]] = None,
        required: Optional[List[str]] = None,
    ) -> bool:
        """
        Register a new tool.
        
        Args:
            name: Tool name
            function: Callable function
            description: Tool description
            parameters: Parameter schema
            required: Required parameter names
            
        Returns:
            bool: Success status
        """
        try:
            self.tools[name] = {
                "function": function,
                "description": description,
                "parameters": parameters or {},
                "required": required or [],
            }
            logger.info(f"Tool registered: {name}")
            return True
        except Exception as e:
            logger.error(f"Failed to register tool {name}: {str(e)}")
            return False
    
    def get_tool(self, name: str) -> Optional[Callable]:
        """
        Get a tool by name.
        
        Args:
            name: Tool name
            
        Returns:
            Callable: Tool function or None
        """
        return self.tools.get(name, {}).get("function")
    
    def get_tool_info(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get tool information.
        
        Args:
            name: Tool name
            
        Returns:
            dict: Tool information
        """
        return self.tools.get(name)
    
    def list_tools(self) -> List[str]:
        """
        List all registered tools.
        
        Returns:
            List[str]: Tool names
        """
        return list(self.tools.keys())
    
    def list_tools_detailed(self) -> List[Dict[str, Any]]:
        """
        List all tools with details.
        
        Returns:
            List[dict]: Detailed tool information
        """
        return [
            {
                "name": name,
                "description": info["description"],
                "parameters": info["parameters"],
                "required": info["required"],
            }
            for name, info in self.tools.items()
        ]
    
    async def call_tool(self, name: str, **kwargs) -> Dict[str, Any]:
        """
        Call a registered tool.
        
        Args:
            name: Tool name
            **kwargs: Tool arguments
            
        Returns:
            dict: {success, result, error}
        """
        try:
            tool_func = self.get_tool(name)
            if not tool_func:
                return {
                    "success": False,
                    "result": None,
                    "error": f"Tool '{name}' not found",
                }
            
            # Check if async
            import asyncio
            import inspect
            
            if inspect.iscoroutinefunction(tool_func):
                result = await tool_func(**kwargs)
            else:
                result = tool_func(**kwargs)
            
            return {
                "success": True,
                "result": result,
                "error": None,
            }
        except Exception as e:
            logger.error(f"Tool execution failed: {name} - {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    def remove_tool(self, name: str) -> bool:
        """
        Remove a tool from registry.
        
        Args:
            name: Tool name
            
        Returns:
            bool: Success status
        """
        if name in self.tools:
            del self.tools[name]
            logger.info(f"Tool removed: {name}")
            return True
        return False
    
    async def install_tool(
        self,
        package: str,
        tool_name: str,
        module_path: str,
        function_name: str,
    ) -> bool:
        """
        Install a tool package and register it.
        
        Args:
            package: Package name for pip install
            tool_name: Tool name for registry
            module_path: Module import path
            function_name: Function name to import
            
        Returns:
            bool: Success status
        """
        try:
            from tools.installer import install_package
            
            # Install package
            install_result = await install_package(package)
            if not install_result["success"]:
                logger.error(f"Package installation failed: {package}")
                return False
            
            # Import and register
            module = importlib.import_module(module_path)
            tool_func = getattr(module, function_name)
            
            description = getattr(tool_func, "__doc__", f"Auto-installed tool: {tool_name}")
            self.register_tool(tool_name, tool_func, description)
            
            logger.info(f"Tool installed and registered: {tool_name}")
            return True
            
        except Exception as e:
            logger.error(f"Tool installation failed: {str(e)}")
            return False


async def initialize_tool_registry() -> ToolRegistry:
    """
    Initialize and populate the tool registry with all available tools.
    
    Returns:
        ToolRegistry: Initialized registry with all tools
    """
    registry = ToolRegistry()
    
    tools_to_register = [
        # Search tools
        ("web_search", "tools.search", "web_search", "Search the web for information"),
        ("news_search", "tools.search", "news_search", "Search for news articles"),
        # Browser tools
        ("navigate", "tools.browser", "navigate", "Navigate to a URL"),
        ("screenshot", "tools.browser", "screenshot", "Take screenshot of URL"),
        # Shell tools
        ("run_command", "tools.shell", "run_command", "Execute shell command"),
        ("install_package", "tools.shell", "install_package", "Install package"),
        # Git tools
        ("git_clone", "tools.git", "clone", "Clone git repository"),
        ("git_commit_push", "tools.git", "commit_push", "Commit and push to git"),
        # File tools
        ("read_file", "tools.files", "read_file", "Read file contents"),
        ("write_file", "tools.files", "write_file", "Write to file"),
        # Code tools
        ("parse_code", "tools.code", "parse_code", "Parse and analyze code"),
        ("lint_code", "tools.code", "lint_code", "Lint code for errors"),
        # n8n tools
        ("list_workflows", "tools.n8n", "list_workflows", "List n8n workflows"),
        ("get_workflow", "tools.n8n", "get_workflow", "Get workflow details"),
        # Vercel tools
        ("list_deployments", "tools.vercel", "list_deployments", "List Vercel deployments"),
        ("get_deployment_status", "tools.vercel", "get_status", "Get deployment status"),
        # WordPress tools
        ("wordpress_create_post", "tools.wordpress", "create_post", "Create WordPress post"),
        ("wordpress_get_posts", "tools.wordpress", "get_posts", "Get WordPress posts"),
        # Social media tools
        ("post_twitter", "tools.social", "post_twitter", "Post to Twitter"),
        ("post_linkedin", "tools.social", "post_linkedin", "Post to LinkedIn"),
        ("post_instagram", "tools.social", "post_instagram", "Post to Instagram"),
        # Media tools
        ("generate_image", "tools.media", "generate_image", "Generate image from prompt"),
        ("text_to_speech", "tools.media", "text_to_speech", "Convert text to speech"),
        # Email tools
        ("send_email", "tools.email_tool", "send_email", "Send email"),
        # Calendar tools
        ("create_event", "tools.calendar_tool", "create_event", "Create calendar event"),
        # Payment tools
        ("create_payment_intent", "tools.payments", "create_payment_intent", "Create payment"),
        # Installer tools
        ("install_pip", "tools.installer", "install_pip", "Install pip package"),
        ("install_npm", "tools.installer", "install_npm", "Install npm package"),
    ]
    
    for tool_name, module_path, func_name, description in tools_to_register:
        try:
            module = importlib.import_module(module_path)
            func = getattr(module, func_name, None)
            if func:
                registry.register_tool(tool_name, func, description)
                logger.info(f"Registered tool: {tool_name}")
            else:
                logger.warning(f"Function {func_name} not found in {module_path}")
        except ImportError as e:
            logger.warning(f"Could not import {module_path}: {str(e)}")
        except Exception as e:
            logger.warning(f"Could not register {tool_name}: {str(e)}")
    
    return registry


# Global registry instance
tool_registry = ToolRegistry()
