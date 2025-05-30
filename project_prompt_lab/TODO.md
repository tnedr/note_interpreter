# Prompt Lab – TODO lista

## Aktuális feladatok

- [ ] Batch runner: több bundle automatikus futtatása egy mappában, összefoglaló riporttal
- [ ] CI/CD integráció: GitHub Actions vagy más pipeline, ami minden PR-nál lefuttatja a bundle-öket dummy/LLM módban
- [ ] Tapasztalati logolás: attempts_index.yaml automatikus frissítése minden bundle futás után
- [ ] Dokumentáció, onboarding: minta bundle-ök, best practice leírások, onboarding guide
- [ ] Új feature-ök, metrikák, validátorok: új output mezők, komplexebb validáció, új LLM provider integráció

## Kész / DONE

- [x] Igazi LLM integráció: a runner script már támogatja a model.type: llm-t, és teszteltük is
- [x] Bundle workflow: lossless result bundle generálás, auditálható, diffelhető formátum
- [x] Dummy output: bundle-onként explicit output YAML-ból vagy fájlból
- [x] Logolás: minden bundle futás logja az agent saját logmappájába kerül

---

*Ezt a listát minden fejlesztési lépés után frissítjük, a kész tételeket áthelyezzük a DONE szekcióba.* 