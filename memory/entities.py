from typing import Dict, Any, List
import time

class EntityManager:
    """Tracks and manages entities discovered during conversations."""
    
    def __init__(self):
        self.entities: Dict[str, Dict[str, Any]] = {}

    def track_entity(self, name: str, properties: Dict[str, Any]):
        """Creates or updates an entity profile."""
        if name not in self.entities:
            self.entities[name] = {
                "first_seen": time.time(),
                "mentions": 0,
                "properties": {}
            }
        
        self.entities[name]["properties"].update(properties)
        self.entities[name]["mentions"] += 1
        self.entities[name]["last_seen"] = time.time()

    def get_entity(self, name: str) -> Dict[str, Any]:
        """Retrieves an entity's profile."""
        return self.entities.get(name, {})

    def list_entities(self) -> List[str]:
        """Returns all tracked entity names."""
        return list(self.entities.keys())
