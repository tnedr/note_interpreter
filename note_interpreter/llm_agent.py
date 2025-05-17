from typing import List, Optional
from note_interpreter.models import LLMOutput, DataEntry

class LLMAgent:
    """
    Minimal LLM agent for MVP 2 pilot: prepares prompt and returns structured output.
    For now, the LLM call is mocked for testability.
    """
    def __init__(self, notes: List[str], user_memory: List[str], classification_config: Optional[dict] = None):
        self.notes = notes
        self.user_memory = user_memory
        self.classification_config = classification_config or {}

    def build_prompt(self) -> str:
        """Construct the prompt for the LLM using notes and user memory."""
        prompt = f"""
You are an AI agent assisting with data entry.

Current Memory:
{chr(10).join(['* ' + m for m in self.user_memory])}

Current Notes:
{chr(10).join(self.notes)}

Please interact with the user to collect the necessary information to complete the CSV and update the memory.
"""
        return prompt

    def run(self) -> LLMOutput:
        """
        (Mock) Run the agent and return structured output conforming to LLMOutput schema.
        Replace this with a real LLM call in the next step.
        """
        # Mocked output for demonstration
        entries = [
            DataEntry(field1="example1", field2=1),
            DataEntry(field1="example2", field2=2)
        ]
        new_memory_points = ["Agent processed 2 notes."]
        return LLMOutput(entries=entries, new_memory_points=new_memory_points)

if __name__ == "__main__":
    from note_interpreter.io import load_notes_from_csv, load_user_memory_from_md
    notes = load_notes_from_csv("docs/examples/example_notes.csv")
    user_memory = load_user_memory_from_md("docs/examples/example_user_memory.md")
    agent = LLMAgent(notes, user_memory)
    output = agent.run()
    print(output.model_dump_json(indent=2)) 