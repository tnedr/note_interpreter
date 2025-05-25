# Prompt Regression & Development Lab – Mini-projekt cél és mappa szerepe

Ez a mappa célja, hogy gyors, iteratív promptfejlesztést és -tesztelést tegyen lehetővé bármely LLM-alapú ügynök (agent) számára. A fő cél, hogy a promptok minél gyorsabban kipróbálhatók, összehasonlíthatók és továbbfejleszthetők legyenek, valósághű inputokkal és automatizált regressziós tesztekkel. A Promptfoo és LangSmith csak technikai eszközök ehhez a workflow-hoz.

## Tesztelési architektúra és workflow

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

## Promptfoo használata

1. Telepítsd a függőségeket:
   ```sh
   pipenv install -r prompt_testing/requirements.txt
   ```
2. Futtasd a teszteket:
   ```sh
   pipenv run promptfoo test promptfoo.yaml --provider openai:gpt-4
   ```
3. Webes playground indítása:
   ```sh
   pipenv run promptfoo web
   ```

## LangSmith használata

1. Regisztrálj a https://smith.langchain.com/ oldalon, és szerezd meg az API kulcsodat.
2. Állítsd be a környezeti változókat (pl. `.env`):
   ```
   LANGCHAIN_API_KEY=your-key-here
   LANGCHAIN_TRACING_V2=true
   ```
3. Futtasd a scriptet:
   ```sh
   pipenv run python langsmith_test.py
   ```

## Új tesztesetek hozzáadása
- A `promptfoo.yaml` fájlban adj hozzá új `tests` szekciókat.
- A `langsmith_test.py` scriptet bővítsd igény szerint. 