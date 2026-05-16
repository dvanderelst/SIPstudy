# Activity Patterns Across the Food-to-Food Interval

Activity was scored from video using a 15-second instantaneous time-sampling method; at each sample point the cat was classified as active (any movement or interaction) or inactive (resting or pausing). To assess how activity was allocated across each food-to-food interval, we fit two logistic regressions (`smf.logit`) per FT interval, pooling data across cats: one for the first two-thirds of the interval and one for the final third. Each model used `TimeSinceFeeding` and `C(Subject)` as predictors, and we tested whether the slope on `TimeSinceFeeding` differed significantly from zero. For the 60s interval, which contains only four sample points, the two-thirds split falls between the second and third points, so the two segments are effectively halves rather than thirds. Figure 3 (reproduced below) shows the average proportion of intervals marked as active across the food-to-food interval. Open circles mark data points in the first two-thirds of each interval, and filled circles mark those in the final one-third, corresponding to the two segments fit by the piecewise models below.

![Figure 3. Average proportion of intervals marked as active across the food-to-food interval.](../behavior_output/activity.png)

## Logistic models per FT interval (first 2/3 and final 1/3)

For each FT interval below, the first table gives the logit fit for the first segment and the second table for the final segment. A positive slope on `TimeSinceFeeding` indicates that the probability of being active rises across the segment; a negative slope indicates it falls. The `p`-value on the `TimeSinceFeeding` row tests whether the slope differs significantly from zero.

<!-- INSERT: activity_models -->
