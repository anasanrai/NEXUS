import git
from typing import Dict, Any
from pathlib import Path
from config import settings

class GitTool:
    """Manages Git repository operations."""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path).resolve()
        try:
            self.repo = git.Repo(self.repo_path)
        except git.InvalidGitRepositoryError:
            self.repo = None

    async def run(self, action: str, **kwargs) -> Dict[str, Any]:
        """
        Executes a Git operation.
        Supported actions: 'status', 'add', 'commit', 'push', 'pull', 'clone'
        """
        try:
            if action == 'clone':
                url = kwargs.get('url')
                to_path = kwargs.get('to_path')
                git.Repo.clone_from(url, to_path)
                return {"status": "cloned", "url": url}

            if not self.repo:
                return {"error": "Not a git repository"}

            if action == 'status':
                return {"status": self.repo.git.status()}
            
            elif action == 'add':
                files = kwargs.get('files', '.')
                self.repo.git.add(files)
                return {"status": "added", "files": files}
            
            elif action == 'commit':
                message = kwargs.get('message', 'Automatic commit by NEXUS')
                self.repo.git.commit('-m', message)
                return {"status": "committed", "message": message}
            
            elif action == 'push':
                origin = self.repo.remote(name='origin')
                origin.push()
                return {"status": "pushed"}
                
            return {"error": f"Unknown action: {action}"}
            
        except Exception as e:
            return {"error": str(e)}
