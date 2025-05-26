# Prompt Lab – MVP1 Implementációs terv

Ez a dokumentum lépésről lépésre végigvezet a Prompt Lab MVP1 megvalósításán. Az MVP1 célja egy nagyon egyszerű, 3 összetevős agent prompt fejlesztése, tesztelése és futtatása.

---

## 0. Előkészületek

- [ ] Projektstruktúra ellenőrzése: `prompt_lab/` és alkönyvtárai (agents, libs, test_inputs, results, scripts, tests, configs) léteznek.
- [ ] README és dokumentáció frissítése, MVP1 céljának rögzítése.

---

## 1. Agent prompt MVP1 – 3 összetevő

**Cél:** Egy agent prompt, amely három mezőt kezel (pl. `note`, `memory`, `clarification`).

### 1.1. Agent mappa létrehozása

- [ ] Hozd létre az `agents/simple_agent/` mappát.
- [ ] Hozd létre benne:
  - [ ] `prompts/`
  - [ ] `test_cases/`
  - [ ] (opcionális) `metadata.yaml`

### 1.2. Prompt verzió létrehozása

- [ ] Hozz létre egy YAML fájlt: `agents/simple_agent/prompts/v1.yaml`
- [ ] Írd bele a 3 összetevős promptot, pl.:
  ```yaml
  system: |
    You are a simple agent. Your job is to process the following:
    - Note: {note}
    - Memory: {memory}
    - Clarification: {clarification}
    Please return a summary.
  ```

### 1.3. Teszteset(ek) létrehozása

- [ ] Hozz létre egy YAML fájlt: `agents/simple_agent/test_cases/test1.yaml`
- [ ] Adj meg egy valósághű inputot:
  ```yaml
  input:
    note: "Buy milk"
    memory: "User often forgets groceries"
    clarification: "Is lactose-free needed?"
  expected:
    output_contains: ["milk", "groceries", "lactose-free"]
  ```

---

## 2. PromptBuilder MVP

- [ ] Hozd létre a `libs/prompt_builder.py`-t.
- [ ] Implementálj egy függvényt, ami betölti a YAML promptot, és behelyettesíti a mezőket.
- [ ] Hozz létre unit tesztet a `tests/` mappában, ami ellenőrzi, hogy a prompt helyesen épül fel.

---

## 3. AgentCore MVP

- [ ] Hozd létre a `libs/agent_core.py`-t.
- [ ] Implementálj egy minimális osztályt/függvényt, ami:
  - [ ] Betölti a promptot a PromptBuilderrel.
  - [ ] Meghívja az LLM-et (vagy mockolja, ha nincs API).
  - [ ] Visszaadja az outputot.
- [ ] Dummy LLM integráció: ha nincs OpenAI API, írj egy dummy függvényt, ami előre definiált választ ad vissza.

---

## 4. Teszt inputok és futtató script

- [ ] Helyezd el a teszt inputokat a `test_inputs/` mappában (akár symlink a test_cases-hez).
- [ ] Hozz létre egy `scripts/run_tests.py` scriptet, ami:
  - [ ] Betölti az agent promptot.
  - [ ] Betölti a teszt inputot.
  - [ ] Lefuttatja az agentet.
  - [ ] Kiírja az outputot és ellenőrzi, hogy az elvárt szavak benne vannak-e.

---

## 5. Eredmények naplózása

- [ ] A script írja ki az eredményt a `results/` mappába (pl. `results/simple_agent_test1.txt`).

---

## 6. Dokumentáció és README frissítés

- [ ] Írd le az MVP1 lépéseit a README-ben.
- [ ] Dokumentáld, hogyan lehet új promptot, tesztet hozzáadni.

---

## 7. (Opcionális) Automatizált teszt

- [ ] Hozz létre egy unit tesztet a `tests/` mappában, ami automatikusan futtatja a fenti pipeline-t.

---

# Összefoglaló checklist

- [ ] Projektstruktúra előkészítése
- [ ] Agent mappa és 3 mezős prompt létrehozása
- [ ] Teszteset(ek) létrehozása
- [ ] PromptBuilder MVP implementálása
- [ ] AgentCore MVP implementálása
- [ ] Dummy LLM vagy OpenAI integráció
- [ ] Futtató script és output ellenőrzés
- [ ] Eredmények naplózása
- [ ] Dokumentáció frissítése
- [ ] (Opcionális) Unit teszt 