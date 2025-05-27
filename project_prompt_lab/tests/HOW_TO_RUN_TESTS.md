# How to Run Tests (Prompt Lab)

This folder contains unit and integration tests for the Prompt Lab modules.

## 1. Dummy (gyors, biztonságos) tesztek futtatása

A legtöbb teszt, köztük a `test_run_stepwise.py`, **csak dummy LLM-et** használ, így gyorsan, determinisztikusan fut, nem igényel API kulcsot.

**Csak dummy tesztek futtatása:**

```bash
pytest project_prompt_lab/tests -m 'not llm_required'
```

> **Fontos:** Ha csak simán futtatod a pytestet marker nélkül (`pytest project_prompt_lab/tests`), akkor **minden teszt lefut**, beleértve a valódi LLM teszteket is!

## 2. Valódi LLM tesztek futtatása

A valódi LLM-et igénylő tesztek (pl. `test_run_stepwise_real_llm.py`) `@pytest.mark.llm_required`-del vannak megjelölve, és **nem futnak le automatikusan**.

Futtatásukhoz:

```bash
pytest project_prompt_lab/tests/test_run_stepwise_real_llm.py -m llm_required
```

> **Fontos:** Ezekhez szükséges az `OPENAI_API_KEY` környezeti változó (pl. `.env` fájlban vagy shellben exportálva).

## 3. Minden teszt futtatása (nem ajánlott CI-ben)

```bash
pytest project_prompt_lab/tests
```

vagy

```bash
pytest project_prompt_lab/tests -m 'not llm_required or llm_required'
```

## 4. Környezeti változó beállítása valódi LLM-hez

- `.env` fájl a projekt gyökerében:
  ```
  OPENAI_API_KEY=sk-...
  ```
- vagy shellben:
  ```bash
  export OPENAI_API_KEY=sk-...
  ```

## 5. Marker használat
- Dummy tesztek: marker nélkül, mindig futnak.
- Valódi LLM tesztek: `@pytest.mark.llm_required` szükséges.
- Marker a projekt gyökerében lévő `pytest.ini`-ben van definiálva.

## 6. Példa: csak egy tesztfájl futtatása

Dummy (gyors):
```bash
pytest project_prompt_lab/tests/test_run_stepwise.py -m 'not llm_required'
```
Valódi LLM:
```bash
pytest project_prompt_lab/tests/test_run_stepwise_real_llm.py -m llm_required
```

---

**Best practice:**
- Dummy teszteket fejlesztéshez, CI-hez használd.
- Valódi LLM teszteket csak explicit, manuális futtatásra, pl. release előtt. 