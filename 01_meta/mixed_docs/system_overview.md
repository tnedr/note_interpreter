# 🧠 System Overview: AI-Powered Note Understanding and Enrichment System

**Author:** DrTamasNagy_with_MarkdownRefiner  
**Date:** 2025-05-17  
**Version:** 2

## 🔑 Key Terminology

- **Raw Entity**: A short note or phrase (e.g., "check launch plan") representing an incomplete or ambiguous user input.
- **Interpreted Text**: The fully rewritten version of the raw entity, enriched with full context and clarity.
- **User Context**: Background information maintained across sessions to help interpret shorthand or ambiguous notes more accurately.
- **Clarification Q&A**: Dialog exchanges between AI and user to resolve ambiguities before interpretation.
- **Metadata**: Structured tags (like type and intent) that classify the interpreted text for downstream use.

## 1. Goal

To create a system that processes structured notes, each note representing a single "raw entity." The system uses a large language model (LLM) to interpret, enrich, and clarify each entity — making it fully understandable, unambiguous, and actionable.

## 2. 🔁 Processing Pipeline

This pipeline outlines the end-to-end journey of each note, transforming a short, ambiguous input into a clear, enriched, and structured entity. It ensures traceability, enables clarification when needed, and ultimately produces standalone, actionable outputs.

### 2.1 Visual Overview

```plaintext
[Raw Input]
     ↓
[Pre-Enrichment Scoring]
     ↓
[Clarification (if needed)]
     ↓
[Textual Interpretation]
     ↓
[Metadata Enrichment]
     ↓
[Structured Output]
```

### 2.2 Raw Input

- Each input note (a "raw entity") is a standalone sentence or phrase entered by the user.
- Notes are processed in batches, with user context and classification config as additional inputs.

### 2.3 Scoring Phase (Pre-Enrichment)

The AI assesses how well it understands the raw input before trying to enrich it. It computes four scores:
- **Understandability**: How grammatically and syntactically clear the sentence is.
- **Interpretability**: How well the AI can map the sentence to a meaning using user context.
- **Ambiguity**: How many valid interpretations the input might have.
- **Confidence**: How confident the AI is in its chosen interpretation.

### 2.4 Clarification Phase (If Needed)

- If confidence is low or ambiguity is high, the AI engages in a back-and-forth with the user to clarify.
- The user answers clarifying questions.
- These answers, plus the user context and the raw input, become the clarification base.

### 2.5 Interpretation (Textual Enrichment)

The AI rewrites the entity as a fully clarified, complete, and self-contained sentence.

The output should:
- Be grammatically correct
- Contain no ambiguity
- Include all necessary context
- Make sense on its own — even without the raw input or Q&A

### 2.6 Metadata Enrichment

After interpretation, the AI assigns structured metadata to the interpreted entity, such as:
- **entity_type**: Task, idea, project, question, etc.
- **intent**: Human intent behind the note (e.g., continue, review, plan)

### 2.7 Structured Output Data

Each processed note is enriched with the following fields:
- Raw input
- Scores (understandability, interpretability, ambiguity, confidence)
- Clarification Q&A (if needed)
- Interpreted text
- Clarity score
- Metadata (entity_type, intent, etc.)

> **Note:** The specific output file format (CSV, JSON, etc.) and column structure are defined in the functional and technical specifications.

## 3. 🧠 User Context & Memory (Evolving)

The system maintains a user context to help the AI interpret raw notes more accurately. This includes:
- Known project names or acronyms
- Personal vocabulary or shorthand
- Preferred phrasing or style
- Common tasks or workflows
- Past interpreted notes
- Clarifications given in previous sessions

The context is:
- Editable directly by the user
- Updated after each batch of notes is processed
- Used during interpretation before prompting questions
- Persistent across sessions to enable continuous improvement

## 4. ✅ Design Principles & Core Guidelines

- One note = one entity
- Scores guide the need for clarification
- Interpretation is only finalized when ambiguity is resolved
- Final result must be fully understandable on its own
- All steps are logged and traceable
- The system can evolve toward an assistant or agent, but the core logic remains tool-based
- The `interpreted_text` should make sense on its own, even if someone sees just that one field

## 5. 🔚 Conclusion

This system transforms raw, often ambiguous notes into clear, contextualized, and structured insights. By combining scoring, clarification, enrichment, and metadata tagging, it ensures each input becomes actionable. Its evolving user context and modular design position it well for integration into productivity tools, personal knowledge bases, or intelligent assistants.

---

[^1]: **Scoring Definitions**:
- *Understandability*: Measures clarity of phrasing and grammar.
- *Interpretability*: Measures how easily the AI can map the note to intent or context.
- *Ambiguity*: Detects whether the note could have multiple meanings.
- *Confidence*: Reflects AI's certainty about its interpretation.

[^2]: **Metadata Fields**:
- *entity_type*: Categorizes the nature of the note (task, idea, etc.)
- *intent*: Indicates the user's goal (e.g., review, initiate).
- *clarity_score*: Measures how clear and actionable the final interpreted text is, post-enrichment.
