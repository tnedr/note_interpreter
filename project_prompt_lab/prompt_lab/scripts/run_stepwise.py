import sys
from pathlib import Path
import yaml

sys.path.append(str(Path(__file__).resolve().parent.parent / "libs"))
from stepwise_manager import StepwisePlanManager
from prompt_builder import PromptBuilder

AGENT_DIR = Path(__file__).parent.parent / "agents" / "grocery_clarifier"
PLAN_FILE = AGENT_DIR / "plan.yaml"

# Dummy LLM for demo

def dummy_llm(prompt: str, step_name: str) -> dict:
    # Simulate output based on step
    if step_name == "step_01_scoring":
        return {"clarity_score": 60}
    elif step_name == "step_02_clarification":
        return {"clarity_score": 60, "clarification_question": "Mit értesz tej alatt?"}
    return {}

def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def main():
    plan = StepwisePlanManager(PLAN_FILE)
    plan.print_plan_summary()
    print("\n--- Stepwise execution ---\n")
    for step in plan.steps:
        print(f"[STEP] {step['step_name']} - {step.get('goal','')}")
        prompt_path = AGENT_DIR / step['prompt_file']
        prompt_config = load_yaml(prompt_path)
        prompt_template = prompt_config.get("system", "")
        for exp_path in step.get('experiment_cases', []):
            exp_file = AGENT_DIR / exp_path
            experiment = load_yaml(exp_file)
            context = experiment.get("input", {})
            expected = experiment.get("expected", {})
            prompt = prompt_template.format(**context)
            print(f"  [EXPERIMENT] {exp_path}")
            print(f"    Prompt: {prompt}")
            output = dummy_llm(prompt, step['step_name'])
            print(f"    Output: {output}")
            if output == expected:
                print("    [PASS] Output matches expected.")
            else:
                print(f"    [FAIL] Output does not match expected.\n      Expected: {expected}\n      Got: {output}")
    print("\n--- Done ---")

if __name__ == "__main__":
    main() 