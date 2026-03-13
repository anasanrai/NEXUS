import os
import shutil
from typing import Dict, Any, List
from pathlib import Path

class FilesTool:
    """Manages file and directory operations."""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path).resolve()

    async def run(self, action: str, **kwargs) -> Dict[str, Any]:
        """
        Executes a file operation.
        Supported actions: 'list', 'read', 'write', 'delete', 'mkdir'
        """
        try:
            if action == 'list':
                path = self.base_path / kwargs.get('path', '.')
                return {"files": [f.name for f in path.iterdir()]}
            
            elif action == 'read':
                path = self.base_path / kwargs.get('path')
                with open(path, 'r') as f:
                    return {"content": f.read()}
            
            elif action == 'write':
                path = self.base_path / kwargs.get('path')
                content = kwargs.get('content', '')
                path.parent.mkdir(parents=True, exist_ok=True)
                with open(path, 'w') as f:
                    f.write(content)
                return {"status": "success"}
            
            elif action == 'delete':
                path = self.base_path / kwargs.get('path')
                if path.is_file():
                    path.unlink()
                elif path.is_dir():
                    shutil.rmtree(path)
                return {"status": "deleted"}
                
            return {"error": f"Unknown action: {action}"}
            
        except Exception as e:
            return {"error": str(e)}
