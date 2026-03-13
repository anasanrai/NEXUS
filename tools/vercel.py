import requests
from typing import Dict, Any
import config

class VercelTool:
    """Manages Vercel deployments via API."""
    
    def __init__(self):
        self.token = config.VERCEL_TOKEN

    async def run(self, action: str, **kwargs) -> Dict[str, Any]:
        """
        Executes a Vercel operation.
        Supported actions: 'list_deployments', 'create_deployment', 'get_project'
        """
        if not self.token:
            return {"error": "VERCEL_TOKEN not configured"}

        headers = {"Authorization": f"Bearer {self.token}"}
        
        try:
            if action == 'list_deployments':
                response = requests.get("https://api.vercel.com/v6/deployments", headers=headers)
                return response.json()
            
            elif action == 'create_deployment':
                # Simplified deployment trigger
                response = requests.post(
                    "https://api.vercel.com/v13/deployments",
                    headers=headers,
                    json=kwargs.get('config', {})
                )
                return response.json()
                
            return {"error": f"Unknown action: {action}"}
            
        except Exception as e:
            return {"error": str(e)}
