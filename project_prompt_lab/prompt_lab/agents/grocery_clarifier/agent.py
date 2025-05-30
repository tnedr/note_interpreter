from prompt_lab.libs.agent_core_v2 import AgentCoreV2
from langchain_openai import ChatOpenAI

class GroceryClarifierAgent(AgentCoreV2):
    """
    Agent for grocery note clarification, using OpenAI LLM.
    The LLM model is passed in as a parameter (dependency injection).
    """
    def __init__(self, api_key: str, llm_model: str, system_prompt: str = None, **kwargs):
        llm = ChatOpenAI(api_key=api_key, model_name=llm_model)
        if system_prompt is None:
            # Default system prompt, can be loaded from YAML if needed
            system_prompt = (
                "You are a shopping assistant. "
                "Evaluate the user's note and return a clarity score (0–100). "
                "If the note is unclear, generate a clarification question."
            )
        super().__init__(
            llm=llm,
            tools=[],  # Add tools if needed
            system_prompt=system_prompt,
            **kwargs
        ) 