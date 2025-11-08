"""Simple experiments helper with optional MLflow logging.

This module provides a tiny `run_experiment` function that:
- Accepts a DataFrame or generates synthetic data when None.
- Fits baseline survival models (calls existing `models.fit_km` and `models.fit_cox`).
- Logs params/metrics/artifacts to MLflow if available; otherwise saves artifacts to `artifacts/`.

Designed to be minimal and safe in CI (MLflow is optional).
"""
from __future__ import annotations

import os
import json
import tempfile
from typing import Optional, Dict, Any

import pandas as pd

try:
    import mlflow
    MLFLOW_AVAILABLE = True
except Exception:
    mlflow = None
    MLFLOW_AVAILABLE = False

from .simulate import generate_cohort
from .models import fit_km, fit_cox


def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def _save_artifact(obj: Any, path: str) -> None:
    _ensure_dir(os.path.dirname(path))
    if isinstance(obj, pd.DataFrame):
        obj.to_csv(path, index=False)
    else:
        with open(path, "w") as f:
            json.dump(obj, f, default=str)


def run_experiment(
    df: Optional[pd.DataFrame] = None,
    params: Optional[Dict[str, Any]] = None,
    artifacts_dir: str = "artifacts/experiments",
    mlflow_experiment_name: str = "theranostics_local",
) -> Dict[str, Any]:
    """Run a minimal experiment: fit KM and Cox, log metrics and artifacts.

    Returns a dictionary with keys: metrics, artifacts, params.
    """
    params = params or {}
    if df is None:
        n = int(params.get("n", 200))
        censor_rate = float(params.get("censor_rate", 0.0))
        biomarker_effect = float(params.get("biomarker_effect", 0.3))
        df = generate_cohort(n=n, censor_rate=censor_rate, biomarker_effect=biomarker_effect)

    # Fit models
    km = fit_km(df)
    cph, df2 = fit_cox(df)

    results = {"metrics": {}, "artifacts": {}, "params": params}

    # Collect simple metrics
    try:
        # KM: median survival estimate (if available)
        median = float(km.median_survival_time_)
        results["metrics"]["km_median_survival"] = median
    except Exception:
        results["metrics"]["km_median_survival"] = None

    try:
        # Cox: concordance or summary
        if hasattr(cph, "concordance_index_"):
            results["metrics"]["cox_concordance"] = float(cph.concordance_index_)
    except Exception:
        results["metrics"]["cox_concordance"] = None

    # Prepare artifacts
    _ensure_dir(artifacts_dir)
    km_path = os.path.join(artifacts_dir, "km_survival_table.csv")
    try:
        # lifelines KM has survival_function_ attribute
        if hasattr(km, "survival_function_"):
            sf = km.survival_function_
            sf.to_csv(km_path)
            results["artifacts"]["km_survival_table"] = km_path
    except Exception:
        pass

    cox_summary_path = os.path.join(artifacts_dir, "cox_summary.json")
    try:
        # lifelines CoxPHFitter has summary_ dataframe
        if hasattr(cph, "summary"):
            s = cph.summary
            s.to_csv(os.path.join(artifacts_dir, "cox_summary.csv"))
            results["artifacts"]["cox_summary_csv"] = os.path.join(artifacts_dir, "cox_summary.csv")
            # also save json
            s_json = s.to_dict(orient="index")
            _save_artifact(s_json, cox_summary_path)
            results["artifacts"]["cox_summary_json"] = cox_summary_path
    except Exception:
        pass

    # Save the processed dataframe used for Cox
    df2_path = os.path.join(artifacts_dir, "cox_input.csv")
    try:
        df2.to_csv(df2_path, index=False)
        results["artifacts"]["cox_input_csv"] = df2_path
    except Exception:
        pass

    # MLflow logging (optional)
    if MLFLOW_AVAILABLE:
        try:
            mlflow.set_experiment(mlflow_experiment_name)
            with mlflow.start_run() as run:
                mlflow.log_params(params)
                for k, v in results["metrics"].items():
                    if v is not None:
                        mlflow.log_metric(k, float(v))
                # Log artifacts
                for name, path in results["artifacts"].items():
                    if os.path.exists(path):
                        mlflow.log_artifact(path, artifact_path="artifacts")
                # Return run id
                results["mlflow_run_id"] = run.info.run_id
                # Print a local UI URL for convenience (works for local runs)
                try:
                    tracking_uri = mlflow.get_tracking_uri()
                    if tracking_uri.startswith("file://") or tracking_uri == "mlruns":
                        # local file store
                        run_dir = os.path.join(tracking_uri.replace("file://", ""), "", str(run.info.run_id))
                        print(f"MLflow run recorded locally. Run id: {run.info.run_id}")
                        print(f"Open MLflow UI and look for experiment '{mlflow_experiment_name}' or run id {run.info.run_id}")
                except Exception:
                    pass
        except Exception:
            # If MLflow logging fails, continue but note it
            results["mlflow_error"] = "failed_to_log"

    # Always write a minimal summary into mlruns/ for easy inspection even without MLflow
    try:
        summary_dir = os.path.join("mlruns", mlflow_experiment_name)
        _ensure_dir(summary_dir)
        summary_path = os.path.join(summary_dir, f"summary_{os.getpid()}_{int(os.times()[-1])}.txt")
        with open(summary_path, "w") as f:
            f.write("params:\n")
            f.write(json.dumps(params, indent=2))
            f.write("\nmetrics:\n")
            f.write(json.dumps(results.get("metrics", {}), indent=2))
            f.write("\nartifacts:\n")
            f.write(json.dumps(results.get("artifacts", {}), indent=2))
        results["summary_path"] = summary_path
    except Exception:
        # don't fail experiments if summary can't be written
        pass

    return results
