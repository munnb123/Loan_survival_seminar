# Audience questions — outside planned speaking time

**Does this predict an individual default date?** No certain date is assigned. The new graph describes loan-level recorded-default incidence under the audited closure proxy. The Cox model describes adjusted conditional default rates. Cox can estimate survival after estimating its baseline in a default-only setting; actual default probabilities with competing closure require both event processes. None of these curves is a validated individual prediction here.

**Why not just use a binary classifier?** A classifier can target default within a specified horizon, but labels require suitable follow-up and competing-event definitions. Time-to-event methods retain timing and can use right-censored histories under suitable assumptions. ML methods can also model survival; no performance superiority is claimed.

**What differs between the timing curves and Cox hazard ratios?** The Aalen–Johansen curves are unadjusted proportions of loans experiencing recorded default by each time, with closure as a competing event. The HRs adjust for the included covariates and origination-year baseline, comparing instantaneous default rates among loans still exposed. Differences between the curves are not adjusted effects, and the HR is not a ratio of the plotted proportions.

**Why does closure differ from observation ending?** Closure ends this loan's default exposure and is a competing event. Administrative censoring ends observation of an otherwise exposed loan without declaring an event. Both remove loans from later cause-specific risk sets, but only closure receives competing-event probability mass in the cumulative-incidence calculation. Treating closures as censoring in 1−KM does not estimate actual default incidence.

**Why retain Cox when some proportional-hazards assumptions are doubtful?** It is a compact explanatory summary of relative-rate associations, not a claim that every effect is constant in truth. The existing diagnostics flag age and new-customer proportional-hazards concerns and age nonlinearity, with a borderline term nonlinear departure. These limit interpretation; they do not justify hiding the diagnostics or introducing more models into this lecture. Intervals remain approximate with tied daily dates.

**Have we evaluated predictive accuracy?** No. No validation of individual predictions, calibration, discrimination or out-of-sample performance is reported. This remains an explanatory lecture with descriptive timing curves and an unchanged audited Cox example. Point estimates are checked, not claims of forecasting accuracy.

## Technical reference for questions — notes only

The two former backup frames have been removed from both audience PDFs. Their useful explanations remain here, without adding speaking time or new calculations.

For distinct default times, the schematic partial likelihood within origination-year risk sets is

$$L(\beta)=\prod_{j:\,\mathrm{default}}\frac{\exp(\beta^{\mathsf T}x_{i_j})}{\sum_{k\in\mathcal R_{y_j}(t_j)}\exp(\beta^{\mathsf T}x_k)}.$$

Each factor conditions on an event and compares its observed identity with loans still exposed immediately beforehand in that year stratum. The common baseline cancels. The actual existing fit uses Efron handling of tied daily defaults; the schematic formula above is not the full tied-event likelihood. Closure and administrative censoring both remove later risk-set exposure, while closure also has competing-event mass in the timing curves.

Existing audited diagnostics, retained for reference rather than displayed as a slide:

| Covariate | Proportional hazards: elapsed-rank p | Proportional hazards: log-time p | Nonlinearity p |
| --- | ---: | ---: | ---: |
| Age | 0.00641 | 0.00768 | 0.00358 |
| Log income | 0.933 | 0.621 | 0.185 |
| Amount | 0.236 | 0.118 | 0.805 |
| Original scheduled term | 0.777 | 0.997 | 0.0438 |
| New customer | 0.00888 | 0.000417 | — |

The proportional-hazards tests are approximate independence-based Schoenfeld checks, not cluster-adjusted tests. Corrected ranks use elapsed event times; no original-term proportional-hazards departure was detected by those checks. Nonlinearity tests are the existing exploratory spline cluster-Wald checks, with no multiplicity correction. No diagnostics have been recomputed for this polish.

The existing one-loan-per-borrower sensitivity has 6,924 loans and 1,842 defaults. Coefficient directions are broadly similar, but composition changes: 95.05% new-customer loans versus 69.47% in the primary cohort. This is not an independent replication or a guarantee against confounding. Source measurement uncertainties and approximate intervals with tied daily times remain.
