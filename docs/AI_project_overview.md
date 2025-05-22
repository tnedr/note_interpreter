# Project Overview for AI Agents

## 1. Project Summary

This project is designed to interpret, enrich, and classify user notes using AI. The system processes raw user input, clarifies ambiguous notes, and outputs structured, self-contained interpretations with metadata (such as clarity, ambiguity, and interpretability scores). The goal is to make user notes actionable, unambiguous, and easy to integrate into further workflows or memory systems.

## 2. File and Directory Structure

- `resources/single_agent/notes_output_schema.yaml`: Defines the schema for a single interpreted/enriched note (DataEntry), including all required fields, types, and descriptions.
- `aihuman_journal/journal.md`: Project journal, logs all significant events, decisions, and changes in a chronological format.
- `src/` (presumed): Contains the main source code for note interpretation, enrichment, and classification logic.
- `tests/` (presumed): Contains test cases and validation scripts for the core logic and schema compliance.
- `README.md`: General project introduction and setup instructions (if present).

> The above structure will be expanded with more details on each file and directory as the documentation progresses.

## 3. Main Components and Workflow

### 3.1 High-Level Components
- **Input Handler**: Loads notes (CSV), user memory (Markdown), and classification config (YAML).
- **LLM Agent**: Central orchestrator that processes a batch of notes, performs scoring, clarification, interpretation, metadata enrichment, and suggests memory updates. Handles all core logic via LLM calls.
- **Clarification Loop**: If clarification is needed, the agent generates questions, collects user answers, and re-invokes itself with updated context (max 2 rounds).
- **Output Generator**: Produces enriched CSV output and updates user memory (append-only).
- **Configuration Manager**: Handles thresholds, file paths, and system parameters.

### 3.2 Processing Pipeline
1. **Load Inputs**: Notes (CSV), User Memory (MD), Classification (YAML)
2. **Scoring Phase**: For each note, the system computes:
   - Understandability
   - Interpretability
   - Ambiguity
   - Clarity/Confidence
3. **Clarification Phase** (if needed):
   - If confidence is low or ambiguity is high, the agent asks clarification questions.
   - User answers are incorporated, and the process repeats (max 2 rounds).
4. **Interpretation**: The AI rewrites the note as a clear, self-contained, unambiguous sentence.
5. **Metadata Enrichment**: The interpreted note is tagged with `entity_type` and `intent` (validated against the classification YAML).
6. **Output**: Structured output (CSV/JSON) with all fields, and memory is updated with new insights.

### 3.3 Core Classes (Python)
- `Note`: Represents a single user note and all associated data (raw input, scores, clarifications, interpretation, metadata).
- `NoteBatch`: Represents a batch of notes, user memory, and classification config.
- `DataEntry`: Structured output for each note (matches output schema).
- `InputHandler`: Loads notes, user memory, and classification config from files.
- `OutputGenerator`: Writes enriched notes to CSV and updates user memory.
- `LLMAgent`: Orchestrates batch processing, clarification, and enrichment.
- `ConfigurationManager`: Manages system parameters and file paths.

### 3.4 Clarification Logic
- Clarification is triggered if `clarity_score < 70` or `ambiguity_score > 60` (thresholds configurable).
- The agent generates clarification questions and collects user answers.
- If ambiguity persists after 2 rounds, the note is finalized with `UNDEFINED` or `MISSING_` flags.

### 3.5 User Memory
- Narrative-style, append-only log (Markdown bullets).
- Used as context for interpretation and clarification.
- Updated after each batch; never rewritten or deleted.

### 3.6 Output Schema (Summary)
Each output entry contains:
- `raw_text`: Original note
- `interpreted_text`: Fully clarified, self-contained version
- `entity_type`: Classification (e.g., task, idea)
- `intent`: User intent (e.g., @DO, @PLAN)
- `clarity_score`, `ambiguity_score`, `interpretability`, `understandability`: Scoring fields
- `ask_user_questions`: Clarification questions (if any)

> See `resources/single_agent/notes_output_schema.yaml` for full schema details.

## 4. Specifications and Rules

### 4.1 Output Schema (YAML)
The output for each interpreted note must follow the schema defined in `resources/single_agent/notes_output_schema.yaml`:
- `raw_text` (string): The original, unprocessed user note as entered.
- `interpreted_text` (string): The final, clear, enriched version of the user's note, fully self-contained and unambiguous.
- `entity_type` (string): The classification of the note (e.g., task, idea, project). Must be one of the allowed entity types.
- `intent` (string): The intent of the note (e.g., @DO, @PLAN, @INFO). Must be one of the allowed intents.
- `clarity_score` (integer, 0–100): How clear and unambiguous the interpretation is. Higher is better. Clarification is triggered if below 70.
- `ambiguity_score` (integer, 0–100): How ambiguous or unclear the note is. Higher means more ambiguous. Clarification is triggered if above 60.
- `interpretability` (integer, 0–100): How clearly the note maps to known memory or patterns.
- `understandability` (integer, 0–100): How grammatically complete and parseable the note is.
- `ask_user_questions` (array of string): Questions to ask the user for clarification if the note is ambiguous or unclear. (Optional)

### 4.2 Allowed Entity Types and Intents
Defined in `resources/single_agent/entity_types_and_intents.yaml`:
- **Entity Types:** task, project, idea, note, routine, reference, log, conversation, wish, trigger, feedback, signal, bookmark, role, template, suggestion, decision, question, insight, hypothesis, workflow
- **Intents:** @DO, @THINK, @PLAN, @BUILD, @LEARN, @REVIEW, @MEET, @BUY, @WAITING, @REFLECT, @DECIDE

If the AI suggests a value not in the YAML, it is flagged as `MISSING_suggested:...`.

### 4.3 Key Parameters and Thresholds
- `confidence_threshold`: 70 (minimum confidence score to avoid clarification)
- `ambiguity_threshold`: 60 (maximum ambiguity score before clarification)
- `max_clarification_rounds`: 2 (maximum clarification rounds)
- `max_input_length`: 300 (maximum characters per note)
- `clarity_score_target`: 90 (target minimum clarity score for a note to be considered complete)
- `classification_source`: yaml (source of allowed entity types/intents)

### 4.4 Output Validation Rules
- Output must be a valid JSON object (or CSV row) with all required fields.
- All three fields (`entries`, `new_memory_points`, `ask_user_questions`) must be present (empty list if none).
- Never return plain text or unstructured answers.
- If ambiguity persists after max clarification rounds, use `UNDEFINED` or `MISSING_` flags.

---

## 5. Example Workflows and Use-Cases

### 5.1 Example Input Files
- `docs/examples/example_notes.csv`:
  ```
  continue plan
  email John re demo
  ???
  ```
- `docs/examples/example_user_memory.md`:
  ```
  * User is working on a new project called NoteInterpreter.
  * User prefers concise, actionable notes.
  * User often refers to 'plan' as the project launch plan.
  ```
- `docs/examples/example_classification.yaml`: (see above for entity types/intents)

### 5.2 Example Output (JSON)
```json
{
  "entries": [
    {
      "raw_text": "continue plan",
      "interpreted_text": "Continue working on the Q3 marketing launch plan.",
      "entity_type": "task",
      "intent": "@DO",
      "clarity_score": 92,
      "ambiguity_score": 10,
      "interpretability": 95,
      "understandability": 98,
      "ask_user_questions": []
    },
    {
      "raw_text": "???",
      "interpreted_text": "UNDEFINED",
      "entity_type": "UNDEFINED",
      "intent": "UNDEFINED",
      "clarity_score": 0,
      "ambiguity_score": 100,
      "interpretability": 0,
      "understandability": 0,
      "ask_user_questions": ["What does '???' refer to?"]
    }
  ],
  "new_memory_points": [
    "* User often refers to 'plan' as the project launch plan."
  ]
}
```

### 5.3 Typical Workflow
1. User provides a batch of notes (CSV), user memory (MD), and classification config (YAML).
2. The system scores each note for clarity, ambiguity, interpretability, and understandability.
3. If a note is unclear, the agent asks clarification questions (max 2 rounds).
4. The agent rewrites each note as a clear, self-contained sentence and tags it with metadata.
5. The output is written as structured data (CSV/JSON), and new memory points are appended to user memory.

---

## 6. Further Resources
- `docs/system_overview.md`: High-level system overview and terminology
- `docs/functional_specification.md`: Functional requirements and detailed workflow
- `docs/technical_specification.md`: Technical architecture, class structure, and data models
- `resources/single_agent/notes_output_schema.yaml`: Output schema definition
- `resources/single_agent/entity_types_and_intents.yaml`: Allowed entity types and intents
- `README.md`: Quickstart, running the pipeline, and test instructions

---

## Next Steps
- Expand on the main components and logic.
- Summarize the key specifications and rules (e.g., from YAML schemas).
- Provide example workflows and use-cases.
- Link to further resources and documentation. 