"""Synthetic cohort generator for survival modeling."""
from __future__ import annotations

import numpy as np
import pandas as pd
from typing import Tuple


def generate_cohort(n: int = 500, seed: int = 42) -> pd.DataFrame:
    """Generate a synthetic cohort with clinical features and time-to-event labels.

    Columns:
    - patient_id
    - age
    - sex (0=F,1=M)
    - tumor_stage (I-IV)
    - biomarker (continuous)
    - treatment_group (A/B)
    - time: time-to-event or censoring in days
    - event: 1=event,0=censored
    """
    rng = np.random.default_rng(seed)
    patient_id = [f"P{idx:05d}" for idx in range(1, n + 1)]
    age = rng.normal(62, 10, size=n).clip(18, 90).astype(int)
    sex = rng.integers(0, 2, size=n)
    tumor_stage = rng.choice([1, 2, 3, 4], size=n, p=[0.25, 0.35, 0.25, 0.15])
    biomarker = rng.normal(0.0, 1.0, size=n)
    treatment_group = rng.choice(["A", "B"], size=n, p=[0.5, 0.5])

    # Simulate baseline hazard influenced by stage, biomarker, and treatment
    base_hazard = 0.001
    stage_coef = {1: 0.5, 2: 1.0, 3: 1.7, 4: 2.5}
    treatment_coef = {"A": 1.0, "B": 0.8}

    linear = np.array([stage_coef[s] for s in tumor_stage])
    linear += biomarker * 0.3
    linear *= np.array([treatment_coef[t] for t in treatment_group])

    # Weibull-like survival times
    u = rng.random(n)
    # scale parameter shorter with higher linear predictor
    scale = 365 * np.exp(-0.3 * linear)
    times = -scale * np.log(u)

    # administrative censoring at 3 years
    censor_time = 365 * 3
    observed_time = np.minimum(times, censor_time)
    event = (times <= censor_time).astype(int)

    df = pd.DataFrame(
        {
            "patient_id": patient_id,
            "age": age,
            "sex": sex,
            "tumor_stage": tumor_stage,
            "biomarker": biomarker,
            "treatment_group": treatment_group,
            "time": observed_time.astype(float),
            "event": event,
        }
    )
    return df


if __name__ == "__main__":
    df = generate_cohort(10)
    print(df.head())
