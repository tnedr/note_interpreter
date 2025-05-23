# pipenv run python -m prompt_testing.run_prompt_tests

import os
import glob
import yaml
from note_interpreter.prompt_builder import PromptBuilder
from note_interpreter.log import log
from langchain_openai import ChatOpenAI

PROMPT_CONFIGS = [
    os.path.join("resources", "clarify_and_score_agent", "prompt_config_v1.yaml"),
    os.path.join("resources", "clarify_and_score_agent", "prompt_config_v2.yaml"),
    # Ide vehetsz fel több prompt configot, ha több verziót akarsz tesztelni
]
INPUT_DIR = os.path.join(os.path.dirname(__file__), 'test_inputs')
LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

log_file_path = os.path.join(LOG_DIR, 'prompt_test.log')
log.__init__(level="info", log_file=log_file_path, to_console=True)

def load_inputs():
    input_files = glob.glob(os.path.join(INPUT_DIR, '*.yaml'))
    inputs = {}
    for inf in input_files:
        with open(inf, encoding='utf-8') as f:
            inputs[os.path.basename(inf)] = yaml.safe_load(f)
    return inputs

def main():
    inputs = load_inputs()
    llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0.0)
    for config_path in PROMPT_CONFIGS:
        for input_name, context in inputs.items():
            header = f"=== Prompt config: {config_path} | Input: {input_name} ==="
            log.info(header)
            prompt = PromptBuilder.build(context=context, config_path=config_path)
            log.info("Prompt:\n" + prompt)
            response = llm.invoke(prompt)
            log.info("LLM output:\n" + response.content)
            print(f"\n[Prompt config: {config_path} | Input: {input_name}]\nLLM output:\n{response.content}\n")

if __name__ == "__main__":
    main() 