import os
import sys
import shutil
from pathlib import Path

# Ensure repo root is on sys.path so tests can import the package without installing
ROOT = str(Path(__file__).resolve().parents[1])
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from theranostics.experiments import run_experiment


def test_run_experiment_creates_artifacts(tmp_path):
    artifacts_dir = str(tmp_path / "artifacts")
    # run small experiment
    res = run_experiment(params={"n": 5}, artifacts_dir=artifacts_dir)

    # Expect artifacts keys
    assert "artifacts" in res
    arts = res["artifacts"]
    assert isinstance(arts, dict)

    # Check that listed artifact files actually exist
    for path in arts.values():
        # paths returned should be absolute or relative; resolve relative to ROOT
        if os.path.isabs(path):
            assert os.path.exists(path), f"artifact {path} not found"
        else:
            alt = os.path.join(ROOT, path)
            assert os.path.exists(alt), f"artifact {path} not found at {alt}"

    # Clean up (tmp_path will be removed by pytest automatically)
    if os.path.exists(artifacts_dir):
        shutil.rmtree(artifacts_dir)
