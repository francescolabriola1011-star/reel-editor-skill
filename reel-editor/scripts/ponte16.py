"""PONTE 16:9 dal nostro taglio al motore reel-editor (8/10/2026), per i video YouTube.

  python3 ponte16.py <cut.mp4> <words_cut.json> <wd> [--fix fix.json]

Scrive in <wd>: base.mp4 (1920x1080 30 fps, chiave a ogni secondo), words.json (parole della
ri-trascrizione del TAGLIO, con le correzioni di fix.json {"indice": "parola"}),
layout.json (volto mediano trovato con Vision di macOS), overview.jpg.
"""
import sys, os, json, shutil, tempfile, argparse
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import jload, jsave, run, duration

ap = argparse.ArgumentParser(); ap.add_argument('cut'); ap.add_argument('words'); ap.add_argument('wd'); ap.add_argument('--fix')
a = ap.parse_args(); W, H = 1920, 1080
os.makedirs(a.wd, exist_ok=True); base = os.path.join(a.wd, 'base.mp4')
# qualita' (8/10/2026, correzione 428): se il taglio e' gia' 1920x1080 a 30 fps non si ricodifica
_v = json.loads(run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height,r_frame_rate', '-of', 'json', a.cut]).stdout)['streams'][0]
if (_v['width'], _v['height'], _v['r_frame_rate']) == (W, H, '30/1'):
    run(['ffmpeg', '-y', '-v', 'error', '-i', a.cut, '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', base])
else:
    run(['ffmpeg', '-y', '-v', 'error', '-i', a.cut, '-vf', f'scale={W}:{H}:flags=lanczos,fps=30', '-c:v', 'libx264', '-preset', 'medium', '-crf', '14', '-g', '30',
         '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', base])
dur = duration(base)
raw = jload(a.words); raw = raw.get('words', raw) if isinstance(raw, dict) else raw
fix = jload(a.fix) if a.fix else {}
words = []
for i, x in enumerate(raw):
    w = (x.get('w') or x.get('word') or '').strip()
    w = fix.get(str(i), w)
    if not w: continue
    words.append({'i': i, 'w': w, 's': round(float(x.get('s', x.get('start', 0))), 3), 'e': round(float(x.get('e', x.get('end', 0))), 3)})
# whisper stacca apostrofi ("All 'interno"), migliaia ("100 .000"), intervalli ("5 -10") e
# percentuali: a schermo sarebbero apostrofi staccati e numeri spezzati, che il collaudo blocca
uniti = []
for w in words:
    t = w['w']
    if uniti and (t[0] in "'’%" or (t[0] in '.-' and len(t) > 1 and t[1].isdigit() and uniti[-1]['w'][-1:].isdigit())):
        uniti[-1]['w'] += t; uniti[-1]['e'] = w['e']
    else:
        uniti.append(dict(w))
words = uniti
jsave(os.path.join(a.wd, 'words.json'), words)

import Quartz, Vision
from Foundation import NSURL
tmp = tempfile.mkdtemp(); run(['ffmpeg', '-v', 'error', '-i', base, '-vf', 'fps=1/6', os.path.join(tmp, 'f_%03d.png')]); boxes = []
for fn in sorted(os.listdir(tmp)):
    srci = Quartz.CGImageSourceCreateWithURL(NSURL.fileURLWithPath_(os.path.join(tmp, fn)), None)
    img = Quartz.CGImageSourceCreateImageAtIndex(srci, 0, None)
    req = Vision.VNDetectFaceRectanglesRequest.alloc().init()
    Vision.VNImageRequestHandler.alloc().initWithCGImage_options_(img, None).performRequests_error_([req], None)
    res = req.results() or []
    if res:
        bb = max(res, key=lambda o: o.boundingBox().size.height).boundingBox()
        w_, h_ = bb.size.width * W, bb.size.height * H; x_ = bb.origin.x * W; y_ = (1 - bb.origin.y - bb.size.height) * H
        boxes.append((x_ + w_ / 2, y_ + h_ / 2, h_))
shutil.rmtree(tmp, ignore_errors=True)
cx, cy, fh = ([float(np.median([q[i] for q in boxes])) for i in range(3)] if boxes else (960.0, 400.0, 160.0))
jsave(os.path.join(a.wd, 'layout.json'), dict(duration=round(dur, 3), face_found=bool(boxes), face_cx=round(cx), face_cy=round(cy), face_h=round(fh), chin_y=round(cy + fh * .5)))
run(['ffmpeg', '-y', '-v', 'error', '-i', base, '-vf', f'fps=12/{dur:.2f},scale=320:-1,tile=4x3', '-frames:v', '1', os.path.join(a.wd, 'overview.jpg')])
print(f"OK ponte16: {len(words)} parole, {dur:.1f}s, volto {bool(boxes)} ({cx:.0f},{cy:.0f},h{fh:.0f})")
