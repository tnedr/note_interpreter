# 04\_IMPLEMENTATION\_PLAN.md – Prompt Lab rendszer fejlesztés

## 🎯 Cél

Ez a dokumentum a Prompt Lab rendszer implementációs tervét tartalmazza, fázisokra és MVP milestone-okra bontva. A cél egy olyan környezet létrehozása, amely képes stepwise módon promtokat fejleszteni, verziózni és tesztelni.

---

## 🧱 Fejlesztési fázisok és MVP milestone-ok

### 🟢 Phase 0 – Projektstruktúra létrehozása

#### Teendők

* Projektkönyvtár és mappaszerkezet létrehozása:

  ```
  prompt_lab/
    agents/
    libs/
    prompt_plans/
    test_cases/
    logs/
    results/
    scripts/
    tests/
  ```
* Alapfájlok:

  * `README.md`, `.gitignore`, `requirements.txt`

#### MVP cél

✅ A projekt elindítható, a könyvtárszerkezet logikus és bővíthető

---

### 🟢 Phase 1 – Teszt pipeline MVP

#### Teendők

* `PromptBuilder` modul:

  * Fájl: `libs/prompt_builder.py`
  * Betölti a YAML promptot, behelyettesíti a mezőket
* `TestRunner`:

  * Egyszerű script: `scripts/run_tests.py`
  * Betölti az agent promptot és teszt inputot
  * Lefuttatja és ellenőrzi az outputot

#### Példafájlok

* `agents/grocery_clarifier/prompts/v1.yaml`

  ```yaml
  system: |
    You are a shopping assistant.
    Evaluate this input and return a clarity score (0–100).
    Input: {note}
  ```
* `test_cases/test1.yaml`

  ```yaml
  input:
    note: "tej"
  expected:
    clarity_score: 60
  ```

#### MVP cél

✅ Egy input–output YAML pár lefuttatható, eredmény ellenőrizve

---

### 🟠 Phase 2 – StepwisePlanManager MVP

#### Teendők

* `libs/stepwise_manager.py`

  * Beolvassa a `prompt_plans/*.md` fájlokat
  * Értelmezi a step definíciókat (step neve, prompt fájl, teszt fájl, elvárt mezők)
  * Naplózza az egyes próbálkozásokat (prompt attempt logok)

#### Prompt Attempt fájlszerkezet

```
agents/grocery_clarifier/step_01_scoring/
  prompts/
    v1.yaml
  logs/
    v1__log.md
  attempts_index.yaml
```

#### MVP cél

✅ Step plan alapján felismeri a step nevét, verziót, teszteseteket, logokat

---

### 🟣 Phase 3 – Grocery Clarifier MVP futtatása

#### Teendők

* Létrehozni: `prompt_plans/plan_grocery_note_clarifier.md`
* Prompt verziók:

  * `v1.yaml`: scoring
  * `v2.yaml`: interpretation
  * `v3.yaml`: clarification question (text)
  * `v4.yaml`: clarification\_tool\_call (structured)
* Minden stephez:

  * 1–2 teszteset YAML-ban
  * log fájl (.md) a prompt próbálkozásokról

#### Script

* `scripts/run_grocery_clarifier.py`:

  * Futtatja egymás után a step verziókat
  * Kiértékeli az eredményeket
  * Naplózza az outputokat a `results/` mappába

#### Dummy LLM támogatás (ha nincs API)

* `libs/mock_llm.py`

  * `generate_response(prompt: str) -> str` – előre definiált outputokat ad vissza

#### MVP cél

✅ Teljes stepwise prompt evolúció működik a Grocery Clarifier példával, tesztelhető módon

---

## 📦 Output

* Működő stepwise prompt lab
* Grocery Clarifier agent teljes példája
* Dokumentált prompt verziók, tesztek, naplók
* Egyszerű script alapú futtatás és naplózás

---

*Ez az implementációs terv a Prompt Lab rendszer MVP szintű működését célozza. Minden fázishoz világos minimum elvárások és konkrét fájlstruktúra tartozik. Átadható Coding AI-nak is feldolgozható formában.*
