# Results explanation and how to interpret outputs

This short guide explains the primary outputs produced by the experiments and how to interpret them.

Primary artifacts
- `cox_summary.csv` / `cox_summary.json`: coefficient estimates, standard errors, Wald z-statistics, and p-values from a Cox proportional hazards model fit (via `lifelines.CoxPHFitter`). Key fields:
  - `coef`: estimated log-hazard ratio for the covariate.
  - `exp(coef)`: hazard ratio (HR) — values >1 indicate higher hazard per unit increase.
  - `se(coef)`: standard error of the coefficient.
  - `z` / `p`: statistic and p-value for testing coef != 0.

- `km_survival_table.csv`: Kaplan–Meier survival table (time, at-risk count, events, survival probability).
- `km_overall.png`, `km_by_treatment.png`: Kaplan–Meier plots (overall and stratified by treatment group) visualizing survival curves and censoring.

How to read results (practical)
- Effect size: `exp(coef)` from the Cox model quantifies the multiplicative change in hazard for a one-unit change in the covariate. For continuous `biomarker`, HR >1 indicates higher biomarker values are associated with increased hazard (worse outcome).
- Statistical significance: p-values assess evidence against a zero effect. Small p (<0.05) suggests an association; interpret along with effect size and sample size.
- Concordance: the Cox concordance (reported in run metrics) indicates model discrimination (0.5 = random, 1.0 = perfect).
- KM plots: check separation between curves and number at risk; with heavy censoring the effective sample size reduces and uncertainty grows.

Grid-sweep-specific notes
- The grid sweep varied `censor_rate` and `biomarker_effect`. Expect:
  - Increasing `biomarker_effect` raises estimated `coef` and improves concordance.
  - Increasing `censor_rate` reduces `event_rate` and can reduce effective power, widening CIs and inflating p-values.

Limitations
- Synthetic data is a simplified model and may not reflect real-world confounding, measurement error, or selection biases.
- Cox proportional hazards assumptions (proportionality over time) are not exhaustively checked in the prototype; add Schoenfeld residual tests for production analyses.

Recommended next steps for analysis
- Add confidence intervals and bootstrap runs across random seeds to report variability.
- Test proportional hazards assumptions and consider time-varying effects if violated.
- For real data ingestion, harmonize DICOM-derived features and clinical covariates; perform covariate selection and regularization where appropriate.
