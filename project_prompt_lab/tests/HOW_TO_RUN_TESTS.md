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

> **Tipp:** Ha egyetlen tesztfájlt futtatsz, és import hibát kapsz (ModuleNotFoundError: No module named 'prompt_lab'), ellenőrizd, hogy a tesztfájl elején benne van-e:
> ```python
> import sys
> from pathlib import Path
> sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
> ```
> Ez biztosítja, hogy a prompt_lab importok működjenek.

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

## 🧑‍💻 Agent- és LLM-barát tesztfuttatás

A legegyszerűbb, legmegbízhatóbb módja a tesztek futtatásának:

```bash
python run_tests_safe.py
```

Ez a script automatikusan beállítja a helyes import utakat, így nem kell külön PYTHONPATH-ot vagy working directory-t megadni. Bármilyen ügynök, CI vagy fejlesztő így futtathatja a teszteket, hiba nélkül.

A script a `project_prompt_lab/tests/` összes tesztjét lefuttatja, marker nélkül a dummy, markerrel a valódi LLM teszteket is.

> **Tipp:** Ha csak dummy teszteket akarsz futtatni:
> ```bash
> python run_tests_safe.py -m 'not llm_required'
> ```

---

**Best practice:**
- Dummy teszteket fejlesztéshez, CI-hez használd.
- Valódi LLM teszteket csak explicit, manuális futtatásra, pl. release előtt.

## ⚠️ Fontos tapasztalat: importok, sys.path és agent-barát tesztfuttatás

- A Python importok működése attól függ, hogy a sys.path-ban milyen könyvtárak szerepelnek.
- Ha a tesztekben vagy a kódban így importálsz: `from prompt_lab.libs...`, akkor a `project_prompt_lab` mappát kell hozzáadni a sys.path-hoz.
- Ha így: `from project_prompt_lab.prompt_lab.libs...`, akkor a projekt gyökerét (note_interpreter) kell a sys.path-hoz adni, és a `project_prompt_lab`-ot csomagként kell kezelni.
- A legjobb, ha mindenhol egységesen a `from prompt_lab...` importot használod az alprojekten belül.
- Az agent-barát `run_tests_safe.py` script úgy lett kialakítva, hogy mind a projekt gyökerét, mind a `project_prompt_lab` mappát hozzáadja a sys.path-hoz, így minden import működik.
- Ha import hibát kapsz, először nézd meg, hogy a tesztfuttató script sys.path-jában benne van-e a szükséges könyvtár (print(sys.path) segíthet).
- A working directory (ahonnan a scriptet indítod) is befolyásolja, hogy a relatív útvonalak hova mutatnak – ezért a runner script mindig abszolút elérési utat használ a tesztmappához.

**Ez a tapasztalat segít elkerülni a ModuleNotFoundError és import hibákat a jövőben!**

---

## ⚠️ Stepwise pipeline tesztek DEPRECATED

A következő tesztek és pipeline-ok a korábbi stepwise architektúrához tartoztak, de az experience bundle workflow-ra való áttérés miatt már nem karbantartottak, deprecated státuszba kerültek, és a tesztfuttatás során automatikusan kihagyásra kerülnek:
- test_run_stepwise.py
- test_stepwise_manager.py
- test_run_stepwise_real_llm.py

Az aktuális, karbantartott tesztstruktúra az experience bundle workflow-t követi.

--- 