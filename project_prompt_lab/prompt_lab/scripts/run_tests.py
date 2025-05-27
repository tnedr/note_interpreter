import os
import yaml
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "libs"))
from prompt_builder import PromptBuilder

# --- Config ---
AGENT_DIR = Path(__file__).parent.parent / "agents" / "grocery_clarifier"
PROMPT_FILE = AGENT_DIR / "prompts" / "s3_v1.yaml"
TEST_CASE_FILE = AGENT_DIR / "test_cases" / "test_s3_01.yaml"

# --- Dummy LLM (just echoes the prompt for now) ---
def dummy_llm(prompt: str) -> dict:
    # In a real test, this would call an LLM. Here, we just simulate output.
    # For demo: always return a fixed clarity_score.
    return {"clarity_score": 60}

# --- Load prompt config (YAML) ---
def load_prompt_config(prompt_path):
    with open(prompt_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# --- Load test case (YAML) ---
def load_test_case(test_case_path):
    with open(test_case_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# --- Main test runner ---
def main():
    print(f"[INFO] Loading prompt: {PROMPT_FILE}")
    prompt_config = load_prompt_config(PROMPT_FILE)
    print(f"[INFO] Loading test case: {TEST_CASE_FILE}")
    test_case = load_test_case(TEST_CASE_FILE)
    context = test_case.get("input", {})
    # Build prompt (if using PromptBuilder logic)
    # For now, just use the prompt as a template with {note}
    prompt_template = prompt_config.get("system", "")
    prompt = prompt_template.format(**context)
    print("[PROMPT]\n" + prompt)
    # Simulate LLM call
    output = dummy_llm(prompt)
    print(f"[LLM OUTPUT] {output}")
    # Compare to expected
    expected = test_case.get("expected", {})
    if output == expected:
        print("[PASS] Output matches expected.")
    else:
        print(f"[FAIL] Output does not match expected.\nExpected: {expected}\nGot: {output}")

if __name__ == "__main__":
    main() 