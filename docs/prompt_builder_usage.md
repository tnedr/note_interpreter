# PromptBuilder – Dinamikus, Agent-specifikus Promptok Használata

Ez a dokumentum bemutatja, hogyan használhatod az általános, újrafelhasználható PromptBuilder-t dinamikus, agent-specifikus promptok generálására, resource folder struktúrával.

---

## 1. Alapelvek

- **PromptBuilder**: Egy általános, szekció-alapú, registry-s Python osztály, amely YAML/JSON config és context alapján generál LLM promptokat.
- **prompt_config.yaml**: Agent-specifikus resource file, amely leírja a prompt szekciók sorrendjét, engedélyezettségét, sablon szövegeit, placeholder-eket.
- **prompt_sections.py**: Agent-specifikus Python modul, amely csak a dinamikus szekció-függvényeket és regisztrációkat tartalmazza.
- **context**: Egy tetszőleges dict, amely minden paramétert tartalmaz, amit a promptban placeholderként vagy dinamikus logikában használni akarsz.

---

## 2. Resource folder struktúra (példa)

```
resources/
  clarify_and_score_agent/
    prompt_config.yaml
    prompt_sections.py
    tools.py
    notes_output_schema.yaml
    ...
```

---

## 3. prompt_config.yaml (példa)

```yaml
sections:
  - name: intro
    enabled: true
    custom_text: |
      # 🤖 {agent_name}
      {agent_description}
  - name: goals
    enabled: true
    custom_text: |
      ## 🎯 Your Goals
      - ...
  - name: output_schema_and_meanings
    enabled: true
  # ... további szekciók ...
```

---

## 4. prompt_sections.py (példa)

```python
from note_interpreter.prompt_builder import PromptBuilder

@PromptBuilder.register_section('output_schema_and_meanings')
def output_schema_and_meanings_section(params, context):
    schema_file = params.get('schema_file', 'resources/clarify_and_score_agent/notes_output_schema.yaml')
    import yaml
    with open(schema_file, 'r', encoding='utf-8') as f:
        schema = yaml.safe_load(f)
    section = "## 📌 Output Schema\n\n"
    for field, info in schema.get('DataEntry', {}).items():
        section += f"- `{field}`: {info.get('description','')}\n"
    return section

# ... további szekciók ...
```

---

## 5. PromptBuilder használata (pipeline/agent kódban)

```python
# Importáld az agent-specifikus szekciómodult!
import resources.clarify_and_score_agent.prompt_sections
from note_interpreter.prompt_builder import PromptBuilder

prompt = PromptBuilder.build(
    context={
        "notes": notes,
        "memory": user_memory,
        "agent_name": "ClarifyAgent",
        "agent_description": "You clarify and score notes.",
        "threshold": 80,
        "prompt_version": "v2.1",
        # ... további paraméterek ...
    },
    config_path="resources/clarify_and_score_agent/prompt_config.yaml"
)
```

---

## 6. Best practice
- **A PromptBuilder core NEM tartalmaz agent-specifikus logikát.**
- **Minden agenthez külön prompt_config.yaml és prompt_sections.py resource legyen.**
- **A context dict minden paramétere placeholderként használható a promptban.**
- **A szekciók bővíthetők decoratorral, a registry automatikusan működik.**
- **A pipeline-ban csak importálni kell a megfelelő szekciómodult, a registry feltöltődik.**

---

## 7. Gyorsstart
1. Hozz létre egy új agent resource foldert (pl. `resources/my_agent/`).
2. Készíts egy `prompt_config.yaml`-t a szekciók sorrendjével, sablonjaival.
3. Készíts egy `prompt_sections.py`-t, regisztráld a dinamikus szekciókat.
4. A pipeline-ban importáld a szekciómodult, hívd a PromptBuilder-t a megfelelő context-tel és config_path-tal.

---

## 8. Példák context paraméterezésre
- `{notes}`: a jegyzetek listája
- `{memory}`: user memory
- `{threshold}`: agent threshold (pl. 80)
- `{agent_name}`: agent neve
- `{prompt_version}`: prompt verzió
- `{clarification_history}`: előző Q&A-k
- `{bármi_más}`: bármilyen egyedi paraméter

---

## 9. További tippek
- A serialize_value utility automatikusan formázza a listákat, dict-eket, None-t, stringet.
- A szekció-függvényekben a context dict minden kulcsa elérhető, így dinamikus logika is írható.
- A prompt_config.yaml és a szekciómodul együtt adja a teljes promptot.

---

Ha kérdésed van, vagy példát szeretnél egy konkrét agentre, nézd meg a resources/clarify_and_score_agent/ mappát, vagy kérj további mintát! 