// The map: a painted landscape, not a board. The hex grid still drives the rules underneath,
// but the player never sees it.
import { terrainAt, roadAt, trackAt, live, isNight, supplyMap, VISION } from '../core/sim.js';
import { dist, key, neighbors } from '../core/hex.js';

const S3 = Math.sqrt(3);
const H = 40;            // hex radius in world units
const PAD = 300;         // painted margin around the playable area
const Q = 0.6;           // raster detail of the painted ground
const RES = 2;           // terrain texture resolution
const COL = { friend: '#3d9bff', friendDark: '#0d2d57', foe: '#f0483a', foeDark: '#4d0f0b', ghost: '#ffd24a', supply: '#ffbe55', gold: '#f6cf7a' };

function hash(x, y) { const s = Math.sin(x * 127.1 + y * 311.7) * 43758.5453; return s - Math.floor(s); }
function vnoise(x, y) {
  const xi = Math.floor(x), yi = Math.floor(y), xf = x - xi, yf = y - yi;
  const u = xf * xf * (3 - 2 * xf), v = yf * yf * (3 - 2 * yf);
  const a = hash(xi, yi), b = hash(xi + 1, yi), c = hash(xi, yi + 1), d = hash(xi + 1, yi + 1);
  return a + (b - a) * u + (c - a) * v + (a - b - c + d) * u * v;
}
function fbm(x, y) { let t = 0, a = 0.5; for (let i = 0; i < 4; i++) { t += a * vnoise(x, y); x *= 2.03; y *= 2.03; a *= 0.5; } return t; }
const mix = (a, b, t) => a + (b - a) * t;
const clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
const wx = (c, r) => H * S3 * (c + 0.5 * (r & 1));
const wy = (c, r) => H * 1.5 * r;

function smoothLine(k, pts) {
  k.beginPath(); k.moveTo(pts[0][0], pts[0][1]);
  for (let i = 1; i < pts.length - 1; i++) { const mx = (pts[i][0] + pts[i + 1][0]) / 2, my = (pts[i][1] + pts[i + 1][1]) / 2; k.quadraticCurveTo(pts[i][0], pts[i][1], mx, my); }
  const l = pts[pts.length - 1]; k.lineTo(l[0], l[1]);
}

// Paint the whole landscape once into an off-screen picture.
function paintTerrain(m) {
  const FW = Math.ceil(wx(m.w - 1, 1) + PAD * 2), FH = Math.ceil(wy(0, m.h - 1) + PAD * 2);
  const WW = Math.ceil(FW * Q), WH = Math.ceil(FH * Q);
  const elev = new Float32Array(WW * WH), forest = new Float32Array(WW * WH), marsh = new Float32Array(WW * WH), wet = new Float32Array(WW * WH);
  const E = { h: 1, f: 0.3, '.': 0.2, m: 0.04, T: 0.22, v: 0.2, w: -0.05, B: -0.05, F: -0.02 };
  for (let py = 0; py < WH; py++) for (let px = 0; px < WW; px++) {
    const x = px / Q - PAD, y = py / Q - PAD;
    const r0 = Math.round(y / (1.5 * H)), c0 = Math.round(x / (S3 * H) - 0.5 * (r0 & 1));
    let sw = 0, se = 0, sf = 0, sm = 0, swt = 0;
    for (let r = r0 - 1; r <= r0 + 1; r++) for (let c = c0 - 1; c <= c0 + 1; c++) {
      const cc = clamp(c, 0, m.w - 1), rr = clamp(r, 0, m.h - 1);
      const t = terrainAt(m, cc, rr); const dx = x - wx(c, r), dy = y - wy(c, r);
      const w = Math.exp(-(dx * dx + dy * dy) / (H * H) * 1.5);
      sw += w; se += w * E[t]; if (t === 'f') sf += w; if (t === 'm') sm += w; if (t === 'w' || t === 'B' || t === 'F') swt += w;
    }
    const i = py * WW + px, n = fbm(x / 110, y / 110);
    elev[i] = se / sw + (n - 0.5) * 0.3 + (0.5 - Math.abs(fbm(x / 34, y / 34) - 0.5) * 2) * 0.1 * (0.6 + 4 * se / sw);
    forest[i] = sf / sw; marsh[i] = sm / sw; wet[i] = swt / sw;
  }
  const base = document.createElement('canvas'); base.width = WW; base.height = WH;
  const bk = base.getContext('2d'); const img = bk.createImageData(WW, WH); const d = img.data;
  for (let py = 0; py < WH; py++) for (let px = 0; px < WW; px++) {
    const i = py * WW + px, x = px / Q - PAD, y = py / Q - PAD;
    const e = elev[i];
    const eA = elev[Math.max(0, py - 2) * WW + Math.max(0, px - 2)], eB = elev[Math.min(WH - 1, py + 2) * WW + Math.min(WW - 1, px + 2)];
    const shade = clamp(1 + (eA - eB) * -6.5, 0.5, 1.45);        // light from the north-west
    const n1 = fbm(x / 60 + 9, y / 60 + 3), n2 = vnoise(x / 3.2, y / 3.2), n3 = fbm(x / 14, y / 14);
    // grassland to dry steppe
    let R = mix(104, 168, n1 * 0.9), G = mix(138, 152, n1 * 0.7), B = mix(72, 96, n1 * 0.8);
    // highlands turn to rock
    const rock = clamp((e - 0.45) * 2.2);
    R = mix(R, 132 + n3 * 30, rock); G = mix(G, 120 + n3 * 26, rock); B = mix(B, 94 + n3 * 20, rock);
    // forest canopy with clumps of light and dark
    const fo = clamp((forest[i] - 0.28 + (n3 - 0.5) * 0.35) * 3.2);
    const canopy = 0.72 + n2 * 0.5;
    R = mix(R, 38 * canopy, fo); G = mix(G, 84 * canopy, fo); B = mix(B, 46 * canopy, fo);
    // marsh: wet greens and dark pools
    const ma = clamp((marsh[i] - 0.3) * 3);
    const pool = clamp((n3 - 0.56) * 9);
    R = mix(R, mix(84, 34, pool), ma); G = mix(G, mix(124, 70, pool), ma); B = mix(B, mix(96, 78, pool), ma);
    // the river valley is greener and darker toward the water
    const wv = clamp(wet[i] * 1.4);
    R = mix(R, 70, wv * 0.5); G = mix(G, 112, wv * 0.5); B = mix(B, 70, wv * 0.5);
    const g = (n2 - 0.5) * 9;
    d[i * 4] = clamp((R + g) * shade, 0, 255); d[i * 4 + 1] = clamp((G + g) * shade, 0, 255); d[i * 4 + 2] = clamp((B + g) * shade, 0, 255); d[i * 4 + 3] = 255;
  }
  bk.putImageData(img, 0, 0);

  const cv = document.createElement('canvas'); cv.width = FW * RES; cv.height = FH * RES;
  const k = cv.getContext('2d'); k.imageSmoothingQuality = 'high'; k.drawImage(base, 0, 0, cv.width, cv.height);
  k.setTransform(RES, 0, 0, RES, PAD * RES, PAD * RES);
  const rnd = (c, r, n) => hash(c * 3.1 + n * 17.7, r * 5.3 + n * 1.3);

  // Farm fields give the open country a lived-in look.
  for (let r = 0; r < m.h; r++) for (let c = 0; c < m.w; c++) {
    if (terrainAt(m, c, r) !== '.' || rnd(c, r, 1) < 0.35) continue;
    const n = 1 + Math.floor(rnd(c, r, 2) * 3);
    for (let i = 0; i < n; i++) {
      const fx = wx(c, r) + (rnd(c, r, 3 + i) - 0.5) * H * 1.2, fy = wy(c, r) + (rnd(c, r, 7 + i) - 0.5) * H * 1.1;
      const fw = 16 + rnd(c, r, 11 + i) * 22, fh = 11 + rnd(c, r, 15 + i) * 14, ang = (rnd(c, r, 19 + i) - 0.5) * 1.2;
      k.save(); k.translate(fx, fy); k.rotate(ang);
      k.fillStyle = ['rgba(196,178,92,0.5)', 'rgba(120,150,70,0.5)', 'rgba(170,140,84,0.45)', 'rgba(142,168,84,0.5)'][Math.floor(rnd(c, r, 23 + i) * 4)];
      k.fillRect(-fw / 2, -fh / 2, fw, fh);
      k.strokeStyle = 'rgba(40,50,24,0.22)'; k.lineWidth = 0.6;
      for (let s = -fh / 2 + 2; s < fh / 2; s += 2.6) { k.beginPath(); k.moveTo(-fw / 2, s); k.lineTo(fw / 2, s); k.stroke(); }
      k.strokeStyle = 'rgba(30,40,20,0.35)'; k.lineWidth = 0.8; k.strokeRect(-fw / 2, -fh / 2, fw, fh);
      k.restore();
    }
  }
  // The river: one flowing ribbon from the top of the map to the bottom.
  const rv = [];
  for (let r = 0; r < m.h; r++) for (let c = 0; c < m.w; c++) if ('wBF'.includes(terrainAt(m, c, r))) { rv.push([wx(c, r) + (rnd(c, r, 4) - 0.5) * 10 * (terrainAt(m, c, r) === 'w' ? 1 : 0), wy(c, r)]); break; }
  rv.unshift([rv[0][0] + 14, -PAD - 10]); rv.push([rv[rv.length - 1][0] - 10, wy(0, m.h - 1) + PAD + 10]);
  k.lineCap = 'round'; k.lineJoin = 'round';
  smoothLine(k, rv); k.strokeStyle = 'rgba(40,66,40,0.55)'; k.lineWidth = 34; k.stroke();
  smoothLine(k, rv); k.strokeStyle = '#c9bd8c'; k.lineWidth = 26; k.globalAlpha = 0.55; k.stroke(); k.globalAlpha = 1;
  smoothLine(k, rv); k.strokeStyle = '#1f5f8f'; k.lineWidth = 21; k.stroke();
  smoothLine(k, rv); k.strokeStyle = '#2f7fb3'; k.lineWidth = 15; k.stroke();
  smoothLine(k, rv); k.strokeStyle = 'rgba(120,190,230,0.55)'; k.lineWidth = 5; k.setLineDash([18, 26]); k.stroke(); k.setLineDash([]);
  // The ford: pale shallows where the river can be waded.
  for (let r = 0; r < m.h; r++) for (let c = 0; c < m.w; c++) if (terrainAt(m, c, r) === 'F') {
    const x = wx(c, r), y = wy(c, r);
    k.fillStyle = 'rgba(214,202,150,0.75)'; k.beginPath(); k.ellipse(x, y, 22, 8, 0.1, 0, 7); k.fill();
    k.strokeStyle = 'rgba(150,205,235,0.9)'; k.lineWidth = 1.4;
    for (let i = -2; i <= 2; i++) { k.beginPath(); k.moveTo(x - 14, y + i * 3); k.lineTo(x + 14, y + i * 3 + 1); k.stroke(); }
  }
  // Roads and the dirt track.
  const chain = (test) => { const segs = []; for (let r = 0; r < m.h; r++) for (let c = 0; c < m.w; c++) { if (!test(c, r)) continue; for (const [nc, nr] of neighbors(c, r, m.w, m.h)) if ((nr > r || (nr === r && nc > c)) && test(nc, nr)) segs.push([[wx(c, r), wy(c, r)], [wx(nc, nr), wy(nc, nr)]]); } return segs; };
  const roadPts = []; for (let c = -1; c <= m.w; c++) roadPts.push([wx(c, 5), wy(0, 5) + Math.sin(c * 1.3) * 3.5]);
  smoothLine(k, roadPts); k.strokeStyle = 'rgba(40,34,22,0.75)'; k.lineWidth = 8.5; k.stroke();
  smoothLine(k, roadPts); k.strokeStyle = '#e3d3a4'; k.lineWidth = 5; k.stroke();
  smoothLine(k, roadPts); k.strokeStyle = 'rgba(120,100,60,0.5)'; k.lineWidth = 0.8; k.setLineDash([7, 7]); k.stroke(); k.setLineDash([]);
  const isTrackish = (c, r) => trackAt(m, c, r) || terrainAt(m, c, r) === 'F' || (c === 4 && r === 5);
  for (const [a, b] of chain(isTrackish)) { k.strokeStyle = 'rgba(60,48,28,0.55)'; k.lineWidth = 4.2; k.beginPath(); k.moveTo(a[0], a[1]); k.lineTo(b[0], b[1]); k.stroke(); k.strokeStyle = '#c9b582'; k.lineWidth = 2.2; k.setLineDash([6, 4]); k.beginPath(); k.moveTo(a[0], a[1]); k.lineTo(b[0], b[1]); k.stroke(); k.setLineDash([]); }
  // The bridge.
  for (let r = 0; r < m.h; r++) for (let c = 0; c < m.w; c++) if (terrainAt(m, c, r) === 'B') {
    const x = wx(c, r), y = wy(c, r);
    k.fillStyle = 'rgba(0,0,0,0.35)'; k.fillRect(x - 22, y - 3, 44, 12);
    k.fillStyle = '#6d6a66'; k.fillRect(x - 22, y - 7, 44, 13);
    k.fillStyle = '#dcd2b4'; k.fillRect(x - 22, y - 4.5, 44, 8);
    k.strokeStyle = '#3a3835'; k.lineWidth = 1.3; k.beginPath(); k.moveTo(x - 22, y - 7); k.lineTo(x + 22, y - 7); k.moveTo(x - 22, y + 6); k.lineTo(x + 22, y + 6); k.stroke();
    for (let i = -18; i <= 18; i += 6) { k.beginPath(); k.moveTo(x + i, y - 7); k.lineTo(x + i, y - 10); k.moveTo(x + i, y + 6); k.lineTo(x + i, y + 9); k.stroke(); }
  }
  // Towns and villages: streets, roofs and shadows.
  const settle = (c, r, n, spread) => {
    const x0 = wx(c, r), y0 = wy(c, r);
    k.fillStyle = 'rgba(150,140,118,0.6)'; k.beginPath(); k.ellipse(x0, y0, spread * 1.05, spread * 0.8, 0, 0, 7); k.fill();
    k.strokeStyle = 'rgba(225,212,170,0.9)'; k.lineWidth = 2;
    for (let i = 0; i < 3; i++) { const a = rnd(c, r, 40 + i) * 3.14; k.beginPath(); k.moveTo(x0 - Math.cos(a) * spread, y0 - Math.sin(a) * spread * 0.7); k.lineTo(x0 + Math.cos(a) * spread, y0 + Math.sin(a) * spread * 0.7); k.stroke(); }
    for (let i = 0; i < n; i++) {
      const a = rnd(c, r, 50 + i) * 6.28, rad = Math.sqrt(rnd(c, r, 80 + i)) * spread * 0.92;
      const bx = x0 + Math.cos(a) * rad, by = y0 + Math.sin(a) * rad * 0.75, bw = 5 + rnd(c, r, 110 + i) * 6, bh = 4 + rnd(c, r, 140 + i) * 4;
      k.save(); k.translate(bx, by); k.rotate((rnd(c, r, 170 + i) - 0.5) * 0.7);
      k.fillStyle = 'rgba(0,0,0,0.38)'; k.fillRect(-bw / 2 + 1.6, -bh / 2 + 1.8, bw, bh);
      k.fillStyle = ['#b9573d', '#c9b48e', '#a34a35', '#d9cfba', '#8d7d68'][Math.floor(rnd(c, r, 200 + i) * 5)]; k.fillRect(-bw / 2, -bh / 2, bw, bh);
      k.fillStyle = 'rgba(255,255,255,0.22)'; k.fillRect(-bw / 2, -bh / 2, bw, bh / 2);
      k.restore();
    }
  };
  for (let r = 0; r < m.h; r++) for (let c = 0; c < m.w; c++) { const t = terrainAt(m, c, r); if (t === 'T') settle(c, r, 46, 30); if (t === 'v') settle(c, r, 14, 17); }
  return { cv, WW: FW, WH: FH };
}

export class Renderer {
  constructor(canvas) {
    this.cv = canvas; this.ctx = canvas.getContext('2d');
    this.size = 36; this.cx = 0; this.cy = 0; this.t = 0;
    this.pos = {}; this.padBottom = 0; this.pad = 0; this.arrows = []; this.arrowT = 0; this.selected = null; this.pulseObjective = false;
    this.terrain = null; this.fog = document.createElement('canvas');
    this.sprites = {}; this.sil = {};
    for (const t of ['arm', 'inf', 'art']) { const im = new Image(); im.onload = () => { this.sprites[t] = im; }; im.src = 'art/' + t + '.png'; }
    this.resize();
  }
  resize() {
    const dpr = Math.min(window.devicePixelRatio || 1, 2.5);
    this.dpr = dpr; this.w = this.cv.clientWidth; this.h = this.cv.clientHeight;
    this.cv.width = Math.round(this.w * dpr); this.cv.height = Math.round(this.h * dpr);
    this.fog.width = Math.max(1, Math.round(this.w / 2)); this.fog.height = Math.max(1, Math.round(this.h / 2));
  }
  hexXY(c, r) { return [this.size * S3 * (c + 0.5 * (r & 1)), this.size * 1.5 * r]; }
  toScreen(c, r) { const [x, y] = this.hexXY(c, r); return [x - this.cx + this.w / 2, y - this.cy + (this.h - this.pad) / 2]; }
  centerOn(c, r) { const [x, y] = this.hexXY(c, r); this.cx = x; this.cy = y; }
  clampCam(m) { const [mx, my] = this.hexXY(m.w - 1, m.h - 1); this.cx = clamp(this.cx, 0, mx); this.cy = clamp(this.cy, 0, my); }
  pick(m, px, py) {
    let best = null, bd = Infinity;
    for (let r = 0; r < m.h; r++) for (let c = 0; c < m.w; c++) { const [x, y] = this.toScreen(c, r); const d = (x - px) ** 2 + (y - py) ** 2; if (d < bd) { bd = d; best = [c, r]; } }
    return bd < (this.size * 1.1) ** 2 ? best : null;
  }
  setArrows(list) { this.arrows = list; this.arrowT = 0; }

  // Units are real photographs cut out and set on the map, with a small status plate.
  sprite(k, x, y, sz, o) {
    const im = this.sprites[o.type]; if (!im) return false;
    const w = sz * 2.5, h = w * im.height / im.width, col = o.ghost ? COL.ghost : o.side === 'p' ? COL.friend : COL.foe;
    k.save(); k.translate(x, y);
    k.fillStyle = 'rgba(0,0,0,0.45)'; k.beginPath(); k.ellipse(0, h * 0.34, w * 0.44, h * 0.2, 0, 0, 7); k.fill();
    if (o.selected) { k.strokeStyle = '#fff'; k.lineWidth = 2; k.beginPath(); k.ellipse(0, h * 0.34, w * 0.52, h * 0.26, 0, 0, 7); k.stroke(); }
    k.save(); if (o.side === 'p') k.scale(-1, 1);
    if (o.ghost) {
      let sc = this.sil[o.type];
      if (!sc) { sc = this.sil[o.type] = document.createElement('canvas'); sc.width = im.width; sc.height = im.height; const c = sc.getContext('2d'); c.drawImage(im, 0, 0); c.globalCompositeOperation = 'source-in'; c.fillStyle = '#2b2410'; c.fillRect(0, 0, sc.width, sc.height); }
      k.globalAlpha = o.alpha ?? 0.8; k.shadowColor = COL.ghost; k.shadowBlur = 6; k.drawImage(sc, -w / 2, -h / 2, w, h); k.shadowBlur = 0;
    } else { k.globalAlpha = o.broken ? 0.55 : 1; k.drawImage(im, -w / 2, -h / 2, w, h); }
    k.restore(); k.globalAlpha = 1;
    // status plate
    const pw = sz * 1.5, ph = sz * 0.42, py = h * 0.5 + sz * 0.05;
    k.fillStyle = 'rgba(6,10,18,0.88)'; k.beginPath(); k.roundRect(-pw / 2, py, pw, ph, ph * 0.3); k.fill();
    k.fillStyle = col; k.beginPath(); k.roundRect(-pw / 2, py, ph * 0.9, ph, ph * 0.3); k.fill();
    if (o.ghost) { k.fillStyle = '#1a1300'; k.font = `700 ${ph * 0.8}px sans-serif`; k.textAlign = 'center'; k.fillText('?', -pw / 2 + ph * 0.45, py + ph * 0.78); }
    if (o.str != null) { const bx = -pw / 2 + ph * 1.1, bw = pw - ph * 1.3; k.fillStyle = 'rgba(255,255,255,0.14)'; k.fillRect(bx, py + ph * 0.34, bw, ph * 0.32); k.fillStyle = o.str > 0.5 ? '#6fe08a' : o.str > 0.25 ? '#ffc04d' : '#ff6a5c'; k.fillRect(bx, py + ph * 0.34, bw * clamp(o.str), ph * 0.32); }
    if (o.dug) { k.fillStyle = '#e9eef5'; const dy = -h * 0.5 - sz * 0.1; k.beginPath(); k.moveTo(-sz * 0.3, dy); k.lineTo(0, dy - sz * 0.26); k.lineTo(sz * 0.3, dy); k.lineTo(sz * 0.18, dy); k.lineTo(0, dy - sz * 0.13); k.lineTo(-sz * 0.18, dy); k.closePath(); k.fill(); }
    if (o.low) { const bx = pw / 2 + sz * 0.22, by = py + ph * 0.5, t = sz * 0.22; k.fillStyle = COL.supply; k.beginPath(); k.moveTo(bx, by - t); k.lineTo(bx + t, by + t * 0.8); k.lineTo(bx - t, by + t * 0.8); k.closePath(); k.fill(); k.fillStyle = '#2a1a00'; k.font = `700 ${t * 1.2}px sans-serif`; k.textAlign = 'center'; k.fillText('!', bx, by + t * 0.62); }
    k.restore(); return true;
  }

  token(k, x, y, sz, o) {
    if (o.type && this.sprite(k, x, y, sz, o)) return;
    const w = sz * 1.5, h = sz * 1.08, col = o.ghost ? COL.ghost : o.side === 'p' ? COL.friend : COL.foe, dark = o.ghost ? '#3d3210' : o.side === 'p' ? COL.friendDark : COL.foeDark;
    k.save(); k.translate(x, y); k.globalAlpha = o.alpha ?? 1;
    // ground shadow and pointer
    k.fillStyle = 'rgba(0,0,0,0.45)'; k.beginPath(); k.ellipse(0, h * 0.62, w * 0.42, h * 0.16, 0, 0, 7); k.fill();
    const cut = o.side === 'p' ? 0 : h * 0.24;
    const plate = () => { k.beginPath(); if (o.side === 'p' && !o.ghost) k.roundRect(-w / 2, -h / 2, w, h, h * 0.2); else { k.moveTo(-w / 2 + cut, -h / 2); k.lineTo(w / 2 - cut, -h / 2); k.lineTo(w / 2, -h / 2 + cut); k.lineTo(w / 2, h / 2 - cut); k.lineTo(w / 2 - cut, h / 2); k.lineTo(-w / 2 + cut, h / 2); k.lineTo(-w / 2, h / 2 - cut); k.lineTo(-w / 2, -h / 2 + cut); k.closePath(); } };
    k.shadowColor = o.selected ? '#fff' : 'rgba(0,0,0,0.6)'; k.shadowBlur = o.selected ? 16 : 8; k.shadowOffsetY = o.selected ? 0 : 3;
    const g = k.createLinearGradient(0, -h / 2, 0, h / 2); g.addColorStop(0, col); g.addColorStop(0.45, dark); g.addColorStop(1, '#070b14');
    plate(); k.fillStyle = g; k.fill(); k.shadowBlur = 0; k.shadowOffsetY = 0;
    k.lineWidth = Math.max(1.5, sz * 0.07); k.strokeStyle = o.selected ? '#fff' : col; if (o.ghost) k.setLineDash([5, 4]); k.stroke(); k.setLineDash([]);
    // silhouette
    k.fillStyle = '#f4f7fb'; k.strokeStyle = '#f4f7fb'; k.lineCap = 'round'; k.lineJoin = 'round';
    const u = sz * 0.5; k.translate(0, -h * 0.06);
    if (o.ghost && !o.type) { k.font = `700 ${h * 0.6}px sans-serif`; k.textAlign = 'center'; k.fillText('?', 0, h * 0.2); }
    else if (o.type === 'arm') {
      k.beginPath(); k.roundRect(-u * 1.05, u * 0.2, u * 2.1, u * 0.42, u * 0.2); k.fill();                    // tracks
      k.beginPath(); k.moveTo(-u * 0.9, u * 0.2); k.lineTo(-u * 0.7, -u * 0.12); k.lineTo(u * 0.8, -u * 0.12); k.lineTo(u * 1.0, u * 0.2); k.closePath(); k.fill(); // hull
      k.beginPath(); k.roundRect(-u * 0.42, -u * 0.5, u * 0.8, u * 0.42, u * 0.12); k.fill();                   // turret
      k.lineWidth = u * 0.14; k.beginPath(); k.moveTo(u * 0.3, -u * 0.3); k.lineTo(u * 1.25, -u * 0.36); k.stroke(); // gun
      k.fillStyle = dark; for (let i = -3; i <= 3; i++) { k.beginPath(); k.arc(i * u * 0.28, u * 0.41, u * 0.1, 0, 7); k.fill(); }
    } else if (o.type === 'inf') {
      k.beginPath(); k.arc(0, -u * 0.34, u * 0.3, Math.PI, 0); k.lineTo(u * 0.38, -u * 0.28); k.lineTo(-u * 0.38, -u * 0.28); k.closePath(); k.fill(); // helmet
      k.beginPath(); k.roundRect(-u * 0.2, -u * 0.28, u * 0.4, u * 0.24, u * 0.06); k.fill();                    // face
      k.beginPath(); k.moveTo(-u * 0.62, u * 0.62); k.quadraticCurveTo(-u * 0.6, u * 0.02, 0, 0); k.quadraticCurveTo(u * 0.6, u * 0.02, u * 0.62, u * 0.62); k.closePath(); k.fill(); // shoulders
      k.lineWidth = u * 0.12; k.beginPath(); k.moveTo(u * 0.3, u * 0.6); k.lineTo(u * 0.85, -u * 0.6); k.stroke(); // rifle
    } else if (o.type === 'art') {
      k.lineWidth = u * 0.2; k.beginPath(); k.moveTo(-u * 0.5, u * 0.2); k.lineTo(u * 1.05, -u * 0.5); k.stroke();  // barrel
      k.lineWidth = u * 0.12; k.beginPath(); k.moveTo(-u * 0.2, u * 0.25); k.lineTo(-u * 1.0, u * 0.6); k.stroke(); // trail
      k.beginPath(); k.moveTo(-u * 0.45, -u * 0.1); k.lineTo(u * 0.2, -u * 0.3); k.lineTo(u * 0.2, u * 0.35); k.lineTo(-u * 0.45, u * 0.35); k.closePath(); k.fill(); // shield
      k.beginPath(); k.arc(-u * 0.05, u * 0.42, u * 0.3, 0, 7); k.fill(); k.fillStyle = dark; k.beginPath(); k.arc(-u * 0.05, u * 0.42, u * 0.12, 0, 7); k.fill();
    }
    k.translate(0, h * 0.06);
    // strength bar
    if (o.str != null) { const bw = w * 0.8; k.fillStyle = 'rgba(0,0,0,0.65)'; k.fillRect(-bw / 2, h * 0.3, bw, h * 0.1); k.fillStyle = o.str > 0.5 ? '#6fe08a' : o.str > 0.25 ? '#ffc04d' : '#ff6a5c'; k.fillRect(-bw / 2, h * 0.3, bw * clamp(o.str), h * 0.1); }
    if (o.dug) { k.fillStyle = '#e9eef5'; k.beginPath(); k.moveTo(-w * 0.2, -h * 0.5); k.lineTo(0, -h * 0.72); k.lineTo(w * 0.2, -h * 0.5); k.lineTo(w * 0.12, -h * 0.5); k.lineTo(0, -h * 0.62); k.lineTo(-w * 0.12, -h * 0.5); k.closePath(); k.fill(); }
    if (o.low) { const bx = w * 0.46, by = -h * 0.46, s = h * 0.2; k.fillStyle = COL.supply; k.strokeStyle = '#2a1a00'; k.lineWidth = 1; k.beginPath(); k.moveTo(bx, by - s); k.lineTo(bx + s, by + s * 0.8); k.lineTo(bx - s, by + s * 0.8); k.closePath(); k.fill(); k.stroke(); k.fillStyle = '#2a1a00'; k.font = `700 ${s * 1.2}px sans-serif`; k.textAlign = 'center'; k.fillText('!', bx, by + s * 0.6); }
    if (o.broken) { k.strokeStyle = '#fff'; k.lineWidth = sz * 0.1; k.beginPath(); k.moveTo(-w * 0.42, h * 0.4); k.lineTo(w * 0.42, -h * 0.4); k.stroke(); }
    k.restore();
  }

  draw(s, opts = {}) {
    const k = this.ctx, m = s.map, sz = this.size; this.t += 1;
    if (!this.terrain) this.terrain = paintTerrain(m);
    this.pad += (this.padBottom - this.pad) * 0.15;
    k.setTransform(this.dpr, 0, 0, this.dpr, 0, 0);
    k.fillStyle = '#0a1018'; k.fillRect(0, 0, this.w, this.h);
    const sc = sz / H, ox = -this.cx + this.w / 2, oy = -this.cy + (this.h - this.pad) / 2;
    k.imageSmoothingQuality = 'high';
    k.drawImage(this.terrain.cv, ox - PAD * sc, oy - PAD * sc, this.terrain.WW * sc, this.terrain.WH * sc);
    const night = isNight(s);
    if (night) { k.fillStyle = 'rgba(8,16,52,0.5)'; k.fillRect(0, 0, this.w, this.h); }
    const mine = live(s, 'p');

    // Supply: small amber convoys running out from the depot along everything it reaches.
    const reach = supplyMap(s, 'p');
    const on = (c, r) => reach.has(key(c, r)) && (roadAt(m, c, r) || trackAt(m, c, r) || 'BF'.includes(terrainAt(m, c, r)));
    k.strokeStyle = COL.supply; k.lineWidth = Math.max(2, sz * 0.09); k.lineCap = 'round'; k.setLineDash([sz * 0.14, sz * 0.62]); k.lineDashOffset = -(this.t * 0.5); k.shadowColor = '#ff9a1f'; k.shadowBlur = 6;
    for (let r = 0; r < m.h; r++) for (let c = 0; c < m.w; c++) {
      if (!on(c, r)) continue; const [x, y] = this.toScreen(c, r);
      for (const [nc, nr] of neighbors(c, r, m.w, m.h)) if ((nr > r || (nr === r && nc > c)) && on(nc, nr)) { const [x2, y2] = this.toScreen(nc, nr); k.beginPath(); k.moveTo(x, y); k.lineTo(x2, y2); k.stroke(); }
    }
    k.setLineDash([]); k.shadowBlur = 0;

    // Fog of war: soft darkness that lifts around our own forces.
    const f = this.fog.getContext('2d'); f.globalCompositeOperation = 'source-over'; f.clearRect(0, 0, this.fog.width, this.fog.height);
    f.fillStyle = night ? 'rgba(4,8,20,0.62)' : 'rgba(6,10,20,0.5)'; f.fillRect(0, 0, this.fog.width, this.fog.height);
    f.globalCompositeOperation = 'destination-out';
    for (const u of mine) { const p = this.pos[u.id]; const x = (p ? p.x - this.cx + this.w / 2 : this.toScreen(u.c, u.r)[0]) / 2, y = (p ? p.y - this.cy + (this.h - this.pad) / 2 : this.toScreen(u.c, u.r)[1]) / 2; const rad = sz * S3 * (VISION + 0.7) / 2; const g = f.createRadialGradient(x, y, rad * 0.45, x, y, rad); g.addColorStop(0, 'rgba(0,0,0,1)'); g.addColorStop(1, 'rgba(0,0,0,0)'); f.fillStyle = g; f.fillRect(x - rad, y - rad, rad * 2, rad * 2); }
    k.drawImage(this.fog, 0, 0, this.w, this.h);

    // Place names
    k.textAlign = 'center'; k.font = `700 ${Math.max(12, sz * 0.46)}px Rajdhani, Tajawal, sans-serif`; k.lineJoin = 'round';
    for (const [name, hex] of opts.labels || []) { const [x, y] = this.toScreen(hex[0], hex[1]); k.strokeStyle = 'rgba(8,12,20,0.85)'; k.lineWidth = 4; k.strokeText(name, x, y + sz * 1.12); k.fillStyle = '#fff3d0'; k.fillText(name, x, y + sz * 1.12); }

    // Objective: a gold flag.
    { const [x, y] = this.toScreen(s.objective[0], s.objective[1]); const p = 0.5 + 0.5 * Math.sin(this.t * 0.08);
      if (this.pulseObjective) { const g = k.createRadialGradient(x, y, 0, x, y, sz * (1.3 + p * 0.5)); g.addColorStop(0, 'rgba(246,207,122,0.55)'); g.addColorStop(1, 'rgba(246,207,122,0)'); k.fillStyle = g; k.fillRect(x - sz * 2, y - sz * 2, sz * 4, sz * 4); }
      const fx = x + sz * 0.62, fy = y - sz * 0.5; k.strokeStyle = '#1a1408'; k.lineWidth = 3.5; k.beginPath(); k.moveTo(fx, fy + sz * 0.5); k.lineTo(fx, fy - sz * 0.75); k.stroke(); k.strokeStyle = '#f0e2b8'; k.lineWidth = 1.8; k.stroke();
      const wv = Math.sin(this.t * 0.12) * sz * 0.05; k.fillStyle = COL.gold; k.strokeStyle = '#3a2a08'; k.lineWidth = 1; k.beginPath(); k.moveTo(fx, fy - sz * 0.75); k.quadraticCurveTo(fx + sz * 0.3, fy - sz * 0.85 + wv, fx + sz * 0.62, fy - sz * 0.56); k.quadraticCurveTo(fx + sz * 0.3, fy - sz * 0.4 - wv, fx, fy - sz * 0.32); k.closePath(); k.fill(); k.stroke(); }

    // Plan arrows: broad, tapered, drawn like a staff officer's grease pencil.
    if (this.arrows.length) {
      this.arrowT = Math.min(1, this.arrowT + 0.018);
      for (const a of this.arrows) {
        const full = a.path.map(([c, r]) => this.toScreen(c, r)); if (full.length < 2) continue;
        const total = full.length - 1, upto = this.arrowT * total, n = Math.floor(upto), fr = upto - n;
        const pts = full.slice(0, n + 1); if (n < total) pts.push([mix(full[n][0], full[n + 1][0], fr), mix(full[n][1], full[n + 1][1], fr)]);
        if (pts.length < 2) continue;
        const last = pts[pts.length - 1], prev = pts[pts.length - 2], ang = Math.atan2(last[1] - prev[1], last[0] - prev[0]);
        k.lineCap = 'round'; k.lineJoin = 'round';
        smoothLine(k, pts); k.strokeStyle = 'rgba(0,0,0,0.5)'; k.lineWidth = sz * 0.36; k.stroke();
        smoothLine(k, pts); k.strokeStyle = a.color; k.lineWidth = sz * 0.24; k.globalAlpha = 0.92; k.stroke();
        smoothLine(k, pts); k.strokeStyle = 'rgba(255,255,255,0.45)'; k.lineWidth = sz * 0.06; k.stroke(); k.globalAlpha = 1;
        const hx = last[0] + Math.cos(ang) * sz * 0.5, hy = last[1] + Math.sin(ang) * sz * 0.5;
        k.fillStyle = a.color; k.strokeStyle = 'rgba(0,0,0,0.6)'; k.lineWidth = 1.5; k.beginPath(); k.moveTo(hx, hy); k.lineTo(last[0] + Math.cos(ang + 2.2) * sz * 0.5, last[1] + Math.sin(ang + 2.2) * sz * 0.5); k.lineTo(last[0] + Math.cos(ang - 2.2) * sz * 0.5, last[1] + Math.sin(ang - 2.2) * sz * 0.5); k.closePath(); k.fill(); k.stroke();
      }
    }

    // Units
    const sp = (u) => { const [tx, ty] = this.hexXY(u.c, u.r); const p = (this.pos[u.id] ||= { x: tx, y: ty }); p.x += (tx - p.x) * 0.1; p.y += (ty - p.y) * 0.1; return [p.x - this.cx + this.w / 2, p.y - this.cy + (this.h - this.pad) / 2]; };
    const order = s.units.filter((u) => u.alive).sort((a, b) => a.r - b.r);
    for (const [id, b] of Object.entries(s.belief)) {
      if (s.visible[id]) continue; const [x, y] = this.toScreen(b.c, b.r); const age = s.tick - b.tick;
      this.token(k, x, y, sz * 0.8, { side: 'e', type: b.type, ghost: true, alpha: clamp(0.95 - age * 0.006, 0.55, 0.95), selected: this.selected === id });
    }
    for (const u of order) {
      if (u.side === 'e' && !s.visible[u.id]) { sp(u); continue; }
      const [x, y] = sp(u);
      this.token(k, x, y, sz * 0.8, { side: u.side, type: u.type, str: u.str / u.maxStr, dug: u.dug >= 18, low: u.side === 'p' && (u.sigma < 0.75 || (!u.inSupply && s.tick > 1)), broken: u.broken > 0, selected: this.selected === u.id });
    }
    // Battles: muzzle flashes and smoke where the fighting is.
    for (const b of Object.values(s.battles)) {
      const [x, y] = this.toScreen(b.hex[0], b.hex[1]);
      for (let i = 0; i < 5; i++) { const ph = (this.t * 0.05 + i * 0.37) % 1; const a = i * 2.4 + Math.floor(this.t * 0.05 + i * 0.37) * 1.7; const px = x + Math.cos(a) * sz * 0.75, py = y + Math.sin(a) * sz * 0.5 - ph * sz * 0.5; k.fillStyle = `rgba(60,58,54,${0.5 * (1 - ph)})`; k.beginPath(); k.ellipse(px, py, sz * (0.14 + ph * 0.3), sz * (0.1 + ph * 0.22), 0, 0, 7); k.fill(); }
      const fl = (this.t * 0.25) % 6; if (fl < 2.2) { const a = Math.floor(this.t * 0.25 / 6) * 2.1; const px = x + Math.cos(a) * sz * 0.7, py = y + Math.sin(a) * sz * 0.5; k.fillStyle = fl < 1 ? '#fff6c8' : '#ff9a3c'; k.beginPath(); for (let i = 0; i < 10; i++) { const rr = sz * (i % 2 ? 0.12 : 0.34) * (1 - fl / 3), aa = i * 0.628 + a; i ? k.lineTo(px + Math.cos(aa) * rr, py + Math.sin(aa) * rr) : k.moveTo(px + Math.cos(aa) * rr, py + Math.sin(aa) * rr); } k.closePath(); k.fill(); }
    }
    // A soft vignette frames the table.
    const v = k.createRadialGradient(this.w / 2, this.h / 2, Math.min(this.w, this.h) * 0.4, this.w / 2, this.h / 2, Math.max(this.w, this.h) * 0.8);
    v.addColorStop(0, 'rgba(0,0,0,0)'); v.addColorStop(1, 'rgba(2,5,12,0.5)'); k.fillStyle = v; k.fillRect(0, 0, this.w, this.h);
  }
}
