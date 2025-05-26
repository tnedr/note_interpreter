---
title: "Agent Instruction – File Index Augmented v2"
modified: 2025-05-26
tags: [agent, instruction, file_index, augmented, cursor]
overview: "Strukturált agent task definíció: file index augmentáció, explicit input/output és task_text mezőkkel."
---

### instruction
goal:
- Add additional information to file index
prerequisites:
- Running the generate_file_index.py script
- Having the file_index.md
input: file_index.md
output: file_index_augmented.md
task_text:
Végig tudsz menni a fájlokon, és odaírni, hogy melyik fájl micsoda kb.? Az eredmény legyen teljesen olyan, mint a file_index.md, csak a fájlnévben legyen benne az "augmented" szó. 