# 📦 Experiment Bundle – YAML alapú prompt-teszt egység

Ez a formátum egyetlen `.yaml` fájlban rögzíti a teljes prompt-futtatási próbálkozás minden fontos komponensét:
- **prompt** (szöveg vagy fájlból)
- **input** (egyedi vagy batch)
- **model információ**
- **expected vs actual output**
- **validációs eredmény**
- **log és metaadatok**

## 🎯 Célja

- **Reprodukálhatóság:** mindig tudd, milyen prompt és milyen modellel generáltad az outputot.
- **Transzparencia:** minden összetevő egy helyen – ember és gép is könnyen olvassa.
- **Debug / review / dokumentáció:** prompt tuning, tesztelés és QA során könnyen visszakövethető legyen minden.
- **Batch feldolgozásra is alkalmas.**

## 🧩 Fájlstruktúra

```yaml
prompt:                  # prompt szöveg vagy fájlhivatkozás
  purpose: "clarity scoring baseline"
  source: prompts/s1_v1.yaml
  text: |
    You are a clarity scorer...
input:                   # input egyedi vagy csv-batch
  format: yaml
  content:
    note: "tej"
model:                   # pontos modell setup
  provider: openai
  name: gpt-4
  version: 0613
  temperature: 0.2
  max_tokens: 512
  system_prompt: "You are a helpful assistant."
expected_output:         # mit vártunk
  clarity_score: 60
  interpreted_text: null
actual_output:           # mit kaptunk vissza
  clarity_score: 45
  interpreted_text: "tej"
validation:              # automatikus összevetés eredménye
  validator_profile: default
  result:
    status: failed
    mismatches:
      - field: clarity_score
        expected: 60
        actual: 45
log:                     # logfájl hivatkozás
  status: failed
  path: logs/exp_001__log.md
meta:                    # kiegészítő információk
  author: tamas
  created_at: "2025-05-29T20:20"
  tags: ["clarity", "step1", "LLM"]
