# Best Practice: Writing Effective overview.md Files

## Purpose
This document provides guidelines for creating clear, useful `overview.md` files in any project folder. A well-structured overview.md helps both humans and AI agents understand the folder's role, contents, and usage.

## Recommended Sections
- **Purpose:** Why does this folder exist? What is its main goal?
- **Context:** How does this folder relate to the rest of the project? What workflows or dependencies are relevant?
- **Usage:** How should this folder be used? Are there naming conventions, contribution rules, or special instructions?
- **File Index:** (Optionally auto-generated) List and briefly describe all files and subfolders.
- **Workflow/Examples:** Typical use cases, best practices, or example scenarios.
- **History/Changelog:** (Optional) Major changes, milestones, or version notes.

## Rationale
- A single, well-structured overview.md makes onboarding, navigation, and AI collaboration easier.
- Keeps all relevant information in one place, reducing confusion and duplication.

## Template Example

```markdown
# <Folder Name> Overview

## Purpose
Describe the main goal of this folder.

## Context
Explain how this folder fits into the overall project.

## Usage
How should this folder be used? Any conventions or rules?

## File Index
- file1.md – short description
- subfolder/ – short description

## Workflow/Examples
Describe typical workflows or provide usage examples.

## History/Changelog
(Optional) List major changes or milestones.
```

---
*Follow this template to ensure every folder in your project is well-documented and easy to understand.* 



# 📂 Folder: [folder_name]

## 📌 Purpose
What is the purpose of this folder?  
Describe its role in the broader system or workflow.

## 🧭 Context
- Where does this folder fit into the overall architecture?
- Which upstream/downstream components does it connect to?
- Any dependencies?

## ⚙️ Usage
- When and how is this folder accessed or used?
- By which scripts, agents, users, or external tools?

## 🗂️ File Index
Brief description of key files and their functions.

| File Name           | Description                          |
|---------------------|--------------------------------------|
| `example.json`      | Raw user input                       |
| `process.py`        | Cleans and validates JSON structure  |

## 🔁 Workflow Role
- Stage: [e.g. preprocessing → modeling → postprocessing]
- Is it part of a pipeline? If yes, which step?
- Trigger mechanism (manual, scheduled, triggered by agent X)

## 🧠 Technical Notes
- Known edge cases
- File naming patterns, expected formats
- Versioning conventions or gotchas

## 📈 Changelog
| Date       | Change                                     | Author   |
|------------|--------------------------------------------|----------|
| 2025-05-27 | Created initial folder and structure       | Tamas    |
| 2025-06-01 | Added input schema and JSON validator tool | Levi     |

## 🧮 Metadata (for AI use)
```yaml
type: [raw_data | processed_data | code | config | ...]
format: [csv | json | py | md]
stage: [dev | test | prod | archived]
status: [active | deprecated | in_review]
contains_pii: [true | false]
