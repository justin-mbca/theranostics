Implementation summary — Theranostics prototype
===============================================

Overview
--------
This repository is a minimal local prototype that demonstrates an end-to-end biomedical data pipeline for oncology-focused survival modeling. It contains synthetic data generation, a small orchestration flow, baseline survival models, and a DICOM ingestion stub with tests.

What was implemented
---------------------
- Project scaffold and environment:
  - `requirements.txt`, `pyproject.toml`, `README.md`.
  - Virtual environment used locally (not committed).
- Synthetic data & modeling:
  - `theranostics/simulate.py` — generates a synthetic clinical cohort with time-to-event labels.
  - `theranostics/models.py` — Kaplan-Meier and CoxPH fitting utilities. Includes small compatibility fallbacks for demo environments.
  - `theranostics/flow.py` — a Prefect flow (local) that orchestrates data generation and model training.
  - `scripts/run_demo.py` — run the demo locally.
- DICOM ingestion:
  - `theranostics/dicom_ingest.py` — minimal DICOM metadata extractor and `ingest_directory()` that writes metadata CSV.
  - `scripts/ingest_dicom.py` — CLI wrapper for directory ingestion.
  - `tests/test_dicom_ingest.py` — unit test that writes a minimal DICOM and validates ingestion.
- Tests and CI readiness:
  - `tests/test_simulate_and_models.py` — basic unit tests for synthetic generator and model functions.
  - `tests/test_dicom_ingest.py` — DICOM ingest test.
  - Quick local test run was executed and passing for the current environment (2 model tests + 1 DICOM test).

How to run locally
-------------------
1) Create & activate a venv and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2) Run unit tests:

```bash
PYTHONPATH=$(pwd) pytest -q
```

3) Run the demo (generate synthetic data and fit baseline models):

```bash
python scripts/run_demo.py
```

4) Ingest a directory of DICOM files (produces CSV):

```bash
python scripts/ingest_dicom.py /path/to/dicom_dir data/bronze/dicom_metadata.csv
```

Design & next steps
--------------------
Planned features to implement next (high value):

- Convert CSV metadata to Parquet and write into `data/bronze/` and `data/silver/` partitions (this will be added as a Prefect task).
- Add Prefect tasks and an orchestrated flow that:
  - pulls from PACS/DICOMweb or local DICOM directories,
  - performs de-identification,
  - stages to object storage (S3/minIO),
  - normalizes EHR/FHIR data to the structured schema,
  - runs NLP extraction on clinical notes.
- Add survival ML experiments: DeepSurv, survival forests, and explainability (SHAP) hooks.
- Add GitHub Actions to run tests and publish junit/coverage artifacts.
- Remove `.venv/` from repo (already untracked) and optionally purge it from history if desired.

Contact & ownership
--------------------
Repo owner: https://github.com/justin-mbca/theranostics
