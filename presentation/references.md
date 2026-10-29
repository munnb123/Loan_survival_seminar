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
