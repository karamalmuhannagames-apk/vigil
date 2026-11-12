// Battle simulator: equal-money fights between unit types, to check the damage table is balanced.
// Attacker fires its attack values, defender fires back its defence values, every round (one attack timer).
// Units fight at 25% + 75% x health left (C8). Damage spreads over the enemy stack.
// usage: node ci/battle_sim.mjs            -> matrix of value kept (%), + = row wins
import { UNITS, byId } from '../core/rules/units.js';

const BUDGET = 12000; // money per side

function stack(u) { const n = Math.max(1, Math.round(BUDGET / u.cost.money)); return { u, n, hp: Array(n).fill(u.hp) }; }
const alive = (s) => s.hp.filter((h) => h > 0);
const power = (s, table, kind) => alive(s).reduce((a, h) => a + (table[kind] || 0) * (0.25 + 0.75 * h / s.u.hp), 0);
function hit(s, dmg) {
  // spread damage evenly over living units
  let live = s.hp.map((h, i) => [h, i]).filter(([h]) => h > 0);
  while (dmg > 1e-9 && live.length) {
    const share = dmg / live.length; dmg = 0;
    for (const [, i] of live) { const take = Math.min(share, s.hp[i]); s.hp[i] -= take; dmg += share - take; }
    live = live.filter(([, i]) => s.hp[i] > 0);
  }
}
export function fight(aId, dId, rounds = 40) {
  const A = stack(byId[aId]), D = stack(byId[dId]);
  for (let r = 0; r < rounds; r++) {
    const da = power(A, A.u.atk, D.u.kind), dd = power(D, D.u.def, A.u.kind);
    if (da === 0 && dd === 0) break;
    hit(D, da); hit(A, dd);
    if (!alive(A).length || !alive(D).length) break;
  }
  const keep = (s) => alive(s).reduce((a, h) => a + h, 0) / (s.n * s.u.hp);
  return { a: keep(A), d: keep(D) };
}

const isMain = process.argv[1] && process.argv[1].endsWith('battle_sim.mjs');
if (isMain) {
  const ids = process.argv.slice(2).length ? process.argv.slice(2) : ['U1', 'U2', 'U3', 'U4', 'U5', 'U13', 'U14', 'U17', 'U18', 'U19', 'U22', 'U25', 'U26', 'U27', 'U28', 'U29', 'U31'];
  console.log('row attacks column, equal money. cell = attacker value kept - defender value kept (%)');
  console.log('      ' + ids.map((i) => i.padStart(5)).join(''));
  for (const a of ids) {
    let line = a.padEnd(6);
    for (const d of ids) {
      const ua = byId[a], ud = byId[d];
      const can = (ua.atk[ud.kind] || 0) > 0;
      if (!can) { line += '    .'; continue; }
      const r = fight(a, d);
      line += String(Math.round((r.a - r.d) * 100)).padStart(5);
    }
    console.log(line);
  }
}
