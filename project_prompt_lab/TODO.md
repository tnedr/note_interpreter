# Prompt Lab – TODO lista

## Aktuális feladatok

- [ ] Batch runner: több bundle automatikus futtatása egy mappában, összefoglaló riporttal
- [ ] CI/CD integráció: GitHub Actions vagy más pipeline, ami minden PR-nál lefuttatja a bundle-öket dummy/LLM módban
- [ ] Tapasztalati logolás: attempts_index.yaml automatikus frissítése minden bundle futás után
- [ ] Dokumentáció, onboarding: minta bundle-ök, best practice leírások, onboarding guide
- [ ] Új feature-ök, metrikák, validátorok: új output mezők, komplexebb validáció, új LLM provider integráció
- [ ] **Prompt Evolution Plan (PEP) integráció:** minden agenthez legyen PEP, amely tartalmazza a végcélt, input/output példákat, stepwise workflow-t, teszteseteket. A workflow jelenleg teljesen human-in-the-loop (HITL), de a rendszer AI-ready, hosszabb távon AI is generálhatja, módosíthatja vagy végrehajthatja a plan-t.
- [ ] Stepwise tesztek, bundle-ök generálása és validálása a PEP alapján, runner vagy UI támogatással.
- [ ] **Function call/tool usage integráció:** a Prompt Lab pipeline támogassa a tool call (pl. OpenAI function calling) workflow-t, stepwise plan és bundle szinten is.
- [ ] Tool call validáció, szimuláció, logolás, tesztelés: a runner képes legyen tool call-t végrehajtani vagy szimulálni, a validátor pedig ellenőrizni.

## Kész / DONE

- [x] Igazi LLM integráció: a runner script már támogatja a model.type: llm-t, és teszteltük is
- [x] Bundle workflow: lossless result bundle generálás, auditálható, diffelhető formátum
- [x] Dummy output: bundle-onként explicit output YAML-ból vagy fájlból
- [x] Logolás: minden bundle futás logja az agent saját logmappájába kerül
- [x] Runner: PromptBuilder-rel generált system prompt, bundle inputból context, initial_message támogatás, log.py loggert használja

---

*Ezt a listát minden fejlesztési lépés után frissítjük, a kész tételeket áthelyezzük a DONE szekcióba.* 