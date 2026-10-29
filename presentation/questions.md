# Audience questions — outside planned speaking time

**Does this predict an individual default date?** No certain date is assigned. The new graph describes loan-level recorded-default incidence under the audited closure proxy. The Cox model describes adjusted conditional default rates. Cox can estimate survival after estimating its baseline in a default-only setting; actual default probabilities with competing closure require both event processes. None of these curves is a validated individual prediction here.

**Why not just use a binary classifier?** A classifier can target default within a specified horizon, but labels require suitable follow-up and competing-event definitions. Time-to-event methods retain timing and can use right-censored histories under suitable assumptions. ML methods can also model survival; no performance superiority is claimed.

**What differs between the timing curves and Cox hazard ratios?** The Aalen–Johansen curves are unadjusted proportions of loans experiencing recorded default by each time, with closure as a competing event. The HRs adjust for the included covariates and origination-year baseline, comparing instantaneous default rates among loans still exposed. Differences between the curves are not adjusted effects, and the HR is not a ratio of the plotted proportions.

**Why does closure differ from observation ending?** Closure ends this loan's default exposure and is a competing event. Administrative censoring ends observation of an otherwise exposed loan without declaring an event. Both remove loans from later cause-specific risk sets, but only closure receives competing-event probability mass in the cumulative-incidence calculation. Treating closures as censoring in 1−KM does not estimate actual default incidence.

**Why retain Cox when some PH assumptions are doubtful?** It is a compact explanatory summary of relative-rate associations, not a claim that every effect is constant in truth. The existing diagnostics flag age and new-customer PH concerns and age nonlinearity, with a borderline term nonlinear departure. These limit interpretation; they do not justify hiding the diagnostics or introducing more models into this lecture. Intervals remain approximate with tied daily dates.

**Have we evaluated predictive accuracy?** No. No validation of individual predictions, calibration, discrimination or out-of-sample performance is reported. This remains an explanatory lecture with descriptive timing curves and an unchanged audited Cox example. Point estimates are checked, not claims of forecasting accuracy.
