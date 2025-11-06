Experiments notebook

This folder contains `experiments.ipynb`, a minimal example that runs a synthetic survival experiment and writes artifacts and a small run summary.

Quick references

- Executed notebook (if present): `out/experiments_executed.ipynb`
- Artifacts: `artifacts/experiments/` (CSV/JSON)
- Summary files: `mlruns/<experiment_name>/summary_<pid>_<ts>.txt` (written by `theranostics.experiments.run_experiment`)

Run locally (interactive)

1. Activate your Python environment.
2. From repo root run:

```bash
jupyter notebook notebooks/experiments.ipynb
```

Run headless (CI-style)

```bash
# run with papermill, injecting n=20
papermill notebooks/experiments.ipynb out/experiments_executed.ipynb -p n 20
```

MLflow UI (optional)

```bash
pip install mlflow
mlflow ui --port 5000
# open http://localhost:5000 to view runs
```

Notes

- The notebook inserts the repo root onto `sys.path` to make local imports work when executed directly.
- The `run_experiment` helper writes a small summary file into `mlruns/` for quick inspection even if MLflow is not installed.
