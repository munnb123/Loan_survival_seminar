# When Will a Borrower Default?

**Survival Analysis in Credit Risk — Luke Munnelly**

A standalone 25-minute MSc seminar. No thesis reference is included. The existing audited analysis, numerical results, report and vector figures are unchanged.

## Deliverables and counts

- `presentation.pdf`: **39 PDF pages**, including progressive reveals and the two backup slides.
- `handout.pdf`: **22 PDF pages**, one per logical slide with all content visible.
- **20 main logical slides** (including title and conclusion) plus **2 optional backup slides**. The 20 main slides occupy 37 presentation pages; backup occupies two more.
- `seminar.tex`: editable main source, including Beamer speaker notes and reserved-space overlays.
- `handout.tex`: handout-mode wrapper around exactly the same source.
- `speaker_notes.md`: natural speaking prompts and a slide-by-slide schedule totalling **25:00**; backups are outside this timing.
- `audited_values.tex`: displayed cohort counts and new-customer estimate generated directly from audited CSVs.
- `build.py`: reproducible build and validation; no models, tests or statistical analyses are added or run.
- `build_report.json`: page counts, frame-to-page ranges, checked log conditions and hashes of the unchanged numerical/figure sources.
- `review.py` and `render_checks.json`: reproducible checks of all rendered pages, overlay text positions, handout equivalence and page boundaries.

Figures use reliable paths to `../results/lecture_figures/*.pdf`. Keep this directory inside the repository; copying only `presentation/` is insufficient.

## Build exactly

Requirements: Python 3 (standard library only), a LaTeX installation with Beamer, Latin Modern, AMS math and TikZ, `latexmk`, `pdflatex`, and Poppler's `pdfinfo`. The delivered PDFs were built with TeX Live 2025. On macOS these are available through a TeX distribution such as MacTeX, with `pdfinfo` supplied by `brew install poppler`.

From the repository root:

```sh
python3 presentation/build.py
```

To render every page and repeat the layout/handout checks:

```sh
python3 presentation/review.py
```

This additional check requires Poppler's `pdftoppm` and `pdftotext` and leaves review images in `presentation/build/review/`.

This refreshes the audited display macros, runs both versions through `latexmk`, copies the finished PDFs into this directory, checks both LaTeX logs, verifies the logical/page counts, and regenerates the Markdown speaker notes from `\talknote` entries in `seminar.tex`. Compilation logs and auxiliaries are retained in the ignored `presentation/build/` directory. No statistical calculation is rerun.

The equivalent underlying LaTeX commands, using the committed audited macros, are:

```sh
cd presentation
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build seminar.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build handout.tex
cp build/seminar.pdf presentation.pdf
cp build/handout.pdf handout.pdf
```

Edit slide content and its `\talknote{duration}{explanation}` in `seminar.tex`. Edit this source rather than the generated notes or number macros. The build validates the present 20+2 structure and 25-minute schedule; update those validation expectations if intentionally restructuring the talk.

## Reveals and pacing

Each click adds a point or interpretation using `\uncover` or item overlays, preserving layout space. There are no per-symbol animation sequences. The complete existing figures are static full-page frames without a second title layered over them. The risk-set example uses consecutive logical slides: setup on slide 12, then the existing worked-answer PDF on slide 13. In handout mode both are retained as distinct teaching steps, while repeated overlay pages disappear. Notes are embedded in the Beamer source but hidden in the audience PDFs; `speaker_notes.md` is the separate readable version.

## Scientific sources and qualifications

Numerical source of truth: [`REPORT.md`](../REPORT.md), [`LECTURE_EXAMPLE.md`](../LECTURE_EXAMPLE.md), and the existing `results/` CSVs. All five existing vector PDF figures are used without modification. The survival and PH curves and the coefficient log(2) in the risk-set example are hypothetical. The empirical result is the existing origination-year-stratified cause-specific default-hazard model among exposed loans, with borrower-clustered approximate intervals.

Visible qualifications distinguish rates from probabilities and associations from causal effects. The relation S=exp(−H) is explicitly restricted to a default-only setting, with a competing-closure warning. Nondefault endings are the audited closure proxy conditional on Repaid status, not universal actual repayment dates. Corrected PH concerns refer to age and new-customer status, not the earlier original-term PH claim. Original term is reconstructed from the original monthly schedule. Monetary values are used as recorded; exact source currency/income-period definitions and the default arrears threshold remain unverified. More detailed qualifications and diagnostics are in the notes and two backups.

## Quality checks

Both versions compile. The checked final logs contain no overflow/underflow boxes, undefined references or missing glyphs. Every presentation page, including intermediate reveals, and every handout logical slide is visually reviewed for clipping, equations, overlap and readable labels. Final-overlay/handout rendering comparisons and repeated-text positions check stable layouts. No model, statistical test, predictive metric or additional empirical analysis is introduced.

The 25-minute pacing is a rehearsal target, not a measured delivery time. Source-definition limitations from the audit remain; slides do not resolve them.
