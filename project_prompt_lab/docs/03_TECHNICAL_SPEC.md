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

**Jelenleg a StepwisePlanManager elsődlegesen `.yaml` típusú plan fájlokat támogat, melyekben explicit módon definiálva vannak a lépések (steps), az egyes step-ekhez tartozó prompt fájl, experiment fájl(ok), elvárt output mezők és tesztelési fókusz.**

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

A Prompt Lab rendszer fő komponensei a `prompt_lab/` könyvtáron belül helyezkednek el. Minden agenthez/prompthoz dedikált almappát kell létrehozni az `agents/` alatt, és minden kapcsolódó fájlt az alábbi, számozott alkönyvtárakban kell tárolni:

```
prompt_lab/
├── agents/
│   └── grocery_clarifier/
│       ├── 01_prompts/            # Prompt sablonok: s<step>_v<version>.yaml
│       ├── 02_inputs/             # Teszt inputok (YAML, CSV, stb.)
│       ├── 03_experiment_bundles/ # YAML alapú tesztcsomagok
│       ├── 04_actual_outputs/     # LLM output dumpok
│       └── 05_logs/               # Automatikus gépi logok
├── libs/                 # Újrafelhasználható Python modulok
├── scripts/              # CLI, futtató szkriptek
├── docs/                 # Specifikációk, útmutatók
├── templates/            # Minták, sablonok
├── other/                # Archív, referencia, régi planek stb.
└── README.md
```

**Minden agent/projekt saját, jól elkülönített környezetben dolgozik, így a prompt verziózás, tesztelés és logolás átlátható és visszakereshető.**

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

## 🧪 Experiment Bundle Architecture

A rendszer YAML-alapú `experiment_bundle` formátummal támogatja a prompt-alapú tesztelést, amely egységesen kezeli a prompt definíciót, inputokat, elvárt kimenetet, modell setupot, validációs eredményeket és logolást.

### 🎯 Cél
- Átlátható, újrafuttatható prompt tesztek
- Validáció és QA automatizálása
- Prompt tuning és összehasonlítás támogatása
- Teljes log és audit trail biztosítása

### 🧱 Fájlstruktúra

agents/
grocery_clarifier/
prompts/
s1_v1.yaml
experiment_bundles/
experiment__step1__tej.yaml
experiment__step1__tej__result.yaml
actual_outputs/
output__step1__tej.json
logs/
log__step1__tej.md

### 📄 Fájl szerepkörök

| Fájl / mappa | Tartalom | Megjegyzés |
|--------------|----------|------------|
| `experiment__*.yaml` | Prompt + input + expected_output | Futtatás előtt |
| `experiment__*__result.yaml` | + actual_output + validation + log | Futtatás után generált |
| `output__*.json` | Csak actual output | Könnyebb batch elemzés |
| `log__*.md` | Részletes nyers log | Auditáláshoz, debughoz |
| `prompts/*.yaml` | Paraméterezett prompt templatek | Reuse és snapshot támogatás |

### ⚙️ Runner script

A `run_experiment_bundle.py` script funkciói:
1. Beolvassa az experiment YAML fájlt
2. Betölti a promptot (inline vagy fájlból)
3. Betölti az inputot (YAML vagy CSV)
4. Inicializálja a LLM modellt a `model` szekció alapján
5. Lefuttatja a promptot
6. Összehasonlítja az outputot az `expected_output`-tal
7. Kitölti a `actual_output`, `validation`, `log` szekciókat
8. Logol és ment (bundle-be vagy külön fájlba)

### ✅ Kompatibilitás

- A `output_validator.py` validációs függvény teljesen integrálható
- A jelenlegi logika (`prompt_builder`, `config_utils`, `log`, `user_output`) támogatja az új formátumot

További részletek külön fájlban: `docs/experiment_bundle_spec.md`
