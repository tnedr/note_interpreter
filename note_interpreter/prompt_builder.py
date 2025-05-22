import yaml
import json
from note_interpreter.log import log
from typing import List, Optional, Dict, Callable, Any

class PromptBuilder:
    """
    Általános, szekció-alapú, registry-s prompt builder.
    - Szekciók: minden szekció egy függvény, amelyet a registry tart nyilván.
    - Config: YAML/JSON file írja le a szekciók sorrendjét, engedélyezettségét, szövegét.
    - Context: tetszőleges dict, minden kulcsa placeholderként használható a promptban.
    - Bővíthető: új szekciók decoratorral, új context mezők context dict-tel.
    - Nincs domain-specifikus logika, minden projektben/agentnél használható.

    Használat:
        prompt = PromptBuilder.build(
            context={
                "notes": notes,
                "memory": memory,
                "threshold": 80,
                "agent_name": "ClarifyAgent"
            },
            config_path="resources/clarify_agent/prompt_config.yaml"
        )
    """
    section_registry: Dict[str, Callable[[dict, dict], str]] = {}

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
        'communication_strategy': 'COMMUNICATION STRATEGY',
        'constraints': 'CONSTRAINTS',
        'reasoning_style': 'REASONING STYLE / HEURISTICS',
        'meta_behavior': 'META BEHAVIOR / FALLBACK',
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

    @staticmethod
    def serialize_value(val):
        if isinstance(val, list):
            return "\n".join([f"- {v}" for v in val])
        elif isinstance(val, dict):
            return json.dumps(val, indent=2, ensure_ascii=False)
        elif val is None:
            return "(none)"
        else:
            return str(val)

    @classmethod
    def fill_placeholders(cls, text, context: dict):
        # context kulcsai: minden átadott paraméter
        for key, value in context.items():
            text = text.replace(f"{{{key}}}", cls.serialize_value(value))
        return text

    @classmethod
    def build(cls, context: dict, config_path: str) -> str:
        """
        context: dict, minden kulcsa placeholderként használható
        config_path: YAML vagy JSON file, amely a szekciókat írja le
        """
        import re
        with open(config_path, 'r', encoding='utf-8') as f:
            if config_path.endswith('.json'):
                config = json.load(f)
            else:
                config = yaml.safe_load(f)
        sections = config.get('sections', [])
        prompt_parts = []
        for section in sections:
            if not section.get('enabled', True):
                continue
            name = section['name']
            params = section.get('params', {})
            custom_text = section.get('custom_text')
            # Separator: szekció neve nagybetűvel, szóköz helyett _
            header = re.sub(r'_', ' ', name).upper()
            separator = f"------------ {header} ------------"
            prompt_parts.append(separator)
            if custom_text:
                prompt_parts.append(cls.fill_placeholders(custom_text, context))
                continue
            func = cls.section_registry.get(name)
            if func:
                try:
                    part = func(params, context)
                    prompt_parts.append(part)
                except Exception as e:
                    prompt_parts.append(f"[ERROR in section '{name}']: {e}")
            else:
                prompt_parts.append(f"[WARNING: section '{name}' not found in registry]")
        prompt = "\n\n".join([p for p in prompt_parts if p])
        return prompt

# --- Példa szekció-regisztráció ---
@PromptBuilder.register_section('intro')
def intro_section(params, context):
    return f"# 🤖 {context.get('agent_name', 'Agent')}\n{context.get('agent_description', '')}"

# További szekciókat a felhasználó bővíthet decoratorral.

# --- Section Implementations and Registry ---

# Példa szekciók (a teljes lista az llm_agent.py-ból átmásolandó):

@PromptBuilder.register_section('goals')
def goals_section(params, context):
    return ("## 🎯 Your Goals\n\n"
            "For each input note, your output must include:\n"
            "1. **Structured JSON Output** via the `finalize_notes` tool, always including:\n"
            "   - `entries`: interpreted notes with enriched metadata\n"
            "   - `new_memory_points`: long-term memory insights (natural language bullet points)\n"
            "2. If you are uncertain, you MUST use the `ask_user` tool to ask clarification questions BEFORE finalizing.\n"
            "3. You MUST use the tools – never respond in plain text.\n"
    )

@PromptBuilder.register_section('output_schema_and_meanings')
def output_schema_and_meanings_section(params, context):
    schema_file = params.get('schema_file', 'resources/single_agent/notes_output_schema.yaml')
    import yaml as _yaml
    with open(schema_file, 'r', encoding='utf-8') as f:
        schema = _yaml.safe_load(f)
    section = "## 📌 Structured Output Schema & Field Meanings\n\nEach entry must have the following fields:\n\n"
    for field, info in schema.get('DataEntry', {}).items():
        section += f"- `{field}` ({info.get('type','')}): {info.get('description','')}\n"
    return section

@PromptBuilder.register_section('classification')
def classification_section(params, context):
    classification_config = context['classification_config']
    entity_types = classification_config.get("entity_types", [])
    intents = classification_config.get("intents", [])
    return (
        "## 🏷️ Allowed Classifications\n\n"
        f"**Entity Types:** {', '.join(entity_types)}\n"
        f"**Intents:** {', '.join(intents)}\n"
    )

@PromptBuilder.register_section('scoring_guidelines')
def scoring_guidelines_section(params, context):
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

@PromptBuilder.register_section('parameter_explanations')
def parameter_explanations_section(params, context):
    parameters = context['parameters']
    section = "## ⚙️ Agent Parameters\n\n"
    for param, info in parameters.items():
        section += f"- `{param}` = {info['value']} ({info['description']})\n"
    return section

@PromptBuilder.register_section('output_validation_rules')
def output_validation_rules_section(params, context):
    return (
        "## 🔒 Output Validation Rules (Mandatory)\n\n"
        "- You MUST return a valid JSON object calling either `ask_user` or `finalize_notes`.\n"
        "- You MUST use the tools for all communication.\n"
        "- Never return plain text or unstructured answers.\n"
        "- For `finalize_notes`, always include both `entries` and `new_memory_points` (even if empty).\n"
        "- For `ask_user`, always include at least one question.\n"
    )

@PromptBuilder.register_section('tool_json_schema')
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

@PromptBuilder.register_section('tool_behavior_summary')
def tool_behavior_summary_section(params, context):
    return (
        "## 🛠️ Tool Behavior Summary\n\n"
        "- `ask_user(...)`: Use this tool to ask the user clarification questions. Do **not** finalize the output until you have the answers.\n"
        "- `finalize_notes(...)`: Use this tool only when you are confident in your interpretation and all necessary clarifications have been made.\n"
        "- Never respond in plain text or unstructured answers.\n"
    )

@PromptBuilder.register_section('context_usage')
def context_usage_section(params, context):
    return (
        "## 🧠 Context Usage\n\n"
        "- Use **user memory** to resolve ambiguity and improve interpretation.\n"
        "- Use **context from other notes** in the batch only if relevant.\n"
        "- Always aim for clarity and actionability.\n"
    )

@PromptBuilder.register_section('clarification_protocol')
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

@PromptBuilder.register_section('memory_update')
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

@PromptBuilder.register_section('memory_point_examples')
def memory_point_examples_section(params, context):
    return (
        "## 📘 Memory Point Examples\n\n"
        "* Tamas is currently working on a Q3 marketing launch plan and often refers to it simply as 'plan.'\n"
        "* Tamas prefers to phrase actionable notes starting with verbs like 'continue,' 'email,' or 'draft.'\n"
        "* Tamas uses the term 'LifeOS' to refer to his integrated personal operating system project.\n"
    )

@PromptBuilder.register_section('example_output')
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

@PromptBuilder.register_section('input_context')
def input_context_section(params, context):
    memory = context['memory']
    notes = context['notes']
    clarification_batches = context['extra_context'].get('clarification_qas') or context['extra_context'].get('clarification_clarification_batches')
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
    if clarification_batches:
        section += "### Clarification batches so far:\n"
        for batch_num, batch in enumerate(clarification_batches, 1):
            qs = batch.get("questions", [])
            resp = batch.get("response", "")
            section += f"Batch {batch_num}:\n"
            for i, q in enumerate(qs, 1):
                section += f"  Q{i}: {q}\n"
            section += f"  User response: {resp}\n"
    return section

@PromptBuilder.register_section('finalization_protocol')
def finalization_protocol_section(params, context):
    return (
        "## 🛑 Finalization Protocol\n\n"
        "- After providing the final structured output, do not ask further questions. The conversation is finished.\n"
        "- Never respond in plain text at any stage.\n"
        "- If no clear interpretation is possible after all clarification rounds:\n"
        "  - Use `\"UNDEFINED\"` for any field that cannot be confidently determined.\n"
        "  - Still call the `finalize_notes` with all fields included.\n"
    )

@PromptBuilder.register_section('communication_strategy')
def communication_strategy_section(params, context):
    return params.get('custom_text', '')

@PromptBuilder.register_section('constraints')
def constraints_section(params, context):
    return params.get('custom_text', '')

@PromptBuilder.register_section('reasoning_style')
def reasoning_style_section(params, context):
    return params.get('custom_text', '')

@PromptBuilder.register_section('meta_behavior')
def meta_behavior_section(params, context):
    return params.get('custom_text', '') 