import yaml
from pathlib import Path
from typing import List, Dict, Any, Optional, Union

class StepwisePlanManager:
    """
    Minimal MVP: Stepwise plan loader and parser.
    - Loads a stepwise plan (YAML or Markdown)
    - Parses steps: step name, prompt file, experiment_cases (list), expected fields
    - Lists steps and their metadata
    - (No execution logic yet)
    """
    def __init__(self, plan_path: Union[str, Path]):
        self.plan_path = Path(plan_path)
        self.steps: List[Dict[str, Any]] = []
        self.plan_meta: Dict[str, Any] = {}
        self._load_plan()

    def _load_plan(self):
        if self.plan_path.suffix in {'.yaml', '.yml'}:
            with open(self.plan_path, 'r', encoding='utf-8') as f:
                plan = yaml.safe_load(f)
            self.plan_meta = {k: v for k, v in plan.items() if k != 'steps'}
            self.steps = plan.get('steps', [])
        elif self.plan_path.suffix == '.md':
            # TODO: Markdown parsing (simple: look for code blocks or step tables)
            # For now, just a placeholder
            self.steps = []
            self.plan_meta = {}
        else:
            raise ValueError(f"Unsupported plan file type: {self.plan_path.suffix}")

    def list_steps(self) -> List[str]:
        """Return a list of step names."""
        return [step.get('step_name', f'step_{i+1}') for i, step in enumerate(self.steps)]

    def get_step(self, step_name: str) -> Optional[Dict[str, Any]]:
        """Return the step dict for a given step name."""
        for step in self.steps:
            if step.get('step_name') == step_name:
                return step
        return None

    def print_plan_summary(self):
        print(f"Stepwise Plan: {self.plan_path}")
        print(f"Meta: {self.plan_meta}")
        print(f"Steps:")
        for i, step in enumerate(self.steps):
            print(f"  {i+1}. {step.get('step_name', f'step_{i+1}')}")
            print(f"     Prompt: {step.get('prompt_file')}")
            print(f"     Experiment cases:")
            for exp in step.get('experiment_cases', []):
                print(f"        - {exp}")
            print(f"     Expected fields: {step.get('expected_output_fields')}")

# TODO: Add execution logic (run all steps, check outputs, log results)
# TODO: Add status tracking, attempt logging, integration with experiment runner 