# When Will a Borrower Default? Survival Analysis in Credit Risk

Python analysis for a 25-minute MSc seminar. Read [REPORT.md](REPORT.md) for the audit, results and limitations. The current lecture source, PDFs and speaking notes are in `presentation/`.

For the short teaching version, open [LECTURE_EXAMPLE.md](LECTURE_EXAMPLE.md). [Download the code and results ZIP](Bondora_results.zip). The GitHub repository and ZIP include aggregate results, not raw borrower-level data.

## Reproduce

Python 3.12 was used. From the repository root:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.lock
bash analysis/reproduce.sh
```

The current cloud environment can instead run:

```sh
BONDORA_PYTHON=/workspace/loan-survival-venv/bin/python bash analysis/reproduce.sh
```

The input is `data/Bondora_Estonia_2013_2015.csv.gz`, supplied by the user after filtering the Kaggle CSV to Estonia and 2013–2015 originations while retaining all columns. It has 9,863 rows and 112 columns. **To rerun from GitHub, obtain the source data, filter `Country=EE` and `2013-01-01 <= LoanDate < 2016-01-01`, retain all columns and follow-up dates, and save the gzipped CSV at this input path.** Raw borrower-level data is excluded from this repository and its downloadable ZIP. The original full-file population and filtering implementation cannot be independently audited from this subset. Source: https://www.kaggle.com/datasets/sid321axn/bondora-peer-to-peer-lending-loan-data (metadata labels it CC0). Input SHA-256 is saved in `results/provenance.json`.

`analysis/run.py` supports `--audit-only`, alternate output directories and explicit endpoint evidence. The executable reproduction script records the exact operational choices used here. Once the input data is supplied locally, the analysis requires no external service or credentials. Input data is ignored by Git; aggregate results are explicitly versioned for review. `requirements.lock` pins the complete installed Python dependency set; `requirements.txt` records direct dependencies.

## Definitions and scope

- Reporting cutoff: `ReportAsOfEOD=2021-07-20` in every row, rather than maximum observed outcome or file modification date. All origination dates have a full 730-day potential window.
- Event: first recorded `DefaultDate`. The exact arrears threshold could not be independently retrieved from Bondora's business dictionary, so no 60-day or 90-day definition is asserted.
- Nondefault exit: `ContractEndDate` only when snapshot `Status=Repaid`. This is an audited **closure proxy**, not proof of full cash repayment. Current/Late contract dates are never treated as repayment. Earlier defaults remain defaults even if current status is Repaid. A stricter closure sensitivity is included.
- Original term: inclusive monthly schedule length from `FirstPaymentDate` to `MaturityDate_Original`, not revised maturity or automatically the raw `LoanDuration`. Monthly original-schedule interpretation is an explicit assumption. The first-payment delay is 17–69 days in this subset. A sensitivity excludes all 59 disagreements with `LoanDuration`.
- Time at risk ends at the earliest default, qualified closure proxy, 730 days or reporting date. Exclude missing closure dates in Repaid loans and same-day default/closure conflicts rather than invent ordering. The three same-day conflicts include two outside 730 days; all three are conservatively quarantined. Complete-case exclusions and every outcome count are saved.
- The primary model is cause-specific Cox with origination-year baseline strata and borrower-clustered sandwich intervals. Repayment/closure removes loans from the default risk set. This does not require independent latent default/repayment times for describing the cause-specific hazard. It does not estimate a cumulative default probability or causal effect.

## Files and validation

- `analysis/run.py`: audit, primary Cox model, original-term/closure sensitivities, one-loan-per-borrower robustness, PH and functional-form diagnostics, HR plots.
- `analysis/test_endpoints.py`: deterministic tests for horizon/cutoff boundaries, conflict exclusions, missing/invalid covariates, default before later repayment, ignoring non-Repaid contract dates, and original rather than current term.
- `analysis/verify.py`: independently reconstructs endpoints and original term, checks coefficients using statsmodels PHReg with Efron ties (same model, not a competitor), and verifies that corrected rank PH results do not change when vintage labels are reversed. Independent standard-error verification is not claimed.
- `results/sample_summary.csv`, `hazard_ratios.csv`, `hazard_ratios.png`/`.svg`, `one_loan_per_borrower_hr.csv` and sensitivity CSVs are real-data outputs.
- `results/ph_schoenfeld_independence.csv`, `ph_residuals.png` and the one-loan diagnostic subdirectory contain approximate independence-based Schoenfeld tests. The rank transform is pooled elapsed event-time rank with tied times kept together. Lifelines' built-in cumulative-event rank is unsafe when fit rows are ordered by vintage/time; `ph_builtin_rank_NOT_FOR_INFERENCE.csv` is retained only to demonstrate that issue.
- `results/functional_form_cluster_wald.csv`: separate four-knot restricted cubic spline checks of continuous covariates, testing two nonlinear terms with the cluster sandwich. Knots are 5/35/65/95 percentiles, falling back to four distinct equally spaced support positions when discrete terms cause repeated quantiles. Actual knots are saved; results are exploratory and knot-sensitive.
- `results/diagnostic_warnings.txt` and `verification.json` retain warnings and checks. The recorded warnings are a lifelines UTC deprecation, not convergence failures.

Lifelines' sandwich approximation has documented limitations with many tied times; daily dates create ties here. PH test p-values on the repeated-loan sample are not cluster-adjusted; the one-loan sample offers an independent-borrower diagnostic but changes sample composition. No global cluster-adjusted PH test, predictive performance, model competition or causal interpretation is claimed. Functional-form misspecification can also affect PH checks. The source business definitions and units remain a documentation limitation; data consistency checks support operational use but do not replace original contracts or payment histories.

Direct dictionary reference (unavailable through this environment's network policy): https://api.bondora.com/doc/ResourceModel?modelName=PublicDatasetItem&v=1 . The accessible Kaggle description is saved in `sources/kaggle_description.md`.


## Descriptive answer to “when?”

The addition in [`results/timing/`](results/timing/README.md) estimates unadjusted recorded-default cumulative incidence by customer status using the exact audited cohort, with the qualified closure proxy as a competing event. It complements the unchanged Cox model: timing curves describe accumulation; hazard ratios describe adjusted relative rates among exposed loans. No predictive accuracy or causal effect is claimed.

```sh
python analysis/cumulative_incidence.py
python presentation/make_result_figure.py
python3 presentation/build.py
python3 presentation/review.py
```

The first two commands require the existing pinned Python plotting/data environment (in this cloud workspace, `/workspace/loan-survival-venv/bin/python`). The last two require LaTeX and Poppler as documented in `presentation/README.md`. Descriptive analysis requires the exact audited input CSV.gz; compiling the committed slides does not require borrower-level data. See `results/timing/validation.json` for the estimator checks and protected Cox-result hashes.
