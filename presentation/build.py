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


def read_csv(name):
    with (ROOT / "results" / name).open(newline="") as f:
        return list(csv.DictReader(f))


def main():
    BUILD.mkdir(exist_ok=True)
    hr = {r['term']: r for r in read_csv('hazard_ratios.csv')}
    sample = read_csv('sample_summary.csv')[0]
    macros = {"LoanCount": f"{int(sample['loans']):,}",
              "BorrowerCount": f"{int(sample['borrowers']):,}",
              "DefaultCount": f"{int(sample['defaults']):,}",
              "NewCustomerHR": f"{float(hr['new_customer']['HR']):.3f}",
              "NewCustomerLower": f"{float(hr['new_customer']['lower95']):.3f}",
              "NewCustomerUpper": f"{float(hr['new_customer']['upper95']):.3f}"}
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
        if len(pages)!=22:
            raise RuntimeError(f'Expected 20 main + 2 backup frames, got {len(pages)}')
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
    report = {'logical_slides':22,'main_slides':20,'backup_slides':2,'pdf_pages':counts,
              'frame_page_ranges':ranges,'log_checks':'No overfull/underfull boxes, undefined references or missing characters',
              'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}}
    (HERE/'build_report.json').write_text(json.dumps(report,indent=2)+'\n')
    tex = (HERE/'seminar.tex').read_text()
    frames = re.findall(r'\\begin\{frame\}(?:\[[^\]]*\])?(?:\{([^}]*)\})?(.*?)\\end\{frame\}',tex,re.DOTALL)
    assert len(frames)==22
    notes = ['# Speaker notes — Luke Munnelly',
             '\nStandalone MSc seminar. **20 main slides, 25:00 total.** Two optional backup slides are outside the timing. '
             'The presentation has 39 pages because progressive reveals expand logical slides; the handout has 22 pages, one per logical slide. '
             'The static PDF figures occupy complete frames and do not animate. On slide 12, discuss the risk-set setup before advancing to the worked answer on slide 13.\n',
             '| Slide | Start–end | Duration | Topic |','| --- | --- | --- | --- |']
    details=[]; elapsed=0
    def clock(s): return f'{s//60:02d}:{s%60:02d}'
    for i,(title,body) in enumerate(frames,1):
        timing, explanation = re.search(r'\\talknote\{([^}]*)\}\{(.*?)\}',body,re.DOTALL).groups()
        if not title:
            figure = re.search(r'\\fullfigure\{([^}]+)\}',body)
            title = figure.group(1)[3:].replace('_',' ').title() if figure else 'When Will a Borrower Default?'
        seconds = sum(int(n)*m for n,m in zip(timing.split(':'),[60,1])) if i<=20 else 0
        span=f'{clock(elapsed)}–{clock(elapsed+seconds)}' if i<=20 else 'Optional'
        notes.append(f'| {i if i<=20 else "B"+str(i-20)} | {span} | {timing if i<=20 else "—"} | {title} |')
        details.append(f'\n## {i if i<=20 else "B"+str(i-20)}. {title} ({span})\n\n'+explanation.strip()+'\n')
        elapsed+=seconds
    assert elapsed==1500, f'Expected 25 minutes, got {elapsed} seconds'
    (HERE/'speaker_notes.md').write_text('\n'.join(notes+details))
    print(json.dumps({'logical_slides':22,'main_slides':20,'backup_slides':2,'pdf_pages':counts},indent=2))


if __name__=='__main__':
    main()
