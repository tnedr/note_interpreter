# Functional Specification – Prompt Lab

---

## Stepwise, Gated Prompt Evolution & Regression Policy (Core Principle)

**This is a core functional principle of the Prompt Lab.**

- **Stepwise, milestone-based development:**
  - Prompt and agent functionality is expanded in clearly defined steps (milestones).
  - Each milestone introduces new features, but all previous features and behaviors must remain intact and functional.

- **Append-only prompt evolution:**
  - Prompt versions are created in an append-only fashion: new sections or logic are added, but existing sections and logic are preserved.
  - This ensures backward compatibility and traceability of prompt evolution.

- **Gated workflow:**
  - Progression to the next milestone is only allowed if the current prompt version passes **all** tests from previous milestones, as well as new tests for the current step.
  - If any regression is detected (i.e., a previously passing test fails), the new prompt version must be fixed before moving forward.

- **Strict regression enforcement:**
  - Regression testing is mandatory at every milestone.
  - The system must automatically run all relevant tests for every prompt version and block advancement if any test fails.

- **Milestone acceptance policy:**
  - A new prompt version (milestone) is only accepted if:
    - All previous and current tests pass
    - All previous functionality is preserved
    - New features are correctly implemented and tested

- **(Optional) Example workflow:**
  ```python
  for step in stepwise_schedule:
      generate_new_prompt(step)
      for test in all_previous_and_current_tests:
          result = run_test(prompt_version=step.version, test_case=test)
          if not result.passed:
              print(f"Step {step.name} failed on test {test.name}. Fix required before proceeding.")
              break
      else:
          print(f"Step {step.name} passed all tests. Proceed to next step.")
  ```

**This policy ensures that prompt evolution is robust, traceable, and always backward compatible. It is a key differentiator of the Prompt Lab compared to ad-hoc prompt development.**

---

## 1. Purpose

Prompt Lab is a modular, extensible environment for:
- Developing, versioning, and maintaining prompts for LLM-based agents.
- Testing prompt behavior with realistic, versioned input scenarios.
- Automating regression testing and output comparison across prompt versions.
- Supporting stepwise, multi-turn agent prompt pipelines (clarification, memory, etc.).
- Enabling prompt engineering as a disciplined, test-driven process.

---

## 2. Main User Stories / Use Cases

- **Prompt Engineer:**
  - Can create, edit, and version prompt YAMLs for any agent.
  - Can define and run test cases (input + expected output) for any prompt version.
  - Can compare outputs across prompt versions to detect regressions or improvements.
  - Can view logs, diffs, and regression reports for all test runs.
  - Can add new agents, prompt pipelines, or test scenarios without changing core lab code.

- **Researcher/Team Lead:**
  - Can audit the evolution of prompts and agent behavior over time.
  - Can ensure that all prompt changes are regression-tested before deployment.

- **CI/CD Pipeline:**
  - Can run all prompt regression tests automatically and report failures.

---

## 3. Functional Requirements

### 3.1 Prompt Management
- Store prompt templates in versioned YAML files, organized by agent and version.
- Support arbitrary prompt structure (section-based, multi-turn, etc.).
- Allow prompt metadata (description, changelog, test coverage) alongside each version.

### 3.2 Test Case Management
- Store test cases as YAML/JSON files, each with input and expected output.
- Support both single-turn and multi-turn (clarification loop) scenarios.
- Allow test cases to be reused across prompt versions.

### 3.3 Test Execution & Evaluation
- Run all test cases against all relevant prompt versions.
- Log all outputs, including raw LLM output, diffs, and pass/fail status.
- Support both automated (assert-based) and manual (human-in-the-loop) evaluation.
- Allow for regression detection: highlight when a new prompt version fails a previously passing test.

### 3.4 Results & Reporting
- Store all test run results, logs, and diffs in a structured, timestamped way.
- Provide summary reports of test coverage, regressions, and prompt evolution.

### 3.5 Extensibility & Modularity
- New agents, prompt pipelines, or test scenarios can be added by creating new files/folders, not by editing core code.
- Core logic (PromptBuilder, AgentCore, test runner) is reusable and agent-agnostic.
- Support for multiple LLM providers and test runners (Promptfoo, LangSmith, etc.).

### 3.6 Stepwise Prompt Development Support
A rendszer támogatja a promptok lépésenkénti, milestone-alapú fejlesztését egy ún. Prompt Evolution Plan alapján.

A Prompt Evolution Plan egy struktúrált dokumentum (pl. YAML vagy Markdown), amely definiálja:
- A promptfejlesztés lépéseit (scoring, interpretation, clarification, stb.)
- Minden lépéshez tartozó új prompt szekciókat és elvárt output mezőket
- A regressziós tesztelés követelményeit

A StepwisePlanManager automatikusan értelmezi és vezérli a prompt evolúcióját:
- Minden új lépés csak akkor aktiválható, ha az előző lépésekhez tartozó összes teszt sikeresen lefutott.
- A fejlesztő (prompt engineer) csak új funkciók hozzáadásával módosíthatja a promptot – meglévő logika nem törölhető (append-only elv).

### Prompt Attempts & Iterative Learning (Human-in-the-loop support)

- A Prompt Lab támogatja, hogy egyetlen step több prompt verzión keresztül valósuljon meg.
- Minden új funkció (milestone) implementációját több próbálkozás (prompt attempt) előzheti meg.
- Egy *Prompt Attempt*:
  - Egy konkrét prompt YAML fájl (pl. `v1.2.yaml`)
  - Hozzá tartozó manuális és/vagy gépi értékelési log (`v1.2__log.md`)
  - Metaadat (status: passed/failed, timestamp, human notes, etc.)

#### Cél
- A fejlesztő dokumentálhassa, hogy egy adott prompt verzió miért működött vagy nem működött.
- A StepwisePlanManager képes legyen ezekhez a próbálkozásokhoz rendelni tapasztalatokat.
- Ezek a tapasztalatok később gépi tanulás, AI-javaslatgenerálás alapját képezhetik.

#### Naplózás módjai
- A prompt fájlban opcionálisan szerepelhet egy `meta` blokk.
- A részletes leírás külön `.md` fájlban vezethető (`logs/v1.2__log.md`)
- Egy stephez több ilyen próbálkozás tartozhat.

#### Példa fájlstruktúra egy stepre
clarify_agent/
step_02_interpretation/
prompts/
v1.1_failed.yaml
v1.2_final.yaml
logs/
v1.1__log.md
v1.2__log.md
attempts_index.yaml (opcionális összefoglaló)

---

## 4. Supported Workflows

- **Stepwise Prompt Development:**
  - Add new prompt version → Add/modify test cases → Run tests → Review results → Iterate.
- **Regression Testing:**
  - Run all tests on all prompt versions before merging/deploying changes.
- **Prompt Comparison:**
  - Compare outputs and diffs between prompt versions for the same test cases.
- **Multi-agent Support:**
  - Add new agent folders with their own prompts and test cases.

### Evolution-based Agent Development
Minden agent fejlesztése egy Prompt Evolution Plan alapján történik.

A workflow:
- Új prompt evolúciós terv létrehozása (prompt_plans/<agent_name>_plan.yaml)
- Prompt verziók implementálása minden milestone-hoz
- Tesztesetek futtatása minden korábbi és aktuális milestone-ra
- Regressziós validáció

Ez lehetővé teszi, hogy komplex funkciókat lépésről lépésre, kontrolláltan építsünk fel.

---

## 5. Boundaries / Out of Scope

- The lab does **not** define or constrain the internal logic of the agents being tested.
- The lab does **not** provide a UI (CLI/scripts only, unless extended).
- The lab does **not** manage LLM API keys or user authentication.
- The lab does **not** enforce a specific prompt schema, but provides best practices and validation tools.

---

## 6. References
- See `README.md` for system overview and philosophy.
- See `TESTING_MASTER_GUIDE.md` for detailed testing principles and schemas.
- See `STEPWISE_PROMPT_IMPLEMENTATION_PLAN.md` for implementation workflow. 