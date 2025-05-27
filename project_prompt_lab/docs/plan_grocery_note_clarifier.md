# plan\_grocery\_note\_clarifier.md – Prompt Evolution Plan

## 🎯 Agent: Grocery Note Clarifier

Ez a dokumentum egy konkrét agent, a Grocery Note Clarifier stepwise fejlesztési tervét írja le. Minden step egy újabb funkció bevezetését célozza meg, amely egyre komplexebb értelmezési képességet tesz lehetővé.

---

## 🧩 Prompt Evolution Steps

### 🔹 Step 1 – Scoring Only

**Cél:** A bemeneti jegyzet világosságának értékelése.

* **Output mezők:**

  * `clarity_score`: int (0–100)
  * `interpreted_text`: null
  * `ask_user_question`: null

**Példák:**

* Input: "tej" → clarity\_score: 60
* Input: "kávé cukor" → clarity\_score: 85

---

### 🔹 Step 2 – Add Interpretation

**Cél:** A jegyzet szándékának értelmezése.

* **Output mezők:**

  * `clarity_score`: int
  * `interpreted_text`: string (ha értelmezhető)
  * `ask_user_question`: null

**Példák:**

* Input: "tej" → interpreted\_text: "vásárolj tejet"
* Input: "kenyér" → interpreted\_text: "vegyél kenyeret"

---

### 🔹 Step 3 – Clarification Question (Free Text)

**Cél:** Homályos jegyzet esetén kérdés felajánlása.

* **Output mezők:**

  * `clarity_score`: int
  * `interpreted_text`: null
  * `ask_user_question`: string

**Példa:**

* Input: "tej" → ask\_user\_question: "Milyen tejet szeretnél? (normál, laktózmentes, hány %-os)"

---

### 🔹 Step 4 – Structured Clarification Output (Function Call Style)

**Cél:** A kérdés gépi feldolgozásra alkalmas struktúrában való megadása.

* **Output mezők:**

  * `clarity_score`: int
  * `interpreted_text`: null
  * `clarification_tool_call`:

    ```json
    {
      "function": "ask_user",
      "parameters": {
        "question": "Milyen tejet szeretnél? (normál, laktózmentes, hány %-os)"
      }
    }
    ```

**Megjegyzés:** Ez a lépés előkészíti az agent tool-calling kompatibilitását.

---

## 🧠 Fejlesztési megjegyzések

* Minden stephez tartozik 1–2 teszteset
* Prompt fájlok külön verziózva (v1.yaml → v4.yaml)
* Minden próbálkozás logolható a `logs/` mappában
* A plan manuálisan szerkeszthető, AI-nak átadható

---

*Ez a plan a Grocery Clarifier agent fejlesztési roadmapje. Használható a Prompt Lab rendszer StepwisePlanManager komponense által inputként.*
