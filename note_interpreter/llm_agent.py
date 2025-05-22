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
from note_interpreter.prompt_builder import SystemPromptBuilder

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

class SingleAgent:
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
        if not SingleAgent._schema:
            SingleAgent._schema = load_schema_from_yaml("resources/single_agent/notes_output_schema.yaml")
        if not SingleAgent._parameters:
            SingleAgent._parameters = load_parameters_from_yaml("resources/single_agent/agent_parameters.yaml")
        self.schema = SingleAgent._schema
        self.parameters = SingleAgent._parameters
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
        tool_call_log = []  # Collect tool call logs for summary if needed
        try:
            for round_num in range(self.max_clarification_rounds):
                # Build fresh system prompt with all context and Q&A
                system_prompt = SystemPromptBuilder.build(
                    self.user_memory,
                    self.notes,
                    classification_config=self.classification_config,
                    extra_context={"clarification_qas": clarification_qas},
                    schema=self.schema,
                    parameters=self.parameters,
                    scoring_metrics=self.scoring_metrics
                )
                # Zero-shot: only system + user message
                conversation_history = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": "Proceed"}
                ]
                if self.debug_mode:
                    log.debug(f"\n-------- SYSTEM PROMPT (round {round_num+1}) --------\n{system_prompt}\n------------------------------------------\n")
                # Pass zero-shot conversation to AgentCore
                response = self.agent_core.invoke_with_message_list(conversation_history)
                if self.debug_mode:
                    log.debug(f"\n-------- LLM RESPONSE --------\n{str(response)}\n------------------------------\n")
                if response["type"] == "tool_call" and response["tool_details"]:
                    tool_name = response["tool_details"]["name"]
                    tool_output = response["display_message"]
                    try:
                        if (not tool_output or tool_output == "") and response["tool_details"] and "args" in response["tool_details"]:
                            output_data = response["tool_details"]["args"]
                        else:
                            output_data = json.loads(tool_output) if isinstance(tool_output, str) else tool_output
                        if self.debug_mode:
                            log.debug(f"[TOOL INVOKED] {tool_name} with args: {json.dumps(output_data, ensure_ascii=False)}")
                        log.info(f"[TOOL INVOKED] {tool_name} with args: {json.dumps(output_data, ensure_ascii=False)}")
                        if tool_name == "ask_user":
                            questions = output_data.get("questions", [])
                            if questions:
                                user_print("\n[ASK_USER] The agent has the following questions for you:", color=YELLOW, bold=True)
                                for i, q in enumerate(questions, 1):
                                    user_print(f"{i}: {q}", color=YELLOW)
                                user_print("\nPlease answer all questions in a single, free-form text. You may answer in any order or style; the agent will interpret your response.", color=YELLOW)
                                user_input = input("Your clarification response: ")
                                # Store the questions and the single free-form response
                                clarification_context = {
                                    "questions": questions,
                                    "response": user_input
                                }
                                clarification_qas.append(clarification_context)
                            continue  # Next round with updated clarification context
                        elif tool_name == "finalize_notes":
                            user_print("\n[FINALIZE_NOTES] The agent is finalizing the output.", color=GREEN, bold=True)
                            final_output = OutputFormatter.format(output_data, original_notes=self.notes)
                            final_output.tool_calls = tool_call_log
                            if self.debug_mode:
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
                    user_print(f"[LLM MESSAGE] {response['display_message']}", color=BLUE)
                    user_input = input("Your answer: ")
                    clarification_qas.append((response["display_message"], user_input))
                    continue
            log.warning("Maximum clarification rounds reached. Finalizing with placeholders if needed.")
            # Build a final system prompt with all Q&A and a note about max rounds
            final_note = f"You have reached the maximum of {self.max_clarification_rounds} clarification rounds. Please finalize your output, even if some fields are UNDEFINED. Number of clarification Q&A rounds: {len(clarification_qas)}."
            system_prompt = SystemPromptBuilder.build(
                self.user_memory,
                self.notes,
                classification_config=self.classification_config,
                extra_context={"clarification_qas": clarification_qas, "finalization_note": final_note},
                schema=self.schema,
                parameters=self.parameters,
                scoring_metrics=self.scoring_metrics
            )
            conversation_history = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Proceed"}
            ]
            if self.debug_mode:
                log.debug(f"\n-------- FINAL SYSTEM PROMPT (max rounds reached) --------\n{system_prompt}\n------------------------------------------\n")
            response = self.agent_core.invoke_with_message_list(conversation_history)
            if self.debug_mode:
                log.debug(f"\n-------- FINAL LLM RESPONSE (max rounds reached) --------\n{str(response)}\n------------------------------\n")
            if response["type"] == "tool_call" and response["tool_details"] and response["tool_details"]["name"] == "finalize_notes":
                tool_output = response["display_message"]
                try:
                    output_data = json.loads(tool_output) if isinstance(tool_output, str) else tool_output
                    user_print("\n[FINALIZE_NOTES] The agent is finalizing the output after max clarification rounds.", color=GREEN, bold=True)
                    final_output = OutputFormatter.format(output_data, original_notes=self.notes)
                    final_output.tool_calls = tool_call_log
                    if self.debug_mode:
                        if hasattr(final_output, "model_dump_json"):
                            output_str = final_output.model_dump_json(indent=2)
                        else:
                            try:
                                output_str = json.dumps(final_output, indent=2, ensure_ascii=False)
                            except Exception:
                                output_str = str(final_output)
                        log.debug(f"\n-------- FINAL OUTPUT (AFTER MAX ROUNDS) --------\n{output_str}\n------------------------------------------\n")
                    return final_output
                except Exception as e:
                    log.error(f"[LLMAgent] Failed to parse tool output after max rounds: {e}. Raw output: {tool_output}")
            # If still not valid, fallback
            entries = [
                DataEntry(
                    raw_text=note,
                    interpreted_text="UNDEFINED",
                    entity_type="UNDEFINED",
                    intent="UNDEFINED",
                    clarity_score=0
                ) for note in self.notes
            ]
            new_memory_points = []
            output_dict = {
                "entries": entries,
                "new_memory_points": new_memory_points
            }
            # Optionally include Q&A if any
            if clarification_qas:
                output_dict["clarification_clarification_batches"] = clarification_qas
            # Build LLMOutput object
            final_output = LLMOutput(**output_dict)
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
    agent = SingleAgent(notes, user_memory)
    output = agent.run()
    user_print(output.model_dump_json(indent=2), color=CYAN) 