"""
Code Management Tool
Edit code, debug, and manage Python/JavaScript files.
"""

import logging
import re
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class CodeTool:
    """Code manipulation and analysis."""
    
    @staticmethod
    def parse_code(code: str, language: str = "python") -> Dict[str, Any]:
        """
        Parse code structure.
        
        Args:
            code: Code content
            language: Programming language
            
        Returns:
            dict: {success, result, error}
        """
        try:
            import ast
            
            if language == "python":
                tree = ast.parse(code)
                functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
                classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
                
                return {
                    "success": True,
                    "result": {
                        "functions": functions,
                        "classes": classes,
                        "lines": len(code.split("\n")),
                    },
                    "error": None,
                }
            
            return {
                "success": False,
                "result": None,
                "error": "Unsupported language",
            }
        except Exception as e:
            logger.error(f"Parse code failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    @staticmethod
    def find_pattern(code: str, pattern: str) -> Dict[str, Any]:
        """
        Find regex pattern in code.
        
        Args:
            code: Code content
            pattern: Regex pattern
            
        Returns:
            dict: {success, result (matches), error}
        """
        try:
            matches = re.findall(pattern, code)
            return {
                "success": True,
                "result": matches,
                "error": None,
            }
        except Exception as e:
            logger.error(f"Find pattern failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    @staticmethod
    def replace_code(code: str, old: str, new: str) -> Dict[str, Any]:
        """
        Replace code section.
        
        Args:
            code: Original code
            old: Text to replace
            new: Replacement text
            
        Returns:
            dict: {success, result, error}
        """
        try:
            updated = code.replace(old, new)
            return {
                "success": True,
                "result": updated,
                "error": None,
            }
        except Exception as e:
            logger.error(f"Replace code failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    @staticmethod
    def lint_code(code: str, language: str = "python") -> Dict[str, Any]:
        """
        Lint code for syntax errors.
        
        Args:
            code: Code content
            language: Programming language
            
        Returns:
            dict: {success, result (errors), error}
        """
        try:
            import ast
            
            if language == "python":
                try:
                    ast.parse(code)
                    return {
                        "success": True,
                        "result": [],
                        "error": None,
                    }
                except SyntaxError as e:
                    return {
                        "success": False,
                        "result": [str(e)],
                        "error": str(e),
                    }
            
            return {
                "success": False,
                "result": None,
                "error": "Unsupported language",
            }
        except Exception as e:
            logger.error(f"Lint failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    @staticmethod
    def format_code(code: str, language: str = "python") -> Dict[str, Any]:
        """
        Format code with proper indentation.
        
        Args:
            code: Code content
            language: Programming language
            
        Returns:
            dict: {success, result (formatted), error}
        """
        try:
            if language == "python":
                import autopep8
                formatted = autopep8.fix_code(code)
                return {
                    "success": True,
                    "result": formatted,
                    "error": None,
                }
            
            return {
                "success": False,
                "result": None,
                "error": "Unsupported language",
            }
        except Exception as e:
            logger.error(f"Format code failed: {str(e)}")
            return {
                "success": False,
                "result": code,
                "error": str(e),
            }
    
    @staticmethod
    def add_docstring(code: str, docstring: str) -> Dict[str, Any]:
        """
        Add docstring to function/class.
        
        Args:
            code: Code content
            docstring: Docstring to add
            
        Returns:
            dict: {success, result, error}
        """
        try:
            lines = code.split("\n")
            insert_index = 0
            
            for i, line in enumerate(lines):
                if line.strip().startswith("def ") or line.strip().startswith("class "):
                    insert_index = i + 1
                    break
            
            indent = " " * 4
            doc_lines = [f'{indent}"""{docstring}"""']
            result_lines = lines[:insert_index] + doc_lines + lines[insert_index:]
            
            return {
                "success": True,
                "result": "\n".join(result_lines),
                "error": None,
            }
        except Exception as e:
            logger.error(f"Add docstring failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }


def parse_code(code: str, language: str = "python") -> Dict[str, Any]:
    """Parse code wrapper."""
    return CodeTool.parse_code(code, language)


def lint_code(code: str, language: str = "python") -> Dict[str, Any]:
    """Lint code wrapper."""
    return CodeTool.lint_code(code, language)
