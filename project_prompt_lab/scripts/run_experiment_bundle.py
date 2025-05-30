import yaml
import os
from pathlib import Path
import sys
from typing import Any, Dict
from datetime import datetime

# Add project_prompt_lab to sys.path for prompt_lab imports
ROOT = Path(__file__).resolve().parent.parent  # project_prompt_lab
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Dummy LLM osztály
class DummyLLM:
    """
    Egyszerű determinisztikus LLM, amely az input alapján visszaad egy fix vagy sablonos választ.
    """
    def __init__(self):
        pass

    def run(self, prompt: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        # Példaként: visszaadja az input note-ot, clarity_score=50
        note = input_data.get("note", "")
        return {
            "clarity_score": 50,
            "interpreted_text": note.upper() if note else None
        }

# Output validátor importálása
from prompt_lab.libs.output_validator import validate_output

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

def load_input(input_section: Dict[str, Any], base_dir: Path) -> Dict[str, Any]:
    fmt = input_section.get('format', 'yaml')
    content = input_section.get('content')
    if fmt == 'yaml':
        return content
    elif fmt == 'csv':
        csv_path = base_dir / content['file']
        import csv
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            # Csak az első sort vesszük (egyes input)
            return next(reader)
    else:
        raise ValueError(f"Unsupported input format: {fmt}")

def main(bundle_path: str):
    base_dir = Path(bundle_path).parent
    bundle = load_bundle(bundle_path)

    # 1. Prompt betöltése
    prompt = load_prompt(bundle['prompt'], base_dir)

    # 2. Input betöltése
    input_data = load_input(bundle['input'], base_dir)

    # 3. Dummy LLM inicializálása
    llm = DummyLLM()

    # 4. Lefuttatás
    actual_output = llm.run(prompt, input_data)

    # 5. Validáció
    expected_output = bundle.get('expected_output', {})
    validation_result = validate_output(actual_output, expected_output)

    # 6. Log generálása (mindig az agent saját 05_logs mappájába)
    # Feltételezzük, hogy a bundle_path szerkezete: .../agents/<agent>/03_experiment_bundles/<bundle>.yaml
    agent_dir = base_dir.parent.parent  # .../agents/<agent>
    logs_dir = agent_dir / "05_logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_path = logs_dir / f"{Path(bundle_path).stem}__log.md"
    log_content = f"# Log for {Path(bundle_path).stem}\n\nPrompt: {prompt}\n\nInput: {input_data}\n\nActual output: {actual_output}\n\nValidation: {validation_result}\n"
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(log_content)

    # 7. Metaadatok
    meta = bundle.get('meta', {}).copy() if 'meta' in bundle else {}
    meta['last_run'] = datetime.now().isoformat(timespec='seconds')
    meta['runner'] = os.environ.get('USER', 'runner')

    # 8. Result bundle létrehozása (új fájl, __result.yaml utótaggal)
    result_bundle = bundle.copy()
    result_bundle['actual_output'] = actual_output
    result_bundle['validation'] = {'result': validation_result}
    result_bundle['log'] = {'status': validation_result['status'], 'path': str(log_path.relative_to(agent_dir))}
    result_bundle['meta'] = meta

    result_path = Path(bundle_path).with_name(f"{Path(bundle_path).stem}__result.yaml")
    save_bundle(result_path, result_bundle)

    print(f"✓ Result bundle létrehozva: {result_path}")
    print(f"  Status: {validation_result['status']}")
    print(f"  Log: {log_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Használat: python run_experiment_bundle.py <bundle.yaml>")
        sys.exit(1)
    main(sys.argv[1]) 