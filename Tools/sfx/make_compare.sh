#!/usr/bin/env bash
# 촬영 원본 | 최종본 비교 영상을 만들고, 최종본 뒤에 붙여 제출용 영상을 만든다.
# 사용: bash make_compare.sh <촬영 원본.mp4> <최종본.mp4> <출력 폴더>
# 원본은 점프 꼭대기(약 2.5초)가 최종본의 공중 정지 시작(2.17초)과 맞도록 앞을 0.33초 자른다.
set -euo pipefail

orig="$1"; final="$2"; outdir="$3"
here="$(cd "$(dirname "$0")" && pwd)"
ff="$(command -v ffmpeg || ls "$LOCALAPPDATA"/Microsoft/WinGet/Packages/Gyan.FFmpeg*/ffmpeg-*/bin/ffmpeg.exe | head -1)"
ORIG_START=0.33

"$ff" -y -v error -ss "$ORIG_START" -i "$orig" -i "$final" \
  -/filter_complex "$here/compare_filter.txt" \
  -map "[v]" -map 1:a -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p -r 30 \
  -c:a aac -b:a 256k "$outdir/LS_Punch_compare.mp4"

"$ff" -y -v error -i "$final" -i "$outdir/LS_Punch_compare.mp4" \
  -filter_complex "[0:v]fps=30,format=yuv420p,setsar=1[a];[1:v]fps=30,format=yuv420p,setsar=1[b];[a][0:a][b][1:a]concat=n=2:v=1:a=1[v][au]" \
  -map "[v]" -map "[au]" -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p -c:a aac -b:a 256k \
  "$outdir/LS_Punch_submit.mp4"
echo "done: $outdir/LS_Punch_compare.mp4, $outdir/LS_Punch_submit.mp4"
