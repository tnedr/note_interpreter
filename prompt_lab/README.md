# 🧪 Prompt Regression & Development Lab

## Overview / Áttekintés

This project is a **modular, testable, and iterative framework** for developing and validating prompts used by LLM-based agents. It is designed as a *subproject* within a larger AI agent development ecosystem, and its goal is to ensure that prompts evolve in a controlled, regression-tested manner.

Ez a projekt egy **moduláris, tesztelhető és iteratív framework** LLM-alapú ügynökök promptjainak fejlesztéséhez és validálásához. Célja, hogy a promptok kontrolláltan, regressziómentesen fejlődjenek.

This lab provides the infrastructure to:
- Develop prompts in a structured and versioned way.
- Test prompts with realistic input scenarios.
- Execute lightweight agents with those prompts.
- Analyze and log the resulting outputs.
- Compare versions to detect regressions or improvements.

A fő cél, hogy minden LLM-alapú ügynök (agent) promptjai könnyen fejleszthetők, tesztelhetők és összehasonlíthatók legyenek, valósághű inputokkal és automatizált regressziós tesztekkel.

---

## Project Goals / Projektcélok

- 🧠 Enable **prompt engineering as a software discipline**.
- 🔁 Facilitate **prompt versioning and regression detection**.
- ⚙️ Leverage **simple, reusable core libraries**: `PromptBuilder`, `AgentCore`, `Logger`.
- 📦 Isolate and test individual agent functionalities before full-scale integration.
- 💡 Serve as a test harness and ideation space for advanced agent behavior.

- A prompt engineering szoftverfejlesztési diszciplínává emelése
- Verziózás, regressziódetektálás
- Újrahasznosítható core library-k (`PromptBuilder`, `AgentCore`, `Logger`)
- Funkciók izolált tesztelése, ötletelés

---

## Project Structure / Mappastruktúra

```plaintext
prompt-lab/
│
├── README.md ← This file
├── architecture.md ← System description & data flow
│
├── agents/ ← Agent definitions + prompt versions
│   └── clarifier/
│       ├── prompts/
│       ├── test_cases/
│       └── metadata.yaml
├── libs/ ← Reusable logic modules
│   ├── prompt_builder.py
│   ├── agent_core.py
│   └── logging_lib.py
├── test_inputs/ ← Shared input components (notes, memory, etc.)
├── results/ ← Test outputs, logs, and analysis results
├── scripts/ ← Main runners and orchestrators
│   ├── run_tests.py
│   ├── evaluate_outputs.py
│   └── main.py ← Optional CLI entrypoint
├── tests/ ← Unit tests for libs/
└── configs/ ← Optional: Promptfoo, LangSmith configs, env vars
```

A részletes tesztelési elveket és workflow-t lásd: `docs/TESTING_MASTER_GUIDE.md`

---

## Core Workflow / Fő workflow

1. 🛠 **Define Agent Behavior**
   - Create or choose an agent folder in `agents/`
   - Add versioned prompts in `prompts/`
   - Add test cases in `test_cases/`

2. 🧱 **Build Prompt**
   - Use `PromptBuilder` to load and assemble prompt from YAML

3. 🧠 **Execute Agent**
   - Use `AgentCore` to run agent logic using the selected prompt

4. 📤 **Input & Output**
   - Feed test input (note, memory, etc.)
   - Receive and log output using `Logger`

5. 🔬 **Evaluate Behavior**
   - Optionally define expected patterns or run diffing and scoring

---

## Tesztelési architektúra és workflow (magyar részletes leírás)

A promptfejlesztés és -tesztelés folyamata a következő lépésekből áll:

1. **Promptverziók kezelése:**  
   Minden ügynök promptja külön YAML fájlban, verziózva található a `prompts/` mappában.

2. **Teszt inputok:**  
   Valósághű, változatos input YAML-ok a `test_inputs/` mappában (pl. notes, user memory, clarification history).

3. **Automatizált tesztfuttatás:**  
   A `run_prompt_tests.py` script minden promptverziót minden inputtal lefuttat, és naplózza az eredményeket.  
   - A script a PromptBuilder-t használja a prompt generálásához.
   - Az LLM-et (pl. OpenAI GPT-4) hívja meg a generált prompttal.
   - Az outputokat logolja, opcionálisan összeveti elvárt eredményekkel.

4. **Promptfoo és LangSmith integráció:**  
   Ezek az eszközök lehetővé teszik a promptok deklaratív, automatizált tesztelését, valamint a webes playground használatát gyors iterációhoz.

5. **Eredmények és regresszió:**  
   Minden promptverzióra és inputra visszamenőleg is futnak a tesztek, így azonnal látható, ha egy új promptverzió visszalépést okoz (regresszió).

---

## Reusable Core Libraries

| Module           | Description                                      |
|------------------|--------------------------------------------------|
| `prompt_builder` | Builds prompt strings from versioned YAML files |
| `agent_core`     | Minimal agent interface for executing prompts   |
| `logging_lib`    | Logs test results, diffs, and evaluations       |

---

## Example Test Case Structure

```yaml
agent: clarifier
prompt_version: v1
input:
  note: "User asked about magnesium absorption"
  memory: "Known deficiencies"
expected:
  output_contains: ["magnesium", "absorption", "gut"]
```

---

## How To Run / Futtatás

1. Telepítsd a függőségeket:
   ```sh
   pip install -r requirements.txt  # vagy pipenv install -r prompt_testing/requirements.txt
   ```
2. Futtasd a teszteket:
   ```sh
   python scripts/run_tests.py
   # vagy
   pipenv run promptfoo test promptfoo.yaml --provider openai:gpt-4
   ```
3. Webes playground indítása:
   ```sh
   pipenv run promptfoo web
   ```
4. LangSmith használata:
   - Regisztrálj a https://smith.langchain.com/ oldalon, és szerezd meg az API kulcsodat.
   - Állítsd be a környezeti változókat (pl. `.env`):
     ```
     LANGCHAIN_API_KEY=your-key-here
     LANGCHAIN_TRACING_V2=true
     ```
   - Futtasd a scriptet:
     ```sh
     pipenv run python langsmith_test.py
     ```

---

## Roadmap

- Automated similarity and structure-based output evaluation
- Prompt diff visualizations
- LangSmith or Promptfoo integration (optional)
- CI-ready architecture for regression automation

---

## Philosophy / Filozófia

Don't build monolith prompts. Build evolving, testable, intelligent components — just like great code.

Ne monolit promptokat építs! Fejlessz evolúciós, tesztelhető, intelligens komponenseket – akárcsak a jó kódot.

---

## Referencia
A részletes tesztelési elveket és workflow-t lásd: `docs/TESTING_MASTER_GUIDE.md` 