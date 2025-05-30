### 🧠 Stepwise Plan – System Prompt Templates

These prompt templates support the structured creation of a stepwise plan for Human-In-The-Loop (HITL) agent workflows.

---

#### ✅ Prompt 1: Végcél, Bemenet és Kimenet meghatározása

```txt
You are designing a human-in-the-loop stepwise plan for a specific agent. Your task is to define the goal, input, and output for the plan.

Given the following background conversation and context, generate the `goal.description`, and structured `input` and `output` sections.

Requirements:
- `goal.description` should clearly state what the agent does, based on what inputs, and what kind of structured output it produces.
- `input`: list each distinct input, with name, short description, format, and 1-2 row example (CSV recommended).
- `output`: list each output artifact similarly with name, description, format, and example.

Structure your answer in valid YAML format with fields: `goal`, `input`, `output`.

Context:
[Paste conversation or user background here]
```

---

#### ✅ Prompt 2: Lépések összefoglalása (Steps Summary)

````txt
Using the defined goal, inputs and outputs from the previous step, create a summary list of major processing steps the agent will perform.

Each step should:
- Have a short, descriptive name
- Optionally include parentheses describing its input/output context

Goal:
[Paste generated goal.description here]

Input:
[Paste YAML input section]

Output:
[Paste YAML output section]

Return a YAML node:
```yaml
steps:
  - Scoring (raw_notes → raw_notes_with_score)
  - Clarification (raw_notes_with_score → clarification_qna)
  - ...
````
---

#### ✅ Prompt 3: Részletes lépések kidolgozása
```txt
Based on the previous goal, inputs, outputs and step summary, define each step in detail.

For each step include:
- `step_name`: unique identifier
- `goal`: what the step tries to achieve
- `input`: input artifact (name, format, description)
- `expected_output`: output artifact (same)
- `human_review`: true/false — should a human validate this step?
- `notes`: optional supporting comment

Use this structure:
```yaml
- step_name: [name]
  goal: [step-specific goal]
  input:
    name: ...
    description: ...
    format: ...
  expected_output:
    name: ...
    description: ...
    format: ...
  human_review: true|false
  notes: ...
````

Goal:
\[Paste goal.description]

Steps:
\[Paste steps summary]

```

---

```
