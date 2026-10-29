# When Will a Borrower Default?

**Survival Analysis in Credit Risk — Luke Munnelly**

Polished standalone lecture for MSc Stochastics and Financial Mathematics students. The audited analysis and numerical results are unchanged. There are no presenter-only labels, implementation field names or backup frames in the audience PDFs.

## Slides and ending

**30 logical slides total: 28 teaching slides, Sources, then Questions.** The overlay-expanded presentation has **57 PDF pages**; the handout has **30 pages**, one per logical slide with all content visible. The final page is a minimal “Questions?” slide that stays on screen during discussion.

The flow remains lending problem → why survival analysis → censoring/survival/hazard → Cox → descriptive timing and adjusted rate comparisons → conclusion. The empirical transition explicitly distinguishes unadjusted group curves from Cox comparisons accounting for the included characteristics. The early six-month example uses ordinary observation language; risk sets are introduced in the Cox estimation example. Endpoint rules use plain language, with field names retained in notes. Proportional hazards is written out on slides.

The three-part conclusion progressively reveals **WHEN?**, **WHICH BORROWERS?**, and **INTERPRETATION**. The 27.4%/21.2% timing comparison is unadjusted/descriptive under the audited closure proxy. The approximately 44% higher default hazard comes from the separate adjusted HR 1.445. A short visible qualification keeps those meanings distinct. Sources follow; questions do not share the conclusion slide.

## Speaking plan — presenter notes only

Use the **25:00 route** in `speaker_notes.md`, covering Sources briefly in the final 20 seconds. Skip the retained explanation slides **6 (55 seconds)** and **14 (45 seconds)** if using that route. Including both gives a calm 26:40 plan. Timing and optional status are deliberately not visible on any slide. Audience discussion is outside both plans.

- After logical slide 5, resume slide 7 on presentation PDF page **15**.
- After logical slide 13, resume slide 15 on presentation PDF page **29**.
- In the short route, conclude from 23:40–24:40, acknowledge Sources from 24:40–25:00, then leave Questions visible.

These are rehearsal targets, not measured delivery times. The generated notes give per-slide times, actual reveal order and full answers to likely questions. The two former backup frames have been removed; their partial-likelihood explanation and existing diagnostic details remain only in `questions.md`/`speaker_notes.md`.

## Editable sources and deliverables

- `seminar.tex`: entry point, white/navy/teal styling and source inclusions.
- `lecture_main.tex`: all 30 logical frames, progressive reveals and `\talknote` speaking prompts.
- `handout.tex`: handout wrapper around the same source.
- `presentation.pdf`, `handout.pdf`: compiled audience deliverables.
- `speaker_notes.md`: generated timings/prompts plus reference answers and citations.
- `questions.md`: anticipated questions and retained technical detail; never displayed as slides.
- `references.md`, `reference_verification.json`: full bibliography and checked citation/data metadata. No course-note author is invented for an unavailable document.
- `audited_values.tex`: displayed values generated from the existing audited CSVs, including the conclusion percentages and rounded hazard increase.
- `make_result_figure.py`, `assets/audited_hazard_ratios.*`: presentation-only version of the unchanged audited HR estimates, with the dots/bars explanation given once on the plot. Important assumption/source qualifications remain in the limitations slide and notes.
- `make_timeline.py`, `assets/loan_timelines.*`: the existing hypothetical timeline illustration.
- `build.py`, `review.py`, `build_report.json`, `render_checks.json`: reproducible build and layout checks.
- `PR_DESCRIPTION.md`: prepared branch/PR summary.

Static figures remain static. Risk-set setup is logical slide 19 and the worked answer is slide 20. Timing curves are slide 23, the adjustment/contrast transition is slide 24, and the HR plot is slide 25. Required aggregate outputs and existing vector figures are referenced through repository-relative paths; keep `presentation/` in the full checkout.

## Exact build commands

Requirements: Python 3 standard library; TeX Live/MacTeX with Beamer, Latin Modern, AMS math and TikZ; `latexmk`, `pdflatex`; Poppler's `pdfinfo`, `pdftoppm` and `pdftotext`. The delivered PDFs use TeX Live 2025. On macOS, `brew install poppler` supplies the Poppler tools.

From the repository root:

```sh
python3 presentation/build.py
python3 presentation/review.py
```

The build refreshes display macros from existing aggregate CSVs, compiles both PDFs, checks logs/page counts, validates the timing routes and ending order, and regenerates the Markdown notes. It does **not** rerun any statistical analysis. The review renders every page, checks text bounds and stable reveals, compares each handout page with the corresponding final reveal, and checks that forbidden presenter labels/field names/PH abbreviations are absent from the audience PDF.

Equivalent underlying LaTeX commands using committed macros and assets:

```sh
cd presentation
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build seminar.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build handout.tex
cp build/seminar.pdf presentation.pdf
cp build/handout.pdf handout.pdf
```

To regenerate only the revised presentation HR asset from the unchanged audited CSV, use the existing pinned plotting environment:

```sh
/workspace/loan-survival-venv/bin/python presentation/make_result_figure.py
```

The existing descriptive timing figure remains `results/timing/default_cif.pdf`; it is not recomputed by the presentation build. The full original audit/analysis reproduction commands remain in the root README. No borrower-level data is needed to compile the committed slides. Build logs and page-review PNGs stay under the ignored `presentation/build/` directory.

## Numerical accuracy and review

Source of truth: `REPORT.md`, `LECTURE_EXAMPLE.md`, `results/hazard_ratios.csv` and `results/timing/horizon_estimates.csv`. The build checks the displayed 27.4%, 21.2%, HR 1.445 and about 44% directly against those outputs. Timing curves are descriptive, loan-level and unadjusted; hazard ratios are adjusted cause-specific associations among exposed loans. Neither establishes a certain individual date, a causal effect or predictive accuracy.

Original closure-proxy and monthly original-term definitions, source currency/income-period uncertainty, age/new-customer proportional-hazards concerns, nonlinearity and approximate tied-date intervals remain in the presentation/notes. Bibliographic details were checked against accessible maintained bibliographies and the Kaggle record; the verification scope is recorded in `references.md` rather than implying unavailable publisher pages were inspected.

Both PDFs compile without warnings, over/underfull boxes, missing characters or undefined references. Changed slides and all relevant reveals are visually inspected for readability, clipping and overlap. Existing text positions stay fixed across reveals, and every handout slide matches its final reveal. The audit, cohort, model, numerical tables and original figures are unchanged. Nothing has been merged.
