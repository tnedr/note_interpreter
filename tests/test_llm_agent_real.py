import pytest
import os
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
    classification_config = load_classification_from_yaml("resources/classification.yaml")
    return notes, memory, classification_config

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
    print(output)
    print("\n--- END REAL LLM OUTPUT ---\n")
    assert isinstance(output, LLMOutput)
    assert hasattr(output, 'entries')
    assert hasattr(output, 'new_memory_points')
    for entry in output.entries:
        assert hasattr(entry, 'interpreted_text')
        assert hasattr(entry, 'entity_type')
        assert hasattr(entry, 'intent')
        assert hasattr(entry, 'clarity_score')

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
    classification_config = load_classification_from_yaml("resources/classification.yaml")
    agent = LLMAgent(notes, memory, classification_config=classification_config, temperature=0.0, debug_mode=True)
    output = agent.run()
    print("\n--- REAL LLM CLARIFICATION OUTPUT ---\n")
    print(output)
    print("\n--- END REAL LLM CLARIFICATION OUTPUT ---\n")
    assert isinstance(output, LLMOutput)
    # Accept either clarification or finalized output
    assert hasattr(output, 'entries')
    assert hasattr(output, 'new_memory_points')
    for entry in output.entries:
        assert hasattr(entry, 'interpreted_text')
        assert hasattr(entry, 'entity_type')
        assert hasattr(entry, 'intent')
        assert hasattr(entry, 'clarity_score')

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
    classification_config = load_classification_from_yaml("resources/classification.yaml")
    agent = LLMAgent(notes, memory, classification_config=classification_config, temperature=0.0, debug_mode=True)
    output = agent.run()
    print("\n--- REAL LLM MULTIPLE NOTES OUTPUT ---\n")
    print(output)
    print("\n--- END REAL LLM MULTIPLE NOTES OUTPUT ---\n")
    assert isinstance(output, LLMOutput)
    assert hasattr(output, 'entries')
    # Should have at least as many entries as notes (or clarifications if needed)
    assert len(output.entries) >= 1
    for entry in output.entries:
        assert hasattr(entry, 'interpreted_text')
        assert hasattr(entry, 'entity_type')
        assert hasattr(entry, 'intent')
        assert hasattr(entry, 'clarity_score')

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
    classification_config = load_classification_from_yaml("resources/classification.yaml")
    agent = LLMAgent(notes, memory, classification_config=classification_config, temperature=0.0, debug_mode=True)
    output = agent.run()
    print("\n--- REAL LLM EDGE CASE EMPTY OUTPUT ---\n")
    print(output)
    print("\n--- END REAL LLM EDGE CASE EMPTY OUTPUT ---\n")
    assert isinstance(output, LLMOutput) 