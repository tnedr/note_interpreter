# Folder Structure Guidelines

## Purpose
This document provides best practices for organizing the folder structure of large, scalable projects.

## Key Principles
- **Numeric Prefixes:** Use `01_`, `02_`, etc. to enforce logical order and grouping.
- **Thematic Blocks:** Group related content by theme or function (e.g., `20_data/`, `41_projects/`).
- **Meta vs. Solution:** Separate meta/documentation (`01_meta/`) from solution code (agents, libs, etc.).
- **Mini-Projects:** For subprojects, use `project_<name>/` with its own main folder and meta.
- **Recursive Application:** Apply these principles at every level of the project hierarchy.

## Example Structure
```
solution_root/
  01_meta/
    best_practices/
      naming_guidelines.md
      overview_doc_best_practice.md
      folder_structure_guidelines.md
      ai_collaboration_rules.md
    file_index.md
    ...
  02_agents/
  03_libs/
  04_tests/
  project_blablabla/
    blablabla/
      __init__.py
      ...
    01_meta/
      file_index.md
      ...
    02_utils/
    03_models/
  ...
```

## Rationale
- **Clarity:** Makes navigation and onboarding easier.
- **Scalability:** Supports growth and multiple subprojects.
- **Consistency:** Reduces confusion and duplication.

---
*Use these guidelines to keep your project structure clean, logical, and future-proof.* 