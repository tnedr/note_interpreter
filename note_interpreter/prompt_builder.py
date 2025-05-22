import yaml
import json
from note_interpreter.log import log
from typing import List, Optional, Dict, Callable, Any

# --- Placeholder serialization utility ---
def serialize_value(val):
    if isinstance(val, list):
        return "\n".join([f"- {v}" for v in val])
    elif isinstance(val, dict):
        return json.dumps(val, indent=2, ensure_ascii=False)
    elif val is None:
        return "(none)"
    else:
        return str(val)

def fill_placeholders(text, context: dict):
    for key, value in context.items():
        text = text.replace(f"{{{key}}}", serialize_value(value))
    return text

class SystemPromptBuilder:
    """
    Config-driven, registry-based prompt builder. Each section is a function registered in a central registry.
    The prompt is built by reading a YAML config file that specifies the order, enabled/disabled state, and parameters for each section.
    Now adds a visible visual separator line before each major section for human clarity.
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

    @classmethod
    def build_from_config(cls, memory: List[str], notes: List[str], classification_config: dict = None, extra_context: Optional[dict] = None, schema: dict = None, parameters: dict = None, scoring_metrics: dict = None, config_path: str = "resources/single_agent/prompt_config.yaml") -> str:
        import re
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        sections = config.get('sections', [])
        log.debug(f"[DEBUG] Section order from config: {[section.get('name') for section in sections]}")
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
        schema_obj = schema or {}
        scoring_metrics_obj = schema_obj.get('scoring_metrics', {})
        context = {
            'notes': notes,
            'user_memory': memory,
            'clarification_history': (extra_context or {}).get('clarification_history', []),
            'extra_context': extra_context or {},
            'memory': memory,
            'classification_config': loaded_classification_config,
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
            header = cls.SECTION_HEADER_MAP.get(name)
            if not header:
                header = re.sub(r'_', ' ', name).upper()
            separator = f"------------ {header} ------------"
            prompt_parts.append(separator)
            if custom_text:
                prompt_parts.append(fill_placeholders(custom_text, context))
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
        if config_path is None:
            config_path = "resources/single_agent/prompt_config.yaml"
        return cls.build_from_config(memory, notes, classification_config, extra_context, schema, parameters, scoring_metrics, config_path)

# --- Section registry átmozgatása ---
# (A szekciók implementációit és regisztrációját is át kell mozgatni, ha szükséges) 