from collections import deque
from typing import Deque, List, Dict


class ConversationMemory:
    """
    Short-term conversation memory (last N turns)
    """

    def __init__(self, max_turns: int = 5):
        self.max_turns = max_turns
        self.history: Deque[Dict[str, str]] = deque(maxlen=max_turns)

    def add_turn(self, user_query: str, assistant_response: str):
        self.history.append({
            "user": user_query,
            "assistant": assistant_response
        })

    def get_memory(self) -> List[Dict[str, str]]:
        return list(self.history)

    def clear(self):
        self.history.clear()
