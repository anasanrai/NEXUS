import sys
import io
import traceback
from typing import Dict, Any

class CodeTool:
    """Executes Python code in a controlled environment."""
    
    def __init__(self):
        pass

    async def run(self, code: str, globals_dict: Dict = None) -> Dict[str, Any]:
        """Runs Python code and captures stdout/stderr."""
        if globals_dict is None:
            globals_dict = {}
            
        stdout = io.StringIO()
        stderr = io.StringIO()
        
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        
        sys.stdout = stdout
        sys.stderr = stderr
        
        try:
            exec(code, globals_dict)
            return {
                "status": "success",
                "output": stdout.getvalue(),
                "error": stderr.getvalue()
            }
        except Exception:
            return {
                "status": "exception",
                "output": stdout.getvalue(),
                "error": traceback.format_exc()
            }
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
