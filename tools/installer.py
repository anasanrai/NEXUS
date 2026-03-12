"""
Package Installer Tool
Self-expand by installing packages on demand.
"""

import logging
import subprocess
from typing import Dict, Any

logger = logging.getLogger(__name__)


class InstallerTool:
    """Package installation and management."""
    
    @staticmethod
    async def install_pip(package: str) -> Dict[str, Any]:
        """
        Install Python package via pip.
        
        Args:
            package: Package name
            
        Returns:
            dict: {success, result, error}
        """
        try:
            result = subprocess.run(
                ["pip", "install", package],
                capture_output=True,
                timeout=120,
                text=True,
            )
            
            if result.returncode != 0:
                logger.error(f"Pip install failed: {result.stderr}")
                return {
                    "success": False,
                    "result": None,
                    "error": result.stderr,
                }
            
            logger.info(f"Package installed: {package}")
            return {
                "success": True,
                "result": f"Installed {package}",
                "error": None,
            }
        except subprocess.TimeoutExpired:
            logger.error(f"Install timeout: {package}")
            return {
                "success": False,
                "result": None,
                "error": "Installation timeout",
            }
        except Exception as e:
            logger.error(f"Install failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    @staticmethod
    async def install_npm(package: str) -> Dict[str, Any]:
        """
        Install Node package via npm.
        
        Args:
            package: Package name
            
        Returns:
            dict: {success, result, error}
        """
        try:
            result = subprocess.run(
                ["npm", "install", "-g", package],
                capture_output=True,
                timeout=120,
                text=True,
            )
            
            if result.returncode != 0:
                logger.error(f"Npm install failed: {result.stderr}")
                return {
                    "success": False,
                    "result": None,
                    "error": result.stderr,
                }
            
            logger.info(f"Package installed: {package}")
            return {
                "success": True,
                "result": f"Installed {package}",
                "error": None,
            }
        except subprocess.TimeoutExpired:
            logger.error(f"Install timeout: {package}")
            return {
                "success": False,
                "result": None,
                "error": "Installation timeout",
            }
        except Exception as e:
            logger.error(f"Install failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    @staticmethod
    async def install_apt(package: str) -> Dict[str, Any]:
        """
        Install system package via apt.
        
        Args:
            package: Package name
            
        Returns:
            dict: {success, result, error}
        """
        try:
            result = subprocess.run(
                ["sudo", "apt-get", "install", "-y", package],
                capture_output=True,
                timeout=180,
                text=True,
            )
            
            if result.returncode != 0:
                logger.error(f"Apt install failed: {result.stderr}")
                return {
                    "success": False,
                    "result": None,
                    "error": result.stderr,
                }
            
            logger.info(f"Package installed: {package}")
            return {
                "success": True,
                "result": f"Installed {package}",
                "error": None,
            }
        except subprocess.TimeoutExpired:
            logger.error(f"Install timeout: {package}")
            return {
                "success": False,
                "result": None,
                "error": "Installation timeout",
            }
        except Exception as e:
            logger.error(f"Install failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    @staticmethod
    async def check_installed(package: str) -> Dict[str, Any]:
        """
        Check if package is installed.
        
        Args:
            package: Package name
            
        Returns:
            dict: {success (installed), result, error}
        """
        try:
            result = subprocess.run(
                ["pip", "show", package],
                capture_output=True,
                timeout=10,
                text=True,
            )
            
            installed = result.returncode == 0
            return {
                "success": installed,
                "result": "Installed" if installed else "Not installed",
                "error": None,
            }
        except Exception as e:
            logger.error(f"Check installed failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    @staticmethod
    async def uninstall_pip(package: str) -> Dict[str, Any]:
        """
        Uninstall Python package.
        
        Args:
            package: Package name
            
        Returns:
            dict: {success, result, error}
        """
        try:
            result = subprocess.run(
                ["pip", "uninstall", "-y", package],
                capture_output=True,
                timeout=120,
                text=True,
            )
            
            if result.returncode != 0:
                logger.error(f"Uninstall failed: {result.stderr}")
                return {
                    "success": False,
                    "result": None,
                    "error": result.stderr,
                }
            
            logger.info(f"Package uninstalled: {package}")
            return {
                "success": True,
                "result": f"Uninstalled {package}",
                "error": None,
            }
        except Exception as e:
            logger.error(f"Uninstall failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }


# Global wrappers
async def install_pip(package: str) -> Dict[str, Any]:
    """Install pip package wrapper."""
    return await InstallerTool.install_pip(package)


async def install_npm(package: str) -> Dict[str, Any]:
    """Install npm package wrapper."""
    return await InstallerTool.install_npm(package)
