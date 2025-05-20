# pipenv run python -m demo.run_llm_agent_demo

from note_interpreter.llm_agent import LLMAgent, MemoryManager

if __name__ == "__main__":
    # Homályos jegyzet, hogy biztosan ask_user toolt kelljen használnia
    notes = ["???"]
    user_memory = []
    agent = LLMAgent(notes, user_memory, debug_mode=True)
    output = agent.run()
    from note_interpreter.log import log
    log.print(output.model_dump_json(indent=2)) 