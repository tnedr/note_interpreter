import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parent

tests_dir = str(ROOT / "tests")
args = ["pytest", tests_dir] + sys.argv[1:]
exit_code = subprocess.call(args)
sys.exit(exit_code) 