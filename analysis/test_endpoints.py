"""Small deterministic tests of scientific endpoint/selection logic, no real data."""
import tempfile
from pathlib import Path
from types import SimpleNamespace
import pandas as pd
from run import audit, cohort


def test_endpoints():
    base = dict(UserName='borrower', Country='EE', LoanDate='2014-01-01',
                DefaultDate=None, ContractEndDate=None, Status='Current', Age=40,
                IncomeTotal=1000, Amount=3000, LoanDuration=36, NewCreditCustomer=True,
                FirstPaymentDate='2014-02-01', MaturityDate_Original='2017-01-01')
    variants = [
        {},
        dict(DefaultDate='2015-12-31'),  # exactly day 729
        dict(DefaultDate='2016-01-01'),  # exactly day 730
        dict(DefaultDate='2016-01-02'),  # after horizon
        dict(Status='Repaid', ContractEndDate='2014-06-01'),
        dict(ContractEndDate='2014-06-01'),  # date alone cannot prove repayment
        dict(DefaultDate='2014-03-01', Status='Repaid', ContractEndDate='2014-06-01'),
        dict(DefaultDate='2014-06-01', Status='Repaid', ContractEndDate='2014-03-01'),
        dict(DefaultDate='2014-03-01', Status='Repaid', ContractEndDate='2014-03-01'),
        dict(Status='Repaid'),
        dict(DefaultDate='2014-01-01'),
        dict(IncomeTotal=0),
        dict(UserName=None),
        dict(LoanDuration=60),  # current duration must not overwrite original term
    ]
    raw = pd.DataFrame([{**base, **v, 'LoanId': str(i)} for i, v in enumerate(variants)])
    args = SimpleNamespace(cutoff='2016-12-31', repayment_column='ContractEndDate')
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        d = cohort(audit(raw, out), args, out).set_index('LoanId')
        assert set(d.index) == {'0', '1', '2', '3', '4', '5', '6', '13'}
        assert d.loc['13', 'term_12m'] == 3
        assert d.loc['0', 'duration'] == 730
        assert d.loc['1', 'event'] == d.loc['2', 'event'] == 1
        assert d.loc['3', 'event'] == 0
        assert d.loc['4', 'exit_reason'] == 'repayment'
        assert d.loc['5', 'exit_reason'] == 'administrative'
        assert d.loc['6', 'exit_reason'] == 'default'
        args.cutoff = '2014-03-01'
        short = cohort(audit(raw, out), args, out).set_index('LoanId')
        assert short.loc['6', 'event'] == 1  # event on cutoff
        assert short.loc['4', 'exit_reason'] == 'administrative'
        assert short.loc['4', 'duration'] == 59
    print('Endpoint boundary, competing exit, conflict and missingness checks passed.')


if __name__ == '__main__':
    test_endpoints()
