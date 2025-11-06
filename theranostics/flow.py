"""Prefect flow to run data generation and model fitting."""
from __future__ import annotations

from prefect import flow, task
from .simulate import generate_cohort
from .models import fit_km, fit_cox


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


if __name__ == "__main__":
    out = pipeline_demo(200)
    print("Run complete. Keys:", list(out.keys()))
