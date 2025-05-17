from typing import List, Optional
from note_interpreter.models import LLMOutput, DataEntry
import os
from dotenv import load_dotenv
load_dotenv()

class LLMAgent:
    """
    LLM agent for MVP 2: prepares prompt and returns structured output using LangChain and OpenAI function-calling API.
    Falls back to mock output if no API key is set.
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
        Run the agent and return structured output conforming to LLMOutput schema.
        Uses LangChain and OpenAI function-calling API if API key is set, otherwise returns mock output.
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("[LLMAgent] No OPENAI_API_KEY found. Using mock output.")
            entries = [
                DataEntry(field1="example1", field2=1),
                DataEntry(field1="example2", field2=2)
            ]
            new_memory_points = ["Agent processed 2 notes. (MOCK)"]
            return LLMOutput(entries=entries, new_memory_points=new_memory_points)
        try:
            print("[LLMAgent] Using real LLM via LangChain and OpenAI function-calling API.")
            from langchain_openai import ChatOpenAI
            from pydantic import BaseModel
            from langchain.tools import tool
            from langchain.agents import create_openai_functions_agent, AgentExecutor
            from langchain.prompts import ChatPromptTemplate

            # Define a tool for structured output
            @tool
            def collect_data_tool(entries: List[dict], new_memory_points: List[str]) -> str:
                """Collects structured data and new memory points."""
                entry_objs = [DataEntry(**e) for e in entries]
                return LLMOutput(entries=entry_objs, new_memory_points=new_memory_points).model_dump_json()

            llm = ChatOpenAI(model="gpt-4.1-mini", openai_api_key=api_key)
            # Define the prompt template for the agent
            prompt_template = ChatPromptTemplate.from_messages([
                ("system", "You are an AI agent assisting with data entry. Use the provided tool to return structured data."),
                ("user", "{input}"),
                ("system", "{agent_scratchpad}")
            ])
            agent = create_openai_functions_agent(llm, [collect_data_tool], prompt_template)
            executor = AgentExecutor(agent=agent, tools=[collect_data_tool], verbose=True)
            prompt = self.build_prompt()
            result = executor.invoke({"input": prompt})
            import json
            if isinstance(result, dict) and "output" in result:
                output_data = json.loads(result["output"])
                entries = [DataEntry(**e) for e in output_data["entries"]]
                new_memory_points = output_data["new_memory_points"]
                return LLMOutput(entries=entries, new_memory_points=new_memory_points)
            else:
                raise ValueError("Unexpected agent output format.")
        except Exception as e:
            import traceback
            print(f"[LLMAgent] LLM call failed: {e}\n{traceback.format_exc()}\nFalling back to mock output.")
            entries = [
                DataEntry(field1="error", field2=0)
            ]
            new_memory_points = [f"LLM call failed: {e}"]
            return LLMOutput(entries=entries, new_memory_points=new_memory_points)

if __name__ == "__main__":
    from note_interpreter.io import load_notes_from_csv, load_user_memory_from_md
    notes = load_notes_from_csv("docs/examples/example_notes.csv")
    user_memory = load_user_memory_from_md("docs/examples/example_user_memory.md")
    agent = LLMAgent(notes, user_memory)
    output = agent.run()
    print(output.model_dump_json(indent=2)) 