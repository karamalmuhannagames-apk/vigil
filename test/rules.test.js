// Rules data and balance: checks every unit and thousands of random battles.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { UNITS, KINDS, MISSILE_COST, upkeep, byId } from '../core/rules/units.js';
import { CITY_OUTPUT, BUILDINGS, PROVINCE_BUILDINGS, levelCost, researchCost } from '../core/rules/economy.js';
import { fight } from '../ci/battle_sim.mjs';

const RES = ['money', 'manpower', 'steel', 'oil', 'chips', 'rare'];

test('every unit is complete and valid', () => {
  assert.equal(UNITS.length, 33);
  const ids = new Set();
  for (const u of UNITS) {
    assert.ok(!ids.has(u.id), `duplicate ${u.id}`); ids.add(u.id);
    assert.ok(u.name && u.ar, `${u.id} needs English and Arabic names`);
    assert.ok(KINDS.includes(u.kind), `${u.id} kind`);
    assert.ok(u.hp > 0 && u.hp <= 60, `${u.id} health`);
    assert.ok(u.speed >= 7 && u.speed <= 50, `${u.id} speed on the 1-50 scale`);
    assert.ok(u.min >= 140 && u.min <= 600, `${u.id} build time 2h20 to 10h`);
    assert.match(u.needs, /^(barracks|factory|airport|port)[1-5]$/, `${u.id} needs`);
    for (const t of [u.atk, u.def]) for (const [k, v] of Object.entries(t)) {
      assert.ok(KINDS.includes(k), `${u.id} unknown target ${k}`);
      assert.ok(Number.isFinite(v) && v > 0 && v <= 50, `${u.id} ${k}=${v}`);
    }
    for (const r of Object.keys(u.cost)) assert.ok(RES.includes(r), `${u.id} cost resource ${r}`);
    assert.ok(u.cost.money > 0, `${u.id} money cost`);
    const up = upkeep(u); assert.ok(up.money > 0 && up.food >= 0, `${u.id} upkeep`);
    if (u.missile) assert.ok(MISSILE_COST[u.missile], `${u.id} missile cost`);
    for (const k of u.l3 || []) assert.ok(u.atk[k] || u.def[k], `${u.id} level-3 ability ${k} must have a value`);
  }
});

test('owner rules hold in the data', () => {
  // ships about 2.5x infantry, planes faster than everything but missiles
  const inf = byId.U1.speed, ships = UNITS.filter((u) => u.kind === 'ship' || u.kind === 'sub');
  for (const s of ships) assert.ok(s.speed >= inf * 2 && s.speed <= inf * 2.8, `${s.id} ship speed`);
  const fastestGroundOrSea = Math.max(...UNITS.filter((u) => !['plane', 'helicopter', 'drone'].includes(u.kind)).map((u) => u.speed));
  for (const a of UNITS.filter((u) => ['plane', 'helicopter', 'drone'].includes(u.kind))) assert.ok(a.speed > fastestGroundOrSea, `${a.id} must outrun ships`);
  // tanks never hit helicopters; cruisers best sub hunters but not 50% better than destroyers
  assert.equal(byId.U5.atk.helicopter, undefined);
  assert.ok(byId.U29.atk.sub > byId.U28.atk.sub && byId.U29.atk.sub < byId.U28.atk.sub * 1.5);
  // corvettes carry no missiles; transports cannot attack
  assert.equal(byId.U33.atk.ship, undefined);
  // missiles hit harder than any gun
  const gun = Math.max(...UNITS.filter((u) => !u.missile).flatMap((u) => [u.atk.soft || 0, u.atk.armoured || 0]));
  for (const id of ['U9', 'U10', 'U11']) assert.ok(byId[id].atk.armoured > gun * 2, `${id} missile damage`);
});

test('economy numbers are sane', () => {
  for (const o of Object.values(CITY_OUTPUT)) for (const v of Object.values(o)) assert.ok(v > 0);
  for (const b of Object.values({ ...BUILDINGS, ...PROVINCE_BUILDINGS })) for (const v of Object.values(b.cost)) assert.ok(v > 0);
  for (const b of Object.values(BUILDINGS)) for (let l = 2; l <= 5; l++) for (const r of Object.keys(b.cost)) assert.ok(levelCost(b.cost, l)[r] > levelCost(b.cost, l - 1)[r]);
  for (const u of UNITS) { let prev = 0; for (let l = 1; l <= 5; l++) { const r = researchCost(u, l); assert.ok(r.money > prev && r.hours >= 3 && r.hours <= 12); prev = r.money; } }
});

test('5,000 random battles: always finish, never break numbers', () => {
  let seed = 12345; const rnd = () => (seed = (seed * 1103515245 + 12345) % 2147483648) / 2147483648;
  for (let i = 0; i < 5000; i++) {
    const a = UNITS[Math.floor(rnd() * UNITS.length)], d = UNITS[Math.floor(rnd() * UNITS.length)];
    const r = fight(a.id, d.id, 1 + Math.floor(rnd() * 60));
    for (const v of [r.a, r.d]) assert.ok(Number.isFinite(v) && v >= 0 && v <= 1, `${a.id} vs ${d.id}: ${v}`);
  }
});

test('counters work as designed (equal money)', () => {
  const wins = (a, d) => { const r = fight(a, d); return r.a - r.d; };
  assert.ok(wins('U22', 'U5') > 0.3, 'attack helicopters beat tanks');
  assert.ok(wins('U14', 'U22') > 0.3, 'short-range air defence beats helicopters');
  assert.ok(wins('U17', 'U18') > 0.3, 'fighters beat strike fighters');
  assert.ok(wins('U5', 'U4') > 0, 'tanks beat fighting vehicles');
  assert.ok(wins('U1', 'U1') < 0, 'defenders have the edge');
  assert.ok(wins('U29', 'U31') >= 0 || wins('U28', 'U31') > 0, 'warships can hunt subs');
});
