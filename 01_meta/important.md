- Minden agenthez külön, célzott prompt_config.yaml-t érdemes írni.
- A prompt szekciók legyenek rövidek, csak az adott agent feladatára fókuszáljanak.
- A ClarifyAndScoreAgent promptja tartalmazza a scoring, clarification, iterációs és Q&A logikát.
- A FinalizeAndMemoryAgent promptja a véglegesítésre, enrichmentre, memóriabővítésre koncentráljon.
- Általános prompt szekciók: constraints, reasoning_style, meta_behavior.

============================ agensek kulon vayg egyutt ===============
- Mikor érdemes mégis külön szedni? Ha a scoring vagy a clarification önmagában is komplex, vagy különböző LLM-et, paramétereket, logikát igényel. Ha a memóriakezelés külön, aszinkron, vagy más pipeline-ban is használható.
- Összevonás előnyei
Egyszerűbb architektúra: Kevesebb osztály, kevesebb átadás, könnyebb tesztelni.
Átláthatóbb pipeline: A fő lépések (tisztázás, véglegesítés) világosabbak.
Könnyebb fejlesztés: Ha a két funkció mindig együtt jár, nem kell feleslegesen szétválasztani.
- javasolt struktura
1. ClarifyAndScoreAgent
Feladat:
Minden iterációban kiszámolja a clarity/ambiguity score-okat.
Ha kell, kérdéseket generál, user inputot vár, beépíti a válaszokat.
Addig iterál, amíg minden jegyzet elég érthető vagy el nem éri a max. körszámot.
Kimenet:
Jegyzetek, minden clarity flag, clarification_qas.
2. FinalizeAndMemoryAgent
Feladat:
Véglegesíti a jegyzeteket (kategorizálás, enrichment).
Új memory pointokat generál, ha kell.
Kimenet:
Végső JSON output, memóriabővítés.
3. Orchestrator (Pipeline)
Feladat:
Vezérli a pipeline-t, hívja a két agentet a megfelelő sorrendben.