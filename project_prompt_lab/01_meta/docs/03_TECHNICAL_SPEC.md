# Technical Specification – Prompt Lab

## 1. Overview
Brief summary of the technical approach for the Prompt Lab project.

## 2. System Architecture
- High-level architecture diagram (to be added)
- Main modules/components and their responsibilities
  - Agents
  - PromptBuilder
  - AgentCore
  - Logging/Evaluation
  - Test runners/scripts
  - Integration with LLM APIs (e.g., OpenAI)
  - StepwisePlanManager

## 3. Data Flow
- How data moves through the system (input → agent → prompt → LLM → output → evaluation)
- Stepwise/multi-turn flow description
- Example sequence diagram (to be added)

## 4. Main Components
### 4.1 Agents
- Definition, versioning, and structure
- Stepwise logic handling

### 4.2 PromptBuilder
- Loads and assembles prompts from YAML
- Supports variable interpolation and multi-step prompts

### 4.3 AgentCore
- Orchestrates agent logic, prompt execution, and LLM calls
- Handles stepwise/clarification logic

### 4.4 Logging & Evaluation
- Captures outputs, diffs, and test results
- Supports regression analysis

### 4.5 Test Runners
- Scripts for automated and manual test execution
- Integration with Promptfoo, LangSmith, etc.

### 4.6 StepwisePlanManager
Feladat: Ez a komponens olvassa a Prompt Evolution Plan fájlokat, és szekvenciálisan végigvezeti az agentet a prompt evolúció lépésein.

Funkciók:
- Plan betöltése YAML/Markdown fájlból
- Lépésenkénti prompt betöltés és tesztfuttatás
- Regressziós validáció kezelése
- Plan szerkezet validálása

Bemenetek:
- plan_path: a Prompt Evolution Plan fájl elérési útja
- agent_id: az agent azonosítója

Kimenetek:
- Futási státuszok, logok
- Regressziós teszteredmények

Bővíthetőség:
- Későbbi támogatás: vizuális plan szerkesztő, többféle fájlformátum (pl. JSON, DSL)

## 5. Interfaces
- YAML/JSON file formats for prompts, test cases, agent definitions
- Command-line interface for test runners
- (Optional) Web UI or playground integration

Prompt Evolution Plan formátum:
- Támogatott típusok: .yaml, .md
- Kötelező mezők:
  - step_name
  - goal
  - required_prompt_sections
  - expected_output_fields
  - test_focus

CLI interfész bővítése:
- Új parancs: run_stepwise --agent note_interpreter --plan clarify_plan.yaml

## 6. Technologies & Dependencies
- Python 3.x
- Pydantic (for data models)
- OpenAI API (or other LLM providers)
- Promptfoo, LangSmith (for testing)
- PyYAML, logging, etc.

## 7. Edge Cases & Error Handling
- Invalid or ambiguous input handling
- LLM API errors, timeouts, retries
- Stepwise prompt failures (e.g., clarification not provided)
- Versioning conflicts

## 8. Extensibility & Future Work
- Support for new agent types or prompt patterns
- Plug-in architecture for new LLM providers
- Advanced evaluation/metrics modules

## 9. Security & Privacy Considerations
- API key management
- Sensitive data handling in logs

## 10. Open Questions / To Be Decided
- [ ] How to handle very long multi-turn conversations?
- [ ] How to support non-OpenAI LLMs?
- [ ] ...

---

*This document is a living specification and should be updated as the project evolves.* 