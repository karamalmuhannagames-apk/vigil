// Hex grid helpers. Pointy-top hexes, "odd-r" offset coordinates: (c, r).
const EVEN = [[1, 0], [0, -1], [-1, -1], [-1, 0], [-1, 1], [0, 1]];
const ODD = [[1, 0], [1, -1], [0, -1], [-1, 0], [0, 1], [1, 1]];

export const key = (c, r) => c + ',' + r;

export function neighbors(c, r, w, h) {
  const d = r & 1 ? ODD : EVEN;
  const out = [];
  for (const [dc, dr] of d) {
    const nc = c + dc, nr = r + dr;
    if (nc >= 0 && nr >= 0 && nc < w && nr < h) out.push([nc, nr]);
  }
  return out;
}

function cube(c, r) {
  const x = c - (r - (r & 1)) / 2;
  const z = r;
  return [x, -x - z, z];
}

export function dist(c1, r1, c2, r2) {
  const a = cube(c1, r1), b = cube(c2, r2);
  return Math.max(Math.abs(a[0] - b[0]), Math.abs(a[1] - b[1]), Math.abs(a[2] - b[2]));
}

export const adjacent = (c1, r1, c2, r2) => dist(c1, r1, c2, r2) === 1;

// Dijkstra over the grid. cost(c, r, fromC, fromR) returns step cost or Infinity.
export function pathfind(w, h, start, goal, cost, maxCost = Infinity) {
  const best = new Map();
  const prev = new Map();
  const open = [[0, start[0], start[1]]];
  best.set(key(start[0], start[1]), 0);
  while (open.length) {
    let bi = 0;
    for (let i = 1; i < open.length; i++) if (open[i][0] < open[bi][0]) bi = i;
    const [g, c, r] = open.splice(bi, 1)[0];
    if (c === goal[0] && r === goal[1]) {
      const path = [];
      let k = key(c, r);
      while (k !== key(start[0], start[1])) {
        const [pc, pr] = k.split(',').map(Number);
        path.unshift([pc, pr]);
        k = prev.get(k);
      }
      return { path, cost: g };
    }
    if (g > best.get(key(c, r))) continue;
    for (const [nc, nr] of neighbors(c, r, w, h)) {
      const step = cost(nc, nr, c, r);
      if (!isFinite(step)) continue;
      const ng = g + step;
      if (ng > maxCost) continue;
      const k = key(nc, nr);
      if (!best.has(k) || ng < best.get(k)) {
        best.set(k, ng);
        prev.set(k, key(c, r));
        open.push([ng, nc, nr]);
      }
    }
  }
  return null;
}

// Cost-limited flood fill. Returns Map(key -> cost).
export function flood(w, h, start, cost, maxCost) {
  const best = new Map();
  const open = [[0, start[0], start[1]]];
  best.set(key(start[0], start[1]), 0);
  while (open.length) {
    let bi = 0;
    for (let i = 1; i < open.length; i++) if (open[i][0] < open[bi][0]) bi = i;
    const [g, c, r] = open.splice(bi, 1)[0];
    if (g > best.get(key(c, r))) continue;
    for (const [nc, nr] of neighbors(c, r, w, h)) {
      const step = cost(nc, nr, c, r);
      if (!isFinite(step)) continue;
      const ng = g + step;
      if (ng > maxCost) continue;
      const k = key(nc, nr);
      if (!best.has(k) || ng < best.get(k)) {
        best.set(k, ng);
        open.push([ng, nc, nr]);
      }
    }
  }
  return best;
}
