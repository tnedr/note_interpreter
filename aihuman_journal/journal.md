# AI-Human Project Journal

- A Prompt Lab funkcionális specifikációja bővült a Stepwise Prompt Development Support (3.6) és az Evolution-based Agent Development workflow szekciókkal.
- A Prompt Lab funkcionális specifikációja bővült a Prompt Attempts & Iterative Learning (Human-in-the-loop support) szekcióval.
- A Prompt Lab technikai specifikációja bővült az Attempt-level tracking and experience logging, valamint a Prompt Attempt Metadata & Logs szekciókkal.
- now 2024-06-08

- A Prompt Lab rendszerleírásába bekerült a StepwisePlanManager komponens, a paraméterezhető Prompt Evolúció elv, és a Prompt Evolution Plan bővíthetőség.
- Az '1. ujsor' sort hozzáadtam az ai_human_collab/project_stepwise_cursor_agent/example.txt fájl végéhez a stepwise AI coding test első lépéseként. 
- A második lépésben beszúrtam a '2. ujsor' sort az ai_human_collab/example.txt fájl végére. 
- Elolvastam a project_stepwise_cursor_agent mappában található összes fájlt, és összefoglaltam a tartalmukat. 
- Minden fő mappába létrehoztam egy _overview.md-t a project_prompt_lab alatt, amely tartalmazza: purpose, context, usage, file index, workflow, changelog.
- Minden _overview.md végére bekerült egy üres _improve szekció a project_prompt_lab fő mappáiban.
- Bővítettem a Prompt Lab technikai specifikációját: hozzáadtam a StepwisePlanManager komponenst az architektúrához, részleteztem a feladatait, és kibővítettem az interfész szekciót a Prompt Evolution Plan formátumával és új CLI paranccsal.
- Áttekintettem és dokumentáltam a libs mappában lévő új modulokat (agent_core.py, prompt_builder.py, colors.py, log.py), rövid összefoglalót írtam az _overview.md-be.
- Elkészült a minimalista teszt pipeline (run_tests.py) az MVP Phase 1-hez: betölti a promptot és tesztesetet, dummy LLM-mel lefuttatja, és ellenőrzi az outputot.
- Elkészült a StepwisePlanManager MVP váza (libs/stepwise_manager.py): betölti és feldolgozza a stepwise plan-t, listázza a step metaadatokat.
- Létrehoztam egy új, experiment-alapú plan.yaml-t a grocery_clarifier agenthez, amely experiment_cases-t és bővített YAML struktúrát használ.
- Végrehajtottam a file_index.md augmentációs instrukcióját, és létrehoztam a file_index_augmented.md-t, minden elemhez rövid magyarázattal.
- now 2025-05-29

- Integráltam az 'Experiment Bundle Architecture' szekciót a TECHNICAL_SPEC.md végére a Prompt Lab projektben.
- now 2024-06-07

- Frissítettem a TECHNICAL_SPEC.md könyvtárszerkezet szekcióját, hogy az agents/<agent>/ alatt számozott, dedikált alkönyvtárak (01_prompts, 02_inputs, 03_experiment_bundles, 04_actual_outputs, 05_logs) szerepeljenek.
- now 2024-06-07

- Kiegészítettem a TECHNICAL_SPEC.md-t egy explicit experiment bundle workflow folyamatábrával, egy mező-összehasonlító táblázattal és egy YAML példával, hogy a bundle → result_bundle átmenet teljesen egyértelmű legyen.
- now 2024-06-07

- Létrehoztam egy agent-barát run_tests_safe.py scriptet a project_prompt_lab alprojektben, és kiegészítettem a HOW_TO_RUN_TESTS.md-t a használatával kapcsolatos útmutatóval.
- A stepwise pipeline-hoz tartozó régi teszteket deprecated státuszba helyeztem, és a HOW_TO_RUN_TESTS.md-t frissítettem, hogy jelezze az experience bundle workflow az aktuális.

- Minden LLM modell beállítást gpt-4.1-mini-re állítottunk át a kódban és a bundle-okban, hogy elkerüljük a drága modellek véletlen használatát.