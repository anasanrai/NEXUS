from typing import List, Dict, Any

class ShortTermMemory:
    """Manages volatile conversation history and context."""
    
    def __init__(self, limit: int = 50):
        self.history: List[Dict[str, str]] = []
        self.limit = limit

    def add_interaction(self, user_input: str, agent_output: str):
        """Adds a new exchange to the history."""
        self.history.append({"role": "user", "content": user_input})
        self.history.append({"role": "assistant", "content": agent_output})
        
        # Enforce limit
        if len(self.history) > self.limit * 2:
            self.history = self.history[-(self.limit * 2):]

    def get_history(self) -> List[Dict[str, str]]:
        """Returns the current conversation matches."""
        return self.history

    def clear(self):
        """Wipes the short-term memory."""
        self.history = []
