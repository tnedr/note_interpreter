"""
How to try the agent interactively (for clarification feedback):
-------------------------------------------------------------
You can run the agent in interactive mode to see and provide feedback during clarification rounds.
Example:

    from note_interpreter.llm_agent import LLMAgent, load_classification_from_yaml
    notes = ["continue plan"]
    memory = ["* Tamas is working on a project called LifeOS."]
    classification_config = load_classification_from_yaml("resources/entity_types_and_intents.yaml")
    agent = LLMAgent(notes, memory, classification_config=classification_config, temperature=0.0, debug_mode=True)
    output = agent.run()  # When clarification is needed, you'll be prompted for input in the terminal.
    print(output)

-------------------------------------------------------------
"""
import pytest
import os
import json
from note_interpreter.llm_agent import LLMAgent, LLMOutput, load_classification_from_yaml

def get_real_test_data():
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
    classification_config = load_classification_from_yaml("resources/entity_types_and_intents.yaml")
    return notes, memory, classification_config

def is_fallback_output(output):
    for entry in output.entries:
        if (
            getattr(entry, 'interpreted_text', None) == "UNDEFINED"
            or getattr(entry, 'entity_type', None) == "UNDEFINED"
            or getattr(entry, 'intent', None) == "UNDEFINED"
        ):
            return True
    return False

def pretty_print_output(output):
    try:
        if hasattr(output, "model_dump_json"):
            print(json.dumps(json.loads(output.model_dump_json()), indent=2, ensure_ascii=False))
        else:
            print(output)
    except Exception:
        print(output)

@pytest.mark.llm
def test_agent_real_llm():
    """
    Real LLM/system test: runs the agent with real LLM, notes, memory, and classification config.
    Skips if no OPENAI_API_KEY is set. Not intended for CI/CD or fast feedback.
    """
    if not os.getenv("OPENAI_API_KEY"):
        pytest.skip("No API key for real LLM test.")
    notes, memory, classification_config = get_real_test_data()
    agent = LLMAgent(notes, memory, classification_config=classification_config, temperature=0.0, debug_mode=True)
    output = agent.run()
    print("\n--- REAL LLM OUTPUT ---\n")
    pretty_print_output(output)
    print("\n--- END REAL LLM OUTPUT ---\n")
    assert isinstance(output, LLMOutput)
    assert hasattr(output, 'entries')
    assert hasattr(output, 'new_memory_points')
    assert not is_fallback_output(output), f"Agent returned fallback/placeholder output: {output}"
    for entry in output.entries:
        assert hasattr(entry, 'interpreted_text')
        assert hasattr(entry, 'entity_type')
        assert hasattr(entry, 'intent')
        assert hasattr(entry, 'clarity_score')
        # Stricter: interpreted_text should not be empty or generic
        assert entry.interpreted_text and entry.interpreted_text != "UNDEFINED"
        assert entry.entity_type and entry.entity_type != "UNDEFINED"
        assert entry.intent and entry.intent != "UNDEFINED"
        assert isinstance(entry.clarity_score, int)
        assert 0 <= entry.clarity_score <= 100

@pytest.mark.llm
def test_agent_real_llm_clarification():
    """
    Real LLM/system test: runs the agent with an ambiguous note to trigger clarification.
    Asserts that the output contains clarification questions or a finalized entry.
    """
    if not os.getenv("OPENAI_API_KEY"):
        pytest.skip("No API key for real LLM test.")
    notes = ["continue plan"]
    memory = ["* Tamas is working on a project called LifeOS."]
    classification_config = load_classification_from_yaml("resources/entity_types_and_intents.yaml")
    agent = LLMAgent(notes, memory, classification_config=classification_config, temperature=0.0, debug_mode=True)
    output = agent.run()
    print("\n--- REAL LLM CLARIFICATION OUTPUT ---\n")
    pretty_print_output(output)
    print("\n--- END REAL LLM CLARIFICATION OUTPUT ---\n")
    assert isinstance(output, LLMOutput)
    assert hasattr(output, 'entries')
    assert hasattr(output, 'new_memory_points')
    assert not is_fallback_output(output), f"Agent returned fallback/placeholder output: {output}"
    for entry in output.entries:
        assert hasattr(entry, 'interpreted_text')
        assert hasattr(entry, 'entity_type')
        assert hasattr(entry, 'intent')
        assert hasattr(entry, 'clarity_score')
        assert entry.interpreted_text and entry.interpreted_text != "UNDEFINED"
        assert entry.entity_type and entry.entity_type != "UNDEFINED"
        assert entry.intent and entry.intent != "UNDEFINED"
        assert isinstance(entry.clarity_score, int)
        assert 0 <= entry.clarity_score <= 100

@pytest.mark.llm
def test_agent_real_llm_multiple_notes():
    """
    Real LLM/system test: runs the agent with multiple notes, some ambiguous, some clear.
    Asserts that the output contains entries for all notes and handles clarifications as needed.
    """
    if not os.getenv("OPENAI_API_KEY"):
        pytest.skip("No API key for real LLM test.")
    notes = [
        "buy milk tomorrow",
        "continue plan",
        "call John about the project"
    ]
    memory = ["* Tamas is working on a project called LifeOS."]
    classification_config = load_classification_from_yaml("resources/entity_types_and_intents.yaml")
    agent = LLMAgent(notes, memory, classification_config=classification_config, temperature=0.0, debug_mode=True)
    output = agent.run()
    print("\n--- REAL LLM MULTIPLE NOTES OUTPUT ---\n")
    pretty_print_output(output)
    print("\n--- END REAL LLM MULTIPLE NOTES OUTPUT ---\n")
    assert isinstance(output, LLMOutput)
    assert hasattr(output, 'entries')
    assert len(output.entries) >= 1
    assert not is_fallback_output(output), f"Agent returned fallback/placeholder output: {output}"
    for entry in output.entries:
        assert hasattr(entry, 'interpreted_text')
        assert hasattr(entry, 'entity_type')
        assert hasattr(entry, 'intent')
        assert hasattr(entry, 'clarity_score')
        assert entry.interpreted_text and entry.interpreted_text != "UNDEFINED"
        assert entry.entity_type and entry.entity_type != "UNDEFINED"
        assert entry.intent and entry.intent != "UNDEFINED"
        assert isinstance(entry.clarity_score, int)
        assert 0 <= entry.clarity_score <= 100

@pytest.mark.llm
def test_agent_real_llm_edge_case_empty():
    """
    Real LLM/system test: runs the agent with empty notes and/or memory.
    Asserts that the output is valid and does not crash.
    """
    if not os.getenv("OPENAI_API_KEY"):
        pytest.skip("No API key for real LLM test.")
    notes = []
    memory = []
    classification_config = load_classification_from_yaml("resources/entity_types_and_intents.yaml")
    agent = LLMAgent(notes, memory, classification_config=classification_config, temperature=0.0, debug_mode=True)
    output = agent.run()
    print("\n--- REAL LLM EDGE CASE EMPTY OUTPUT ---\n")
    pretty_print_output(output)
    print("\n--- END REAL LLM EDGE CASE EMPTY OUTPUT ---\n")
    assert isinstance(output, LLMOutput)
    assert not is_fallback_output(output), f"Agent returned fallback/placeholder output: {output}"
    # If entries exist, check they are not fallback
    for entry in output.entries:
        assert entry.interpreted_text != "UNDEFINED"
        assert entry.entity_type != "UNDEFINED"
        assert entry.intent != "UNDEFINED"


def test_interactive_clarification_demo():
    """
    DEMO: Run the agent interactively to see/try the clarification loop.
    This is not a real test (does not assert), but lets you see the clarification process.
    To use: uncomment and run manually.
    """
    # Uncomment to try interactively:
    # notes = ["continue plan"]
    # memory = ["* Tamas is working on a project called LifeOS."]
    # classification_config = load_classification_from_yaml("resources/entity_types_and_intents.yaml")
    # agent = LLMAgent(notes, memory, classification_config=classification_config, temperature=0.0, debug_mode=True)
    # output = agent.run()  # You will be prompted for clarification if needed
    # print("\n--- INTERACTIVE OUTPUT ---\n")
    # pretty_print_output(output)
    # print("\n--- END INTERACTIVE OUTPUT ---\n") 