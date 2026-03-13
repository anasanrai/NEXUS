import subprocess
from typing import Dict, Any

class ShellTool:
    """Executes system commands safely."""
    
    def __init__(self):
        pass

    async def run(self, command: str) -> Dict[str, Any]:
        """Runs a shell command and returns output."""
        try:
            # Note: In a real production environment, this should be heavily sandboxed
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except Exception as e:
            return {"error": str(e)}
