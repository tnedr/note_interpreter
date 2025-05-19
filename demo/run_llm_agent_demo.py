# This file was moved to demo/run_llm_agent_demo.py
# (Original content preserved)

from note_interpreter.llm_agent import LLMAgent, MemoryManager

if __name__ == "__main__":
    notes = MemoryManager.load_from_md("docs/examples/example_notes.csv")
    user_memory = MemoryManager.load_from_md("docs/examples/example_user_memory.md")
    agent = LLMAgent(notes, user_memory, debug_mode=True)
    output = agent.run()
    from note_interpreter.log import log
    log.print(output.model_dump_json(indent=2)) 