# Prompt Testing Environment

Ez a mappa tartalmazza a prompt-alapú teszteléshez szükséges eszközöket a note_interpreter projekthez.

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