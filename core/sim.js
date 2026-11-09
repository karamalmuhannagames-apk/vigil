// The simulation. Pure and deterministic: step(state) advances one tick (10 game minutes).
// State is plain JSON so it can be cloned for planning, saved, and replayed.
import { neighbors, dist, adjacent, pathfind, flood, key } from './hex.js';

export const TICK_MIN = 10;
export const STOCK_MAX = 6;        // hours of supply a unit carries (Blitz scale)
export const HALF_LIFE = 4;        // hours for supply to halve once stocks are gone
export const SUPPLY_RANGE = { p: 30, e: 12 };  // supply reach: our truck columns are long, their depot is small
export const VISION = 2;
const K_LOSS = 0.02, K_MORALE = 4;

export const clone = (s) => structuredClone(s);

export function rand(s) {
  let t = (s.rng = (s.rng + 0x6d2b79f5) >>> 0);
  t = Math.imul(t ^ (t >>> 15), t | 1);
  t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
}

export const idx = (m, c, r) => r * m.w + c;
export const terrainAt = (m, c, r) => m.terrain[idx(m, c, r)];
export const roadAt = (m, c, r) => m.road[idx(m, c, r)] === 1;
export const trackAt = (m, c, r) => m.road[idx(m, c, r)] === 2;
export const unitAt = (s, c, r) => s.units.find((u) => u.alive && u.c === c && u.r === r);
export const live = (s, side) => s.units.filter((u) => u.alive && (!side || u.side === side));
export const hourOf = (s) => (s.startHour + (s.tick * TICK_MIN) / 60) % 24;
export const isNight = (s) => { const h = hourOf(s); return h >= 19 || h < 5; };
export const effective = (u) => u.alive && u.broken === 0;

// Movement cost of entering a hex, by unit type. Infinity = impassable.
export function moveCost(m, type, c, r) {
  const t = terrainAt(m, c, r);
  if (t === 'w') return Infinity;
  const armor = type === 'arm' || type === 'art';
  if (t === 'B') return 1;
  if (t === 'F') return armor ? 5 : 4;
  if (roadAt(m, c, r)) return 1;
  if (trackAt(m, c, r)) return 1.5;
  if (t === 'f' || t === 'h') return armor ? 4 : 3;
  if (t === 'm') return armor ? 6 : 4;
  return armor ? 1.5 : 2;
}
const SPEED = { inf: 0.5, arm: 0.8, art: 0.5 };

function supplyCost(m, c, r) {
  const t = terrainAt(m, c, r);
  if (t === 'w') return Infinity;
  if (t === 'B' || roadAt(m, c, r)) return 1;
  if (t === 'F') return 4;
  if (trackAt(m, c, r)) return 1.5;
  if (t === 'f' || t === 'h') return 7;
  if (t === 'm') return 9;
  return 5;
}

// Which hexes each side can supply. Enemy units and the hexes next to them block the flow,
// unless a friendly unit stands there.
export function supplyMap(s, side) {
  const m = s.map;
  const blocked = new Set();
  for (const e of s.units) {
    if (!e.alive || e.side === side) continue;
    blocked.add(key(e.c, e.r));
    if (e.broken === 0) for (const [nc, nr] of neighbors(e.c, e.r, m.w, m.h)) blocked.add(key(nc, nr));
  }
  for (const f of s.units) if (f.alive && f.side === side) blocked.delete(key(f.c, f.r));
  const d = s.depots[side];
  return flood(m.w, m.h, d, (c, r) => (blocked.has(key(c, r)) ? Infinity : supplyCost(m, c, r)), SUPPLY_RANGE[side]);
}

function updateSupply(s) {
  for (const side of ['p', 'e']) {
    const reach = supplyMap(s, side);
    for (const u of live(s, side)) {
      u.inSupply = reach.has(key(u.c, u.r));
      const burn = (TICK_MIN / 60) * (u.engaged ? 2 : 1);
      if (u.inSupply) {
        u.stock = Math.min(STOCK_MAX, u.stock + TICK_MIN / 60);
        u.dry = Math.max(0, u.dry - TICK_MIN / 30);
      } else if (u.stock > 0) {
        u.stock = Math.max(0, u.stock - burn);
      } else {
        u.dry += burn;
      }
      u.sigma = u.stock > 0 ? 1 : 0.5 ** (u.dry / HALF_LIFE);
    }
  }
}

function knownFoes(s, side) {
  return s.units.filter((o) => o.alive && o.side !== side && o.broken === 0 && (side === 'e' || s.visible[o.id] || s.belief[o.id]));
}

// Routes respect zones of control: a unit may enter a hex next to a known enemy, but may not
// slip from one such hex to another. That is what makes a guarded bridge a real chokepoint.
export function pathFor(s, u, goal, allowGoalEnemy = true, avoidFriends = false) {
  const m = s.map;
  const foes = knownFoes(s, u.side);
  const pos = (o) => (u.side === 'p' && !s.visible[o.id] && s.belief[o.id] ? s.belief[o.id] : o);
  const zoc = (c, r) => foes.some((o) => { const q = pos(o); return dist(q.c, q.r, c, r) === 1; });
  const foeAt = (c, r) => foes.some((o) => { const q = pos(o); return q.c === c && q.r === r; });
  return pathfind(m.w, m.h, [u.c, u.r], goal, (c, r, fc, fr) => {
    const base = moveCost(m, u.type, c, r);
    if (!isFinite(base)) return Infinity;
    const isGoal = c === goal[0] && r === goal[1];
    if (foeAt(c, r)) return isGoal && allowGoalEnemy ? base : Infinity;
    // Closing with the enemy you are ordered to attack is always allowed.
    const closing = allowGoalEnemy && dist(c, r, goal[0], goal[1]) <= 1;
    if (!closing && zoc(c, r) && zoc(fc, fr)) return Infinity;
    const o = unitAt(s, c, r);
    if (o && o.side === u.side && o.id !== u.id) return avoidFriends ? (isGoal ? Infinity : base + 6) : base + 1.5;
    return base;
  });
}

export function orderMove(s, u, goal) {
  const p = pathFor(s, u, goal, false);
  if (!p) return false;
  u.order = { type: 'move', goal, path: p.path };
  u.prog = 0;
  return true;
}

export function orderAttack(s, u, target, opts = {}) {
  const p = pathFor(s, u, target, true);
  if (!p) return false;
  u.order = { type: 'attack', target, path: p.path.slice(0, -1), ...opts };
  u.prog = 0;
  return true;
}

export const orderHold = (u) => { u.order = { type: 'hold' }; u.prog = 0; };

// ---- Combat -------------------------------------------------------------------------------

const TERRAIN_DEF = { T: 1.4, f: 1.3, h: 1.3, v: 1.2 };

function artySupport(s, side, c, r) {
  let n = 0;
  for (const a of live(s, side)) {
    if (a.type === 'art' && a.broken === 0 && a.sigma > 0.4 && !a.engagedDirect && dist(a.c, a.r, c, r) <= 3) n++;
  }
  return n;
}

// Every factor is a multiplier on one side's power. lo = log-odds shift in the attacker's favour.
export function battleFactors(s, attackers, def) {
  const m = s.map;
  const f = [];
  const add = (k, mult, side) => {
    if (Math.abs(mult - 1) < 0.005) return;
    f.push({ key: k, mult, side, lo: side === 'a' ? Math.log(mult) : -Math.log(mult) });
  };
  const aRaw = attackers.reduce((t, u) => t + u.str, 0);
  const t = terrainAt(m, def.c, def.r);
  add('terrain_' + t, TERRAIN_DEF[t] || 1, 'd');
  add('dug_in', 1 + 0.3 * Math.min(1, def.dug / 18), 'd');
  // River crossing: worst crossing among the attackers, weighted by their share of strength.
  let cross = 0;
  for (const u of attackers) {
    const ut = terrainAt(m, u.c, u.r);
    if (ut === 'B') cross += (u.str / aRaw) * 0.4;
    if (ut === 'F') cross += (u.str / aRaw) * 0.5;
  }
  add('river', 1 - cross, 'a');
  const aSig = attackers.reduce((tt, u) => tt + u.str * (0.35 + 0.65 * u.sigma), 0) / aRaw;
  add('our_supply', aSig, 'a');
  add('their_supply', 0.35 + 0.65 * def.sigma, 'd');
  add('flank', attackers.length >= 3 ? 1.55 : attackers.length === 2 ? 1.3 : 1, 'a');
  let arm = 0;
  for (const u of attackers) if (u.type === 'arm') arm += (u.str / aRaw) * (t === '.' || t === 'v' ? 0.5 : t === 'T' || t === 'f' ? -0.3 : 0.15);
  add('armor', 1 + arm, 'a');
  if (def.type === 'art') add('caught_guns', 0.5, 'd');
  if (def.type === 'arm' && (t === '.' || t === 'v')) add('their_armor', 1.25, 'd');
  add('our_guns', 1 + 0.18 * artySupport(s, attackers[0].side, def.c, def.r), 'a');
  add('their_guns', 1 + 0.18 * artySupport(s, def.side, def.c, def.r), 'd');
  if (isNight(s)) add('night', 0.85, 'a');
  let A = aRaw, D = def.str;
  for (const x of f) { if (x.side === 'a') A *= x.mult; else D *= x.mult; }
  const numbers = Math.log(aRaw / def.str);
  const odds = (A * A) / (A * A + D * D);
  return { factors: f, A, D, numbers, odds, aRaw, dRaw: def.str };
}

// Top three factors by weight, with the rest folded into "other" so the card stays honest.
export function topFactors(bf, n = 3) {
  const all = [{ key: 'numbers', lo: bf.numbers }, ...bf.factors.map((x) => ({ key: x.key, lo: x.lo }))];
  all.sort((a, b) => Math.abs(b.lo) - Math.abs(a.lo));
  const top = all.slice(0, n).filter((x) => Math.abs(x.lo) > 0.02);
  const other = all.slice(n).reduce((t, x) => t + x.lo, 0);
  return { top, other };
}

function retreatHex(s, u) {
  const m = s.map;
  const enemies = live(s).filter((e) => e.side !== u.side && e.broken === 0);
  const d = s.depots[u.side];
  let best = null, bestScore = -Infinity;
  for (const [c, r] of neighbors(u.c, u.r, m.w, m.h)) {
    if (!isFinite(moveCost(m, u.type, c, r)) || unitAt(s, c, r)) continue;
    const near = Math.min(...enemies.map((e) => dist(e.c, e.r, c, r)), 9);
    if (near < 1) continue;
    const score = near * 1.5 - dist(c, r, d[0], d[1]) * 2;
    if (score > bestScore) { bestScore = score; best = [c, r]; }
  }
  return best;
}

function breakUnit(s, u, why) {
  const to = retreatHex(s, u);
  if (!to) {
    u.alive = false;
    s.stats[u.side === 'p' ? 'pLost' : 'eLost'] += u.str;
    s.events.push({ tick: s.tick, type: 'surrender', unit: u.id });
    u.str = 0;
    return;
  }
  u.c = to[0]; u.r = to[1];
  u.broken = 18; u.morale = 30; u.dug = 0; u.engaged = false;
  orderHold(u);
  s.events.push({ tick: s.tick, type: 'broke', unit: u.id, why });
}

function damage(s, u, amt) {
  const a = Math.min(u.str, amt);
  u.str -= a;
  s.stats[u.side === 'p' ? 'pLost' : 'eLost'] += a;
  if (u.str < 6) {
    s.stats[u.side === 'p' ? 'pLost' : 'eLost'] += u.str;
    u.str = 0; u.alive = false;
    s.events.push({ tick: s.tick, type: 'destroyed', unit: u.id });
  }
}

function resolveBattles(s) {
  const groups = {};
  for (const u of s.units) { u.engaged = false; u.engagedDirect = false; }
  for (const u of s.units) {
    if (!effective(u) || u.order.type !== 'attack' || u.order.path.length) continue;
    const [tc, tr] = u.order.target;
    const d = unitAt(s, tc, tr);
    if (!d || d.side === u.side || !adjacent(u.c, u.r, tc, tr)) continue;
    (groups[key(tc, tr)] ||= []).push(u);
  }
  const seen = new Set();
  for (const k of Object.keys(groups)) {
    const atk = groups[k];
    const [tc, tr] = k.split(',').map(Number);
    const def = unitAt(s, tc, tr);
    if (!def) continue;
    seen.add(k);
    const bf = battleFactors(s, atk, def);
    let b = s.battles[k];
    if (!b) {
      b = s.battles[k] = { key: k, start: s.tick, hex: [tc, tr], attackerSide: atk[0].side, defender: def.id,
        attackers: atk.map((u) => u.id), first: { odds: bf.odds, top: topFactors(bf), aRaw: bf.aRaw, dRaw: bf.dRaw },
        surprise: atk[0].side === 'p' ? !s.knownAtPlan?.[def.id] : false, aLoss: 0, dLoss: 0 };
      s.events.push({ tick: s.tick, type: 'battle', hex: [tc, tr], side: atk[0].side, defender: def.id });
    }
    b.last = { odds: bf.odds, top: topFactors(bf) };
    for (const id of atk.map((u) => u.id)) if (!b.attackers.includes(id)) b.attackers.push(id);
    for (const u of atk) { u.engaged = true; u.engagedDirect = true; }
    def.engaged = true; def.engagedDirect = true;
    const share = bf.A / (bf.A + bf.D);
    const dLoss = K_LOSS * bf.A * (0.8 + 0.4 * rand(s)) / 1;
    const aLoss = K_LOSS * bf.D * (0.8 + 0.4 * rand(s));
    b.aLoss += aLoss; b.dLoss += dLoss;
    damage(s, def, dLoss);
    for (const u of atk) damage(s, u, aLoss * (u.str / bf.aRaw || 0));
    def.morale -= K_MORALE * share * (1 + 0.25 * (atk.length - 1)) * (def.sigma < 0.6 ? 1.4 : 1);
    for (const u of atk) u.morale -= K_MORALE * (1 - share) * (u.sigma < 0.6 ? 1.4 : 1);
    // No fixed breaking point: below 40 morale a unit may break, and more likely the lower it gets.
    let won = null;
    if (!def.alive) won = 'a';
    else if (def.morale < 40 && rand(s) < (40 - def.morale) / 60) { breakUnit(s, def, 'battle'); won = 'a'; }
    for (const u of atk) {
      if (u.alive && u.morale < 40 && rand(s) < (40 - u.morale) / 60) breakUnit(s, u, 'battle');
    }
    const still = atk.filter((u) => effective(u));
    if (won === 'a') {
      if (still.length) {
        const lead = still.reduce((x, y) => (y.str > x.str ? y : x));
        if (!unitAt(s, tc, tr) && !lead.order.noAdvance) { lead.c = tc; lead.r = tr; lead.dug = 0; }
        for (const u of still) orderHold(u);
      }
      endBattle(s, b, 'a');
    } else if (!still.length) {
      endBattle(s, b, 'd');
    }
  }
  for (const k of Object.keys(s.battles)) if (!seen.has(k)) endBattle(s, s.battles[k], 'broken_off');
}

function endBattle(s, b, winner) {
  b.end = s.tick; b.winner = winner;
  s.battleLog.push(b);
  delete s.battles[b.key];
  s.events.push({ tick: s.tick, type: 'battle_end', hex: b.hex, winner, side: b.attackerSide });
}

// ---- Movement, vision, upkeep ---------------------------------------------------------------

function moveUnits(s) {
  for (const u of s.units) {
    if (!effective(u) || u.engaged) continue;
    const o = u.order;
    if ((o.type !== 'move' && o.type !== 'attack') || !o.path.length) continue;
    const [nc, nr] = o.path[0];
    const occ = unitAt(s, nc, nr);
    if (occ) {
      if (occ.side !== u.side) {
        // Ran into an enemy on the route (possibly one we did not know about): fight it.
        u.order = { type: 'attack', target: [nc, nr], path: [], bumped: true };
      } else {
        // A friend is in the way: wait a moment, then find a way around.
        u.wait = (u.wait || 0) + 1;
        if (u.wait > 2) {
          const goal = o.type === 'move' ? o.goal : o.target;
          const p = pathFor(s, u, goal, o.type === 'attack', true);
          if (p) o.path = o.type === 'attack' ? p.path.slice(0, -1) : p.path;
          u.wait = 0;
        }
      }
      continue;
    }
    u.wait = 0;
    u.prog += SPEED[u.type] * (isNight(s) ? 0.8 : 1) * (0.5 + 0.5 * u.sigma);
    const cost = moveCost(s.map, u.type, nc, nr);
    if (u.prog >= cost) {
      u.prog -= cost; u.c = nc; u.r = nr; u.dug = 0;
      o.path.shift();
      if (!o.path.length && o.type === 'move') orderHold(u);
    }
  }
}

function updateVision(s) {
  const mine = live(s, 'p');
  s.visible = {};
  for (const e of live(s, 'e')) {
    const seen = mine.some((u) => dist(u.c, u.r, e.c, e.r) <= VISION) || e.engagedDirect;
    if (seen) {
      s.visible[e.id] = true;
      if (!s.belief[e.id]) s.events.push({ tick: s.tick, type: 'spotted', unit: e.id, hex: [e.c, e.r] });
      s.belief[e.id] = { c: e.c, r: e.r, tick: s.tick, conf: 'confirmed', type: e.type, str: Math.round(e.str) };
    }
  }
  for (const id of Object.keys(s.belief)) {
    const e = s.units.find((u) => u.id === id);
    if (!e.alive) { delete s.belief[id]; continue; }
    const b = s.belief[id];
    // We can see the hex and nothing is there: the report is stale.
    if (!s.visible[id] && mine.some((u) => dist(u.c, u.r, b.c, b.r) <= VISION)) delete s.belief[id];
  }
}

function upkeep(s) {
  for (const u of s.units) {
    if (!u.alive) continue;
    if (u.broken > 0) { u.broken--; if (u.broken === 0) u.morale = Math.max(u.morale, 45); }
    if (!u.engaged) {
      if (u.order.type === 'hold') u.dug = Math.min(30, u.dug + 1);
      u.morale = Math.min(80, u.morale + (u.inSupply ? 0.5 : 0.2));
    }
  }
}

// ---- The enemy (plays by the same rules) -----------------------------------------------------

function enemyAI(s) {
  const mine = live(s, 'e').filter(effective);
  const foes = live(s, 'p').filter(effective);
  for (const u of mine) {
    if (u.type !== 'arm') continue;
    if (u.order.type === 'attack' && unitAt(s, ...u.order.target)?.side === 'p') continue;
    let best = null, bestOdds = 0.52;
    for (const f of foes) {
      if (dist(u.c, u.r, f.c, f.r) > 3) continue;
      const odds = battleFactors(s, [u], f).odds;
      if (odds > bestOdds) { bestOdds = odds; best = f; }
    }
    if (best) orderAttack(s, u, [best.c, best.r]);
    else if (u.order.type !== 'hold' && !u.engaged) orderHold(u);
  }
}

function checkResult(s) {
  if (s.result) return;
  const [oc, or] = s.objective;
  const holder = unitAt(s, oc, or);
  if (holder && holder.side === 'p') { s.result = { win: true, tick: s.tick }; return; }
  const able = live(s, 'p').filter((u) => u.type !== 'art' && u.broken === 0);
  if (!able.length && !live(s, 'p').some((u) => u.type !== 'art' && u.broken > 0)) s.result = { win: false, tick: s.tick, why: 'destroyed' };
  if (s.tick >= 36 * 6) s.result = { win: false, tick: s.tick, why: 'time' };
}

export function step(s) {
  if (s.result) return s;
  s.tick++;
  enemyAI(s);
  updateSupply(s);
  moveUnits(s);
  resolveBattles(s);
  upkeep(s);
  updateVision(s);
  checkResult(s);
  return s;
}

export function lossPct(s) {
  return s.stats.pLost / s.stats.pStart;
}
