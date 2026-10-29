# Speaker notes — Luke Munnelly

Standalone lecture for MSc Stochastics and Financial Mathematics students. **26 main logical slides; 26:40 at a calm pace.** Skip optional slides 5 (55 seconds) and 13 (45 seconds) for a **25:00 speaking route**. Audience questions and the two backup slides are outside both plans. Timings include the indicated pauses and figure reading, not extra theory or audience discussion. The presentation has 52 overlay-expanded pages; the handout has 28 pages, one per logical slide.

## Practical 25-minute route

- After slide 4, skip optional slide 5 and resume slide 6 on presentation PDF page 12.
- After slide 12, skip optional slide 13 and resume slide 14 on presentation PDF page 26.
- These transitions are self-contained: slide 4 already explains the horizon issue, and slide 14 requires no cumulative-hazard notation.
- Do not rush the opening, graph reading or conditional risk-set calculation. If nervous, take the scripted short pauses rather than filling them with extra material.
- Risk-set setup is slide 18; the static worked-answer figure is slide 19. Explain the setup before advancing.

## Schedule

| Slide | Full-plan time | 25-minute route | Duration | Topic |
| --- | --- | --- | --- | --- |
| 1 | 00:00–00:25 | 00:00–00:25 | 0:25 | When Will a Borrower Default? |
| 2 | 00:25–01:35 | 00:25–01:35 | 1:10 | Should these be the same outcome? |
| 3 | 01:35–02:30 | 01:35–02:30 | 0:55 | A third borrower has not defaulted yet |
| 4 | 02:30–03:30 | 02:30–03:30 | 1:00 | A binary label needs a horizon |
| 5 | 03:30–04:25 | Skip | 0:55 | Which 12-month labels are known? |
| 6 | 04:25–05:20 | 03:30–04:25 | 0:55 | Why survival analysis? |
| 7 | 05:20–05:50 | 04:25–04:55 | 0:30 | Choose the event and the clock |
| 8 | 05:50–07:20 | 04:55–06:25 | 1:30 | Follow-up timelines |
| 9 | 07:20–08:05 | 06:25–07:10 | 0:45 | The survival function |
| 10 | 08:05–09:10 | 07:10–08:15 | 1:05 | Illustrative Survival |
| 11 | 09:10–09:50 | 08:15–08:55 | 0:40 | How rapidly are defaults occurring now? |
| 12 | 09:50–11:10 | 08:55–10:15 | 1:20 | From a short interval to a hazard rate |
| 13 | 11:10–11:55 | Skip | 0:45 | From hazard to survival |
| 14 | 11:55–12:30 | 10:15–10:50 | 0:35 | Borrowers have different characteristics |
| 15 | 12:30–13:50 | 10:50–12:10 | 1:20 | The Cox model |
| 16 | 13:50–14:50 | 12:10–13:10 | 1:00 | Compare otherwise identical borrowers |
| 17 | 14:50–15:50 | 13:10–14:10 | 1:00 | Proportional Hazards |
| 18 | 15:50–17:00 | 14:10–15:20 | 1:10 | How does Cox learn relative effects? |
| 19 | 17:00–18:30 | 15:20–16:50 | 1:30 | Cox Risk Set |
| 20 | 18:30–19:30 | 16:50–17:50 | 1:00 | The audited Bondora cohort |
| 21 | 19:30–20:40 | 17:50–19:00 | 1:10 | Follow-up uses audited endpoints |
| 22 | 20:40–21:40 | 19:00–20:00 | 1:00 | Five predictors and their contrasts |
| 23 | 21:40–23:10 | 20:00–21:30 | 1:30 | Audited Hazard Ratios |
| 24 | 23:10–24:25 | 21:30–22:45 | 1:15 | New versus existing customer |
| 25 | 24:25–25:50 | 22:45–24:10 | 1:25 | Where interpretation is limited |
| 26 | 25:50–26:40 | 24:10–25:00 | 0:50 | Back to the lending question |
| B1 | Backup | Backup | — | Backup: partial likelihood |
| B2 | Backup | Backup | — | Backup: corrected diagnostics |

## 1. When Will a Borrower Default? (00:00–00:25; short route: 00:00–00:25)

Introduce the lending question rather than the method. This is a standalone lecture for MSc Stochastics and Financial Mathematics students. We will use a small audited example to interpret default rates, not compare prediction algorithms. Advance promptly to the two borrowers.


## 2. Should these be the same outcome? (00:25–01:35; short route: 00:25–01:35)

Start with the exact question: One borrower defaults after three months, another after two years. Should we treat these as the same outcome? Show only the first borrower, then reveal the second and pause for three seconds. They share an eventual default label but expose the lender for very different lengths of time. Cash flows and time exposed to credit risk differ; no numerical loss calculation is needed. Reveal the final statement only after making this distinction. This is a rhetorical pause, not planned audience-question time.


## 3. A third borrower has not defaulted yet (01:35–02:30; short route: 01:35–02:30)

Introduce a third hypothetical borrower. We have watched this loan for only six months and have not seen a default. Pause before revealing the last line. We know something useful: no default occurred during the observed exposure. We do not know its later outcome. Do not call this borrower a permanent nondefault or assume that it is comparable to a loan watched for two years. This motivates handling incomplete follow-up.


## 4. A binary label needs a horizon (02:30–03:30; short route: 02:30–03:30)

A conventional classifier can answer a perfectly legitimate fixed-horizon question, such as default within twelve months. The issue is not that classification is wrong: it is that a label requires the relevant horizon to be observed, or otherwise appropriately handled. An event observed before the horizon is known; a no-default label generally needs exposure through that horizon, with competing events addressed according to the intended target. Our six-month borrower does not yet supply that label. If already running long, skip the next worked-label slide and go directly to slide 6; this explanation is self-contained.


## 5. Which 12-month labels are known? (03:30–04:25; short route: Skip)

OPTIONAL: skip this entire slide to save 55 seconds. It elaborates slide 4 without introducing a new concept. First read the three histories with the answers hidden. Reveal the first two labels: a default at month three is inside the twelve-month horizon, and a default at month twenty-four implies event-free exposure through month twelve in these simple histories. Pause, then reveal Unknown for the loan only observed through six months. This borrower is not a negative training example just because no default has yet appeared. Resume with slide 6.


## 6. Why survival analysis? (04:25–05:20; short route: 03:30–04:25)

Connect both opening problems to the method. Time-to-event data retain event timing and can use incomplete right-censored histories under appropriate observation assumptions. This does not mean censoring can be ignored or that survival analysis is automatically unbiased. We choose Cox because a small set of relative-hazard effects is interpretable for this lecture. Survival analysis is a type of outcome framework, not the opposite of machine learning; ML survival methods also exist. We will not compare their predictive performance.


## 7. Choose the event and the clock (05:20–05:50; short route: 04:25–04:55)

Before writing any formula, specify the event and the start of the clock. Here the event is first recorded default and the origin is loan issuance. The illustrations use months; the audited example uses days. Some histories stop before a default is seen, and we need to distinguish why they stop. Move directly to the timelines.


## 8. Follow-up timelines (05:50–07:20; short route: 04:55–06:25)

Use the same hypothetical borrowers as in the opening: A defaults at three months and B at twenty-four. C is still active when observation ends at six months: this is right censoring. We know only that it remained default-free through the observed period. Add D, which closes at twelve months: closure is a competing event ending default exposure, not simply failure to keep observing an active loan. Point to the cross, censoring bar and closure diamond in turn. The whole figure is static; do not click expecting internal reveals. For interpreting the default rate, remove a closed loan from the exposed risk set. Appropriate administrative-censoring assumptions still matter.


## 9. The survival function (07:20–08:05; short route: 06:25–07:10)

We now have a reason to introduce notation. Let T_D be time to default in a simplified world without competing closure. Read S(t) as the probability that the event has not happened by t. Reveal the plain-language interpretation after reading the equation. Survival is the technical term for remaining event-free; it does not imply anything about the borrower outside this defined event.


## 10. Illustrative Survival (08:05–09:10; short route: 07:10–08:15)

This curve is hypothetical, not a Bondora estimate. Start at one on the vertical axis and move right along elapsed months. Trace the month-twelve guide up to the curve, then across to about 0.79. Pause for three seconds so the audience can read the guides. About 79 percent remain default-free at twelve months in this default-only example. The formula exp(-0.02t) uses t in months. The same plot is already visible throughout this frame; guide attention verbally rather than pretending it animates.


## 11. How rapidly are defaults occurring now? (09:10–09:50; short route: 08:15–08:55)

Introduce hazard in ordinary language before the limit definition. Restrict attention to loans still exposed at the current time and ask about the rate of imminent defaults. It is a local rate, not the fraction that will eventually default. Reveal the term hazard after that intuition. If time is measured in months, its units are inverse months. The next equation formalises this same question rather than introducing a different object.


## 12. From a short interval to a hazard rate (09:50–11:10; short route: 08:55–10:15)

Read the numerator first: conditional on no default yet, what is the chance of default in the next small interval? Divide by its length and shrink the interval to obtain a rate. Do not explain every symbol as a separate reveal. Once the definition is explained, reveal the short-interval approximation. For the earlier curve a constant hazard of 0.02 per month gives an approximate 0.02 one-month conditional probability, with exact value 1-exp(-0.02), about 0.0198. Do not multiply a rate over a long horizon as though it were an exact probability. If running long, skip slide 13 and go directly to borrower characteristics on slide 14.


## 13. From hazard to survival (11:10–11:55; short route: Skip)

OPTIONAL: skip this entire slide to save 45 seconds. It connects two already introduced objects. H accumulates the hazard over time and, in the default-only setting, S equals exp(-H). For the illustrative constant rate, H(t)=0.02t, giving the earlier curve. Reveal the survival equation only after the integral. With competing closure, exp(-H_D) is not the actual event-free survival or actual default probability: those depend on the competing process too. No cumulative-incidence analysis is being added. Continue with slide 14; it does not rely on H notation.


## 14. Borrowers have different characteristics (11:55–12:30; short route: 10:15–10:50)

We have described how risk varies with elapsed time. Now ask whether borrowers with different characteristics have different default rates. Use age, income and customer status simply as examples, not claims about the direction of their effects. This motivates adding covariates to a common time-dependent baseline. The Cox model offers an interpretable multiplicative description.


## 15. The Cox model (12:30–13:50; short route: 10:50–12:10)

Show the whole equation first and read it as baseline times a positive covariate multiplier. Reveal the baseline explanation and point to h_0(t): we do not require a constant hazard or choose a fixed parametric shape here. It represents the rate at reference covariates. Then reveal the multiplier explanation: exp(beta transpose x) scales that rate. In the audited example the object is the cause-specific default hazard among loans neither defaulted nor closed, and the baseline is allowed to differ by origination year. Borrower coefficients are shared across those strata.


## 16. Compare otherwise identical borrowers (13:50–14:50; short route: 12:10–13:10)

The baseline cancels for two otherwise identical borrowers in the same baseline stratum. The customer indicator differs by one, so their relative hazard is exp(beta_new). Explain the equation before revealing the illustrative value of 1.5. That means a fifty percent higher instantaneous rate, not fifty percentage points or a fifty percent higher default probability over a horizon. This value is hypothetical and is not the final Bondora estimate. Under PH the ratio remains constant, even though both hazards may vary, as the next picture shows.


## 17. Proportional Hazards (14:50–15:50; short route: 13:10–14:10)

First follow A's curve, then B's. Both rates change over time; B stays one and a half times A. Point to the right panel showing the flat ratio. Pause briefly to let the audience compare the changing left panel with the constant right panel. Proportional hazards concerns the ratio, not constancy of either rate. These curves are hypothetical, not evidence that the assumption holds for Bondora. The plot is static throughout this frame.


## 18. How does Cox learn relative effects? (15:50–17:00; short route: 14:10–15:20)

Introduce a separate teaching risk set, not the original three opening histories. All borrowers are still exposed just before this default time, in the same baseline stratum, and other covariates are identical. Their weights are one, one and exp(beta). Explain that we condition on one default occurring and ask which borrower it belongs to. Ask rhetorically what fraction of the total weight belongs to C, then pause for three seconds. Do not advance to the worked answer until the setup is understood.


## 19. Cox Risk Set (17:00–18:30; short route: 15:20–16:50)

Now show the answer: C's conditional share is exp(beta) divided by 2+exp(beta). Point to the symbolic expression before explaining the numerical example. With beta=log(2), chosen only for illustration, the weights are one, one and two, so C receives half of the total weight. Pause to allow the arithmetic to settle. This is conditional on one event occurring now, not a probability of default over a horizon. Cox combines comparisons like this across observed event times to estimate relative effects; the common baseline cancels. Full partial likelihood and the existing Efron handling of tied daily defaults are left to backup notes.


## 20. The audited Bondora cohort (18:30–19:30; short route: 16:50–17:50)

Move clearly from hypothetical teaching examples to empirical data. The audited analysis retains 9,844 loans, 6,924 borrowers and 2,508 recorded defaults within 730 days. Reveal these counts after defining the country, origination years and horizon. The cutoff is the explicitly recorded ReportAsOfEOD of 20 July 2021, not the latest observed default or the file creation date. All origination dates have at least 730 days of potential observation. The event count is descriptive, not a model-predicted horizon probability.


## 21. Follow-up uses audited endpoints (19:30–20:40; short route: 17:50–19:00)

Keep this operational definition short. A later repaid status does not erase an earlier recorded default. ContractEndDate occurs on Current and Late loans too and can be a future date, so not every such value is a repayment. The audit restricts the nondefault exit to a closure proxy in loans labeled Repaid; write-offs mean this still need not be literal full cash repayment. The general stopping rule also includes reporting cutoff, but for this cohort the 730-day cap comes first. Keep the uncertainty about the source's arrears threshold explicit; do not assert a sixty- or ninety-day definition.


## 22. Five predictors and their contrasts (20:40–21:40; short route: 19:00–20:00)

Read these as comparison units, not raw coefficient sizes. The model uses log income, and multiplying its coefficient by log(2) gives the displayed doubling contrast. Original scheduled term is reconstructed from FirstPaymentDate to MaturityDate_Original assuming monthly installments, not from revised maturity. Amount and income are used as recorded; the existing plot's euro label has the report's unverified-currency qualification. Baseline hazards differ by origination year and intervals cluster repeated borrowers. We use this one existing Cox model; no predictors, fits or selection procedures are added.


## 23. Audited Hazard Ratios (21:40–23:10; short route: 20:00–21:30)

This is the final audited empirical plot, not an illustrative or preliminary estimate. Orient the audience to the reference line at one and the logarithmic horizontal scale. Walk through the directions briefly: age and income below one, original term and new-customer status above one, and amount near one with an interval spanning one. Pause to read the exact contrasts, especially income doubling. These are borrower-clustered approximate 95 percent Wald intervals. Leave detailed diagnostics for backup but retain the visible assumptions and source-unit qualifications. Focus the next slide on one careful interpretation rather than narrating every p-value.


## 24. New versus existing customer (23:10–24:25; short route: 21:30–22:45)

Show and explain the estimate first. On the next reveal, subtract one from the unrounded 1.4445 and convert to about forty-four percent. This is a conditional instantaneous default rate among loans still exposed, adjusting for the included covariates and origination-year baseline. It is not forty-four percentage points, a default-probability ratio or a causal effect of being new. The corrected diagnostics flag new-customer PH concerns in the full sample, so the single constant HR compresses a possibly time-varying association. Give that qualification before moving to general limitations.


## 25. Where interpretation is limited (24:25–25:50; short route: 22:45–24:10)

One short point per reveal. Corrected elapsed-rank and log-time diagnostics flag age and new-customer status; the superseded original-term PH finding is not repeated. Age also shows nonlinearity, while term has a borderline nonlinear departure, a separate assumption. Daily ties make the borrower-clustered Wald intervals approximate. The full-sample PH tests are approximate and not cluster adjusted. The source arrears threshold, full-repayment timing, monetary measurement definitions and original monthly-schedule proxy remain qualified. Detailed p-values and sensitivity checks are in backup material; do not turn this into a new modelling exercise.


## 26. Back to the lending question (25:50–26:40; short route: 24:10–25:00)

Return explicitly to the original borrowers. We should not discard the distinction between default at three months and default at two years. Six default-free months are informative but do not establish a later nondefault label. Survival methods preserve timing and can accommodate censoring under suitable assumptions, and Cox gives interpretable conditional rate comparisons. It does not say exactly when each individual will default. End the planned speaking time here, then invite questions. Audience questions and the two backup frames are outside the timing.


## B1. Backup: partial likelihood (Backup; short route: Backup)

Each factor is the conditional probability of the observed defaulting identity given one event in that stratum's risk set. The baseline cancels and we combine contributions over event times. Censoring and closure affect who is in the risk set. The formula is schematic for untied events; do not imply it is the exact tied-data likelihood used by the existing software.


## B2. Backup: corrected diagnostics (Backup; short route: Backup)

These are the existing audited diagnostics, not newly run tests. In year-stratified fits the software's cumulative row-order rank is unsafe; corrected elapsed ranks remove the apparent original-term departure. Nonlinearity and proportional hazards are different questions. No multiplicity correction or omnibus cluster-adjusted PH test is claimed. The one-loan sample is 95.05 percent new customer compared with 69.47 percent in the primary sample; its new-customer interval widens and income/term effects attenuate. Source files are REPORT.md and the audited diagnostic CSVs.
