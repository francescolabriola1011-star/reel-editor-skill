"""PONTE dal nostro taglio al motore reel-editor (8/10/2026).

Il motore reel-editor (skill di Michele, con cui Francesco ha rifatto il 3262) monta su
base.mp4 + words.json + layout.json. Il TAGLIO e il TESTO li facciamo noi, con le nostre
protezioni (edl_guard, apertura mai tagliata, verbatim verificato sul tratto corto):
qui si prendono gia' fatti dalla cartella di lavoro di build_reel.py.

Uso:  python3 ponte.py <work_dir_nostro> <work_dir_reel_editor>
  legge  <nostro>/base.mp4 (montato tagliato 1080x1920 con audio), words_remap.json, script.txt
  scrive <re>/base.mp4, words.json (parole dello SCRIPT coi tempi dell'audio), layout.json, overview.jpg
"""
import sys, os, re, json, shutil, subprocess, difflib, unicodedata
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

src, wd = sys.argv[1], sys.argv[2]
os.makedirs(wd, exist_ok=True)
base = os.path.join(wd, 'base.mp4')
shutil.copy(os.path.join(src, 'base.mp4'), base)
dur = duration(base)

def norm(w):
    w = unicodedata.normalize('NFD', w.lower())
    return re.sub(r'[^a-z0-9]', '', ''.join(c for c in w if unicodedata.category(c) != 'Mn'))

remap = [x for x in jload(os.path.join(src, 'words_remap.json')) if x['w'].strip()]
sp = os.path.join(src, 'script.txt')
script = open(sp).read().split() if os.path.exists(sp) else [x['w'].strip() for x in remap]
# il VERBATIM: le parole a schermo sono quelle dello script (verificato da noi), i TEMPI
# sono quelli dell'audio. Allineamento con difflib come nello STEP 4 della skill reel.
a = [norm(x['w']) for x in remap]; b = [norm(w) for w in script]
sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
tempi = [None] * len(script)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal' or (tag == 'replace' and i2 - i1 == j2 - j1):
        for k in range(j2 - j1):
            tempi[j1 + k] = (remap[i1 + k]['s'], remap[i1 + k]['e'])
    elif tag == 'replace' and i2 > i1:
        s0, e0 = remap[i1]['s'], remap[i2 - 1]['e']; n = j2 - j1
        for k in range(n):
            tempi[j1 + k] = (s0 + (e0 - s0) * k / n, s0 + (e0 - s0) * (k + 1) / n)
# parole dello script senza audio corrispondente: tempi interpolati fra le vicine
for j in range(len(script)):
    if tempi[j] is None:
        prev = next((tempi[k][1] for k in range(j - 1, -1, -1) if tempi[k]), 0.0)
        nxt = next((tempi[k][0] for k in range(j + 1, len(script)) if tempi[k]), prev + .3)
        tempi[j] = (prev, max(prev + .05, min(nxt, prev + .3)))
words = [{'i': i, 'w': w, 's': round(s, 3), 'e': round(e, 3)} for i, (w, (s, e)) in enumerate(zip(script, tempi))]
jsave(os.path.join(wd, 'words.json'), words); jsave(os.path.join(wd, 'words_raw.json'), words)
mancanti = sum(1 for t in tempi if t is None)

# volto: Vision di macOS (OpenCV 5 qui non ha CascadeClassifier). Un fotogramma ogni 1,5 s,
# volto piu' grande, mediana. Coordinate su 1080x1920.
import tempfile, Quartz, Vision
from Foundation import NSURL
tmp = tempfile.mkdtemp()
run(['ffmpeg', '-v', 'error', '-i', base, '-vf', 'fps=2/3', os.path.join(tmp, 'f_%03d.png')])
boxes = []
for fn in sorted(os.listdir(tmp)):
    srci = Quartz.CGImageSourceCreateWithURL(NSURL.fileURLWithPath_(os.path.join(tmp, fn)), None)
    img = Quartz.CGImageSourceCreateImageAtIndex(srci, 0, None)
    req = Vision.VNDetectFaceRectanglesRequest.alloc().init()
    Vision.VNImageRequestHandler.alloc().initWithCGImage_options_(img, None).performRequests_error_([req], None)
    res = req.results() or []
    if res:
        bb = max(res, key=lambda o: o.boundingBox().size.height).boundingBox()
        w_, h_ = bb.size.width * W, bb.size.height * H
        x_ = bb.origin.x * W; y_ = (1 - bb.origin.y - bb.size.height) * H
        boxes.append((x_ + w_ / 2, y_ + h_ / 2, h_))
shutil.rmtree(tmp, ignore_errors=True)
if boxes:
    cx, cy, fh = [float(np.median([q[i] for q in boxes])) for i in range(3)]; found = True
else:
    cx, cy, fh, found = 540.0, 850.0, 300.0, False
head_top = cy - fh * .5 - fh * .25
lay = dict(duration=round(dur, 3), face_found=found, face_cx=round(cx), face_cy=round(cy), face_h=round(fh),
           chin_y=round(cy + fh * .5), head_top=round(head_top), panel_ok=bool(head_top >= 600), panel_y=120, panel_h=490)
jsave(os.path.join(wd, 'layout.json'), lay)
n = min(24, max(6, int(dur / 3)))
run(['ffmpeg', '-y', '-v', 'error', '-i', base, '-vf', f'fps={n}/{dur:.2f},scale=180:-1,tile=12x{(n + 11) // 12}', '-frames:v', '1', os.path.join(wd, 'overview.jpg')])
print(f"OK ponte: {len(words)} parole dallo script, durata {dur:.1f}s, volto {found} ({cx:.0f},{cy:.0f},h{fh:.0f}), "
      f"pannelli {'SI' if lay['panel_ok'] else 'NO'}")
