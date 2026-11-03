"""확장판(올드보이 오마주) 최종 편집.

MRQ PNG(LS_Room, LS_Punch) + 합성 효과음 + 자막 → 제출용 MP4. (원본 비교 영상은 넣지 않는다 — 2026-11-04 사용자 결정)
사용: python make_story.py <MovieRenders 폴더> <출력 폴더>
"""
import os
import subprocess
import sys
import wave
import glob

import numpy as np

REN, OUT = sys.argv[1:3]
HERE = os.path.dirname(os.path.abspath(__file__))
SFX = os.path.join(HERE, '..', 'sfx')
TMP = os.path.join(OUT, 'story_tmp')
os.makedirs(TMP, exist_ok=True)

FF = 'ffmpeg'
for c in glob.glob(os.path.expandvars(r'$LOCALAPPDATA/Microsoft/WinGet/Packages/Gyan.FFmpeg*/ffmpeg-*/bin/ffmpeg.exe')):
    FF = c
FONT = "C\\:/Windows/Fonts/malgun.ttf"
FONTB = "C\\:/Windows/Fonts/malgunbd.ttf"
SR = 48000
ROOM_FPS = 30
ROOM_SEC = 5127 / ROOM_FPS
ENC = ['-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', '-r', '30',
       '-c:a', 'aac', '-b:a', '256k', '-ar', str(SR), '-ac', '2']


def ff(args, script=None):
    cmd = [FF, '-y', '-v', 'error'] + args
    if script is not None:
        p = os.path.join(TMP, 'filter.txt')
        open(p, 'w', encoding='utf-8').write(script)
        i = cmd.index('@FILTER@')
        cmd[i:i + 1] = ['-/filter_complex', p]
    print('>', ' '.join(a if len(a) < 80 else a[:77] + '...' for a in cmd[3:]))
    subprocess.run(cmd, check=True)


def text(t, size, y, start=None, end=None, font=FONTB, color='white', box=True):
    """drawtext 한 줄. 페이드 인/아웃 0.4초."""
    s = f"drawtext=fontfile='{font}':text='{t}':fontcolor={color}:fontsize={size}:x=(w-text_w)/2:y={y}"
    if box:
        s += ':box=1:boxcolor=black@0.45:boxborderw=18'
    if start is not None:
        s += (f":enable='between(t,{start},{end})'"
              f":alpha='if(lt(t,{start}+0.4),(t-{start})/0.4,if(gt(t,{end}-0.4),({end}-t)/0.4,1))'")
    return s


# ---------- 1) 방 장면 효과음 (방 울림 + TV 웅웅 + 쟁반 밀림 + 날이 바뀌는 쉭) ----------
rng = np.random.default_rng(11)


def lowpass(x, fc):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X / np.sqrt(1 + (f / fc) ** 4), len(x))


def bandpass(x, fc, q=1.0):
    X = np.fft.rfft(x)
    f = np.maximum(np.fft.rfftfreq(len(x), 1 / SR), 1)
    return np.fft.irfft(X / np.sqrt(1 + (q * (f / fc - fc / f)) ** 2), len(x))


def norm(x):
    return x / (np.abs(x).max() + 1e-9)


N = int(ROOM_SEC * SR)
room = np.zeros(N)
room += norm(lowpass(rng.standard_normal(N), 180)) * 0.06          # 방 울림
t = np.arange(N) / SR
hum = (np.sin(2 * np.pi * 60 * t) + 0.5 * np.sin(2 * np.pi * 120 * t) + 0.2 * np.sin(2 * np.pi * 180 * t))
tv = np.where((t < 4.0) | ((t > 85.4) & (t < 93.5)) | ((t > 102.1) & (t < 110.1)) | ((t > 120.1) & (t < 128.2)) | ((t > 136.8) & (t < 144.8)) | ((t > 154.8) & (t < 162.9)), 1.0, 0.35)  # TV 클로즈업·섀도복싱(TV 앞)에서 크게
room += norm(hum) * 0.025 * tv + norm(bandpass(rng.standard_normal(N), 6000, 0.5)) * 0.012 * tv


def put(sig, sec, g):
    i = int(sec * SR)
    j = min(N, i + len(sig))
    room[i:j] += sig[:j - i] * g


for s0, ln in ((1100 / 30, 38 / 30), (1800 / 30, 30 / 30), (2575 / 30, 40 / 30), (4115 / 30, 40 / 30)):           # 쟁반이 배식구로 밀려 들어옴
    n = int(ln * SR)
    sc = bandpass(rng.standard_normal(n), 2500, 2.0) * (0.6 + 0.4 * np.sin(np.linspace(0, 40, n)) ** 2)
    sc *= np.minimum(1, np.linspace(0, 6, n)) * np.minimum(1, np.linspace(6, 0, n))
    put(norm(sc), s0, 0.18)
    clank = np.sin(2 * np.pi * 1800 * np.arange(int(0.25 * SR)) / SR) * np.exp(-np.arange(int(0.25 * SR)) / SR * 25)
    put(clank, s0 + ln, 0.15)
for s0 in (38.2, 61.0, 71.0, 85.4, 110.1, 120.1, 144.8, 162.9):                                   # 자막(날짜) 바뀔 때 쉭
    n = int(0.8 * SR)
    w = bandpass(rng.standard_normal(n), 900, 1.2) * np.sin(np.linspace(0, np.pi, n)) ** 2
    put(norm(w), s0 - 0.3, 0.12)
room[:int(1.5 * SR)] *= np.linspace(0, 1, int(1.5 * SR))
pcm = (np.stack([room, np.roll(room, 600)], 1) / np.abs(room).max() * 0.7 * 32767).astype(np.int16)
room_wav = os.path.join(TMP, 'room.wav')
with wave.open(room_wav, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())

# ---------- 2) 방 장면 영상 + 자막 ----------
SUBS = [  # (시작, 끝, 문구) — 쉼표·콜론은 drawtext에서 따로 이스케이프해야 해서 쓰지 않는다. LS_Room 프레임/30 기준
    (4.5, 9.5, '어느 날 눈을 떠 보니 갇혀 있었다'),
    (26.5, 31.0, '문은 열리지 않았다'),
    (38.2, 43.0, '1일째 — 배식구로 들어온 건 군만두뿐'),
    (52.8, 57.5, '날짜를 세기 시작했다'),
    (61.0, 66.0, '100일째 — 오늘도 군만두'),
    (71.0, 76.0, '1년째 — 벽을 쳐 봤지만…'),
    (85.4, 90.0, '3년째 — 몸을 만들기 시작했다'),
    (93.6, 98.0, '벽의 X가 늘어 간다'),
    (110.1, 115.0, '5년째 — 또 군만두'),
    (120.1, 125.0, '10년째 — 아직 멀었다'),
    (144.8, 150.0, '13년째 — 군만두 맛도 잊었다'),
    (162.9, 169.5, '15년째 — 오늘 이 벽을 부순다'),
]
room_mp4 = os.path.join(TMP, 'room.mp4')
vf = '[0:v]' + ','.join(text(s, 44, 'h-150', a, b) for a, b, s in SUBS) + '[v]'
ff(['-framerate', '30', '-i', os.path.join(REN, 'LS_Room.%04d.png'), '-i', room_wav,
    '@FILTER@', '-map', '[v]', '-map', '1:a', '-shortest'] + ENC + [room_mp4], vf)
room_raw = os.path.join(TMP, 'room_raw.mp4')   # 비교 몽타주용(자막 없음)
ff(['-framerate', '30', '-i', os.path.join(REN, 'LS_Room.%04d.png'),
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', room_raw])

# ---------- 3) 클라이맥스 + 탈출 ----------
climax_raw = os.path.join(TMP, 'climax_raw.mp4')
ff(['-framerate', '30', '-i', os.path.join(REN, 'LS_Punch.%04d.png'), '-i', os.path.join(SFX, 'LS_Punch_sfx.wav'),
    '-shortest'] + ENC + [climax_raw])
climax = os.path.join(TMP, 'climax.mp4')
ff(['-i', climax_raw, '@FILTER@', '-map', '[v]', '-map', '0:a'] + ENC + [climax],
   '[0:v]' + text('자유다!', 48, 'h-150', 13.0, 15.6) + '[v]')


# ---------- 4) 카드 ----------
def card(path, dur, lines):
    vf = 'color=c=black:s=1920x1080:r=30:d=%s,' % dur + ','.join(
        text(t_, sz, y, 0.0, dur, font=f_, color=c_, box=False) for t_, sz, y, f_, c_ in lines) + '[v]'
    ff(['-f', 'lavfi', '-i', f'anullsrc=r={SR}:cl=stereo', '-t', str(dur), '@FILTER@',
        '-map', '[v]', '-map', '0:a'] + ENC + [path], vf)


title = os.path.join(TMP, 'title.mp4')
card(title, 7, [('갇힌 남자', 96, 380, FONTB, 'white'),
                ('— 「올드보이」 오마주 —', 40, 520, FONT, '0xBBBBBB'),
                ('마커리스 모션캡처 · 메타휴먼 · 컨트롤 리그 · Chaos 파괴', 32, 640, FONT, '0x888888')])
ending = os.path.join(TMP, 'ending.mp4')
card(ending, 8, [('THE END', 90, 400, FONTB, 'white'),
                 ('모캡 영상 7개 직접 촬영 → MetaHuman Animator 마커리스 솔브 → Puncher로 리타깃', 30, 560, FONT, '0xAAAAAA'),
                 ('Unreal Engine 5.8 · Claude Code + Unreal MCP로 시퀀스·리깅 키 자동화', 30, 610, FONT, '0xAAAAAA')])
# ---------- 6) 전체 이어 붙이기 ----------
parts = [title, room_mp4, climax, ending]
args = []
for p in parts:
    args += ['-i', p]
fc = ''.join(f'[{i}:v]fps=30,scale=1920:1080,setsar=1,format=yuv420p[v{i}];[{i}:a]aresample={SR},'
             f'aformat=channel_layouts=stereo[a{i}];' for i in range(len(parts)))
fc += ''.join(f'[v{i}][a{i}]' for i in range(len(parts))) + f'concat=n={len(parts)}:v=1:a=1[v][a]'
final = os.path.join(OUT, 'Oldboy_submit.mp4')
ff(args + ['@FILTER@', '-map', '[v]', '-map', '[a]'] + ENC + [final], fc)
print('done:', final)
