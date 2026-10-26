"""Bondora date audit and explanatory cause-specific default analysis.

Audit runs without an asserted reporting date. Model fitting requires explicit
cutoff provenance and evidence for the selected repayment date definition.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import warnings

os.environ.setdefault('MPLCONFIGDIR', '/tmp/bondora-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from lifelines import CoxPHFitter
from lifelines.statistics import proportional_hazard_test
from lifelines.utils import normalize
from scipy.stats import chi2

COVS = ['age_10y', 'log_income', 'amount_1000', 'term_12m', 'new_customer']
LABELS = ['Age (10 years)', 'Income (doubling)', 'Amount (€1,000)',
          'Original term (12 months)', 'New vs existing customer']
DATES = ['ReportAsOfEOD', 'LoanDate', 'DefaultDate', 'ContractEndDate', 'FirstPaymentDate',
         'MaturityDate_Original', 'MaturityDate_Last', 'LastPaymentOn']


def save_json(path, value):
    path.write_text(json.dumps(value, indent=2, default=str) + '\n')


def read_data(path):
    # Read identifiers as strings; do not turn missing usernames into one cluster.
    return pd.read_csv(path, sep=None, engine='python', low_memory=True,
                       dtype={'LoanId': 'string', 'UserName': 'string'})


def audit(raw, out):
    d = raw.copy()
    rows = []
    for col in DATES:
        if col not in d:
            continue
        original = d[col]
        d[col] = pd.to_datetime(original, errors='coerce', format='mixed').dt.normalize()
        bad = original.notna() & d[col].isna()
        rows.append(dict(field=col, nonmissing=int(d[col].notna().sum()),
                         unparseable=int(bad.sum()), minimum=d[col].min(), maximum=d[col].max()))
    pd.DataFrame(rows).to_csv(out / 'date_audit.csv', index=False)
    for col in ['DefaultDate', 'ContractEndDate']:
        if col in d and 'Status' in d:
            pd.crosstab(d.Status.fillna('MISSING'), d[col].notna(), dropna=False).to_csv(
                out / f'{col}_by_status.csv')
    checks = {}
    for col in ['DefaultDate', 'ContractEndDate', 'LastPaymentOn']:
        if col in d and 'LoanDate' in d:
            checks[col + '_before_issue'] = int((d[col] < d.LoanDate).sum())
    if {'DefaultDate', 'ContractEndDate'} <= set(d):
        checks['default_after_contract_end'] = int((d.DefaultDate > d.ContractEndDate).sum())
        checks['default_same_day_contract_end'] = int((d.DefaultDate == d.ContractEndDate).sum())
    if {'ContractEndDate', 'MaturityDate_Original'} <= set(d):
        checks['contract_end_equals_original_maturity'] = int(
            (d.ContractEndDate == d.MaturityDate_Original).sum())
    checks['rows'] = len(d)
    if 'LoanId' in d:
        checks['duplicate_nonmissing_loan_ids'] = int(d.loc[d.LoanId.notna(), 'LoanId'].duplicated().sum())
    if {'Status', 'ReportAsOfEOD', 'PrincipalWriteOffs', 'PrincipalPaymentsMade', 'Amount', 'PrincipalBalance'} <= set(d):
        rows = []
        for status, g in d.groupby('Status'):
            rows.append(dict(status=status, loans=len(g), recorded_default=int(g.DefaultDate.notna().sum()),
                             contract_end_present=int(g.ContractEndDate.notna().sum()),
                             contract_end_after_report=int((g.ContractEndDate > g.ReportAsOfEOD).sum()),
                             contract_end_equals_original_maturity=int(g.ContractEndDate.eq(g.MaturityDate_Original).sum()),
                             contract_end_equals_last_payment=int(g.ContractEndDate.eq(g.LastPaymentOn).sum()),
                             principal_writeoff_positive=int(g.PrincipalWriteOffs.gt(.01).sum()),
                             principal_payments_short_of_amount=int((g.PrincipalPaymentsMade < g.Amount-.02).sum())))
        pd.DataFrame(rows).to_csv(out / 'endpoint_financial_audit.csv', index=False)
    if {'FirstPaymentDate','MaturityDate_Original','LoanDuration'} <= set(d):
        months = ((d.MaturityDate_Original.dt.year-d.FirstPaymentDate.dt.year)*12
                  +d.MaturityDate_Original.dt.month-d.FirstPaymentDate.dt.month+1)
        checks['original_schedule_term_disagrees_with_LoanDuration'] = int(months.ne(d.LoanDuration).sum())
        checks['first_payment_delay_days_min'] = int((d.FirstPaymentDate-d.LoanDate).dt.days.min())
        checks['first_payment_delay_days_max'] = int((d.FirstPaymentDate-d.LoanDate).dt.days.max())
    save_json(out / 'audit_counts.json', checks)
    return d


def cohort(d, args, out):
    required = ['LoanId', 'UserName', 'Country', 'LoanDate', 'DefaultDate',
                'Age', 'IncomeTotal', 'Amount', 'LoanDuration', 'FirstPaymentDate', 'MaturityDate_Original',
                'NewCreditCustomer', 'Status', args.repayment_column]
    missing = sorted(set(required) - set(d))
    if missing:
        raise ValueError(f'Missing required columns: {missing}')
    if args.repayment_column not in DATES:
        d[args.repayment_column] = pd.to_datetime(d[args.repayment_column], errors='coerce', format='mixed').dt.normalize()
    cutoff = pd.Timestamp(args.cutoff).normalize()
    if 'ReportAsOfEOD' in d and (d.ReportAsOfEOD.isna().any() or not d.ReportAsOfEOD.eq(cutoff).all()):
        raise ValueError('Supplied cutoff must agree with every ReportAsOfEOD in this single-snapshot analysis.')
    flow = [{'step': 'snapshot', 'remaining': len(d), 'excluded': 0}]

    def keep(mask, name):
        nonlocal d
        n = len(d)
        d = d.loc[mask].copy()
        flow.append(dict(step=name, remaining=len(d), excluded=n-len(d)))

    keep(d.Country.astype(str).str.upper().eq('EE') & d.LoanDate.between('2013-01-01', '2015-12-31'),
         'Estonia issued 2013–2015')
    if d.LoanId.dropna().duplicated().any():
        raise ValueError('Duplicate LoanId in cohort: resolve data provenance before fitting.')
    # A repaid status alone has no dated exit; a date alone does not establish repayment.
    repaid = d.Status.astype(str).str.casefold().eq('repaid')
    d['repayment_date'] = d[args.repayment_column].where(repaid)
    contradictions = {
        'repaid_missing_repayment_date': int((repaid & d.repayment_date.isna()).sum()),
        'default_before_issue': int((d.DefaultDate < d.LoanDate).sum()),
        'repayment_before_issue': int((d.repayment_date < d.LoanDate).sum()),
        'default_after_recorded_repayment': int((d.DefaultDate > d.repayment_date).sum()),
        'default_repayment_same_date': int((d.DefaultDate == d.repayment_date).sum()),
        'default_after_cutoff': int((d.DefaultDate > cutoff).sum()),
        'repayment_after_cutoff': int((d.repayment_date > cutoff).sum()),
    }
    save_json(out / 'cohort_date_conflicts.json', contradictions)
    # Quarantine inconsistent endpoints, including ties (ordering is unknowable).
    valid = ~(repaid & d.repayment_date.isna())
    valid &= ~(d.DefaultDate < d.LoanDate) & ~(d.repayment_date < d.LoanDate)
    valid &= ~(d.DefaultDate >= d.repayment_date)
    keep(valid, 'remove unresolved outcome/date conflicts')
    d['admin_end'] = pd.concat([d.LoanDate + pd.Timedelta(days=730),
                              pd.Series(cutoff, index=d.index)], axis=1).min(axis=1)
    d['exit'] = pd.concat([d.admin_end, d.DefaultDate, d.repayment_date], axis=1).min(axis=1)
    d['event'] = (d.DefaultDate.notna() & d.DefaultDate.eq(d.exit)).astype(int)
    d['exit_reason'] = np.select([d.event.eq(1), d.repayment_date.eq(d.exit)],
                                 ['default', 'repayment'], default='administrative')
    d['duration'] = (d.exit - d.LoanDate).dt.days
    keep(d.duration.gt(0), 'positive follow-up (exclude day-zero exits)')
    d['year'] = d.LoanDate.dt.year.astype(int)
    for col in ['Age', 'IncomeTotal', 'Amount', 'LoanDuration']:
        d[col] = pd.to_numeric(d[col], errors='coerce')
    # Monthly original schedule: inclusive scheduled payment months, not revised
    # maturity and not a current-term field. First-payment lag audited separately.
    d['original_term_months'] = ((d.MaturityDate_Original.dt.year-d.FirstPaymentDate.dt.year)*12
                                +d.MaturityDate_Original.dt.month-d.FirstPaymentDate.dt.month+1)
    new = d.NewCreditCustomer.astype(str).str.lower().map({'true': 1, 'false': 0, '1': 1, '0': 0, '1.0': 1, '0.0': 0})
    d['new_customer'] = new
    pre_cc = d.copy()
    valid = d[['Age', 'IncomeTotal', 'Amount', 'original_term_months', 'new_customer']].notna().all(axis=1)
    valid &= d.Age.between(18, 100) & d.IncomeTotal.gt(0) & d.Amount.gt(0) & d.original_term_months.gt(0)
    valid &= d.UserName.notna() & d.UserName.str.strip().ne('') & d.LoanId.notna()
    keep(valid, 'complete valid covariates and borrower/loan identifiers')
    pd.DataFrame(flow).to_csv(out / 'cohort_flow.csv', index=False)
    pd.DataFrame({'missing': pre_cc[['Age', 'IncomeTotal', 'Amount', 'LoanDuration', 'new_customer', 'UserName']].isna().sum()}).to_csv(out / 'covariate_missingness.csv')
    d['age_10y'] = d.Age / 10
    d['log_income'] = np.log(d.IncomeTotal)
    d['amount_1000'] = d.Amount / 1000
    d['term_12m'] = d.original_term_months / 12
    d = d.sort_values(['LoanDate', 'LoanId']).reset_index(drop=True)
    return d


def model_frame(d, extra=()):
    return d[['duration', 'event', 'year', 'UserName'] + COVS + list(extra)].copy()


def fit(d, extra=()):
    return CoxPHFitter().fit(model_frame(d, extra), 'duration', 'event',
                             strata=['year'], cluster_col='UserName', robust=True)


def sandwich(model, frame):
    # lifelines variance_matrix_ is model-based even when robust=True.
    # Reconstruct the actual cluster sandwich and assert its diagonal matches
    # the reported robust standard errors. Version pinned in requirements.txt.
    x, t, e, w, _, _, _ = model._preprocess_dataframe(frame)
    v = model._compute_sandwich_estimator(normalize(x, model._norm_mean, model._norm_std), t, e, w)
    np.testing.assert_allclose(np.sqrt(np.diag(v)), model.standard_errors_.values, rtol=1e-8)
    return pd.DataFrame(v, index=model.params_.index, columns=model.params_.index)


def wald(model, frame, terms):
    b = model.params_.loc[terms].values
    v = sandwich(model, frame).loc[terms, terms].values
    stat = float(b @ np.linalg.solve(v, b))
    return dict(chi2=stat, df=len(terms), p=float(chi2.sf(stat, len(terms))))


def hr_table(m):
    b = m.params_.loc[COVS].to_numpy()
    se = m.standard_errors_.loc[COVS].to_numpy()
    scale = np.array([1, np.log(2), 1, 1, 1])
    return pd.DataFrame(dict(term=COVS, contrast=LABELS, HR=np.exp(b*scale),
                             lower95=np.exp((b-1.96*se)*scale), upper95=np.exp((b+1.96*se)*scale),
                             p=m.summary.loc[COVS, 'p'].values))


def summary(d):
    rows = []
    for year, sub in [('All', d)] + [(str(y), g) for y, g in d.groupby('year')]:
        row = dict(year=year, loans=len(sub), borrowers=sub.UserName.nunique(),
                   defaults=int(sub.event.sum()), closure_censored=int(sub.exit_reason.eq('repayment').sum()),
                   administrative=int(sub.exit_reason.eq('administrative').sum()),
                   person_years=sub.duration.sum()/365.25,
                   new_customer_pct=100*sub.new_customer.mean(),
                   borrowers_with_multiple_loans=int(sub.groupby('UserName').size().gt(1).sum()))
        for col in ['Age', 'IncomeTotal', 'Amount', 'original_term_months', 'duration']:
            q = sub[col].quantile([.25, .5, .75])
            row[col+'_median_IQR'] = f'{q.loc[.5]:.2f} [{q.loc[.25]:.2f}, {q.loc[.75]:.2f}]'
        rows.append(row)
    return pd.DataFrame(rows)


def diagnostics(d, m, out):
    # Standard Schoenfeld tests are approximate and assume independent loans.
    # Use an independence fit for diagnostics, never pass clustered SEs to
    # lifelines' independence-based PH statistic. Repeat on one-loan cohort.
    f = model_frame(d).drop(columns='UserName')
    independent = CoxPHFitter().fit(f, 'duration', 'event', strata=['year'])
    # lifelines' built-in rank uses cumsum(event), but fit order is year/time.
    # Ranking in that order spuriously treats later vintages as later durations.
    # Rank tied event times globally on the elapsed-time axis instead.
    def pooled_event_rank(durations, events, weights):
        return pd.Series(np.searchsorted(np.sort(durations[events]), durations, side='right'), index=durations.index)
    rank = proportional_hazard_test(independent, f, time_transform=pooled_event_rank).summary
    rank['transform'] = 'pooled_event_rank'
    log = proportional_hazard_test(independent, f, time_transform='log').summary
    log['transform'] = 'log'
    ph = pd.concat([rank, log]).set_index('transform', append=True)
    ph.to_csv(out / 'ph_schoenfeld_independence.csv')
    residuals = independent.compute_residuals(f, 'scaled_schoenfeld')
    fig, axes = plt.subplots(2, 3, figsize=(12, 7))
    for ax, col, label in zip(axes.flat, COVS, LABELS):
        values = pd.DataFrame({'day': d.loc[residuals.index, 'duration'],
                               'r': residuals[col] * (np.log(2) if col == 'log_income' else 1)})
        ax.scatter(values.day, values.r, s=3, alpha=.12)
        # Binned means describe residual trends; no independence CI implied.
        values['bin'] = pd.cut(values.day, bins=np.linspace(0, 730, 13), include_lowest=True)
        means = values.groupby('bin', observed=True)[['day', 'r']].mean()
        ax.plot(means.day, means.r, 'r.-')
        ax.axhline(0, color='gray', linewidth=.7)
        ax.set(title=label, xlabel='Days since issue', ylabel='Scaled Schoenfeld residual')
    axes.flat[-1].axis('off')
    fig.tight_layout(); fig.savefig(out / 'ph_residuals.png', dpi=180); plt.close(fig)
    # Restricted cubic spline departures, one continuous variable at a time.
    # Four knots (5%,35%,65%,95%) give two nonlinear terms alongside linear.
    checks = []
    for col in COVS[:-1]:
        z = d[col]
        knots = np.quantile(z, [.05, .35, .65, .95])
        if len(np.unique(knots)) != 4 and z.nunique() >= 4:
            # Discrete original terms commonly have coincident quantiles.
            support = np.sort(z.unique())
            knots = support[np.round(np.linspace(0, len(support)-1, 4)).astype(int)]
        if len(np.unique(knots)) != 4:
            checks.append(dict(term=col, status='not estimable: coincident knots', knots=knots.tolist()))
            continue
        dd = d.copy(); terms = []
        for j, k in enumerate(knots[:-2]):
            name = f'{col}_nonlinear_{j}'
            dd[name] = (np.maximum(z-k, 0)**3
                        - np.maximum(z-knots[-2], 0)**3*(knots[-1]-k)/(knots[-1]-knots[-2])
                        + np.maximum(z-knots[-1], 0)**3*(knots[-2]-k)/(knots[-1]-knots[-2])) / (knots[-1]-knots[0])**2
            terms.append(name)
        sm = fit(dd, terms)
        checks.append(dict(term=col, status='fitted', knots=knots.tolist(),
                           **wald(sm, model_frame(dd, terms), terms)))
    pd.DataFrame(checks).to_csv(out / 'functional_form_cluster_wald.csv', index=False)


def run(args):
    out = Path(args.output); out.mkdir(parents=True, exist_ok=True)
    path = Path(args.csv)
    provenance = dict(source_url=args.source_url, sha256=hashlib.file_digest(path.open('rb'), 'sha256').hexdigest(),
                      reporting_cutoff=args.cutoff, cutoff_evidence=args.cutoff_evidence,
                      repayment_column=args.repayment_column, repayment_evidence=args.repayment_evidence,
                      default_evidence=args.default_evidence)
    save_json(out / 'provenance.json', provenance)
    d = audit(read_data(path), out)
    if args.audit_only:
        print('Audit completed; no cohort or model claims made.'); return
    if not all([args.cutoff, args.cutoff_evidence, args.repayment_evidence, args.default_evidence]):
        raise ValueError('Fitting requires --cutoff, --cutoff-evidence, --repayment-evidence and --default-evidence. Audit available with --audit-only.')
    d = cohort(d, args, out)
    if not len(d) or not d.event.any():
        raise ValueError('No analyzable loans/defaults.')
    summary(d).to_csv(out / 'sample_summary.csv', index=False)
    m = fit(d); table = hr_table(m); table.to_csv(out / 'hazard_ratios.csv', index=False)
    # Prespecified sensitivity: earliest analyzable loan per borrower, ties broken
    # by LoanId. This targets a different sample; it is not an independent study.
    one = d.drop_duplicates('UserName', keep='first').reset_index(drop=True)
    om = fit(one)
    hr_table(om).to_csv(out / 'one_loan_per_borrower_hr.csv', index=False)
    summary(one).to_csv(out / 'one_loan_per_borrower_summary.csv', index=False)
    one_dir = out / 'one_loan_diagnostics'; one_dir.mkdir(exist_ok=True)
    concordant = d.loc[d.original_term_months.eq(d.LoanDuration)].copy()
    hr_table(fit(concordant)).to_csv(out / 'original_term_agreement_sensitivity_hr.csv', index=False)
    summary(concordant).to_csv(out / 'original_term_agreement_sensitivity_summary.csv', index=False)
    if {'PrincipalWriteOffs', 'PrincipalPaymentsMade', 'PrincipalBalance', 'LastPaymentOn'} <= set(d):
        corroborated = (d.PrincipalWriteOffs.le(.01) & (d.PrincipalPaymentsMade >= d.Amount-.02)
                        & d.PrincipalBalance.abs().le(.02) & d.ContractEndDate.eq(d.LastPaymentOn))
        # Keep all observed defaults. Exclude only ambiguous nondefault exits
        # inside follow-up, not later closures irrelevant to the risk window.
        strict = d.loc[~d.exit_reason.eq('repayment') | corroborated].copy()
        hr_table(fit(strict)).to_csv(out / 'closure_sensitivity_hr.csv', index=False)
        summary(strict).to_csv(out / 'closure_sensitivity_summary.csv', index=False)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        diagnostics(d, m, out)
        diagnostics(one, om, one_dir)
    (out / 'diagnostic_warnings.txt').write_text('\n'.join(str(w.message) for w in caught))
    fig, ax = plt.subplots(figsize=(7, 3.8))
    y = np.arange(len(table))
    ax.errorbar(table.HR, y, xerr=[table.HR-table.lower95, table.upper95-table.HR], fmt='o', capsize=3)
    ax.axvline(1, color='gray', linestyle='--'); ax.set_xscale('log')
    ax.set_xticks([.75, 1, 1.25, 1.5], ['0.75', '1.00', '1.25', '1.50'])
    ax.minorticks_off()
    ax.set_yticks(y, LABELS); ax.invert_yaxis()
    ax.set_xlabel('Cause-specific hazard ratio (borrower-clustered 95% CI)')
    ax.set_title('Recorded default within 730 days\nBaseline stratified by origination year', fontsize=12)
    fig.tight_layout(); fig.savefig(out / 'hazard_ratios.png', dpi=220)
    fig.savefig(out / 'hazard_ratios.svg'); plt.close(fig)
    save_json(out / 'run_counts.json', {'loans': len(d), 'borrowers': d.UserName.nunique(),
                                       'defaults': int(d.event.sum()), 'one_loan_n': len(one),
                                       'one_loan_defaults': int(one.event.sum())})
    print(table.to_string(index=False))
    print('Completed. Review audit, attrition, warnings and diagnostics before interpreting estimates.')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('csv'); p.add_argument('--output', default='results')
    p.add_argument('--audit-only', action='store_true')
    p.add_argument('--cutoff'); p.add_argument('--cutoff-evidence')
    p.add_argument('--repayment-column', default='ContractEndDate')
    p.add_argument('--repayment-evidence'); p.add_argument('--default-evidence')
    p.add_argument('--source-url', default='https://www.kaggle.com/datasets/sid321axn/bondora-peer-to-peer-lending-loan-data')
    run(p.parse_args())
