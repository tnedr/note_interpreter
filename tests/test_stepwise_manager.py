import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import pytest
from prompt_lab.libs.stepwise_manager import StepwisePlanManager

AGENT_DIR = Path(__file__).resolve().parent.parent / "prompt_lab" / "agents" / "grocery_clarifier"
PLAN_FILE = AGENT_DIR / "plan.yaml"

def test_plan_loading():
    plan = StepwisePlanManager(PLAN_FILE)
    assert len(plan.steps) == 2
    assert plan.steps[0]['step_name'] == 'step_01_scoring'
    assert 'experiment_cases' in plan.steps[0]
    assert plan.steps[0]['experiment_cases'][0].endswith('experiment_s1_01.yaml')
    assert plan.steps[1]['step_name'] == 'step_02_clarification'
    assert 'clarification_question' in plan.steps[1]['expected_output_fields'] 