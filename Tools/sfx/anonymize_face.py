"""촬영 원본에서 머리(얼굴)를 따라가며 모자이크로 지운다. 공개 저장소용.

사용: python anonymize_face.py <원본.mp4> <출력.mp4> [--init CX,CY] [--box W,H] [--preview 미리보기.jpg]
  --init: 첫 프레임 머리 중심(원본 해상도 픽셀). 기본값은 punch.mp4 기준 (850,822).
  --box : 가릴 사각형 크기(원본 해상도). 기본 190x230 (머리보다 넉넉하게).

OpenCV 없이 numpy만으로 추적한다: 절반 해상도 회색조에서 머리 템플릿을
프레임마다 정규화 상호상관(NCC)으로 찾고, 템플릿을 조금씩 갱신한다.
오디오는 버린다(비교 영상에서는 최종본 소리를 쓴다).
"""
import argparse
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw


def probe(path):
    out = subprocess.check_output([
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=width,height,r_frame_rate", "-of", "csv=p=0", path,
    ]).decode().strip().split(",")
    return int(out[0]), int(out[1]), out[2]


def read_frames(path, w, h):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", path, "-f", "rawvideo",
                          "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    n = w * h * 3
    while True:
        buf = p.stdout.read(n)
        if len(buf) < n:
            break
        yield np.frombuffer(buf, np.uint8).reshape(h, w, 3)
    p.wait()


def gray_half(rgb):
    g = rgb[::2, ::2].astype(np.float32) @ np.array([0.299, 0.587, 0.114], np.float32)
    return g


def ncc_search(img, tpl, cx, cy, radius):
    th, tw = tpl.shape
    t = tpl - tpl.mean()
    tn = np.sqrt((t * t).sum()) + 1e-6
    best, bx, by = -2.0, cx, cy
    H, W = img.shape
    for dy in range(-radius, radius + 1, 1):
        y0 = cy + dy - th // 2
        if y0 < 0 or y0 + th > H:
            continue
        # 한 행의 모든 dx를 한 번에 계산
        xs0 = cx - radius - tw // 2
        xs1 = cx + radius - tw // 2
        xs0c, xs1c = max(xs0, 0), min(xs1, W - tw)
        if xs0c > xs1c:
            continue
        strip = img[y0:y0 + th, xs0c:xs1c + tw]
        win = np.lib.stride_tricks.sliding_window_view(strip, (th, tw))[0]
        wm = win - win.mean(axis=(1, 2), keepdims=True)
        num = (wm * t).sum(axis=(1, 2))
        den = np.sqrt((wm * wm).sum(axis=(1, 2))) * tn + 1e-6
        score = num / den
        i = int(score.argmax())
        if score[i] > best:
            best, bx, by = float(score[i]), xs0c + i + tw // 2, cy + dy
    return bx, by, best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--init", default="850,822")
    ap.add_argument("--box", default="190,230")
    ap.add_argument("--block", type=int, default=48, help="모자이크 블록 크기(px)")
    ap.add_argument("--preview")
    a = ap.parse_args()

    w, h, rate = probe(a.src)
    cx, cy = (int(v) // 2 for v in a.init.split(","))
    bw, bh = (int(v) for v in a.box.split(","))
    tw, th = 44, 60  # 절반 해상도 템플릿 크기
    radius = 22

    # 1단계: 추적
    centers, scores = [], []
    tpl0 = tpl = None
    for i, rgb in enumerate(read_frames(a.src, w, h)):
        g = gray_half(rgb)
        if tpl is None:
            tpl0 = tpl = g[cy - th // 2:cy + th // 2, cx - tw // 2:cx + tw // 2].copy()
        else:
            cx, cy, s = ncc_search(g, tpl, cx, cy, radius)
            scores.append(s)
            cur = g[cy - th // 2:cy + th // 2, cx - tw // 2:cx + tw // 2]
            if cur.shape == tpl.shape:
                tpl = 0.75 * tpl + 0.20 * cur + 0.05 * tpl0
        centers.append((cx * 2, cy * 2))
    c = np.array(centers, np.float32)
    # 살짝 평활화(3프레임 이동 평균)
    k = np.ones(3) / 3
    cs = np.stack([np.convolve(np.pad(c[:, j], 1, mode="edge"), k, "valid") for j in range(2)], 1)
    print(f"frames={len(c)}  min NCC={min(scores):.2f}  mean NCC={np.mean(scores):.2f}", file=sys.stderr)

    # 2단계: 모자이크 적용해 인코딩
    enc = subprocess.Popen([
        "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{w}x{h}", "-r", rate, "-i", "-", "-an",
        "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", a.dst,
    ], stdin=subprocess.PIPE)
    previews = []
    for i, rgb in enumerate(read_frames(a.src, w, h)):
        x, y = cs[i]
        x0, y0 = int(max(x - bw / 2, 0)), int(max(y - bh / 2, 0))
        x1, y1 = int(min(x + bw / 2, w)), int(min(y + bh / 2, h))
        im = Image.fromarray(rgb)
        reg = im.crop((x0, y0, x1, y1))
        sw, sh = max(1, (x1 - x0) // a.block), max(1, (y1 - y0) // a.block)
        reg = reg.resize((sw, sh), Image.BILINEAR).resize((x1 - x0, y1 - y0), Image.NEAREST)
        im.paste(reg, (x0, y0))
        enc.stdin.write(im.tobytes())
        if a.preview and i % 15 == 0:
            previews.append(im.crop((w // 2 - 360, 400, w // 2 + 360, 1300)).resize((180, 225)))
    enc.stdin.close()
    enc.wait()

    if a.preview and previews:
        cols = 10
        rows = (len(previews) + cols - 1) // cols
        sheet = Image.new("RGB", (180 * cols, 225 * rows))
        for j, p in enumerate(previews):
            sheet.paste(p, ((j % cols) * 180, (j // cols) * 225))
        sheet.save(a.preview)


if __name__ == "__main__":
    main()
