import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import os
import pytest
from pathlib import Path
import yaml
from prompt_lab.libs.stepwise_manager import StepwisePlanManager
from prompt_lab.libs.config_utils import get_llm_model_from_config
from prompt_lab.agents.grocery_clarifier.agent import GroceryClarifierAgent
import json

pytest.skip("DEPRECATED: Stepwise pipeline teszt, experience bundle váltás miatt nem karbantartott.", allow_module_level=True)
# DEPRECATED: Stepwise pipeline teszt, experience bundle váltás miatt nem karbantartott.

AGENT_DIR = Path(__file__).resolve().parent.parent / "prompt_lab" / "agents" / "grocery_clarifier"
PLAN_FILE = AGENT_DIR / "plan.yaml"

def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

@pytest.mark.llm_required
def test_stepwise_pipeline_real_llm():
    """
    Real LLM/system test: runs the stepwise pipeline with the real LLM agent.
    Skips if no OPENAI_API_KEY is set. Not intended for CI/CD or fast feedback.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        pytest.skip("No API key for real LLM test.")
    model = get_llm_model_from_config()
    agent = GroceryClarifierAgent(api_key=api_key, llm_model=model)
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
            messages = [
                {"role": "system", "content": agent.system_prompt},
                {"role": "user", "content": prompt}
            ]
            output = agent.invoke_with_message_list(messages)
            print("\n--- FULL LLM OUTPUT ---\n")
            print(json.dumps(output, indent=2, ensure_ascii=False, default=str))
            print("\n--- END FULL LLM OUTPUT ---\n")
            # Try to parse the full result from display_message
            result = None
            if output["type"] in ("conversation", "tool_call"):
                try:
                    result = json.loads(output["display_message"])
                except Exception:
                    # fallback to previous logic
                    if output["type"] == "tool_call":
                        result = output.get("tool_details", {})
                    else:
                        result = {"clarity_score": 60}
            else:
                result = {"error": output.get("display_message")}
            assert result == expected, f"Step {step['step_name']} experiment {exp_path} failed: {result} != {expected}" 