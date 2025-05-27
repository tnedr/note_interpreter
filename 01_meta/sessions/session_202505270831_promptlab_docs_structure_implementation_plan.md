# 🧭 Session Log – Prompt Lab Spec Finalization (2025-05-27)

## 📌 Session Type

Spec Finalization & Design Clarification

## 🎯 Session Intent

A Prompt Lab nevű fejlesztési keretrendszer dokumentációjának és könyvtárszerkezetének véglegesítése. Kiemelten kezeltük az agents-központú logikát, a prompt engineering workflow lépéseit, a fájlnév-konvenciókat, a gépi és humán visszajelzések strukturált tárolását, valamint a teljes mappastruktúra olyan módon való kialakítását, hogy az egy Coding AI számára is könnyen feldolgozható legyen.

## 🧠 Dialogue Pathway

### 1. 📂 Dokumentumok átvizsgálása

* Átnéztük és értelmeztük az alábbi specifikációkat:

  * SYSTEM\_SPEC
  * FUNCTIONAL\_SPEC
  * TECHNICAL\_SPEC (frissítve)
  * IMPLEMENTATION\_PLAN korábbi és új verziója
  * TESTING GUIDE, STEPWISE PROMPT PLAN (áthelyezve archívumba)

### 2. 🏗️ Mappa- és fájlstruktúra definiálása

* Kialakítottuk az agent-alapú struktúrát:

  * `prompt_lab/agents/<agent_name>/`
  * `prompts/`, `test_cases/`, `logs/`, `outputs/`, `plan.md`, `attempts_index.yaml`, `overview.md`
* Támogató mappák: `libs/`, `scripts/`, `docs/`, `templates/`, `other/`

### 3. 🧩 Prompt workflow modellezés

* Lefektettük a step–prompt–attempt hármas kapcsolatot
* `attempts_index.yaml` mezőinek kidolgozása: `step`, `prompt`, `input`, `test_case`, `output`, `log`, `status`, `feedback`, `timestamp`
* Gépi és humán visszajelzés szétválasztása
* Több próbálkozás, verziózás kezelése `s<step>_v<version>.yaml` formátumban

### 4. 🧪 Tesztelési logika és fájlkezelés

* Structured output kezelése opcionálisan `outputs/` mappában
* Automatikus logolás `logs/` alatt
* Emberi visszajelzés az `attempts_index.yaml` `feedback:` mezőjében

### 5. 📄 Specifikációk frissítése

* `TECHNICAL_SPEC.md` bővítve:

  * teljes fájlstruktúra és mappa-rendszer
  * fájltípus–funkció mátrix
  * `attempts_index.yaml` példák (2 attempt)
  * prompt `meta:` blokk és kötelező `step:` mező említve

## 🌿 Branches & Follow-ups

* `prompt versioning` (mappa vs. fájlnév) → fájlnév formátum használata
* `attempts:` kulcs használata YAML-ban → megtartva gépi feldolgozáshoz
* Teszt fájlok mappázása `step_X/` szerint → helyette fájlnév alapján strukturálás
* Néhány nem aktív fájl (`06_TESTING_MASTER_GUIDE.md`, `07_stepwise_prompt_engineering_plan.md`) áthelyezése `other/` alá

## 🎁 Deliverables

* Frissített `03_TECHNICAL_SPEC.md` dokumentum (új fájlstruktúra, fájltípusok, példák)
* Új `attempts_index.yaml` sablon és 2 próbálkozás dokumentálása
* Új fájlnév-konvenciók: `s<step>_v<version>.yaml`, `test_s<step>_XX.yaml`
* Új mappastruktúra: agents-alapú, moduláris, AI-kompatibilis
* Letisztult logikai láncolat: step → prompt → attempt (input + log + output + feedback)
* Jóváhagyott, véglegesített 04_IMPLEMENTATION_PLAN.md

## 🔜 Next Steps

* Első prompt sablon (`s3_v1.yaml`) és teszteset (`test_s3_01.yaml`) létrehozása
* `prompt_builder.py` implementálása sablon–input injektálásra
* `run_tests.py` script prototípus tervezése
* Coding AI onboarding: implementációs fázis elindítása

---

*Session led and documented by Session Assistant – 2025-05-27.*
