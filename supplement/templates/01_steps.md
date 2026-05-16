# Step Counts

Daily step counts were recorded throughout the study using a Fitbit Zip on each cat's collar. To test whether FT food delivery altered step counts beyond intrinsic baseline variation, we fit a per-cat OLS regression of daily step count on day using baseline observations only, then compared the distribution of residuals from that fit against the residuals obtained by applying the same model to the FT-interval days. A Kolmogorov–Smirnov two-sample test was used to test whether the two distributions could be drawn from the same underlying distribution. Figure 2 (reproduced below) shows the raw daily step counts and the fitted baseline trend for each cat.

![Figure 2. Daily step counts across baseline and FT intervals.](../steps_output/steps.png)

## Baseline regression models

The tables below give the per-cat baseline OLS regressions of daily step count (in thousands) on day number, fit on baseline observations only. For each cat, the model is:

```
<!-- INSERT: steps_formula -->
```

The `Days` coefficient captures the intrinsic linear trend across the study period; the residuals from these fits are used in the Kolmogorov–Smirnov tests reported in the next subsection.

<!-- INSERT: steps_regressions -->

## Kolmogorov–Smirnov tests of FT vs. baseline residual distributions

Each row compares the distribution of residuals from the corresponding cat's baseline regression against the distribution of residuals obtained by applying that same baseline model to the FT interval named in the comparison column. A *p*-value below 0.001 indicates that the FT-interval residuals differ significantly from baseline residuals — i.e., that the intervention altered step counts beyond what would be expected from intrinsic baseline variation.

<!-- INSERT: steps_ks_table -->
