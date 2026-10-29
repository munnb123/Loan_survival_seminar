"""Build Beamer PDFs, derive displayed numbers from audited outputs, check logs."""
import csv
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BUILD = HERE / "build"
MAIN_SLIDES = 28
BACKUP_SLIDES = 2
OPTIONAL_SLIDES = {6, 14}


def clock(seconds):
    return f'{seconds//60:02d}:{seconds%60:02d}'


def frame_sources():
    text = (HERE/'lecture_main.tex').read_text()+'\n'+(HERE/'backup.tex').read_text()
    frames = re.findall(r'\\begin\{frame\}(?:\[[^\]]*\])?(?:\{([^}]*)\})?(.*?)\\end\{frame\}',text,re.DOTALL)
    assert len(frames)==MAIN_SLIDES+BACKUP_SLIDES
    return frames


def read_csv(name):
    with (ROOT / "results" / name).open(newline="") as f:
        return list(csv.DictReader(f))


def main():
    BUILD.mkdir(exist_ok=True)
    hr = {r['term']: r for r in read_csv('hazard_ratios.csv')}
    sample = read_csv('sample_summary.csv')[0]
    timing={(r['group'],int(r['month'])):r for r in read_csv('timing/horizon_estimates.csv')}
    macros = {"LoanCount": f"{int(sample['loans']):,}",
              "BorrowerCount": f"{int(sample['borrowers']):,}",
              "DefaultCount": f"{int(sample['defaults']):,}",
              "NewCustomerHR": f"{float(hr['new_customer']['HR']):.3f}",
              "NewCustomerLower": f"{float(hr['new_customer']['lower95']):.3f}",
              "NewCustomerUpper": f"{float(hr['new_customer']['upper95']):.3f}",
              "NewCIFTwentyFour":f"{100*float(timing['new',24]['default_cif']):.1f}",
              "ExistingCIFTwentyFour":f"{100*float(timing['existing',24]['default_cif']):.1f}"}
    (HERE/'audited_values.tex').write_text('% Generated from existing audited CSVs by build.py; no model fitting.\n'+
        ''.join('\\newcommand{\\'+k+'}{'+v+'}\n' for k,v in macros.items()))
    counts = {}
    ranges = {}
    for source, target in [('seminar', 'presentation'), ('handout', 'handout')]:
        log_capture = BUILD / f'{source}-build-output.txt'
        with log_capture.open('w') as out:
            subprocess.run(['latexmk','-pdf','-interaction=nonstopmode','-halt-on-error',
                            '-file-line-error','-outdir=build',source+'.tex'],
                           cwd=HERE,stdout=out,stderr=subprocess.STDOUT,check=True)
        log = (BUILD / f'{source}.log').read_text(errors='replace')
        problems = re.findall(r'^.*(?:Overfull|Underfull|undefined|Missing character|multiply defined).*$'
                              ,log,flags=re.MULTILINE)
        if problems:
            raise RuntimeError('\n'.join(problems))
        nav = (BUILD / f'{source}.nav').read_text()
        pages = [(int(a),int(b)) for a,b in re.findall(r'\\beamer@framepages\s*\{(\d+)\}\s*\{(\d+)\}',nav)]
        if len(pages)!=MAIN_SLIDES+BACKUP_SLIDES:
            raise RuntimeError(f'Expected {MAIN_SLIDES} main + {BACKUP_SLIDES} backup frames, got {len(pages)}')
        if source=='handout' and any(a!=b for a,b in pages):
            raise RuntimeError('Handout still contains repeated overlay pages')
        info = subprocess.run(['pdfinfo',str(BUILD/f'{source}.pdf')],capture_output=True,text=True,check=True).stdout
        count = int(re.search(r'^Pages:\s+(\d+)',info,re.MULTILINE).group(1))
        assert pages[-1][1] == count
        counts[target] = count
        ranges[target] = pages
        shutil.copyfile(BUILD/f'{source}.pdf',HERE/f'{target}.pdf')
    sources = [ROOT/'REPORT.md',ROOT/'LECTURE_EXAMPLE.md',ROOT/'results/hazard_ratios.csv']
    sources += sorted((ROOT/'results/lecture_figures').glob('*.pdf'))
    sources += [HERE/'assets/loan_timelines.pdf']
    sources += [HERE/'assets/audited_hazard_ratios.pdf',ROOT/'results/timing/default_cif.pdf',
                ROOT/'results/timing/horizon_estimates.csv',ROOT/'results/timing/numbers_at_risk.csv']
    frames=frame_sources()
    report = {'logical_slides':MAIN_SLIDES+BACKUP_SLIDES,'main_slides':MAIN_SLIDES,'backup_slides':BACKUP_SLIDES,'pdf_pages':counts,
              'frame_page_ranges':ranges,'log_checks':'No overfull/underfull boxes, undefined references or missing characters',
              'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}}
    notes = ['# Speaker notes — Luke Munnelly',
             f'\nStandalone lecture for MSc Stochastics and Financial Mathematics students. **{MAIN_SLIDES} main logical slides; 26:40 at a calm pace.** '
             'Skip optional slides 6 (55 seconds) and 14 (45 seconds) for a **25:00 speaking route**. '
             'Audience questions and the two backup slides are outside both plans. Timings include the indicated pauses and figure reading, not extra theory or audience discussion. '
             f'The presentation has {counts["presentation"]} overlay-expanded pages; the handout has {counts["handout"]} pages, one per logical slide.\n',
             '## Practical 25-minute route\n',
             f'- After slide 5, skip optional slide 6 and resume slide 7 on presentation PDF page {ranges["presentation"][6][0]}.',
             f'- After slide 13, skip optional slide 14 and resume slide 15 on presentation PDF page {ranges["presentation"][14][0]}.',
             '- These transitions are self-contained: slide 5 already explains the horizon issue, and slide 15 requires no cumulative-hazard notation.',
             '- Do not rush the opening, graph reading or conditional risk-set calculation. If nervous, take the scripted short pauses rather than filling them with extra material.',
             '- Risk-set setup is slide 19; the static worked-answer figure is slide 20. The descriptive timing curve is slide 23; the adjusted Cox HR plot is slide 25.\n',
             '## Schedule\n',
             '| Slide | Full-plan time | 25-minute route | Duration | Topic |',
             '| --- | --- | --- | --- | --- |']
    details=[]; elapsed=0; essential=0; titles=[]
    for i,(title,body) in enumerate(frames,1):
        timing, explanation = re.search(r'\\talknote\{([^}]*)\}\{(.*?)\}',body,re.DOTALL).groups()
        if not title:
            figure = re.search(r'\\fullfigure\{([^}]+)\}',body)
            title = figure.group(1)[3:].replace('_',' ').title() if figure else ('Follow-up timelines' if '\\timelinefigure' in body else ('Descriptive default timing' if '\\timingfigure' in body else ('Adjusted Cox hazard ratios' if '\\resultfigure' in body else 'When Will a Borrower Default?')))
        titles.append(title)
        seconds = sum(int(n)*m for n,m in zip(timing.split(':'),[60,1])) if i<=MAIN_SLIDES else 0
        span=f'{clock(elapsed)}–{clock(elapsed+seconds)}' if i<=MAIN_SLIDES else 'Backup'
        short='Skip' if i in OPTIONAL_SLIDES else (f'{clock(essential)}–{clock(essential+seconds)}' if i<=MAIN_SLIDES else 'Backup')
        label=str(i) if i<=MAIN_SLIDES else 'B'+str(i-MAIN_SLIDES)
        notes.append(f'| {label} | {span} | {short} | {timing if i<=MAIN_SLIDES else "—"} | {title} |')
        details.append(f'\n## {label}. {title} ({span}; short route: {short})\n\n'+explanation.strip()+'\n')
        elapsed+=seconds
        if i not in OPTIONAL_SLIDES:essential+=seconds
    assert elapsed==1600 and essential==1500, (elapsed,essential)
    report.update(frame_titles=titles,speaking_seconds=elapsed,slot_route_seconds=essential,optional_main_slides=sorted(OPTIONAL_SLIDES))
    (HERE/'build_report.json').write_text(json.dumps(report,indent=2)+'\n')
    (HERE/'speaker_notes.md').write_text('\n'.join(notes+details)+'\n'+(HERE/'questions.md').read_text())
    print(json.dumps({k:report[k] for k in ['logical_slides','main_slides','backup_slides','pdf_pages','speaking_seconds','slot_route_seconds']},indent=2))


if __name__=='__main__':
    main()
