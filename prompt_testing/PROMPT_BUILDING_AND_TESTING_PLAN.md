# Prompt Building & Testing Plan

Ez a terv lépésről lépésre végigvezet a prompt optimalizáció és tesztelés folyamatán, kifejezetten a note interpretation + clarification + scoring problémakörre, PromptBuilder és multi-agent workflow mellett.

---

## 1. Célok és kiinduló problémák
- Mit akarunk elérni? (pl. homályos jegyzetek értelmezése, pontozása, visszakérdezés)
- Fő kihívások: félreérthető input, hiányos válasz, hallucináció elkerülése

---

## 2. Iteratív prompt fejlesztési lépések

### 2.1. "Szabad" (plain text) baseline prompt
- Készíts egy egyszerű promptot, ami csak magyarázatot, pontszámot, visszakérdezést kér.
- Teszteld, hogy a modell érti-e a feladatot, visszakérdez-e, jól pontoz-e.

### 2.2. Strukturált output (JSON) prompt
- Ugyanaz, de mindig JSON-t kérj vissza (pl. note, score, clarification_questions, reasoning).
- Teszteld, hogy a JSON mindig helyes-e, minden mező szerepel-e.

### 2.3. Tool-alapú, agent prompt
- Vezesd be a tool-hívásokat (clarify_notes, finalize_notes, stb.), schema-t, constraints-et.
- Teszteld, hogy a modell csak tool-hívásokat használ-e, a schema-t betartja-e.

### 2.4. Finomhangolás, edge case-ek, regresszió
- Ritka, nehéz, vagy szándékosan félrevezető inputokkal tesztelj.
- Prompt finomítása: példák, reasoning style, constraints, fallback, stb.
- Minden új prompt verziót visszatesztelni a régi inputokon is (regresszió).

---

## 3. Prompt módosítási/építési elvek
- Kis lépésekben változtass (egy blokk, egy példa, egy constraint egyszerre)
- Minden változathoz legyen teszt input és elvárt viselkedés
- Logolj minden prompt+input+output kombinációt
- Minden fontos részhez adj példát (clarity_score, visszakérdezés, UNDEFINED, stb.)
- Használj explicit constraints-et
- Reasoning style-t mindig teszteld
- Meta behavior: mindig legyen fallback, ha a modell bizonytalan

---

## 4. Prompt variációk és tesztelés workflow
1. Minden prompt verzió külön YAML (PromptBuilder-kompatibilis)
2. A teszt script minden prompt verziót minden inputtal végigfuttat
3. A logban minden output visszakereshető, összehasonlítható
4. Ha egy prompt változtatás javít, megtartjuk, ha ront, visszavonjuk
5. A legjobb promptokat regressziós tesztként is elmentjük

---

## 5. Automatizálás és tooling
- PromptBuilder: minden prompt generálás egységesen innen
- run_prompt_tests.py: minden prompt variáció, minden input, minden output logolva
- Promptfoo/LangSmith: regressziós és minőségi tesztek, diff, összehasonlítás
- (Opcionális) Automatikus diff script: kiemeli, hogy melyik prompt variáció miben ad mást

---

## 6. Döntési fa: mikor mit módosíts?
- Ha a modell nem érti a feladatot → több/más példa, explicitabb célok
- Ha nem kérdez vissza → több clarification példa, reasoning style hangsúlyozása
- Ha nem strukturált az output → JSON schema, explicit constraints, példák
- Ha nem tool-hívásokat használ → tool schema, constraints, meta behavior
- Ha túl "hallucinál" → constraints, fallback, UNDEFINED policy

---

## 7. Példák prompt variációkra
- plain_v1.yaml: szabad, magyarázó prompt
- json_v1.yaml: strukturált JSON output
- tool_v1.yaml: tool-alapú, szigorú agent prompt
- v1, v2, v3...: finomhangolt, éles promptok

---

*Ezt a tervet szabadon módosíthatod, bővítheted a saját workflow-dhoz!* 