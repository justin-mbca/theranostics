Title: feat: grid-sweep artifacts, report, and CI smoke test

## Summary

This PR adds artifacts and reporting from a 3x3 grid sweep of the theranostics experiment runner (varying `censor_rate` and `biomarker_effect`). It also adds a short report and a small CI smoke job to catch lifelines/pandas/scipy incompatibilities early.

Files of note in this branch:

- `artifacts/experiments/grid_sweep_results.csv` — full numeric results and run metadata
- `artifacts/experiments/grid_coef.png`, `artifacts/experiments/grid_pvalues.png` — heatmaps
- `reports/grid_sweep_report.md` — quick human-readable report and reproduction steps
- `.github/workflows/ci.yml` — added `smoke-lifelines` job which runs a minimal CoxPHFitter check
- `theranostics/_compat.py` — small runtime compatibility shim loaded on import to work around pandas/lifelines/scipy mismatches during local development

## Why

- The grid-sweep artifacts demonstrate the pipeline end-to-end (data generation, modeling, artifacts). The report makes the results easy to review.
- The smoke CI job fails fast on dependency incompatibilities and provides quick feedback to maintainers.
- The compat shim is a small, documented developer convenience to stabilize the local dev experience while we decide on a final pinned dependency set.

## How to review

1. Inspect `reports/grid_sweep_report.md` for the overview and quick results.
2. Browse `artifacts/experiments/` for the full CSV and figures.
3. Run the smoke test locally:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python - <<'PY'
from theranostics.simulate import generate_cohort
from lifelines import CoxPHFitter
df = generate_cohort(n=200, seed=42, censor_rate=0.2, biomarker_effect=1.0)
df2 = df[['time','event','biomarker','age']]
print('Running tiny Cox fit...')
from lifelines import CoxPHFitter
cph = CoxPHFitter()
cph.fit(df2, duration_col='time', event_col='event')
print(cph.summary.loc['biomarker', ['coef','p']])
PY
```

## Notes & next steps

- Recommend selecting and pinning a final dependency matrix and removing `theranostics/_compat.py` once CI confirms the matrix.
- Optionally convert the smoke job into a pytest-based smoke test so it appears in `pytest` reports and JUnit artifacts.

---
Generated PR description. Paste into the GitHub PR body when creating the pull request for `feat/grid-sweep-artifacts`.
