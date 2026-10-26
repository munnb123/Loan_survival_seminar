"""Draw lecture figures only; read final HRs without fitting or changing models.

Run from any directory with the existing pinned plotting environment:
  python analysis/lecture_figures.py
"""
import csv
import hashlib
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/bondora-matplotlib")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.text import Text
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "lecture_figures"
INPUT = ROOT / "results" / "hazard_ratios.csv"
NAVY = "#142D4E"
TEAL = "#087F8C"
ORANGE = "#D66B21"
GRAY = "#718096"
PALE = "#E5EAF0"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 20,
    "text.color": NAVY, "axes.labelcolor": NAVY, "axes.edgecolor": GRAY,
    "xtick.color": NAVY, "ytick.color": NAVY,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.facecolor": "white", "figure.facecolor": "white",
    "svg.fonttype": "none", "savefig.facecolor": "white",
    "pdf.fonttype": 42, "ps.fonttype": 42,
})


def canvas(title, subtitle):
    fig = plt.figure(figsize=(14.4, 8.1))
    fig.text(.07, .93, title, fontsize=30, weight="bold")
    fig.text(.07, .87, subtitle, fontsize=18, color=GRAY)
    return fig


def save(fig, name):
    """Fixed 16:9 canvas; reject text outside it before exporting both formats."""
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    frame = fig.bbox
    for obj in fig.findobj(Text):
        if not obj.get_visible() or not obj.get_text():
            continue
        box = obj.get_window_extent(renderer)
        if not np.isfinite(box.extents).all():
            continue
        if box.x0 < frame.x0-1 or box.x1 > frame.x1+1 or box.y0 < frame.y0-1 or box.y1 > frame.y1+1:
            raise ValueError(f"Text outside {name} canvas: {obj.get_text()!r}")
    for suffix in ["svg", "png", "pdf"]:
        fig.savefig(OUT / f"{name}.{suffix}", dpi=240,
                    metadata={"Creator": "Loan_survival_seminar lecture_figures.py"}
                    if suffix in {"svg", "pdf"} else {"Software": "Loan_survival_seminar lecture_figures.py"})
    plt.close(fig)


def timelines():
    fig = canvas("Loan timelines: three different endpoints",
                 "ILLUSTRATIVE · Hypothetical loans measured from origination")
    ax = fig.add_axes([.11, .30, .82, .47])
    for y, end, color, marker, label in [
        (3, 8, NAVY, "X", "Default at month 8"),
        (2, 18, TEAL, "|", "Observation ends at month 18"),
        (1, 12, ORANGE, "D", "Closure at month 12"),
    ]:
        ax.plot([0, end], [y, y], color=color, linewidth=5, solid_capstyle="butt")
        ax.plot(0, y, "o", color=color, markersize=7)
        ax.plot(end, y, marker=marker, color=color, markersize=18,
                markeredgewidth=3, linestyle="none")
        ax.text(end, y+.23, label, color=color, fontsize=20, ha="center")
    ax.set(xlim=(-.5, 24), ylim=(.5, 3.65), xlabel="Months since origination")
    ax.set_xticks([0, 4, 8, 12, 16, 18, 24])
    ax.set_yticks([3, 2, 1], ["Loan A", "Loan B", "Loan C"])
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0, pad=15)
    fig.text(.11, .14, "B: right censoring — still active when observation ends.", fontsize=20, color=TEAL)
    fig.text(.11, .075, "C: closure — a competing event that ends default exposure.", fontsize=20, color=ORANGE)
    save(fig, "01_loan_timelines")


def survival():
    fig = canvas("Survival: the probability of remaining default-free",
                 "HYPOTHETICAL · Default-only setting; not a Bondora estimate")
    ax = fig.add_axes([.11, .22, .82, .55])
    t = np.linspace(0, 24, 481)
    s = np.exp(-.02*t)
    s12 = np.exp(-.02*12)
    ax.plot(t, s, color=TEAL, linewidth=4)
    ax.plot([0, 12, 12], [s12, s12, 0], color=ORANGE, linestyle="--", linewidth=2)
    ax.plot(12, s12, "o", color=ORANGE, markersize=11)
    ax.annotate(r"$S(12)=e^{-0.24}\approx 0.79$", xy=(12, s12), xytext=(13.6, .50),
                fontsize=23, color=NAVY, arrowprops={"arrowstyle": "->", "color": ORANGE, "lw": 2})
    ax.text(.49, .93, r"$S(t)=\exp(-0.02t)$", transform=ax.transAxes, fontsize=27)
    ax.set(xlim=(0, 24), ylim=(0, 1.06), xlabel="Time, t (months)", ylabel="Survival probability, S(t)")
    ax.set_xticks([0, 6, 12, 18, 24]); ax.set_yticks([0, .25, .5, .75, 1])
    fig.text(.11, .075, "At 12 months, about 79% remain default-free in this hypothetical setting.", fontsize=20)
    save(fig, "02_illustrative_survival")


def hazards():
    fig = canvas("Proportional hazards: changing rates, constant ratio",
                 "HYPOTHETICAL · A hazard is an instantaneous rate, not a probability")
    ax = fig.add_axes([.11, .25, .49, .51])
    ratio = fig.add_axes([.74, .25, .20, .51])
    t = np.linspace(0, 24, 481)
    a = .024+.008*np.sin(np.pi*t/18)+.0003*t
    b = 1.5*a
    assert np.all(a>0) and np.all(b>0)
    np.testing.assert_allclose(b/a, 1.5)
    ax.plot(t, a, color=TEAL, linewidth=4)
    ax.plot(t, b, color=ORANGE, linewidth=4)
    ax.text(8, .057, r"B: $h_B(t)=1.5h_A(t)$", color=ORANGE, fontsize=21)
    ax.text(10, .019, r"A: $h_A(t)$", color=TEAL, fontsize=23)
    ax.set(xlim=(0, 24), ylim=(0, .065), xlabel="Time (months)", ylabel="Hazard rate (per month)")
    ax.set_xticks([0, 6, 12, 18, 24]); ax.set_yticks([0, .02, .04, .06])
    ratio.plot(t, b/a, color=ORANGE, linewidth=4)
    ratio.text(12, 1.64, "Ratio = 1.5", ha="center", color=ORANGE, fontsize=22)
    ratio.set(xlim=(0, 24), ylim=(1, 2), xlabel="Time (months)", ylabel=r"$h_B(t)/h_A(t)$")
    ratio.set_xticks([0, 12, 24]); ratio.set_yticks([1, 1.5, 2])
    fig.text(.11, .10, "The baseline hazard can vary over time; proportionality concerns the ratio.", fontsize=20)
    save(fig, "03_proportional_hazards")


def risk_set():
    fig = canvas("Cox regression compares borrowers in the risk set",
                 "ILLUSTRATIVE · At risk immediately before a default; all other covariates equal")
    for x, who, status, relative, color in [
        (.07, "A", "Existing customer", r"Relative risk: $1$", TEAL),
        (.37, "B", "Existing customer", r"Relative risk: $1$", TEAL),
        (.67, "C", "New customer", r"Relative risk: $e^{\beta}$", ORANGE),
    ]:
        fig.add_artist(FancyBboxPatch((x, .49), .26, .29, boxstyle="round,pad=0.012",
                       transform=fig.transFigure, facecolor="white", edgecolor=color, linewidth=2))
        fig.text(x+.13, .71, who, ha="center", fontsize=29, weight="bold", color=color)
        fig.text(x+.13, .63, status, ha="center", fontsize=21)
        fig.text(x+.13, .55, relative, ha="center", fontsize=23)
    fig.text(.5, .365, r"$P(C\ \mathrm{defaults}\mid\mathrm{one\ default\ in\ risk\ set})"
             r"=\frac{e^{\beta}}{2+e^{\beta}}$", ha="center", fontsize=26)
    fig.text(.5, .22, r"If $\beta=\log(2)$:     $\frac{2}{1+1+2}=\frac{1}{2}$",
             ha="center", fontsize=29, color=ORANGE)
    fig.text(.5, .085, "Conditional on one default occurring now; not a probability over a time horizon.",
             ha="center", fontsize=19)
    save(fig, "04_cox_risk_set")


def hazard_ratios():
    with INPUT.open(newline="") as f:
        data = {r["term"]: r for r in csv.DictReader(f)}
    terms = ["age_10y", "log_income", "amount_1000", "term_12m", "new_customer"]
    assert set(data) == set(terms), "Expected final audited five-covariate model"
    values = np.array([[float(data[t][c]) for c in ["HR", "lower95", "upper95"]] for t in terms])
    hr, low, high = values.T
    assert np.isfinite(values).all() and np.all(0 < low) and np.all(low < hr) and np.all(hr < high)
    fig = canvas("Recorded default: adjusted hazard ratios",
                 "EMPIRICAL · Final audited Cox estimates; baseline stratified by origination year")
    ax = fig.add_axes([.43, .35, .32, .41])
    y = np.arange(5)
    ax.axvline(1, color=GRAY, linestyle="--", linewidth=2)
    for i in y:
        color = TEAL if hr[i] < 1 else ORANGE
        ax.errorbar(hr[i], i, xerr=[[hr[i]-low[i]], [high[i]-hr[i]]], fmt="o",
                    color=color, markersize=10, capsize=5, linewidth=3)
    ax.set_xscale("log"); ax.set_xlim(.69, 1.68); ax.set_ylim(4.6, -.6)
    ax.set_xticks([.75, 1, 1.25, 1.5], ["0.75", "1.00", "1.25", "1.50"])
    ax.minorticks_off()
    ax.set_yticks(y, ["Age: +10 years", "Income: doubling", "Loan amount: +€1,000*",
                     "Original scheduled term: +12 months", "New customer: yes vs no"])
    ax.tick_params(axis="y", length=0, pad=15, labelsize=20)
    ax.spines["left"].set_visible(False)
    ax.set_xlabel("Hazard ratio (log scale)", fontsize=20, labelpad=12)
    fig.text(.79, .79, "HR (95% CI)", fontsize=20, weight="bold")
    for i in y:
        ax.text(1.12, i, f"{hr[i]:.3f} ({low[i]:.3f}–{high[i]:.3f})",
                transform=ax.get_yaxis_transform(), fontsize=18, va="center")
    fig.text(.07, .20, "Borrower-clustered 95% CIs are approximate with tied daily event times.", fontsize=17)
    fig.text(.07, .145, "PH departures: age and new-customer status. Nonlinearity: age; borderline for term.", fontsize=17)
    fig.text(.07, .09, "*Monetary fields as recorded; source currency/period definitions remain unverified.", fontsize=16)
    fig.text(.07, .045, "Conditional associations, not causal effects or default probabilities. See REPORT.md.", fontsize=16)
    save(fig, "05_audited_hazard_ratios")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    original_hash = hashlib.sha256(INPUT.read_bytes()).hexdigest()
    for draw in [timelines, survival, hazards, risk_set, hazard_ratios]:
        draw()
    assert hashlib.sha256(INPUT.read_bytes()).hexdigest() == original_hash
    print("Exported five SVG, five vector PDF and five 3456×1944 PNG figures.")
    print(f"Audited estimates unchanged; source SHA-256: {original_hash}")


if __name__ == "__main__":
    main()
