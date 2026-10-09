"""Normalizza il video (1080x1920, 30 fps costanti, SDR), estrae l'audio, trova il volto.
Uso: python3 prep.py <video_in> <workdir>
Produce: norm.mp4, a16k.wav, layout.json, overview.jpg"""
import sys, os, subprocess, numpy as np
from common import *

src, wd = sys.argv[1], sys.argv[2]
os.makedirs(wd, exist_ok=True)
info = probe(src)
v = next(s for s in info['streams'] if s['codec_type'] == 'video')
has_audio = any(s['codec_type'] == 'audio' for s in info['streams'])
if not has_audio: raise SystemExit('ERRORE: il video non ha traccia audio.')
hdr = v.get('color_transfer') in ('smpte2084', 'arib-std-b67')
vf = []
if hdr: vf.append('zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv')
vf += [f'scale={W}:{H}:force_original_aspect_ratio=increase', f'crop={W}:{H}', f'fps={FPS}', 'format=yuv420p']
norm = os.path.join(wd, 'norm.mp4')
run(['ffmpeg', '-y', '-v', 'error', '-i', src, '-vf', ','.join(vf), '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '14',
     '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-ac', '1', norm])
run(['ffmpeg', '-y', '-v', 'error', '-i', norm, '-ac', '1', '-ar', '16000', os.path.join(wd, 'a16k.wav')])
dur = duration(norm)

# volto: mediana su un fotogramma ogni ~1.5 s
import cv2
p = subprocess.run(['ffmpeg', '-v', 'error', '-i', norm, '-vf', 'fps=2/3,scale=540:960,format=gray', '-f', 'rawvideo', '-'], capture_output=True)
fr = np.frombuffer(p.stdout, np.uint8).reshape(-1, 960, 540)
cas = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
boxes = []
for f in fr:
    d = cas.detectMultiScale(f, 1.1, 5, minSize=(70, 70))
    if len(d):
        x, y, w, h = max(d, key=lambda b: b[2] * b[3]); boxes.append((x * 2 + w, y * 2 + h, h * 2))
if boxes:
    cx, cy, fh = [float(np.median([b[i] for b in boxes])) for i in range(3)]
    found = True
else:
    cx, cy, fh, found = 540.0, 850.0, 300.0, False
head_top = cy - fh * .5 - fh * .25
lay = dict(duration=round(dur, 3), face_found=found, face_cx=round(cx), face_cy=round(cy), face_h=round(fh),
           chin_y=round(cy + fh * .5), head_top=round(head_top),
           panel_ok=bool(head_top >= 600), panel_y=120, panel_h=490)
jsave(os.path.join(wd, 'layout.json'), lay)
n = min(24, max(6, int(dur / 3)))
run(['ffmpeg', '-y', '-v', 'error', '-i', norm, '-vf', f'fps={n}/{dur:.2f},scale=180:-1,tile=12x{(n + 11) // 12}', '-frames:v', '1', os.path.join(wd, 'overview.jpg')])
src_ar = v['width'] / v['height']
print(f"OK prep: durata {dur:.1f}s | HDR->SDR: {hdr} | volto trovato: {found} (centro {cx:.0f},{cy:.0f}, altezza {fh:.0f})")
print(f"   pannelli sopra la testa: {'SI' if lay['panel_ok'] else 'NO (testa troppo in alto: non usare panel=)'}")
if src_ar > 0.7: print("   ATTENZIONE: il sorgente non è verticale, è stato ritagliato al centro in 9:16. Controlla overview.jpg.")
if not found: print("   ATTENZIONE: nessun volto rilevato, uso valori standard. Controlla overview.jpg e correggi layout.json a mano.")
