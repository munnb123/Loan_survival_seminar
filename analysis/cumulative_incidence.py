"""Descriptive, tie-compatible Aalen–Johansen CIFs on the unchanged audited cohort.

No regression fitting, date jitter, independence CIs or 1-minus-KM calculations.
Run: python analysis/cumulative_incidence.py
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile
from types import SimpleNamespace

os.environ.setdefault('MPLCONFIGDIR','/tmp/bondora-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from run import audit, cohort, read_data, summary

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results/timing'
MONTH_DAYS=730/24
GROUPS=[('existing',0),('new',1)]


def aj(d):
    """Product-integral recursion with all tied causes at t using the same Y(t-).

    Same-day administrative censoring is removed AFTER the event increments.
    S remains the event-free probability when observation ends; it is not Y/n
    after administrative censoring.
    """
    counts=d.groupby(['duration','cause']).size().unstack(fill_value=0)
    y=len(d);s=1.;f1=f2=0.
    rows=[dict(day=0,at_risk=y,defaults=0,closures=0,censored=0,default_cif=0.,closure_cif=0.,event_free=1.)]
    for day,r in counts.iterrows():
        a,b,c=[int(r.get(k,0)) for k in [1,2,0]]
        assert y>0 and 0<=a+b+c<=y
        f1+=s*a/y;f2+=s*b/y;s*=1-(a+b)/y
        rows.append(dict(day=int(day),at_risk=y,defaults=a,closures=b,censored=c,
                         default_cif=f1,closure_cif=f2,event_free=s))
        y-=a+b+c
    return pd.DataFrame(rows)


def toy_checks():
    # Tied default/closure at day 1: both use risk set 4, then day 2 has 2.
    d=pd.DataFrame({'duration':[1,1,2,2],'cause':[1,2,1,0]})
    a=aj(d)
    np.testing.assert_allclose(a.iloc[-1][['default_cif','closure_cif','event_free']].astype(float),[.5,.25,.25])
    # Terminal ties retain default, closure and administrative censoring ordering.
    t=aj(pd.DataFrame({'duration':[730]*3,'cause':[1,2,0]}))
    np.testing.assert_allclose(t.iloc[-1][['default_cif','closure_cif','event_free']].astype(float),[1/3]*3)
    # A censored observation before events must not be treated as closure.
    c=aj(pd.DataFrame({'duration':[1,2,2],'cause':[0,1,2]}))
    np.testing.assert_allclose(c.iloc[-1][['default_cif','closure_cif','event_free']].astype(float),[.5,.5,0])
    # Row order within tied days cannot change the estimator.
    pd.testing.assert_frame_equal(a,aj(d.iloc[::-1]))


def recover(path):
    # Reuse exact audited construction; its auxiliary files go to a temp directory.
    with tempfile.TemporaryDirectory() as tmp:
        p=Path(tmp)
        d=cohort(audit(read_data(path),p),SimpleNamespace(cutoff='2021-07-20',repayment_column='ContractEndDate'),p)
        for name in ['cohort_flow.csv','cohort_date_conflicts.json']:
            if name.endswith('.csv'):
                pd.testing.assert_frame_equal(pd.read_csv(p/name),pd.read_csv(ROOT/'results'/name))
            else: assert json.loads((p/name).read_text())==json.loads((ROOT/'results'/name).read_text())
    expected=pd.read_csv(ROOT/'results/sample_summary.csv',dtype={'year':str})
    actual=summary(d)
    for col in ['year','loans','borrowers','defaults','closure_censored','administrative']:
        assert actual[col].tolist()==expected[col].tolist(),col
    d['cause']=d.exit_reason.map({'administrative':0,'default':1,'repayment':2})
    assert d.cause.notna().all() and d.cause.eq(1).equals(d.event.eq(1))
    closure=d.loc[d.cause.eq(2)]
    assert closure.Status.str.casefold().eq('repaid').all()
    assert closure.exit.eq(closure.repayment_date).all()
    assert d.loc[d.cause.eq(0),'duration'].eq(730).all()
    assert d.duration.between(1,730).all()
    return d


def plot(curves,risk):
    navy,teal,orange='#142D4E','#087F8C','#D66B21'
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':20,'text.color':navy,
                         'axes.labelcolor':navy,'xtick.color':navy,'ytick.color':navy,
                         'axes.spines.top':False,'axes.spines.right':False,
                         'pdf.fonttype':42,'svg.fonttype':'none'})
    fig=plt.figure(figsize=(14.4,8.1),facecolor='white')
    fig.text(.07,.93,'When do recorded defaults accumulate?',fontsize=30,weight='bold')
    fig.text(.07,.86,'UNADJUSTED / DESCRIPTIVE · Closure proxy treated as a competing event',fontsize=18,color='#596878')
    ax=fig.add_axes([.16,.37,.66,.41])
    for group,color,label in [('new',orange,'New customers'),('existing',teal,'Existing customers')]:
        c=curves.loc[curves.group.eq(group)]
        ax.step(c.day/MONTH_DAYS,100*c.default_cif,where='post',color=color,lw=3.5,label=label)
        ax.text(24.4,100*c.default_cif.iloc[-1],f'{100*c.default_cif.iloc[-1]:.1f}%',color=color,fontsize=20,va='center')
    ax.set(xlim=(0,24),ylim=(0,40),xlabel='Months since origination',ylabel='Default cumulative\nincidence (%)')
    ax.set_xticks([0,6,12,18,24]);ax.set_yticks([0,10,20,30,40])
    ax.legend(loc='upper left',frameon=False,fontsize=19)
    fig.text(.07,.23,'Loans at risk just before the indicated month',fontsize=17,color='#596878')
    for group,y,color,label in [('new',.16,orange,'New'),('existing',.105,teal,'Existing')]:
        fig.text(.055,y,label,color=color,fontsize=18)
        for _,r in risk.loc[risk.group.eq(group)].iterrows():
            fig.text(.16+.66*r.month/24,y,f'{int(r.at_risk):,}',ha='center',fontsize=18)
    fig.text(.07,.035,'Aalen–Johansen · No uncertainty bands · Month = 730/24 days · Not a causal comparison',fontsize=15,color='#596878')
    for ext in ['pdf','svg','png']:fig.savefig(OUT/f'default_cif.{ext}',dpi=240,facecolor='white')
    plt.close(fig)


def document(horizons):
    lines=['## Descriptive timing: recorded-default cumulative incidence','',
           'The same **9,844-loan audited cohort** is used without changing the Cox model. '
           'A deterministic Aalen–Johansen estimator treats first recorded default and the qualified closure proxy as competing events; administrative exits remain censoring. '
           'All tied daily cause counts use the same pre-event risk set, and same-day administrative censoring is removed after the event increments. **No date jitter, 1−KM substitution or new regression is used.**','',
           '| Customer status | 6 months | 12 months | 24 months |','| --- | ---: | ---: | ---: |']
    for g,label in [('new','New'),('existing','Existing'),('all','All loans')]:
        vals=horizons.loc[horizons.group.eq(g),'default_cif']
        lines.append('| '+label+' | '+' | '.join(f'{100*v:.2f}%' for v in vals)+' |')
    lines+=['','![Unadjusted recorded-default incidence with competing closure](results/timing/default_cif.png)','',
            '**Time convention:** one plotted month = 730/24 = 30.4167 days; 6, 12 and 24 months correspond exactly to 182.5, 365 and 730 days. '
            'Daily event times are not rounded or jittered. Horizon estimates include events at/before the exact grid time (thus through day 182 for 6 months). '
            'Numbers at risk are loans with exit time ≥ the indicated time, immediately before any exits exactly then; the 24-month table therefore includes loans administratively censored at day 730.','',
            '**Independent check:** this cohort has no administrative censoring before day 730. At every event time, and at each displayed horizon, '
            'the estimated default CIF agrees within numerical tolerance with the count of audited first-default exits at/before that time divided by the starting group size. '
            'This is special to complete potential follow-up with competing closure fully classified; it is not a general replacement for competing-risks estimation. '
            'Default CIF + closure CIF + remaining event-free probability equals one throughout. Counts reconcile by vintage with the existing sample summary, and boundary/conflict exclusions are inherited unchanged.','',
            '**Interpretation:** these are unadjusted, loan-level descriptive proportions experiencing recorded default before closure, under the chosen closure proxy. '
            'New and existing customers differ in other characteristics and origination years. The curves are not adjusted Cox survival predictions, not individual default-date forecasts and not causal effects. '
            'Repeated borrowers affect uncertainty; no confidence bands or independence-based inferential claims are supplied. '
            'The unchanged new-customer Cox HR remains 1.445 (borrower-clustered approximate 95% CI 1.308–1.595), an adjusted relative rate among exposed loans, not a ratio of these CIFs.','',
            'Cox can estimate survival curves after baseline-hazard estimation in a default-only setting. With competing closure, actual default probabilities require accounting for both events. '
            'No predictive accuracy is evaluated. Source endpoint/monetary definitions and the existing PH/nonlinearity caveats remain.','',
            'Reproduce this addition with `python analysis/cumulative_incidence.py`; outputs, point-estimate validation and month/risk-set conventions are saved in `results/timing/`.']
    text='\n'.join(lines)+'\n'
    (OUT/'summary.md').write_text(text.replace('(results/timing/default_cif.png)','(default_cif.png)'))
    for filename in ['REPORT.md','LECTURE_EXAMPLE.md']:
        p=ROOT/filename;s=p.read_text();start='<!-- DESCRIPTIVE_TIMING_START -->';end='<!-- DESCRIPTIVE_TIMING_END -->'
        block=start+'\n'+text+end
        if start in s:
            before,rest=s.split(start,1);_,after=rest.split(end,1)
            p.write_text(before+block+after)
        else:p.write_text(s.rstrip()+'\n\n'+block+'\n')


def main(path):
    toy_checks();OUT.mkdir(parents=True,exist_ok=True)
    protected=[ROOT/'analysis/run.py',ROOT/'results/hazard_ratios.csv',ROOT/'results/sample_summary.csv']
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
    assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==json.loads((ROOT/'results/provenance.json').read_text())['sha256']
    d=recover(path);curves=[];horizons=[];risk=[];counts=[];errors=[]
    for group,value in GROUPS+[('all',None)]:
        g=d if value is None else d.loc[d.new_customer.eq(value)]
        c=aj(g);c['group']=group
        assert c.iloc[0].default_cif==0 and c.iloc[0].closure_cif==0
        for name in ['default_cif','closure_cif']:
            assert c[name].between(-1e-12,1+1e-12).all() and (c[name].diff().dropna()>=-1e-12).all()
        np.testing.assert_allclose(c.default_cif+c.closure_cif+c.event_free,1,atol=1e-12)
        assert c.event_free.between(-1e-12,1+1e-12).all() and (c.event_free.diff().dropna()<=1e-12).all()
        direct=np.array([((g.duration<=t)&g.cause.eq(1)).sum()/len(g) for t in c.day])
        errors.append(float(np.max(np.abs(c.default_cif-direct))))
        np.testing.assert_allclose(c.default_cif,direct,atol=1e-12)
        for month in [0,6,12,18,24]:
            day=month*MONTH_DAYS;n=int((g.duration>=day).sum())
            # Independent risk count: starting loans minus strictly earlier exits.
            assert n==len(g)-int((g.duration<day).sum())
            risk.append(dict(group=group,month=month,day=day,at_risk=n))
            if month in [6,12,24]:
                r=c.loc[c.day<=day].iloc[-1]
                direct_h=int(((g.duration<=day)&g.cause.eq(1)).sum())
                assert abs(r.default_cif-direct_h/len(g))<1e-12
                horizons.append(dict(group=group,month=month,day=day,loans=len(g),defaults_by_horizon=direct_h,
                                     default_cif=r.default_cif,closure_cif=r.closure_cif,event_free=r.event_free))
        counts.append(dict(group=group,loans=len(g),borrowers=g.UserName.nunique(),defaults=int(g.cause.eq(1).sum()),
                           closures=int(g.cause.eq(2).sum()),administrative=int(g.cause.eq(0).sum())))
        curves.append(c)
    curves=pd.concat(curves,ignore_index=True);horizons=pd.DataFrame(horizons);risk=pd.DataFrame(risk)
    curves.to_csv(OUT/'curves.csv',index=False);horizons.to_csv(OUT/'horizon_estimates.csv',index=False)
    risk.to_csv(OUT/'numbers_at_risk.csv',index=False);pd.DataFrame(counts).to_csv(OUT/'cohort_counts.csv',index=False)
    plot(curves,risk);document(horizons)
    assert all(hashlib.sha256(p.read_bytes()).hexdigest()==hashes[str(p.relative_to(ROOT))] for p in protected)
    validation=dict(cohort_and_vintage_counts='exactly reconciled',boundary_conflict_rules='unchanged audited construction',
                    all_administrative_censoring_at_day_730=True,tie_method='simultaneous cause increments; censoring afterward; no jitter',
                    toy_tie_and_censor_checks='passed',simplex_and_monotonicity_checks='passed',
                    risk_set_and_horizon_cross_checks='passed',day_730_counts=curves.loc[curves.group.eq('all')&curves.day.eq(730),['at_risk','defaults','closures','censored']].iloc[0].astype(int).to_dict(),
                    max_absolute_error_vs_independent_observed_fraction=max(errors),days_per_month=MONTH_DAYS,
                    input_sha256=hashlib.sha256(Path(path).read_bytes()).hexdigest(),protected_sha256=hashes,
                    uncertainty='No bands; no independence-based or borrower-clustered inference claimed')
    (OUT/'validation.json').write_text(json.dumps(validation,indent=2)+'\n')
    print(horizons[['group','month','default_cif']].to_string(index=False))
    print(json.dumps(validation,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--csv',default=str(ROOT/'data/Bondora_Estonia_2013_2015.csv.gz'))
    main(p.parse_args().csv)
