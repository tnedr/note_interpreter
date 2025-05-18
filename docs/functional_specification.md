# ⚙️ Functional Specification – AI-Powered Note Understanding and Enrichment System

**Version:** 1.5  
**Author:** DrTamasNagy  
**Date:** 2025-05-17

---

## 1. 🎯 Purpose

This document defines the functional behavior of the AI-powered note enrichment system. It specifies how short user-created notes are scored, clarified if needed, rewritten into a fully interpretable format, and enriched with structured metadata. The goal is to ensure each note becomes standalone, actionable, and context-aware, enabling integration into downstream workflows.

---

## 2. 📥 Input Specification

### Classification Configuration (YAML Input)

In addition to note and context files, the system requires a YAML file that defines accepted classification types. This allows the `entity_type` and `intent` metadata fields to be aligned with a user-defined taxonomy.

**Classification YAML (required):**
```yaml
entity_types:
  - task
  - project
  - idea
  - note
  - routine
  - reference
  - log
  - conversation
  - wish
  - trigger
  - feedback
  - signal
  - bookmark
  - role
  - template
  - suggestion
  - decision
  - question
  - insight
  - hypothesis
  - workflow
intents:
  - @DO
  - @THINK
  - @PLAN
  - @BUILD
  - @LEARN
  - @REVIEW
  - @MEET
  - @BUY
  - @WAITING
  - @REFLECT
  - @DECIDE
```

- This classification file is used during metadata enrichment (see Section 3.4) to validate outputs and enforce consistency with user-defined vocabularies.


**Definition:**
A *note* refers to a short, user-written text input that may be ambiguous or incomplete, which the system will interpret, clarify if needed, and enrich into a structured entity.


### 2.1 Inputs

- **Notes Input (CSV):**
  - One note per row
  - Only one field per row (no ID column)
  - Text content must be <= 300 characters

- **User Memory Input (Markdown):**
  - Markdown-style `.md` document
  - Each line must start with a `* ` bullet
  - Each entry must be a standalone, grammatically complete sentence
  - Used for long-term enrichment, scoring, and clarification context

### 2.2 Input Example

**Notes CSV:**
```
continue plan
email John re demo
```

**User Memory Input (Markdown):**
```
* Tamas is working on a project called LifeOS
* Tamas wants to learn specific tricks with big weapons
```

> Note: Each user memory entry must begin with `* ` (Markdown-style bullet). This is a standalone Markdown file and should follow the long-term memory format described in Section 9.2.

---

## 3. 🔁 Processing Pipeline

### 3.1 Step 1: Contextual Scoring

Each note is scored by the AI considering:
- The note itself
- The full **user context** (from context CSV)
- **Other notes in the same input batch** (to detect patterns and references)

| Score              | Range | Description |
|-------------------|-------|-------------|
| understandability  | 0–100 | grammar and clarity for AI parsing |
| interpretability   | 0–100 | AI's ability to map meaning to user memory/context |
| ambiguity          | 0–100 | multiple valid interpretations requiring clarification |
| confidence         | 0–100 | AI's certainty in chosen interpretation |

> **Clarification Trigger:**
> If `confidence < 70` or `ambiguity > 60`, system initiates a clarification dialog. See Section 5 for configurable threshold values.

---

### 3.2 Step 2: Clarification Q&A (If Triggered)

- AI generates targeted questions to resolve ambiguity
- The system supports up to 2 clarification rounds per note to balance clarity and simplicity
- Questions and empty answer fields are appended to the note's row in the CSV:
  - `Q1`, `A1`, `Q2`, `A2`, etc.
- User provides answers manually into `A1`, `A2`, etc.
- Answers are reused in interpretation and update global user context

---

### 3.3 Step 3: Textual Interpretation

The AI rewrites the note into a complete and unambiguous sentence. This process focuses on language enrichment and contextual clarity. It must result in a grammatically correct, self-contained output.

This is distinct from metadata enrichment (Step 4), which translates the interpreted meaning into structured, machine-readable fields like entity_type and intent. While interpretation supports human understanding, metadata supports system actions and automation.

- Resolves ambiguity
- Integrates relevant context and clarifications
- Is grammatically correct and meaningful on its own

---

### 3.4 Step 4: Metadata Enrichment

Each interpreted note is tagged with metadata based on a simplified semantic model. Only two metadata fields are required: `entity_type` and `intent`. All others (e.g., status markers, tags) are optional and may be inferred later using the user's life model or project taxonomy. These two fields drive downstream action (e.g., routing to task manager or idea tracker).

The system uses the provided classification YAML input (see Section 2) to validate and constrain metadata generation. If a metadata value (either `entity_type` or `intent`) inferred by the AI is not listed in the YAML file, it is flagged with a special prefix: `MISSING_suggested:...`. For example, if the AI suggests an `entity_type` of `goal` or an `intent` of `@DEFINE` that are not in the YAML, the results would be: `MISSING_suggested:goal` and `MISSING_suggested:@DEFINE`.

This preserves structure while allowing downstream review and potential YAML extension. Additional metadata fields (e.g., tags, status) may be introduced in future system versions.

| Field          | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| entity_type    | One of the defined types (e.g., task, idea, project, routine, etc.)         |
| intent         | Describes the action or mental process (e.g., @DO, @THINK, @PLAN, etc.)     |
| clarity_score  | 0–100 post-enrichment clarity and completeness                              |

> ⚠️ **Metadata is critical** – it determines downstream action (e.g., sending to task manager).

---

### 3.5 Step 5: Long-Term Memory Update

> ⚠️ Note: The specific mechanisms by which the LLM agent processes notes, prompts for clarification, and finalizes interpretation are defined in the system's Technical Design Document.


After processing (including interpretation and optional clarification), the system appends relevant information to the narrative-style user memory. This ensures future improvements in AI interpretation and clarification.

Types of updates include:
- Terms, projects, or shorthand clarified in Q&A
- Inferred intents, phrasing patterns, or emerging topic relevance
- Newly mentioned systems, tools, or recurring action structures

The memory is append-only and supports either per-note or per-batch updating.

See [Section 9](#9-🧠-user-memory-update) for details.

## 4. 📤 Output Specification

### 4.1 Final Output Format (Per Note)

The output format mirrors the structure and sequence of processing defined in Sections 3.1–3.4, enabling traceability and alignment with the system's logic.
Output is represented in enhanced CSV format.

### Example Output Row (CSV):
| Note           | Understandability | Interpretability | Ambiguity | Confidence | Interpreted Text                                             | Clarity Score | Q1                          | A1                             | entity_type | intent   |
|----------------|-------------------|-------------------|-----------|-------------|---------------------------------------------------------------|----------------|------------------------------|--------------------------------|--------------|----------|
| plan email sequence  | 75                | 65                | 70        | 50          | Continue working on the Q3 launch email sequence.          | 92             | Which plan are you referring to? | Q3 marketing launch plan | task         | @DO |


---

## 5. 🔧 Configurable Parameters

> 🧪 In development or debug mode, the system may output logs explaining:
> - Why clarification was triggered
> - Which scores fell below threshold
> - How interpretation was generated
> - Any uncertainty or fallback logic used

| Parameter             | Default | Valid Range | Description                                                       |
|-----------------------|---------|-------------|-------------------------------------------------------------------|
| confidence_threshold  | 70      | 0–100       | Confidence score below this value triggers clarification         |
| ambiguity_threshold   | 60      | 0–100       | Ambiguity score above this value triggers clarification          |
| clarity_score_target  | 90      | 0–100       | Target minimum clarity score for a note to be considered complete|
| max_input_length      | 300     | Positive int| Maximum number of characters allowed in raw input notes          |
| classification_source | yaml    | 'yaml'      | Source of classification list; required YAML file defines allowed `entity_type` and `intent` values |

---

## 6. 🚨 Edge Case Handling

| Condition                    | Handling                                                          |
|-----------------------------|--------------------------------------------------------------------|
| Clarification limit exceeded | Flag note as unresolved; log for manual intervention              |

---

## 7. ✅ Completion Criteria

A note is fully processed when:
- Scores are calculated using context
- Clarification fields (if needed) are filled
- Interpreted text is generated
- Metadata is present, including both `entity_type` and `intent`
- Clarity score >= target

---

## 8. 📂 Output Integration

_This system does not push enriched notes into downstream systems directly. It produces a CSV output which can be consumed by other agents or tools._

---

## 9. 🧠 User Memory Update

> ⚠️ Note: The orchestration of LLM behavior (e.g., using memory and batch inputs to generate clarifications and enriched notes) is handled by the system's LLM agent, as described in the Technical Design Document.

The system maintains and evolves a narrative-style user memory that stores relevant personal context, behavioral patterns, goals, and interpreted semantics. This memory enables the system to improve its understanding of shorthand, preferences, and ambiguity over time.

Append-Only Memory Behavior:
The user memory is maintained as an append-only log. Once a memory entry is added, it is never modified or deleted. This approach ensures full traceability, auditability, and preserves the complete historical context of the user's interactions.
In future versions, the system may introduce mechanisms to mark entries as deprecated or archived when they become irrelevant (e.g., completed or closed projects). However, even then, no entries will be deleted or edited, maintaining the integrity of the historical record.

### 9.1 Update Triggers
User memory is actively used as part of the prompt input for the large language model (LLM). During batch processing:
- The full long-term narrative memory is included as part of the prompt context for the LLM at every interpretation step.
- This ensures the LLM has access to evolving user understanding and can provide higher-fidelity interpretation and clarification.
User memory updates occur:
- After processing each batch or per note session (based on system configuration).
- Typically append-only to preserve historical context.
- Future versions may allow deferred or periodic updates (e.g., daily).
- Memory entries may be marked as deprecated if they become irrelevant (e.g., completed or closed projects), but this is not currently implemented.

### 9.2 Update Content
The system appends new information to user memory based on:
- Terms, projects, or shorthand clarified in Q&A sessions.
- Inferred intents, phrasing patterns, or emerging topic relevance from interpreted notes.
- Newly mentioned systems, tools, or recurring action structures.
- Intent-entity_type mappings emerging from user interactions.
- Patterns that help reduce the need for repetitive clarifications.

### 9.3 Memory Format and Rules
User memory is recorded as a freeform narrative document written in natural language. To optimize for both AI and human readability:
- Memory entries are prefixed with a Markdown-style bullet (e.g., *).
- Each entry must be a grammatically complete, standalone sentence.
- Cross-line dependencies are discouraged; each block should stand on its own.

Example:
```
* Tamas is currently working on a Q3 marketing launch plan. He often uses shorthand like "plan" to refer to this. He prefers direct action phrasing like "continue working on."

* Tamas uses Make.com and Canva for automating Instagram post generation. He often journals ideas and project drafts in Logseq.
```

This memory:
- Is human-readable and editable.
- Can be incrementally appended after each processing batch.
- Is included in LLM prompts during scoring, clarification, and interpretation phases.

### 9.3 Purpose and Benefits
- To continuously improve the AI's ability to interpret and clarify the user's notes.
- To reduce repetitive clarifications by learning from past interactions.
- To tailor interpretations to the user's style and preferences.
- To allow the system to evolve in alignment with the user's changing context.


---

## 10. 📘 Glossary

**Input Concepts**

| Term              | Definition                                                                 |
|-------------------|----------------------------------------------------------------------------|
| Note              | A short, user-written input to be interpreted                             |
| Clarification     | AI-generated question to resolve ambiguity in a note                      |
| Clarification Round | One back-and-forth interaction consisting of a question and user-provided answer |

**System Concepts**

| Term              | Definition                                                                 |
|-------------------|----------------------------------------------------------------------------|
| Scoring           | Metric-based evaluation of notes, including clarity, ambiguity, and confidence |
| Metadata          | Structured tags describing the note's type and intent                     |
| Entity Type       | Classification of the note's content (e.g., task, idea, project)           |
| Intent            | The user's underlying goal or mental action (e.g., @DO, @PLAN, @THINK)     |

**Output Concepts**

| Term              | Definition                                                                 |
|-------------------|----------------------------------------------------------------------------|
| Interpreted Text  | A rewritten version of the note that is unambiguous and complete          |
| Clarity Score     | Post-enrichment score reflecting how complete, understandable, and actionable the rewritten note is |
| User Memory       | Narrative-style long-term context built from past clarifications and notes | Narrative-style long-term context built from past clarifications and notes|

---

## 📌 Summary

This system transforms ambiguous user input into clear, structured, and actionable output enriched with metadata.
Its evolving user memory and modular design enable seamless integration into intelligent assistant ecosystems.
It introduces a modular, CSV-native architecture that supports batch processing, live clarification loops, and self-improving interpretation — all grounded in long-term narrative memory.
