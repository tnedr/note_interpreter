import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import yaml
import pytest
from prompt_lab.libs.stepwise_manager import StepwisePlanManager

AGENT_DIR = Path(__file__).resolve().parent.parent / "prompt_lab" / "agents" / "grocery_clarifier"
PLAN_FILE = AGENT_DIR / "plan.yaml"

# Dummy LLM for test

def dummy_llm(prompt: str, step_name: str) -> dict:
    if step_name == "step_01_scoring":
        return {"clarity_score": 60}
    elif step_name == "step_02_clarification":
        return {"clarity_score": 60, "clarification_question": "Mit értesz tej alatt?"}
    return {}

def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

@pytest.skip("DEPRECATED: Stepwise pipeline teszt, experience bundle váltás miatt nem karbantartott.", allow_module_level=True)
# DEPRECATED: Stepwise pipeline teszt, experience bundle váltás miatt nem karbantartott.
def test_stepwise_pipeline():
    plan = StepwisePlanManager(PLAN_FILE)
    for step in plan.steps:
        prompt_path = AGENT_DIR / step['prompt_file']
        prompt_config = load_yaml(prompt_path)
        prompt_template = prompt_config.get("system", "")
        for exp_path in step.get('experiment_cases', []):
            exp_file = AGENT_DIR / exp_path
            experiment = load_yaml(exp_file)
            context = experiment.get("input", {})
            expected = experiment.get("expected", {})
            prompt = prompt_template.format(**context)
            output = dummy_llm(prompt, step['step_name'])
            assert output == expected, f"Step {step['step_name']} experiment {exp_path} failed: {output} != {expected}" 