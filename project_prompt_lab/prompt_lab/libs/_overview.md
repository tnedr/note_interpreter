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
- prompt_builder.py: Szekció-alapú, registry-s prompt builder, YAML/JSON-ból épít, placeholder kitöltés, decoratorral bővíthető szekciók.
- colors.py: ANSI színkódok user-facing outputhoz, banner színek, egyszerű színkezelés CLI/console outputhoz.
- log.py: Singleton logger, debug/info/warning/error, fájlba és konzolra is tud logolni, könnyen újrainicializálható.

## Workflow
1. Új utility modul fejlesztése
2. Tesztelés, dokumentálás
3. Több helyen történő felhasználás

## Changelog
- 2024-06-07: _overview.md létrehozva.
- 2024-06-08: agent_core.py, prompt_builder.py, colors.py, log.py rövid leírás hozzáadva.

## _improve 