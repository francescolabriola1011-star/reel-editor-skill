import os, json, subprocess
CACHE = os.environ.get('REEL_CACHE', '/home/claude/.cache/reel-editor')
ASR = os.path.join(CACHE, 'sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8')
VAD = os.path.join(CACHE, 'silero_vad.onnx')
W, H, FPS = 1080, 1920, 30

def jload(p):
    with open(p) as f: return json.load(f)
def jsave(p, o):
    with open(p, 'w') as f: json.dump(o, f, ensure_ascii=False, indent=1)
def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0: raise SystemExit('ERRORE ffmpeg:\n' + r.stderr[-1500:])
    return r
def probe(path):
    r = run(['ffprobe', '-v', 'error', '-print_format', 'json', '-show_streams', '-show_format', path])
    return json.loads(r.stdout)
def duration(path): return float(probe(path)['format']['duration'])
