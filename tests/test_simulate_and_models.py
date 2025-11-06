import pandas as pd

from theranostics.simulate import generate_cohort
from theranostics.models import fit_km, fit_cox


def test_generate_cohort_basic():
    df = generate_cohort(50, seed=1)
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == 50
    assert set(["patient_id", "time", "event"]).issubset(df.columns)


def test_models_run():
    df = generate_cohort(200, seed=2)
    km = fit_km(df)
    assert km.event_observed.sum() >= 0
    cph, df2 = fit_cox(df)
    # summary should be a DataFrame with rows for coefficients
    assert hasattr(cph, "summary")
