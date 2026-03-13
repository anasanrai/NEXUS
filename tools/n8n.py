import requests
from typing import Dict, Any
from config import settings

class N8nTool:
    """Interacts with n8n workflow automation API."""
    
    def __init__(self):
        self.api_key = settings.N8N_API_KEY
        self.base_url = "http://localhost:5678/api/v1" # Default local n8n

    async def run(self, action: str, **kwargs) -> Dict[str, Any]:
        """
        Executes an n8n operation.
        Supported actions: 'list_workflows', 'trigger_workflow', 'get_execution'
        """
        if not self.api_key:
            return {"error": "N8N_API_KEY not configured"}

        headers = {"X-N8N-API-KEY": self.api_key}
        
        try:
            if action == 'list_workflows':
                response = requests.get(f"{self.base_url}/workflows", headers=headers)
                return response.json()
            
            elif action == 'trigger_workflow':
                workflow_id = kwargs.get('workflow_id')
                response = requests.post(
                    f"{self.base_url}/workflows/{workflow_id}/execute", 
                    headers=headers,
                    json=kwargs.get('data', {})
                )
                return response.json()
                
            return {"error": f"Unknown action: {action}"}
            
        except Exception as e:
            return {"error": str(e)}
