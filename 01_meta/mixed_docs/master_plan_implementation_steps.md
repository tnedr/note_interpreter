# Multi-Agent System Master Plan – Implementation Steps

## Verzió: 1.0

---

## 0. Dokumentum célja

Ez a dokumentum lépésről lépésre tartalmazza a master plan implementációs tervét, különös hangsúllyal a **context (memória, előzmények, pipeline state)** kezelésére, hogy AI code agentek számára is egyértelmű legyen a kontextuskezelés minden pipeline és agent lépésnél.

---

## Kiemelt következő lépések (AgentCore-architektúra)

- [ ] Töröld a base_agent.py-t, mert a modern architektúrában az AgentCore és a context-driven design váltja ki.
- [ ] Minden új agent (ClarifyAndScoreAgent, NoteFinalizerAgent, stb.) legyen vékony wrapper, amely az AgentCore-t példányosítja a megfelelő toolokkal, prompttal, contexttel.
- [ ] Az agentek run metódusa csak a context forwardolásáért, validációért, output mappingért feleljen.
- [ ] A pipeline/orchestrator minden agentet explicit példányosítson, és a contextet mindig átadja.
- [ ] Az agentek outputját, state-jét, context változásait logolja, auditálja.
- [ ] Frissítsd a projekt journal-t, hogy a BaseAgent törölve lett, és minden agent az AgentCore köré szerveződik.

---

## 2. Agentek és pipeline explicit szétválasztása

- [ ] **Agent interface-ek definiálása**: Hozd létre az absztrakt agent interface-t (pl. `BaseAgent`), amely minden agent közös metódusait tartalmazza.
- [ ] **ClarifyAndScoreAgent refaktor**: A jelenlegi LLM agent logikát bontsd ki külön agent osztályba.
- [ ] **NoteFinalizerAgent implementálása**: Hozd létre a véglegesítő agentet, amely enrichmentet, memóriabővítést végez.
- [ ] **HumanAnswerCollector (UI/CLI)**: Külön modulba szervezd a user kérdés-válasz interakciót.
- [ ] **AgentOrchestrator (pipeline controller)**: Implementáld az orchestrator modult, amely a pipeline lépéseit, iterációs logikát, agent hívásokat vezérli.

### Context handling
- **Agentek közötti context**: Minden agent csak explicit contextet kapjon (notes, memory, clarification_history, pipeline state), implicit globális változók nélkül.
- **Orchestrator**: Minden pipeline lépésnél logolja a context változásokat (pl. memory update, clarification_history bővülés, state váltás).
- **Audit trail**: A clarification_history, memory, és pipeline state minden iterációban mentésre/logolásra kerüljön.

---

## 3. Adatstruktúra és séma egységesítés

- [ ] **Note objektum és output schema**: Egységesítsd a NoteInput/NoteOutput/DataEntry mezőit a master plan szerinti sorrendben és névvel.
- [ ] **Clarification history kezelés**: Biztosítsd, hogy a clarification_history minden iterációban bővül, és audit trailként működik.

### Context handling
- **Schema validáció**: Minden context-váltásnál validáld a note objektumokat a YAML/Python sémák szerint.
- **Clarification_history**: Minden Q&A batch logolva legyen, és minden agent csak a contextben átadott history-t használja.

---

## 4. Prompt architektúra és verziózás

- [ ] **Prompt könyvtár struktúra**: Hozd létre a `prompts/clarify_agent/`, `prompts/finalizer_agent/` könyvtárakat, verziózott prompt_config.yaml fájlokkal.
- [ ] **Prompt szekciók és contractok**: Ellenőrizd, hogy minden prompt tartalmazza a master plan szerinti szekciókat.
- [ ] **Prompt versioning**: Vezesd be a prompt version mezőt, és dokumentáld a prompt regression tesztelés workflowját.

### Context handling
- **Prompt context injection**: Minden agent promptba explicit context injection (notes, memory, clarification_history, pipeline state, prompt version).
- **Prompt changelog**: Prompt változásnál a context snapshot is mentésre kerüljön regression célból.

---

## 5. Tesztelés, validáció, regression harness

- [ ] **Unit és integrációs tesztek**: Írj unit teszteket minden agentre.
- [ ] **Prompt regression harness**: Hozd létre a regression_tests/ könyvtárat, input/output snapshotokkal.
- [ ] **End-to-end pipeline teszt**: Írj teljes pipeline tesztet, covering all main flows.

### Context handling
- **Regression snapshot**: Minden regression teszthez a teljes context (input, memory, config, prompt version) legyen elmentve.
- **Test context isolation**: Minden teszt izolált contexttel fusson, ne legyen side effect.

---

## 6. Fallback, hiba- és warning kezelés

- [ ] **Fallback logika**: Implementáld, hogy ha egy note három kör után is alacsony score-t kap, archive/manual review-ra kerüljön.
- [ ] **Error handling**: Minden agent valid JSON-t adjon vissza, plain text esetén log error, skip.

### Context handling
- **Error context**: Minden hiba/warning context (input, agent state, memory, Q&A) logolva legyen, hogy visszakereshető legyen a pipeline állapota.
- **Manual review**: Manuális review esetén a teljes context snapshotot mentsd el.

---

## 7. Bővíthetőség, modularitás, konfiguráció

- [ ] **YAML-alapú pipeline config**: A pipeline sorrend, agentek, thresholdok, max_rounds, prompt szekciók legyenek YAML-ből konfigurálhatók.
- [ ] **Új agentek hozzáadása**: Készíts sablont új agentekhez.

### Context handling
- **Config context**: Minden pipeline futásnál a használt config, paraméterek, prompt verziók legyenek logolva.
- **Agent extension**: Új agent hozzáadásakor a context contractot is dokumentáld.

---

## 8. Dokumentáció és journal update

- [ ] **Master plan changelog**: Minden jelentős lépésnél frissítsd a master plan changelogját és a projekt journal-t.
- [ ] **Fejlesztési státusz, TODO lista**: Tartsd naprakészen a TODO listát a master plan végén.

### Context handling
- **Decision context**: Minden döntésnél, journal entrynél a releváns context (input, memory, config, prompt version) legyen rögzítve.

---

## 9. UI/UX (opcionális)

- [ ] **Streamlit/Gradio prototípus**: Készíts egy egyszerű UI-t a HumanAnswerCollectorhoz.

### Context handling
- **User context**: A UI minden user interakcióhoz mutassa az aktuális contextet (jegyzet, memory, Q&A history, pipeline state).

---

## 10. Deployment, monitoring (haladó)

- [ ] **Monitoring, debug dashboard**: Opcionálisan implementálj egy dashboardot a pipeline állapotának, warningoknak, hibáknak a követésére.

### Context handling
- **Monitoring context**: A dashboard minden pipeline futásnál mutassa a teljes contextet (input, memory, agent state, Q&A, config, prompt version).

---

## 11. Összefoglaló checklist AI code agenteknek

- [ ] Minden agent csak explicit contextet használjon, implicit state nélkül.
- [ ] Minden pipeline lépésnél a context változásokat logolni/auditálni kell.
- [ ] Minden promptba, tesztbe, regression snapshotba a teljes contextet injektálni kell.
- [ ] Minden hiba, warning, manual review esetén a context snapshotot el kell menteni.
- [ ] Új agent, prompt, config, vagy pipeline változtatásnál a context contractot dokumentálni kell.

---

## 12. Tesztelési stratégia és új tesztek (útmutató)

> **Megjegyzés:** A `resources/single_agent` foldert egyelőre ne archiváld, maradjon meg referenciának és összehasonlítási alapnak az új architektúra bevezetése alatt. A tesztek implementálása az új agentek, orchestrator és context handling után következzen, amikor már stabil az új pipeline.

### Új tesztek, amikre szükség lesz:

- [ ] **Agent unit tesztek**
  - ClarifyAndScoreAgent: input/output contract, clarification loop, context injection
  - NoteFinalizerAgent: enrichment, memory update, output schema
  - HumanAnswerCollector: user Q&A kezelés, context mapping
- [ ] **Orchestrator tesztek**
  - Iterációs logika, pipeline state váltás, context forwarding
- [ ] **Context handling tesztek**
  - Minden context változás (memory, clarification_history, state) helyes logolása, audit trail
- [ ] **Prompt regression tesztek**
  - Prompt változás után snapshot összehasonlítás (regression_tests/)
- [ ] **End-to-end pipeline tesztek**
  - Teljes pipeline futás különböző inputokkal (clear, ambiguous, unresolved notes)
- [ ] **Fallback és warning tesztek**
  - Hibás output, max_rounds, manual review, UNDEFINED mezők kezelése

#### Példák
- `test_clarify_and_score_agent_contract()`
- `test_note_finalizer_enrichment()`
- `test_orchestrator_iteration_and_context()`
- `test_context_audit_trail()`
- `test_prompt_regression_case_001()`
- `test_pipeline_fallback_behavior()`

> **Javaslat:** A régi single_agent teszteket csak akkor töröld vagy migráld, ha az új architektúra minden fő funkciója már le van fedve új tesztekkel, és a pipeline stabilan működik.

--- 