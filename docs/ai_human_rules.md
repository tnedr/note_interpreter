# 🤝 AI-Human Collaboration Rules

These guidelines ensure efficient, traceable, and effective collaboration between human and AI team members in this project.

---

## 1. Documentation & File Management
- Keep Markdown files under 500 lines; split into smaller files if needed.
- Use clear section headers and cross-links between docs for navigation.
- Store all major specs, plans, and rules in the `docs/` directory.

## 2. Task & Project Tracking
- Maintain a checklist or task table in `implementation_plan.md` (or in each MVP plan file).
- Mark tasks as `[x]` (done) or `[ ]` (to-do) and update regularly.
- Keep a high-level summary of project state at the top of the plan or in a `PROJECT_STATUS.md` if needed.

## 3. Journal & Decision Logging
- Log every major event, decision, or milestone in `aihuman_journal/journal.md`.
- Use the agreed format: newest entries at the top, with a `- now [date]` marker at the bottom of each day's block.

## 4. Iterative, Test-Driven Development
- Work in small, testable increments (one class or function at a time).
- Write or update tests before/with each code change.
- Run tests frequently and fix issues immediately.

## 5. Automation
- Use scripts or CI (e.g., GitHub Actions) to run all tests on every change.
- Use templates for journal entries, test cases, and doc updates.

## 6. Explicit AI Suggestions
- For each MVP or feature, include an "AI Suggestions" subsection in the relevant plan file.
- Review and discuss these suggestions before implementation.

## 7. Communication
- Use clear, concise commit messages and journal entries.
- Summarize key decisions and observations in the journal for future reference.

---

**Tip:** You can copy these rules into a notepad in Cursor.ai for quick reference, or keep them open in a split view while working on the project. 