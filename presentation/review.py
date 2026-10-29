"""Render every page; check handout equivalence and overlay text positions.

Uses only Python's standard library plus Poppler. Rendered PNGs remain in build/.
Human visual inspection of those PNGs is still necessary.
"""
import json
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
OUT = HERE/'build'/'review'
NS = {'x':'http://www.w3.org/1999/xhtml'}


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    report=json.loads((HERE/'build_report.json').read_text())
    for name in ['presentation','handout']:
        subprocess.run(['pdftoppm','-png','-scale-to','1600',str(HERE/f'{name}.pdf'),str(OUT/name)],check=True)
    subprocess.run(['pdftotext','-bbox',str(HERE/'presentation.pdf'),str(OUT/'text.xml')],check=True)
    pages=ET.parse(OUT/'text.xml').getroot().findall('.//x:page',NS)
    movement=[]; outside=[]; differences=[]
    for n,page in enumerate(pages,1):
        width=float(page.attrib['width']);height=float(page.attrib['height'])
        for word in page.findall('.//x:word',NS):
            x0,y0,x1,y1=[float(word.attrib[k]) for k in ['xMin','yMin','xMax','yMax']]
            if x0<-.2 or y0<-.2 or x1>width+.2 or y1>height+.2:
                outside.append([n,word.text])
    def positions(page):
        result={}
        for w in page.findall('.//x:word',NS):
            result.setdefault(w.text,set()).add((round(float(w.attrib['xMin']),2),round(float(w.attrib['yMin']),2)))
        return result
    for slide,(a,b) in enumerate(report['frame_page_ranges']['presentation'],1):
        if (OUT/f'presentation-{b:02d}.png').read_bytes() != (OUT/f'handout-{slide:02d}.png').read_bytes():
            differences.append(slide)
        first=positions(pages[a-1])
        for p in range(a+1,b+1):
            later=positions(pages[p-1])
            for text,coords in first.items():
                if text in later and not coords<=later[text]:movement.append([slide,p,text])
    # Ensure the displayed baseline/relative-effect labels survived TeX frame parsing.
    cox_frame=report['frame_titles'].index('The Cox model')
    a,b=report['frame_page_ranges']['presentation'][cox_frame]
    for n in range(a,b+1):
        words={w.text for w in pages[n-1].findall('.//x:word',NS)}
        assert {'baseline','multiplier'}<=words, f'Cox equation missing on PDF page {n}'
    result={'presentation_pages_rendered':len(pages),'handout_pages_rendered':report['pdf_pages']['handout'],
            'handout_final_overlay_differences':differences,'overlay_text_movement':movement,
            'text_outside_page':outside,'Cox_equation_visible_on_all_reveals':True}
    (HERE/'render_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    assert not differences and not movement and not outside,result
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
