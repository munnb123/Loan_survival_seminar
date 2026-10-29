# Speaker notes — Luke Munnelly

Standalone lecture for MSc Stochastics and Financial Mathematics students. **28 main logical slides; 26:40 at a calm pace.** Skip optional slides 6 (55 seconds) and 14 (45 seconds) for a **25:00 speaking route**. Audience questions and the two backup slides are outside both plans. Timings include the indicated pauses and figure reading, not extra theory or audience discussion. The presentation has 56 overlay-expanded pages; the handout has 30 pages, one per logical slide.

## Practical 25-minute route

- After slide 5, skip optional slide 6 and resume slide 7 on presentation PDF page 15.
- After slide 13, skip optional slide 14 and resume slide 15 on presentation PDF page 29.
- These transitions are self-contained: slide 5 already explains the horizon issue, and slide 15 requires no cumulative-hazard notation.
- Do not rush the opening, graph reading or conditional risk-set calculation. If nervous, take the scripted short pauses rather than filling them with extra material.
- Risk-set setup is slide 19; the static worked-answer figure is slide 20. The descriptive timing curve is slide 23; the adjusted Cox HR plot is slide 25.

## Schedule

| Slide | Full-plan time | 25-minute route | Duration | Topic |
| --- | --- | --- | --- | --- |
| 1 | 00:00–00:20 | 00:00–00:20 | 0:20 | When Will a Borrower Default? |
| 2 | 00:20–01:15 | 00:20–01:15 | 0:55 | Should these be the same outcome? |
| 3 | 01:15–02:05 | 01:15–02:05 | 0:50 | Principal still outstanding |
| 4 | 02:05–02:55 | 02:05–02:55 | 0:50 | What do six months tell us? |
| 5 | 02:55–03:45 | 02:55–03:45 | 0:50 | A binary label needs a horizon |
| 6 | 03:45–04:40 | Skip | 0:55 | Which 12-month labels are known? |
| 7 | 04:40–05:25 | 03:45–04:30 | 0:45 | Why survival analysis? |
| 8 | 05:25–05:50 | 04:30–04:55 | 0:25 | Choose the event and the clock |
| 9 | 05:50–07:10 | 04:55–06:15 | 1:20 | Follow-up timelines |
| 10 | 07:10–07:50 | 06:15–06:55 | 0:40 | The survival function |
| 11 | 07:50–08:50 | 06:55–07:55 | 1:00 | Illustrative Survival |
| 12 | 08:50–09:25 | 07:55–08:30 | 0:35 | How rapidly are defaults occurring now? |
| 13 | 09:25–10:30 | 08:30–09:35 | 1:05 | From a short interval to a hazard rate |
| 14 | 10:30–11:15 | Skip | 0:45 | From hazard to survival |
| 15 | 11:15–11:40 | 09:35–10:00 | 0:25 | From timing to borrower characteristics |
| 16 | 11:40–13:00 | 10:00–11:20 | 1:20 | The Cox model |
| 17 | 13:00–13:50 | 11:20–12:10 | 0:50 | Compare otherwise identical borrowers |
| 18 | 13:50–14:40 | 12:10–13:00 | 0:50 | Proportional Hazards |
| 19 | 14:40–15:40 | 13:00–14:00 | 1:00 | How does Cox learn relative effects? |
| 20 | 15:40–17:10 | 14:00–15:30 | 1:30 | Cox Risk Set |
| 21 | 17:10–18:10 | 15:30–16:30 | 1:00 | The audited Bondora cohort |
| 22 | 18:10–19:15 | 16:30–17:35 | 1:05 | Follow-up uses audited endpoints |
| 23 | 19:15–21:05 | 17:35–19:25 | 1:50 | Descriptive default timing |
| 24 | 21:05–22:00 | 19:25–20:20 | 0:55 | Five predictors and their contrasts |
| 25 | 22:00–23:10 | 20:20–21:30 | 1:10 | Adjusted Cox hazard ratios |
| 26 | 23:10–24:20 | 21:30–22:40 | 1:10 | New versus existing customer |
| 27 | 24:20–25:40 | 22:40–24:00 | 1:20 | Where interpretation is limited |
| 28 | 25:40–26:40 | 24:00–25:00 | 1:00 | When will a borrower default? |
| B1 | Backup | Backup | — | Backup: partial likelihood |
| B2 | Backup | Backup | — | Backup: corrected diagnostics |

## 1. When Will a Borrower Default? (00:00–00:20; short route: 00:00–00:20)

Introduce the lending question rather than the method. This is a standalone lecture for MSc Stochastics and Financial Mathematics students. We will use a small audited example to interpret default rates, not compare prediction algorithms. Advance promptly to the two borrowers.


## 2. Should these be the same outcome? (00:20–01:15; short route: 00:20–01:15)

Start with the exact question: One borrower defaults after three months, another after two years. Should we treat these as the same outcome? Show only the first borrower, then reveal the second and pause for three seconds. They share an eventual default label but expose the lender for very different lengths of time. Cash flows and time exposed to credit risk differ; no numerical loss calculation is needed. Reveal the final statement only after making this distinction. This is a rhetorical pause, not planned audience-question time.


## 3. Principal still outstanding (01:15–02:05; short route: 01:15–02:05)

Use a deliberately hypothetical principal-only schedule: twelve thousand euros, four hundred euros principal repaid each month. Explain the setup before revealing both balances. After three payments, 12000 minus 3 times 400 leaves 10800; after twenty-four payments, 2400 remains. Reveal the final interpretation only after the arithmetic. Earlier default can leave more principal outstanding, which makes timing economically relevant. This is not a calculation of actual credit loss: recoveries, interest and other factors are deliberately omitted. The hypothetical euro units are chosen for teaching, not inferred from Bondora.


## 4. What do six months tell us? (02:05–02:55; short route: 02:05–02:55)

For this actively observed hypothetical loan, six default-free months tell us T_D is greater than six months, not what its eventual value will be. Reveal the inequality and the risk-set contribution together after describing the history. This loan contributes to the exposed risk sets until its observation ends; it is not discarded and is not assumed to remain default-free forever. A closure would instead remove its exposure through a competing event. We cannot assign a certain individual default date from this partial history.


## 5. A binary label needs a horizon (02:55–03:45; short route: 02:55–03:45)

A conventional classifier can answer a perfectly legitimate fixed-horizon question, such as default within twelve months. The issue is not that classification is wrong: it is that a label requires the relevant horizon to be observed, or otherwise appropriately handled. An event observed before the horizon is known; a no-default label generally needs exposure through that horizon, with competing events addressed according to the intended target. Our six-month borrower does not yet supply that label. If already running long, skip the next worked-label slide and go directly to slide 7; this explanation is self-contained.


## 6. Which 12-month labels are known? (03:45–04:40; short route: Skip)

OPTIONAL: skip this entire slide to save 55 seconds. It elaborates slide 5 without introducing a new concept. First read the three histories with the answers hidden. Reveal the first two labels: a default at month three is inside the twelve-month horizon, and a default at month twenty-four implies event-free exposure through month twelve in these simple histories. Pause, then reveal Unknown for the loan only observed through six months. This borrower is not a negative training example just because no default has yet appeared. Resume with slide 7.


## 7. Why survival analysis? (04:40–05:25; short route: 03:45–04:30)

Connect both opening problems to the method. Time-to-event data retain event timing and can use incomplete right-censored histories under appropriate observation assumptions. This does not mean censoring can be ignored or that survival analysis is automatically unbiased. We choose Cox because a small set of relative-hazard effects is interpretable for this lecture. Survival analysis is a type of outcome framework, not the opposite of machine learning; ML survival methods also exist. We will not compare their predictive performance.


## 8. Choose the event and the clock (05:25–05:50; short route: 04:30–04:55)

Before writing any formula, specify the event and the start of the clock. Here the event is first recorded default and the origin is loan issuance. The illustrations use months; the audited example uses days. Some histories stop before a default is seen, and we need to distinguish why they stop. Move directly to the timelines.


## 9. Follow-up timelines (05:50–07:10; short route: 04:55–06:15)

Use the same hypothetical borrowers as in the opening: A defaults at three months and B at twenty-four. C is still active when observation ends at six months: this is right censoring. We know only that it remained default-free through the observed period. Add D, which closes at twelve months: closure is a competing event ending default exposure, not simply failure to keep observing an active loan. Point to the cross, censoring bar and closure diamond in turn. The whole figure is static; do not click expecting internal reveals. For interpreting the default rate, remove a closed loan from the exposed risk set. Appropriate administrative-censoring assumptions still matter.


## 10. The survival function (07:10–07:50; short route: 06:15–06:55)

We now have a reason to introduce notation. Let T_D be time to default in a simplified world without competing closure. Read S(t) as the probability that the event has not happened by t. Reveal the plain-language interpretation after reading the equation. Survival is the technical term for remaining event-free; it does not imply anything about the borrower outside this defined event.


## 11. Illustrative Survival (07:50–08:50; short route: 06:55–07:55)

This curve is hypothetical, not a Bondora estimate. Start at one on the vertical axis and move right along elapsed months. Trace the month-twelve guide up to the curve, then across to about 0.79. Pause for three seconds so the audience can read the guides. About 79 percent remain default-free at twelve months in this default-only example. The formula exp(-0.02t) uses t in months. The same plot is already visible throughout this frame; guide attention verbally rather than pretending it animates.


## 12. How rapidly are defaults occurring now? (08:50–09:25; short route: 07:55–08:30)

Introduce hazard in ordinary language before the limit definition. Restrict attention to loans still exposed at the current time and ask about the rate of imminent defaults. It is a local rate, not the fraction that will eventually default. Reveal the term hazard after that intuition. If time is measured in months, its units are inverse months. The next equation formalises this same question rather than introducing a different object.


## 13. From a short interval to a hazard rate (09:25–10:30; short route: 08:30–09:35)

Read the numerator first: conditional on no default yet, what is the chance of default in the next small interval? Divide by its length and shrink the interval to obtain a rate. Do not explain every symbol as a separate reveal. Once the definition is explained, reveal the short-interval approximation. For the earlier curve a constant hazard of 0.02 per month gives an approximate 0.02 one-month conditional probability, with exact value 1-exp(-0.02), about 0.0198. Do not multiply a rate over a long horizon as though it were an exact probability. If running long, skip slide 14 and go directly to borrower characteristics on slide 15.


## 14. From hazard to survival (10:30–11:15; short route: Skip)

OPTIONAL: skip this entire slide to save 45 seconds. It connects two already introduced objects. H accumulates the hazard over time and, in the default-only setting, S equals exp(-H). For the illustrative constant rate, H(t)=0.02t, giving the earlier curve. Reveal the survival equation only after the integral. With competing closure, exp(-H_D) is not the actual event-free survival or actual default probability: those depend on the competing process too. No cumulative-incidence analysis is being added. Continue with slide 15; it does not rely on H notation.


## 15. From timing to borrower characteristics (11:15–11:40; short route: 09:35–10:00)

Make the progression explicit: We have described event timing. Now we want to understand how it differs between borrowers. Age, income or customer status may be associated with different rates. This motivates adding characteristics to a time-dependent baseline. Later the worked example will make the same distinction empirically: unadjusted timing curves describe accumulation, while Cox describes adjusted relative rates among exposed loans. No new regression is introduced.


## 16. The Cox model (11:40–13:00; short route: 10:00–11:20)

Show the whole equation first and read it as baseline times a positive covariate multiplier. Reveal the baseline explanation and point to h_0(t): we do not require a constant hazard or choose a fixed parametric shape here. It represents the rate at reference covariates. Then reveal the multiplier explanation: exp(beta transpose x) scales that rate. In the audited example the object is the cause-specific default hazard among loans neither defaulted nor closed, and the baseline is allowed to differ by origination year. Borrower coefficients are shared across those strata.


## 17. Compare otherwise identical borrowers (13:00–13:50; short route: 11:20–12:10)

The baseline cancels for two otherwise identical borrowers in the same baseline stratum. The customer indicator differs by one, so their relative hazard is exp(beta_new). Explain the equation before revealing the illustrative value of 1.5. That means a fifty percent higher instantaneous rate, not fifty percentage points or a fifty percent higher default probability over a horizon. This value is hypothetical and is not the final Bondora estimate. Under PH the ratio remains constant, even though both hazards may vary, as the next picture shows.


## 18. Proportional Hazards (13:50–14:40; short route: 12:10–13:00)

First follow A's curve, then B's. Both rates change over time; B stays one and a half times A. Point to the right panel showing the flat ratio. Pause briefly to let the audience compare the changing left panel with the constant right panel. Proportional hazards concerns the ratio, not constancy of either rate. These curves are hypothetical, not evidence that the assumption holds for Bondora. The plot is static throughout this frame.


## 19. How does Cox learn relative effects? (14:40–15:40; short route: 13:00–14:00)

Introduce a separate teaching risk set, not the original three opening histories. All borrowers are still exposed just before this default time, in the same baseline stratum, and other covariates are identical. Their weights are one, one and exp(beta). Explain that we condition on one default occurring and ask which borrower it belongs to. Ask rhetorically what fraction of the total weight belongs to C, then pause for three seconds. Do not advance to the worked answer until the setup is understood.


## 20. Cox Risk Set (15:40–17:10; short route: 14:00–15:30)

Now show the answer: C's conditional share is exp(beta) divided by 2+exp(beta). Point to the symbolic expression before explaining the numerical example. With beta=log(2), chosen only for illustration, the weights are one, one and two, so C receives half of the total weight. Pause to allow the arithmetic to settle. This is conditional on one event occurring now, not a probability of default over a horizon. Cox combines comparisons like this across observed event times to estimate relative effects; the common baseline cancels. Full partial likelihood and the existing Efron handling of tied daily defaults are left to backup notes.


## 21. The audited Bondora cohort (17:10–18:10; short route: 15:30–16:30)

Move clearly from hypothetical teaching examples to empirical data. The audited analysis retains 9,844 loans, 6,924 borrowers and 2,508 recorded defaults within 730 days. Reveal these counts after defining the country, origination years and horizon. The cutoff is the explicitly recorded ReportAsOfEOD of 20 July 2021, not the latest observed default or the file creation date. All origination dates have at least 730 days of potential observation. The event count is descriptive, not a model-predicted horizon probability.


## 22. Follow-up uses audited endpoints (18:10–19:15; short route: 16:30–17:35)

Keep this operational definition short. A later repaid status does not erase an earlier recorded default. ContractEndDate occurs on Current and Late loans too and can be a future date, so not every such value is a repayment. The audit restricts the nondefault exit to a closure proxy in loans labeled Repaid; write-offs mean this still need not be literal full cash repayment. The general stopping rule also includes reporting cutoff, but for this cohort the 730-day cap comes first. Keep the uncertainty about the source's arrears threshold explicit; do not assert a sixty- or ninety-day definition.


## 23. Descriptive default timing (19:15–21:05; short route: 17:35–19:25)

Move from endpoint definitions to when the recorded defaults accumulate. These are unadjusted descriptive cumulative-incidence curves, using Aalen–Johansen with the audited closure proxy as a competing event. The vertical axis is the estimated proportion of loans experiencing recorded default by each time before a competing closure. Point to twelve months: about 14.3 percent for new-customer loans and 9.9 percent for existing-customer loans. At twenty-four months the figures are about 27.4 and 21.2 percent. Read one horizon slowly rather than listing every number. The at-risk table includes observed loans immediately before each grid time. The month scale maps 730 days to 24 months. All have full potential follow-up, so these point estimates also agree with directly counted event fractions. No bands are shown: repeated borrowers are present and no independence-based uncertainty is being presented. New and existing customers differ in other covariates and vintages; these descriptive differences are not causal and are not the adjusted Cox HR. The next covariates/HR slides answer the complementary question about conditional rates.


## 24. Five predictors and their contrasts (21:05–22:00; short route: 19:25–20:20)

Read these as comparison units, not raw coefficient sizes. The model uses log income, and multiplying its coefficient by log(2) gives the displayed doubling contrast. Original scheduled term is reconstructed from FirstPaymentDate to MaturityDate_Original assuming monthly installments, not from revised maturity. Amount and income are used as recorded; the existing plot's euro label has the report's unverified-currency qualification. Baseline hazards differ by origination year and intervals cluster repeated borrowers. We use this one existing Cox model; no predictors, fits or selection procedures are added.


## 25. Adjusted Cox hazard ratios (22:00–23:10; short route: 20:20–21:30)

Now ask which characteristics are associated with the conditional rate, adjusting for the included covariates and origination-year baseline. This cleaner figure reads the same final audited coefficients and borrower-clustered 95 percent intervals; none were refitted. Orient the audience to one and the logarithmic scale. Contrast it explicitly with the preceding unadjusted timing graph: these hazard ratios are adjusted relative rates among exposed loans, not differences or ratios of cumulative incidences. Exact predictor contrasts remain visible. Daily ties make the intervals approximate, and age/new-customer PH concerns remain visible. Detailed nonlinearity, diagnostic and source-definition caveats follow in limitations and backup notes.


## 26. New versus existing customer (23:10–24:20; short route: 21:30–22:40)

Show and explain the estimate first. On the next reveal, subtract one from the unrounded 1.4445 and convert to about forty-four percent. This is a conditional instantaneous default rate among loans still exposed, adjusting for the included covariates and origination-year baseline. It is not forty-four percentage points, a default-probability ratio or a causal effect of being new. The corrected diagnostics flag new-customer PH concerns in the full sample, so the single constant HR compresses a possibly time-varying association. Give that qualification before moving to general limitations.


## 27. Where interpretation is limited (24:20–25:40; short route: 22:40–24:00)

One short point per reveal. Corrected elapsed-rank and log-time diagnostics flag age and new-customer status; the superseded original-term PH finding is not repeated. Age also shows nonlinearity, while term has a borderline nonlinear departure, a separate assumption. Daily ties make the borrower-clustered Wald intervals approximate. The full-sample PH tests are approximate and not cluster adjusted. The source arrears threshold, full-repayment timing, monetary measurement definitions and original monthly-schedule proxy remain qualified. Detailed p-values and sensitivity checks are in backup material; do not turn this into a new modelling exercise.


## 28. When will a borrower default? (25:40–26:40; short route: 24:00–25:00)

Return to the title and opening borrowers. A three-month default and a two-year default occur after different amounts of exposure and repayment; six observed default-free months do not reveal an eventual event date. We cannot assign certainty to an individual date, but we can describe accumulation: by 24 months about 27.4 percent of new-customer loans and 21.2 percent of existing-customer loans have a recorded default under the audited closure proxy. That comparison is unadjusted. Separately the unchanged Cox HR of 1.445 relates new-customer status to the adjusted conditional default rate, with its PH qualification. Cox is not inherently unable to estimate survival: with a fitted baseline it can do so in a default-only setting. Actual default probabilities under competing closure require accounting for both events. No predictive accuracy has been evaluated. End the speaking plan here and invite questions; questions and backups are outside the timing.


## B1. Backup: partial likelihood (Backup; short route: Backup)

Each factor is the conditional probability of the observed defaulting identity given one event in that stratum's risk set. The baseline cancels and we combine contributions over event times. Censoring and closure affect who is in the risk set. The formula is schematic for untied events; do not imply it is the exact tied-data likelihood used by the existing software.


## B2. Backup: corrected diagnostics (Backup; short route: Backup)

These are the existing audited diagnostics, not newly run tests. In year-stratified fits the software's cumulative row-order rank is unsafe; corrected elapsed ranks remove the apparent original-term departure. Nonlinearity and proportional hazards are different questions. No multiplicity correction or omnibus cluster-adjusted PH test is claimed. The one-loan sample is 95.05 percent new customer compared with 69.47 percent in the primary sample; its new-customer interval widens and income/term effects attenuate. Source files are REPORT.md and the audited diagnostic CSVs.

# Audience questions — outside planned speaking time

**Does this predict an individual default date?** No certain date is assigned. The new graph describes loan-level recorded-default incidence under the audited closure proxy. The Cox model describes adjusted conditional default rates. Cox can estimate survival after estimating its baseline in a default-only setting; actual default probabilities with competing closure require both event processes. None of these curves is a validated individual prediction here.

**Why not just use a binary classifier?** A classifier can target default within a specified horizon, but labels require suitable follow-up and competing-event definitions. Time-to-event methods retain timing and can use right-censored histories under suitable assumptions. ML methods can also model survival; no performance superiority is claimed.

**What differs between the timing curves and Cox hazard ratios?** The Aalen–Johansen curves are unadjusted proportions of loans experiencing recorded default by each time, with closure as a competing event. The HRs adjust for the included covariates and origination-year baseline, comparing instantaneous default rates among loans still exposed. Differences between the curves are not adjusted effects, and the HR is not a ratio of the plotted proportions.

**Why does closure differ from observation ending?** Closure ends this loan's default exposure and is a competing event. Administrative censoring ends observation of an otherwise exposed loan without declaring an event. Both remove loans from later cause-specific risk sets, but only closure receives competing-event probability mass in the cumulative-incidence calculation. Treating closures as censoring in 1−KM does not estimate actual default incidence.

**Why retain Cox when some PH assumptions are doubtful?** It is a compact explanatory summary of relative-rate associations, not a claim that every effect is constant in truth. The existing diagnostics flag age and new-customer PH concerns and age nonlinearity, with a borderline term nonlinear departure. These limit interpretation; they do not justify hiding the diagnostics or introducing more models into this lecture. Intervals remain approximate with tied daily dates.

**Have we evaluated predictive accuracy?** No. No validation of individual predictions, calibration, discrimination or out-of-sample performance is reported. This remains an explanatory lecture with descriptive timing curves and an unchanged audited Cox example. Point estimates are checked, not claims of forecasting accuracy.
