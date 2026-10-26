# Lecture figures

Five 16:9 figures for “When Will a Borrower Default? Survival Analysis in Credit Risk”. Each has an SVG, a **vector PDF with embedded TrueType fonts**, and a 3456 × 1944 PNG (240 dpi). White backgrounds, navy text and teal/orange accents are shared across the set. These are figures only; no presentation has been created.

| File stem | Type and purpose | Suggested spoken explanation |
| --- | --- | --- |
| `01_loan_timelines` | Illustrative. Show default (cross), right censoring (bar) and closure (diamond) on the origination-time axis. | “A defaults at month eight. B is still active when observation ends at month eighteen, so its outcome is right censored. C closes at month twelve: closure is a competing event that removes default exposure.” |
| `02_illustrative_survival` | Hypothetical default-only setting, **not a Bondora estimate**. Plot S(t)=exp(−0.02t), with t in months, and mark S(12)=0.7866≈0.79. | “Survival is the probability of remaining default-free beyond time t. Here about 79% remain default-free at twelve months. This simple example has no competing closure event; it is not an empirical curve.” |
| `03_proportional_hazards` | Hypothetical. Show positive, time-varying hazards and their constant ratio. | “Both rates change over time. Proportional hazards means their ratio stays constant—here 1.5—not that either hazard is constant. A hazard is a rate per month, not a default probability.” |
| `04_cox_risk_set` | Illustrative partial-likelihood contribution for one default among three otherwise identical borrowers at risk. β=log(2) is chosen for teaching, **not estimated from Bondora**. | “Condition on one default occurring now. The two existing customers have relative risk one each, and the new customer has exp(β). Its share is exp(β)/(2+exp(β)). With β=log(2), that is one half. This is the conditional identity of the defaulting borrower, not a forecast over a horizon.” |
| `05_audited_hazard_ratios` | Empirical presentation of the **final audited** five-covariate Cox HRs and borrower-clustered 95% CIs, read directly from `../hazard_ratios.csv`. Log horizontal axis; reference at HR=1. | “These are adjusted associations with the instantaneous recorded-default rate among exposed loans. Income is shown per doubling, age per ten years, amount per 1,000 recorded monetary units, original scheduled term per twelve months, and new versus existing customer. They are not causal effects or default probabilities.” |

## Reproduce

From the repository root, with the existing pinned environment:

```sh
python analysis/lecture_figures.py
```

In this cloud workspace:

```sh
/workspace/loan-survival-venv/bin/python analysis/lecture_figures.py
```

The script writes only these fifteen figure files, checks all text against the canvas boundary, checks the illustrative hazard ratio numerically, and verifies that the audited input CSV hash remains unchanged. It does not read borrower-level data, fit models, run statistical tests, modify the audit, or overwrite the original HR figures. The hypothetical hazards are h_A(t)=0.024+0.008 sin(πt/18)+0.0003t and h_B(t)=1.5h_A(t), in inverse months.

For Beamer, include a PDF directly, for example:

```latex
\includegraphics[width=\linewidth]{results/lecture_figures/04_cox_risk_set.pdf}
```

PDF paths and text remain vector objects; SVG text remains editable and uses DejaVu Sans. PDFs embed the font subsets, so they are preferable for consistent LaTeX inclusion. The figure canvas is 16:9; it includes its title and small explanatory notes.

## Empirical cautions retained

Read [the audited report](../../REPORT.md) for interpretation. The same year-stratified Cox model and estimates are used without changes. Age has PH and nonlinearity concerns; new-customer status has a PH departure in the main sample; original term has a borderline nonlinear departure. The corrected original-term PH check did not detect a departure. These concerns limit constant-HR interpretations. Borrower-clustered Wald intervals are approximate with tied daily dates. The euro label follows the existing results contrast, with the report's qualification that original currency/income-period definitions are unverified. Recorded closure is a proxy restricted to Repaid status, not a universal interpretation of ContractEndDate. The source's default arrears-day threshold remains unverified.

## Export review

All five PNGs and rendered SVG/PDF exports were reviewed for clipping, overlap, endpoint symbols, formulas and contrast labels. The PDFs were checked for embedded fonts and absence of raster image objects. Existing audited model files, data, numerical result tables and report were preserved.
