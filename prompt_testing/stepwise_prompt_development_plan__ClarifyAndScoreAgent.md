# Stepwise Prompt Development Plan for ClarifyAndScoreAgent



## Project Goal and Final Input/Output Schema

**Goal:**
Reliably transform batches of user notes into clear, actionable, and schema-compliant structured outputs, using all available context (user memory, clarification history, etc.), with robust handling of ambiguity and always producing valid, machine-readable results.

**Final Input Schema (YAML):**
```yaml
notes_batch:
  - id: note_001
    raw_text: "Apply to PROMPT_BUILD..."
    clarification_history:
      - question: "Do you mean a specific tool?"
        answer: "Yes, LangChain prompt tester"
      - question: "When is the deadline?"
        answer: "Next week"
  - id: note_002
    raw_text: "Schedule lab"
    clarification_history: []
user_memory:
  - "User often references LangChain tools."
  - "The term 'lab' usually refers to AI workflows."
clarity_score_threshold: 70
```

**Final Output Schema (YAML):**
```yaml
notes_batch:
  - id: note_001
    raw_text: "Apply to PROMPT_BUILD..."
    clarification_history:
      - question: "Do you mean a specific tool?"
        answer: "Yes, LangChain prompt tester"
      - question: "When is the deadline?"
        answer: "Next week"
    interpreted_text: "Apply to the LangChain prompt testing tool for your AI workflow by next week."
    clarity_score: 88
    ask_user_question: null
  - id: note_002
    raw_text: "Schedule lab"
    clarification_history: []
    interpreted_text: null
    clarity_score: 45
    ask_user_question: "What kind of lab do you want to schedule?"
```

**Expected Behavior:**
- For each note, the agent should provide an interpreted_text, clarity_score, and, if needed, a clarification question (ask_user_question).
- If the note is ambiguous or cannot be interpreted, interpreted_text should be null or UNDEFINED, and ask_user_question should be set.
- The agent must use user_memory and clarification_history as context when available.
- Output must be valid, machine-readable, and schema-compliant in the final step.

**Clarification History Structure:**
- Each note in notes_batch can have a clarification_history field, which is a list of Q&A pairs (question/answer objects).
- This allows for multi-turn clarification for each note individually.

---

## Stepwise Expansion Logic

The agent's testable behavior is expanded incrementally in the following order:
1. Start with only scoring notes for clarity (no interpretation, no memory, no clarification).
2. Add interpretation (paraphrasing) of notes.
3. Add clarification question generation for ambiguous notes.
4. Introduce user_memory as additional context for interpretation and scoring.
5. Add clarification_history as an input, allowing the agent to use previous Q&A for each note.
6. Require strict, fully schema-compliant output and tool call structure.
7. Test edge cases, fallbacks (e.g., UNDEFINED), and regression.

Each step builds on the previous, and all earlier tests must continue to pass as new capabilities are added.

---

## Summary Table: Stepwise Development

| Step | Goal | New Input Fields | New Output Fields | Test Focus |
|------|------|------------------|------------------|------------|
| 1    | Scoring only | notes | clarity_score | Valid score for each note |
| 2    | + Interpretation | notes | interpreted_text | Score + interpretation |
| 3    | + Clarification | notes | ask_user_question | Clarification logic |
| 4    | + User Memory | user_memory | (use memory) | Contextualization |
| 5    | + Clarification History | clarification_history | (use history) | Multi-turn logic |
| 6    | + Structured Output | all fields | all fields, tool calls | Full compliance |
| 7    | + Edge/Fallbacks | all fields | UNDEFINED, error handling | Robustness |

---

## Prompt Versioning
- Each prompt version is saved as a separate YAML file (PromptBuilder-compatible).
- Version names: `plain_v1.yaml`, `json_v1.yaml`, `tool_v1.yaml`, `v2`, `v3`, etc.
- Regression tests are run on all previous and current prompt versions.

---

# Stepwise Development

## Step 1: Scoring Only

**Goal:**
Assign a clarity_score (0-100) to each note. No interpretation, memory, or clarification yet.

**Input Schema:**
```yaml
notes_batch:
  - id: note_001
    raw_text: "Apply to PROMPT_BUILD..."
  - id: note_002
    raw_text: "Schedule lab"
```

**Output Schema:**
```yaml
notes_batch:
  - id: note_001
    clarity_score: 88
  - id: note_002
    clarity_score: 45
```

**Test Criteria:**
- Every note has a clarity_score (0-100).
- Output is valid YAML/JSON.

**Edge/Fallbacks:**
- If a note is too ambiguous, assign a low score.

**Regression:**
- All notes must have a score; no missing fields.

---

## Step 2: Scoring + Interpretation

**Goal:**
Add interpretation of each note, in addition to clarity scoring. The model should now return both a clarity_score and a brief interpreted_text for each note.

**Input Schema:**
(same as previous step)

**Output Schema:**
```yaml
notes_batch:
  - id: note_001
    clarity_score: 88
    interpreted_text: "Apply to the LangChain prompt testing tool for your AI workflow."
```

**Test Criteria:**
- Every note has a clarity_score (0-100).
- Every note has a non-empty interpreted_text.
- Output is valid YAML/JSON.

**Edge/Fallbacks:**
- If the note is too ambiguous, interpreted_text should be null or empty.

**Regression:**
- All tests from Step 1 must still pass.

---

## Step 3: Scoring + Interpretation + Clarification

**Goal:**
For ambiguous notes, generate a clarification question. Add ask_user_question field.

**Input Schema:**
(same as previous step)

**Output Schema:**
```yaml
notes_batch:
  - id: note_001
    clarity_score: 88
    interpreted_text: "Apply to the LangChain prompt testing tool for your AI workflow."
    ask_user_question: null
  - id: note_002
    clarity_score: 45
    interpreted_text: null
    ask_user_question: "What kind of lab do you want to schedule?"
```

**Test Criteria:**
- Every note has clarity_score, interpreted_text, and ask_user_question.
- If a note is ambiguous, ask_user_question is non-empty.
- Output is valid YAML/JSON.

**Edge/Fallbacks:**
- If the model is uncertain, ask_user_question should be set.

**Regression:**
- All tests from Steps 1 and 2 must still pass.

---

## Step 4: Add User Memory

**Goal:**
The agent should use user_memory as additional context when interpreting notes and scoring, but output can still be semi-structured.

**Input Schema:**
```yaml
notes_batch:
  - id: note_001
    raw_text: "Schedule lab"
user_memory:
  - "User prefers AI workflow labs."
```

**Output Schema:**
```yaml
notes_batch:
  - id: note_001
    clarity_score: 70
    interpreted_text: "Schedule an AI workflow lab."
    ask_user_question: null
```

**Test Criteria:**
- Output reflects user_memory if relevant.
- Output is valid YAML, but not required to be fully schema-compliant yet.

**Edge/Fallbacks:**
- If user_memory is not relevant, output as in previous steps.

**Regression:**
- All previous step tests must still pass.

---

## Step 5: Add Clarification History

**Goal:**
The agent should use clarification_history for each note as additional context. Output can still be semi-structured.

**Input Schema:**
```yaml
notes_batch:
  - id: note_001
    raw_text: "Schedule lab"
    clarification_history:
      - question: "What kind of lab?"
        answer: "AI workflow lab"
      - question: "When?"
        answer: "Next week"
user_memory:
  - "User prefers AI workflow labs."
```

**Output Schema:**
```yaml
notes_batch:
  - id: note_001
    clarity_score: 80
    interpreted_text: "Schedule an AI workflow lab next week."
    ask_user_question: null
```

**Test Criteria:**
- Output reflects clarification_history if present.
- Output is valid YAML, but not required to be fully schema-compliant yet.

**Edge/Fallbacks:**
- If clarification_history is empty, output as in previous steps.

**Regression:**
- All previous step tests must still pass.

---

## Step 6: Full Structured Output (Tool/Agent Workflow)

**Goal:**
Output must strictly follow the defined schema (all fields), and use tool calls if required. Output must always be valid, machine-readable, and schema-compliant.

**Input Schema:**
(same as final input schema at top)

**Output Schema:**
(same as final output schema at top)

**Test Criteria:**
- Output strictly matches schema.
- All fields present, valid types.
- Output is always valid YAML/JSON.

**Edge/Fallbacks:**
- If the model is uncertain, use UNDEFINED or set ask_user_question.

**Regression:**
- All previous step tests must pass.

---

## Step 7: Edge Cases, Fallbacks, and Regression

**Goal:**
Test with difficult, ambiguous, or adversarial notes. Add constraints, fallback logic (e.g., UNDEFINED fields), and regression tests for all previous steps.

**Input/Output Schema:**
(same as Step 6)

**Test Criteria:**
- Model handles edge cases robustly.
- Always produces valid, schema-compliant output.
- Fallbacks (UNDEFINED, error messages) are used when needed.

**Edge/Fallbacks:**
- If the model cannot interpret, set interpreted_text: UNDEFINED.
- If clarification is impossible, set ask_user_question: UNDEFINED.

**Regression:**
- All previous step tests must pass.
- Regression suite includes edge/adversarial cases.

---

*You are encouraged to modify and extend this plan for your own workflow!* 