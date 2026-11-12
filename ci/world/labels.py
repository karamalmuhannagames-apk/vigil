# Recomputes the country name positions on the finished map (art/world), with the same rules as build.py.
# usage: python3 ci/world/labels.py
import json, os
import numpy as np
from PIL import Image
import scipy.ndimage as ndi
OUT = 'art/world'
world = json.load(open(os.path.join(OUT, 'world.json'), encoding='utf-8'))
im = np.asarray(Image.open(os.path.join(OUT, 'nations.png')).convert('RGB')).astype(np.int64)
nation = im[..., 0] + im[..., 1] * 256 - 1
H, W = nation.shape
countries = {c['iso']: c for c in world['countries']}
ids = [c['iso'] for c in sorted(world['countries'], key=lambda c: c['index'])]
from PIL import ImageFont as _IF
try:
    _font = _IF.truetype('app/fonts/IBMPlexSansArabic-Bold.ttf', 100, layout_engine=_IF.Layout.RAQM)
except Exception:
    _font = None
def _textw(t):                                   # width of the text at height 100
    if _font is None: return 55 * len(t)
    bb = _font.getbbox(t, direction='rtl'); return bb[2] - bb[0]
_lab = nation + 1
_objs = ndi.find_objects(_lab)
for i, a in enumerate(ids):
    c = countries[a]; sl = _objs[i] if i < len(_objs) else None
    if sl is None: continue
    pad_ = 40
    sl = (slice(max(0, sl[0].start - pad_), min(H, sl[0].stop + pad_)), slice(max(0, sl[1].start - pad_), min(W, sl[1].stop + pad_)))
    y0s, x0s = sl[0].start, sl[1].start
    m = (_lab[sl] == i + 1)
    ok_ = m | (_lab[sl] == 0)                      # a name may spill over its own sea, never far over a neighbour
    io = np.pad(ok_.astype(np.int32), ((1, 0), (1, 0))).cumsum(0).cumsum(1)
    cl, ncl = ndi.label(m)
    if ncl > 1:                                   # main landmass for the centre; islands may still hold part of a name
        main = cl == (np.argmax(np.bincount(cl.ravel())[1:]) + 1)
    else: main = m
    ii = np.pad(m.astype(np.int32), ((1, 0), (1, 0))).cumsum(0).cumsum(1)
    hh_, ww_ = m.shape
    yy, xx = np.nonzero(main)
    cy, cx = yy.mean(), xx.mean(); span = np.sqrt(len(yy)) + 1
    step = max(1, int(span / 28))
    cyx = np.stack(np.nonzero(main[::step, ::step]), 1) * step
    if len(cyx) > 1500: cyx = cyx[np.random.default_rng(i).choice(len(cyx), 1500, replace=False)]
    name = c.get('name_ar') or c.get('name_en') or ''
    words = name.split(' ')
    layouts = [(_textw(name) / 100.0, 1.0, [name])]
    if len(words) > 1:
        mid = len(name) / 2; k = min(range(1, len(words)), key=lambda j: abs(len(' '.join(words[:j])) - mid))
        l1, l2 = ' '.join(words[:k]), ' '.join(words[k:])
        layouts.append((max(_textw(l1), _textw(l2)) / 100.0, 2.05, [l1, l2]))
    best = None
    for LOOSE, (ar, lines_h, lines) in [(L, lay) for L in (False, True) for lay in layouts]:
        ys, xs = cyx[:, 0].astype(np.float64), cyx[:, 1].astype(np.float64)
        lo = np.zeros(len(ys)); hi = np.full(len(ys), float(max(hh_, ww_)))
        for _ in range(14):                       # binary search the biggest text height at every candidate
            h = (lo + hi) / 2; bh = h * lines_h * 0.9; bw = h * ar
            y1 = np.clip(np.round(ys - bh / 2), 0, hh_).astype(int); y2 = np.clip(np.round(ys + bh / 2), 0, hh_).astype(int)
            x1 = np.clip(np.round(xs - bw / 2), 0, ww_).astype(int); x2 = np.clip(np.round(xs + bw / 2), 0, ww_).astype(int)
            area = np.maximum(1, (bh) * (bw))
            inside = (ii[y2, x2] - ii[y1, x2] - ii[y2, x1] + ii[y1, x1]) / area
            okf = (io[y2, x2] - io[y1, x2] - io[y2, x1] + io[y1, x1]) / area
            ok = (inside >= 0.9) | (LOOSE & (okf >= 0.93) & (inside >= 0.45))
            lo = np.where(ok, h, lo); hi = np.where(ok, hi, h)
        far = np.hypot(ys - cy, xs - cx) / span
        score = lo * (1 - 0.55 * np.minimum(far, 1)) * (1.0 if lines_h == 1 else 0.93)
        k = int(np.argmax(score))
        # a name on the country's own land wins unless it would be under 45% of the size it gets over its own sea
        sc_ = score[k] * (0.45 if LOOSE else 1.0)
        if best is None or sc_ > best[0]:
            best = (sc_, int(xs[k]) + x0s, int(ys[k]) + y0s, float(lo[k]), lines)
    if best:
        _, x, y, h, lines = best
        c['label'] = {'x': x, 'y': y, 'th': round(h, 1), 'lines': lines}

json.dump(world, open(os.path.join(OUT, 'world.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print('labels rewritten')
