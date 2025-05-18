import pytest
from note_interpreter.llm_agent import LLMAgent, LLMOutput, DataEntry, SystemPromptBuilder
from note_interpreter.io import load_notes_from_csv, load_user_memory_from_md

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

def test_agent_initialization():
    agent = LLMAgent(notes=["test"], user_memory=["* memory"], debug_mode=True)
    assert agent.state.conversation_history[0]['content'] == 'Agent initialized.'

def test_mock_output_no_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    agent = LLMAgent(notes=["test"], user_memory=["* memory"])
    output = agent.run()
    assert isinstance(output, LLMOutput)
    assert output.entries[0].field1 == "example1"

def test_conversation_history_logging():
    agent = LLMAgent(notes=["test"], user_memory=["* memory"], debug_mode=True)
    agent._log_history('user', 'Test message')
    assert agent.state.conversation_history[-1]['role'] == 'user'
    assert agent.state.conversation_history[-1]['content'] == 'Test message'

def test_error_logging():
    agent = LLMAgent(notes=["test"], user_memory=["* memory"], debug_mode=True)
    agent._log_error("Test error")
    assert "Test error" in agent.state.errors

def test_finalization_on_max_rounds(monkeypatch):
    # Simulate LLM always returning ambiguous output (forces max rounds)
    class DummyExecutor:
        def invoke(self, _):
            return {"output": "Some ambiguous string"}
    agent = LLMAgent(notes=["ambiguous"], user_memory=["* memory"], max_clarification_rounds=1)
    # Patch the run method to simulate max rounds reached
    monkeypatch.setattr(agent, "run", lambda: LLMOutput(entries=[DataEntry(field1="UNDEFINED", field2=-1)], new_memory_points=["Clarification incomplete. Some fields may be undefined."]))
    output = agent.run()
    assert output.entries[0].field1 == "UNDEFINED"

def test_system_prompt_builder_modular():
    memory = ["Remember to always check the date.", "User prefers concise answers."]
    notes = ["Buy milk tomorrow.", "Schedule meeting with John."]
    clarification_qas = [
        ("What kind of milk?", "Almond"),
        ("What time for the meeting?", "10am")
    ]
    prompt = SystemPromptBuilder.build(memory, notes, {"clarification_qas": clarification_qas})
    print("\n--- SYSTEM PROMPT FOR AI REVIEW ---\n")
    print(prompt)
    print("\n--- END SYSTEM PROMPT ---\n")
    # Assert all sections are present
    assert "Your base task is to enrich user notes" in prompt
    assert "If you have multiple clarification questions" in prompt
    assert "You must ALWAYS use the provided tool" in prompt
    assert "Your decision protocol is as follows" in prompt
    assert "Current Memory:" in prompt
    assert "Current Notes:" in prompt
    assert "Clarification Q&A so far:" in prompt
    # Optionally, check that the Q&A is formatted
    assert "Q1: What kind of milk?" in prompt
    assert "A1: Almond" in prompt
    assert "Q2: What time for the meeting?" in prompt
    assert "A2: 10am" in prompt

# You can add more tests for tool call handling, clarification loop, etc. 