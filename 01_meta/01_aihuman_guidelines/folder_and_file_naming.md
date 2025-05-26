# Naming Guidelines for Python Projects

## 1. Project Structure & Organization

- The main solution folder (project root) may contain:
  - A `meta/` or `01_meta/` folder for documentation, file indexes, naming guidelines, and other meta resources.
  - Numbered main folders (e.g., `02_agents/`, `03_libs/`, etc.) for core solution components, where the prefix reflects logical or workflow order.
  - One or more **mini-projects** (subprojects) inside the solution. Each mini-project should be named `project_<name>/` and contain a main subfolder `<name>/` for the actual Python package or code.
    - Example: `project_blablabla/blablabla/`
  - Each mini-project can have its own `meta/` or `01_meta/` folder, and follow the same structure as the main solution.

**This structure ensures:**
- Clear separation of meta/documentation and solution code.
- Logical ordering and easy navigation.
- Scalable organization for multiple subprojects within a larger solution.

### Example

```
solution_root/
  01_meta/
    file_index.md
    naming_guidelines.md
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

## 2. Project Root vs. Package Naming
- **Do NOT use the same name for the project root and the main Python package.**
  - ❌ Bad: `myproject/myproject/`
  - ✅ Good: `myproject_root/myproject/` or `myproject_solution/myproject/`
- The project root can be descriptive (e.g., `myproject_root`), while the package folder should be short and import-friendly (e.g., `myproject`).

## 3. Python Package & Module Naming
- Use **lowercase_with_underscores** for package and module names.
- Avoid special characters and spaces.
- Example:
  - `myproject/agents/`
  - `myproject/libs/`
  - `myproject/utils.py`

## 4. Numeric Prefixes for Folders and Files
- Use **numeric prefixes** (e.g., `01_`, `02_`, ...) to enforce logical ordering in folders and files.
- **Purpose:**
  - Ensures that items appear in a consistent, intended order in directory listings, regardless of alphabetical sorting.
  - Makes onboarding and navigation easier for new contributors.
- **How to assign numbers:**
  - Start with `01_` for the most important or first-to-read item (e.g., `01_README.md`, `01_agents/`).
  - Continue incrementally (`02_`, `03_`, ...) for subsequent items, following the logical workflow or usage order.
  - Reserve high numbers (e.g., `90_`, `99_`) for meta, templates, or rarely used resources.
  - When adding new items, choose a number that fits the intended position in the workflow or documentation sequence.
- **Best practices:**
  - Keep numbers two digits for consistency (`01_`, `02_`, ..., `10_`, ...).
  - Avoid renumbering unless absolutely necessary; use gaps (e.g., `05_`, `07_`) to allow for future insertions.
  - Document the numbering scheme in the README or a dedicated guidelines file.

## 5. Folder Naming for Solution vs. Meta
- **Solution code** (agents, libs, test_inputs, etc.) should use numeric prefixes for logical ordering:
  - `01_agents/`, `02_libs/`, `03_test_inputs/`, ...
- **Meta/documentation** folders should use high numeric prefixes (e.g., `90_`, `99_`) or be grouped under a `meta/` or `docs/` folder:
  - `90_docs/`, `99_templates/`, or `meta/`, `docs/`
- This keeps solution and meta resources visually and structurally separated.

## 6. File Naming
- Use **lowercase_with_underscores** for Python files and modules.
- Use **numeric prefixes** for documentation files to enforce logical reading order:
  - `01_README.md`, `02_FUNCTIONAL_SPEC.md`, `03_TECHNICAL_SPEC.md`, ...
- For templates or guides, use high numbers or a `template_`/`guide_` prefix:
  - `99_naming_guidelines.md`, `template_agent_test_plan.md`

## 7. General Best Practices
- Be descriptive but concise.
- Avoid ambiguous or overloaded names.
- Use English for all code and documentation file/folder names.
- For new folders/files, check for existing names to avoid duplication.

## 8. Example Structure
```
myproject_root/
  myproject/           # Python package
    __init__.py
    01_agents/
    02_libs/
    ...
  docs/
    01_README.md
    02_FUNCTIONAL_SPEC.md
    03_TECHNICAL_SPEC.md
    04_implementation_plan.md
    05_agent_test_plan_template.md
    06_TESTING_MASTER_GUIDE.md
    07_stepwise_prompt_engineering_plan.md
    99_naming_guidelines.md
  tests/
  requirements.txt
  setup.py
```

## 9. Rationale
- **Clarity:** New contributors can easily navigate and understand the project.
- **Maintainability:** Avoids import and packaging issues.
- **Scalability:** Easy to add new modules, docs, or meta resources without confusion.

---

*Follow these guidelines to keep your Python projects clean, scalable, and professional.* 