Helper scripts
--------------

`make_test_dicom.py` — create minimal DICOM files for local testing.

`ingest_dicom.py` — CLI wrapper to run the DICOM metadata ingest. Can be executed directly (it will add the repo root to `sys.path`) or via `scripts/run_ingest.sh` which sets `PYTHONPATH`.

`run_ingest.sh` — small wrapper that sets `PYTHONPATH` and runs `ingest_dicom.py`.

Examples
```
python scripts/make_test_dicom.py /tmp/mydicoms --count 3
./scripts/run_ingest.sh /tmp/mydicoms data/bronze/dicom_metadata.csv
```
