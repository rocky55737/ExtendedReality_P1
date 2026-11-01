#!/usr/bin/env bash
# MRQ PNG 시퀀스 + 효과음 → 제출용 MP4
# 사용: bash mux.sh <PNG 폴더> [출력.mp4]
# PNG 이름은 MRQ 기본값({sequence_name}.{frame_number}.png)을 가정한다.
set -euo pipefail

src="$1"
out="${2:-LS_Punch_final.mp4}"
here="$(cd "$(dirname "$0")" && pwd)"

ffmpeg_exe="$(command -v ffmpeg || true)"
if [ -z "$ffmpeg_exe" ]; then
  ffmpeg_exe="$(ls "$LOCALAPPDATA"/Microsoft/WinGet/Packages/Gyan.FFmpeg*/ffmpeg-*/bin/ffmpeg.exe | head -1)"
fi

first="$(ls "$src"/*.png | head -1)"
prefix="$(basename "$first" | sed -E 's/[0-9]+\.png$//')"
digits="$(basename "$first" | sed -E 's/.*[^0-9]([0-9]+)\.png$/\1/' | tr -d '\n' | wc -c)"
start="$(basename "$first" | sed -E 's/.*[^0-9]([0-9]+)\.png$/\1/' | sed 's/^0*//')"
count="$(ls "$src"/*.png | wc -l)"
echo "frames: $count (start ${start:-0}), prefix '$prefix'"

"$ffmpeg_exe" -y -framerate 30 -start_number "${start:-0}" -i "$src/${prefix}%0${digits}d.png" \
  -i "$here/LS_Punch_sfx.wav" \
  -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p \
  -c:a aac -b:a 256k -shortest "$out"
echo "done: $out"
