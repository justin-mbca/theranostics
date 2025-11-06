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

Notes
- This is a small local prototype. For production use the architecture in the design doc: object storage, feature store, secured FHIR/DICOM connectors, and managed model infra.
