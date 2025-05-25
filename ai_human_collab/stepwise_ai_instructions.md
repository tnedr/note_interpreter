# Stepwise AI Coding Assistant – Prototípus Utasítások

Ez a dokumentum egy sablont és konkrét utasításokat tartalmaz arra, hogyan lehet az AI coding assistantet lépésenkénti, kontrollált végrehajtásra bírni.

## Általános sablon

> **Utasítás az AI coding assistantnek:**
> 
> 1. Csak az alábbi lépést hajtsd végre, mást ne módosíts, ne refaktorálj, ne írj tesztet, ne változtass más fájlt!
> 2. A lépés végrehajtása után részletesen írd le, pontosan mit csináltál (fájlok, sorok, funkciók, stb.).
> 3. Állj meg, és várj további utasításra, mielőtt bármilyen újabb lépést végrehajtanál!
> 4. Ne hajts végre több lépést egyszerre, ne próbálj optimalizálni vagy előre dolgozni!

## Példa prompt

> **Feladat:** Hozd létre a NoteParser osztály vázát a note_interpreter.py fájlban. Ne írj implementációt, ne módosíts más fájlt, ne adj hozzá tesztet.
> 
> **Instrukciók:**
> - Csak ezt az egy lépést hajtsd végre!
> - A végén írd le, pontosan mit csináltál.
> - Várj további utasításra!

## Megjegyzések
- Ezt a sablont minden lépésnél alkalmazni kell, hogy az AI valóban lépésenként, kontrolláltan haladjon.
- A promptot szükség szerint testre lehet szabni az adott feladathoz.
- Ha a lépés kész, manuálisan commitoljuk gitbe, majd jöhet a következő lépés.

## Konkrét példa: stepwise file update and commit

> **Feladat:**
> Egy megadott fájlba (pl. `example.txt`) szúrj be egy új sort minden lépésben, az alábbiak szerint:
> - 1. lépés: Szúrd be a fájl végére: `1. ujsor`
> - 2. lépés: Szúrd be a fájl végére: `2. ujsor`
> - 3. lépés: Szúrd be a fájl végére: `3. ujsor`
> - 4. lépés: Szúrd be a fájl végére: `4. ujsor`
> - 5. lépés: Szúrd be a fájl végére: `5. ujsor`
>
> **Instrukciók minden lépéshez:**
> 1. Csak az adott sort szúrd be, mást ne módosíts!
> 2. A lépés végrehajtása után részletesen írd le, pontosan mit csináltál.
> 3. Commitold a változást a git repository-ba, a következő üzenettel: `AI step N: Insert 'N. ujsor' into example.txt` (ahol N az aktuális lépés száma).
> 4. Állj meg, és várj további utasításra! 