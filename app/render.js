// The war table: a canvas map drawn like a command room at night.
import { terrainAt, roadAt, trackAt, live, isNight, supplyMap, VISION } from '../core/sim.js';
import { dist, key, neighbors } from '../core/hex.js';

const S3 = Math.sqrt(3);
const C = {
  table: '#0b1220', ink: '#0e1626',
  plain: '#2b3d40', plain2: '#304448', forest: '#1d4335', hill: '#4a4538', marsh: '#24444a', town: '#62502f', village: '#4d4530',
  water: '#11466e', waterGlow: '#2f7fb8', road: '#6f6654', track: '#5a5446',
  friend: '#4aa8ff', friendFill: '#0f2c4d', foe: '#ff5a4a', foeFill: '#4a1512', unknown: '#ffd24a', unknownFill: '#3d3210',
  supply: '#ffb347', gold: '#f2c66d', text: '#e8eef5', dim: '#8ea0b3', grid: 'rgba(160,190,220,0.07)',
};

export class Renderer {
  constructor(canvas) {
    this.cv = canvas; this.ctx = canvas.getContext('2d');
    this.size = 30; this.cx = 0; this.cy = 0; this.t = 0;
    this.pos = {}; this.padBottom = 0; this.pad = 0; this.arrows = []; this.arrowT = 0; this.selected = null; this.pulseObjective = false;
    this.grain = this.makeGrain();
    this.resize();
  }
  makeGrain() {
    const g = document.createElement('canvas'); g.width = g.height = 96;
    const x = g.getContext('2d'); const d = x.createImageData(96, 96);
    let s = 7;
    for (let i = 0; i < d.data.length; i += 4) { s = (s * 16807) % 2147483647; const v = s % 255; d.data[i] = d.data[i + 1] = d.data[i + 2] = v; d.data[i + 3] = 10; }
    x.putImageData(d, 0, 0); return g;
  }
  resize() {
    const dpr = Math.min(window.devicePixelRatio || 1, 2.5);
    this.dpr = dpr; this.w = this.cv.clientWidth; this.h = this.cv.clientHeight;
    this.cv.width = Math.round(this.w * dpr); this.cv.height = Math.round(this.h * dpr);
  }
  hexXY(c, r) { return [this.size * S3 * (c + 0.5 * (r & 1)), this.size * 1.5 * r]; }
  toScreen(c, r) { const [x, y] = this.hexXY(c, r); return [x - this.cx + this.w / 2, y - this.cy + (this.h - this.pad) / 2]; }
  centerOn(c, r) { const [x, y] = this.hexXY(c, r); this.cx = x; this.cy = y; }
  clampCam(m) {
    const [mx, my] = this.hexXY(m.w - 1, m.h - 1);
    this.cx = Math.max(-this.size, Math.min(mx + this.size, this.cx));
    this.cy = Math.max(-this.size, Math.min(my + this.size, this.cy));
  }
  pick(m, px, py) {
    let best = null, bd = Infinity;
    for (let r = 0; r < m.h; r++) for (let c = 0; c < m.w; c++) {
      const [x, y] = this.toScreen(c, r); const d = (x - px) ** 2 + (y - py) ** 2;
      if (d < bd) { bd = d; best = [c, r]; }
    }
    return bd < (this.size * 1.1) ** 2 ? best : null;
  }
  hexPath(x, y, s) {
    const k = this.ctx; k.beginPath();
    for (let i = 0; i < 6; i++) { const a = (Math.PI / 180) * (60 * i - 30); const px = x + s * Math.cos(a), py = y + s * Math.sin(a); i ? k.lineTo(px, py) : k.moveTo(px, py); }
    k.closePath();
  }
  setArrows(list) { this.arrows = list; this.arrowT = 0; }

  draw(s, opts = {}) {
    const k = this.ctx, m = s.map, sz = this.size; this.t += 1;
    this.pad += (this.padBottom - this.pad) * 0.15;
    k.setTransform(this.dpr, 0, 0, this.dpr, 0, 0);
    k.fillStyle = C.table; k.fillRect(0, 0, this.w, this.h);
    const night = isNight(s);
    const mine = live(s, 'p');
    const seen = (c, r) => mine.some((u) => dist(u.c, u.r, c, r) <= VISION);
    const rnd = (c, r, n) => { let v = Math.sin(c * 127.1 + r * 311.7 + n * 74.7) * 43758.5453; return v - Math.floor(v); };

    // Terrain
    for (let r = 0; r < m.h; r++) for (let c = 0; c < m.w; c++) {
      const [x, y] = this.toScreen(c, r);
      if (x < -sz * 2 || y < -sz * 2 || x > this.w + sz * 2 || y > this.h + sz * 2) continue;
      const tt = terrainAt(m, c, r);
      const col = { '.': rnd(c, r, 1) > 0.5 ? C.plain : C.plain2, f: C.forest, h: C.hill, m: C.marsh, w: C.water, B: C.water, F: C.water, T: C.town, v: C.village }[tt];
      this.hexPath(x, y, sz + 0.6); k.fillStyle = col; k.fill();
      k.strokeStyle = C.grid; k.lineWidth = 1; k.stroke();
      if (tt === 'f') {
        for (let i = 0; i < 7; i++) { const ax = x + (rnd(c, r, i) - 0.5) * sz * 1.3, ay = y + (rnd(c, r, i + 9) - 0.5) * sz * 1.2; k.fillStyle = i % 2 ? '#1f4a3c' : '#28594a'; k.beginPath(); k.arc(ax, ay, sz * 0.17, 0, 7); k.fill(); }
      } else if (tt === 'h') {
        k.strokeStyle = 'rgba(210,200,180,0.22)'; k.lineWidth = 1.2;
        for (let i = 0; i < 3; i++) { k.beginPath(); k.ellipse(x, y + 2, sz * (0.62 - i * 0.2), sz * (0.42 - i * 0.14), -0.3, 0, 7); k.stroke(); }
      } else if (tt === 'm') {
        k.strokeStyle = 'rgba(120,200,200,0.3)'; k.lineWidth = 1.2;
        for (let i = 0; i < 5; i++) { const ax = x + (rnd(c, r, i) - 0.5) * sz * 1.2, ay = y + (rnd(c, r, i + 5) - 0.5) * sz; k.beginPath(); k.moveTo(ax - 5, ay); k.lineTo(ax + 5, ay); k.stroke(); }
      } else if (tt === 'T' || tt === 'v') {
        const n = tt === 'T' ? 8 : 4;
        for (let i = 0; i < n; i++) { const ax = x + (rnd(c, r, i) - 0.5) * sz * 1.1, ay = y + (rnd(c, r, i + 3) - 0.5) * sz * 0.9; k.fillStyle = i % 3 ? '#8a7a5c' : '#b39b6e'; k.fillRect(ax - 3, ay - 3, 6 + rnd(c, r, i + 20) * 4, 5); }
      } else if (tt === 'w' || tt === 'B' || tt === 'F') {
        const g = k.createRadialGradient(x, y, 2, x, y, sz); g.addColorStop(0, 'rgba(60,150,210,0.55)'); g.addColorStop(1, 'rgba(14,51,80,0)');
        k.fillStyle = g; this.hexPath(x, y, sz); k.fill();
        k.strokeStyle = 'rgba(140,200,240,0.35)'; k.lineWidth = 1;
        const off = (this.t * 0.25 + c * 7) % 14;
        for (let i = -1; i < 2; i++) { k.beginPath(); k.moveTo(x - 8, y + i * 7 + off - 7); k.quadraticCurveTo(x, y + i * 7 + off - 10, x + 8, y + i * 7 + off - 7); k.stroke(); }
      }
    }
    // Roads and tracks
    const link = (test, style, width, dash) => {
      k.strokeStyle = style; k.lineWidth = width; k.lineCap = 'round'; k.setLineDash(dash || []);
      for (let r = 0; r < m.h; r++) for (let c = 0; c < m.w; c++) {
        if (!test(c, r)) continue;
        const [x, y] = this.toScreen(c, r);
        for (const [nc, nr] of neighbors(c, r, m.w, m.h)) {
          if ((nr > r || (nr === r && nc > c)) && (test(nc, nr) || (dash && (roadAt(m, nc, nr) || terrainAt(m, nc, nr) === 'F')))) { const [x2, y2] = this.toScreen(nc, nr); k.beginPath(); k.moveTo(x, y); k.lineTo(x2, y2); k.stroke(); }
        }
      }
      k.setLineDash([]);
    };
    link((c, r) => roadAt(m, c, r), '#3b3528', sz * 0.34);
    link((c, r) => roadAt(m, c, r), C.road, sz * 0.2);
    link((c, r) => trackAt(m, c, r), C.track, sz * 0.12, [5, 6]);
    // Bridge and ford marks
    for (let r = 0; r < m.h; r++) for (let c = 0; c < m.w; c++) {
      const tt = terrainAt(m, c, r); const [x, y] = this.toScreen(c, r);
      if (tt === 'B') { k.fillStyle = '#9c8f76'; k.fillRect(x - sz * 0.8, y - sz * 0.16, sz * 1.6, sz * 0.32); k.strokeStyle = '#d9cba8'; k.lineWidth = 1.5; k.strokeRect(x - sz * 0.8, y - sz * 0.16, sz * 1.6, sz * 0.32); }
      if (tt === 'F') { k.strokeStyle = '#cfe6f5'; k.lineWidth = 2; k.setLineDash([3, 5]); k.beginPath(); k.moveTo(x - sz * 0.7, y); k.lineTo(x + sz * 0.7, y); k.stroke(); k.setLineDash([]); }
    }
    // Supply: amber light flowing out from our depot along what it can reach.
    if (!opts.hideSupply) {
      const reach = supplyMap(s, 'p');
      k.strokeStyle = C.supply; k.lineWidth = 2; k.setLineDash([4, 10]); k.lineDashOffset = -(this.t * 0.6); k.globalAlpha = 0.85; k.shadowColor = C.supply; k.shadowBlur = 8;
      for (let r = 0; r < m.h; r++) for (let c = 0; c < m.w; c++) {
        const on = (cc, rr) => reach.has(key(cc, rr)) && (roadAt(m, cc, rr) || trackAt(m, cc, rr) || 'BF'.includes(terrainAt(m, cc, rr)));
        if (!on(c, r)) continue;
        const [x, y] = this.toScreen(c, r);
        for (const [nc, nr] of neighbors(c, r, m.w, m.h)) if ((nr > r || (nr === r && nc > c)) && on(nc, nr)) { const [x2, y2] = this.toScreen(nc, nr); k.beginPath(); k.moveTo(x, y); k.lineTo(x2, y2); k.stroke(); }
      }
      k.setLineDash([]); k.globalAlpha = 1; k.shadowBlur = 0;
    }
    // Fog of war: what we cannot see is dimmed.
    for (let r = 0; r < m.h; r++) for (let c = 0; c < m.w; c++) {
      if (seen(c, r)) continue; const [x, y] = this.toScreen(c, r);
      this.hexPath(x, y, sz + 0.6); k.fillStyle = 'rgba(5,9,18,0.36)'; k.fill();
    }
    // Place names
    k.textAlign = 'center'; k.font = `600 ${Math.max(11, sz * 0.4)}px Rajdhani, Tajawal, sans-serif`;
    for (const [name, hex] of opts.labels || []) { const [x, y] = this.toScreen(hex[0], hex[1]); k.fillStyle = 'rgba(8,12,22,0.7)'; const w = k.measureText(name).width + 10; k.fillRect(x - w / 2, y + sz * 0.62, w, sz * 0.5); k.fillStyle = C.gold; k.fillText(name, x, y + sz * 0.99); }
    // Objective ring
    const [ox, oy] = this.toScreen(s.objective[0], s.objective[1]);
    const pulse = 0.5 + 0.5 * Math.sin(this.t * 0.07);
    k.strokeStyle = C.gold; k.lineWidth = this.pulseObjective ? 3 : 1.6; k.globalAlpha = this.pulseObjective ? 0.5 + 0.5 * pulse : 0.6;
    this.hexPath(ox, oy, sz * (this.pulseObjective ? 1.02 + 0.1 * pulse : 1)); k.stroke(); k.globalAlpha = 1;
    // Plan arrows draw themselves
    if (this.arrows.length) {
      this.arrowT = Math.min(1, this.arrowT + 0.02);
      for (const a of this.arrows) {
        const pts = a.path.map(([c, r]) => this.toScreen(c, r)); if (pts.length < 2) continue;
        const total = pts.length - 1, upto = this.arrowT * total;
        k.strokeStyle = a.color || C.friend; k.lineWidth = sz * 0.2; k.lineCap = 'round'; k.lineJoin = 'round'; k.globalAlpha = 0.85; k.shadowColor = a.color || C.friend; k.shadowBlur = 10;
        k.beginPath(); k.moveTo(pts[0][0], pts[0][1]); let last = pts[0], prev = pts[0];
        for (let i = 1; i <= total; i++) {
          if (i <= upto) { k.lineTo(pts[i][0], pts[i][1]); prev = last; last = pts[i]; }
          else { const f = upto - (i - 1); if (f > 0) { const x = pts[i - 1][0] + (pts[i][0] - pts[i - 1][0]) * f, y = pts[i - 1][1] + (pts[i][1] - pts[i - 1][1]) * f; k.lineTo(x, y); prev = pts[i - 1]; last = [x, y]; } break; }
        }
        k.stroke();
        const ang = Math.atan2(last[1] - prev[1], last[0] - prev[0]);
        k.fillStyle = a.color || C.friend; k.beginPath(); k.moveTo(last[0] + Math.cos(ang) * sz * 0.5, last[1] + Math.sin(ang) * sz * 0.5);
        k.lineTo(last[0] + Math.cos(ang + 2.4) * sz * 0.4, last[1] + Math.sin(ang + 2.4) * sz * 0.4); k.lineTo(last[0] + Math.cos(ang - 2.4) * sz * 0.4, last[1] + Math.sin(ang - 2.4) * sz * 0.4); k.closePath(); k.fill();
        k.globalAlpha = 1; k.shadowBlur = 0;
      }
    }
    // Battles: a pulsing ring where the fighting is
    for (const b of Object.values(s.battles)) { const [x, y] = this.toScreen(b.hex[0], b.hex[1]); const p = (this.t % 40) / 40; k.strokeStyle = `rgba(255,150,80,${1 - p})`; k.lineWidth = 3; k.beginPath(); k.arc(x, y, sz * (0.6 + p * 0.9), 0, 7); k.stroke(); }

    // Units
    const drawUnit = (id, type, side, x, y, o) => {
      const col = side === 'p' ? C.friend : o.ghost ? C.unknown : C.foe, fill = side === 'p' ? C.friendFill : o.ghost ? C.unknownFill : C.foeFill;
      const w = sz * 1.05, h = sz * 0.74;
      k.globalAlpha = o.alpha ?? 1; k.lineWidth = 2; k.strokeStyle = col; k.fillStyle = fill; k.shadowColor = col; k.shadowBlur = o.selected ? 16 : 6;
      k.beginPath();
      if (side === 'p') k.roundRect(x - w / 2, y - h / 2, w, h, 3);
      else if (o.ghost) { for (let i = 0; i < 4; i++) { const a = (Math.PI / 2) * i; k.moveTo(x + Math.cos(a) * h * 0.28 + h * 0.36, y + Math.sin(a) * h * 0.28); k.arc(x + Math.cos(a) * h * 0.28, y + Math.sin(a) * h * 0.28, h * 0.36, 0, 7); } }
      else { k.moveTo(x, y - h * 0.72); k.lineTo(x + w * 0.56, y); k.lineTo(x, y + h * 0.72); k.lineTo(x - w * 0.56, y); k.closePath(); }
      if (o.ghost) k.setLineDash([4, 4]);
      k.fill(); k.stroke(); k.setLineDash([]); k.shadowBlur = 0;
      // Branch symbol
      k.strokeStyle = col; k.fillStyle = col; k.lineWidth = 1.6;
      const iw = w * 0.3, ih = h * 0.28;
      if (o.ghost && !type) { k.font = `700 ${h * 0.6}px sans-serif`; k.textAlign = 'center'; k.fillText('?', x, y + h * 0.2); }
      else if (type === 'inf') { k.beginPath(); k.moveTo(x - iw, y - ih); k.lineTo(x + iw, y + ih); k.moveTo(x + iw, y - ih); k.lineTo(x - iw, y + ih); k.stroke(); }
      else if (type === 'arm') { k.beginPath(); k.ellipse(x, y, iw, ih * 0.8, 0, 0, 7); k.stroke(); }
      else if (type === 'art') { k.beginPath(); k.arc(x, y, ih * 0.55, 0, 7); k.fill(); }
      // Strength bar and state marks
      if (o.str != null) { const bw = w * 0.9; k.fillStyle = 'rgba(0,0,0,0.6)'; k.fillRect(x - bw / 2, y + h * 0.62, bw, 3.5); k.fillStyle = col; k.fillRect(x - bw / 2, y + h * 0.62, bw * Math.max(0, Math.min(1, o.str)), 3.5); }
      if (o.dug) { k.strokeStyle = C.text; k.lineWidth = 1.5; k.beginPath(); k.moveTo(x - 6, y - h * 0.62); k.lineTo(x, y - h * 0.88); k.lineTo(x + 6, y - h * 0.62); k.stroke(); }
      if (o.low) { k.fillStyle = C.supply; k.beginPath(); k.arc(x + w * 0.5, y - h * 0.5, 4.5, 0, 7); k.fill(); k.fillStyle = '#231400'; k.font = '700 7px sans-serif'; k.textAlign = 'center'; k.fillText('!', x + w * 0.5, y - h * 0.5 + 2.5); }
      if (o.broken) { k.strokeStyle = '#fff'; k.lineWidth = 2; k.beginPath(); k.moveTo(x - w * 0.5, y + h * 0.5); k.lineTo(x + w * 0.5, y - h * 0.5); k.stroke(); }
      k.globalAlpha = 1;
    };
    for (const u of s.units) {
      if (!u.alive) continue;
      const [tx, ty] = this.hexXY(u.c, u.r);
      const p = (this.pos[u.id] ||= { x: tx, y: ty });
      p.x += (tx - p.x) * 0.12; p.y += (ty - p.y) * 0.12;
      const x = p.x - this.cx + this.w / 2, y = p.y - this.cy + (this.h - this.pad) / 2;
      if (u.side === 'p') drawUnit(u.id, u.type, 'p', x, y, { str: u.str / u.maxStr, dug: u.dug >= 18, low: u.sigma < 0.75 || (!u.inSupply && s.tick > 1), broken: u.broken > 0, selected: this.selected === u.id, alpha: u.sigma < 0.5 ? 0.7 : 1 });
      else if (s.visible[u.id]) drawUnit(u.id, u.type, 'e', x, y, { str: u.str / u.maxStr, dug: u.dug >= 18, broken: u.broken > 0, selected: this.selected === u.id });
    }
    for (const [id, b] of Object.entries(s.belief)) {
      if (s.visible[id]) continue;
      const [x, y] = this.toScreen(b.c, b.r);
      const age = s.tick - b.tick;
      drawUnit(id, b.conf === 'confirmed' ? b.type : b.type, 'e', x, y, { ghost: b.conf !== 'confirmed' || age > 6, alpha: Math.max(0.45, 0.9 - age * 0.01), selected: this.selected === id });
    }
    // Night, vignette and grain give the table its depth.
    if (night) { k.fillStyle = 'rgba(6,12,36,0.36)'; k.fillRect(0, 0, this.w, this.h); }
    const v = k.createRadialGradient(this.w / 2, this.h / 2, Math.min(this.w, this.h) * 0.3, this.w / 2, this.h / 2, Math.max(this.w, this.h) * 0.75);
    v.addColorStop(0, 'rgba(0,0,0,0)'); v.addColorStop(1, 'rgba(2,5,12,0.55)'); k.fillStyle = v; k.fillRect(0, 0, this.w, this.h);
    k.fillStyle = k.createPattern(this.grain, 'repeat'); k.fillRect(0, 0, this.w, this.h);
  }
}
