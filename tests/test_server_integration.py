import subprocess
import time
import requests
import os
import sys
import tempfile
import shutil
import pytest

def test_server_file_indexer(tmp_path):
    # 1. Elindítjuk a szervert háttérben
    server_proc = subprocess.Popen(
        [sys.executable, "-m", "mcp_file_indexer.server"],
        cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),  # projekt gyökere
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(2)  # Várunk, hogy a szerver elinduljon

    try:
        # 2. Létrehozunk ideiglenes fájlokat
        test_file1 = tmp_path / "file1.txt"
        test_file1.write_text("Hello world!")
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        test_file2 = subdir / "file2.txt"
        test_file2.write_text("Teszt tartalom")

        # 3. HTTP-kérés a szerverre (mint a Cursor agent)
        url = "http://127.0.0.1:8000/mcp/"
        headers = {"Accept": "text/event-stream"}
        params = {"directory": str(tmp_path)}
        response = requests.get(url, headers=headers, params=params, stream=True)

        assert response.status_code == 200
        # Feldolgozzuk a streamelt választ
        lines = [line.decode() for line in response.iter_lines() if line]
        joined = "\n".join(lines)
        assert "file1.txt" in joined
        assert "file2.txt" in joined

    finally:
        server_proc.terminate()
        try:
            server_proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_proc.kill() 