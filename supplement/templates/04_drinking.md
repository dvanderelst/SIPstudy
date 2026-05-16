# Water Consumption

Water consumption was recorded during each experimental session (the period during which food was delivered on intervention days, or an equivalent fixed window on baseline days). The analysis reported here uses the in-session column (`session` in `data/SIP_data.csv`); a separate continuation period for Citrine and Elia ("phase 2") is computed by `AnalysisDrink.read_data` but not used in the paper. To test whether FT food delivery altered in-session water consumption beyond intrinsic baseline variation, we fit a per-cat OLS regression of session water consumption (ml) on day using baseline observations only, then compared the distribution of residuals from that fit against the residuals obtained by applying the same model to the FT-interval days. A Kolmogorov–Smirnov two-sample test was used to test whether the two distributions could be drawn from the same underlying distribution. Figure 5 (reproduced below) shows the raw daily session consumption and the fitted baseline trend for each cat.

![Figure 5. Daily in-session water consumption across baseline and FT intervals.](../drinking_output/phase_1_session.png)

## Baseline regression models (phase 1, in-session consumption)

The tables below give the per-cat baseline OLS regressions of in-session water consumption (ml) on day number, fit on baseline observations only. The model is:

```
<!-- INSERT: drinking_formula -->
```

The `Days` coefficient captures the intrinsic linear trend across the study period; the residuals from these fits are used in the Kolmogorov–Smirnov tests reported in the next subsection.

<!-- INSERT: drinking_regressions -->

## Kolmogorov–Smirnov tests of FT vs. baseline residual distributions

Each row compares the distribution of residuals from the corresponding cat's baseline regression against the distribution of residuals obtained by applying that same baseline model to the FT interval named in the comparison column. A *p*-value below 0.001 indicates that the FT-interval residuals differ significantly from baseline residuals — i.e., that the intervention altered in-session water consumption beyond what would be expected from intrinsic baseline variation.

<!-- INSERT: drinking_ks_table -->
