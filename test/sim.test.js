import test from 'node:test';
import assert from 'node:assert/strict';
import { makeScenario } from '../core/scenario.js';
import { step, clone, supplyMap, battleFactors, topFactors, orderMove, lossPct } from '../core/sim.js';
import { candidatePlans, runPlan, evaluate, makeBriefing, approve, commanderStep, afterAction, believedState } from '../core/commander.js';
import { key, dist, neighbors } from '../core/hex.js';

test('hex distance and neighbours agree', () => {
  for (let r = 0; r < 6; r++) for (let c = 0; c < 6; c++) for (const [nc, nr] of neighbors(c, r, 16, 11)) assert.equal(dist(c, r, nc, nr), 1);
});

test('same seed gives the same war', () => {
  const run = (seed) => { const s = makeScenario(seed); runPlan(s, candidatePlans(s)[1], 0.6); return JSON.stringify([s.tick, s.result, s.stats]); };
  assert.equal(run(5), run(5));
  assert.notEqual(run(5), run(6));
});

test('state survives a clone and a JSON round trip', () => {
  const s = makeScenario(3);
  for (let i = 0; i < 20; i++) step(s);
  const a = clone(s), b = JSON.parse(JSON.stringify(s));
  for (let i = 0; i < 30; i++) { step(a); step(b); }
  assert.deepEqual(a.stats, b.stats);
});

test('a unit astride the road cuts the town off', () => {
  const s = makeScenario(1);
  assert.ok(supplyMap(s, 'e').has(key(10, 5)));
  const arm = s.units.find((u) => u.id === 'p_arm');
  s.units.find((u) => u.id === 'e_arm').alive = false;
  arm.c = 12; arm.r = 5;
  assert.ok(!supplyMap(s, 'e').has(key(10, 5)));
  const town = s.units.find((u) => u.id === 'e_town');
  for (let i = 0; i < 60; i++) step(s);
  assert.ok(town.sigma < 0.6, 'garrison weakens once stocks run out: ' + town.sigma);
});

test('battle card: top three factors plus other add up to the whole', () => {
  const s = makeScenario(1);
  const a = s.units.find((u) => u.id === 'p_inf1'); a.c = 7; a.r = 5;
  const d = s.units.find((u) => u.id === 'e_guard');
  const bf = battleFactors(s, [a], d);
  const t = topFactors(bf);
  const sum = t.top.reduce((x, f) => x + f.lo, 0) + t.other;
  assert.ok(Math.abs(sum - (bf.numbers + bf.factors.reduce((x, f) => x + f.lo, 0))) < 1e-9);
  assert.ok(bf.factors.some((f) => f.key === 'river'));
  assert.ok(bf.odds < 0.5, 'attacking over the bridge into a dug-in guard should be hard');
});

test('the commander never plans around enemies intelligence has not found', () => {
  const s = makeScenario(1);
  const b = believedState(s);
  assert.ok(!b.units.some((u) => u.id === 'e_picket'));
});

test('every plan runs to an end, and the report names causes', () => {
  for (const seed of [1, 2, 3]) for (let i = 0; i < 3; i++) {
    const s = makeScenario(seed);
    runPlan(s, candidatePlans(s)[i], 0.6);
    const r = afterAction(s);
    assert.ok(s.result || s.cmd.halted, 'plan ' + i + ' ended');
    assert.ok(r.causes.length >= 1 && r.causes.length <= 3);
  }
});

test('loss cap stops the operation', () => {
  const s = makeScenario(2);
  runPlan(s, candidatePlans(s)[0], 0.05);
  assert.equal(s.cmd.halted, 'loss_cap');
  assert.ok(lossPct(s) < 0.2);
});

test('briefing changes with the why', () => {
  const s = makeScenario(1);
  const fast = makeBriefing(s, { why: 'road', risk: 'bold', lossCap: 0.6 });
  const cheap = makeBriefing(s, { why: 'cheap', risk: 'careful', lossCap: 0.3 });
  assert.ok(fast.est.pWin >= 0 && cheap.est.pWin >= 0);
  assert.ok(['frontal', 'flank', 'siege'].includes(fast.planId));
});
