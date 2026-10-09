"""Unisce i blocchi renderizzati, normalizza la voce e la mixa con la musica (che si abbassa quando si parla).
  python3 mix.py <workdir> <output.mp4> [--music-vol 0.21] [--no-music] [--music file_audio]
"""
import sys, os, glob, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
ap = argparse.ArgumentParser(); ap.add_argument('wd'); ap.add_argument('out'); ap.add_argument('--music-vol', type=float, default=.21)
ap.add_argument('--no-music', action='store_true'); ap.add_argument('--music', default=None)
a = ap.parse_args(); wd = a.wd
parts = sorted(glob.glob(os.path.join(wd, 'parts', 'part_*.mp4')))
parts = [p for p in parts if not p.endswith('.tmp.mp4')]
if not parts: raise SystemExit('ERRORE: nessun blocco renderizzato. Lancia prima render.py <workdir> all')
with open(os.path.join(wd, '_list.txt'), 'w') as f: f.write(''.join(f"file '{os.path.abspath(p)}'\n" for p in parts))
vid = os.path.join(wd, '_video.mp4'); run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', os.path.join(wd, '_list.txt'), '-c', 'copy', vid])
base = os.path.join(wd, 'base.mp4'); voice = "[1:a]aresample=48000,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000,pan=stereo|c0=c0|c1=c0"
os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
if a.no_music:
    run(['ffmpeg', '-y', '-v', 'error', '-i', vid, '-i', base, '-filter_complex', voice + '[a]', '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-shortest', a.out])
else:
    mus = a.music or os.path.join(wd, 'music.wav')
    fc = (voice + ",asplit=2[v1][v2];" + f"[2:a]aresample=48000,volume={a.music_vol}[m];[m][v1]sidechaincompress=threshold=0.04:ratio=2.5:attack=15:release=400[md];"
          "[v2][md]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95:level=0[a]")
    run(['ffmpeg', '-y', '-v', 'error', '-i', vid, '-i', base, '-stream_loop', '-1', '-i', mus, '-filter_complex', fc, '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-shortest', a.out])
os.remove(vid); os.remove(os.path.join(wd, '_list.txt'))
print(f"OK {a.out}: {duration(a.out):.1f}s, {os.path.getsize(a.out) / 1e6:.0f} MB")
