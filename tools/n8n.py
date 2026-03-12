"""
n8n Workflow Management Tool
Create, update, debug and manage n8n workflows.
"""

import logging
from typing import Dict, Any, Optional, List
import httpx

from config import config

logger = logging.getLogger(__name__)


class N8nTool:
    """n8n workflow management."""
    
    def __init__(self):
        """Initialize n8n tool."""
        self.base_url = config.workflow.n8n_url.rstrip("/")
        self.api_key = config.workflow.n8n_api_key
    
    def _headers(self) -> Dict[str, str]:
        """Get auth headers."""
        return {
            "X-N8N-API-KEY": self.api_key,
            "Content-Type": "application/json",
        }
    
    async def list_workflows(self) -> Dict[str, Any]:
        """
        List all workflows.
        
        Returns:
            dict: {success, result, error}
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/api/v1/workflows",
                    headers=self._headers(),
                    timeout=15,
                )
            
            if response.status_code != 200:
                return {
                    "success": False,
                    "result": None,
                    "error": f"API error: {response.status_code}",
                }
            
            workflows = response.json().get("data", [])
            return {
                "success": True,
                "result": workflows,
                "error": None,
            }
        except Exception as e:
            logger.error(f"List workflows failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    async def get_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """
        Get workflow details.
        
        Args:
            workflow_id: Workflow ID
            
        Returns:
            dict: {success, result, error}
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/api/v1/workflows/{workflow_id}",
                    headers=self._headers(),
                    timeout=15,
                )
            
            if response.status_code != 200:
                return {
                    "success": False,
                    "result": None,
                    "error": f"API error: {response.status_code}",
                }
            
            return {
                "success": True,
                "result": response.json(),
                "error": None,
            }
        except Exception as e:
            logger.error(f"Get workflow failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    async def create_workflow(self, definition: dict) -> Dict[str, Any]:
        """
        Create new workflow.
        
        Args:
            definition: Workflow JSON definition
            
        Returns:
            dict: {success, result, error}
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/v1/workflows",
                    headers=self._headers(),
                    json=definition,
                    timeout=15,
                )
            
            if response.status_code not in [200, 201]:
                return {
                    "success": False,
                    "result": None,
                    "error": f"API error: {response.status_code}",
                }
            
            logger.info("Workflow created")
            return {
                "success": True,
                "result": response.json(),
                "error": None,
            }
        except Exception as e:
            logger.error(f"Create workflow failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    async def activate_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """
        Activate workflow.
        
        Args:
            workflow_id: Workflow ID
            
        Returns:
            dict: {success, result, error}
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.patch(
                    f"{self.base_url}/api/v1/workflows/{workflow_id}",
                    headers=self._headers(),
                    json={"active": True},
                    timeout=15,
                )
            
            if response.status_code != 200:
                return {
                    "success": False,
                    "result": None,
                    "error": f"API error: {response.status_code}",
                }
            
            logger.info(f"Workflow activated: {workflow_id}")
            return {
                "success": True,
                "result": "Activated",
                "error": None,
            }
        except Exception as e:
            logger.error(f"Activate workflow failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    async def get_executions(self, workflow_id: str, limit: int = 10) -> Dict[str, Any]:
        """
        Get workflow executions.
        
        Args:
            workflow_id: Workflow ID
            limit: Max results
            
        Returns:
            dict: {success, result, error}
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/api/v1/workflows/{workflow_id}/executions",
                    headers=self._headers(),
                    params={"limit": limit},
                    timeout=15,
                )
            
            if response.status_code != 200:
                return {
                    "success": False,
                    "result": None,
                    "error": f"API error: {response.status_code}",
                }
            
            return {
                "success": True,
                "result": response.json(),
                "error": None,
            }
        except Exception as e:
            logger.error(f"Get executions failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }


# Global instance
n8n_tool = N8nTool()


async def list_workflows() -> Dict[str, Any]:
    """List workflows wrapper."""
    return await n8n_tool.list_workflows()


async def get_workflow(workflow_id: str) -> Dict[str, Any]:
    """Get workflow wrapper."""
    return await n8n_tool.get_workflow(workflow_id)
