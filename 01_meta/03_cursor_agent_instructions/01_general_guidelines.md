---
title: "Cursor Agent Instructions – General Guidelines"
modified: 2025-05-26
tags: [meta, agent, instructions, cursor, automation, guidelines]
overview: "Általános irányelvek, sablon és best practice-ek Cursor agent task/instruction íráshoz."
---

# Cursor Agent Instructions – Általános irányelvek

Ez a dokumentum összefoglalja, hogyan érdemes Cursor agent task/instruction definíciókat írni, hogy átlátható, újrahasznosítható és fejleszthető legyen az automatizációs workflow.

## Mi az a Cursor Agent Instruction?
Egy strukturált, célorientált utasítás vagy workflow-leírás, amelyet egy AI-ügynök (agent) végrehajt. Nem egyszerű prompt, hanem összetett, akár több lépéses, kontextusfüggő feladat.

## Sablon
```markdown
### Agent Instruction
- **Cél:** [Mi a végső cél, output?]
- **Bemenet:** [Milyen inputot kap az agent?]
- **Elvárt output:** [Milyen formátumú, tartalmú eredményt várunk?]
- **Lépések:**
  1. [Első lépés]
  2. [Második lépés]
  3. ...
- **Speciális szabályok / megjegyzések:**
  - [Pl. mit ne hagyjon ki, milyen formátumot kövessen, stb.]
```

## Best Practices
- **Legyen egyértelmű a cél:** Fogalmazd meg pontosan, mit vársz el az agenttől.
- **Határozd meg a bemenetet:** Milyen fájlokon, adatokon dolgozzon?
- **Részletezd a lépéseket:** Ha összetett a feladat, bontsd lépésekre.
- **Formátum és output:** Írd le, milyen formátumban, struktúrában várod az eredményt.
- **Legyen újrahasznosítható:** Úgy írd, hogy máskor is felhasználható legyen.
- **Meta-instrukciók:** Ha több agent vagy workflow dolgozik együtt, legyen világos a feladatmegosztás. 