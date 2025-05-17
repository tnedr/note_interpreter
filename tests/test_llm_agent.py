import pytest
from note_interpreter.llm_agent import LLMAgent
from note_interpreter.io import load_notes_from_csv, load_user_memory_from_md
from note_interpreter.models import LLMOutput

def test_llm_agent_pilot():
    notes = load_notes_from_csv("docs/examples/example_notes.csv")
    user_memory = load_user_memory_from_md("docs/examples/example_user_memory.md")
    agent = LLMAgent(notes, user_memory)
    output = agent.run()
    assert isinstance(output, LLMOutput)
    assert hasattr(output, 'entries')
    assert hasattr(output, 'new_memory_points')
    assert isinstance(output.entries, list)
    assert isinstance(output.new_memory_points, list)
    assert len(output.entries) > 0
    for entry in output.entries:
        assert hasattr(entry, 'field1')
        assert hasattr(entry, 'field2') 