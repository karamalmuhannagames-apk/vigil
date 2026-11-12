# Prepares the loading-screen photos from the full-resolution originals in art/loading/hq:
# rejects anything smaller than 3000 px wide or not sharp, crops to 16:9, grades gently, saves 3840x2160.
# usage: python3 ci/photos/prepare.py
import json, os
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

SRC, OUT = 'art/loading/hq', 'app/img/loading'
FOCUS = {'01': 50, '02': 42, '03': 38, '04': 50, '05': 58, '06': 62, '07': 55, '08': 68, '09': 64, '10': 66, '11': 50, '12': 45, '13': 55}
info = json.load(open(f'{SRC}/info.json'))
os.makedirs(OUT, exist_ok=True)
for f in os.listdir(OUT):
    if f.endswith('.jpg'): os.remove(os.path.join(OUT, f))
kept, report = {}, []
n = 0
for name in sorted(info):
    im = Image.open(f'{SRC}/{name}').convert('RGB')
    w, h = im.size
    # sharpness: variance of the Laplacian on a 2000 px copy (blurry photos score low)
    g = np.asarray(im.convert('L').resize((2000, round(2000 * h / w))), dtype=np.float32)
    lap = g[1:-1, 1:-1] * 4 - g[:-2, 1:-1] - g[2:, 1:-1] - g[1:-1, :-2] - g[1:-1, 2:]
    sharp = float(lap.var())
    if w < 3000 or sharp < 60:
        report.append(f'{name} rejected: {w}x{h} sharpness {sharp:.0f}'); continue
    W, H = 3840, 2160
    r = max(W / w, H / h); im = im.resize((round(w * r), round(h * r)), Image.LANCZOS)
    l, t = (im.width - W) // 2, (im.height - H) // 2; im = im.crop((l, t, l + W, t + H))
    im = ImageEnhance.Color(im).enhance(0.85); im = ImageEnhance.Contrast(im).enhance(1.06)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=40, threshold=3))
    n += 1; out = f'{n:02d}.jpg'
    im.save(f'{OUT}/{out}', quality=84, optimize=True, progressive=True)
    kept[out] = {**info[name], 'focus': FOCUS.get(name, 50)}
    report.append(f'{name} -> {out}: {w}x{h} sharpness {sharp:.0f}, {os.path.getsize(f"{OUT}/{out}") // 1024} KB')
json.dump(kept, open(f'{OUT}/credits.json', 'w'), indent=1, ensure_ascii=False)
print('\n'.join(report))
