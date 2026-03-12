"""
Vercel Deployment Management Tool
Manage deployments, logs, environment variables.
"""

import logging
from typing import Dict, Any, Optional
import httpx

from config import config

logger = logging.getLogger(__name__)


class VercelTool:
    """Vercel deployment management."""
    
    def __init__(self):
        """Initialize Vercel tool."""
        self.token = config.deployment.vercel_token
        self.project_id = config.deployment.vercel_project_id
        self.base_url = "https://api.vercel.com"
    
    def _headers(self) -> Dict[str, str]:
        """Get auth headers."""
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
    
    async def list_deployments(
        self,
        project: Optional[str] = None,
        limit: int = 10,
    ) -> Dict[str, Any]:
        """
        List deployments.
        
        Args:
            project: Project name/ID
            limit: Max results
            
        Returns:
            dict: {success, result, error}
        """
        try:
            project = project or self.project_id
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/v6/deployments",
                    headers=self._headers(),
                    params={"projectId": project, "limit": limit},
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
                "result": response.json().get("deployments", []),
                "error": None,
            }
        except Exception as e:
            logger.error(f"List deployments failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    async def get_status(self, project: Optional[str] = None) -> Dict[str, Any]:
        """
        Get project status.
        
        Args:
            project: Project name/ID
            
        Returns:
            dict: {success, result, error}
        """
        try:
            project = project or self.project_id
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/v9/projects/{project}",
                    headers=self._headers(),
                    timeout=15,
                )
            
            if response.status_code != 200:
                return {
                    "success": False,
                    "result": None,
                    "error": f"API error: {response.status_code}",
                }
            
            data = response.json()
            return {
                "success": True,
                "result": {
                    "name": data.get("name"),
                    "status": "active",
                    "domains": data.get("alias", []),
                },
                "error": None,
            }
        except Exception as e:
            logger.error(f"Get status failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    async def trigger_deploy(self, project: Optional[str] = None) -> Dict[str, Any]:
        """
        Trigger deployment.
        
        Args:
            project: Project name/ID
            
        Returns:
            dict: {success, result, error}
        """
        try:
            project = project or self.project_id
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/v12/deployments",
                    headers=self._headers(),
                    json={"projectId": project},
                    timeout=30,
                )
            
            if response.status_code not in [200, 201]:
                return {
                    "success": False,
                    "result": None,
                    "error": f"API error: {response.status_code}",
                }
            
            result = response.json()
            logger.info(f"Deployment triggered: {result.get('uid')}")
            
            return {
                "success": True,
                "result": {
                    "deployment_id": result.get("uid"),
                    "status": result.get("state"),
                },
                "error": None,
            }
        except Exception as e:
            logger.error(f"Trigger deploy failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    async def get_logs(self, deployment_id: str) -> Dict[str, Any]:
        """
        Get deployment logs.
        
        Args:
            deployment_id: Deployment ID
            
        Returns:
            dict: {success, result, error}
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/v12/deployments/{deployment_id}/builds",
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
            logger.error(f"Get logs failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    async def set_env(
        self,
        project: Optional[str] = None,
        key: str = "",
        value: str = "",
    ) -> Dict[str, Any]:
        """
        Set environment variable.
        
        Args:
            project: Project name/ID
            key: Env var key
            value: Env var value
            
        Returns:
            dict: {success, result, error}
        """
        try:
            project = project or self.project_id
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/v9/projects/{project}/env",
                    headers=self._headers(),
                    json={"key": key, "value": value, "target": ["production"]},
                    timeout=15,
                )
            
            if response.status_code not in [200, 201]:
                return {
                    "success": False,
                    "result": None,
                    "error": f"API error: {response.status_code}",
                }
            
            logger.info(f"Env var set: {key}")
            return {
                "success": True,
                "result": f"Set {key}",
                "error": None,
            }
        except Exception as e:
            logger.error(f"Set env failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }


# Global instance
vercel_tool = VercelTool()
