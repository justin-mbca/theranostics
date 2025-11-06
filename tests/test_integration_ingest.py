import os
import subprocess
import sys

import pytest


def test_integration_ingest_roundtrip(tmp_path):
    # skip if pydicom isn't available
    try:
        import pydicom  # noqa: F401
    except Exception:
        pytest.skip("pydicom not installed")

    out_dir = tmp_path / "dicoms"
    out_dir_str = str(out_dir)
    # create 2 minimal DICOMs using the helper script
    res = subprocess.run([sys.executable, "scripts/make_test_dicom.py", out_dir_str, "--count", "2"], check=True, capture_output=True)
    assert res.returncode == 0

    # run the ingest wrapper to produce CSV
    out_csv = tmp_path / "out.csv"
    # use the shell wrapper which sets PYTHONPATH
    res2 = subprocess.run(["bash", "scripts/run_ingest.sh", out_dir_str, str(out_csv)], check=True, capture_output=True)
    assert res2.returncode == 0

    assert out_csv.exists()
    text = out_csv.read_text(encoding="utf-8")
    # expect at least one patient row or header
    assert "patient_id" in text or len(text.strip().splitlines()) >= 2
