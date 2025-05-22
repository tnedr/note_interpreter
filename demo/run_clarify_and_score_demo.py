# pipenv run python -m demo.run_clarify_and_score_demo

from note_interpreter.clarify_and_score_agent import ClarifyAndScoreAgent
from note_interpreter.prompt_builder import PromptBuilder
from note_interpreter.log import log
import os
from datetime import datetime

# Logolás beállítása konzolra és file-ba, debug szinten (singleton)
log.reset()
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file_path = os.path.join(
    log_dir,
    f"clarify_and_score_demo_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
)
log.__init__(level="debug", log_file=log_file_path, to_console=True)
# A log file elérési útja: logs/clarify_and_score_demo_YYYY-MM-DD_HH-MM-SS.log

# Valós inputok
notes = [
    "continue plan",
    "email John re demo",
    "???"
]
user_memory = [
    "* User is working on a new project called NoteInterpreter.",
    "* User prefers concise, actionable notes."
]
clarification_history = []

# Prompt generálás a configból
context = {
    "notes": notes,
    "user_memory": user_memory,
    "clarification_history": clarification_history,
    # Add any other required context fields here
}
prompt = PromptBuilder.build(
    context=context,
    config_path="resources/clarify_and_score_agent/prompt_config.yaml"
)
log.info("Generated prompt:\n" + prompt)

# Agent példányosítás
agent = ClarifyAndScoreAgent(
    prompt=prompt,
    config={"model": "gpt-4.1-mini", "temperature": 0.0},
    debug_mode=True
)

# Futtatás
def main():
    log.info("Running ClarifyAndScoreAgent...")
    output = agent.run(notes, user_memory, clarification_history)
    log.info(f"Raw agent output: {output}")
    print("\nAgent output:")
    for note in output:
        print(note)

if __name__ == "__main__":
    main() 