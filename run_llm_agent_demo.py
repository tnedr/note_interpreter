import os
import json
from note_interpreter.llm_agent import LLMAgent, load_classification_from_yaml
from note_interpreter.colors import RESET, BOLD, CYAN, YELLOW, MAGENTA, BLUE, GREEN, RED, WHITE, BANNER_COLORS

# Set this to True for user-friendly output, False for full debug
user_mode = True

def pretty_print_output(output):
    try:
        if hasattr(output, "model_dump_json"):
            print(json.dumps(json.loads(output.model_dump_json()), indent=2, ensure_ascii=False))
        else:
            print(output)
    except Exception:
        print(output)

def main():
    # Use ambiguous notes and empty memory to trigger clarification
    notes = [
        "stuff",
        "remind me",
        "the thing"
    ]
    memory = []
    classification_config = load_classification_from_yaml("resources/entity_types_and_intents.yaml")

    if user_mode:
        print(f"\n{BOLD}{CYAN}========== AGENT STARTED =========={RESET}")
        print(f"{BOLD}[User] Notes:{RESET}")
        for n in notes:
            print(f"  - {n}")
        print()
    else:
        print("\n========== AGENT STARTED ==========")
        print("Running LLMAgent demo with ambiguous notes:")
        for n in notes:
            print(" -", n)
        print("\nIf clarification is needed, you will be prompted for input.\n")

    # Set agent debug_mode based on user_mode
    agent = LLMAgent(
        notes,
        memory,
        classification_config=classification_config,
        temperature=0.0,  # Deterministic output
        debug_mode=not user_mode
    )

    # Monkeypatch agent to print tool invocations and questions in user_mode
    orig_handle_user_message = agent.agent_core.handle_user_message
    def wrapped_handle_user_message(user_context):
        response = orig_handle_user_message(user_context)
        if user_mode:
            if response.get("type") == "tool_call" and response.get("tool_details"):
                tool_name = response["tool_details"].get("name")
                print(f"\n{BOLD}{MAGENTA}-------- TOOL INVOCATION: {tool_name} --------{RESET}")
                if tool_name == "clarification_tool":
                    tool_output = response.get("display_message")
                    try:
                        output_data = json.loads(tool_output) if isinstance(tool_output, str) and tool_output else tool_output
                    except Exception:
                        output_data = tool_output
                    questions = []
                    if output_data:
                        questions = output_data.get("questions", [])
                    if questions:
                        print(f"{BOLD}{BLUE}-------- CLARIFICATION QUESTIONS --------{RESET}")
                        for i, q in enumerate(questions, 1):
                            print(f"  {i}: {q}")
                        print(f"{BOLD}{BLUE}-----------------------------------------{RESET}")
        return response
    agent.agent_core.handle_user_message = wrapped_handle_user_message

    output = agent.run()
    if user_mode:
        print(f"\n{BOLD}{GREEN}========== FINAL RESULT =========={RESET}")
        pretty_print_output(output)
        print(f"{BOLD}{GREEN}=================================={RESET}\n")
    else:
        print("\n========== FINAL OUTPUT ==========")
        pretty_print_output(output)
        print("==================================\n")

if __name__ == "__main__":
    # Make sure your OPENAI_API_KEY is set in your environment before running!
    main() 