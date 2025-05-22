# pipenv run python -m demo.run_clarify_and_score_demo

from note_interpreter.clarify_and_score_agent import ClarifyAndScoreAgent
from note_interpreter.prompt_builder import PromptBuilder
from note_interpreter.log import log

# Logolás beállítása konzolra, debug szinten (singleton)
log.reset()
log.__init__(level="debug", to_console=True)

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