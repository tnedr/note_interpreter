from prompt_lab.libs.config_utils import get_llm_model_from_config
from prompt_lab.agents.grocery_clarifier.agent import GroceryClarifierAgent

def test_grocery_clarifier_agent_init():
    model = get_llm_model_from_config()
    agent = GroceryClarifierAgent(api_key="dummy-key", llm_model=model)
    assert agent is not None
    assert hasattr(agent, 'llm')
    assert agent.llm.model_name == model 