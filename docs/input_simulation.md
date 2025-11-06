# Input data simulation

This document explains how the synthetic cohort is generated in `theranostics.simulate.generate_cohort` and which parameters control the simulation.

Key parameters
- `n` (int): number of patients simulated (default 500).
- `seed` (int): random seed for reproducibility.
- `censor_rate` (float 0.0-1.0): fraction of subjects to apply additional random censoring.
- `biomarker_effect` (float): multiplicative effect of the continuous `biomarker` on the linear predictor (larger values increase hazard association strength).

Generated columns (DataFrame schema)
- `patient_id` (str): unique identifier P00001...
- `age` (int): simulated age (clipped to 18-90).
- `sex` (int): 0 = F, 1 = M.
- `tumor_stage` (int): 1-4.
- `biomarker` (float): standard-normal continuous biomarker.
- `treatment_group` (str): 'A' or 'B'.
- `time` (float): observed follow-up time in days (event or censoring).
- `event` (int): 1 if event occurred, 0 if censored.

Simulation model (short)
- Baseline hazard is modulated by discrete `tumor_stage` and `treatment_group` coefficients.
- A linear predictor is constructed: stage_coef + biomarker * `biomarker_effect`; treatment scales the predictor.
- Survival times are drawn from a Weibull-like construction using an exponential transform of a uniform random variable and a scale parameter shortened by higher linear predictor.
- Administrative censoring at 3 years (365*3 days) is applied. If `censor_rate` > 0, a random fraction of subjects receive an earlier random censoring time.

Reproducibility
- Use `seed` to reproduce runs. The experiment runner writes `mlruns/theranostics_local/summary_*.txt` files linking parameters and artifacts for each run.

Where to change behavior
- `theranostics.simulate.generate_cohort` contains the above logic. Adjust `stage_coef`, `treatment_coef`, or the scale formula to reflect alternative hazard models.
