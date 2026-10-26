# Speaker notes — Luke Munnelly

Standalone MSc seminar. **20 main slides, 25:00 total.** Two optional backup slides are outside the timing. The presentation has 39 pages because progressive reveals expand logical slides; the handout has 22 pages, one per logical slide. The static PDF figures occupy complete frames and do not animate. On slide 12, discuss the risk-set setup before advancing to the worked answer on slide 13.

| Slide | Start–end | Duration | Topic |
| --- | --- | --- | --- |
| 1 | 00:00–00:30 | 0:30 | When Will a Borrower Default? |
| 2 | 00:30–01:35 | 1:05 | Why does timing matter? |
| 3 | 01:35–02:10 | 0:35 | Define the event and the clock |
| 4 | 02:10–03:45 | 1:35 | Loan Timelines |
| 5 | 03:45–04:50 | 1:05 | The survival function |
| 6 | 04:50–05:55 | 1:05 | Illustrative Survival |
| 7 | 05:55–07:35 | 1:40 | The hazard is an instantaneous rate |
| 8 | 07:35–09:00 | 1:25 | From hazard to survival |
| 9 | 09:00–10:30 | 1:30 | The Cox model |
| 10 | 10:30–11:35 | 1:05 | A hazard ratio compares two rates |
| 11 | 11:35–12:45 | 1:10 | Proportional Hazards |
| 12 | 12:45–14:10 | 1:25 | Immediately before one default |
| 13 | 14:10–15:55 | 1:45 | Cox Risk Set |
| 14 | 15:55–17:00 | 1:05 | The audited Bondora cohort |
| 15 | 17:00–18:30 | 1:30 | Follow-up uses audited endpoints |
| 16 | 18:30–19:30 | 1:00 | Five covariates; one Cox model |
| 17 | 19:30–21:10 | 1:40 | Audited Hazard Ratios |
| 18 | 21:10–22:30 | 1:20 | New versus existing customer |
| 19 | 22:30–24:05 | 1:35 | Where interpretation is limited |
| 20 | 24:05–25:00 | 0:55 | Conclusion |
| B1 | Optional | — | Backup: partial likelihood |
| B2 | Optional | — | Backup: corrected diagnostics |

## 1. When Will a Borrower Default? (00:00–00:30)

Introduce the question: not just whether a default occurs, but when. This is an explanatory methods example, not a forecasting competition.


## 2. Why does timing matter? (00:30–01:35)

A binary label loses the timing of A's default and can wrongly treat B as a permanent nondefault. B tells us it remained exposed without a recorded default through eighteen months. Ask the audience what we really know about B.


## 3. Define the event and the clock (01:35–02:10)

Set the time origin at origination and the event at first recorded default. The hypothetical examples use months for intuition; the empirical analysis measures days and stops at 730 days. Some observations end without a default, which is why the next diagram matters. This lecture is standalone and does not refer to prior thesis work.


## 4. Loan Timelines (02:10–03:45)

Walk through the complete static figure. A is an observed event at month eight. B is right censored at eighteen: active when observation ends. C closes at twelve, a competing event, so this loan no longer remains exposed to first default. Closure and administrative censoring have different substantive meanings, even though the cause-specific Cox risk set removes both at exit. In Bondora we use an audited closure proxy, not every contract-end date.


## 5. The survival function (03:45–04:50)

Define T_D as time to default in this deliberately simple setting. Survival is an established technical term; here the surviving state means no default yet. Later we will distinguish this default-only illustration from loans that can also close.


## 6. Illustrative Survival (04:50–05:55)

The entire curve is hypothetical. Read the twelve-month guide lines: exp(-0.02 times 12) is about 0.79. This is a probability between zero and one. The constant 0.02 is per month. Do not describe the curve as a Bondora estimate or as a cumulative-incidence estimate under competing closure.


## 7. The hazard is an instantaneous rate (05:55–07:35)

Condition on reaching t without default. The numerator is a probability over a short interval; dividing by its length makes it a rate. For the earlier example, a hazard of 0.02 per month implies an approximate 0.02 probability over a sufficiently short interval of one month, with the exact one-month probability 1-exp(-0.02), about 0.0198. The approximation is local, not a rule for multiplying across long horizons. Under competing exits, the cause-specific default hazard conditions on remaining exposed to both default and closure.


## 8. From hazard to survival (07:35–09:00)

H is cumulative hazard, a dimensionless accumulation of the instantaneous rate. With only default, survival is exp(-H). With competing closure, exp(-H_D) is not the actual event-free survival or actual probability of avoiding default. Event-free survival depends on all cause-specific hazards; default incidence also depends on remaining exposed. We will not estimate those probabilities in this seminar.


## 9. The Cox model (09:00–10:30)

The baseline can vary freely with elapsed time and, in this analysis, with origination year. The covariates multiply it through exp(beta transpose x). The coefficients are shared across the year strata. Still exposed means neither defaulted nor reached the qualified closure exit. The model describes conditional associations, not causal effects. Separate baseline strata do not remove all calendar-time confounding.


## 10. A hazard ratio compares two rates (10:30–11:35)

The baseline cancels for a comparison within the same origination-year stratum. A one-unit covariate contrast changes the rate by exp(beta), conditional on the other covariates. The ratio is constant over time only under the proportional-hazards assumption. It is not automatically a probability ratio, even in a default-only setting.


## 11. Proportional Hazards (11:35–12:45)

Point first to the two smoothly varying hazards, then to the ratio panel. These are static hypothetical curves. Both rates change, but B stays one and a half times A. Proportional hazards does not mean constant hazards. This is an illustration of the assumption, not evidence that it holds for Bondora.


## 12. Immediately before one default (12:45–14:10)

All three borrowers are still at risk immediately before this default time, in the same baseline stratum. They differ only in the new-customer indicator. Assign weights one, one and exp(beta). Ask what share of the total risk weight belongs to C. Do not reveal the numerical answer until the next frame. This conditions on one event occurring, not on a future time horizon.


## 13. Cox Risk Set (14:10–15:55)

Now show the full worked answer. C's risk weight divided by total weight is exp(beta)/(2+exp(beta)). Choose beta=log(2) purely for illustration: the weights are one, one, two, so C accounts for half of the conditional probability mass. This is not the empirical new-customer coefficient. Cox combines comparisons of this kind across observed default times to learn relative effects. The common baseline cancels within a risk set. Actual daily data may have tied defaults, which the existing analysis handles with Efron's approximation.


## 14. The audited Bondora cohort (15:55–17:00)

The supplied filtered snapshot has 9,863 candidate loans. After the audited exclusions, 9,844 loans from 6,924 borrowers remain and 2,508 recorded defaults fall within 730 days. The cutoff is the explicit ReportAsOfEOD, not the latest observed default. Fourteen missing closure dates, three same-day default/closure conflicts and two nonpositive incomes account for exclusions. These counts are not model-predicted default probabilities.


## 15. Follow-up uses audited endpoints (17:00–18:30)

Do not replace DefaultDate with a late-status label or erase a default because a loan was later repaid. ContractEndDate also occurs on Current and Late loans, often in the future, so it cannot universally mean actual repayment. Repaid status can coexist with write-offs. The model uses an audited closure proxy, representing a competing exit. The general rule also caps at reporting date, but this cohort reaches 730 days first. Original contracts and complete payment histories are unavailable.


## 16. Five covariates; one Cox model (18:30–19:30)

Contrasts are age per ten years, income doubling, amount per 1,000 recorded monetary units, original term per twelve months and new versus existing customer. Original term uses FirstPaymentDate and MaturityDate_Original, not revised maturity. Monetary currency and income-period source definitions are not independently verified; the existing euro label has that qualification. Baseline hazards differ by origination year, while standard errors cluster repeated loans by borrower. No selection or model competition is being introduced.


## 17. Audited Hazard Ratios (19:30–21:10)

Show the final audited estimates, not earlier exploratory numbers. The vertical line is one and the horizontal axis is logarithmic. Intervals are borrower-clustered approximate 95 percent Wald intervals. Age and income estimates are below one; new customer and original term are above one; amount is near one with an interval spanning one. Do not read these as causal or cumulative-risk effects. Keep the visible caveats: age/new-customer PH concerns, age nonlinearity, borderline term nonlinearity, approximate intervals with tied dates and unverified source monetary units.


## 18. New versus existing customer (21:10–22:30)

Subtract one from 1.4445 and multiply by one hundred: about 44 percent. This is conditional on age, income, amount, original scheduled term and origination-year baseline, and on remaining exposed. It is not 44 percentage points, a ratio of horizon default probabilities, or a causal effect of being new. New-customer status has a PH concern in the full sample, so a single constant HR compresses a potentially changing association.


## 19. Where interpretation is limited (22:30–24:05)

The corrected rank-time and log-time diagnostics flag age and new-customer status. Do not repeat the earlier original-term PH finding: it was not reproduced with corrected elapsed ranks. Age also shows nonlinearity; original term has a borderline nonlinear departure, which is a different assumption. PH tests in the repeated-loan sample are approximate and not cluster adjusted. One loan per borrower gives broadly similar directions but changes composition, especially new-customer prevalence. The source arrears threshold, literal full-repayment date and original currency/measurement definitions remain uncertain. We report these rather than adding more models.


## 20. Conclusion (24:05–25:00)

Close the original question: when, not just whether. The example illustrates how to use follow-up, remove competing exits from the cause-specific risk set, and interpret a rate comparison carefully. Do not claim that the model forecasts when an individual borrower will default. Invite questions; the next two frames are optional backup material and are outside the 25-minute plan.


## B1. Backup: partial likelihood (Optional)

Each factor is the conditional probability of the observed defaulting identity given one event in that stratum's risk set. The baseline cancels and we combine contributions over event times. Censoring and closure affect who is in the risk set. The formula is schematic for untied events; do not imply it is the exact tied-data likelihood used by the existing software.


## B2. Backup: corrected diagnostics (Optional)

These are the existing audited diagnostics, not newly run tests. In year-stratified fits the software's cumulative row-order rank is unsafe; corrected elapsed ranks remove the apparent original-term departure. Nonlinearity and proportional hazards are different questions. No multiplicity correction or omnibus cluster-adjusted PH test is claimed. The one-loan sample is 95.05 percent new customer compared with 69.47 percent in the primary sample; its new-customer interval widens and income/term effects attenuate. Source files are REPORT.md and the audited diagnostic CSVs.
