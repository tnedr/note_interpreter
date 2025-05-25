# Stepwise Prompt Implementation Plan

Ez a dokumentum lépésről lépésre bemutatja, hogyan érdemes a Note Interpreter projektben (vagy bármely LLM-alapú agentnél) a promptokat fejleszteni, bővíteni és tesztelni. A terv minden lépéshez konkrét célokat, szükséges prompt szekciókat, output mezőket és tesztelési fókuszt rendel.

---

## 1. Áttekintés

A promptfejlesztés iteratív, lépésenként bővülő workflow-ban történik. Minden lépés egy újabb képességet, szekciót vagy validációs logikát vezet be, miközben a korábbi lépések regressziós tesztjei is folyamatosan futnak.

---

## 2. Stepwise fejlesztési lépések

### 1. MVP – Scoring only
- **Cél:** Csak clarity_score-t ad vissza minden jegyzetre.
- **Prompt szekciók:** intro, goals, scoring_guidelines
- **Output:** clarity_score
- **Teszt:** Minden jegyzethez 0-100 közötti score.

### 2. + Interpretation
- **Cél:** Score + értelmezett szöveg (interpreted_text/clarified_text).
- **Prompt szekciók:** +output_schema
- **Output:** clarity_score, interpreted_text
- **Teszt:** Minden jegyzethez értelmezés.

### 3. + Clarification
- **Cél:** Homályos jegyzetekhez kérdés generálása.
- **Prompt szekciók:** +clarification_protocol, tool_json_schema, example_output
- **Output:** ask_user_question
- **Teszt:** Ambiguity esetén kérdés generálás.

### 4. + User Memory
- **Cél:** user_memory használata a kontextusban.
- **Prompt szekciók:** +input_context, parameter_explanations
- **Output:** Kontextus-függő értelmezés.
- **Teszt:** Memory relevancia.

### 5. + Clarification History
- **Cél:** clarification_history használata.
- **Prompt szekciók:** input_context, clarification_protocol
- **Output:** Multi-turn logika.
- **Teszt:** History-függő output.

### 6. + Structured Output
- **Cél:** Szigorúan séma-kompatibilis, gépileg feldolgozható output.
- **Prompt szekciók:** +output_validation_rules, constraints, meta_behavior
- **Output:** Minden mező, valid típusok.
- **Teszt:** Mindig érvényes, teljes output.

### 7. + Edge/Fallbacks
- **Cél:** Edge case-ek, fallback logika, UNDEFINED/null kezelés.
- **Prompt szekciók:** meta_behavior, constraints
- **Output:** UNDEFINED, hibakezelés.
- **Teszt:** Robusztusság, regresszió.

---

## 3. Stepwise összefoglaló táblázat

| Lépés | Cél | Új prompt szekciók | Új output mezők | Teszt fókusz |
|-------|-----|--------------------|----------------|-------------|
| 1     | Scoring only | intro, goals, scoring_guidelines | clarity_score | Score minden jegyzetre |
| 2     | + Interpretation | +output_schema | interpreted_text | Score + értelmezés |
| 3     | + Clarification | +clarification_protocol, tool_json_schema | ask_user_question | Kérdés generálás |
| 4     | + User Memory | +input_context, parameter_explanations | (memory) | Kontextus |
| 5     | + Clarification History | (protocol/history) | (history) | Multi-turn |
| 6     | + Structured Output | +output_validation_rules, constraints, meta_behavior | minden mező | Szigorú séma |
| 7     | + Edge/Fallbacks | (mint fent) | UNDEFINED, error | Robusztusság |

---

## 4. Példa prompt YAML verziók

- `scoring_only_v1.yaml`: csak scoring szekciók
- `clarify_v1.yaml`: scoring + interpretation + clarification
- `clarify_with_memory_v1.yaml`: scoring + interpretation + clarification + memory

---

## 5. Tesztesetek

Minden lépéshez tartozik egy vagy több input/output teszteset (`test_cases/`), amelyek regressziósan is futnak minden új promptverzióra.

---

## 6. Ajánlott workflow

1. Hozz létre új prompt YAML-t az aktuális lépéshez az agents/<agent>/prompts/ mappában.
2. Készíts hozzá teszteseteket a test_cases/ mappában.
3. Futtasd a teszteket, validáld az outputot.
4. Dokumentáld a változást a PROMPT_CHANGELOG.md-ben.
5. Minden új lépésnél futtasd le a korábbi lépések tesztjeit is (regresszió).

---

Ez a terv bármely agent/prompt fejlesztéséhez adaptálható, és a prompt_lab/docs alatt referenciaként szolgál. 