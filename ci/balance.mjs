// Balance report: how each plan really does, and what the commander predicts.
import { makeScenario } from '../core/scenario.js';
import { candidatePlans, runPlan, evaluate, makeBriefing, afterAction } from '../core/commander.js';
import { lossPct } from '../core/sim.js';
const N = 40;
for (let i = 0; i < 3; i++) {
  let w = 0, loss = 0, hrs = 0, halt = 0; const causes = {};
  for (let seed = 1; seed <= N; seed++) {
    const s = makeScenario(seed * 13);
    runPlan(s, candidatePlans(s)[i], 0.6);
    if (s.result?.win) w++; if (s.cmd.halted) halt++;
    loss += lossPct(s); hrs += s.tick / 6;
    for (const c of afterAction(s).causes) causes[c.key] = (causes[c.key] || 0) + 1;
  }
  const s0 = makeScenario(13);
  const est = evaluate(s0, candidatePlans(s0)[i], 0.6);
  console.log(candidatePlans(s0)[i].id.padEnd(8), 'real win', (w / N * 100).toFixed(0) + '%', 'loss', (loss / N * 100).toFixed(0) + '%', 'hours', (hrs / N).toFixed(1), 'halted', halt,
    '| predicted win', (est.pWin * 100).toFixed(0) + '%', 'loss', (est.loss * 100).toFixed(0) + '%', 'h', est.hours.toFixed(1));
  console.log('   causes', JSON.stringify(causes));
}
for (const why of ['road', 'destroy', 'cheap']) for (const risk of ['careful', 'balanced', 'bold']) {
  const s = makeScenario(13);
  console.log(why.padEnd(8), risk.padEnd(9), '->', makeBriefing(s, { why, risk, lossCap: 0.6 }).planId);
}
