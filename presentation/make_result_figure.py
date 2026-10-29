"""Simplified presentation-only view of the unchanged audited HR table."""
import csv
import os
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR','/tmp/bondora-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]


def main():
    with (ROOT/'results/hazard_ratios.csv').open() as f:rows={r['term']:r for r in csv.DictReader(f)}
    terms=['age_10y','log_income','amount_1000','term_12m','new_customer']
    labels=['Age: +10 years','Income: doubling','Amount: +1,000 monetary units',
            'Original scheduled term: +12 months','New customer: yes vs no']
    navy,teal,orange='#142D4E','#087F8C','#D66B21'
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':20,'text.color':navy,
                         'axes.labelcolor':navy,'xtick.color':navy,'ytick.color':navy,
                         'pdf.fonttype':42,'svg.fonttype':'none'})
    fig=plt.figure(figsize=(14.4,8.1),facecolor='white')
    fig.text(.07,.93,'Adjusted associations with the default rate',fontsize=28,weight='bold')
    fig.text(.07,.86,'ADJUSTED · Audited cause-specific Cox model; origination-year baseline strata',fontsize=18,color='#596878')
    ax=fig.add_axes([.43,.29,.49,.48])
    ax.axvline(1,color='#718096',ls='--',lw=2)
    for y,t in enumerate(terms):
        r=rows[t];hr,lo,hi=[float(r[k]) for k in ['HR','lower95','upper95']]
        ax.errorbar(hr,y,xerr=[[hr-lo],[hi-hr]],fmt='o',ms=11,capsize=5,lw=3,color=teal if hr<1 else orange)
    ax.set_xscale('log');ax.set_xlim(.69,1.68);ax.set_ylim(4.6,-.6)
    ax.set_xticks([.75,1,1.25,1.5],['0.75','1.00','1.25','1.50']);ax.minorticks_off()
    ax.set_yticks(range(5),labels);ax.tick_params(axis='y',length=0,pad=16)
    for edge in ['top','right','left']:ax.spines[edge].set_visible(False)
    ax.spines['bottom'].set_color('#718096');ax.set_xlabel('Hazard ratio (log scale)',labelpad=14)
    fig.text(.07,.14,'Dots: hazard-ratio estimates · Bars: approximate borrower-clustered 95% confidence intervals.',fontsize=16)
    fig.text(.07,.07,'Adjusted associations. Source monetary currency/income period unverified.',fontsize=16,color='#596878')
    out=ROOT/'presentation/assets'
    for ext in ['pdf','svg','png']:fig.savefig(out/f'audited_hazard_ratios.{ext}',dpi=240,facecolor='white')
    plt.close(fig)


if __name__=='__main__':main()
