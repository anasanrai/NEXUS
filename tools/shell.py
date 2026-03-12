"""
Shell Command Execution Tool
Execute shell commands and manage packages.
"""

import logging
import subprocess
import asyncio
from typing import Dict, Any, Optional, Tuple

logger = logging.getLogger(__name__)


class ShellTool:
    """Shell command execution functionality."""
    
    @staticmethod
    async def run_command(
        cmd: str,
        timeout: int = 30,
        shell: bool = True,
    ) -> Dict[str, Any]:
        """
        Run a shell command.
        
        Args:
            cmd: Command to run
            timeout: Timeout in seconds
            shell: Use shell execution
            
        Returns:
            dict: {success, result, error, exit_code}
        """
        try:
            process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout,
                )
            except asyncio.TimeoutError:
                process.kill()
                logger.error(f"Command timeout: {cmd}")
                return {
                    "success": False,
                    "result": None,
                    "error": "Command timeout",
                    "exit_code": -1,
                }
            
            stdout_str = stdout.decode("utf-8", errors="ignore")
            stderr_str = stderr.decode("utf-8", errors="ignore")
            
            return {
                "success": process.returncode == 0,
                "result": stdout_str,
                "error": stderr_str if process.returncode != 0 else None,
                "exit_code": process.returncode,
            }
            
        except Exception as e:
            logger.error(f"Command execution failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
                "exit_code": -1,
            }
    
    @staticmethod
    def run_command_sync(
        cmd: str,
        timeout: int = 30,
    ) -> Dict[str, Any]:
        """
        Run a shell command synchronously.
        
        Args:
            cmd: Command to run
            timeout: Timeout in seconds
            
        Returns:
            dict: {success, result, error, exit_code}
        """
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                timeout=timeout,
                text=True,
            )
            
            return {
                "success": result.returncode == 0,
                "result": result.stdout,
                "error": result.stderr if result.returncode != 0 else None,
                "exit_code": result.returncode,
            }
            
        except subprocess.TimeoutExpired:
            logger.error(f"Command timeout: {cmd}")
            return {
                "success": False,
                "result": None,
                "error": "Command timeout",
                "exit_code": -1,
            }
        except Exception as e:
            logger.error(f"Command execution failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
                "exit_code": -1,
            }
    
    @staticmethod
    async def install_package(
        package: str,
        manager: str = "pip",
    ) -> Dict[str, Any]:
        """
        Install a package using pip, npm, or apt.
        
        Args:
            package: Package name
            manager: Package manager (pip, npm, apt)
            
        Returns:
            dict: {success, result, error}
        """
        cmd_map = {
            "pip": f"pip install {package}",
            "npm": f"npm install {package}",
            "apt": f"sudo apt-get install -y {package}",
        }
        
        cmd = cmd_map.get(manager, f"pip install {package}")
        result = await ShellTool.run_command(cmd, timeout=120)
        
        return {
            "success": result["success"],
            "result": f"Installed {package}" if result["success"] else None,
            "error": result["error"],
        }
    
    @staticmethod
    async def get_file_list(directory: str = ".") -> Dict[str, Any]:
        """
        List files in directory.
        
        Args:
            directory: Directory path
            
        Returns:
            dict: {success, result, error}
        """
        result = await ShellTool.run_command(f"ls -la {directory}")
        return result
    
    @staticmethod
    async def check_command_exists(cmd: str) -> bool:
        """
        Check if command exists.
        
        Args:
            cmd: Command name
            
        Returns:
            bool: Command exists
        """
        result = await ShellTool.run_command(f"command -v {cmd}")
        return result["success"]


# Global wrappers
async def run_command(cmd: str, timeout: int = 30) -> Dict[str, Any]:
    """Run shell command wrapper."""
    return await ShellTool.run_command(cmd, timeout)


async def install_package(package: str, manager: str = "pip") -> Dict[str, Any]:
    """Install package wrapper."""
    return await ShellTool.install_package(package, manager)
