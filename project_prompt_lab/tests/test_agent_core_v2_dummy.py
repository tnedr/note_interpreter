import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import pytest
from prompt_lab.libs.agent_core_v2 import AgentCoreV2, ToolDefinition
from langchain_openai import ChatOpenAI

class DummyLLM:
    def invoke(self, messages):
        # Simulate a simple LLM response object with .content
        class Response:
            content = "Dummy response"
            tool_calls = []
        return Response()

def test_agentcorev2_dummy_response():
    # No tools for this simple test
    agent = AgentCoreV2(
        llm=DummyLLM(),
        tools=[],
        system_prompt="You are a dummy agent."
    )
    messages = [
        {"role": "system", "content": "You are a dummy agent."},
        {"role": "user", "content": "Hello!"}
    ]
    response = agent.invoke_with_message_list(messages)
    # Check multi-level response structure
    assert "raw_response" in response
    assert "parsed_response" in response
    assert "display_message" in response
    assert response["display_message"] == "Dummy response"
    assert response["type"] == "conversation" or response["type"] == "CONVERSATION"
    # No tool usage expected
    assert response["tool_details"] is None 