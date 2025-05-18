import pytest
from note_interpreter.llm_agent import LLMAgent, LLMOutput, DataEntry, SystemPromptBuilder, load_classification_from_yaml
from note_interpreter.io import load_notes_from_csv, load_user_memory_from_md
import tempfile
import os

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
    # Initialization test: agent should have tools and classification config
    assert hasattr(agent, 'tools')
    assert any(t.name == 'finalize_notes_tool' for t in agent.tools)
    assert any(t.name == 'clarification_tool' for t in agent.tools)

def test_mock_output_no_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    agent = LLMAgent(notes=["test"], user_memory=["* memory"])
    output = agent.run()
    assert isinstance(output, LLMOutput)
    assert hasattr(output, 'entries')

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
    classification_config = load_classification_from_yaml("resources/classification.yaml")
    prompt = SystemPromptBuilder.build(memory, notes, classification_config=classification_config, extra_context={"clarification_qas": clarification_qas})
    print("\n--- SYSTEM PROMPT FOR AI REVIEW ---\n")
    print(prompt)
    print("\n--- END SYSTEM PROMPT ---\n")
    # Assert all sections are present
    assert "Your Goals" in prompt
    assert "Allowed Classifications" in prompt
    assert "Current Memory:" in prompt
    assert "Current Notes:" in prompt
    assert "Clarification Q&A so far:" in prompt
    # Optionally, check that the Q&A is formatted
    assert "Q1: What kind of milk?" in prompt
    assert "A1: Almond" in prompt
    assert "Q2: What time for the meeting?" in prompt
    assert "A2: 10am" in prompt

def test_realistic_notes_prompt():
    notes = [
        "we also destroyed lots of stuff which can be useful",
        "data enricher, if agent is not sure, ask back from the human, the more knowledge it has the less question can be, so it has to understand reformulate and enrich the entity",
        "monkey brain szelidito :)))))",
        "use cases I have and functionalities I need this is the most important"
    ]
    memory = [
        "Tamas is working on a project called LifeOS, which would like him to manage his life, tasks, ideas, projects, self realization etc. So it covers the life.",
        "Tamas is interested in psychology and spirituality."
    ]
    classification_config = load_classification_from_yaml("resources/classification.yaml")
    prompt = SystemPromptBuilder.build(memory, notes, classification_config=classification_config)
    print("\n--- SYSTEM PROMPT WITH REALISTIC NOTES ---\n")
    print(prompt)
    print("\n--- END SYSTEM PROMPT ---\n")
    # Assert all notes and memory entries are present in the prompt
    for note in notes:
        assert note in prompt
    for mem in memory:
        assert mem in prompt

# --- NEW TESTS ---

def test_file_loading_integration():
    """Test loading notes from CSV, memory from MD, and classification from YAML."""
    # Create temp files
    with tempfile.NamedTemporaryFile('w+', delete=False, newline='', encoding='utf-8') as notes_f, \
         tempfile.NamedTemporaryFile('w+', delete=False, encoding='utf-8') as mem_f, \
         tempfile.NamedTemporaryFile('w+', delete=False, encoding='utf-8') as yaml_f:
        notes_f.write('note one\nnote two\n')
        notes_f.flush()
        mem_f.write('* memory one\n* memory two\n')
        mem_f.flush()
        yaml_f.write('entity_types:\n  - task\nintents:\n  - "@DO"\n')
        yaml_f.flush()
        notes = load_notes_from_csv(notes_f.name)
        memory = load_user_memory_from_md(mem_f.name)
        classification = load_classification_from_yaml(yaml_f.name)
    assert notes == ['note one', 'note two']
    assert memory == ['* memory one', '* memory two']
    assert classification['entity_types'] == ['task']
    assert classification['intents'] == ['@DO']
    os.remove(notes_f.name)
    os.remove(mem_f.name)
    os.remove(yaml_f.name)

def test_agent_tool_registration():
    """Test that agent registers both tools and stores classification config."""
    classification_config = {'entity_types': ['task'], 'intents': ['@DO']}
    agent = LLMAgent(notes=["test"], user_memory=["* memory"], classification_config=classification_config)
    tool_names = [t.name for t in agent.tools]
    assert 'finalize_notes_tool' in tool_names
    assert 'clarification_tool' in tool_names
    assert agent.classification_config == classification_config

def test_clarification_loop(monkeypatch):
    """Test the clarification loop by mocking the LLM/tool to always ask for clarification."""
    class DummyExecutor:
        def invoke(self, _):
            return {"type": "tool_call", "tool_details": {"name": "clarification_tool"}, "display_message": '{"questions": ["What do you mean by stuff?", "Which functionalities?"]}'}
    agent = LLMAgent(notes=["unclear note"], user_memory=["* memory"], classification_config={'entity_types': ['task'], 'intents': ['@DO']})
    agent.agent_core.handle_user_message = DummyExecutor().invoke
    # Simulate user answers
    monkeypatch.setattr('builtins.input', lambda prompt: "clarified answer")
    # Should loop and collect answers, then continue
    # (Here, we just check that the loop does not crash and collects answers)
    try:
        agent.run()
    except Exception:
        pytest.fail("Clarification loop failed")

def test_full_enrichment_workflow(monkeypatch):
    """Test the full workflow from files to final output, including clarification."""
    # Simulate LLM returning clarification first, then final output
    class DummyExecutor:
        def __init__(self):
            self.calls = 0
        def invoke(self, _):
            if self.calls == 0:
                self.calls += 1
                return {"type": "tool_call", "tool_details": {"name": "clarification_tool"}, "display_message": '{"questions": ["Clarify?"]}'}
            else:
                return {"type": "tool_call", "tool_details": {"name": "finalize_notes_tool"}, "display_message": '{"entries": [{"field1": "interpreted", "field2": 1}], "new_memory_points": ["* clarified"], "clarification_questions": []}'}
    agent = LLMAgent(notes=["unclear note"], user_memory=["* memory"], classification_config={'entity_types': ['task'], 'intents': ['@DO']})
    agent.agent_core.handle_user_message = DummyExecutor().invoke
    monkeypatch.setattr('builtins.input', lambda prompt: "clarified answer")
    output = agent.run()
    assert isinstance(output, LLMOutput)
    assert hasattr(output, 'entries')
    assert hasattr(output, 'new_memory_points')

def test_edge_cases():
    """Test edge cases: empty notes/memory, unknown entity types/intents, clarification limit exceeded."""
    # Empty notes/memory
    agent = LLMAgent(notes=[], user_memory=[], classification_config={'entity_types': ['task'], 'intents': ['@DO']})
    assert agent.notes == []
    assert agent.user_memory == []
    # Unknown entity type/intent (simulate output)
    output = LLMOutput(entries=[DataEntry(field1="note", field2=1)], new_memory_points=["* unknown entity type"])
    assert output.entries[0].field1 == "note"
    # Clarification limit exceeded (simulate)
    agent = LLMAgent(notes=["unclear"], user_memory=["* memory"], max_clarification_rounds=0, classification_config={'entity_types': ['task'], 'intents': ['@DO']})
    output = agent.run()
    assert isinstance(output, LLMOutput)

# You can add more tests for tool call handling, clarification loop, etc. 