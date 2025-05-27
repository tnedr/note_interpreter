# 01_SYSTEM_SPEC.md – Prompt Lab rendszerleírás

## 1. Cél (Purpose)
A Prompt Lab egy moduláris, bővíthető környezet LLM-alapú agent promptok fejlesztésére, verziózására, tesztelésére és regressziós ellenőrzésére.

## 2. Rendszeráttekintés (System Overview)
- A Prompt Lab célja, hogy a prompt engineering folyamatot lépésről lépésre, mérföldköveken keresztül, visszamenőleges kompatibilitással és automatizált teszteléssel támogassa.
- Minden promptverzió és agent viselkedés szigorúan tesztelt, minden új funkció/mérföldkő csak akkor léphet életbe, ha a korábbi tesztek is sikeresek.

## 3. Fő komponensek (Main Components)
- **Agents:** Agent-specifikus promptok, logika, tesztesetek.
- **PromptBuilder:** Prompt YAML-ok betöltése, szekciók összeállítása, változók behelyettesítése.
- **AgentCore:** Agent logika, prompt pipeline, LLM hívások, stepwise/multi-turn kezelés.
- **Teszt Runner:** Automatizált és manuális tesztfuttatás, eredmények naplózása, regressziók detektálása.
- **Eredménykezelés:** Teszt outputok, diff-ek, logok, riportok strukturált tárolása.

## 4. Adatfolyam (Data Flow)
1. Teszt input (YAML/JSON) →
2. Agent + PromptBuilder →
3. LLM hívás (vagy dummy) →
4. Output értékelés, diff, naplózás →
5. Regressziók, riportok

## 5. Kulcselvek (Key Principles)
- **Stepwise fejlesztés:** Minden új promptverzió/mérföldkő csak akkor léphet életbe, ha minden korábbi teszt sikeres.
- **Append-only prompt evolúció:** Promptok csak bővülhetnek, meglévő logika nem törölhető.
- **Automatizált regresszió:** Minden promptverzió minden tesztesetét automatikusan futtatni kell.
- **Séma-kompatibilitás:** Input/output mindig gépileg feldolgozható, explicit mezőkkel.
- **Edge case/fallback kezelés:** Homályos, hibás inputokra is robusztus, előre definiált válaszok.

## 6. Bővíthetőség (Extensibility)
- Új agent, prompt pipeline vagy teszteset hozzáadása csak új file/folder létrehozásával, core kód módosítása nélkül.
- Több LLM provider, teszt runner (Promptfoo, LangSmith, stb.) támogatott.

## 7. Hivatkozások (References)
- 02_FUNCTIONAL_SPEC.md – Funkcionális specifikáció
- 03_TECHNICAL_SPEC.md – Technikai specifikáció
- 06_TESTING_MASTER_GUIDE.md – Tesztelési elvek
- 07_stepwise_prompt_engineering_plan.md – Stepwise prompt fejlesztési terv
- stepwise_prompt_development_plan__ClarifyAndScoreAgent.md – Részletes stepwise terv

---
*Ez a dokumentum a Prompt Lab projekt teljes rendszerleírása. Minden fejlesztés, bővítés, tesztelés előtt ezt vedd alapul!* 