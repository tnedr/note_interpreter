from typing import List, Optional
from note_interpreter.models import LLMOutput, DataEntry
import os
from dotenv import load_dotenv
load_dotenv()
from pydantic import BaseModel, Field
import json
import re

class StrictDataEntry(BaseModel):
    field1: str = Field(..., description="Description for field1")
    field2: int = Field(..., description="Description for field2")
    class Config:
        extra = "forbid"

class StrictLLMOutput(BaseModel):
    entries: List[StrictDataEntry] = Field(..., description="List of structured data entries.")
    new_memory_points: List[str] = Field(..., description="New bullet points to append to the Markdown memory.")
    class Config:
        extra = "forbid"

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
            from langchain.tools import tool
            from langchain.agents import create_openai_functions_agent, AgentExecutor
            from langchain.prompts import ChatPromptTemplate

            # Strict tool for structured output
            @tool
            def collect_data_tool(entries: List[dict], new_memory_points: List[str]) -> str:
                """You must ALWAYS use this tool to return your answer in structured form as JSON. Never reply in plain text. If you cannot answer, call the tool with empty fields."""
                # If the LLM cannot answer, return empty fields
                if not entries and not new_memory_points:
                    return StrictLLMOutput(entries=[], new_memory_points=[]).model_dump_json()
                entry_objs = [StrictDataEntry(**e) for e in entries]
                return StrictLLMOutput(entries=entry_objs, new_memory_points=new_memory_points).model_dump_json()

            llm = ChatOpenAI(model="gpt-4.1-mini", openai_api_key=api_key)
            prompt_template = ChatPromptTemplate.from_messages([
                ("system", "You are an AI agent assisting with data entry. You must ALWAYS use the provided tool to return your answer in structured form as JSON. Never reply in plain text. If you cannot answer, you must call the tool with empty fields."),
                ("user", "{input}"),
                ("system", "{agent_scratchpad}")
            ])
            agent = create_openai_functions_agent(llm, [collect_data_tool], prompt_template)
            executor = AgentExecutor(agent=agent, tools=[collect_data_tool], verbose=True)
            prompt = self.build_prompt()
            result = executor.invoke({"input": prompt})
            if isinstance(result, dict) and "output" in result:
                print("Raw LLM output:", result["output"])
                raw_output = result["output"]
                # Extract the first JSON object from the output
                match = re.search(r'\{.*\}', raw_output, re.DOTALL)
                if match:
                    json_str = match.group(0)
                    output_data = json.loads(json_str)
                    entries = [DataEntry(**e) for e in output_data.get("entries", [])]
                    new_memory_points = output_data.get("new_memory_points", [])
                    return LLMOutput(entries=entries, new_memory_points=new_memory_points)
                else:
                    raise ValueError("No valid JSON object found in LLM output.")
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