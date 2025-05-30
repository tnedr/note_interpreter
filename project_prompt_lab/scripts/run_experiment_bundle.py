# pipenv run python project_prompt_lab/scripts/run_experiment_bundle.py project_prompt_lab/prompt_lab/agents/grocery_clarifier/03_experiment_bundles/experiment_dummy_explicit.yaml
import sys
import os
import yaml
from typing import Any, Dict
from datetime import datetime
from pathlib import Path
import importlib.util
from project_prompt_lab.prompt_lab.libs.prompt_builder import PromptBuilder
from project_prompt_lab.prompt_lab.libs.log import log
from project_prompt_lab.prompt_lab.libs.output_validator import validate_output


# Dummy LLM osztály
class DummyLLM:
    """
    Egyszerű determinisztikus LLM, amely az input alapján visszaad egy fix vagy sablonos választ.
    """
    def __init__(self, output=None):
        self.output = output

    def run(self, prompt: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        if self.output is not None:
            return self.output
        note = input_data.get("note", "")
        return {
            "clarity_score": 50,
            "interpreted_text": note.upper() if note else None
        }



def load_bundle(bundle_path: str) -> Dict[str, Any]:
    with open(bundle_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def save_bundle(bundle_path: str, bundle: Dict[str, Any]):
    with open(bundle_path, 'w', encoding='utf-8') as f:
        yaml.dump(bundle, f, allow_unicode=True, sort_keys=False)

def load_prompt(prompt_section: Dict[str, Any], base_dir: Path) -> str:
    if prompt_section.get('text'):
        return prompt_section['text']
    elif prompt_section.get('source'):
        prompt_path = base_dir / prompt_section['source']
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        raise ValueError("No prompt text or source specified.")

def load_input(input_section: Dict[str, Any], base_dir: Path) -> Any:
    fmt = input_section.get('format', 'yaml')
    content = input_section.get('content')
    if fmt == 'yaml':
        return content
    elif fmt == 'csv':
        csv_path = base_dir / content['file']
        with open(csv_path, 'r', encoding='utf-8') as f:
            # Fejléc nélkül, minden sort egy listába
            lines = [line.strip() for line in f if line.strip()]
        # Egyetlen stringként adja vissza, sortöréssel elválasztva
        return '\n'.join(lines)
    else:
        raise ValueError(f"Unsupported input format: {fmt}")

def main(bundle_path: str):
    base_dir = Path(bundle_path).parent
    bundle = load_bundle(bundle_path)

    # 1. Prompt betöltése
    prompt = load_prompt(bundle['prompt'], base_dir)

    # 2. Input betöltése
    input_data = load_input(bundle['input'], base_dir)

    # 3. LLM inicializálása (új séma szerint)
    model = bundle.get('model')
    if not model or 'type' not in model:
        raise ValueError("A bundle 'model' mezője kötelező, és tartalmaznia kell a 'type'-ot!")
    if model['type'] == 'dummy':
        dummy_output = None
        if 'output' in model:
            dummy_output = model['output']
        elif 'output_file' in model:
            dummy_output_path = base_dir / model['output_file']
            if dummy_output_path.suffix.lower() in ('.yaml', '.yml'):
                with open(dummy_output_path, 'r', encoding='utf-8') as f:
                    dummy_output = yaml.safe_load(f)
            elif dummy_output_path.suffix.lower() == '.csv':
                import csv
                with open(dummy_output_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    dummy_output = next(reader)
            else:
                raise ValueError(f"Unsupported dummy output_file format: {dummy_output_path.suffix}")
        else:
            raise ValueError("Dummy model-hez kötelező az 'output' vagy 'output_file' mező!")
        llm = DummyLLM(output=dummy_output)
        actual_output = llm.run(prompt, input_data)
    elif model['type'] == 'llm':
        if 'provider' not in model or 'name' not in model:
            raise ValueError("LLM model-hez kötelező a 'provider' és 'name' mező!")
        # Dinamikus agent import az agent könyvtárból
        agent_dir = base_dir.parent  # .../agents/<agent>
        agent_py = agent_dir / 'agent.py'
        if not agent_py.exists():
            raise FileNotFoundError(f"Nem található agent.py: {agent_py}")
        spec = importlib.util.spec_from_file_location("agent_module", str(agent_py))
        agent_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(agent_module)
        # Az első olyan osztály, ami 'Agent'-re végződik
        agent_class = next(
            cls for name, cls in vars(agent_module).items()
            if isinstance(cls, type) and name.endswith('Agent')
        )
        # PromptBuilder-rel generált system prompt
        # Ha batch CSV input, akkor a promptban {csv}-t cseréljük input_data-ra
        if bundle['input']['format'] == 'csv' and '{csv}' in prompt:
            prompt_filled = prompt.replace('{csv}', input_data)
            context = {'csv': input_data}
        else:
            prompt_filled = prompt
            context = bundle['input']['content']
        prompt_config_path = bundle['prompt'].get('config_path')
        if prompt_config_path:
            system_prompt = PromptBuilder.build(context, prompt_config_path)
        else:
            system_prompt = prompt_filled
        # Initial user message a bundle-ből (ha nincs, legyen üres string)
        initial_message = bundle.get('initial_message', "")
        log.info(f"System prompt (PromptBuilder):\n{system_prompt}")
        log.info(f"Initial user message: {initial_message}")
        agent = agent_class(
            api_key=os.getenv("OPENAI_API_KEY"),
            llm_model=model['name'],
            system_prompt=system_prompt
        )
        response = agent.handle_user_message(initial_message)
        actual_output = {
            'display_message': response.get('display_message'),
            'parsed_response': response.get('parsed_response'),
            'raw_response': response.get('raw_response')
        }
    else:
        raise ValueError(f"Ismeretlen model.type: {model['type']}")

    # 4. Validáció
    expected_output = bundle.get('expected_output', {})
    validation_result = validate_output(actual_output, expected_output)

    # 5. Log generálása (mindig az agent saját 05_logs mappájába)
    agent_dir = base_dir.parent  # .../agents/<agent>
    logs_dir = agent_dir / "05_logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_path = logs_dir / f"{Path(bundle_path).stem}__log.md"
    log_content = f"# Log for {Path(bundle_path).stem}\n\nPrompt: {prompt}\n\nInput: {input_data}\n\nActual output: {actual_output}\n\nValidation: {validation_result}\n"
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(log_content)

    # 6. Metaadatok
    meta = bundle.get('meta', {}).copy() if 'meta' in bundle else {}
    meta['last_run'] = datetime.now().isoformat(timespec='seconds')
    meta['runner'] = os.environ.get('USER', 'runner')

    # 7. Result bundle létrehozása (eredeti YAML + result szekciók)
    result_sections = {
        'actual_output': actual_output,
        'validation': {'result': validation_result},
        'log': {'status': validation_result['status'], 'path': str(log_path.relative_to(agent_dir))},
        'meta': meta
    }
    result_yaml = yaml.dump(result_sections, allow_unicode=True, sort_keys=False)
    with open(bundle_path, 'r', encoding='utf-8') as f:
        original_yaml = f.read().rstrip()
    result_path = Path(bundle_path).with_name(f"{Path(bundle_path).stem}__result.yaml")
    with open(result_path, 'w', encoding='utf-8') as f:
        f.write(original_yaml + '\n\n' + result_yaml)

    print(f"✓ Result bundle létrehozva: {result_path}")
    print(f"  Status: {validation_result['status']}")
    print(f"  Log: {log_path}")

if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            print("Használat: python run_experiment_bundle.py <bundle.yaml>")
            sys.exit(1)
        main(sys.argv[1])
    except Exception as e:
        import traceback
        log.error(f"Hiba a futás során: {e}")
        traceback.print_exc()
        print(f"[ERROR] {e}")
        print("A részletes hibát lásd a logfájlban, ha készült.") 