"""
File Management Tool
Read, write, delete and manipulate files.
"""

import logging
from typing import Dict, Any
from pathlib import Path
import json
import yaml

logger = logging.getLogger(__name__)


class FilesTool:
    """File operations."""
    
    @staticmethod
    def read_file(path: str) -> Dict[str, Any]:
        """
        Read file contents.
        
        Args:
            path: File path
            
        Returns:
            dict: {success, result, error}
        """
        try:
            with open(path, "r") as f:
                content = f.read()
            return {
                "success": True,
                "result": content,
                "error": None,
            }
        except Exception as e:
            logger.error(f"Read file failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    @staticmethod
    def write_file(path: str, content: str, append: bool = False) -> Dict[str, Any]:
        """
        Write to file.
        
        Args:
            path: File path
            content: File content
            append: Append instead of overwrite
            
        Returns:
            dict: {success, result, error}
        """
        try:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            mode = "a" if append else "w"
            with open(path, mode) as f:
                f.write(content)
            logger.info(f"File written: {path}")
            return {
                "success": True,
                "result": f"Written {path}",
                "error": None,
            }
        except Exception as e:
            logger.error(f"Write file failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    @staticmethod
    def delete_file(path: str) -> Dict[str, Any]:
        """
        Delete file.
        
        Args:
            path: File path
            
        Returns:
            dict: {success, result, error}
        """
        try:
            Path(path).unlink()
            logger.info(f"File deleted: {path}")
            return {
                "success": True,
                "result": f"Deleted {path}",
                "error": None,
            }
        except Exception as e:
            logger.error(f"Delete file failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    @staticmethod
    def list_directory(path: str = ".") -> Dict[str, Any]:
        """
        List directory contents.
        
        Args:
            path: Directory path
            
        Returns:
            dict: {success, result (list), error}
        """
        try:
            contents = [str(p.name) for p in Path(path).iterdir()]
            return {
                "success": True,
                "result": contents,
                "error": None,
            }
        except Exception as e:
            logger.error(f"List directory failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    @staticmethod
    def read_json(path: str) -> Dict[str, Any]:
        """
        Read JSON file.
        
        Args:
            path: File path
            
        Returns:
            dict: {success, result, error}
        """
        try:
            with open(path) as f:
                data = json.load(f)
            return {
                "success": True,
                "result": data,
                "error": None,
            }
        except Exception as e:
            logger.error(f"Read JSON failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    @staticmethod
    def write_json(path: str, data: dict) -> Dict[str, Any]:
        """
        Write JSON file.
        
        Args:
            path: File path
            data: Data to write
            
        Returns:
            dict: {success, result, error}
        """
        try:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            with open(path, "w") as f:
                json.dump(data, f, indent=2)
            logger.info(f"JSON written: {path}")
            return {
                "success": True,
                "result": f"Written {path}",
                "error": None,
            }
        except Exception as e:
            logger.error(f"Write JSON failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    @staticmethod
    def read_yaml(path: str) -> Dict[str, Any]:
        """
        Read YAML file.
        
        Args:
            path: File path
            
        Returns:
            dict: {success, result, error}
        """
        try:
            with open(path) as f:
                data = yaml.safe_load(f)
            return {
                "success": True,
                "result": data,
                "error": None,
            }
        except Exception as e:
            logger.error(f"Read YAML failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }


# Global wrappers
def read_file(path: str) -> Dict[str, Any]:
    """Read file wrapper."""
    return FilesTool.read_file(path)


def write_file(path: str, content: str, append: bool = False) -> Dict[str, Any]:
    """Write file wrapper."""
    return FilesTool.write_file(path, content, append)
