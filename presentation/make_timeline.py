"""Presentation-only hypothetical diagram matching the revised opening loans."""
import os
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR','/tmp/bondora-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT=Path(__file__).resolve().parent/'assets'


def main():
    OUT.mkdir(exist_ok=True)
    navy,teal,orange='#142D4E','#087F8C','#D66B21'
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':20,'text.color':navy,
                         'axes.labelcolor':navy,'xtick.color':navy,'ytick.color':navy,
                         'pdf.fonttype':42,'svg.fonttype':'none'})
    fig=plt.figure(figsize=(14.4,8.1),facecolor='white')
    fig.text(.07,.93,'Follow-up can end in different ways',fontsize=30,weight='bold')
    fig.text(.07,.87,'ILLUSTRATIVE · Hypothetical loans; months since origination',fontsize=18,color='#596878')
    ax=fig.add_axes([.11,.28,.82,.49])
    for y,end,color,marker,label in [(4,3,navy,'X','Default at month 3'),
                                     (3,24,navy,'X','Default at month 24'),
                                     (2,6,teal,'|','Observation ends at month 6'),
                                     (1,12,orange,'D','Closure at month 12')]:
        ax.plot([0,end],[y,y],color=color,lw=5)
        ax.plot(0,y,'o',color=color,ms=6)
        ax.plot(end,y,marker=marker,color=color,ms=17,mew=3,linestyle='none')
        ax.text(end if end<24 else end-.2,y+.24,label,ha='center' if end<24 else 'right',color=color,fontsize=20)
    ax.set(xlim=(-.5,26),ylim=(.5,4.7),xlabel='Months since origination')
    ax.set_xticks([0,3,6,12,18,24]);ax.set_yticks([4,3,2,1],['Loan A','Loan B','Loan C','Loan D'])
    for edge in ['top','right','left']:ax.spines[edge].set_visible(False)
    ax.spines['bottom'].set_color('#718096');ax.tick_params(axis='y',length=0,pad=15)
    fig.text(.11,.13,'C: right censoring — active when observation ends.',fontsize=20,color=teal)
    fig.text(.11,.065,'D: closure — a competing event ending default exposure.',fontsize=20,color=orange)
    for ext in ['pdf','svg','png']:fig.savefig(OUT/f'loan_timelines.{ext}',dpi=240,facecolor='white')
    plt.close(fig)


if __name__=='__main__':main()
