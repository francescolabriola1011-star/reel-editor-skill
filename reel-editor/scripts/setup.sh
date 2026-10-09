#!/bin/sh
# Installa dipendenze e modelli (idempotente). Uso: sh setup.sh
set -e
CACHE="${REEL_CACHE:-/home/claude/.cache/reel-editor}"
mkdir -p "$CACHE"
python3 -c "import skia" 2>/dev/null || pip install skia-python --break-system-packages -q
python3 -c "import sherpa_onnx" 2>/dev/null || pip install sherpa-onnx --break-system-packages -q
python3 -c "import scipy, cv2, numpy, PIL" 2>/dev/null || pip install scipy opencv-python-headless numpy pillow --break-system-packages -q
REL=https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models
M=sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8
if [ ! -f "$CACHE/$M/encoder.int8.onnx" ]; then
  echo "Scarico il modello di trascrizione (~490 MB)..."
  curl -sL --fail -o "$CACHE/m.tar.bz2" "$REL/$M.tar.bz2"
  tar xjf "$CACHE/m.tar.bz2" -C "$CACHE" && rm "$CACHE/m.tar.bz2"
fi
[ -f "$CACHE/silero_vad.onnx" ] || curl -sL --fail -o "$CACHE/silero_vad.onnx" "$REL/silero_vad.onnx"
echo "OK setup: $CACHE"
