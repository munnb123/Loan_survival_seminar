# Speaker notes — Luke Munnelly

Standalone lecture for MSc Stochastics and Financial Mathematics students. **30 logical slides: 28 teaching slides, Sources, then Questions.** Use the **25:00 speaking route**, skipping slides 6 (55 seconds) and 14 (45 seconds) if delivering in the 25-minute slot. Including both explanations gives a calm 26:40 plan. Optional-skip guidance and timing are notes-only; no rehearsal labels or backup frames appear in either audience PDF. Sources take 20 seconds within the speaking plan; audience questions are outside it. Timings include the indicated pauses and figure reading. The presentation has 57 overlay-expanded pages; the handout has 30 pages, one per logical slide.

## Practical 25-minute route

- After slide 5, skip optional slide 6 and resume slide 7 on presentation PDF page 15.
- After slide 13, skip optional slide 14 and resume slide 15 on presentation PDF page 29.
- These transitions are self-contained: slide 5 already explains the horizon issue, and slide 15 requires no cumulative-hazard notation.
- Do not rush the opening, graph reading or conditional risk-set calculation. If nervous, take the scripted short pauses rather than filling them with extra material.
- Risk-set setup is slide 19; the static worked-answer figure is slide 20. The descriptive timing curve is slide 23; the adjusted Cox HR plot is slide 25.

## Schedule

| Slide | Full-plan time | 25-minute route | Duration | Topic |
| --- | --- | --- | --- | --- |
| 1 | 00:00–00:15 | 00:00–00:15 | 0:15 | When Will a Borrower Default? |
| 2 | 00:15–01:10 | 00:15–01:10 | 0:55 | Should these be the same outcome? |
| 3 | 01:10–01:55 | 01:10–01:55 | 0:45 | Principal still outstanding |
| 4 | 01:55–02:45 | 01:55–02:45 | 0:50 | What do six months tell us? |
| 5 | 02:45–03:35 | 02:45–03:35 | 0:50 | A binary label needs a horizon |
| 6 | 03:35–04:30 | Skip | 0:55 | Which 12-month labels are known? |
| 7 | 04:30–05:15 | 03:35–04:20 | 0:45 | Why survival analysis? |
| 8 | 05:15–05:40 | 04:20–04:45 | 0:25 | Choose the event and the clock |
| 9 | 05:40–07:00 | 04:45–06:05 | 1:20 | Follow-up timelines |
| 10 | 07:00–07:40 | 06:05–06:45 | 0:40 | The survival function |
| 11 | 07:40–08:40 | 06:45–07:45 | 1:00 | Illustrative Survival |
| 12 | 08:40–09:15 | 07:45–08:20 | 0:35 | How rapidly are defaults occurring now? |
| 13 | 09:15–10:20 | 08:20–09:25 | 1:05 | From a short interval to a hazard rate |
| 14 | 10:20–11:05 | Skip | 0:45 | From hazard to survival |
| 15 | 11:05–11:30 | 09:25–09:50 | 0:25 | From timing to borrower characteristics |
| 16 | 11:30–12:50 | 09:50–11:10 | 1:20 | The Cox model |
| 17 | 12:50–13:40 | 11:10–12:00 | 0:50 | Compare otherwise identical borrowers |
| 18 | 13:40–14:30 | 12:00–12:50 | 0:50 | Proportional Hazards |
| 19 | 14:30–15:30 | 12:50–13:50 | 1:00 | How does Cox learn relative effects? |
| 20 | 15:30–17:00 | 13:50–15:20 | 1:30 | Cox Risk Set |
| 21 | 17:00–18:00 | 15:20–16:20 | 1:00 | The audited Bondora cohort |
| 22 | 18:00–19:05 | 16:20–17:25 | 1:05 | Follow-up uses audited endpoints |
| 23 | 19:05–20:45 | 17:25–19:05 | 1:40 | Descriptive default timing |
| 24 | 20:45–21:40 | 19:05–20:00 | 0:55 | From timing curves to adjusted rates |
| 25 | 21:40–22:50 | 20:00–21:10 | 1:10 | Adjusted Cox hazard ratios |
| 26 | 22:50–24:00 | 21:10–22:20 | 1:10 | New versus existing customer |
| 27 | 24:00–25:20 | 22:20–23:40 | 1:20 | Where interpretation is limited |
| 28 | 25:20–26:20 | 23:40–24:40 | 1:00 | Conclusion |
| 29 | 26:20–26:40 | 24:40–25:00 | 0:20 | Sources |
| 30 | Discussion — outside speaking time | Discussion — outside speaking time | — | Questions? |

## 1. When Will a Borrower Default? (00:00–00:15; short route: 00:00–00:15)

Introduce the lending question rather than the method. This is a standalone lecture for MSc Stochastics and Financial Mathematics students. We will use a small audited example to interpret default rates, not compare prediction algorithms. Advance promptly to the two borrowers.


## 2. Should these be the same outcome? (00:15–01:10; short route: 00:15–01:10)

Start with the exact question: One borrower defaults after three months, another after two years. Should we treat these as the same outcome? Show only the first borrower, then reveal the second and pause for three seconds. They share an eventual default label but expose the lender for very different lengths of time. Cash flows and time exposed to credit risk differ; no numerical loss calculation is needed. Reveal the final statement only after making this distinction. This is a rhetorical pause, not planned audience-question time.


## 3. Principal still outstanding (01:10–01:55; short route: 01:10–01:55)

Use a deliberately hypothetical principal-only schedule: twelve thousand euros, four hundred euros principal repaid each month. Explain the setup before revealing both balances. After three payments, 12000 minus 3 times 400 leaves 10800; after twenty-four payments, 2400 remains. Reveal the final interpretation only after the arithmetic. Earlier default can leave more principal outstanding, which makes timing economically relevant. This is not a calculation of actual credit loss: recoveries, interest and other factors are deliberately omitted. The hypothetical euro units are chosen for teaching, not inferred from Bondora.


## 4. What do six months tell us? (01:55–02:45; short route: 01:55–02:45)

For this actively observed hypothetical loan, six default-free months tell us T_D is greater than six months, not what its eventual value will be. Reveal the inequality and the observation-information statement together after describing the history. Save the term risk set for the later Cox estimation explanation. Use the loan's six months of observed exposure; it is not discarded and is not assumed to remain default-free forever. A closure would instead remove its exposure through a competing event. We cannot assign a certain individual default date from this partial history.


## 5. A binary label needs a horizon (02:45–03:35; short route: 02:45–03:35)

A conventional classifier can answer a perfectly legitimate fixed-horizon question, such as default within twelve months. The issue is not that classification is wrong: it is that a label requires the relevant horizon to be observed, or otherwise appropriately handled. An event observed before the horizon is known; a no-default label generally needs exposure through that horizon, with competing events addressed according to the intended target. Our six-month borrower does not yet supply that label. If already running long, skip the next worked-label slide and go directly to slide 7; this explanation is self-contained.


## 6. Which 12-month labels are known? (03:35–04:30; short route: Skip)

OPTIONAL: skip this entire slide to save 55 seconds. It elaborates slide 5 without introducing a new concept. First read the three histories with the answers hidden. Reveal the first two labels: a default at month three is inside the twelve-month horizon, and a default at month twenty-four implies event-free exposure through month twelve in these simple histories. Pause, then reveal Unknown for the loan only observed through six months. This borrower is not a negative training example just because no default has yet appeared. Resume with slide 7.


## 7. Why survival analysis? (04:30–05:15; short route: 03:35–04:20)

Connect both opening problems to the method. Time-to-event data retain event timing and can use incomplete right-censored histories under appropriate observation assumptions. This does not mean censoring can be ignored or that survival analysis is automatically unbiased. We choose Cox because a small set of relative-hazard effects is interpretable for this lecture. Survival analysis is a type of outcome framework, not the opposite of machine learning; ML survival methods also exist. We will not compare their predictive performance.


## 8. Choose the event and the clock (05:15–05:40; short route: 04:20–04:45)

Before writing any formula, specify the event and the start of the clock. Here the event is first recorded default and the origin is loan issuance. The illustrations use months; the audited example uses days. Some histories stop before a default is seen, and we need to distinguish why they stop. Move directly to the timelines.


## 9. Follow-up timelines (05:40–07:00; short route: 04:45–06:05)

Use the same hypothetical borrowers as in the opening: A defaults at three months and B at twenty-four. C is still active when observation ends at six months: this is right censoring. We know only that it remained default-free through the observed period. Add D, which closes at twelve months: closure is a competing event ending default exposure, not simply failure to keep observing an active loan. Point to the cross, censoring bar and closure diamond in turn. The whole figure is static; do not click expecting internal reveals. For interpreting the default rate, remove a closed loan from the exposed risk set. Appropriate administrative-censoring assumptions still matter.


## 10. The survival function (07:00–07:40; short route: 06:05–06:45)

We now have a reason to introduce notation. Let T_D be time to default in a simplified world without competing closure. Read S(t) as the probability that the event has not happened by t. Reveal the plain-language interpretation after reading the equation. Survival is the technical term for remaining event-free; it does not imply anything about the borrower outside this defined event.


## 11. Illustrative Survival (07:40–08:40; short route: 06:45–07:45)

This curve is hypothetical, not a Bondora estimate. Start at one on the vertical axis and move right along elapsed months. Trace the month-twelve guide up to the curve, then across to about 0.79. Pause for three seconds so the audience can read the guides. About 79 percent remain default-free at twelve months in this default-only example. The formula exp(-0.02t) uses t in months. The same plot is already visible throughout this frame; guide attention verbally rather than pretending it animates.


## 12. How rapidly are defaults occurring now? (08:40–09:15; short route: 07:45–08:20)

Introduce hazard in ordinary language before the limit definition. Restrict attention to loans still exposed at the current time and ask about the rate of imminent defaults. It is a local rate, not the fraction that will eventually default. Reveal the term hazard after that intuition. If time is measured in months, its units are inverse months. The next equation formalises this same question rather than introducing a different object.


## 13. From a short interval to a hazard rate (09:15–10:20; short route: 08:20–09:25)

Read the numerator first: conditional on no default yet, what is the chance of default in the next small interval? Divide by its length and shrink the interval to obtain a rate. Do not explain every symbol as a separate reveal. Once the definition is explained, reveal the short-interval approximation. For the earlier curve a constant hazard of 0.02 per month gives an approximate 0.02 one-month conditional probability, with exact value 1-exp(-0.02), about 0.0198. Do not multiply a rate over a long horizon as though it were an exact probability. If running long, skip slide 14 and go directly to borrower characteristics on slide 15.


## 14. From hazard to survival (10:20–11:05; short route: Skip)

OPTIONAL: skip this entire slide to save 45 seconds. It connects two already introduced objects. H accumulates the hazard over time and, in the default-only setting, S equals exp(-H). For the illustrative constant rate, H(t)=0.02t, giving the earlier curve. Reveal the survival equation only after the integral. With competing closure, exp(-H_D) is not the actual event-free survival or actual default probability: those depend on the competing process too. This equation is not the empirical cumulative-incidence calculation. Continue with slide 15; it does not rely on H notation.


## 15. From timing to borrower characteristics (11:05–11:30; short route: 09:25–09:50)

Make the progression explicit: We have described event timing. Now we want to understand how it differs between borrowers. Age, income or customer status may be associated with different rates. This motivates adding characteristics to a time-dependent baseline. Later the worked example will make the same distinction empirically: unadjusted timing curves describe accumulation, while Cox describes adjusted relative rates among exposed loans. No new regression is introduced.


## 16. The Cox model (11:30–12:50; short route: 09:50–11:10)

Show the whole equation first and read it as baseline times a positive covariate multiplier. Reveal the baseline explanation and point to h_0(t): we do not require a constant hazard or choose a fixed parametric shape here. It represents the rate at reference covariates. Then reveal the multiplier explanation: exp(beta transpose x) scales that rate. In the audited example the object is the cause-specific default hazard among loans neither defaulted nor closed, and the baseline is allowed to differ by origination year. Borrower coefficients are shared across those strata.


## 17. Compare otherwise identical borrowers (12:50–13:40; short route: 11:10–12:00)

The baseline cancels for two otherwise identical borrowers in the same baseline stratum. The customer indicator differs by one, so their relative hazard is exp(beta_new). Explain the equation before revealing the illustrative value of 1.5. That means a fifty percent higher instantaneous rate, not fifty percentage points or a fifty percent higher default probability over a horizon. This value is hypothetical and is not the final Bondora estimate. Under PH the ratio remains constant, even though both hazards may vary, as the next picture shows.


## 18. Proportional Hazards (13:40–14:30; short route: 12:00–12:50)

First follow A's curve, then B's. Both rates change over time; B stays one and a half times A. Point to the right panel showing the flat ratio. Pause briefly to let the audience compare the changing left panel with the constant right panel. Proportional hazards concerns the ratio, not constancy of either rate. These curves are hypothetical, not evidence that the assumption holds for Bondora. The plot is static throughout this frame.


## 19. How does Cox learn relative effects? (14:30–15:30; short route: 12:50–13:50)

Introduce a separate teaching example, not the original three opening histories. Call the collection of exposed borrowers just before this default a risk set. All borrowers are still exposed just before this default time, in the same baseline stratum, and other covariates are identical. Their weights are one, one and exp(beta). Explain that we condition on one default occurring and ask which borrower it belongs to. Ask rhetorically what fraction of the total weight belongs to C, then pause for three seconds. Do not advance to the worked answer until the setup is understood.


## 20. Cox Risk Set (15:30–17:00; short route: 13:50–15:20)

Now show the answer: C's conditional share is exp(beta) divided by 2+exp(beta). Point to the symbolic expression before explaining the numerical example. With beta=log(2), chosen only for illustration, the weights are one, one and two, so C receives half of the total weight. Pause to allow the arithmetic to settle. This is conditional on one event occurring now, not a probability of default over a horizon. Cox combines comparisons like this across observed event times to estimate relative effects; the common baseline cancels. Full partial likelihood and the existing Efron handling of tied daily defaults are left to speaker notes.


## 21. The audited Bondora cohort (17:00–18:00; short route: 15:20–16:20)

Move clearly from hypothetical teaching examples to empirical data. The audited analysis retains 9,844 loans, 6,924 borrowers and 2,508 recorded defaults within 730 days. Reveal these counts after defining the country, origination years and horizon. The cutoff is the explicitly recorded ReportAsOfEOD of 20 July 2021, not the latest observed default or the file creation date. All origination dates have at least 730 days of potential observation. The event count is descriptive, not a model-predicted horizon probability.


## 22. Follow-up uses audited endpoints (18:00–19:05; short route: 16:20–17:25)

Use ordinary language on the slide. The first recorded default is DefaultDate. The recorded contract ending is ContractEndDate only when snapshot Status=Repaid. A later repaid label does not erase an earlier default; the audit retains first-default timing. ContractEndDate also occurs on Current and Late loans, sometimes in the future, so do not treat every contract date as actual repayment. The general stopping rule also includes the reporting cutoff, but every analyzed loan can reach the 730-day cap first. Closure remains a competing-event proxy and can coexist with write-offs. The source's exact default arrears threshold is unverified. No endpoint or boundary rule has changed.


## 23. Descriptive default timing (19:05–20:45; short route: 17:25–19:05)

Move from endpoint definitions to when the recorded defaults accumulate. These are unadjusted descriptive cumulative-incidence curves, using Aalen–Johansen with the audited closure proxy as a competing event. The vertical axis is the estimated proportion of loans experiencing recorded default by each time before a competing closure. Point to twelve months: about 14.3 percent for new-customer loans and 9.9 percent for existing-customer loans. At twenty-four months the figures are about 27.4 and 21.2 percent. Read one horizon slowly rather than listing every number. The at-risk table includes observed loans immediately before each grid time. The month scale maps 730 days to 24 months. All have full potential follow-up, so these point estimates also agree with directly counted event fractions. No bands are shown: repeated borrowers are present and no independence-based uncertainty is being presented. New and existing customers differ in other covariates and vintages; these descriptive differences are not causal and are not the adjusted Cox HR. The next covariates/HR slides answer the complementary question about conditional rates.


## 24. From timing curves to adjusted rates (20:45–21:40; short route: 19:05–20:00)

Make the distinction explicit: The timing curves show unadjusted differences between customer groups. Cox regression compares their default rates while accounting for the other included characteristics. The descriptive curves are not Cox predictions. On the first reveal refer back to the new/existing customer groups; on the second introduce adjustment and the five contrasts together. Read these as comparison units: age per ten years, income doubling, amount per thousand recorded monetary units, original scheduled term per twelve months and new versus existing customer. Income uses a log transform; the doubling contrast rescales the coefficient by log(2). Original term comes from FirstPaymentDate to MaturityDate_Original assuming monthly installments, not revised maturity. Currency/income-period definitions remain unverified.


## 25. Adjusted Cox hazard ratios (21:40–22:50; short route: 20:00–21:10)

Now ask which characteristics are associated with the conditional rate, adjusting for the included covariates and origination-year baseline. This cleaner figure reads the same final audited coefficients and borrower-clustered 95 percent intervals; none were refitted. Explain the plot symbols once here: dots are hazard-ratio estimates, and bars are approximate borrower-clustered 95 percent confidence intervals. Orient the audience to one and the logarithmic scale. Contrast it explicitly with the preceding unadjusted timing graph: these hazard ratios are adjusted relative rates among exposed loans, not differences or ratios of cumulative incidences. Exact predictor contrasts remain visible. Daily ties make the intervals approximate, and age/new-customer proportional-hazards concerns remain on the limitations slide and in the notes. Detailed nonlinearity, diagnostic and source-definition caveats follow in limitations and speaker notes.


## 26. New versus existing customer (22:50–24:00; short route: 21:10–22:20)

Show and explain the estimate first. On the next reveal, subtract one from the unrounded 1.4445 and convert to about forty-four percent. This is a conditional instantaneous default rate among loans still exposed, adjusting for the included covariates and origination-year baseline. It is not forty-four percentage points, a default-probability ratio or a causal effect of being new. The corrected diagnostics flag new-customer PH concerns in the full sample, so the single constant HR compresses a possibly time-varying association. Give that qualification before moving to general limitations.


## 27. Where interpretation is limited (24:00–25:20; short route: 22:20–23:40)

One short point per reveal. Corrected elapsed-rank and log-time diagnostics flag age and new-customer status; the superseded original-term PH finding is not repeated. Age also shows nonlinearity, while term has a borderline nonlinear departure, a separate assumption. Daily ties make the borrower-clustered Wald intervals approximate. The full-sample PH tests are approximate and not cluster adjusted. The source arrears threshold, full-repayment timing, monetary measurement definitions and original monthly-schedule proxy remain qualified. Detailed p-values and sensitivity checks are in the speaker notes; do not turn this into a new modelling exercise.


## 28. Conclusion (25:20–26:20; short route: 23:40–24:40)

Answer the opening question in three calm steps. First, the observed accumulation: by the study's two-year, 730-day horizon, recorded default reached about 27.4 percent for new-customer loans and 21.2 percent for existing-customer loans. These are unadjusted loan-level descriptive estimates under the audited closure proxy. Second, the separate adjusted association: the unchanged new-customer hazard ratio is 1.4445, displayed as 1.445, or about 44 percent higher conditional default hazard among exposed loans. This is not a ratio of the two cumulative proportions or a causal effect. Third, describe patterns over time without assigning a certain individual default date. Keep detailed qualifications in the notes; do not read them all aloud. Cox can estimate survival with its baseline in a default-only setting; actual probabilities with competing closure need both event processes. Advance to Sources briefly, then leave the separate Questions slide visible during discussion.


## 29. Sources (26:20–26:40; short route: 24:40–25:00)

Cover sources briefly rather than reading every citation. The actual dataset is Bondora Peer to Peer Lending Loan Data, distributed on Kaggle by sid321axn, with the 20 July 2021 reporting snapshot used here. Cox's 1972 paper supplies the regression model; Aalen and Johansen's 1978 paper supplies the transition-probability estimator; Putter, Fiocco and Geskus's 2007 tutorial supports the competing-risk interpretation. Full titles and bibliographic verification are in references.md. The repository link provides the exact audited numerical outputs and reproducible code. No course-note document was supplied in the available files, and no course-note author is inferred. End the speaking plan after this brief acknowledgement and advance to Questions.


## 30. Questions? (Discussion — outside speaking time; short route: Discussion — outside speaking time)

Discussion is outside the planned speaking time. Leave this minimal slide on screen throughout questions. Do not advance to a list of anticipated questions or to backup frames; the useful answers and detailed method/diagnostic notes are in questions.md and the generated speaker_notes.md.

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

# Sources and bibliographic verification

The short Sources slide uses author/year and compact publication details; full references and the evidence checked for this polish are below. Links are provided here rather than displayed as a wall of URLs in the talk. No statistical analysis was rerun.

## Dataset actually analysed

**Bondora. _Bondora Peer to Peer Lending Loan Data_.** Kaggle distribution by **Manu Siddhartha**, account `sid321axn`, updated 23 July 2021. [Dataset record](https://www.kaggle.com/datasets/sid321axn/bondora-peer-to-peer-lending-loan-data).

The actual input used in this repository is `LoanData_Bondora.csv`, filtered by the user to Estonian originations in 2013–2015 and supplied as `Bondora_Estonia_2013_2015.csv.gz`. The report's cutoff is **20 July 2021**, taken from `ReportAsOfEOD` in the data. The Kaggle upload/update date is not that cutoff. The dataset record names Bondora as the data source and currently reports CC0. The repository's audited input SHA-256 remains `52e847936a33fb3f9ab7a0901f662a624ed747a9c4c081f490dd0c1f3786798a`.

Verification: the [Kaggle dataset API record](https://www.kaggle.com/api/v1/datasets/view/sid321axn/bondora-peer-to-peer-lending-loan-data) was successfully retrieved during this polish. Title, distributor/account, update timestamp and dataset description were checked against that response. The reporting cutoff and actual analysed file are verified by the existing report/provenance, not inferred from the API timestamp.

## Principal methods and supporting paper

1. **Cox, D. R. (1972).** Regression models and life-tables (with discussion). _Journal of the Royal Statistical Society, Series B_, **34**, 187–220. Principal reference for Cox regression and its risk-set/partial-likelihood interpretation.

   Bibliographic details checked against entry `Cox72` in the maintained `survival` package bibliography: [pinned source](https://github.com/therneau/survival/blob/b76de62301f2ed4efcdbd8c062acc6759a54e511/vignettes/refer.bib). The author, year, title, journal abbreviation, volume and pages agree. No unchecked issue or DOI is asserted here.

2. **Aalen, O., and Johansen, S. (1978).** An empirical transition matrix for non-homogeneous Markov chains based on censored observations. _Scandinavian Journal of Statistics_, **5**, 141–150. Principal reference for the empirical transition-matrix estimator underlying the descriptive competing-risk cumulative incidence.

   Bibliographic details checked against the [CRAN `etm` function reference](https://github.com/cran/etm/blob/db40647f7f522b67434a3eb635e89c0dee1ecc23/man/etm.Rd), which gives the authors, full title, year, journal, volume and pages. The product-integral/state-probability interpretation was also consulted in the maintained `survival` vignette [Multi-state models and competing risks](https://github.com/therneau/survival/blob/b76de62301f2ed4efcdbd8c062acc6759a54e511/vignettes/compete.Rnw). This is a methodological citation; the repository uses its existing deterministic daily-tie implementation, not the R package.

3. **Putter, H., Fiocco, M., and Geskus, R. B. (2007).** Tutorial in biostatistics: Competing risks and multi-state models. _Statistics in Medicine_, **26**, 2389–2430. Supporting paper for distinguishing cause-specific rates, competing exits and cumulative incidence.

   Bibliographic details checked against entry `Tut` in the author's `mstate` repository: [pinned bibliography](https://github.com/hputter/mstate/blob/406e5856790c1649a7bcf03fff9a0afa247e7265/vignettes/Tutorial.bib). The companion [author-written tutorial](https://github.com/hputter/mstate/blob/406e5856790c1649a7bcf03fff9a0afa247e7265/vignettes/Tutorial.Rnw) explicitly identifies this paper and discusses the Aalen–Johansen estimator. The authors, title, year, journal, volume and pages were cross-checked with `survival`'s bibliography.

Publisher/JSTOR/Crossref requests were blocked by the environment's network proxy; bibliographic verification therefore used the accessible maintained package/author sources above. Full original papers were not downloaded. This limitation does not affect the audited numerical outputs. Unverified DOI/issue fields and unrelated papers have been omitted rather than guessed.

## Course notes

No supplied course-note document was available in the repository or attachments inspected for this task. No course-note author or citation is invented. These published references support the actual content in the lecture; they are not attributions for an unavailable course-note document.

## Reproducible analysis

[munnb123/Loan_survival_seminar](https://github.com/munnb123/Loan_survival_seminar/tree/presentation/msc-survival-seminar). This presentation is developed on `presentation/msc-survival-seminar`; numerical source of truth is the existing audited `REPORT.md`, `LECTURE_EXAMPLE.md` and aggregate CSV outputs. The current polished slide sources, notes and PDFs are under `presentation/` on that branch.
