## 6. MCP csomag telepítési lehetőségek

A MCP Project File Indexer csomagot többféleképpen is telepítheted más projektekbe:

### 6.1. Fejlesztői mód (editable)
```bash
pipenv shell
pip install -e C:/Users/Tamas/PycharmProjects/mcp_file_indexer

```
- Előnye: a forráskód módosításai azonnal elérhetők.

### 6.2. Normál telepítés helyi könyvtárból
```bash
pip install /path/to/mcp_project_file_indexer
```
- A setup.py vagy pyproject.toml alapján telepíti a csomagot.

### 6.3. Telepítés GitHub-ról
```bash
pip install git+https://github.com/<felhasznalo>/<repo>.git
```
- Példa:
```bash
pip install git+https://github.com/tamas/mcp_project_file_indexer.git
```
- Ehhez szükséges, hogy a repo tartalmazza a setup.py-t vagy pyproject.toml-t.

### 6.4. Telepítés PyPI-ról
```bash
pip install mcp_project_file_indexer
```
- Ehhez előbb publikálnod kell a csomagot a PyPI-n.

#### Összefoglaló táblázat

| Mód                | Parancs példa                                               | Frissül a forráskóddal? |
|--------------------|-------------------------------------------------------------|-------------------------|
| Fejlesztői (-e)    | pip install -e /path/to/mcp_project_file_indexer            | Igen                    |
| Helyi normál       | pip install /path/to/mcp_project_file_indexer               | Nem                     |
| GitHub             | pip install git+https://github.com/user/repo.git            | Nem (csak újratelepítéssel) |
| PyPI               | pip install mcp_project_file_indexer                        | Nem (csak újratelepítéssel) |

### Megjegyzések
- GitHub-os vagy PyPI-s telepítéshez legyen setup.py vagy pyproject.toml a projektben!
- Privát repo esetén a GitHub-os telepítéshez token vagy SSH kulcs kellhet.


### 6.5. Cursor.ai használat MCP csomaggal
Ha már telepítve van az MCP-csomag (pl. mcp_file_indexer):

🔧 1. Készíts (vagy frissíts) egy .cursor/mcp.json fájlt
{
  "servers": {
    "file-indexer": {
      "transport": "stdio",
      "command": "python",
      "args": ["-m", "mcp_file_indexer.server"]
    }
  }
}
Ha server.py nem __main__-ként fut, akkor:

"args": ["path/to/server.py"]
📄 2. Helyezz el egy .mdc szabályfájlt .cursor/rules/ mappában
Példa: .cursor/rules/file-index-generator.mdc

id: pfi
title: 'File Index Generator'
description: 'Listázza a projekt fájljait MCP-vel'
server: file-indexer
call:
  method: tools/call
  params:
    name: agent_tool
    arguments:
      directory: '.'
✅ 3. Használat Cursorban
Nyisd meg a projekted Cursorban (az a mappa legyen aktív, ahol .cursor/ van).

Írd be: /pfi

Automatikusan meghívja a agent_tool-t az MCP-szerveren keresztül.

📋 Összefoglaló táblázat
Mód	Parancs példa	Frissül a forráskóddal?	Használható Cursor-ban?
Fejlesztői (-e)	pip install -e /path/...	✅ Igen	✅ Igen
Helyi normál	pip install /path/...	❌ Nem	✅ Igen
GitHub	pip install git+https://...	❌ Nem	✅ Igen
PyPI	pip install mcp_project_file_indexer	❌ Nem	✅ Igen

