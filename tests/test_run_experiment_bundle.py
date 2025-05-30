import subprocess
import yaml
from pathlib import Path

def test_run_experiment_bundle(tmp_path):
    # Másoljuk a teszt bundle-t a temp könyvtárba
    bundle_src = Path("project_prompt_lab/prompt_lab/examples/experiment_bundles/test_bundle.yaml")
    bundle_dst = tmp_path / "test_bundle.yaml"
    bundle_dst.write_text(bundle_src.read_text(encoding="utf-8"), encoding="utf-8")

    # Futtassuk a scriptet
    result = subprocess.run([
        "python", "run_experiment_bundle.py", str(bundle_dst)
    ], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed: {result.stderr}"

    # Ellenőrizzük a bundle-t
    bundle = yaml.safe_load(bundle_dst.read_text(encoding="utf-8"))
    assert "actual_output" in bundle
    assert bundle["actual_output"] == {
        "clarity_score": 50,
        "interpreted_text": "TESZT JEGYZET"
    }
    assert "validation" in bundle
    assert bundle["validation"]["result"]["status"] == "passed"
    assert "log" in bundle
    assert bundle["log"]["status"] == "passed" 