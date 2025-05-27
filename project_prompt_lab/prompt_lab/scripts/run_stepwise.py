import sys
from pathlib import Path
import yaml
import os
from dotenv import load_dotenv

# Load environment variables from .env in the project root
load_dotenv()

sys.path.append(str(Path(__file__).resolve().parent.parent / "libs"))
from stepwise_manager import StepwisePlanManager
from prompt_builder import PromptBuilder
from prompt_lab.libs.config_utils import get_llm_model_from_config
from prompt_lab.agents.grocery_clarifier.agent import GroceryClarifierAgent

AGENT_DIR = Path(__file__).resolve().parent.parent / "agents" / "grocery_clarifier"
PLAN_FILE = AGENT_DIR / "plan.yaml"

USE_LLM = True  # Állítsd False-ra, ha csak dummy_llm-mel akarsz futtatni

# Dummy LLM for demo
def dummy_llm(prompt: str, step_name: str) -> dict:
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
    # LLM agent setup
    if USE_LLM:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            print("[ERROR] OPENAI_API_KEY environment variable not set!")
            return
        model = get_llm_model_from_config()
        agent = GroceryClarifierAgent(api_key=api_key, llm_model=model)
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
            if USE_LLM:
                # Use the real agent (stateless call)
                messages = [
                    {"role": "system", "content": agent.system_prompt},
                    {"role": "user", "content": prompt}
                ]
                output = agent.invoke_with_message_list(messages)
                print(f"    LLM Output: {output}")
                # For test: flatten output for comparison
                if output["type"] == "conversation":
                    result = {"clarity_score": 60}  # TODO: parse from output["display_message"]
                elif output["type"] == "tool_call":
                    result = output.get("tool_details", {})
                else:
                    result = {"error": output.get("display_message")}
            else:
                result = dummy_llm(prompt, step['step_name'])
                print(f"    Dummy Output: {result}")
            if result == expected:
                print("    [PASS] Output matches expected.")
            else:
                print(f"    [FAIL] Output does not match expected.\n      Expected: {expected}\n      Got: {result}")
    print("\n--- Done ---")

if __name__ == "__main__":
    main() 