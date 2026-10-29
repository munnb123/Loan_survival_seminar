# When Will a Borrower Default?
## A simple survival-analysis example for an MSc lecture

**Question:** Among loans that have not yet defaulted or closed, how does the rate of recorded default vary with borrower and loan characteristics?

**Data:** Estonian Bondora loans issued in 2013–2015. Follow each loan from issue for at most 730 days. The snapshot explicitly reports through 20 July 2021.

| Sample | Count |
| --- | ---: |
| Analyzed loans | 9,844 |
| Borrowers | 6,924 |
| Recorded defaults within 730 days | 2,508 |
| Closure-proxy exits within 730 days | 2,729 |
| Follow-up ending at 730 days | 4,607 |

**One model:** cause-specific Cox regression with age, log income, amount, original scheduled term and new-customer status. Separate baseline hazards by origination year; cluster standard errors by borrower. No model selection, prediction comparison or performance metrics.

| Covariate contrast | Hazard ratio | 95% confidence interval |
| --- | ---: | ---: |
| Age: 10 years older | 0.758 | 0.725–0.793 |
| Income: doubling | 0.854 | 0.795–0.918 |
| Amount: 1,000 recorded monetary units higher | 1.017 | 0.995–1.039 |
| Original scheduled term: 12 months longer | 1.058 | 1.022–1.096 |
| New vs existing customer | 1.445 | 1.308–1.595 |

![Hazard ratios](results/hazard_ratios.png)

**Example interpretation:** conditional on the included covariates and origination year, a new customer has an estimated 44% higher instantaneous default rate than an existing customer while their loans remain at risk. This is an association, not a causal effect or a 44 percentage-point increase in default probability.

**Three teaching points:**

1. **Time and outcome definitions come first.** Use DefaultDate even if the loan was later repaid. ContractEndDate is not universally actual repayment: ignore it for Current/Late loans and use it only as a closure proxy for Repaid loans. The exact default arrears threshold is unverified.
2. **A hazard ratio is a summary with assumptions.** Age shows nonlinearity and evidence against proportional hazards; new-customer status also shows a PH departure in the full sample. The corrected diagnostic does not reproduce a PH departure for original term. Explain these caveats without adding a more complex lecture model.
3. **Repeated loans are not independent observations.** Use borrower-clustered intervals. Keeping one analyzed loan per borrower gives broadly similar coefficient directions, although the sample becomes predominantly new customers and some associations attenuate.

Original term is reconstructed from the original monthly payment schedule, not revised maturity. Removing 59 disputed term records or ten ambiguous closure-censored records barely changes the main coefficients. These checks and source-definition limitations are documented in [REPORT.md](REPORT.md); they can remain backup material.

## Minimal model code

After the documented date audit and cohort construction:

```python
from lifelines import CoxPHFitter

# df has one row per loan. duration and event use the audited definitions.
columns = ["duration", "event", "year", "UserName",
           "age_10y", "log_income", "amount_1000", "term_12m", "new_customer"]

model = CoxPHFitter()
model.fit(df[columns], duration_col="duration", event_col="event",
          strata=["year"], cluster_col="UserName", robust=True)
model.print_summary()
```

The income coefficient in this code is per natural-log unit; multiply the coefficient and its standard error by ln(2) to display the doubling contrast in the table. See [README.md](README.md) for the full reproducible run. The analysis uses recorded monetary values; confirm original currency/period definitions before making literal euro/month claims. All intervals are approximate with tied daily event times. The lecture source and compiled slides are in `presentation/`.

<!-- DESCRIPTIVE_TIMING_START -->
## Descriptive timing: recorded-default cumulative incidence

The same **9,844-loan audited cohort** is used without changing the Cox model. A deterministic Aalen–Johansen estimator treats first recorded default and the qualified closure proxy as competing events; administrative exits remain censoring. All tied daily cause counts use the same pre-event risk set, and same-day administrative censoring is removed after the event increments. **No date jitter, 1−KM substitution or new regression is used.**

| Customer status | 6 months | 12 months | 24 months |
| --- | ---: | ---: | ---: |
| New | 5.47% | 14.29% | 27.36% |
| Existing | 2.50% | 9.88% | 21.20% |
| All loans | 4.56% | 12.94% | 25.48% |

![Unadjusted recorded-default incidence with competing closure](results/timing/default_cif.png)

**Time convention:** one plotted month = 730/24 = 30.4167 days; 6, 12 and 24 months correspond exactly to 182.5, 365 and 730 days. Daily event times are not rounded or jittered. Horizon estimates include events at/before the exact grid time (thus through day 182 for 6 months). Numbers at risk are loans with exit time ≥ the indicated time, immediately before any exits exactly then; the 24-month table therefore includes loans administratively censored at day 730.

**Independent check:** this cohort has no administrative censoring before day 730. At every event time, and at each displayed horizon, the estimated default CIF agrees within numerical tolerance with the count of audited first-default exits at/before that time divided by the starting group size. This is special to complete potential follow-up with competing closure fully classified; it is not a general replacement for competing-risks estimation. Default CIF + closure CIF + remaining event-free probability equals one throughout. Counts reconcile by vintage with the existing sample summary, and boundary/conflict exclusions are inherited unchanged.

**Interpretation:** these are unadjusted, loan-level descriptive proportions experiencing recorded default before closure, under the chosen closure proxy. New and existing customers differ in other characteristics and origination years. The curves are not adjusted Cox survival predictions, not individual default-date forecasts and not causal effects. Repeated borrowers affect uncertainty; no confidence bands or independence-based inferential claims are supplied. The unchanged new-customer Cox HR remains 1.445 (borrower-clustered approximate 95% CI 1.308–1.595), an adjusted relative rate among exposed loans, not a ratio of these CIFs.

Cox can estimate survival curves after baseline-hazard estimation in a default-only setting. With competing closure, actual default probabilities require accounting for both events. No predictive accuracy is evaluated. Source endpoint/monetary definitions and the existing PH/nonlinearity caveats remain.

Reproduce this addition with `python analysis/cumulative_incidence.py`; outputs, point-estimate validation and month/risk-set conventions are saved in `results/timing/`.
<!-- DESCRIPTIVE_TIMING_END -->
