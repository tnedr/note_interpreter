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

### Attempt-level tracking and experience logging

A StepwisePlanManager támogatja az iteratív promptfejlesztést step szinten:
- Minden prompt fájlhoz metaadatot rendelhet (`meta` blokk vagy külön `.md`)
- Automatikusan nyilvántartja, hogy melyik próbálkozás mikor és miért lett sikeres/sikertelen
- Opcionálisan aggregálhatja az attempt logokat egy `attempts_index.yaml` fájlba

#### Példák
- `v1.2.yaml`: meta blokk (status, attempt_id, author, timestamp)
- `v1.2__log.md`: részletes leírás a hibáról és a tapasztalatról

A rendszer lehetővé teszi a tapasztalati naplók visszacsatolását más komponensekhez (pl. AI javaslatgeneráláshoz).

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

### Prompt Attempt Metadata & Logs

#### 1. Prompt fájl `meta` szekció (opcionális)
```yaml
meta:
  attempt_id: "attempt_003"
  status: "failed"
  author: "tamas"
  timestamp: "2025-05-27T14:12"
  notes:
    - "clarity_score missing"
    - "LLM interpreted vague instruction"
```

#### 2. Log fájl formátum (logs/attempt_003__log.md)
```markdown
# Log for attempt_003 (prompt: v1.2.yaml)

## Issues Encountered
- Output field `clarity_score` was null
- LLM misunderstood instruction

## Root Cause
- Missing schema section in prompt

## Fix Plan
- Add output_schema section with explicit field description

## Human Notes
Likely fixed by adding examples to scoring_guidelines.

*Created by: tamas on 2025-05-27*
```

#### 3. (Opcionális) attempts_index.yaml
```yaml
attempts:
  - id: "attempt_003"
    prompt: "v1.2.yaml"
    log: "v1.2__log.md"
    status: "failed"
    timestamp: "2025-05-27"
    notes: ["clarity_score missing", "unclear scoring"]
```

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

# 03\_TECHNICAL\_SPEC.md – Prompt Lab Technikai Specifikáció

# 03\_TECHNICAL\_SPEC.md – Prompt Lab Technikai Specifikáció

## 🧱 Könyvtárszerkezet (Folder Structure)

A Prompt Lab rendszer fő komponensei a `prompt_lab/` könyvtáron belül helyezkednek el:

```
prompt_lab/
├── agents/                # Agent-specifikus mappa
│   └── grocery_clarifier/
│       ├── prompts/      # Prompt sablonok: s<step>_v<version>.yaml
│       ├── test_cases/   # Tesztfájlok: test_s<step>_XX.yaml
│       ├── outputs/      # LLM output dumpok
│       ├── logs/         # Automatikus gépi logok
│       ├── attempts_index.yaml  # Minden próbálkozás összefoglalója
│       ├── plan.md       # Stepwise roadmap
│       └── overview.md   # Leírás az agentről
├── libs/                 # Újrafelhasználható Python modulok
├── scripts/              # CLI, futtató szkriptek
├── docs/                 # Specifikációk, útmutatók
├── templates/            # Minták, sablonok
├── other/                # Archív, referencia, régi planek stb.
└── README.md
```

---

## 📄 Fájltípusok és szerepeik

| Fájlnév példa           | Kiterjesztés      | Tartalom                                                       | Hely                 | Megjegyzés            |
| ----------------------- | ----------------- | -------------------------------------------------------------- | -------------------- | --------------------- |
| `s3_v1.yaml`            | `.yaml`           | Prompt sablon `{input}` változóval, opcionális `meta:` blokkal | `prompts/`           | Aktív verziók         |
| `test_s3_01.yaml`       | `.yaml`           | input + expected                                               | `test_cases/`        | Teszt összevetéshez   |
| `s3_v1__output_01.json` | `.json` / `.yaml` | LLM válasz                                                     | `outputs/`           | Opcionális            |
| `s3_v1__log.md`         | `.md`             | Automatikus log (diff, match)                                  | `logs/`              | Kötelező              |
| `attempts_index.yaml`   | `.yaml`           | Minden próbálkozás metaadata                                   | gyökér (agent alatt) | `step:` mező kötelező |
| `plan.md`               | `.md`             | Prompt evolution roadmap                                       | gyökér               | Step-leírás           |
| `overview.md`           | `.md`             | Rövid leírás az agent céljáról                                 | gyökér               | Emberi dokumentáció   |

---

## 🧠 Prompt Attempt logikai struktúra (attempts\_index.yaml)

```yaml
attempts:
  - id: "s3_v1__2025-05-27__01"
    step: "step_3"
    prompt: "prompts/s3_v1.yaml"
    input:
      note: "tej"
    test_case: "test_cases/test_s3_01.yaml"
    output: "outputs/s3_v1__output_01.json"
    log: "logs/s3_v1__log.md"
    status:
      auto: "failed"
      manual: "needs_review"
    feedback:
      author: "tamas"
      notes:
        - "Nem generált kérdést, pedig kellett volna."
        - "Talán hiányzott a clarification prompt rész."
    timestamp: "2025-05-27T14:52"

  - id: "s3_v1__2025-05-27__02"
    step: "step_3"
    prompt: "prompts/s3_v1.yaml"
    input:
      note: "tej"
    test_case: "test_cases/test_s3_01.yaml"
    output: "outputs/s3_v1__output_02.json"
    log: "logs/s3_v1__log_2.md"
    status:
      auto: "passed"
      manual: "approved"
    feedback:
      author: "tamas"
      notes:
        - "Kiváló output, strukturált kérdéssel."
        - "Prompt jól működik ebben a step-ben."
    timestamp: "2025-05-27T15:20"
```

---

Ez a struktúra biztosítja, hogy minden prompt próbálkozás teljes körűen dokumentált és reprodukálható legyen. A step–prompt–attempt láncolat gépi és humán oldalról is nyomon követhető.

*A Prompt Lab rendszer technikai specifikációja ezzel teljes körű támogatást ad a stepwise prompt engineering workflow-hoz.*
