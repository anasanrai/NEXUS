import subprocess
import sys
from typing import Dict, Any

class InstallerTool:
    """Manages installation of Python packages and system dependencies."""
    
    def __init__(self):
        pass

    async def run(self, package: str) -> Dict[str, Any]:
        """Installs a package using pip."""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", package],
                capture_output=True,
                text=True
            )
            return {
                "status": "success" if result.returncode == 0 else "error",
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        except Exception as e:
            return {"error": str(e)}
