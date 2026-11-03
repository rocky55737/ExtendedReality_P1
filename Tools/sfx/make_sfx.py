"""LS_Punch 효과음 합성 (원곡·외부 음원 없이 numpy로 직접 만든다).

시퀀스 프레임(30fps)을 Slomo 트랙을 반영한 영상 시간으로 바꿔서 이벤트를 배치한다.
사용: python make_sfx.py <출력.wav>
"""
import sys
import wave

import numpy as np

SR = 48000
FPS = 30
SEQ_END = 430
# LS_Punch Slomo 트랙 키 (프레임, 배속)
SLOMO_KEYS = [(0, 1.0), (180, 1.0), (184, 0.35), (205, 0.35), (215, 1.0), (300, 1.0), (430, 1.0)]

rng = np.random.default_rng(7)


def rate_at(f):
    for (f0, r0), (f1, r1) in zip(SLOMO_KEYS, SLOMO_KEYS[1:]):
        if f0 <= f <= f1:
            return r0 + (r1 - r0) * (f - f0) / (f1 - f0)
    return 1.0


def seq_to_sec(frame):
    """시퀀스 프레임 → 렌더된 영상 시간(초)."""
    t, f, step = 0.0, 0.0, 0.05
    while f < frame:
        d = min(step, frame - f)
        t += d / (FPS * rate_at(f + d / 2))
        f += d
    return t


TOTAL = seq_to_sec(SEQ_END)
N = int(TOTAL * SR) + SR  # 끝에 1초 여유
out = np.zeros((N, 2))


def spectral(x, gain_fn):
    """FFT 영역에서 주파수별 이득을 곱하는 필터."""
    X = np.fft.rfft(x)
    fr = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X * gain_fn(fr), len(x))


def lowpass(x, fc):
    return spectral(x, lambda f: 1 / np.sqrt(1 + (f / fc) ** 4))


def bandpass(x, fc, q=1.0):
    return spectral(x, lambda f: 1 / np.sqrt(1 + (q * (f / fc - fc / np.maximum(f, 1))) ** 2))


def env(n, attack, release, curve=4.0):
    t = np.arange(n) / SR
    a = np.clip(t / max(attack, 1e-4), 0, 1)
    r = np.exp(-curve * np.maximum(t - attack, 0) / max(release, 1e-4))
    return a * r


def place(sig, sec, gain=1.0, pan=0.0):
    i = int(sec * SR)
    if sig.ndim == 1:
        l, r = np.sqrt((1 - pan) / 2), np.sqrt((1 + pan) / 2)
        sig = np.stack([sig * l * 1.414, sig * r * 1.414], 1)
    j = min(N, i + len(sig))
    out[i:j] += sig[: j - i] * gain


def noise(sec):
    return rng.standard_normal(int(sec * SR))


def sweep(f0, f1, sec, shape=1.0):
    n = int(sec * SR)
    k = np.linspace(0, 1, n) ** shape
    freq = f0 + (f1 - f0) * k
    return np.sin(2 * np.pi * np.cumsum(freq) / SR)


# 1) 바람 앰비언스 (전체)
wind = lowpass(noise(TOTAL + 1), 400)
wind *= 0.6 + 0.4 * np.sin(2 * np.pi * 0.13 * np.arange(len(wind)) / SR)
wind = np.stack([wind, np.roll(wind, 900)], 1)
place(wind / np.abs(wind).max(), 0, 0.05)

# 2) 도약: 발 디딤 + 위로 휙
t_jump = seq_to_sec(58)
place(lowpass(noise(0.12), 900) * env(int(0.12 * SR), 0.003, 0.08), t_jump - 0.02, 0.35)
w = bandpass(noise(0.45), 700, 1.5) * env(int(0.45 * SR), 0.15, 0.3)
place(w / np.abs(w).max(), t_jump, 0.25)

# 3) 기 모으기 (65~125): 점점 올라가는 드론 + 지직거림, 떨림이 커짐
t0, t1 = seq_to_sec(65), seq_to_sec(125)
dur = t1 - t0
n = int(dur * SR)
k = np.linspace(0, 1, n)
drone = sum(sweep(55 * h, 110 * h, dur, 1.6) / h for h in (1, 2, 3, 5))
trem = 1 - (0.15 + 0.5 * k) * (0.5 + 0.5 * np.sin(2 * np.pi * (6 + 14 * k ** 2) * np.arange(n) / SR))
crackle = bandpass(noise(dur), 3000, 0.7) * (rng.random(n) < 0.0015 + 0.02 * k ** 2)
crackle = lowpass(crackle, 6000) * 6
hum = bandpass(noise(dur), 220, 2.0)
charge = (drone * 0.5 + hum * 0.3) * trem + crackle * k
charge *= np.clip(k * 3, 0, 1) * (0.25 + 0.75 * k ** 1.5)
charge[-int(0.03 * SR):] *= np.linspace(1, 0, int(0.03 * SR))  # 컷과 함께 뚝 끊김
place(charge / np.abs(charge).max(), t0, 0.55)
# 떨림 시작 무렵 낮은 쿵 울림
place(sweep(60, 40, 1.2) * env(int(1.2 * SR), 0.01, 1.0), seq_to_sec(72), 0.25)

# 4) 착지
t_land = seq_to_sec(131)
thud = sweep(90, 40, 0.5) * env(int(0.5 * SR), 0.002, 0.35) + lowpass(noise(0.5), 600) * env(int(0.5 * SR), 0.001, 0.12)
place(thud / np.abs(thud).max(), t_land, 0.6)

# 5) 스트레이트 휘두름 + 공기포 발사
t_fire = seq_to_sec(177)
swoosh_n = int(0.35 * SR)
sw = bandpass(noise(0.35), 900, 1.2) * env(swoosh_n, 0.25, 0.08, 6)
place(sw / np.abs(sw).max(), t_fire - 0.3, 0.35, pan=-0.2)
fire = sweep(140, 45, 0.9, 0.5) * env(int(0.9 * SR), 0.004, 0.6) + bandpass(noise(0.9), 400, 0.8) * env(int(0.9 * SR), 0.002, 0.3) * 0.8
place(fire / np.abs(fire).max(), t_fire, 0.6)

# 6) 벽 충돌 (184): 슬로모션이라 길고 낮게 울리는 폭발 + 파편
t_hit = seq_to_sec(184)
bd = 3.5
nb = int(bd * SR)
boom = sweep(70, 28, bd, 0.4) * env(nb, 0.005, 2.6, 3) * 1.2
crack = lowpass(noise(bd), 5000) * env(nb, 0.001, 0.25, 5)
body = lowpass(noise(bd), 250) * env(nb, 0.01, 2.0, 3) * 2.5
impact = boom + crack * 0.7 + body
impact = np.tanh(impact / np.abs(impact).max() * 2.0)
place(np.stack([impact, np.roll(impact, 240)], 1), t_hit, 0.9)

# 파편: 짧은 돌 부딪힘 소리 여러 개, 슬로모션 구간과 그 뒤로 흩어짐
t_end_slow = seq_to_sec(215)
for _ in range(70):
    ts = t_hit + 0.15 + rng.gamma(1.6, 0.9)
    if ts > TOTAL - 0.5:
        continue
    ln = rng.uniform(0.04, 0.18)
    s = bandpass(noise(ln), rng.uniform(600, 3500), rng.uniform(1.5, 4)) * env(int(ln * SR), 0.001, ln * 0.6, 6)
    g = rng.uniform(0.04, 0.16) * (0.6 if ts < t_end_slow else 1.0)
    place(s / np.abs(s).max(), ts, g, pan=rng.uniform(-0.8, 0.8))
# 무너지는 낮은 우르르
rd = 4.0
rumble = lowpass(noise(rd), 160) * env(int(rd * SR), 0.4, 3.0, 2.5)
place(rumble / np.abs(rumble).max(), t_hit + 0.2, 0.35)

# 6.5) 탈출 (300~430, 2026-11-04): 웅크림 → 도약 → 닭 날갯짓(8프레임 주기) + 꼬꼬 → 구멍 밖으로 휙
t_take = seq_to_sec(318)
place(lowpass(noise(0.15), 800) * env(int(0.15 * SR), 0.003, 0.1), t_take - 0.05, 0.4)
w = bandpass(noise(0.6), 600, 1.3) * env(int(0.6 * SR), 0.2, 0.35)
place(w / np.abs(w).max(), t_take, 0.3)
for f in range(322, 418, 8):
    ln = 0.14
    fl = lowpass(noise(ln), 700) * env(int(ln * SR), 0.01, 0.08, 5)
    place(fl / np.abs(fl).max(), seq_to_sec(f) - 0.03, 0.32, pan=rng.uniform(-0.2, 0.2))
def cluck(ln=0.16, f0=520):
    n = int(ln * SR)
    k = np.linspace(0, 1, n)
    freq = f0 * (1 + 0.6 * np.sin(np.pi * k) - 0.3 * k)
    ph = 2 * np.pi * np.cumsum(freq) / SR
    tone = sum(np.sin(h * ph) / h for h in (1, 2, 3, 4, 6))
    tone = bandpass(tone + 0.3 * noise(ln), 1200, 0.8)
    return tone * env(n, 0.008, ln * 0.5, 4)
for f, f0 in ((326, 520), (333, 600), (350, 540), (358, 640), (378, 560)):
    c = cluck(f0=f0)
    place(c / np.abs(c).max(), seq_to_sec(f), 0.35)
wd = seq_to_sec(430) - seq_to_sec(350)
ww = bandpass(noise(wd), 500, 0.9) * np.clip(np.linspace(0, 2, int(wd * SR)), 0, 1)
place(ww / np.abs(ww).max(), seq_to_sec(350), 0.18)

# 7) 마무리 페이드
fade = int(1.2 * SR)
end_i = int(TOTAL * SR)
out[end_i - fade:end_i] *= np.linspace(1, 0, fade)[:, None]
out[end_i:] = 0

out = out[: end_i]
out /= np.abs(out).max() / 0.9
pcm = (out * 32767).astype(np.int16)
with wave.open(sys.argv[1] if len(sys.argv) > 1 else "sfx.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())

print(f"total {TOTAL:.3f}s ({TOTAL * FPS:.1f} output frames)")
for f in (58, 65, 125, 131, 177, 184, 215, 300, 318, 430):
    print(f"seq {f:3d} -> {seq_to_sec(f):6.3f}s")
