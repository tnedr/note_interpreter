# _overview.md

## Purpose
Közös utility modulok, segédfüggvények (pl. PromptBuilder, Logger) számára fenntartott mappa.

## Context
Ide kerül minden olyan kód, amely több agent vagy tesztelési workflow számára is hasznos lehet.

## Usage
Használd a libs mappát közös, újrahasznosítható kódok tárolására.

## File Index
- README.md: Általános leírás
- agent_core.py: Általános, bővíthető agent logika, stepwise workflow, LLM integráció, tool binding, shared context kezelés. Alap minden komplex agenthez.
- agent_core_v2.py: Új generációs agent core, multi-level response, részletes logika, output validáció támogatás. Függ: output_validator.py, user_output.py
- prompt_builder.py: Szekció-alapú, registry-s prompt builder, YAML/JSON-ból épít, placeholder kitöltés, decoratorral bővíthető szekciók.
- colors.py: ANSI színkódok user-facing outputhoz, banner színek, egyszerű színkezelés CLI/console outputhoz.
- log.py: Singleton logger, debug/info/warning/error, fájlba és konzolra is tud logolni, könnyen újrainicializálható.
- output_validator.py: Újrafelhasználható output validátor függvények (validate_output, validate_llm_reply). Nem függ más libs moduloktól.

## Modulfüggőségek (libs/)

- output_validator.py
  - Nem függ más libs moduloktól.
- agent_core_v2.py
  - Függ: output_validator.py (output validációhoz)
  - Függ: user_output.py (logoláshoz)
- agent_core.py
  - Függ: user_output.py (logoláshoz)
- prompt_builder.py
  - Nem függ más libs moduloktól.
- colors.py
  - Nem függ más libs moduloktól.
- log.py
  - Nem függ más libs moduloktól.

## Workflow
1. Új utility modul fejlesztése
2. Tesztelés, dokumentálás
3. Több helyen történő felhasználás

## Changelog
- 2024-06-07: _overview.md létrehozva.
- 2024-06-08: agent_core.py, prompt_builder.py, colors.py, log.py rövid leírás hozzáadva.
- 2024-06-09: Modulfüggőségek szekció hozzáadva, output_validator.py és agent_core_v2.py dokumentálva.

## _improve 