"""모캡 프레젠테이션 영상: 큰 화면(메타휴먼 리타게팅 렌더) 위에 [촬영 원본 | 모캡 스켈레톤] 이분할 창.

사용: python Tools/sfx/make_mocapshow.py <렌더 PNG 폴더> <punch.mp4> <스켈레톤 녹화.mp4> <출력.mp4>

타이밍 (모두 AS_MHP_punch 애니메이션 0초 기준으로 맞춘다)
- 렌더: LS_MocapShow 0~152프레임(30fps) = 애니메이션 0~5.07초
- 촬영 원본: MHP_punch가 59.94fps 영상의 30~335프레임을 처리했으므로 0.5005초부터
- 스켈레톤 녹화: MHP_punch 편집기 화면 녹화. 뼈대가 녹화 0.10초부터 움직이기 시작한다
  (녹화 속 원본 화면은 에디터 재생이 끊겨서 쓰지 않고, 원본은 punch.mp4를 직접 쓴다)
"""
import glob
import os
import shutil
import subprocess
import sys

render_dir, orig, skel, out = sys.argv[1:5]
ff = shutil.which('ffmpeg') or glob.glob(os.path.expandvars(
    r'%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg*\ffmpeg-*\bin\ffmpeg.exe'))[0]

pngs = sorted(glob.glob(os.path.join(render_dir, '*.png')))
pattern = os.path.join(render_dir, pngs[0].split(os.sep)[-1].rsplit('.', 2)[0] + '.%04d.png')
DUR = len(pngs) / 30.0
TAIL = 1.0          # 끝에서 1초 정지
ORIG_START = 30 / 59.94
SKEL_START = 0.10
SKEL_CROP = 'crop=540:720:986:120'   # 녹화 1938x862 안에서 뼈대(x 1036~1476, y 260~697)를 감싸는 영역

H = 560                       # 작은 창 높이
OW = round(H * 9 / 16 / 2) * 2   # 원본(세로 9:16) 폭 = 316
SW = round(H * 3 / 4 / 2) * 2    # 스켈레톤(3:4) 폭 = 420
GAP = 12
X0 = 1920 - 40 - (OW + GAP + SW)
Y0 = 120
BOLD = "fontfile='C\\:/Windows/Fonts/malgunbd.ttf'"
REG = "fontfile='C\\:/Windows/Fonts/malgun.ttf'"


def text(t, size, x, y, font=BOLD, color='white'):
    return (f"drawtext={font}:text='{t}':fontcolor={color}:fontsize={size}:x={x}:y={y}"
            ":shadowcolor=black@0.8:shadowx=2:shadowy=2")


tp = f'tpad=stop_mode=clone:stop_duration={TAIL}'
filt = ';'.join([
    f'[0:v]fps=30,scale=1920:1080,setsar=1,{tp}[big]',
    f'[1:v]fps=30,scale={OW}:{H},setsar=1,{tp}[o]',
    f'[2:v]fps=30,{SKEL_CROP},scale={SW}:{H},setsar=1,{tp}[s]',
    # 작은 창 뒤 반투명 판
    f'[big]drawbox=x={X0 - 12}:y={Y0 - 56}:w={OW + GAP + SW + 24}:h={H + 68}:color=black@0.55:t=fill[b1]',
    f'[b1][o]overlay=x={X0}:y={Y0}[b2]',
    f'[b2][s]overlay=x={X0 + OW + GAP}:y={Y0}[b3]',
    '[b3]' + ','.join([
        f'drawbox=x={X0}:y={Y0}:w={OW}:h={H}:color=white@0.9:t=2',
        f'drawbox=x={X0 + OW + GAP}:y={Y0}:w={SW}:h={H}:color=0x00FFE6@0.9:t=2',
        text('① 직접 촬영한 영상', 26, X0, Y0 - 44),
        text('② 마커리스 모캡 스켈레톤', 26, X0 + OW + GAP, Y0 - 44, color='0x7FFFF0'),
        text('③ 메타휴먼에 리타게팅', 34, 48, 1080 - 96),
        text('MetaHuman Animator 마커리스 모캡 → Performer Skeleton → MetaHuman', 22, 48, 1080 - 50,
             font=REG, color='0xDDDDDD'),
    ]) + '[v]',
])

cmd = [ff, '-y', '-v', 'error',
       '-framerate', '30', '-i', pattern,
       '-ss', f'{ORIG_START:.4f}', '-t', f'{DUR:.3f}', '-i', orig,
       '-ss', f'{SKEL_START:.3f}', '-t', f'{DUR:.3f}', '-i', skel,
       '-filter_complex', filt, '-map', '[v]', '-an',
       '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p', '-r', '30', out]
subprocess.run(cmd, check=True)
print('done:', out, f'({DUR + TAIL:.2f}s)')
