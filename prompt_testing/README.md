# Prompt Regression & Development Lab – Mini-projekt cél és mappa szerepe

Ez a mappa egy önálló, iteratív promptfejlesztő és regressziós tesztkörnyezet a note_interpreter projekthez. Célja, hogy:
- Gyorsan lehessen új promptokat fejleszteni, verziózni és tesztelni különböző inputokra, user memory-ra és clarification history-re.
- Automatizált regressziós tesztekkel biztosítsa, hogy minden promptverzió visszafelé kompatibilis és minőségi maradjon.
- Támogassa a prompt-alapú ügynökök (pl. ClarifyAndScoreAgent) fejlesztését, edge case-ek és tipikus felhasználói szcenáriók lefedésével.

A mappa tartalmaz prompt sablonokat, teszt inputokat, automatizált tesztfuttató szkripteket, valamint Promptfoo és LangSmith integrációt a gyors iteráció és minőségbiztosítás érdekében.

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