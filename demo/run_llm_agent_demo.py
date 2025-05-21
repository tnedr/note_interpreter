# pipenv run python -m demo.run_llm_agent_demo

from note_interpreter.llm_agent import SingleAgent
from note_interpreter.user_output import user_print, CYAN

if __name__ == "__main__":
    # Homályos jegyzet, hogy biztosan ask_user toolt kelljen használnia
    notes = ["buy apples", "continue project","???"]
    user_memory = ["Tamas currently working on a machine learning trading projekct"]
    agent = SingleAgent(notes, user_memory, debug_mode=True)
    output = agent.run()
    user_print(output.model_dump_json(indent=2), color=CYAN) 