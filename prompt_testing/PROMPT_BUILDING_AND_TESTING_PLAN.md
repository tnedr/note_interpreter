# Prompt Building & Testing Plan for ClarifyAndScoreAgent

**Note:** This file is the dedicated testing and prompt development plan for the agent: **ClarifyAndScoreAgent**. Each agent in the system will have its own plan file (e.g., `prompt_building_and_testing_plan__ClarifyAndScoreAgent.md`, `prompt_building_and_testing_plan__OtherAgent.md`, etc.), with input/output schemas and test methodology tailored to that agent.

**Ultimate Goal:**
Reliably transform well-defined, structured input (notes, user memory, clarification history, etc.) into clear, actionable, and schema-compliant structured outputs, using a multi-step, test-driven prompt optimization process. The final system must robustly handle ambiguous notes, ask for clarification when needed, and always produce valid, machine-readable results with minimal hallucination.

_This plan and the associated prompt/test files are specifically for the **ClarifyAndScoreAgent** prompt development and evaluation._

# Canonical Input & Output Structure (ClarifyAndScoreAgent, V2)

## Input Schema (YAML Example)
```yaml
notes_batch:
  - id: note_001
    raw_text: "Apply to PROMPT_BUILD..."
    clarification_history:
      - question: "Do you mean a specific tool?"
        answer: "Yes, LangChain prompt tester"
  - id: note_002
    raw_text: "Schedule lab"
    clarification_history: []  # can be omitted or empty
user_memory:
  - "User often references LangChain tools."
  - "The term 'lab' usually refers to AI workflows."
clarity_score_threshold: 70
```

## Output Schema (YAML Example)
```yaml
notes_batch:
  - id: note_001
    raw_text: "Apply to PROMPT_BUILD..."
    clarification_history:
      - question: "Do you mean a specific tool?"
        answer: "Yes, LangChain prompt tester"
    interpreted_text: "Apply to the LangChain prompt testing tool for your AI workflow."
    clarity_score: 88
    ask_user_question: null
  - id: note_002
    raw_text: "Schedule lab"
    clarification_history: []
    interpreted_text: null
    clarity_score: 45
    ask_user_question: "What kind of lab do you want to schedule?"
```

---

# Advantages of This Schema
- **Traceability:** Each note is uniquely identified by `id`, making it easy to track across rounds, agents, or merges.
- **Encapsulation:** All relevant data for a note (text, clarification history, output fields) is grouped together, making both prompting and downstream processing much simpler.
- **Batch-Friendly:** The structure naturally supports batch processing and is easy to extend for multi-agent workflows.
- **Extensible:** You can add more fields (e.g., timestamps, agent annotations) to each note entry without breaking the schema.
- **Prompt Simplicity:** The LLM prompt can directly reference each note's context and history, reducing ambiguity and improving output quality.
- **Cleaner Code:** No need to cross-reference separate lists for clarification history or outputs—everything is in one place.

---

# Prompt Guidelines & Best Practices

- For every input section in your prompt, add a **short, explicit description** at the start that explains what each field is and how it should be used (e.g., what input_notes means, what user_memory is for, etc.).
- Place this description immediately before the data, so the LLM always knows what it is seeing and how to use it.
- This reduces ambiguity, prevents misinterpretation, and makes prompts more robust and maintainable.
- As your input context grows, update the section-level descriptions accordingly.
- **Build prompts incrementally:** Start with the simplest possible prompt (e.g., scoring only), then add interpretation, then clarification questions, and only at the end require strict structured output/schema compliance. Each step should add one new layer of complexity.
- Example:
  - "Below is a list called notes_batch. Each item is a note object with an id, raw_text, and clarification_history."
  - "user_memory: Background information or preferences about the user. Use only if needed for context."

---

## Roadmap: Stepwise Prompt & System Development

1. **Scoring Only**
   - Goal: For each note, assign a clarity_score (and optionally ambiguity_score, interpretability, understandability).
   - No interpretation, no clarification, no structured output required—just scoring.

2. **Scoring + Interpretation**
   - For each note, provide both a score and a brief interpretation (paraphrase or explanation of the note's meaning).
   - Output can be freeform (not strictly structured yet).

3. **Scoring + Interpretation + Clarification Questions**
   - For each note, provide a score, an interpretation, and, if the note is ambiguous, generate clarification questions.
   - Output can still be freeform, but must include all three elements.

4. **Full Structured Output (Tool/Agent Workflow)**
   - All of the above, but output must strictly follow the defined schema (DataEntry), and use tool calls if required (clarify_notes, finalize_notes, etc.).
   - Output must always be valid, machine-readable, and schema-compliant.

5. **Edge Cases, Fallbacks, and Regression**
   - Test with difficult, ambiguous, or adversarial notes.
   - Add constraints, fallback logic (e.g., UNDEFINED fields), and regression tests for all previous steps.

---

## 1. Objectives and Key Challenges
- What do we want to achieve? (e.g., interpret ambiguous notes, assign clarity scores, ask clarifying questions, produce structured output)
- Main challenges: ambiguous input, incomplete user answers, avoiding hallucination, ensuring output is always valid and actionable

---

## 2. Iterative Prompt Development Steps

### 2.1. "Freeform" (plain text) baseline prompt
- Start with a simple prompt that only asks for interpretation, scoring, and clarification questions in plain text.
- Test if the model understands the task, asks clarifying questions, and scores notes sensibly.

### 2.2. Structured output (JSON) prompt
- Require the model to always return JSON (e.g., note, score, clarification_questions, reasoning).
- Test if the JSON is always valid, all fields are present, and the reasoning is clear.

### 2.3. Tool-based, agent prompt
- Introduce tool calls (clarify_notes, finalize_notes, etc.), schemas, and strict constraints.
- Test if the model only uses tool calls, follows the schema, and never responds in plain text.

### 2.4. Fine-tuning, edge cases, regression
- Test with rare, difficult, or intentionally misleading inputs.
- Refine the prompt: add examples, adjust reasoning style, constraints, fallback, etc.
- Every new prompt version should be regression-tested on previous inputs.

---

## 3. Prompt Modification/Building Principles
- Change only one thing at a time (one block, one example, one constraint)
- Every variant should have test input and expected behavior
- Log every prompt+input+output combination
- Add examples for every important part (clarity_score, clarification, UNDEFINED, etc.)
- Use explicit constraints
- Always test reasoning style
- Meta behavior: always have a fallback if the model is uncertain

---

## 4. Prompt Variants & Testing Workflow
1. Each prompt version is a separate YAML (PromptBuilder-compatible)
2. The test script runs every prompt version on every input
3. All outputs are logged and can be compared
4. If a prompt change improves results, keep it; if not, revert
5. The best prompts are saved as regression tests

---

## 5. Automation & Tooling
- PromptBuilder: all prompt generation is unified here
- run_prompt_tests.py: runs all prompt variants, all inputs, logs all outputs
- Promptfoo/LangSmith: regression and quality tests, diff, comparison
- (Optional) Automatic diff script: highlights differences between prompt variants

---

## 6. Decision Tree: What to Modify When?
- If the model doesn't understand the task → add/change examples, clarify objectives
- If it doesn't ask clarifying questions → add more clarification examples, emphasize reasoning style
- If output isn't structured → add JSON schema, explicit constraints, examples
- If it doesn't use tool calls → add tool schema, constraints, meta behavior
- If it hallucinates → add constraints, fallback, UNDEFINED policy

---

## 7. Example Prompt Variants
- plain_v1.yaml: freeform, explanatory prompt
- json_v1.yaml: structured JSON output
- tool_v1.yaml: tool-based, strict agent prompt
- v1, v2, v3...: fine-tuned, production-ready prompts

---

*You are encouraged to modify and extend this plan for your own workflow!* 