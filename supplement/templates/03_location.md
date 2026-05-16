# Location (Time in Feeder Area)

At each 15-second sample point the cat's location was scored using a six-zone system covering the run, plus several non-zone categories (Shelf, Fence, Litter Box, Out of View; see `Library/AnalysisBehavior.read_data` for the full mapping). For analysis the location was collapsed into a binary `AtFeeder` outcome — Feeder Area vs. Non-Feeder; the exact zone-to-category mapping is in the `loc_cat` lambda of `read_data`. Three logistic models were fit on this outcome to characterise how proximity to the feeder varied across baseline and the FT conditions.

Figure 4 (reproduced below) shows the average proportion of intervals spent in the feeder area across the food-to-food interval. Open circles mark data points in the first two-thirds of each interval, and filled circles mark those in the final one-third, corresponding to the two segments fit by the piecewise models below.

![Figure 4. Average proportion of intervals spent in the feeder area.](../behavior_output/location.png)

## Effect of FT interval (categorical, baseline as reference)

A logistic regression was fit on all observations (baseline plus all five FT intervals), pooling data across cats. FT interval was encoded as a categorical predictor with baseline as the reference level; subject was included as a fixed effect. The model is:

```
<!-- INSERT: location_baseline_vs_experimental_formula -->
```

Each `Feeder_Interval = N` coefficient tests whether time in the feeder area during that interval differs significantly from baseline.

<!-- INSERT: location_baseline_vs_experimental -->

## Effect of interval length on time at feeder (continuous, intervention only)

A second logistic regression was fit on the intervention observations only (baseline excluded), treating FT interval length as a continuous predictor. This tests whether longer FT intervals are associated with systematically more or less time in the feeder area. The model is:

```
<!-- INSERT: location_interval_model_formula -->
```

A significant negative slope on `Feeder_Interval` indicates that as interval length increases, cats spend less time near the feeder.

<!-- INSERT: location_interval_model -->

## Logistic models per FT interval (first 2/3 and final 1/3)

For each FT interval the data was split into the first two-thirds of the food-to-food interval and the final third, and a logistic regression was fit separately to each segment, using `TimeSinceFeeding` and `C(Subject)` as predictors. For the 60s interval, which contains only four sample points, the two-thirds split falls between the second and third points so the two segments are effectively halves. For the 240s final-third model, Minerva was excluded because she was at the feeder in all 57 of her observations in that segment, which caused the logit fit to diverge; her exclusion did not change the `TimeSinceFeeding` slope or *p*-value to four decimal places.

For each interval below, the first table gives the logit fit for the first segment and the second table for the final segment. A positive slope on `TimeSinceFeeding` indicates that the probability of being in the feeder area rises across the segment; a negative slope indicates it falls.

<!-- INSERT: location_models -->
