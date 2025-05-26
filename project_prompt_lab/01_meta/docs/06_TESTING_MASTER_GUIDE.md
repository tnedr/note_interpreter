# Prompt & Agent Testing Master Guide

Ez a dokumentum összefoglalja a prompt- és agent-tesztelés általános elveit, workflow-ját és best practice-eit. Célja, hogy minden új prompt vagy agent fejlesztésekor egységes, automatizálható, visszakereshető és bővíthető tesztelési környezetet biztosítson.

---

## 1. Tesztelési cél

Gyors, iteratív promptfejlesztés és -tesztelés támogatása bármely LLM-alapú ügynök (agent) számára. A cél, hogy a promptok minél gyorsabban kipróbálhatók, összehasonlíthatók és továbbfejleszthetők legyenek, valósághű inputokkal és automatizált regressziós tesztekkel.

---

## 2. Input/Output sémák

### Input séma (példa YAML):
```yaml
notes_batch:
  - id: note_001
    raw_text: "Email John"
    clarification_history: []
user_memory:
  - "User prefers concise notes."
clarity_score_threshold: 70
```

### Output séma (példa YAML):
```yaml
notes_batch:
  - id: note_001
    interpreted_text: "Send an email to John."
    clarity_score: 90
    ask_user_question: null
```

#### Kötelező elvek:
- Minden mezőnek mindig szerepelnie kell (ha nincs érték: null vagy UNDEFINED).
- Az input/output legyen gépileg feldolgozható (YAML vagy JSON).
- A sémát minden promptverzió és teszt input kövesse.

---

## 3. Edge case-ek, fallbackok
- Ha a modell nem tud értelmezni, `interpreted_text: UNDEFINED`, `ask_user_question` kötelező.
- Ha a note túl homályos, `clarity_score` legyen alacsony.
- Minden mező explicit módon szerepeljen, még ha üres/null is.

---

## 4. Promptverziózás és changelog
- Minden jelentős promptváltoztatás új YAML fájlban, verzióval ellátva (pl. `clarify_v2.yaml`).
- Rövid changelog minden verzióhoz (pl. `PROMPT_CHANGELOG.md`).

---

## 5. Tesztelési workflow
- Minden promptverziót minden inputtal le kell futtatni.
- Az outputokat automatikusan össze kell vetni az elvárt outputtal (diff).
- Minden regressziót azonnal jelezni kell.
- Promptfoo/LangSmith csak technikai eszköz, a workflow-tól függetlenül cserélhető.

---

## 6. Best practice-ek
- Teszt inputok legyenek változatosak (edge case, tipikus, hibás input).
- Dokumentáld, ha egy promptverzióban fallback logika változik.
- Minden új agent/prompt fejlesztésekor ezt a dokumentumot vedd alapul.

---

## 7. Példák

### Input példa:
```yaml
notes_batch:
  - id: note_002
    raw_text: "???"
    clarification_history: []
user_memory:
  - "User often references LangChain tools."
clarity_score_threshold: 70
```

### Elvárt output példa:
```yaml
notes_batch:
  - id: note_002
    interpreted_text: UNDEFINED
    clarity_score: 20
    ask_user_question: "Mit jelent a '???' ebben a kontextusban?"
```

---

Ezt a dokumentumot minden prompt/agent fejlesztésnél és tesztelésnél kötelező referenciaként használni! 