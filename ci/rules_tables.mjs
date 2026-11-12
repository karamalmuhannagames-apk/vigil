// Prints the unit, damage and economy tables of the rules doc from core/rules (the single source of truth).
import { UNITS, KINDS, MISSILE_COST, upkeep } from '../core/rules/units.js';
import { CITY_OUTPUT, PROVINCE_OUTPUT, BUILDINGS, PROVINCE_BUILDINGS, levelCost, researchCost } from '../core/rules/economy.js';
const L = (u) => u.id;
const cap = { soft: 'soft', armoured: 'armoured', plane: 'plane', helicopter: 'helicopter', drone: 'drone', ship: 'ship', sub: 'sub' };
const v = (x) => (x === undefined ? '' : Number.isInteger(x) ? x.toFixed(1) : String(x));
const KH = ['Soft', 'Armoured', 'Plane', 'Helicopter', 'Drone', 'Missile', 'Ship', 'Sub', 'Building', 'Population'];
const head = (cols) => `| ${cols.join(' | ')} |\n|${' --- |'.repeat(cols.length)}`;
const hm = (m) => `${Math.floor(m / 60)} h${m % 60 ? ' ' + (m % 60) + ' min' : ''}`;
const fmt = (o) => Object.entries(o).map(([r, x]) => `${x} ${r === 'rare' ? 'rare metals' : r}`).join(', ');
const out = {};
out.kind = head(['#', 'Unit', 'Kind', 'Health']) + '\n' + UNITS.map((u) => `| ${u.id} | ${u.name} | ${u.kind} | ${u.hp} |`).join('\n');
const tbl = (key) => head(['#', 'Unit', ...KH]) + '\n' + UNITS.map((u) => `| ${u.id} | ${u.name} | ${KINDS.map((k) => { const x = u[key][k]; return x === undefined ? '' : v(x) + ((u.l3 || []).includes(k) ? ' (L3)' : ''); }).join(' | ')} |`).join('\n');
out.atk = tbl('atk'); out.def = tbl('def');
out.cost = head(['#', 'Unit', 'Money', 'Manpower', 'Steel', 'Oil', 'Chips', 'Rare metals', 'Build time', 'Needs', 'Upkeep per game day']) + '\n' +
  UNITS.map((u) => { const c = u.cost; return `| ${u.id} | ${u.name} | ${c.money || ''} | ${c.manpower || ''} | ${c.steel || ''} | ${c.oil || ''} | ${c.chips || ''} | ${c.rare || ''} | ${hm(u.min)} | ${u.needs.replace(/(\D+)(\d)/, (m, a, b) => ({ barracks: 'barracks', factory: 'factory', airport: 'airport', port: 'port' }[a]) + ' ' + b)} | ${fmt(upkeep(u))} |`; }).join('\n');
out.missile = head(['Reload', 'Cost of one missile or salvo']) + '\n' + Object.entries({ salvo: 'Rocket salvo (U8)', loiter: 'Loitering drone (U12)', air: 'Air-launched missile', cruise: 'Cruise missile (U11, ships, subs)', srbm: 'Short-range ballistic (U9)', mrbm: 'Medium-range ballistic (U10)' }).map(([k, n]) => `| ${n} | ${fmt(MISSILE_COST[k])} |`).join('\n');
out.city = head(['City', 'Money', 'Manpower', 'Food', 'Oil', 'Steel', 'Chips', 'Rare metals']) + '\n' + Object.entries(CITY_OUTPUT).map(([n, o]) => `| ${n} | ${o.money} | ${o.manpower} | ${o.food} | ${o.oil} | ${o.steel} | ${o.chips} | ${o.rare} |`).join('\n');
out.build = head(['Building', 'Level 1 cost', 'Level 5 cost', 'What it does']) + '\n' + Object.entries({ ...BUILDINGS, ...PROVINCE_BUILDINGS }).map(([n, b]) => `| ${n.replace(/([A-Z])/g, ' $1').toLowerCase()} | ${fmt(b.cost)} | ${BUILDINGS[n] ? fmt(levelCost(b.cost, 5)) : 'one level'} | ${b.effect} |`).join('\n');
const ex = ['U1', 'U5', 'U17', 'U28', 'U16'].map((id) => UNITS.find((u) => u.id === id));
out.research = head(['Unit', 'Level 1', 'Level 2', 'Level 3', 'Level 4', 'Level 5']) + '\n' + ex.map((u) => `| ${u.name} | ${[1, 2, 3, 4, 5].map((l) => { const r = researchCost(u, l); return `${r.money} money, ${r.chips} chips, ${r.hours} h`; }).join(' | ')} |`).join('\n');
console.log(JSON.stringify(out));
