from note_interpreter.agent_core import AgentCore, BaseSharedContext, ToolDefinition
from typing import List, Dict, Any, Optional
import os
import json
from langchain_openai import ChatOpenAI

# Helper: default tool definition (példa)
def get_default_tools():
    # TODO: Töltsd be a tools.py-ból vagy YAML-ból, ha van
    return [
        ToolDefinition(
            name="clarify_notes",
            description="Generates clarification questions for notes below threshold.",
            schema={"type": "object", "properties": {"questions": {"type": "array", "items": {"type": "string"}}}, "required": ["questions"]}
        ),
        ToolDefinition(
            name="score_notes",
            description="Assigns clarity_score to each note.",
            schema={"type": "object", "properties": {"clarity_score": {"type": "integer"}}}
        )
    ]

# Helper: prompt betöltése
def load_default_prompt():
    prompt_path = os.path.join("resources", "clarify_and_score_agent", "prompt.txt")
    if os.path.exists(prompt_path):
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    # Fallback: default string
    return "# ClarifyAndScoreAgent system prompt\nYou are an agent that clarifies notes and assigns scores."

class ClarifyAndScoreAgent:
    """
    Context-driven agent wrapper, master plan architektúra szerint.
    Minden context explicit paraméterként megy át, nincs implicit state.
    """
    def __init__(self, prompt: Optional[str] = None, tools: Optional[List[ToolDefinition]] = None, config: Optional[Dict[str, Any]] = None, prompt_version: Optional[str] = None, debug_mode: bool = False):
        self.config = config or {}
        self.prompt_version = prompt_version
        self.debug_mode = debug_mode
        # LLM példányosítás (configból vagy default)
        model = self.config.get("model", "gpt-4o")
        temperature = self.config.get("temperature", 0.0)
        openai_api_key = os.getenv("OPENAI_API_KEY")
        self.llm = ChatOpenAI(model=model, openai_api_key=openai_api_key, temperature=temperature)
        # Toolok betöltése
        self.tools = tools if tools is not None else get_default_tools()
        # Prompt betöltése
        self.prompt = prompt if prompt is not None else load_default_prompt()

    def run(self, notes: List[str], user_memory: List[str], clarification_history: Optional[List[Dict[str, Any]]] = None, pipeline_state: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Fő belépési pont: minden context explicit paraméterként.
        Output: master plan szerinti NoteOutput lista (dict-ekkel)
        """
        # Shared context összeállítása
        shared_context = BaseSharedContext(
            notes=notes,
            user_memory=user_memory,
            clarification_history=clarification_history or [],
            pipeline_state=pipeline_state or {},
            config=self.config,
            prompt_version=self.prompt_version
        )
        # AgentCore példányosítása
        agent_core = AgentCore(
            llm=self.llm,
            tools=self.tools,
            system_prompt=self.prompt,
            shared_context=shared_context,
            debug_mode=self.debug_mode
        )
        # Futtatás
        output = agent_core.handle_user_message("Proceed")
        # Output validáció és mapping
        return self._map_and_validate_output(output)

    def _map_and_validate_output(self, output: Any) -> List[Dict[str, Any]]:
        """
        Output validáció és mapping a master plan szerinti NoteOutput sémára.
        """
        # Elvárt mezők a master plan szerint
        required_fields = [
            "id", "raw_text", "clarification_history", "clarified_text", "clarity_score", "new_questions", "long_term_memory"
        ]
        # Feltételezzük, hogy output egy list of dict (jegyzetek)
        notes = []
        if isinstance(output, dict) and "notes" in output:
            notes = output["notes"]
        elif isinstance(output, list):
            notes = output
        else:
            # Fallback: próbáljuk JSON-ként értelmezni
            try:
                notes = json.loads(output)
            except Exception:
                notes = []
        validated = []
        for i, note in enumerate(notes):
            mapped = {}
            for field in required_fields:
                if field in note:
                    mapped[field] = note[field]
                else:
                    mapped[field] = "UNDEFINED"
            # id generálás fallback
            if mapped["id"] == "UNDEFINED":
                mapped["id"] = f"note_{i+1}"
            validated.append(mapped)
        if not validated:
            # Ha semmi nincs, dobjunk warningot
            print("[WARNING] Agent output is empty or invalid, returning empty NoteOutput list.")
        return validated 