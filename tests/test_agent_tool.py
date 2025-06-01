import os
import pytest
from mcp_file_indexer.agent import MCPAgent

def test_agent_tool_file_indexing(tmp_path):
    # Létrehozunk egy ideiglenes mappát, és benne néhány fájlt
    test_file1 = tmp_path / "file1.txt"
    test_file1.write_text("Hello world!")

    subdir = tmp_path / "subdir"
    subdir.mkdir()
    test_file2 = subdir / "file2.txt"
    test_file2.write_text("Teszt tartalom")

    # Inicializáljuk az MCPAgent-et
    agent = MCPAgent()

    # A bemeneti adatok itt JSON-szerű dict formájában vannak megadva
    input_params = {"directory": str(tmp_path), "config_path": "nonexistent.yaml"}
    
    # Meghívjuk az MCPAgent handle_structured metódusát
    result = agent.handle_structured(input_params)
    
    # A result-nek tartalmaznia kell egy "files" kulcsot, amiben IndexedFile példányok vannak
    files = result.get("files", [])
    # Kinyerjük a relatív elérési utakat
    file_paths = [f.path for f in files]

    # Ellenőrizzük, hogy a teszt fájlok benne vannak
    assert "file1.txt" in file_paths
    assert os.path.join("subdir", "file2.txt") in file_paths 