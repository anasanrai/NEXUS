import json
import os
from typing import Dict, Any, List
from pathlib import Path

class LongTermMemory:
    """Manages persistent data storage via JSON files (expandable to DB)."""
    
    def __init__(self, storage_path: str = "memory_store"):
        self.storage_dir = Path(storage_path)
        self.storage_dir.mkdir(exist_ok=True)

    def save_fact(self, key: str, value: Any):
        """Persists a fact or data point."""
        file_path = self.storage_dir / f"{key}.json"
        with open(file_path, 'w') as f:
            json.dump({"data": value}, f)

    def get_fact(self, key: str) -> Any:
        """Retrieves a persistent fact."""
        file_path = self.storage_dir / f"{key}.json"
        if file_path.exists():
            with open(file_path, 'r') as f:
                return json.load(f).get("data")
        return None

    def list_keys(self) -> List[str]:
        """Lists all stored fact keys."""
        return [f.stem for f in self.storage_dir.glob("*.json")]
