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
import datetime
from note_interpreter.colors import RESET, BOLD, CYAN, YELLOW, MAGENTA, BLUE, GREEN, RED, WHITE, BANNER_COLORS
from note_interpreter.log import log
from note_interpreter.user_output import user_print

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

class SystemPromptBuilder:
    """
    Config-driven, registry-based prompt builder. Each section is a function registered in a central registry.
    The prompt is built by reading a YAML config file that specifies the order, enabled/disabled state, and parameters for each section.
    Now adds a visible visual separator line before each major section for human clarity.
    """
    section_registry: Dict[str, Callable[[dict, dict], str]] = {}

    # Mapping from section name to human-readable header (should match prompt_config.yaml headers)
    SECTION_HEADER_MAP = {
        'intro': 'IDENTITY / ROLE',
        'goals': 'GOALS / OBJECTIVES',
        'output_schema_and_meanings': 'OPERATIONAL PROTOCOL',
        'classification': 'OPERATIONAL PROTOCOL',
        'scoring_guidelines': 'OPERATIONAL PROTOCOL',
        'parameter_explanations': 'OPERATIONAL PROTOCOL',
        'output_validation_rules': 'OPERATIONAL PROTOCOL',
        'tool_json_schema': 'TOOL INVENTORY & USAGE',
        'tool_behavior_summary': 'TOOL INVENTORY & USAGE',
        'context_usage': 'CONTEXT & REASONING STYLE',
        'clarification_protocol': 'CONTEXT & REASONING STYLE',
        'memory_update': 'MEMORY MANAGEMENT',
        'memory_point_examples': 'MEMORY MANAGEMENT',
        'example_output': 'EXAMPLES',
        'input_context': 'INPUT CONTEXT & FINALIZATION',
        'finalization_protocol': 'INPUT CONTEXT & FINALIZATION',
        'custom_section': 'CUSTOM / EXTENSION',
    }

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
        Adds a visible visual separator line before each major section for human clarity.
        """
        import re
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        sections = config.get('sections', [])
        log.debug(f"[DEBUG] Section order from config: {[section.get('name') for section in sections]}")
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
        # scoring_metrics is now always sourced from schema
        schema_obj = schema or {}
        scoring_metrics_obj = schema_obj.get('scoring_metrics', {})
        context = {
            'memory': memory,
            'notes': notes,
            'classification_config': loaded_classification_config,
            'extra_context': extra_context or {},
            'schema': schema_obj,
            'parameters': parameters or {},
            'scoring_metrics': scoring_metrics_obj,
        }
        prompt_parts = []
        for section in sections:
            if not section.get('enabled', True):
                continue
            name = section['name']
            params = section.get('params', {})
            custom_text = section.get('custom_text')
            # --- Visual separator ---
            # Use mapping if available, else prettify the section name
            header = cls.SECTION_HEADER_MAP.get(name)
            if not header:
                # Prettify: underscores to spaces, capitalize words
                header = re.sub(r'_', ' ', name).upper()
            separator = f"------------ {header} ------------"
            prompt_parts.append(separator)
            # --- Custom text/override ---
            if custom_text:
                prompt_parts.append(custom_text)
                continue
            func = cls.section_registry.get(name)
            if func:
                try:
                    part = func(params, context)
                    prompt_parts.append(part)
                except Exception as e:
                    log.warning(f"Prompt section '{name}' failed: {e}")
            else:
                log.warning(f"Prompt section '{name}' not found in registry.")
        prompt = "\n\n".join([p for p in prompt_parts if p])
        log.debug("[DEBUG] Final built system prompt:\n" + prompt)
        return prompt

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
    def intro_section(params, context):
        return "# 🤖 System Prompt: AI Note Interpretation & Enrichment Agent\n\nYou are an AI assistant that helps users interpret, clarify, and enrich their personal notes for life management, project tracking, and self-improvement. Your job is to turn ambiguous, shorthand, or incomplete notes into clear, actionable, and structured data, asking for clarification if needed, and updating long-term memory with new insights.\n"

    @staticmethod
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
    def goals_section(params, context):
        return (
            "## 🎯 Your Goals\n\n"
            "For each input note, your output must include:\n"
            "1. **Structured JSON Output** via the `finalize_notes` tool, always including:\n"
            "   - `entries`: interpreted notes with enriched metadata\n"
            "   - `new_memory_points`: long-term memory insights (natural language bullet points)\n"
            "2. If you are uncertain, you MUST use the `ask_user` tool to ask clarification questions BEFORE finalizing.\n"
            "3. You MUST use the tools – never respond in plain text.\n"
        )

    @staticmethod
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
    def tool_json_schema_section(params, context):
        schema = [
            {
                "name": "ask_user",
                "description": "Ask the user clarification questions if the note is ambiguous or unclear.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "questions": {
                            "type": "array",
                            "items": { "type": "string" }
                        }
                    },
                    "required": ["questions"]
                }
            },
            {
                "name": "finalize_notes",
                "description": "Return the final, structured, enriched output.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entries": { "type": "array", "items": { "type": "object" } },
                        "new_memory_points": { "type": "array", "items": { "type": "string" } }
                    },
                    "required": ["entries", "new_memory_points"]
                }
            }
        ]
        return (
            "## 🛠️ Tool JSON Schema\n\n"
            "```json\n" + json.dumps(schema, indent=2) + "\n```\n"
        )

    @staticmethod
    def parameter_explanations_section(params, context):
        parameters = context['parameters']
        section = "## ⚙️ Agent Parameters\n\n"
        for param, info in parameters.items():
            section += f"- `{param}` = {info['value']} ({info['description']})\n"
        return section

    @staticmethod
    def output_validation_rules_section(params, context):
        return (
            "## 🔒 Output Validation Rules (Mandatory)\n\n"
            "- You MUST return a valid JSON object calling either `ask_user` or `finalize_notes`.\n"
            "- You MUST use the tools for all communication.\n"
            "- Never return plain text or unstructured answers.\n"
            "- For `finalize_notes`, always include both `entries` and `new_memory_points` (even if empty).\n"
            "- For `ask_user`, always include at least one question.\n"
        )

    @staticmethod
    def tool_behavior_summary_section(params, context):
        return (
            "## 🛠️ Tool Behavior Summary\n\n"
            "- `ask_user(...)`: Use this tool to ask the user clarification questions. Do **not** finalize the output until you have the answers.\n"
            "- `finalize_notes(...)`: Use this tool only when you are confident in your interpretation and all necessary clarifications have been made.\n"
            "- Never respond in plain text or unstructured answers.\n"
        )

    @staticmethod
    def context_usage_section(params, context):
        return (
            "## 🧠 Context Usage\n\n"
            "- Use **user memory** to resolve ambiguity and improve interpretation.\n"
            "- Use **context from other notes** in the batch only if relevant.\n"
            "- Always aim for clarity and actionability.\n"
        )

    @staticmethod
    def clarification_protocol_section(params, context):
        return (
            "## 🔍 Clarification Protocol\n\n"
            "If interpretation is uncertain, or if you are not sure which tool to use, or how to use a tool, you MUST always ask the user for clarification using the ask_user tool BEFORE attempting any other tool or providing a final answer.\n"
            "- Generate clarification questions ONLY IF:\n"
            "  - confidence_score < 70, OR\n"
            "  - ambiguity_score > 60, OR\n"
            "  - the tool usage or required parameters are ambiguous in any way.\n\n"
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
    def memory_point_examples_section(params, context):
        return (
            "## 📘 Memory Point Examples\n\n"
            "* Tamas is currently working on a Q3 marketing launch plan and often refers to it simply as 'plan.'\n"
            "* Tamas prefers to phrase actionable notes starting with verbs like 'continue,' 'email,' or 'draft.'\n"
            "* Tamas uses the term 'LifeOS' to refer to his integrated personal operating system project.\n"
        )

    @staticmethod
    def example_output_section(params, context):
        return (
            "## 🧮 Example Entry Output (JSON)\n\n"
            "```json\n"
            "{\n"
            "  \"entries\": [\n"
            "    {\n"
            "      \"raw_text\": \"Continue working on the Q3 marketing launch plan.\",\n"
            "      \"interpreted_text\": \"Continue working on the Q3 marketing launch plan.\",\n"
            "      \"entity_type\": \"task\",\n"
            "      \"intent\": \"@DO\",\n"
            "      \"clarity_score\": 92\n"
            "    }\n"
            "  ],\n"
            "  \"new_memory_points\": [\n"
            "    \"* Tamas is currently working on a Q3 marketing launch plan and often uses 'plan' to refer to it.\"\n"
            "  ]\n"
            "}\n"
            "```\n"
        )

    @staticmethod
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
    def finalization_protocol_section(params, context):
        return (
            "## 🛑 Finalization Protocol\n\n"
            "- After providing the final structured output, do not ask further questions. The conversation is finished.\n"
            "- Never respond in plain text at any stage.\n"
            "- If no clear interpretation is possible after all clarification rounds:\n"
            "  - Use `\"UNDEFINED\"` for any field that cannot be confidently determined.\n"
            "  - Still call the `finalize_notes` with all fields included.\n"
        )

# Register all section methods after class definition
SystemPromptBuilder.register_section('intro')(SystemPromptBuilder.intro_section)
SystemPromptBuilder.register_section('classification')(SystemPromptBuilder.classification_section)
SystemPromptBuilder.register_section('goals')(SystemPromptBuilder.goals_section)
SystemPromptBuilder.register_section('scoring_guidelines')(SystemPromptBuilder.note_scoring_guidelines_section)
SystemPromptBuilder.register_section('output_schema_and_meanings')(SystemPromptBuilder.output_schema_and_meanings_section)
SystemPromptBuilder.register_section('tool_json_schema')(SystemPromptBuilder.tool_json_schema_section)
SystemPromptBuilder.register_section('parameter_explanations')(SystemPromptBuilder.parameter_explanations_section)
SystemPromptBuilder.register_section('output_validation_rules')(SystemPromptBuilder.output_validation_rules_section)
SystemPromptBuilder.register_section('tool_behavior_summary')(SystemPromptBuilder.tool_behavior_summary_section)
SystemPromptBuilder.register_section('context_usage')(SystemPromptBuilder.context_usage_section)
SystemPromptBuilder.register_section('clarification_protocol')(SystemPromptBuilder.clarification_protocol_section)
SystemPromptBuilder.register_section('memory_update')(SystemPromptBuilder.memory_update_section)
SystemPromptBuilder.register_section('memory_point_examples')(SystemPromptBuilder.memory_point_examples_section)
SystemPromptBuilder.register_section('example_output')(SystemPromptBuilder.example_output_section)
SystemPromptBuilder.register_section('input_context')(SystemPromptBuilder.input_context_section)
SystemPromptBuilder.register_section('finalization_protocol')(SystemPromptBuilder.finalization_protocol_section)

class ClarificationManager:
    """Handles clarification logic for the agent."""
    @staticmethod
    def needs_clarification(agent_response: dict) -> bool:
        return bool(agent_response.get('questions'))

    @staticmethod
    def get_questions(agent_response: dict) -> List[str]:
        return agent_response.get('questions', [])

    @staticmethod
    def update_clarification_qas(clarification_qas: List[Tuple[str, str]], questions: List[str]) -> List[Tuple[str, str]]:
        answers = []
        for q in questions:
            user_print(q, color=YELLOW)
            a = input(f"Your answer to '{q}': ")
            answers.append((q, a))
        return clarification_qas + answers

class OutputFormatter:
    """Validates and formats the final output."""
    @staticmethod
    def format(agent_response: dict, original_notes: list = None) -> LLMOutput:
        entries = []
        for idx, e in enumerate(agent_response.get('entries', [])):
            # If raw_text is missing, try to fill it from original_notes
            if 'raw_text' not in e and original_notes and idx < len(original_notes):
                e['raw_text'] = original_notes[idx]
            entries.append(DataEntry(**e))
        new_memory_points = agent_response.get('new_memory_points', [])
        return LLMOutput(entries=entries, new_memory_points=new_memory_points)

class LLMAgent:
    _schema = None
    _parameters = None
    """
    Modular LLM agent using AgentCore for conversation and tool orchestration.
    Handles memory, prompt building, clarification loop, and structured output.
    Now uses two tools: 'clarification_tool' for clarification questions, and 'finalize_notes_tool' for final output.
    Accepts a classification_config for allowed entity_types and intents.
    If temperature=0.0, output is deterministic (recommended for tests).
    Loads output schema, agent parameters, and scoring metrics from YAML for consistency.
    """
    def __init__(self, notes: List[str], user_memory: List[str], classification_config: dict = None, max_clarification_rounds: int = None, debug_mode: bool = False, shared_context: Optional[dict] = None, temperature: float = None, use_color: bool = True):
        self.notes = notes
        self.user_memory = user_memory
        self.classification_config = classification_config or {}
        # Load schema and parameters if not already loaded
        if not LLMAgent._schema:
            LLMAgent._schema = load_schema_from_yaml("resources/notes_output_schema.yaml")
        if not LLMAgent._parameters:
            LLMAgent._parameters = load_parameters_from_yaml("resources/agent_parameters.yaml")
        self.schema = LLMAgent._schema
        self.parameters = LLMAgent._parameters
        # scoring_metrics is now always sourced from schema
        self.scoring_metrics = self.schema.get('scoring_metrics', {})
        # Use parameters for agent config
        self.max_clarification_rounds = max_clarification_rounds if max_clarification_rounds is not None else self.parameters['max_clarification_rounds']['value']
        self.debug_mode = debug_mode
        self.shared_context = shared_context or {}
        self.temperature = temperature if temperature is not None else self.parameters['temperature']['value']
        self.use_color = use_color
        self.llm = ChatOpenAI(model="gpt-4.1-mini", openai_api_key=os.getenv("OPENAI_API_KEY"), temperature=self.temperature)
        self.tools = [
            self._get_finalize_notes_tool(),
            self._get_ask_user_tool()
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
            debug_mode=self.debug_mode,
            logger=log,
            printer=user_print
        )

    def _get_finalize_notes_tool(self) -> ToolDefinition:
        def finalize_notes(entries=None, new_memory_points=None, shared_context=None):
            if entries is None:
                entries = []
            if new_memory_points is None:
                new_memory_points = []
            return {
                "entries": entries,
                "new_memory_points": new_memory_points
            }
        return ToolDefinition(
            name="finalize_notes",
            description="Returns the final structured interpretation and enrichment of all notes.",
            schema={
                "type": "object",
                "properties": {
                    "entries": {"type": "array", "items": {"type": "object"}},
                    "new_memory_points": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["entries", "new_memory_points"]
            },
            function=finalize_notes
        )

    def _get_ask_user_tool(self) -> ToolDefinition:
        def ask_user(questions=None, shared_context=None):
            if questions is None:
                questions = []
            return {
                "questions": questions
            }
        return ToolDefinition(
            name="ask_user",
            description="Poses clarification questions to the user in a structured way.",
            schema={
                "type": "object",
                "properties": {
                    "questions": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["questions"]
            },
            function=ask_user
        )

    def run(self) -> LLMOutput:
        clarification_qas = []
        archive_done = False
        tool_call_log = []  # Collect tool call logs for summary if needed
        conversation_history = []
        try:
            # Build initial system prompt
            system_prompt = SystemPromptBuilder.build(
                self.user_memory,
                self.notes,
                classification_config=self.classification_config,
                extra_context={"clarification_qas": clarification_qas},
                schema=self.schema,
                parameters=self.parameters,
                scoring_metrics=self.scoring_metrics
            )
            conversation_history.append({"role": "system", "content": system_prompt})
            for round_num in range(self.max_clarification_rounds):
                # Build user message (context for this round)
                user_context = SystemPromptBuilder.build(
                    self.user_memory,
                    self.notes,
                    classification_config=self.classification_config,
                    extra_context={"clarification_qas": clarification_qas},
                    schema=self.schema,
                    parameters=self.parameters,
                    scoring_metrics=self.scoring_metrics
                )
                conversation_history.append({"role": "user", "content": user_context})
                if self.debug_mode:
                    log.debug("\n-------- SYSTEM PROMPT (round %d) --------\n%s\n------------------------------------------\n" % (round_num+1, user_context))
                # Pass full conversation history to AgentCore
                response = self.agent_core.handle_user_message(conversation_history)
                if self.debug_mode:
                    log.debug("\n-------- LLM RESPONSE --------\n%s\n------------------------------\n" % str(response))
                # Append assistant/tool response to history
                if response["type"] == "tool_call" and response["tool_details"]:
                    tool_name = response["tool_details"]["name"]
                    tool_output = response["display_message"]
                    try:
                        if (not tool_output or tool_output == "") and response["tool_details"] and "args" in response["tool_details"]:
                            output_data = response["tool_details"]["args"]
                        else:
                            output_data = json.loads(tool_output) if isinstance(tool_output, str) else tool_output
                        # --- INTERAKTÍV LOG ---
                        user_print(f"\n[TOOL INVOKED] {tool_name} with args: {json.dumps(output_data, ensure_ascii=False)}", color=CYAN, bold=True)
                        tool_call_log.append({"tool": tool_name, "args": output_data})
                        log.info(f"[TOOL INVOKED] {tool_name} with args: {json.dumps(output_data, ensure_ascii=False)}")
                        # Add tool call as assistant message
                        conversation_history.append({
                            "role": "assistant",
                            "content": f"TOOL CALL: {tool_name} with args: {json.dumps(output_data, ensure_ascii=False)}"
                        })
                        if tool_name == "ask_user":
                            questions = output_data.get("questions", [])
                            if questions:
                                user_print("\n[ASK_USER] The agent has the following questions for you:", color=YELLOW, bold=True)
                                for i, q in enumerate(questions, 1):
                                    user_print(f"{i}: {q}", color=YELLOW)
                            answers = []
                            for i, q in enumerate(questions, 1):
                                a = input(f"Your answer to '{q}': ")
                                answers.append((q, a))
                            clarification_qas.extend(answers)
                            # Add Q&A as assistant message for LLM context
                            for q, a in answers:
                                conversation_history.append({
                                    "role": "assistant",
                                    "content": f"Clarification Q&A: Q: {q}  A: {a}"
                                })
                            continue  # Next round with updated Q&A
                        elif tool_name == "finalize_notes":
                            user_print("\n[FINALIZE_NOTES] The agent is finalizing the output.", color=GREEN, bold=True)
                            final_output = OutputFormatter.format(output_data, original_notes=self.notes)
                            final_output.tool_calls = tool_call_log
                            if self.debug_mode:
                                # Pretty-print final output
                                if hasattr(final_output, "model_dump_json"):
                                    output_str = final_output.model_dump_json(indent=2)
                                else:
                                    try:
                                        output_str = json.dumps(final_output, indent=2, ensure_ascii=False)
                                    except Exception:
                                        output_str = str(final_output)
                                log.debug(f"\n-------- FINAL OUTPUT --------\n{output_str}\n------------------------------\n")
                            return final_output
                    except Exception as e:
                        log.error(f"[LLMAgent] Failed to parse tool output: {e}. Raw output: {tool_output}")
                        continue
                else:
                    # If not a tool call, treat as clarification request or message
                    user_print(f"[LLM MESSAGE] {response['display_message']}", color=BLUE)
                    user_input = input("Your answer: ")
                    clarification_qas.append((response["display_message"], user_input))
                    # Add Q&A as assistant message for LLM context
                    conversation_history.append({
                        "role": "assistant",
                        "content": f"Clarification Q&A: Q: {response['display_message']}  A: {user_input}"
                    })
                    continue
            # If max rounds reached, finalize with placeholders
            log.warning("Maximum clarification rounds reached. Finalizing with placeholders if needed.")
            entries = [DataEntry(interpreted_text="UNDEFINED", entity_type="UNDEFINED", intent="UNDEFINED", clarity_score=0, raw_text="UNDEFINED")]
            new_memory_points = ["Clarification incomplete. Some fields may be undefined."]
            final_output = LLMOutput(entries=entries, new_memory_points=new_memory_points)
            final_output.tool_calls = tool_call_log
            if self.debug_mode:
                if hasattr(final_output, "model_dump_json"):
                    output_str = final_output.model_dump_json(indent=2)
                else:
                    try:
                        output_str = json.dumps(final_output, indent=2, ensure_ascii=False)
                    except Exception:
                        output_str = str(final_output)
                log.debug(f"\n-------- FINAL OUTPUT (FALLBACK) --------\n{output_str}\n------------------------------------------\n")
            return final_output
        finally:
            # Always archive the log at the end of run
            if self.debug_mode:
                log_dir = "logs"
                log_filename = os.path.join(log_dir, "llm_agent_debug.log")
                import shutil
                import datetime
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
                archive_filename = os.path.join(log_dir, f"llm_agent_debug_{timestamp}.log")
                try:
                    if os.path.exists(log_filename):
                        shutil.copyfile(log_filename, archive_filename)
                except Exception as e:
                    pass

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
    user_print(output.model_dump_json(indent=2), color=CYAN) 