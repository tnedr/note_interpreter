---
modified: 2025-05-29
# Augmented: minden elemhez részletes magyarázat, különösen a Python file-okhoz és dokumentációkhoz
# Az eredeti file_index.md alapján generálva, részletes kód- és dokumentáció-annotációkkal
#
title: "Project File Index (Augmented, részletes)"
tags: [index, project_files, structure, augmented, detailed]
overview: "Ez a dokumentum minden fájlt és mappát részletesen ismertet, különös tekintettel a Python modulok osztályaira, függvényeire, valamint a dokumentációk tartalmára."
---

## Table of Contents
- [Project Root](#project-root)

## Project Root
- project_prompt_lab (folder)  # Prompt lab projekt, LLM agentek fejlesztéséhez, teszteléséhez, stepwise evolúcióhoz
  - _overview.md  # Áttekintő: a mappa célja, tartalma, workflow, changelog
  - docs (folder)  # Dokumentációk, specifikációk, útmutatók
    - 01_SYSTEM_SPEC.md  # Rendszerleírás: a Prompt Lab célja, fő komponensek (Agents, PromptBuilder, AgentCore, StepwisePlanManager), adatfolyam, kulcselvek, bővíthetőség, hivatkozások. Részletesen bemutatja a rendszer működését, fejlesztési elveit.
    - 02_FUNCTIONAL_SPEC.md  # Funkcionális specifikáció: a rendszer elvárt funkciói, use case-ek, felhasználói történetek, fő workflow-k.
    - 03_TECHNICAL_SPEC.md  # Technikai specifikáció: architektúra, fő komponensek részletes leírása (pl. StepwisePlanManager, PromptBuilder), interfészek, fájlformátumok, edge case-ek, bővíthetőség, naplózás, metaadatok, példák.
    - 04_implementation_plan.md  # Implementációs terv: fejlesztési ütemezés, milestone-ok, MVP-k, főbb lépések.
    - _improve.md  # Javítási javaslatok, fejlesztési ötletek.
    - _overview.md  # Áttekintő, tartalomjegyzék, dokumentációs workflow.
    - guide_testing_strategies_general.md  # Tesztelési stratégiák, best practice-ek, regressziós tesztelés.
    - plan_grocery_note_clarifier.md  # Grocery clarifier agent stepwise fejlesztési terve.
    - reference_stepwise_plan_clarify_score_full.md  # Stepwise terv referencia, milestone-ok, elvárt outputok.
    - requirements.txt  # Prompt lab függőségek, Python csomagok listája.
    - template_stepwise_prompt_plan_extended.md  # Stepwise prompt evolúciós terv sablon, adaptálható bármely agenthez.
  - prompt_lab (folder)  # Prompt lab kódok, agentek, könyvtárak
    - agents (folder)  # Agentek, minden agent külön mappában, promptokkal, tesztekkel, logokkal
      - README.md  # Általános leírás az agents mappa szerepéről, agentek szervezése
      - _overview.md  # Áttekintő: agentek szerkezete, workflow, changelog
      - grocery_clarifier (folder)  # Grocery clarifier agent stepwise fejlesztése
        - attempts_index.yaml  # Próbálkozások metaadatai: minden teszt, output, log, státusz, visszacsatolás, timestamp
        - experiments (folder)  # Kísérleti tesztesetek YAML-ban, pl. input, elvárt output
          - experiment_s1_01.yaml  # Teszteset: input note, elvárt clarity_score
          - experiment_s2_01.yaml  # Teszteset: input note, elvárt output
          - test_s3_01.yaml  # Teszteset: input note, elvárt output
        - logs (folder)  # Automatikus logok, minden prompt/output próbálkozásról
          - s3_v2.1__log.txt  # Log: részletes diff, output, hibák, tapasztalatok
        - outputs (folder)  # LLM outputok, JSON vagy YAML formátumban
          - s3_v2.1__output_01.json  # LLM output dump, egy konkrét teszteset eredménye
        - plan.yaml  # Stepwise prompt evolúciós terv: minden step neve, célja, prompt file, tesztesetek, elvárt output mezők, tesztfókusz
        - prompts (folder)  # Prompt sablonok YAML-ban, minden stephez külön
          - s1_v1.yaml  # Prompt sablon step 1-hez
          - s2_v1.yaml  # Prompt sablon step 2-höz
          - s3_v1.yaml  # Prompt sablon step 3-hoz
          - s3_v2.1.yaml  # Prompt sablon step 3 v2.1-hez
      - logs (folder)  # Agent logok, automatikus diff, output, hibák
        - v2__log.md  # Log: részletes diff, output, hibák, tapasztalatok
    - libs (folder)  # Újrafelhasználható Python modulok, utilityk
      - README.md  # Általános leírás: a libs mappa célja, utility modulok, pl. PromptBuilder, Logger
      - _overview.md  # Részletes áttekintő: minden file szerepe, workflow, changelog
      - agent_core.py  # Általános, bővíthető agent logika. Főbb osztályok/funkciók:
        # - BaseSharedContext: közös adatmodell, dinamikus mezők, export/import YAML-ba, thread-safe update, metaadatok kezelése.
        # - ToolDefinition: tool leíró dataclass (név, leírás, séma, függvény).
        # - ToolProvider (ABC): absztrakt tool provider, OpenAI/Anthropic implementációk.
        # - AgentState: agent állapotmodell (beszélgetés, tool outputok, hibák, metaadatok).
        # - AgentCore: generikus agent mag, stepwise workflow, LLM integráció, tool binding, interaktív session, tool hívások kezelése, conversation history, prompt injection, debug/logolás.
      - prompt_builder.py  # Szekció-alapú, registry-s prompt builder. Főbb osztályok/funkciók:
        # - PromptBuilder: szekciók registry-je, YAML/JSON config alapján prompt építés, placeholder kitöltés, decoratorral bővíthető szekciók.
        # - Számos szekciófüggvény: intro, goals, output_schema_and_meanings, scoring_guidelines, parameter_explanations, tool_json_schema, stb. (mindegyik külön funkció, a prompt szövegének generálásához).
      - colors.py  # ANSI színkódok user-facing outputhoz, banner színek, egyszerű színkezelés CLI/console outputhoz.
      - log.py  # Singleton logger: Log osztály (debug/info/warning/error, fájlba és konzolra logolás, újrainicializálható), log példány importálható.
      - stepwise_manager.py  # StepwisePlanManager osztály: stepwise plan loader/parser, YAML/MD plan betöltés, step metaadatok listázása, step lekérdezés, összefoglaló printelése.
    - other (folder)  # Egyéb, archív vagy referencia promptok, scoring configok
      - prompts (folder)  # Promptok, scoring configok, referencia YAML-ok
        - _overview.md  # Áttekintő, promptok, scoring configok, workflow
        - clarify_v1.yaml  # Clarify prompt sablon
        - promptfoo.yaml  # Promptfoo tesztelési konfiguráció
        - scoring_only_v1.yaml  # Csak scoring prompt sablon
    - templates (folder)  # Sablonok, minta file-ok
  - tests (folder)  # Tesztek, unit/integrációs
    - README.md  # Tesztek áttekintője, tesztelési workflow, coverage
    - _overview.md  # Áttekintő, tesztelési workflow, coverage