"""Independent endpoint reconstruction, coefficient check and PH rank-order check."""
import argparse
import json
from pathlib import Path
from types import SimpleNamespace
import numpy as np
import pandas as pd
from lifelines import CoxPHFitter
from lifelines.statistics import proportional_hazard_test
from statsmodels.duration.hazard_regression import PHReg
from run import COVS, audit, cohort, model_frame


def verify(csv, output):
    out = Path(output)
    raw = pd.read_csv(csv, low_memory=False)
    d = cohort(audit(raw, out), SimpleNamespace(cutoff='2021-07-20', repayment_column='ContractEndDate'), out)
    # Reconstruct endpoints independently from raw columns without run.cohort.
    r = raw.copy()
    for c in ['LoanDate', 'DefaultDate', 'ContractEndDate', 'FirstPaymentDate','MaturityDate_Original']:
        r[c] = pd.to_datetime(r[c], errors='coerce').dt.normalize()
    repaid = r.Status.eq('Repaid')
    closure = r.ContractEndDate.where(repaid)
    valid = r.Country.eq('EE') & r.LoanDate.dt.year.between(2013, 2015)
    valid &= ~(repaid & closure.isna())
    valid &= ~(r.DefaultDate < r.LoanDate) & ~(closure < r.LoanDate)
    valid &= ~(r.DefaultDate >= closure)
    valid &= r[['Age', 'IncomeTotal', 'Amount', 'LoanDuration', 'NewCreditCustomer', 'UserName', 'LoanId']].notna().all(axis=1)
    valid &= r.Age.between(18, 100) & r.IncomeTotal.gt(0) & r.Amount.gt(0) & r.LoanDuration.gt(0)
    end = pd.concat([r.LoanDate+pd.Timedelta(days=730), r.DefaultDate, closure,
                     pd.Series(pd.Timestamp('2021-07-20'),index=r.index)],axis=1).min(axis=1)
    days = (end-r.LoanDate).dt.days
    valid &= days.gt(0)
    independent = pd.DataFrame({'LoanId':r.loc[valid,'LoanId'], 'duration':days[valid],
                                'event':r.DefaultDate[valid].eq(end[valid]).astype(int)}).set_index('LoanId').sort_index()
    pd.testing.assert_frame_equal(d.set_index('LoanId')[['duration','event']].sort_index(), independent)
    original = ((r.MaturityDate_Original.dt.year-r.FirstPaymentDate.dt.year)*12
                +r.MaturityDate_Original.dt.month-r.FirstPaymentDate.dt.month+1)/12
    expected_term = pd.Series(original[valid].to_numpy(),index=r.loc[valid,'LoanId']).sort_index()
    np.testing.assert_array_equal(d.set_index('LoanId').term_12m.sort_index(),expected_term)
    aux = PHReg(d.duration,d[COVS],status=d.event,strata=d.year,ties='efron').fit()
    f = model_frame(d).drop(columns='UserName')
    lm = CoxPHFitter().fit(f,'duration','event',strata=['year'])
    delta = float(np.max(np.abs(aux.params-lm.params_.values)))
    assert delta < 1e-5
    pd.DataFrame({'term':COVS, 'lifelines_beta':lm.params_.values,
                  'statsmodels_beta':aux.params}).to_csv(out/'independent_implementation_check.csv',index=False)
    naive = proportional_hazard_test(lm,f,time_transform='rank').summary
    naive.to_csv(out/'ph_builtin_rank_NOT_FOR_INFERENCE.csv')
    def time_rank(t,e,w):
        return pd.Series(np.searchsorted(np.sort(t[e]),t,side='right'),index=t.index)
    corrected = proportional_hazard_test(lm,f,time_transform=time_rank).summary
    # Reverse labels: exactly the same strata, but a different internal fit order.
    swapped = f.copy(); swapped['year'] = 4028-swapped.year
    other = CoxPHFitter().fit(swapped,'duration','event',strata=['year'])
    permuted = proportional_hazard_test(other,swapped,time_transform=time_rank).summary
    np.testing.assert_allclose(corrected.p,permuted.p,rtol=1e-6,atol=1e-8)
    save = {'endpoint_reconstruction':'passed', 'loans':len(d), 'defaults':int(d.event.sum()),
            'coefficient_max_absolute_difference':delta, 'coefficient_tolerance':1e-5,
            'corrected_PH_invariant_to_vintage_label_order':'passed',
            'SE_crosscheck':'not claimed: coefficient-only independent implementation check'}
    (out/'verification.json').write_text(json.dumps(save,indent=2)+'\n')
    print(json.dumps(save,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('csv');p.add_argument('--output',default='results')
    a=p.parse_args();verify(a.csv,a.output)
