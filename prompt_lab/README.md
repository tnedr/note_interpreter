# 🧪 Prompt Regression & Development Lab

## Overview / Áttekintés

This project is a **modular, testable, and iterative framework** for developing and validating prompts used by LLM-based agents. It is designed as a *subproject* within a larger AI agent development ecosystem, and its goal is to ensure that prompts evolve in a controlled, regression-tested manner.

**This lab is designed for _stepwise, multi-turn prompt development_: you can build, test, and version agents that interact with the user in multiple rounds, asking clarifying questions if needed, not just static one-shot prompts.**

**Ez a labor kifejezetten _lépésenkénti, többkörös promptfejlesztésre_ készült: olyan agenteket lehet vele építeni és tesztelni, amelyek több lépésben, pontosító kérdésekkel, interaktívan működnek – nem csak egyszerű, statikus promptokat kezel.**

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
- 🧩 **Stepwise, multi-turn agent logic**: Support for agents that clarify, iterate, and refine their output through multiple prompt rounds.
- **Lépésenkénti, többkörös agent logika**: Olyan agentek támogatása, amelyek pontosítanak, visszakérdeznek, és több lépésben adják meg a végső választ.

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

1. 🛠 **Define stepwise agent behavior** – not just static prompts, but multi-turn, clarification-capable agents.
2. 🧱 **Build Prompt** – Use `PromptBuilder` to load and assemble prompt from YAML
3. 🧠 **Execute Agent** – Use `AgentCore` to run agent logic using the selected prompt
4. 📤 **Input & Output** – Feed test input (note, memory, etc.), including multi-step clarification scenarios
5. 🔬 **Evaluate Behavior** – Optionally define expected patterns or run diffing and scoring

**A workflow támogatja a több lépéses, pontosító kérdéseket is tartalmazó agent pipeline-ok fejlesztését és tesztelését.**

---

## Tesztelési architektúra és workflow (magyar részletes leírás)

A promptfejlesztés és -tesztelés folyamata a következő lépésekből áll:

1. **Promptverziók kezelése:**  
   Minden ügynök promptja külön YAML fájlban, verziózva található a `prompts/` mappában.
2. **Teszt inputok:**  
   Valósághű, változatos input YAML-ok a `test_inputs/` mappában (pl. notes, user memory, clarification history, több lépéses példák).
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
  # clarification_history: ["Does the user have gut issues?"]
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
- **Stepwise, multi-turn agent test harness and visualization**

---

## Philosophy / Filozófia

Don't build monolith prompts. Build evolving, testable, **stepwise**, intelligent components — just like great code.

Ne monolit promptokat építs! Fejlessz evolúciós, tesztelhető, **lépésenként fejlődő**, intelligens komponenseket – akárcsak a jó kódot.

---

## Referencia
A részletes tesztelési elveket és workflow-t lásd: `docs/TESTING_MASTER_GUIDE.md`

## Meta Input/Output – The Prompt Lab as a System / Meta bemenet és kimenet

**Meta Input (what you give to the Prompt Lab):**
- **Agent definition:**  
  What is the agent's goal?  
  What are its expected inputs/outputs?  
  What is the stepwise prompt pipeline (how many steps, what happens in each)?
- **Prompt versions:**  
  YAML files describing each prompt step.
- **Test cases:**  
  Input scenarios (possibly multi-step), expected outputs, clarification flows.
- **Evaluation criteria:**  
  What counts as a "good" output? (e.g., must contain certain info, must ask clarification if ambiguous, etc.)

**Meta Output (what the Prompt Lab produces):**
- **Test results:**  
  For each agent version and test case, what was the output? Did it match expectations?
- **Logs and diffs:**  
  Detailed logs, output differences between prompt versions.
- **Regression reports:**  
  Did a new prompt version break anything?
- **Prompt evolution history:**  
  How did the agent's stepwise logic change over time?

---

**Meta bemenet (amit a Prompt Lab kap):**
- **Agens definíció:**  
  Mi az agent célja?  
  Mik az elvárt inputjai/outputjai?  
  Mi a stepwise prompt pipeline (hány lépés, mi történik egyes lépésekben)?
- **Prompt verziók:**  
  YAML fájlok, amelyek minden prompt lépést leírnak.
- **Tesztesetek:**  
  Input szcenáriók (akár több lépésben), elvárt outputok, clarification flow-k.
- **Értékelési kritériumok:**  
  Mitől "jó" egy output? (pl. tartalmaznia kell bizonyos infót, kérdezzen, ha nem egyértelmű, stb.)

**Meta kimenet (amit a Prompt Lab előállít):**
- **Teszteredmények:**  
  Minden agent verzióra és tesztesetre, mi lett az output? Megfelelt-e az elvárásnak?
- **Logok és diffek:**  
  Részletes naplók, output különbségek prompt verziók között.
- **Regressziós riportok:**  
  Történt-e visszalépés egy új prompt verzióval?
- **Prompt pipeline evolúció:**  
  Hogyan változott az agent stepwise logikája az idő során?

---

**Példa:**

- Agent célja: "A felhasználó jegyzetét értelmezi, ha kell, pontosít."
- Stepwise pipeline:  
  1. Lépés: note + memory → ha nem egyértelmű, clarification kérdés  
  2. Lépés: note + memory + clarification → végső output
- Teszteset:  
  "Buy milk" + "User often forgets groceries" → "Do you need lactose-free milk?" → "Yes" → "User wants lactose-free milk."
- Elvárt viselkedés: mindig kérdezzen, ha nem egyértelmű.
- Kimenet: teszteredmények, logok, diffek, regressziók, prompt pipeline evolúció.

--- 