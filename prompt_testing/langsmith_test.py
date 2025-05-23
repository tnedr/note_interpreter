import os
from langsmith import traceable
from langchain_openai import ChatOpenAI

# Ellenőrizzük a környezeti változókat
print("LANGCHAIN_API_KEY:", os.getenv("LANGCHAIN_API_KEY"))
print("LANGCHAIN_TRACING_V2:", os.getenv("LANGCHAIN_TRACING_V2"))

@traceable
def run_prompt_test(notes, user_memory, clarification_history):
    prompt = f"""
    Notes: {notes}
    User memory: {user_memory}
    Clarification history: {clarification_history}
    Output: ...
    """
    print("Prompt:\n", prompt)
    llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0.0)
    response = llm.invoke(prompt)
    print("LLM output:\n", response.content)
    return response.content

if __name__ == "__main__":
    run_prompt_test(
        notes="continue plan",
        user_memory="* User is working on a new project called NoteInterpreter.",
        clarification_history=""
    ) 