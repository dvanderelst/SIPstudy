# Supplementary Materials

This document accompanies the manuscript *"Effects of a fixed-time food delivery on the behavior of domestic cats (Felis catus)"*. It contains the full statistical output for the analyses summarised in the Results section of the paper.

The supplement is organised in the same order as the paper:

1. Step counts
2. Activity patterns across the food-to-food interval
3. Space allocation (time near the feeder)
4. Water consumption

All tables in this supplement are regenerated from the raw data (`data/`) by running `SCRIPT_compile_stat_results.py`. The figures reproduced here are the same figures that appear in the main text.


# Step Counts

Daily step counts were recorded throughout the study using a Fitbit Zip on each cat's collar. To test whether FT food delivery altered step counts beyond intrinsic baseline variation, we fit a per-cat OLS regression of daily step count on day using baseline observations only, then compared the distribution of residuals from that fit against the residuals obtained by applying the same model to the FT-interval days. A Kolmogorov–Smirnov two-sample test was used to test whether the two distributions could be drawn from the same underlying distribution. Figure 2 (reproduced below) shows the raw daily step counts and the fitted baseline trend for each cat.

![Figure 2. Daily step counts across baseline and FT intervals.](../steps_output/steps.png)

## Baseline regression models

The tables below give the per-cat baseline OLS regressions of daily step count (in thousands) on day number, fit on baseline observations only. For each cat, the model is:

```
Steps ~ Days
```

The `Days` coefficient captures the intrinsic linear trend across the study period; the residuals from these fits are used in the Kolmogorov–Smirnov tests reported in the next subsection.

### Bernie

```
                            OLS Regression Results                            
==============================================================================
Dep. Variable:                  steps   R-squared:                       0.352
Model:                            OLS   Adj. R-squared:                  0.340
Method:                 Least Squares   F-statistic:                     30.41
Date:                Sat, 16 May 2026   Prob (F-statistic):           9.23e-07
Time:                        17:28:14   Log-Likelihood:                -120.19
No. Observations:                  58   AIC:                             244.4
Df Residuals:                      56   BIC:                             248.5
Df Model:                           1                                         
Covariance Type:            nonrobust                                         
==============================================================================
                 coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------
Intercept      4.7564      0.476     10.001      0.000       3.804       5.709
Days           0.0544      0.010      5.515      0.000       0.035       0.074
==============================================================================
Omnibus:                        0.593   Durbin-Watson:                   1.952
Prob(Omnibus):                  0.743   Jarque-Bera (JB):                0.664
Skew:                           0.223   Prob(JB):                        0.717
Kurtosis:                       2.724   Cond. No.                         89.2
==============================================================================

Notes:
[1] Standard Errors assume correct specification of covariance matrix.
```

### Citrine

```
                            OLS Regression Results                            
==============================================================================
Dep. Variable:                  steps   R-squared:                       0.072
Model:                            OLS   Adj. R-squared:                  0.054
Method:                 Least Squares   F-statistic:                     3.895
Date:                Sat, 16 May 2026   Prob (F-statistic):             0.0540
Time:                        17:28:14   Log-Likelihood:                -150.25
No. Observations:                  52   AIC:                             304.5
Df Residuals:                      50   BIC:                             308.4
Df Model:                           1                                         
Covariance Type:            nonrobust                                         
==============================================================================
                 coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------
Intercept     16.9085      1.161     14.557      0.000      14.576      19.241
Days          -0.0498      0.025     -1.973      0.054      -0.101       0.001
==============================================================================
Omnibus:                        0.695   Durbin-Watson:                   1.574
Prob(Omnibus):                  0.706   Jarque-Bera (JB):                0.522
Skew:                           0.242   Prob(JB):                        0.770
Kurtosis:                       2.922   Cond. No.                         86.9
==============================================================================

Notes:
[1] Standard Errors assume correct specification of covariance matrix.
```

### Elia

```
                            OLS Regression Results                            
==============================================================================
Dep. Variable:                  steps   R-squared:                       0.017
Model:                            OLS   Adj. R-squared:                  0.001
Method:                 Least Squares   F-statistic:                     1.054
Date:                Sat, 16 May 2026   Prob (F-statistic):              0.309
Time:                        17:28:14   Log-Likelihood:                -70.141
No. Observations:                  62   AIC:                             144.3
Df Residuals:                      60   BIC:                             148.5
Df Model:                           1                                         
Covariance Type:            nonrobust                                         
==============================================================================
                 coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------
Intercept      2.0513      0.179     11.491      0.000       1.694       2.408
Days           0.0035      0.003      1.027      0.309      -0.003       0.010
==============================================================================
Omnibus:                        1.439   Durbin-Watson:                   1.441
Prob(Omnibus):                  0.487   Jarque-Bera (JB):                0.955
Skew:                           0.297   Prob(JB):                        0.620
Kurtosis:                       3.133   Cond. No.                         95.2
==============================================================================

Notes:
[1] Standard Errors assume correct specification of covariance matrix.
```

### Minerva

```
                            OLS Regression Results                            
==============================================================================
Dep. Variable:                  steps   R-squared:                       0.001
Model:                            OLS   Adj. R-squared:                 -0.018
Method:                 Least Squares   F-statistic:                   0.04356
Date:                Sat, 16 May 2026   Prob (F-statistic):              0.835
Time:                        17:28:14   Log-Likelihood:                -76.059
No. Observations:                  54   AIC:                             156.1
Df Residuals:                      52   BIC:                             160.1
Df Model:                           1                                         
Covariance Type:            nonrobust                                         
==============================================================================
                 coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------
Intercept      2.8276      0.286      9.881      0.000       2.253       3.402
Days           0.0012      0.006      0.209      0.835      -0.010       0.012
==============================================================================
Omnibus:                        1.117   Durbin-Watson:                   1.136
Prob(Omnibus):                  0.572   Jarque-Bera (JB):                1.170
Skew:                          -0.292   Prob(JB):                        0.557
Kurtosis:                       2.578   Cond. No.                         106.
==============================================================================

Notes:
[1] Standard Errors assume correct specification of covariance matrix.
```

## Kolmogorov–Smirnov tests of FT vs. baseline residual distributions

Each row compares the distribution of residuals from the corresponding cat's baseline regression against the distribution of residuals obtained by applying that same baseline model to the FT interval named in the comparison column. A *p*-value below 0.001 indicates that the FT-interval residuals differ significantly from baseline residuals — i.e., that the intervention altered step counts beyond what would be expected from intrinsic baseline variation.

| Subject   | Comparison                | KS statistic   | p-value   |
|:----------|:--------------------------|:---------------|:----------|
| Bernie    | interval 60s vs Baseline  | ks = 0.283     | p = 0.763 |
| Bernie    | interval 120s vs Baseline | ks = 0.351     | p = 0.415 |
| Bernie    | interval 180s vs Baseline | ks = 0.497     | p = 0.147 |
| Bernie    | interval 240s vs Baseline | ks = 0.210     | p = 0.955 |
| Bernie    | interval 300s vs Baseline | ks = 0.645     | p = 0.023 |
| Citrine   | interval 60s vs Baseline  | ks = 0.500     | p = 0.563 |
| Citrine   | interval 120s vs Baseline | ks = 0.808     | p = 0.005 |
| Citrine   | interval 180s vs Baseline | ks = 0.519     | p = 0.119 |
| Citrine   | interval 240s vs Baseline | ks = 0.481     | p = 0.178 |
| Citrine   | interval 300s vs Baseline | ks = 0.246     | p = 0.884 |
| Elia      | interval 60s vs Baseline  | ks = 0.355     | p = 0.499 |
| Elia      | interval 120s vs Baseline | ks = 0.452     | p = 0.228 |
| Elia      | interval 180s vs Baseline | ks = 0.290     | p = 0.739 |
| Elia      | interval 240s vs Baseline | ks = 0.639     | p = 0.025 |
| Elia      | interval 300s vs Baseline | ks = 0.439     | p = 0.250 |
| Minerva   | interval 60s vs Baseline  | ks = 0.226     | p = 0.929 |
| Minerva   | interval 120s vs Baseline | ks = 0.296     | p = 0.728 |
| Minerva   | interval 180s vs Baseline | ks = 0.630     | p = 0.031 |
| Minerva   | interval 240s vs Baseline | ks = 0.389     | p = 0.396 |
| Minerva   | interval 300s vs Baseline | ks = 0.630     | p = 0.031 |


# Activity Patterns Across the Food-to-Food Interval

Activity was scored from video using a 15-second instantaneous time-sampling method; at each sample point the cat was classified as active (any movement or interaction) or inactive (resting or pausing). To assess how activity was allocated across each food-to-food interval, we fit two logistic regressions (`smf.logit`) per FT interval, pooling data across cats: one for the first two-thirds of the interval and one for the final third. Each model used `TimeSinceFeeding` and `C(Subject)` as predictors, and we tested whether the slope on `TimeSinceFeeding` differed significantly from zero. For the 60s interval, which contains only four sample points, the two-thirds split falls between the second and third points, so the two segments are effectively halves rather than thirds. Figure 3 (reproduced below) shows the average proportion of intervals marked as active across the food-to-food interval.

![Figure 3. Average proportion of intervals marked as active across the food-to-food interval.](../behavior_output/activity.png)

## Logistic models per FT interval (first 2/3 and final 1/3)

For each FT interval below, the first table gives the logit fit for the first segment and the second table for the final segment. A positive slope on `TimeSinceFeeding` indicates that the probability of being active rises across the segment; a negative slope indicates it falls. The `p`-value on the `TimeSinceFeeding` row tests whether the slope differs significantly from zero.

### 60s interval

**First segment (first 2/3 of interval):**

```
                           Logit Regression Results                           
==============================================================================
Dep. Variable:                 Active   No. Observations:                  488
Model:                          Logit   Df Residuals:                      484
Method:                           MLE   Df Model:                            3
Date:                Sat, 16 May 2026   Pseudo R-squ.:                 0.04769
Time:                        17:28:14   Log-Likelihood:                -288.26
converged:                       True   LL-Null:                       -302.69
Covariance Type:            nonrobust   LLR p-value:                 2.387e-06
=====================================================================================
                        coef    std err          z      P>|z|      [0.025      0.975]
-------------------------------------------------------------------------------------
Intercept             0.4877      0.351      1.390      0.164      -0.200       1.175
Subject = Elia       -1.1217      0.247     -4.533      0.000      -1.607      -0.637
Subject = Minerva    -1.0771      0.248     -4.341      0.000      -1.563      -0.591
TimeSinceFeeding     -0.0231      0.013     -1.708      0.088      -0.050       0.003
=====================================================================================
```

**Second segment (final 1/3 of interval):**

```
                           Logit Regression Results                           
==============================================================================
Dep. Variable:                 Active   No. Observations:                  487
Model:                          Logit   Df Residuals:                      483
Method:                           MLE   Df Model:                            3
Date:                Sat, 16 May 2026   Pseudo R-squ.:                 0.03339
Time:                        17:28:14   Log-Likelihood:                -303.90
converged:                       True   LL-Null:                       -314.40
Covariance Type:            nonrobust   LLR p-value:                 0.0001056
=====================================================================================
                        coef    std err          z      P>|z|      [0.025      0.975]
-------------------------------------------------------------------------------------
Intercept            -2.6132      0.714     -3.660      0.000      -4.012      -1.214
Subject = Elia       -0.5354      0.241     -2.219      0.026      -1.008      -0.063
Subject = Minerva    -0.7026      0.245     -2.864      0.004      -1.183      -0.222
TimeSinceFeeding      0.0458      0.013      3.498      0.000       0.020       0.071
=====================================================================================
```

### 120s interval

**First segment (first 2/3 of interval):**

```
                           Logit Regression Results                           
==============================================================================
Dep. Variable:                 Active   No. Observations:                  551
Model:                          Logit   Df Residuals:                      546
Method:                           MLE   Df Model:                            4
Date:                Sat, 16 May 2026   Pseudo R-squ.:                  0.1328
Time:                        17:28:14   Log-Likelihood:                -312.03
converged:                       True   LL-Null:                       -359.83
Covariance Type:            nonrobust   LLR p-value:                 8.516e-20
=====================================================================================
                        coef    std err          z      P>|z|      [0.025      0.975]
-------------------------------------------------------------------------------------
Intercept             0.6358      0.275      2.313      0.021       0.097       1.175
Subject = Citrine    -1.3530      0.268     -5.052      0.000      -1.878      -0.828
Subject = Elia       -2.0174      0.252     -8.020      0.000      -2.510      -1.524
Subject = Minerva    -2.2682      0.305     -7.438      0.000      -2.866      -1.670
TimeSinceFeeding      0.0027      0.005      0.575      0.566      -0.006       0.012
=====================================================================================
```

**Second segment (final 1/3 of interval):**

```
                           Logit Regression Results                           
==============================================================================
Dep. Variable:                 Active   No. Observations:                  324
Model:                          Logit   Df Residuals:                      319
Method:                           MLE   Df Model:                            4
Date:                Sat, 16 May 2026   Pseudo R-squ.:                  0.1456
Time:                        17:28:14   Log-Likelihood:                -187.73
converged:                       True   LL-Null:                       -219.72
Covariance Type:            nonrobust   LLR p-value:                 4.252e-13
=====================================================================================
                        coef    std err          z      P>|z|      [0.025      0.975]
-------------------------------------------------------------------------------------
Intercept            -6.8073      1.153     -5.904      0.000      -9.067      -4.547
Subject = Citrine    -1.2505      0.379     -3.303      0.001      -1.993      -0.508
Subject = Elia       -1.3703      0.333     -4.118      0.000      -2.022      -0.718
Subject = Minerva    -0.5576      0.362     -1.540      0.124      -1.267       0.152
TimeSinceFeeding      0.0683      0.011      6.298      0.000       0.047       0.090
=====================================================================================
```

### 180s interval

**First segment (first 2/3 of interval):**

```
                           Logit Regression Results                           
==============================================================================
Dep. Variable:                 Active   No. Observations:                  471
Model:                          Logit   Df Residuals:                      466
Method:                           MLE   Df Model:                            4
Date:                Sat, 16 May 2026   Pseudo R-squ.:                  0.1733
Time:                        17:28:14   Log-Likelihood:                -239.05
converged:                       True   LL-Null:                       -289.14
Covariance Type:            nonrobust   LLR p-value:                 8.938e-21
=====================================================================================
                        coef    std err          z      P>|z|      [0.025      0.975]
-------------------------------------------------------------------------------------
Intercept             1.3888      0.304      4.575      0.000       0.794       1.984
Subject = Citrine    -1.1504      0.304     -3.781      0.000      -1.747      -0.554
Subject = Elia       -2.1627      0.317     -6.814      0.000      -2.785      -1.541
Subject = Minerva    -2.2866      0.328     -6.972      0.000      -2.929      -1.644
TimeSinceFeeding     -0.0160      0.003     -4.637      0.000      -0.023      -0.009
=====================================================================================
```

**Second segment (final 1/3 of interval):**

```
                           Logit Regression Results                           
==============================================================================
Dep. Variable:                 Active   No. Observations:                  229
Model:                          Logit   Df Residuals:                      224
Method:                           MLE   Df Model:                            4
Date:                Sat, 16 May 2026   Pseudo R-squ.:                  0.1054
Time:                        17:28:14   Log-Likelihood:                -136.87
converged:                       True   LL-Null:                       -153.00
Covariance Type:            nonrobust   LLR p-value:                 1.691e-06
=====================================================================================
                        coef    std err          z      P>|z|      [0.025      0.975]
-------------------------------------------------------------------------------------
Intercept            -6.4208      1.431     -4.488      0.000      -9.225      -3.617
Subject = Citrine    -1.0766      0.442     -2.433      0.015      -1.944      -0.209
Subject = Elia       -0.9195      0.384     -2.392      0.017      -1.673      -0.166
Subject = Minerva    -0.8926      0.390     -2.290      0.022      -1.656      -0.129
TimeSinceFeeding      0.0416      0.009      4.627      0.000       0.024       0.059
=====================================================================================
```

### 240s interval

**First segment (first 2/3 of interval):**

```
                           Logit Regression Results                           
==============================================================================
Dep. Variable:                 Active   No. Observations:                  531
Model:                          Logit   Df Residuals:                      526
Method:                           MLE   Df Model:                            4
Date:                Sat, 16 May 2026   Pseudo R-squ.:                  0.1936
Time:                        17:28:14   Log-Likelihood:                -225.81
converged:                       True   LL-Null:                       -280.02
Covariance Type:            nonrobust   LLR p-value:                 1.589e-22
=====================================================================================
                        coef    std err          z      P>|z|      [0.025      0.975]
-------------------------------------------------------------------------------------
Intercept             0.6110      0.278      2.199      0.028       0.066       1.156
Subject = Citrine    -2.4003      0.373     -6.436      0.000      -3.131      -1.669
Subject = Elia       -1.4499      0.268     -5.404      0.000      -1.976      -0.924
Subject = Minerva    -3.1442      0.488     -6.437      0.000      -4.102      -2.187
TimeSinceFeeding     -0.0076      0.003     -2.756      0.006      -0.013      -0.002
=====================================================================================
```

**Second segment (final 1/3 of interval):**

```
                           Logit Regression Results                           
==============================================================================
Dep. Variable:                 Active   No. Observations:                  280
Model:                          Logit   Df Residuals:                      275
Method:                           MLE   Df Model:                            4
Date:                Sat, 16 May 2026   Pseudo R-squ.:                  0.1746
Time:                        17:28:14   Log-Likelihood:                -150.62
converged:                       True   LL-Null:                       -182.49
Covariance Type:            nonrobust   LLR p-value:                 4.746e-13
=====================================================================================
                        coef    std err          z      P>|z|      [0.025      0.975]
-------------------------------------------------------------------------------------
Intercept            -4.8439      1.168     -4.148      0.000      -7.133      -2.555
Subject = Citrine    -1.0072      0.363     -2.776      0.006      -1.718      -0.296
Subject = Elia       -2.2305      0.402     -5.548      0.000      -3.019      -1.443
Subject = Minerva    -1.9570      0.419     -4.675      0.000      -2.777      -1.137
TimeSinceFeeding      0.0261      0.006      4.576      0.000       0.015       0.037
=====================================================================================
```

### 300s interval

**First segment (first 2/3 of interval):**

```
                           Logit Regression Results                           
==============================================================================
Dep. Variable:                 Active   No. Observations:                  536
Model:                          Logit   Df Residuals:                      531
Method:                           MLE   Df Model:                            4
Date:                Sat, 16 May 2026   Pseudo R-squ.:                 0.09096
Time:                        17:28:14   Log-Likelihood:                -315.13
converged:                       True   LL-Null:                       -346.66
Covariance Type:            nonrobust   LLR p-value:                 6.586e-13
=====================================================================================
                        coef    std err          z      P>|z|      [0.025      0.975]
-------------------------------------------------------------------------------------
Intercept             0.8772      0.248      3.533      0.000       0.391       1.364
Subject = Citrine    -0.4818      0.263     -1.831      0.067      -0.998       0.034
Subject = Elia       -0.5221      0.242     -2.161      0.031      -0.996      -0.048
Subject = Minerva    -1.6867      0.312     -5.398      0.000      -2.299      -1.074
TimeSinceFeeding     -0.0094      0.002     -5.316      0.000      -0.013      -0.006
=====================================================================================
```

**Second segment (final 1/3 of interval):**

```
                           Logit Regression Results                           
==============================================================================
Dep. Variable:                 Active   No. Observations:                  283
Model:                          Logit   Df Residuals:                      278
Method:                           MLE   Df Model:                            4
Date:                Sat, 16 May 2026   Pseudo R-squ.:                  0.1142
Time:                        17:28:14   Log-Likelihood:                -162.82
converged:                       True   LL-Null:                       -183.81
Covariance Type:            nonrobust   LLR p-value:                 1.690e-08
=====================================================================================
                        coef    std err          z      P>|z|      [0.025      0.975]
-------------------------------------------------------------------------------------
Intercept            -5.2401      1.198     -4.375      0.000      -7.588      -2.892
Subject = Citrine    -0.9090      0.372     -2.442      0.015      -1.638      -0.179
Subject = Elia       -0.7684      0.342     -2.249      0.025      -1.438      -0.099
Subject = Minerva    -1.8594      0.435     -4.279      0.000      -2.711      -1.008
TimeSinceFeeding      0.0210      0.005      4.524      0.000       0.012       0.030
=====================================================================================
```


# Space Allocation (Time in Feeder Area)

<!-- TODO: 2–3 sentence intro: logistic GLM predicting AtFeeder (Zones 5 & 6) from C(Subject) + C(Feeder_Interval, baseline as reference) + TimeSinceFeeding; second model using interval length as a continuous predictor (intervention data only) to test for systematic change across interval lengths; same two-thirds vs. final-third piecewise analysis as for activity, but for the AtFeeder outcome -->

![Figure 4. Average proportion of intervals spent in the feeder area.](../behavior_output/location.png)

## Effect of FT interval (categorical, baseline as reference)

<!-- INSERT: location_baseline_vs_experimental -->

## Effect of interval length on time at feeder (continuous, intervention only)

<!-- INSERT: location_interval_model -->

## Logistic models per FT interval (first 2/3 and final 1/3)

<!-- INSERT: location_models -->


# Water Consumption

<!-- TODO: 2–3 sentence intro: same residual-comparison approach as for step counts; baseline OLS regression of in-session water consumption (ml) on day, fitted per cat; per-interval residuals compared against baseline residuals via KS test; alpha level 0.001; note phase-1 dependent variable = "session" (in-session consumption); see AnalysisDrink for phase definitions and Citrine/Elia date cutoffs -->

![Figure 5. Daily water consumption across baseline and FT intervals.](../drinking_output/phase_1_session.png)

## Baseline regression models (phase 1, in-session consumption)

<!-- INSERT: drinking_regressions -->

## Kolmogorov–Smirnov tests of FT vs. baseline residual distributions

<!-- INSERT: drinking_ks_table -->
