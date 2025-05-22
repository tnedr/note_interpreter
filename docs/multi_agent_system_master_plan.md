# Multi-Agent Jegyzetértelmező – Master System Plan

## Verzió: 1.2.1
- 2025-05-22: Validator Agent koncepció bevezetve
- 2025-05-21: Adatstruktúrák optimalizált sorrendje hozzáadva
- 2025-05-20: Clarify loop és iteration contract pontosítása

## 0. A dokumentum célja

Ez a dokumentum a Multi-Agent Jegyzetértelmező rendszer specifikációját tartalmazza. Fő célja, hogy:

- vezérfonalként szolgáljon az implementációhoz (promptok, agentek, adatstruktúrák),
- biztosítsa a pipeline egységes működését és iterálhatóságát,
- meghatározza a modularitás, bővíthetőség és tesztelhetőség alapelveit.

Ez a dokumentum nem helyettesíti a futó kódot, hanem azt egészíti ki koncepcióval, specifikációval és döntési dokumentációval.

## 1. Áttekintés és cél
A rendszer célja, hogy a felhasználó jegyzeteit több, egymásra épülő, specializált AI agent dolgozza fel, mindegyik egy-egy jól körülhatárolt feladatot lát el. A pipeline addig iterál, amíg minden jegyzet elég érthető, majd véglegesíti és bővíti a memóriát. A terv az alternatív (legfrissebb) architektúrát követi, de beépíti a korábbi tervek bővíthetőségi, prompt, tesztelési és workflow tapasztalatait is.

---

## 2. Fő agentek és szerepek (összevont táblázat)
| Agent Name              | Role                                                                 | Input                                             | Output                                 | Notes                                      |
|------------------------|----------------------------------------------------------------------|---------------------------------------------------|----------------------------------------|--------------------------------------------|
| ClarifyAndScoreAgent    | Clarifies notes using memory & Q&A; assigns scores, asks questions   | Batch of DataEntryInput[] (with memory & Q&A)     | Batch of DataEntry[]                   | Central agent, stateless, idempotent       |
| HumanAnswerCollector   | Waits for user answers; attaches to correct note                     | new_questions per id                             | Appends to clarification_history[]      | UI/interactive layer                       |
| NoteFinalizerAgent*    | Polishes clarified notes (if clarity_score ≥ threshold)              | Notes with clarity_score ≥ threshold             | Final clarified_text                    | Optional if ClarifyAndScoreAgent covers all|
| AgentOrchestrator      | Controls iteration loop; stops when all notes are above threshold    | Entire batch state                               | Updated batch, continues or halts loop  | Workflow layer (Make.com, LangChain, etc.) |
| MemoryEmbedder*        | Embeds resolved notes into long-term memory                          | Clarified notes with high score                  | Updates memory                          | Enables context-based future clarification |

*Opcionális agentek

---

## 3. Pipeline logika és workflow
### 3.1 Folyamatábra (lépések)
1. **Input:** jegyzetek, user memory
2. **ClarifyAndScoreAgent:**
   - minden jegyzethez score-ok
   - csak a threshold alatt lévőkre kérdez vissza
   - user válaszokat beépíti, clarification_qas-t bővíti
   - iterál, amíg minden jegyzet egyértelmű vagy max. kör elérve
3. **FinalizeAndMemoryAgent / NoteFinalizerAgent:**
   - véglegesíti a jegyzeteket, enrich-el, memóriát bővít, outputot ad
4. **MemoryEmbedder (opcionális):**
   - hosszú távú memóriába menti a legjobb jegyzeteket

### 3.2 Clarification Loop (részletesen)
- Minden körben csak a threshold alatt lévő jegyzetekre kérdez vissza.
- A user válaszait a megfelelő jegyzethez rendeli (id alapján).
- A clarification_history minden körben bővül (audit trail).
- A pipeline addig iterál, amíg minden jegyzet clarity_score ≥ threshold, vagy el nem éri a max_rounds-ot.

### 3.3 ClarifyAndScoreAgent működéslogikája (javasolt frissítés)
- Az agent mindig kizárólag a bemenetként kapott `clarification_history` alapján dolgozik, nem épít be új válaszokat.
- A `clarified_text` mezőt minden jegyzethez generálja, ha az adott `raw_text` + `long_term_memory` + `clarification_history` elegendő információt ad.
- A `clarity_score`-t minden jegyzetre kiszámolja (0–100).
- Ha a `clarity_score < threshold`, akkor a `new_questions` tömböt is visszaadja.
- Az agent stateless: minden iteráció új hívás, minden állapotváltozást a pipeline (orchestrator) és a felhasználói válaszok adnak meg.
- A pipeline gondoskodik róla, hogy a user válaszait a megfelelő id-jú jegyzethez illessze és a következő körre újra beadja.

### 3.4 pipeline_config.yaml példa
```yaml
clarify_score_threshold: 80
max_rounds: 3
agents:
  - name: ClarifyAndScoreAgent
    model: gpt-4o
  - name: HumanAnswerCollector
    mode: UI
  - name: NoteFinalizerAgent
    model: gpt-4-turbo
```

---

## 4. Adatstruktúra, input/output sémák
### 4.1 Jegyzet objektum (mezők optimális sorrendje)
- id
- raw_text
- clarification_history (Q&A-k, minden eddigi válasz)
- clarified_text (cache, minden körben frissül)
- clarity_score (aktuális iteráció eredménye)
- new_questions (aktuális iteráció eredménye)
- long_term_memory (opcionális)

Példa:
```yaml
- id: "note_3"
  raw_text: "meeting review"
  clarification_history:
    - question: "Which meeting?"
      answer: "Tuesday team meeting"
  clarified_text: ""
  clarity_score: 38
  new_questions:
    - "What needs to be reviewed?"
```

#### 🧠 Rationale for This Order
- **id:** Mindig első – stabil kulcs a pipeline minden lépésében.
- **raw_text:** Az eredeti input az alap, ezért követi az id-t.
- **clarification_history:** Logikusan ezt követi, hiszen ez adja a plusz megértést az értelmezés előtt.
- **clarified_text:** Az értelmezett eredmény, amely az előzőekből születik.
- **clarity_score:** Az output minőségét értékeli – természetes, hogy az értelmezés után következik.
- **new_questions:** Utolsóként, mert ez a következő iterációhoz szükséges akció.

Ez a struktúra tükrözi azt a kognitív sorrendet, ahogy egy ember vagy agent feldolgozza a jegyzetet.

### 4.2 Python class definíciók
```python
@dataclass
class NoteInput:
    id: str
    raw_text: str
    clarification_history: list[dict[str, str]]
    long_term_memory: list[str] = field(default_factory=list)

@dataclass
class NoteOutput:
    id: str
    clarified_text: str
    clarity_score: int
    new_questions: list[str]
```

Ezek a struktúrák könnyen átvihetők JSON schema-vá vagy OpenAPI definícióvá is.

---

## 5. Prompt szekciók (összevont, agent-specifikus)
### ClarifyAndScoreAgent
- **intro**: Az agent fő feladata a jegyzetek érthetőségének maximalizálása, scoring és tisztázó kérdések generálása.
- **goals**: Minden jegyzethez clarity/ambiguity score-t kell adni, és csak a threshold alatt lévőkre kell kérdést feltenni. Addig iterál, amíg minden jegyzet érthető.
- **output_schema_and_meanings**: A scoring output mezői (pl. clarity_score, ambiguity_score, clarified_text, clarification_history).
- **scoring_guidelines**: Mikor kell kérdezni, milyen thresholdok vannak, milyen score-ok alapján dönt.
- **clarification_protocol**: Hogyan generáljon kérdéseket, hogyan kezelje a user válaszait, hogyan építse be a jegyzetekbe.
- **parameter_explanations**: threshold, max_rounds, stb.
- **output_validation_rules**: Minden körben csak a threshold alatt lévőkre kérdezzen, minden Q&A batch-et logoljon.
- **tool_json_schema**: (ha LLM tool-alapú) – scoring, clarification tool paraméterek.
- **example_output**: Példa egy scoring+clarification iterációra (jegyzet, score, kérdés, válasz, frissített jegyzet).
- **iteration_contract**: Az agent mindig stateless, minden állapotot a pipeline kezel. A `clarification_history[]` az egyetlen módja a korábbi válaszok integrálásának.

### FinalizeAndMemoryAgent / NoteFinalizerAgent
- **intro**: Az agent fő feladata a végleges, struktúrált output elkészítése, enrichment, kategorizálás, memóriabővítés.
- **goals**: Minden jegyzethez végleges értelmezés, kategória, intent, enrichment, új memory pointok generálása.
- **output_schema_and_meanings**: A végső output mezői (pl. interpreted_text, entity_type, intent, new_memory_points).
- **memory_update**: Hogyan generáljon memory pointokat, mikor bővítse a memóriát.
- **output_validation_rules**: Minden jegyzethez legyen teljes értelmezés, minden kötelező mező szerepeljen.
- **tool_json_schema**: (ha LLM tool-alapú) – finalize tool paraméterek.
- **example_output**: Példa egy véglegesített jegyzetre, memóriabővítéssel.

### Általános szekciók (mindkét agentnél)
- **constraints**: Ne hallucináljon, ne válaszoljon plain textben, csak a saját feladatára fókuszáljon.
- **reasoning_style**: Lépésről lépésre gondolkodjon, explicit legyen a logika.
- **meta_behavior**: Ha nem biztos, kérdezzen vissza, vagy adjon UNDEFINED-et.

---

## 6. Tesztelhetőség és bővíthetőség (kiegészítés)
- Minden agent külön tesztelhető (mock input/output, unit test).
- A pipeline egészében is tesztelhető, különböző inputokkal, edge case-ekkel, end-to-end.
- Új agent könnyen hozzáadható (pl. ReviewAgent, FeedbackAgent).
- LLM modellek cserélhetők: minden agent akár más LLM-et is használhat.
- Konfiguráció YAML-ből: pipeline sorrend, thresholdok, max. körök, prompt szekciók.
- Debug/monitoring dashboard (pl. Streamlit, Gradio) opcionális.
- Új edge case: ha `clarified_text = ""` de `new_questions = []`, az ellentmondás lehet, erre figyelmeztető tesztet kell írni.
- Új prompt regression teszt: ha a `clarified_text` nincs összhangban a Q&A-vel, az hibát jelezzen.

---

## 7. Alternatívák és döntési pontok (kiegészítés)
### 7.1 Agent setup
- **Minimális MVP:** ClarifyAndScoreAgent + HumanAnswerCollector + Orchestrator
- **Bővített:** NoteFinalizerAgent, MemoryEmbedder, SemanticSorterAgent
- **Döntés:** MVP-vel indulj, de a pipeline legyen bővíthető!

### 7.2 Iterációs logika
- **Alap:** Minden körben csak a threshold alatt lévőkre kérdez vissza
- **Alternatíva:** Egyedi stratégiák (pl. prioritás, csoportosítás)
- **Döntés:** Kezdd a standard logikával, később bővíthető

### 7.3 Prompt struktúra
- **Egy közös prompt_config.yaml** vagy **agentenként külön**
- **Döntés:** Agentenként külön prompt_config.yaml ajánlott a modularitás miatt

### 7.4 Tesztelési stratégia
- **Unit + integrációs + end-to-end**
- **Prompt regression, edge case, fallback tesztek**
- **Döntés:** Minden szinten legyen teszt, prompt változásokat is tesztelni kell

### 7.5 Bővíthetőség
- **LLM, pipeline sorrend, paraméterek, agentek** mind legyenek könnyen cserélhetők, konfigurálhatók
- **Döntés:** YAML-alapú konfiguráció, jól dokumentált agent interface

#### ⚠️ Figyelembe veendő pontok, kérdések
1. Mi történik, ha `clarified_text = ""` de `clarity_score ≥ threshold`? Ezt érdemes hibaként vagy warningként kezelni, mert logikai ellentmondás.
2. Egyértelmű-e, hogy a `clarified_text` nem frissül, ha nincs új válasz? Az agent lehetne úgy is paraméterezve, hogy ha nincs új `clarification_history`, akkor megtartja a régi `clarified_text`-et és nem dolgozza újra – ez gyorsíthatja az iterációkat.

---

## 8. Referenciák, források
- AI_multi_agent_alt_plan.md (legfrissebb architektúra)
- AI_multi_agent_build_plan.md (workflow, tesztelés, prompt tuning)
- multi_agent_system_design.md (prompt szekciók, bővíthetőség)

## 9. Fogalomjegyzék

- **clarified_text** – A lehető legjobb, véglegesített, egyértelműen értelmezett változata a jegyzetnek.
- **clarity_score** – Egy 0–100 skálán kifejezett metrika, ami az értelmezhetőség fokát méri.
- **new_questions** – Csak akkor van, ha a clarity_score nem elég magas; ezek tisztázó kérdések a user felé.
- **clarification_history** – Minden Q&A logikai előzménye, ami segít újra lefuttatni az értelmezést.
- **threshold** – Az a minimális clarity_score, ami felett a jegyzet értelmezettnek minősül.

---

## 10. Tesztelési és validálási sablonok

### 10.1 Unit test struktúra

- `test_clarify_score_below_threshold_triggers_questions()`
- `test_idempotent_behavior_with_same_input()`
- `test_empty_clarified_text_requires_question()`

### 10.2 Prompt regression példa

Input note:
```yaml
raw_text: "talk to boss"
clarification_history: []
long_term_memory: []
```
Elvárt kérdés: "About what topic do you want to talk to your boss?"

Ha nem jelenik meg, prompt regression hiba.

---

## 11. Prompt verziózás és visszamenőleges kompatibilitás

- Minden prompt sablonnak legyen `version` mezője (pl. `prompt_config_v1.2.yaml`).
- Prompt változtatás előtt `prompt_regression_test()` kötelező.
- Prompt-változások hatását külön `changelog` szakasz dokumentálja.

---

## 12. Prompt könyvtár és struktúra

📘 Koncepció: Minden agenthez külön prompt könyvtár, verziózott fájlokkal.

```plaintext
prompts/
  clarify_agent/
    prompt_v1.0.yaml
    prompt_v1.1.yaml
  finalizer_agent/
    prompt_v1.0.yaml
```

- Minden prompt fájl tartalmazza: intro, constraints, output schema, scoring_guidelines, clarification_protocol, stb.
- Prompt version minden fájlban kötelező.

---

## 13. Várható hibák és fallback stratégiák

- 🛑 Ha egy agent valid JSON helyett plain textet ad vissza → log error, skip
- ❌ Ha `clarified_text == "" && new_questions == []` → warning és review agent trigger
- 🔁 Ha egy note három kör után is alacsony score-t kap → archive vagy manual review

---

## 14. Fejlesztési státusz és TODO

- [x] ClarifyAndScoreAgent prompt v1.0 kész
- [ ] Prompt regression test framework kialakítása
- [ ] Streamlit UI prototípus
- [ ] HumanAnswerCollector LangChain integráció

--- 