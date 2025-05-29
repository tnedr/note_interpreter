# 🛠️ Technical Specification – AI-Powered Note Understanding and Enrichment System

**Version:** 0.4 (Batch-Oriented LLM Agent)
**Author:** DrTamasNagy_with_cursorai  
**Date:** 2025-05-17  
**Version:** 1


---

## 1. System Architecture

### 1.1 High-Level Components

- **Input Handler:** Loads notes (CSV), user memory (Markdown), and classification config (YAML).
- **LLM Agent:** Central orchestrator that receives a batch of notes and user memory, performs scoring, clarification, interpretation, metadata enrichment, and suggests memory updates for the entire batch. Handles all core logic via LLM calls.
- **Clarification Loop:** If clarification is needed, the agent generates questions for the batch, collects user answers, and re-invokes itself with updated context.
- **Output Generator:** Produces enriched CSV output and updates user memory.
- **Configuration Manager:** Handles thresholds, file paths, and system parameters.

### 1.2 Batch Interaction Flow

1. **Load Inputs:** Notes (CSV), User Memory (MD), Classification (YAML)
2. **LLM Agent Batch Processing:** The agent receives a `NoteBatch` object (containing all notes, user memory, and classification config) and processes the batch in one shot:
   - Computes scores (understandability, interpretability, ambiguity, confidence) for each note
   - Generates clarification questions for notes that need them
3. **Clarification (if needed):** If clarification is required, the agent presents grouped questions for the batch to the user, collects answers, and re-runs itself with all context and answers.
4. **Final Enrichment:** The agent produces interpreted notes, metadata, and memory update suggestions for the batch.
5. **Output:** Write enriched CSV, update user memory (append-only).

---

## 1.3 Class Structure

### Main Classes and Responsibilities

- **Note**
  - Represents a single user note and all associated data (raw input, scores, clarifications, interpretation, metadata).

- **NoteBatch**
  - Represents a batch of notes to be processed together, along with user memory and classification config.
  - Attributes:
    - `notes`: list of Note or raw note strings
    - `user_memory`: UserMemory
    - `classification_config`: ClassificationConfig

- **UserMemory**
  - Loads, manages, and updates the narrative-style user memory (Markdown bullets).

- **ClassificationConfig**
  - Loads and validates the classification YAML (entity types, intents).

- **InputHandler**
  - Loads notes, user memory, and classification config from files and constructs a NoteBatch.

- **LLMAgent**
  - Orchestrates batch processing: scoring, clarification, interpretation, metadata enrichment, and memory update suggestions for the entire NoteBatch using LLM calls.
  - Handles clarification loop if needed.
  - Example method: `process_batch(batch: NoteBatch) -> BatchResult`

- **OutputGenerator**
  - Writes enriched notes to CSV and updates user memory file.

- **ConfigurationManager**
  - Manages system parameters, thresholds, and file paths.

#### Relationships
- `LLMAgent` operates on `NoteBatch` objects, using `Note`, `UserMemory`, and `ClassificationConfig` as input/output models.
- `InputHandler` and `OutputGenerator` interact with the file system and these core classes.
- `ConfigurationManager` is accessed by all components for settings.

---

## 2. Data Structures

### 2.1 Note Object
```python
class Note:
    raw_input: str
    scores: dict  # {understandability, interpretability, ambiguity, confidence}
    clarification_q_and_a: list[dict]  # [{question, user_answer}]
    interpreted_text: str
    clarity_score: int
    metadata: dict  # {entity_type, intent, ...}
```

### 2.2 NoteBatch Object
```python
class NoteBatch:
    notes: list[Note]  # or list[str] for raw notes
    user_memory: UserMemory
    classification_config: ClassificationConfig
```

### 2.3 User Memory
- Markdown file, each line: `* <sentence>`
- Loaded as a list of strings for context injection.

### 2.4 Classification Config
- YAML file, e.g.:
  ```yaml
  entity_types: [task, project, idea, ...]
  intents: [@DO, @PLAN, ...]
  ```

---

## 3. Core Logic & LLM Agent Pipeline

### 3.1 LLM Agent Batch Processing
- The agent receives a `NoteBatch` object containing:
  - The full batch of notes
  - User memory context
  - Classification YAML
- For each note in the batch, the agent:
  - Computes scores (understandability, interpretability, ambiguity, confidence)
  - Generates clarification questions if needed
  - Suggests memory updates
- If clarification is needed for any note:
  - The agent groups and presents all questions for the batch to the user
  - After receiving answers, the agent re-processes the batch with answers integrated
- The agent then:
  - Produces interpreted text, metadata, and final memory updates for each note in the batch

### 3.2 Clarification Strategy
- Max 2 clarification rounds per note
- Clarifications are grouped and presented in one conversational block for the batch
- If ambiguity remains, the note is flagged for manual review

### 3.3 Output Generation
- Write all fields to output CSV
- Append new context to user memory (Markdown)
- Validate metadata against YAML config; flag missing values as `MISSING_suggested:<value>`

---

## 4. File I/O

### 4.1 Input Files
- `notes.csv` (one note per row)
- `user_memory.md` (Markdown bullets)
- `classification.yaml` (entity_types, intents)

### 4.2 Output Files
- `enriched_notes.csv` (all fields per note)
- `user_memory.md` (append new context)

---

## 5. Configuration
- All thresholds (confidence, ambiguity, clarity) are configurable (default in functional spec)
- File paths for input/output are configurable via CLI or config file

---

## 6. Error Handling & Edge Cases
- If clarification limit exceeded: flag note as unresolved
- If metadata value missing from YAML: flag as `MISSING_suggested`
- If input note > max length: truncate or flag error
- Handle malformed input, LLM API errors, and partial batch failures with retries or logging

---

## 7. Extensibility
- Modular design: input/output, LLM agent orchestration, and clarification loop are separate modules
- Easy to swap LLM provider or prompt templates
- Future: add web UI, API, or integration with productivity tools

---

## 8. Logging & Traceability
- All steps (LLM agent input/output, clarifications, metadata) are logged per note and per batch
- Optionally, debug logs explain why clarifications were triggered or how outputs were generated

---

## 9. Security & Privacy
- User memory and notes are stored locally
- No data is sent externally unless explicitly configured

---

## 10. Testing
- Unit tests for input/output, LLM agent orchestration, and clarification loop
- Integration tests for end-to-end pipeline
- Use test data/fixtures for all major edge cases

---

## 11. Glossary
- See `docs/system_overview.md` and `docs/functional_specification.md`

---

<!-- Please add inline comments or suggestions below each section as needed. --> 