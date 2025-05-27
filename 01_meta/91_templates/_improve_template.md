📄 improve.md – Development, Planning, and Forward Thinking

 A running log of improvement ideas, TODOs, technical debt, and review notes for the folder. Both humans and AI agents should add to this file as they identify areas for enhancement.


# 🚀 Improvement & Development Plan: [folder_name]

## ✅ Action Items
Clear, executable tasks that should be done. Short-term and well-defined.

- [ ] Validate all JSON entries for schema compliance
- [ ] Rename files to follow consistent timestamp naming
- [ ] Add unit tests for `process.py`

## 💡 Ideas & Suggestions
Open-ended, creative, or speculative improvements.

- Use a small LLM to auto-label entries?
- Switch storage format from JSON to SQLite for better indexing?
- Consider hashing large text fields for deduplication?

## ❓ Open Questions & Decisions
Topics that require clarification, external input, or decisions.

- Do we need GDPR-compliant anonymization for this data?
- Should this folder be merged with `legacy_feedback/`?
- Who is the current owner of this module?

## 🧱 Technical Debt
Known quality problems, short-term fixes, or fragile parts that should be improved later.

- Inconsistent data cleaning logic (copied across multiple scripts)
- Hardcoded path references to `/tmp/feedback`
- No version tracking for incoming data dumps

## 🔭 Longer-Term Vision
Optional. Where could this folder/module evolve if there were time/resources?

- Refactor into microservice or agent structure
- Integrate with the future `DataValidatorAgent`
📌 Használati elv
Az Action Items a konkrét és végrehajtandó teendőkre fókuszál – ez akár egy task management rendszerbe is beolvasható (pl. Notion, GitHub Issues).

Az Ideas inkább ösztönzi a kreativitást és az LLM-es újítást.

A Questions segít LLM-eknek follow-up kérdéseket generálni.

A Technical Debt egy teherlista – refaktor prioritásban segíthet.

A Vision opcionális, de hosszabb távon értékes útmutató lehet egy ágenstervhez is.

