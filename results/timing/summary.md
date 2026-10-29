## Descriptive timing: recorded-default cumulative incidence

The same **9,844-loan audited cohort** is used without changing the Cox model. A deterministic Aalen–Johansen estimator treats first recorded default and the qualified closure proxy as competing events; administrative exits remain censoring. All tied daily cause counts use the same pre-event risk set, and same-day administrative censoring is removed after the event increments. **No date jitter, 1−KM substitution or new regression is used.**

| Customer status | 6 months | 12 months | 24 months |
| --- | ---: | ---: | ---: |
| New | 5.47% | 14.29% | 27.36% |
| Existing | 2.50% | 9.88% | 21.20% |
| All loans | 4.56% | 12.94% | 25.48% |

![Unadjusted recorded-default incidence with competing closure](default_cif.png)

**Time convention:** one plotted month = 730/24 = 30.4167 days; 6, 12 and 24 months correspond exactly to 182.5, 365 and 730 days. Daily event times are not rounded or jittered. Horizon estimates include events at/before the exact grid time (thus through day 182 for 6 months). Numbers at risk are loans with exit time ≥ the indicated time, immediately before any exits exactly then; the 24-month table therefore includes loans administratively censored at day 730.

**Independent check:** this cohort has no administrative censoring before day 730. At every event time, and at each displayed horizon, the estimated default CIF agrees within numerical tolerance with the count of audited first-default exits at/before that time divided by the starting group size. This is special to complete potential follow-up with competing closure fully classified; it is not a general replacement for competing-risks estimation. Default CIF + closure CIF + remaining event-free probability equals one throughout. Counts reconcile by vintage with the existing sample summary, and boundary/conflict exclusions are inherited unchanged.

**Interpretation:** these are unadjusted, loan-level descriptive proportions experiencing recorded default before closure, under the chosen closure proxy. New and existing customers differ in other characteristics and origination years. The curves are not adjusted Cox survival predictions, not individual default-date forecasts and not causal effects. Repeated borrowers affect uncertainty; no confidence bands or independence-based inferential claims are supplied. The unchanged new-customer Cox HR remains 1.445 (borrower-clustered approximate 95% CI 1.308–1.595), an adjusted relative rate among exposed loans, not a ratio of these CIFs.

Cox can estimate survival curves after baseline-hazard estimation in a default-only setting. With competing closure, actual default probabilities require accounting for both events. No predictive accuracy is evaluated. Source endpoint/monetary definitions and the existing PH/nonlinearity caveats remain.

Reproduce this addition with `python analysis/cumulative_incidence.py`; outputs, point-estimate validation and month/risk-set conventions are saved in `results/timing/`.
