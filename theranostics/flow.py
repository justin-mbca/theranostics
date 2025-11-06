"""Prefect flow to run data generation and model fitting."""
from __future__ import annotations

from prefect import flow, task
from .simulate import generate_cohort
from .models import fit_km, fit_cox
from theranostics.dicom_ingest import ingest_directory


@task
def make_data(n: int = 500):
    df = generate_cohort(n=n)
    return df


@task
def train_models(df):
    km = fit_km(df)
    cph, df2 = fit_cox(df)
    return {
        "km_survival_function": km.survival_function_.to_dict(),
        "cox_summary": cph.summary,
    }


@flow
def pipeline_demo(n: int = 500):
    df = make_data(n)
    results = train_models(df)
    return results


@task
def dicom_ingest_task(dicom_dir: str, out_parquet: str):
    # use ingest_directory with to_parquet=True to write a parquet artifact
    return ingest_directory(dicom_dir, out_parquet, to_parquet=True)


@flow
def pipeline_with_dicom(n: int = 500, dicom_dir: str = None, out_parquet: str = 'data/bronze/dicom.parquet'):
    """Run the demo pipeline and optionally ingest DICOMs.

    Returns a dict with model results. If `dicom_dir` is provided the dict
    will include the numeric key `dicom_count` (int) indicating how many
    DICOM files were processed and written to `out_parquet`.
    """

    df = make_data(n)
    results = train_models(df)
    if dicom_dir:
        # Call the task synchronously so the flow returns the numeric count
        dicom_count = dicom_ingest_task(dicom_dir, out_parquet)
        return {**results, 'dicom_count': dicom_count}
    return results


if __name__ == "__main__":
    out = pipeline_demo(200)
    print("Run complete. Keys:", list(out.keys()))
