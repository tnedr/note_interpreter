from typing import List

class BaseAgent:
    def run(self, notes: List[str], user_memory: List[str]):
        raise NotImplementedError 