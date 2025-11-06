![CI](https://github.com/justin-mbca/theranostics/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/justin-mbca/theranostics/branch/main/graph/badge.svg?token=CODECOV_TOKEN)](https://codecov.io/gh/justin-mbca/theranostics)


Theranostics - Local prototype

This repository contains a minimal local prototype for the Biomedical Data Scientist pipeline.

What it does
- Generates a synthetic cohort (clinical features + time-to-event labels).
- Runs a Prefect flow that writes the dataset and fits baseline survival models (Kaplan-Meier, CoxPH).

Quickstart (macOS / bash)

1) Create a venv and install requirements

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2) Run the demo

```bash
python scripts/run_demo.py
```

3) Run tests

```bash
pytest -q
```

Run the Prefect demo (local):

```bash
# ensure venv activated
python -m pip install -r requirements.txt
python -c "from theranostics.flow import pipeline_with_dicom; pipeline_with_dicom(dicom_dir='path/to/dicom', out_parquet='data/bronze/dicom.parquet')"
```

Coverage report (locally):

```bash
pytest --cov=theranostics --cov-report=xml:coverage.xml
```

Notes
- This is a small local prototype. For production use the architecture in the design doc: object storage, feature store, secured FHIR/DICOM connectors, and managed model infra.
