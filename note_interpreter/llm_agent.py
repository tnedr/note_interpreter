from typing import List, Optional, Tuple, Dict, Callable, Any
from note_interpreter.models import LLMOutput, DataEntry
import os
from dotenv import load_dotenv
load_dotenv()
from pydantic import BaseModel, Field
import json
from note_interpreter.agent_core import AgentCore, ToolDefinition, OpenAIToolProvider
from langchain_openai import ChatOpenAI
import yaml
import logging

class MemoryManager:
    """Handles loading and saving long-term memory."""
    @staticmethod
    def load_from_md(path: str) -> List[str]:
        # Placeholder: actual implementation should parse markdown
        with open(path, encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        return lines

# Loader for classification YAML
def load_classification_from_yaml(path: str) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def load_schema_from_yaml(path: str) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def load_parameters_from_yaml(path: str) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def load_scoring_metrics_from_yaml(path: str) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

class SystemPromptBuilder:
    """
    Config-driven, registry-based prompt builder. Each section is a function registered in a central registry.
    The prompt is built by reading a YAML config file that specifies the order, enabled/disabled state, and parameters for each section.
    """
    section_registry: Dict[str, Callable[[dict, dict], str]] = {}

    @classmethod
    def register_section(cls, name: str):
        def decorator(func):
            cls.section_registry[name] = func
            return func
        return decorator

    @classmethod
    def build_from_config(cls, memory: List[str], notes: List[str], classification_config: dict = None, extra_context: Optional[dict] = None, schema: dict = None, parameters: dict = None, scoring_metrics: dict = None, config_path: str = "resources/prompt_config.yaml") -> str:
        """
        Build the prompt from a YAML config file. Each enabled section is rendered in order.
        Now supports loading classification config from the file specified in the 'classification' section params.
        """
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        sections = config.get('sections', [])
        # Check if classification section has a file param
        classification_file = None
        for section in sections:
            if section.get('name') == 'classification' and section.get('params', {}).get('classification_file'):
                classification_file = section['params']['classification_file']
                break
        if classification_file:
            with open(classification_file, 'r', encoding='utf-8') as f:
                loaded_classification_config = yaml.safe_load(f)
        else:
            loaded_classification_config = classification_config or {}
        context = {
            'memory': memory,
            'notes': notes,
            'classification_config': loaded_classification_config,
            'extra_context': extra_context or {},
            'schema': schema or {},
            'parameters': parameters or {},
            'scoring_metrics': scoring_metrics or {},
        }
        prompt_parts = []
        for section in sections:
            if not section.get('enabled', True):
                continue
            name = section['name']
            params = section.get('params', {})
            custom_text = section.get('custom_text')
            # Custom text/override
            if custom_text:
                prompt_parts.append(custom_text)
                continue
            func = cls.section_registry.get(name)
            if func:
                try:
                    part = func(params, context)
                    prompt_parts.append(part)
                except Exception as e:
                    logging.warning(f"Prompt section '{name}' failed: {e}")
            else:
                logging.warning(f"Prompt section '{name}' not found in registry.")
        return "\n".join([p for p in prompt_parts if p])

    @classmethod
    def build(cls, memory: List[str], notes: List[str], classification_config: dict = None, extra_context: Optional[dict] = None, schema: dict = None, parameters: dict = None, scoring_metrics: dict = None, config_path: str = None) -> str:
        """
        Backward-compatible build method. Uses config if provided, else default config.
        """
        if config_path is None:
            config_path = "resources/prompt_config.yaml"
        return cls.build_from_config(memory, notes, classification_config, extra_context, schema, parameters, scoring_metrics, config_path)

    # --- Section Implementations ---
    @staticmethod
    @register_section('intro')
    def intro_section(params, context):
        return "# 🤖 System Prompt: AI Note Interpretation & Enrichment Agent\n\nYou are an AI assistant that helps users interpret, clarify, and enrich their personal notes for life management, project tracking, and self-improvement. Your job is to turn ambiguous, shorthand, or incomplete notes into clear, actionable, and structured data, asking for clarification if needed, and updating long-term memory with new insights.\n"

    @staticmethod
    @register_section('classification')
    def classification_section(params, context):
        classification_config = context['classification_config']
        entity_types = classification_config.get("entity_types", [])
        intents = classification_config.get("intents", [])
        return (
            "## 🏷️ Allowed Classifications\n\n"
            f"**Entity Types:** {', '.join(entity_types)}\n"
            f"**Intents:** {', '.join(intents)}\n"
        )

    @staticmethod
    @register_section('goals')
    def goals_section(params, context):
        return (
            "## 🎯 Your Goals\n\n"
            "For each input note, your output must include:\n"
            "1. **Structured JSON Output** via the `finalize_notes_tool`, always including:\n"
            "   - `entries`: interpreted notes with enriched metadata\n"
            "   - `new_memory_points`: long-term memory insights (natural language bullet points)\n"
            "   - `clarification_questions`: questions if clarification is needed\n"
            "2. You MUST use the tool – never respond in plain text.\n"
        )

    @staticmethod
    @register_section('scoring_guidelines')
    def note_scoring_guidelines_section(params, context):
        scoring_metrics = context['scoring_metrics']
        parameters = context['parameters']
        if not scoring_metrics:
            return ""
        section = "## 🧪 Note Scoring Guidelines\n\nEach note is internally evaluated using the following metrics (not shown in output but used for clarification logic):\n\n"
        triggers = []
        for metric, info in scoring_metrics.items():
            section += f"- `{metric}` ({info.get('range','')}): {info.get('description','')}\n"
            if 'clarification_trigger' in info:
                if info['clarification_trigger'] == 'above':
                    threshold = parameters.get(f"{metric}_threshold", {}).get('value', None) if parameters else None
                    if threshold is not None:
                        triggers.append(f"- `{metric}` > {threshold}")
                elif info['clarification_trigger'] == 'below':
                    threshold = parameters.get(f"{metric}_threshold", {}).get('value', None) if parameters else None
                    if threshold is not None:
                        triggers.append(f"- `{metric}` < {threshold}")
        if triggers:
            section += "\nTrigger clarification if:\n" + "\n".join(triggers) + "\n"
        return section

    @staticmethod
    @register_section('output_schema_and_meanings')
    def output_schema_and_meanings_section(params, context):
        """
        Unified output schema and field meanings, loaded from YAML.
        params['schema_file'] should specify the YAML file.
        """
        schema_file = params.get('schema_file', 'resources/notes_output_schema.yaml')
        import yaml as _yaml
        with open(schema_file, 'r', encoding='utf-8') as f:
            schema = _yaml.safe_load(f)
        section = "## 📌 Structured Output Schema & Field Meanings\n\nEach entry must have the following fields:\n\n"
        for field, info in schema.get('DataEntry', {}).items():
            section += f"- `{field}` ({info.get('type','')}): {info.get('description','')}\n"
        return section

    @staticmethod
    @register_section('tool_json_schema')
    def tool_json_schema_section(params, context):
        schema = {
            "type": "object",
            "properties": {
                "entries": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "interpreted_text": {"type": "string"},
                            "entity_type": {"type": "string"},
                            "intent": {"type": "string"},
                            "clarity_score": {"type": "integer"}
                        },
                        "required": ["interpreted_text", "entity_type", "intent", "clarity_score"]
                    }
                },
                "new_memory_points": {"type": "array", "items": {"type": "string"}},
                "clarification_questions": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["entries", "new_memory_points", "clarification_questions"]
        }
        return (
            "## 🛠️ Tool JSON Schema (for finalize_notes_tool)\n\n"
            "```json\n" + json.dumps(schema, indent=2) + "\n```\n"
        )

    @staticmethod
    @register_section('parameter_explanations')
    def parameter_explanations_section(params, context):
        parameters = context['parameters']
        section = "## ⚙️ Agent Parameters\n\n"
        for param, info in parameters.items():
            section += f"- `{param}` = {info['value']} ({info['description']})\n"
        return section

    @staticmethod
    @register_section('output_validation_rules')
    def output_validation_rules_section(params, context):
        return (
            "## 🔒 Output Validation Rules (Mandatory)\n\n"
            "- You MUST return a valid JSON object calling `finalize_notes_tool`.\n"
            "- You MUST include all three fields: `entries`, `new_memory_points`, and `clarification_questions`.\n"
            "- Even if empty, provide an empty list (`[]`) for any missing category.\n"
            "- Never return plain text or unstructured answers.\n"
        )

    @staticmethod
    @register_section('tool_behavior_summary')
    def tool_behavior_summary_section(params, context):
        return (
            "## 🛠️ Tool Behavior Summary\n\n"
            "- `finalize_notes_tool(...)` is the only valid way to output results.\n"
            "- It accepts three parameters:\n"
            "  - `entries`: your main result\n"
            "  - `new_memory_points`: context insights\n"
            "  - `clarification_questions`: if you need help\n"
        )

    @staticmethod
    @register_section('context_usage')
    def context_usage_section(params, context):
        return (
            "## 🧠 Context Usage\n\n"
            "- Use **user memory** to resolve ambiguity and improve interpretation.\n"
            "- Use **context from other notes** in the batch only if relevant.\n"
            "- Always aim for clarity and actionability.\n"
        )

    @staticmethod
    @register_section('clarification_protocol')
    def clarification_protocol_section(params, context):
        return (
            "## 🔍 Clarification Protocol\n\n"
            "If interpretation is uncertain:\n"
            "- Generate clarification questions ONLY IF:\n"
            "  - `confidence_score < 70`, OR\n"
            "  - `ambiguity_score > 60`\n\n"
            "If clarification is needed:\n"
            "- List all questions in a single message, numbered:\n"
            "  ```\n"
            "  1: [question]\n"
            "  2: [question]\n"
            "  ```\n"
            "- Ask the user to reply with:\n"
            "  ```\n"
            "  1: [answer]\n"
            "  2: [answer]\n"
            "  ```\n\n"
            "If answers are received:\n"
            "- Re-interpret the note with updated understanding.\n"
            "- Repeat for up to **2 clarification rounds maximum**.\n"
            "- If ambiguity persists, finalize output and use `UNDEFINED` or `MISSING_` flags.\n"
        )

    @staticmethod
    @register_section('memory_update')
    def memory_update_section(params, context):
        return (
            "## 🧠 Memory Update Rules\n\n"
            "For every finalized interpretation:\n"
            "- Append memory points about:\n"
            "  - Clarified terms or shorthand\n"
            "  - Project references or tools\n"
            "  - Patterns in phrasing or note structure\n"
            "- Use natural language in bullet-point format (`* ...`)\n"
            "- Never rewrite or delete past memory – this log is append-only.\n"
        )

    @staticmethod
    @register_section('memory_point_examples')
    def memory_point_examples_section(params, context):
        return (
            "## 📘 Memory Point Examples\n\n"
            "* Tamas is currently working on a Q3 marketing launch plan and often refers to it simply as 'plan.'\n"
            "* Tamas prefers to phrase actionable notes starting with verbs like 'continue,' 'email,' or 'draft.'\n"
            "* Tamas uses the term 'LifeOS' to refer to his integrated personal operating system project.\n"
        )

    @staticmethod
    @register_section('example_output')
    def example_output_section(params, context):
        return (
            "## 🧮 Example Entry Output (JSON)\n\n"
            "```json\n"
            "{\n"
            "  \"entries\": [\n"
            "    {\n"
            "      \"interpreted_text\": \"Continue working on the Q3 marketing launch plan.\",\n"
            "      \"entity_type\": \"task\",\n"
            "      \"intent\": \"@DO\",\n"
            "      \"clarity_score\": 92\n"
            "    }\n"
            "  ],\n"
            "  \"new_memory_points\": [\n"
            "    \"* Tamas is currently working on a Q3 marketing launch plan and often uses 'plan' to refer to it.\"\n"
            "  ],\n"
            "  \"clarification_questions\": []\n"
            "}\n"
            "```\n"
        )

    @staticmethod
    @register_section('input_context')
    def input_context_section(params, context):
        memory = context['memory']
        notes = context['notes']
        clarification_qas = context['extra_context'].get('clarification_qas')
        section = "---\n\n## 🔎 Input Context\n\n"
        section += "### Current Memory:\n"
        if memory:
            section += "\n".join([f"* {m}" for m in memory]) + "\n\n"
        else:
            section += "(none)\n\n"
        section += "### Current Notes:\n"
        if notes:
            section += "  \n".join(notes) + "  \n\n"
        else:
            section += "(none)\n\n"
        if clarification_qas:
            section += "### Clarification Q&A so far:\n"
            for i, (q, a) in enumerate(clarification_qas, 1):
                section += f"Q{i}: {q}  \nA{i}: {a}  \n"
        return section

    @staticmethod
    @register_section('finalization_protocol')
    def finalization_protocol_section(params, context):
        return (
            "## 🛑 Finalization Protocol\n\n"
            "- After providing the final structured output, do not ask further questions. The conversation is finished.\n"
            "- Never respond in plain text at any stage.\n"
            "- If no clear interpretation is possible after all clarification rounds:\n"
            "  - Use `\"UNDEFINED\"` for any field that cannot be confidently determined.\n"
            "  - Still call the `finalize_notes_tool` with all fields included.\n"
        )

class ClarificationManager:
    """Handles clarification logic for the agent."""
    @staticmethod
    def needs_clarification(agent_response: dict) -> bool:
        return bool(agent_response.get('clarification_questions'))

    @staticmethod
    def get_questions(agent_response: dict) -> List[str]:
        return agent_response.get('clarification_questions', [])

    @staticmethod
    def update_clarification_qas(clarification_qas: List[Tuple[str, str]], questions: List[str]) -> List[Tuple[str, str]]:
        answers = []
        for q in questions:
            print(q)
            a = input(f"Your answer to '{q}': ")
            answers.append((q, a))
        return clarification_qas + answers

class OutputFormatter:
    """Validates and formats the final output."""
    @staticmethod
    def format(agent_response: dict) -> LLMOutput:
        entries = [DataEntry(**e) for e in agent_response.get('entries', [])]
        new_memory_points = agent_response.get('new_memory_points', [])
        return LLMOutput(entries=entries, new_memory_points=new_memory_points)

class LLMAgent:
    _logging_initialized = False
    _schema = None
    _parameters = None
    _scoring_metrics = None
    """
    Modular LLM agent using AgentCore for conversation and tool orchestration.
    Handles memory, prompt building, clarification loop, and structured output.
    Now uses two tools: 'clarification_tool' for clarification questions, and 'finalize_notes_tool' for final output.
    Accepts a classification_config for allowed entity_types and intents.
    If temperature=0.0, output is deterministic (recommended for tests).
    Loads output schema, agent parameters, and scoring metrics from YAML for consistency.
    """
    def __init__(self, notes: List[str], user_memory: List[str], classification_config: dict = None, max_clarification_rounds: int = None, debug_mode: bool = False, shared_context: Optional[dict] = None, temperature: float = None):
        self.notes = notes
        self.user_memory = user_memory
        self.classification_config = classification_config or {}
        # Load schema, parameters, and scoring metrics if not already loaded
        if not LLMAgent._schema:
            LLMAgent._schema = load_schema_from_yaml("resources/notes_output_schema.yaml")
        if not LLMAgent._parameters:
            LLMAgent._parameters = load_parameters_from_yaml("resources/agent_parameters.yaml")
        if not LLMAgent._scoring_metrics:
            LLMAgent._scoring_metrics = load_scoring_metrics_from_yaml("resources/scoring_metrics.yaml")
        self.schema = LLMAgent._schema
        self.parameters = LLMAgent._parameters
        self.scoring_metrics = LLMAgent._scoring_metrics
        # Use parameters for agent config
        self.max_clarification_rounds = max_clarification_rounds if max_clarification_rounds is not None else self.parameters['max_clarification_rounds']['value']
        self.debug_mode = debug_mode
        self.shared_context = shared_context or {}
        self.temperature = temperature if temperature is not None else self.parameters['temperature']['value']
        if self.debug_mode and not LLMAgent._logging_initialized:
            logger = logging.getLogger()
            logger.setLevel(logging.DEBUG)
            # Remove all handlers (to avoid duplicate logs)
            for handler in logger.handlers[:]:
                logger.removeHandler(handler)
            # Add file handler
            file_handler = logging.FileHandler("llm_agent_debug.log", mode='w', encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
            logger.addHandler(file_handler)
            # Add console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            console_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
            logger.addHandler(console_handler)
            LLMAgent._logging_initialized = True
        self.llm = ChatOpenAI(model="gpt-4.1-mini", openai_api_key=os.getenv("OPENAI_API_KEY"), temperature=self.temperature)
        self.tools = [
            self._get_finalize_notes_tool(),
            self._get_clarification_tool()
        ]
        self.agent_core = AgentCore(
            llm=self.llm,
            tools=self.tools,
            system_prompt=SystemPromptBuilder.build(
                self.user_memory,
                self.notes,
                classification_config=self.classification_config,
                schema=self.schema,
                parameters=self.parameters,
                scoring_metrics=self.scoring_metrics
            ),
            shared_context=self.shared_context,
            debug_mode=self.debug_mode
        )

    def _get_finalize_notes_tool(self) -> ToolDefinition:
        def finalize_notes_tool(entries=None, new_memory_points=None, clarification_questions=None, shared_context=None):
            if entries is None:
                entries = []
            if new_memory_points is None:
                new_memory_points = []
            if clarification_questions is None:
                clarification_questions = []
            return {
                "entries": entries,
                "new_memory_points": new_memory_points,
                "clarification_questions": clarification_questions
            }
        return ToolDefinition(
            name="finalize_notes_tool",
            description="Returns the final structured interpretation and enrichment of all notes.",
            schema={
                "type": "object",
                "properties": {
                    "entries": {"type": "array", "items": {"type": "object"}},
                    "new_memory_points": {"type": "array", "items": {"type": "string"}},
                    "clarification_questions": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["entries", "new_memory_points", "clarification_questions"]
            },
            function=finalize_notes_tool
        )

    def _get_clarification_tool(self) -> ToolDefinition:
        def clarification_tool(questions=None, context=None, shared_context=None):
            if questions is None:
                questions = []
            if context is None:
                context = []
            return {
                "questions": questions,
                "context": context
            }
        return ToolDefinition(
            name="clarification_tool",
            description="Poses clarification questions to the user in a structured way.",
            schema={
                "type": "object",
                "properties": {
                    "questions": {"type": "array", "items": {"type": "string"}},
                    "context": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["questions"]
            },
            function=clarification_tool
        )

    def run(self) -> LLMOutput:
        clarification_qas = []
        for round_num in range(self.max_clarification_rounds):
            user_context = SystemPromptBuilder.build(
                self.user_memory,
                self.notes,
                classification_config=self.classification_config,
                extra_context={"clarification_qas": clarification_qas},
                schema=self.schema,
                parameters=self.parameters,
                scoring_metrics=self.scoring_metrics
            )
            if self.debug_mode:
                logging.debug(f"System prompt (round {round_num+1}):\n{user_context}\n")
            response = self.agent_core.handle_user_message(user_context)
            if self.debug_mode:
                logging.debug(f"Raw AgentCore response: {response}")
            # Check which tool was called
            if response["type"] == "tool_call" and response["tool_details"]:
                tool_name = response["tool_details"]["name"]
                tool_output = response["display_message"]
                try:
                    if (not tool_output or tool_output == "") and response["tool_details"] and "args" in response["tool_details"]:
                        output_data = response["tool_details"]["args"]
                    else:
                        output_data = json.loads(tool_output) if isinstance(tool_output, str) else tool_output
                    if self.debug_mode:
                        logging.debug(f"Tool '{tool_name}' output: {output_data}")
                    if tool_name == "clarification_tool":
                        questions = output_data.get("questions", [])
                        if questions:
                            print("\nClarification questions:")
                            for i, q in enumerate(questions, 1):
                                print(f"{i}: {q}")
                        answers = []
                        for i, q in enumerate(questions, 1):
                            a = input(f"Your answer to '{q}': ")
                            answers.append((q, a))
                        clarification_qas.extend(answers)
                        continue  # Next round with updated Q&A
                    elif tool_name == "finalize_notes_tool":
                        final_output = OutputFormatter.format(output_data)
                        if self.debug_mode:
                            logging.debug(f"Final output: {final_output}")
                        return final_output
                except Exception as e:
                    logging.error(f"[LLMAgent] Failed to parse tool output: {e}. Raw output: {tool_output}")
                    continue
            else:
                # If not a tool call, treat as clarification request or message
                print("LLM says:", response["display_message"])
                user_input = input("Your answer: ")
                clarification_qas.append((response["display_message"], user_input))
                continue
        # If max rounds reached, finalize with placeholders
        logging.warning("Maximum clarification rounds reached. Finalizing with placeholders if needed.")
        entries = [DataEntry(interpreted_text="UNDEFINED", entity_type="UNDEFINED", intent="UNDEFINED", clarity_score=0)]
        new_memory_points = ["Clarification incomplete. Some fields may be undefined."]
        final_output = LLMOutput(entries=entries, new_memory_points=new_memory_points)
        if self.debug_mode:
            logging.debug(f"Final output (fallback): {final_output}")
        return final_output

    def _is_fallback_output(self, output: LLMOutput) -> bool:
        """Returns True if the output is a fallback/placeholder (e.g., UNDEFINED fields)."""
        for entry in output.entries:
            if (
                entry.interpreted_text == "UNDEFINED"
                or entry.entity_type == "UNDEFINED"
                or entry.intent == "UNDEFINED"
            ):
                return True
        return False

if __name__ == "__main__":
    # Example usage
    notes = MemoryManager.load_from_md("docs/examples/example_notes.csv")
    user_memory = MemoryManager.load_from_md("docs/examples/example_user_memory.md")
    agent = LLMAgent(notes, user_memory)
    output = agent.run()
    print(output.model_dump_json(indent=2)) 