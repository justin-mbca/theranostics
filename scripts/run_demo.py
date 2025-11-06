"""Run the local demo pipeline (no server required)."""
from theranostics.simulate import generate_cohort
from theranostics.models import fit_km, fit_cox


def main():
    df = generate_cohort(300)
    print("Cohort generated:", df.shape)
    km = fit_km(df)
    print("KM median survival:", km.median_survival_time_)
    cph, _ = fit_cox(df)
    print("Cox summary:\n", cph.summary)


if __name__ == "__main__":
    main()
