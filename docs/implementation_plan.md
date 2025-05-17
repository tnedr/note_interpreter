# 🚀 Implementation Plan

## MVP Milestones

### MVP 1: Core Batch Note Interpreter (No LLM, No Clarification)
- **Goal:** Prove the data pipeline, file I/O, and data models work.
- **Features:**
  - Read notes from CSV, user memory from Markdown, and classification config from YAML.
  - Output a CSV with the same notes, but with placeholder fields for scores, interpretation, and metadata.
- **Why:** Ensures your data flow and file handling are robust before adding LLM complexity.

## MVP 1 Implementation Plan

### Goal
Prove the data pipeline, file I/O, and data models work (no LLM, no clarification logic).

### Task Checklist
- [x] Define `Note` and `NoteBatch` classes using `pydantic` for validation.
- [x] Add serialization/deserialization methods for `Note` (from/to CSV row).
- [x] Implement `InputHandler` to read notes from CSV, user memory from Markdown, and classification config from YAML.
- [x] Implement `OutputGenerator` to write a batch of notes to CSV with placeholder fields for scores, interpretation, and metadata.
- [x] Write unit tests for data models and file I/O.
- [x] Write an integration test for the full pipeline (read input → process → write output).
- [x] Add example input files to `docs/examples/`.
- [x] Document how to run the MVP 1 pipeline and tests in the `README.md`.

### AI Suggestions
- Use test-driven development: write or update tests before implementing each feature.
- Keep each function/class small and focused for easier testing and debugging.
- Automate test runs with a script or CI (e.g., GitHub Actions).
- Log each major step or decision in `aihuman_journal/journal.md`.

### Progress Tracking
| Task | Status |
|------|--------|
| Define data models | [x] |
| Implement file I/O | [x] |
| Write unit tests | [x] |
| Write integration test | [x] |
| Add example files | [x] |
| Update documentation | [x] |

### MVP 2: LLM Batch Processing (No Clarification Loop)
- **Goal:** Integrate the LLM agent for batch processing of notes.
- **Features:**
  - LLM agent processes a batch of notes and user memory, returning scores, interpretation, and metadata for each note.
  - Output enriched CSV.
  - No clarification questions yet—just one-shot processing.
- **Why:** Validates LLM integration, prompt design, and output parsing.

### MVP 3: Clarification Loop
- **Goal:** Add the clarification loop for ambiguous notes.
- **Features:**
  - Detect notes needing clarification (based on scores).
  - Present clarification questions to the user, collect answers, and re-run the LLM agent.
  - Limit to 2 clarification rounds per note.
- **Why:** Demonstrates the full "human-in-the-loop" workflow and resolves ambiguity.

### MVP 4: Validation, Logging, and Error Handling
- **Goal:** Harden the system for real-world use.
- **Features:**
  - Validate all outputs, flag unresolved notes, and check metadata against config.
  - Add structured logging and error handling for LLM/API/file issues.
- **Why:** Ensures reliability and traceability.

### MVP 5: CLI Interface and Documentation
- **Goal:** Make the system usable by others.
- **Features:**
  - Command-line interface for running the pipeline.
  - Usage instructions and example files in the docs.
- **Why:** Enables real users to try the system and provide feedback.

### MVP 6: (Optional) Minimal Web UI
- **Goal:** Provide a simple web interface for batch uploads and clarification dialogs.
- **Features:**
  - Web form for uploading files and answering clarifications.
- **Why:** Lowers the barrier for non-technical users.

---

## 0. **Preparation**

- **Review and finalize all specifications** (system, functional, technical).
- Ensure all documentation files are up to date and referenced in the README.
- Set up a project management board (e.g., GitHub Projects, Trello, or Notion) to track tasks and milestones.

---

## 1. **Project Setup**

1.1 **Repository Hygiene**
- Ensure `.gitignore`, `requirements.txt`, and `README.md` are up to date.
- Add `docs/file_index.md` and `metadata/file_index.yaml` to help navigation.

1.2 **Environment**
- Set up a Python virtual environment.
- Install core dependencies (e.g., `pydantic`, `pyyaml`, `pandas`, `openai` or other LLM SDKs, `pytest`).

---

## 2. **Core Data Models**

2.1 **Implement `Note` and `NoteBatch` classes**
- Use `pydantic` for validation and serialization.
- Add unit tests for model validation.

2.2 **Implement `UserMemory` and `ClassificationConfig`**
- Methods for loading, saving, and updating from files.
- Validation for Markdown and YAML formats.

---

## 3. **Input/Output Handlers**

3.1 **InputHandler**
- Read notes from CSV, user memory from Markdown, and classification config from YAML.
- Construct a `NoteBatch` object.
- Handle file errors and validation.

3.2 **OutputGenerator**
- Write enriched notes to CSV.
- Append new entries to user memory Markdown.
- Ensure atomic file writes (avoid data loss).

---

## 4. **Configuration Management**

- Implement `ConfigurationManager` to load thresholds and file paths from a YAML or `.env` file.
- Allow CLI overrides for key parameters.

---

## 5. **LLM Agent Integration**

5.1 **LLMAgent Class**
- Method: `process_batch(batch: NoteBatch) -> BatchResult`
- Handles:
  - Prompt construction (including user memory, classification config, and all notes)
  - LLM API calls (OpenAI, Azure, or local model)
  - Parsing and validation of LLM responses

5.2 **Prompt Engineering**
- Draft and test prompt templates for:
  - One-shot batch processing (scoring, clarification, interpretation, metadata)
  - Clarification follow-up (with user answers)
- Add example prompt/response schemas to the docs.

5.3 **Error Handling**
- Handle LLM API errors, timeouts, and malformed responses.
- Implement retries and logging.

---

## 6. **Clarification Loop**

- Detect which notes require clarification (based on scores).
- Present grouped questions to the user (CLI or UI).
- Collect answers and re-invoke the LLM agent with updated context.
- Limit to 2 clarification rounds per note.

---

## 7. **Validation and Post-Processing**

- Validate that all required fields are present in the output.
- Check metadata against the classification config; flag missing or invalid values.
- Flag unresolved notes for manual review.

---

## 8. **Logging and Traceability**

- Implement structured logging for all major steps (input, LLM calls, clarifications, output).
- Optionally, add debug mode for detailed trace logs.

---

## 9. **Testing**

- Write unit tests for all core classes and functions.
- Write integration tests for the full pipeline (input → LLM agent → output).
- Create test fixtures for edge cases (ambiguous notes, malformed input, etc.).
- Set up GitHub Actions or other CI for automated testing.

---

## 10. **CLI or Minimal UI**

- Implement a CLI interface for running the pipeline:
  - Specify input/output files, config, and debug mode.
  - Optionally, add a simple web UI for batch uploads and clarification dialogs.

---

## 11. **Documentation and Examples**

- Update `README.md` with usage instructions and example commands.
- Add example input/output files to `docs/examples/`.
- Document the LLM prompt/response schema in the technical spec.

---

## 12. **Milestones & Timeline (suggested order)**

1. Data models and file I/O (2–3 days)
2. LLM agent integration and prompt design (3–5 days)
3. Clarification loop and post-processing (2–3 days)
4. Testing and validation (2–3 days)
5. CLI/UI and documentation (2–3 days)
6. Final review, polish, and release (1–2 days)

---

## 13. **Future Enhancements (Post-MVP)**

- Add support for additional input/output formats (e.g., Excel, JSON).
- Integrate with productivity tools (Notion, Todoist, etc.).
- Add a plugin system for custom enrichment steps.
- Support for multiple LLM providers or local models.
- Advanced analytics and reporting.

---

**Would you like a breakdown of any step, or help with the first implementation tasks?** 