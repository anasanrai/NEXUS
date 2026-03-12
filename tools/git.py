"""
Git Tool for version control operations
Clone, commit, push and manage GitHub repositories.
"""

import logging
from typing import Dict, Any, Optional
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)


class GitTool:
    """Git operations for version control."""
    
    def __init__(self, token: str = ""):
        """
        Initialize Git tool.
        
        Args:
            token: GitHub access token
        """
        self.token = token
    
    @staticmethod
    def clone(repo_url: str, path: str) -> Dict[str, Any]:
        """
        Clone a repository.
        
        Args:
            repo_url: Repository URL
            path: Local path
            
        Returns:
            dict: {success, result, error}
        """
        try:
            import git
            git.Repo.clone_from(repo_url, path)
            logger.info(f"Repository cloned: {repo_url}")
            return {
                "success": True,
                "result": f"Cloned to {path}",
                "error": None,
            }
        except Exception as e:
            logger.error(f"Clone failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    @staticmethod
    def commit_push(
        path: str,
        message: str,
        branch: str = "main",
    ) -> Dict[str, Any]:
        """
        Commit and push changes.
        
        Args:
            path: Repository path
            message: Commit message
            branch: Branch name
            
        Returns:
            dict: {success, result, error}
        """
        try:
            import git
            repo = git.Repo(path)
            repo.index.add(A=True)
            repo.index.commit(message)
            repo.remotes.origin.push(branch)
            
            logger.info(f"Pushed to {branch}")
            return {
                "success": True,
                "result": f"Pushed: {message}",
                "error": None,
            }
        except Exception as e:
            logger.error(f"Commit/Push failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    @staticmethod
    def read_file(path: str, file_path: str) -> Dict[str, Any]:
        """
        Read file from repository.
        
        Args:
            path: Repository path
            file_path: File path in repo
            
        Returns:
            dict: {success, result, error}
        """
        try:
            full_path = Path(path) / file_path
            with open(full_path, "r") as f:
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
    def write_file(path: str, file_path: str, content: str) -> Dict[str, Any]:
        """
        Write file to repository.
        
        Args:
            path: Repository path
            file_path: File path in repo
            content: File content
            
        Returns:
            dict: {success, result, error}
        """
        try:
            full_path = Path(path) / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, "w") as f:
                f.write(content)
            logger.info(f"File written: {file_path}")
            return {
                "success": True,
                "result": f"Written {file_path}",
                "error": None,
            }
        except Exception as e:
            logger.error(f"Write file failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    def create_pr(
        self,
        repo: str,
        title: str,
        body: str,
        head: str = "develop",
        base: str = "main",
    ) -> Dict[str, Any]:
        """
        Create pull request on GitHub.
        
        Args:
            repo: Repo name (owner/repo)
            title: PR title
            body: PR description
            head: Head branch
            base: Base branch
            
        Returns:
            dict: {success, result, error}
        """
        try:
            import httpx
            
            url = f"https://api.github.com/repos/{repo}/pulls"
            headers = {
                "Authorization": f"token {self.token}",
                "Accept": "application/vnd.github.v3+json",
            }
            
            data = {
                "title": title,
                "body": body,
                "head": head,
                "base": base,
            }
            
            response = httpx.post(url, headers=headers, json=data, timeout=15)
            
            if response.status_code not in [200, 201]:
                return {
                    "success": False,
                    "result": None,
                    "error": f"GitHub API error: {response.status_code}",
                }
            
            pr_data = response.json()
            logger.info(f"PR created: {pr_data['html_url']}")
            
            return {
                "success": True,
                "result": {
                    "pr_number": pr_data["number"],
                    "url": pr_data["html_url"],
                },
                "error": None,
            }
        except Exception as e:
            logger.error(f"Create PR failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }


# Global wrappers
def clone(repo_url: str, path: str) -> Dict[str, Any]:
    """Clone repository wrapper."""
    return GitTool.clone(repo_url, path)


def commit_push(path: str, message: str, branch: str = "main") -> Dict[str, Any]:
    """Commit and push wrapper."""
    return GitTool.commit_push(path, message, branch)
