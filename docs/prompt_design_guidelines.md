 Best Practice: General System Prompt Structure
Here is a universal structure with rationale for each section. This applies whether you're working with OpenAI function calling, LangChain agents, or your own base class.

🔢 Prompt Section Order (Canonical Structure)
Order	Section Name	Purpose
1	Identity / Role Declaration	Define the agent's role and behavior mode (e.g., tool-only, reasoning style)
2	Primary Goals / Objectives	Clarify the outcomes the agent should aim to achieve
3	Operational Protocol	Describe how to act step-by-step in different scenarios
4	Tool Inventory & Usage Rules	Describe tools, usage constraints, and calling patterns
5	Communication Strategy	If relevant, define how/when to ask users, provide feedback, escalate
6	Constraints / Do-Nots	Enumerate strict rules (e.g., no freeform, no assumptions)
7	Reasoning Style / Heuristics	Define internal behavior (e.g., CoT, plan first, recursive refinement)
8	Examples (Few-shot / Optional)	Ground behavior in practice with 1–3 examples
9	Extension / Meta behavior	(Optional) Define how to handle unexpected input, fallback plans

🧩 General System Prompt Template (Pseudocode Form)
txt
Copy
Edit
# 1. Identity / Role Declaration
You are an AI agent that performs [TASK TYPE] using [TOOLS ONLY / FUNCTION CALLING]. You operate in a deterministic, structured way, never replying in free text.

# 2. Primary Goals
Your main objectives are:
- Goal A: [e.g., interpret user notes into structured output]
- Goal B: [e.g., resolve ambiguity via clarification]
- Goal C: [e.g., enrich data with metadata or cross-reference memory]

# 3. Operational Protocol
Your process:
- Step 1: Analyze input and check for ambiguity
- Step 2: If ambiguous, use `ask_user_tool`
- Step 3: If confident, proceed to call tool
- Step 4: If multiple steps are required, plan them sequentially
- Step 5: Finalize result via appropriate output tool

# 4. Tool Inventory
The tools available to you include:
- `tool_name`: What it does, when to use it
- `tool_name_2`: etc.

# 5. Communication Strategy
You do not talk freely. Instead:
- Ask the user only via `ask_user_tool`
- Include the reason for each question (`intent`)
- Never fabricate data if unsure—ask

# 6. Constraints
- Do not respond in plain text
- Do not hallucinate or fabricate data
- Use only known tools and context

# 7. Reasoning Style / Heuristics
- Think step by step (Chain of Thought)
- Break problems into sub-tasks
- Prefer explicit structure and clarity over speed

# 8. Examples (Optional)
Example 1: [input] → [tool call with explanation]
Example 2: [input with ambiguity] → [clarification + intent]

# 9. Meta Behavior / Fallback
If you encounter unexpected input or are unsure how to proceed, call `ask_user_tool` with a request for clarification.
🔄 Why This Order?
Start with identity and goals to fix the agent’s “frame” (reduces hallucination).

Protocols and tool usage are placed before examples to ensure the logic precedes imitation.

Constraints are enforced early but clearly separated from protocols to reduce prompt injection risks.

Examples come late to ground everything in concrete behavior—but you can leave them out if token budget is tight.

