// Paints map tiles away from the screen thread, so dragging and zooming never wait for painting.
// Same painting rules as the map page: ground textures mixed by forest / desert / rock, shaded by relief,
// coloured by who owns the land; coasts and borders as smooth curves.
let TEX = null, LUT = null, REL = null, SEA = null, STOP_LUT = null;

self.onmessage = async (ev) => {
  const m = ev.data;
  if (m.type === 'init') { TEX = m.TEX; LUT = m.LUT; SEA = m.SEA; return; }
  if (m.type === 'rel') { REL = m.rel; return; }
  if (m.type === 'tile') {
    try {
      const bmp = await paint(m);
      self.postMessage({ type: 'tile', key: m.key, bmp }, [bmp]);
    } catch (e) {
      self.postMessage({ type: 'tile', key: m.key, failed: true });
    }
  }
};

async function bitmap(url) {
  const r = await fetch(url); if (!r.ok) throw new Error('missing ' + url);
  return createImageBitmap(await r.blob());
}
function data(img, w, h) {
  const c = new OffscreenCanvas(w, h), g = c.getContext('2d', { willReadFrequently: true });
  g.imageSmoothingEnabled = true; g.imageSmoothingQuality = 'high';
  g.drawImage(img, 0, 0, w, h); return g.getImageData(0, 0, w, h).data;
}

async function paint({ z, tx, ty, C, lumI, bioI, natI }) {
  // the page hands over the three source images, so this worker never needs to load files itself
  const N0 = natI.width;
  const md = data(natI, N0, N0);
  const ids = new Int32Array(N0 * N0); for (let i = 0; i < N0 * N0; i++) ids[i] = md[i * 4] + md[i * 4 + 1] * 256 - 1;
  // smooth owner per painted pixel: where countries meet, the owner with the largest bilinear share wins
  const own = new Int32Array(C * C), sc = N0 / C;
  for (let y = 0; y < C; y++) {
    const v = Math.max(0, Math.min(N0 - 1.001, (y + 0.5) * sc - 0.5)), y0 = v | 0, fy = v - y0, y1 = Math.min(N0 - 1, y0 + 1);
    for (let x = 0; x < C; x++) {
      const u = Math.max(0, Math.min(N0 - 1.001, (x + 0.5) * sc - 0.5)), x0 = u | 0, fx = u - x0, x1 = Math.min(N0 - 1, x0 + 1);
      const a = ids[y0 * N0 + x0], b = ids[y0 * N0 + x1], c2 = ids[y1 * N0 + x0], d2 = ids[y1 * N0 + x1];
      if (a === b && a === c2 && a === d2 && fx > 0.25 && fx < 0.75 && fy > 0.25 && fy < 0.75) { own[y * C + x] = a; continue; }
      if (a === b && a === c2 && a === d2) { const e = ids[Math.max(0, y0 - 1) * N0 + x0] === a && ids[Math.min(N0 - 1, y1 + 1) * N0 + x1] === a && ids[y0 * N0 + Math.max(0, x0 - 1)] === a && ids[y1 * N0 + Math.min(N0 - 1, x1 + 1)] === a; if (e) { own[y * C + x] = a; continue; } }
      let best = a, bw = -1; const seen = [], wts = [];
      for (let j = -1; j <= 2; j++) for (let i = -1; i <= 2; i++) {
        const xi = Math.max(0, Math.min(N0 - 1, x0 + i)), yj = Math.max(0, Math.min(N0 - 1, y0 + j));
        const wx = Math.max(0, 1 - Math.abs(u - (x0 + i)) / 1.6), wy = Math.max(0, 1 - Math.abs(v - (y0 + j)) / 1.6);
        const ww = wx * wy; if (!ww) continue;
        const id = ids[yj * N0 + xi]; const k = seen.indexOf(id);
        if (k < 0) { seen.push(id); wts.push(ww); } else wts[k] += ww;
      }
      for (let k = 0; k < seen.length; k++) if (wts[k] > bw) { bw = wts[k]; best = seen[k]; }
      own[y * C + x] = best;
    }
  }
  // land mask from the id image, smoothed by upscaling (clean curved coasts)
  const mask = new OffscreenCanvas(N0, N0), mg = mask.getContext('2d'); const mi = mg.createImageData(N0, N0);
  for (let q = 0; q < md.length; q += 4) { const land = md[q] + md[q + 1] > 0 ? 255 : 0; mi.data[q] = mi.data[q + 1] = mi.data[q + 2] = land; mi.data[q + 3] = 255; }
  mg.putImageData(mi, 0, 0);
  const ms = data(mask, C, C), ld = data(lumI, C, C), bd = data(bioI, C, C);
  const outC = new OffscreenCanvas(C, C), og = outC.getContext('2d'); const out = og.createImageData(C, C), d = out.data;
  const { FN, fl, fa, fv, open, arid, rock, wave, WN } = TEX;
  const wamp = [0.4, 0.55, 0.8, 1.1, 1.3][z] || 1.3;
  const gx0 = tx * C, gy0 = ty * C;
  const lut = {};
  const relOf = (n) => (REL && REL[n]) || 'neutral';
  const idAt = (x, y) => { x = Math.max(0, Math.min(C - 1, x)); y = Math.max(0, Math.min(C - 1, y)); return own[y * C + x]; };
  for (let y = 0; y < C; y++) {
    const gy = gy0 + y, fr = (gy % FN) * FN, gr = (gy & 511) * 512, wr = (gy % WN) * WN;
    for (let x = 0; x < C; x++) {
      const q = (y * C + x) * 4, gx = gx0 + x;
      const m = ms[q];
      let n = own[y * C + x];
      const L = ld[q] / 127.5;
      let sr = 0, sg = 0, sb = 0;
      if (m < 170) {
        const cw = m > 0 ? 0.35 : Math.pow(bd[q] / 255, 3) * 0.22, k = (1 + (L - 1) * 0.3) * Math.max(0.45, 1 + wamp * wave[wr + gx % WN]);
        sr = (SEA.deep[0] + (SEA.coast[0] - SEA.deep[0]) * cw) * k; sg = (SEA.deep[1] + (SEA.coast[1] - SEA.deep[1]) * cw) * k; sb = (SEA.deep[2] + (SEA.coast[2] - SEA.deep[2]) * cw) * k;
        if (m > 14) { const e = 1 - 0.55 * Math.min(1, (m - 14) / 50); sr *= e; sg *= e; sb *= e; }
        if (m < 86) { d[q] = sr; d[q + 1] = sg; d[q + 2] = sb; d[q + 3] = 255; continue; }
      }
      if (n < 0) {
        for (let r = 1; r < 6 && n < 0; r++) n = Math.max(idAt(x - r, y), idAt(x + r, y), idAt(x, y - r), idAt(x, y + r));
        if (n < 0) { d[q] = sr; d[q + 1] = sg; d[q + 2] = sb; d[q + 3] = 255; continue; }
      }
      const gi = gr + (gx & 511), ar = bd[q + 1] / 255, rk = bd[q + 2] / 255;
      let vv = open[gi] * (1 - ar) + arid[gi] * ar;
      vv = vv * (1 - rk) + rock[gi] * rk;
      const fi = fr + gx % FN, a = fa[fi];
      if (a) {
        const dens = bd[q] / 255 + (open[(gi + 131 * 512 + 77) & 262143] - 158) * 0.006, tv = fv[fi] / 255;
        if (tv ? dens > tv : dens > 0.55) { const al = a / 255; vv = vv * (1 - al) + fl[fi] * al; }
      }
      const t = lut[n] || (lut[n] = LUT[relOf(n)]);
      const i = (Math.min(255, vv * L) | 0) * 3;
      if (m >= 170) { d[q] = t[i]; d[q + 1] = t[i + 1]; d[q + 2] = t[i + 2]; }
      else { const w = (m - 86) / 84; d[q] = sr + (t[i] - sr) * w; d[q + 1] = sg + (t[i + 1] - sg) * w; d[q + 2] = sb + (t[i + 2] - sb) * w; }
      d[q + 3] = 255;
    }
  }
  og.putImageData(out, 0, 0);
  return outC.transferToImageBitmap();
}
