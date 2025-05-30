import yaml
import os
from pathlib import Path
import sys
from typing import Any, Dict

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
from project_prompt_lab.prompt_lab.libs.output_validator import validate_output

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

    # 6. Bundle frissítése
    bundle['actual_output'] = actual_output
    if 'validation' not in bundle:
        bundle['validation'] = {}
    bundle['validation']['result'] = validation_result
    if 'log' not in bundle:
        bundle['log'] = {}
    bundle['log']['status'] = validation_result['status']

    # 7. Mentés
    save_bundle(bundle_path, bundle)
    print(f"✓ Bundle lefuttatva és frissítve: {bundle_path}")
    print(f"  Status: {validation_result['status']}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Használat: python run_experiment_bundle.py <bundle.yaml>")
        sys.exit(1)
    main(sys.argv[1]) 