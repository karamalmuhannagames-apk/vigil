// The commander: turns an Intent Order (what + why + limits) into a plan, briefs it,
// carries it out, and writes the after-action report. Decisions are utility scores;
// no language model is involved anywhere in here.
import { clone, step, live, unitAt, effective, orderMove, orderAttack, orderHold, battleFactors, lossPct, rand } from './sim.js';
import { dist, adjacent, neighbors } from './hex.js';

export const COMMANDERS = {
  haddad: { id: 'haddad', trait: 'careful', background: 'engineer', w: { loss: 0.35, risk: 0.5, time: -0.1 } },
};

export const WHYS = {
  road: { win: 1.0, loss: 0.7, time: 0.5, kills: 0.1 },      // "so our supply trucks can pass"
  destroy: { win: 1.0, loss: 0.5, time: 0.1, kills: 0.7 },   // "so their garrison is finished"
  cheap: { win: 0.8, loss: 1.6, time: 0.1, kills: 0.0 },     // "at the lowest cost in lives"
};
export const RISK = { careful: { loss: 1.4, time: 0.7, risk: 1.5 }, balanced: { loss: 1, time: 1, risk: 1 }, bold: { loss: 0.7, time: 1.5, risk: 0.4 } };

// Three ways to take the town. Each is a list of phases; a phase gives orders and waits for a condition.
export function candidatePlans(s) {
  const P = s.places;
  const [tc, tr] = P.town;
  const guard = [8, 5];
  return [
    { id: 'frontal', phases: [
      { orders: [['p_art', 'move', [5, 5]], ['p_inf1', 'attack', guard], ['p_arm', 'move', [6, 5]], ['p_inf2', 'move', [5, 4]]], until: { type: 'clear', hex: guard } },
      { orders: [['p_art', 'move', [8, 5]], ['p_inf1', 'attack', [tc, tr]], ['p_arm', 'attack', [tc, tr]], ['p_inf2', 'attack', [tc, tr]]], until: { type: 'taken' } },
    ] },
    { id: 'flank', phases: [
      { orders: [['p_art', 'move', [5, 5]], ['p_inf1', 'move', [6, 5]], ['p_arm', 'attack', [11, 6]], ['p_inf2', 'move', [10, 6]]], until: { type: 'arrived', units: ['p_arm', 'p_inf2'] } },
      { orders: [['p_arm', 'attack', [tc, tr]], ['p_inf2', 'attack', [tc, tr]], ['p_inf1', 'move', [6, 5]]], until: { type: 'taken' } },
    ] },
    { id: 'siege', phases: [
      { orders: [['p_art', 'move', [5, 5]], ['p_inf1', 'move', [6, 5]], ['p_arm', 'attack', [11, 6]], ['p_inf2', 'move', [10, 6]]], until: { type: 'arrived', units: ['p_arm', 'p_inf2'] } },
      { orders: [], until: { type: 'starved', unit: 'e_town', ticks: 66 } },
      { orders: [['p_inf2', 'attack', [tc, tr]], ['p_arm', 'attack', [tc, tr]], ['p_inf1', 'move', [6, 5]]], until: { type: 'taken' } },
    ] },
  ];
}

function issue(s, o) {
  const [id, type, hex] = o;
  const u = s.units.find((x) => x.id === id);
  if (!u || !effective(u)) return;
  (s.cmd.assign ||= {})[id] = o;
  if (type === 'move') { if (!(u.c === hex[0] && u.r === hex[1])) orderMove(s, u, hex); }
  else if (type === 'attack') {
    const d = unitAt(s, hex[0], hex[1]);
    if (d && d.side !== u.side) orderAttack(s, u, hex);
    else if (!d) orderMove(s, u, hex);
  }
}

function phaseDone(s, ph, cmd) {
  const c = ph.until;
  if (c.type === 'taken') return false;
  if (c.type === 'clear') { const d = unitAt(s, c.hex[0], c.hex[1]); return !d || d.side === 'p'; }
  if (c.type === 'arrived') return c.units.every((id) => { const u = s.units.find((x) => x.id === id); return !u.alive || u.broken > 0 || (u.order.type === 'hold' && !u.engaged); });
  if (c.type === 'starved') {
    const e = s.units.find((x) => x.id === c.unit);
    if (!e.alive) return true;
    if (s.visible[e.id] && e.sigma < 0.55) return true;
    return s.tick - cmd.phaseStart >= c.ticks;
  }
  return false;
}

// Called every tick before the simulation steps. The commander only uses what our side can see.
export function commanderStep(s) {
  const cmd = s.cmd;
  if (!cmd || cmd.halted || s.result) return;
  const plan = cmd.plan;
  if (lossPct(s) > cmd.lossCap) {
    cmd.halted = 'loss_cap';
    for (const u of live(s, 'p')) if (!u.engaged) orderHold(u); else u.order = { type: 'hold' };
    s.events.push({ tick: s.tick, type: 'halt', why: 'loss_cap' });
    return;
  }
  let ph = plan.phases[cmd.phase];
  if (cmd.fresh) { for (const o of ph.orders) issue(s, o); cmd.fresh = false; cmd.phaseStart = s.tick; }
  if (cmd.phase < plan.phases.length - 1 && phaseDone(s, ph, cmd)) {
    cmd.phase++; cmd.fresh = true;
    s.events.push({ tick: s.tick, type: 'phase', phase: cmd.phase, plan: plan.id });
    return;
  }
  // Flank security and persistence: deal with enemies that block the way, then resume.
  for (const u of live(s, 'p')) {
    if (!effective(u) || u.type === 'art' || u.engaged) continue;
    const mine = (cmd.assign || {})[u.id];
    if (u.order.type === 'hold' && mine) {
      const at = mine[2];
      const arrived = u.c === at[0] && u.r === at[1];
      const tgt = unitAt(s, at[0], at[1]);
      if (mine[1] === 'attack' && tgt && tgt.side === 'e') {
        // A shaken or starving unit rests before it is sent in again.
        if (u.morale > 48) orderAttack(s, u, at);
        continue;
      }
      if (mine[1] === 'attack' && !tgt && !arrived && cmd.phase === plan.phases.length - 1) { orderMove(s, u, at); continue; }
      if (mine[1] === 'move' && arrived) {
        // Flank security: while waiting, overrun a weak enemy next to us if the odds are clearly good.
        const near = live(s, 'e').filter((e) => s.visible[e.id] && e.broken === 0 && adjacent(e.c, e.r, u.c, u.r) && !(e.c === s.objective[0] && e.r === s.objective[1]));
        const soft = near.map((e) => [battleFactors(s, [u], e).odds, e]).sort((a, b) => b[0] - a[0])[0];
        if (soft && soft[0] > 0.7 && u.morale > 50) orderAttack(s, u, [soft[1].c, soft[1].r], { noAdvance: true });
        continue;
      }
      if (mine[1] === 'move' && !arrived && !tgt) {
        // Something stopped us short. If a visible enemy sits next to us and the odds are fair, clear it.
        const near = live(s, 'e').filter((e) => s.visible[e.id] && adjacent(e.c, e.r, u.c, u.r));
        const soft = near.map((e) => [battleFactors(s, [u], e).odds, e]).sort((a, b) => b[0] - a[0])[0];
        if (soft && soft[0] > 0.55) orderAttack(s, u, [soft[1].c, soft[1].r]);
        else orderMove(s, u, at);
      }
    }
  }
}

// What the commander believes: our own units, plus only the enemy units intelligence knows about.
export function believedState(s) {
  const b = clone(s);
  b.units = b.units.filter((u) => u.side === 'p' || s.belief[u.id]);
  for (const u of b.units) {
    if (u.side === 'e') { const bel = s.belief[u.id]; u.c = bel.c; u.r = bel.r; u.str = bel.str; }
  }
  b.events = []; b.battleLog = []; b.battles = {};
  b.knownAtPlan = Object.fromEntries(Object.keys(s.belief).map((k) => [k, true]));
  return b;
}

export function runPlan(s, plan, lossCap, maxTicks = 216) {
  s.cmd = { plan, phase: 0, fresh: true, lossCap, halted: null, phaseStart: s.tick };
  const t0 = s.tick;
  while (!s.result && !s.cmd.halted && s.tick - t0 < maxTicks) { commanderStep(s); step(s); }
  return s;
}

// Estimate a plan by playing it out several times on the believed state.
export function evaluate(s, plan, lossCap, runs = 6) {
  const base = believedState(s);
  let wins = 0; const losses = [], hours = [], kills = [];
  for (let i = 0; i < runs; i++) {
    const t = clone(base);
    t.rng = (s.rng + 7919 * (i + 1)) >>> 0;
    runPlan(t, clone(plan), lossCap);
    const win = !!(t.result && t.result.win);
    if (win) wins++;
    losses.push(lossPct(t));
    hours.push(((t.tick - s.tick) * 10) / 60);
    kills.push(t.stats.eLost);
  }
  const avg = (a) => a.reduce((x, y) => x + y, 0) / a.length;
  return { pWin: wins / runs, loss: avg(losses), lossLo: Math.min(...losses), lossHi: Math.max(...losses), hours: avg(hours), kills: avg(kills) };
}

export function utility(est, why, risk, commander, adjust = 0) {
  const W = WHYS[why], R = RISK[risk], C = commander.w;
  const lossW = W.loss * R.loss * (1 + C.loss) * (1 + 0.5 * Math.max(0, adjust));
  const timeW = W.time * R.time * (1 + C.time) * (1 + 0.8 * Math.max(0, -adjust));
  const riskW = 0.6 * R.risk * (1 + C.risk) * (1 + 0.5 * Math.max(0, adjust));
  return W.win * est.pWin * 2 - lossW * est.loss * 3 - timeW * (est.hours / 24) * 1.2 + W.kills * (est.kills / 300) - riskW * (est.lossHi - est.lossLo) - riskW * (1 - est.pWin) * 0.5;
}

const RISK_KEY = { frontal: 'risk_chokepoint', flank: 'risk_supply', siege: 'risk_slow' };

// The Briefing: the chosen plan, the likely result, the main risk, and how sure we are.
export function makeBriefing(s, intent, adjust = 0) {
  const commander = COMMANDERS[intent.commander || 'haddad'];
  const options = candidatePlans(s).map((plan) => {
    const est = evaluate(s, plan, intent.lossCap);
    return { plan, est, u: utility(est, intent.why, intent.risk, commander, adjust) };
  });
  options.sort((a, b) => b.u - a.u);
  const best = options[0];
  const known = Object.values(s.belief);
  const confirmed = known.filter((b) => b.conf === 'confirmed').length;
  const confidence = known.length && confirmed / known.length > 0.8 ? 'high' : confirmed >= 2 ? 'medium' : 'low';
  return {
    planId: best.plan.id, plan: best.plan, est: best.est, risk: RISK_KEY[best.plan.id], confidence,
    alternatives: options.slice(1).map((o) => ({ planId: o.plan.id, est: o.est })),
    intent, adjust,
  };
}

export function approve(s, briefing, by = 'commander') {
  s.cmd = { plan: clone(briefing.plan), phase: 0, fresh: true, lossCap: briefing.intent.lossCap, halted: null, phaseStart: s.tick, by, intent: briefing.intent, est: briefing.est };
  s.knownAtPlan = Object.fromEntries(Object.keys(s.belief).map((k) => [k, true]));
  s.events.push({ tick: s.tick, type: 'approved', plan: briefing.plan.id });
}

// The After-Action Report: up to three ranked causes, built only from what really happened.
export function afterAction(s) {
  const win = !!(s.result && s.result.win);
  const causes = [];
  const pBattles = s.battleLog.filter((b) => b.attackerSide === 'p');
  const eBattles = s.battleLog.filter((b) => b.attackerSide === 'e');
  const surprise = pBattles.find((b) => b.surprise);
  if (surprise) causes.push({ key: 'cause_surprise', good: false, w: 1.2, unit: surprise.defender });
  if (s.events.some((e) => e.type === 'halt')) causes.push({ key: 'cause_cap', good: false, w: 1.5 });
  const dry = s.units.filter((u) => u.side === 'p' && u.dry > 0.5);
  if (dry.length) causes.push({ key: 'cause_our_supply', good: false, w: 0.9 + 0.2 * dry.length });
  const starving = s.units.find((u) => u.id === 'e_town');
  if (starving && starving.dry > 0.5) causes.push({ key: 'cause_their_supply', good: true, w: 1.3 });
  if (eBattles.some((b) => b.winner === 'a')) causes.push({ key: 'cause_counterattack', good: false, w: 1.1 });
  // Weigh the factors of the battles that decided the day.
  const tally = {};
  for (const b of pBattles) {
    const scale = b.hex[0] === s.objective[0] && b.hex[1] === s.objective[1] ? 1.5 : 1;
    for (const f of b.first.top.top) { tally[f.key] = (tally[f.key] || 0) + f.lo * scale; }
  }
  for (const [k, lo] of Object.entries(tally)) {
    if (Math.abs(lo) < 0.15) continue;
    if (k === 'their_supply' && causes.some((c) => c.key === 'cause_their_supply')) continue;
    if (k === 'our_supply' && causes.some((c) => c.key === 'cause_our_supply')) continue;
    causes.push({ key: 'factor_' + k, good: lo > 0, w: Math.abs(lo) });
  }
  // Causes that explain the actual result come first.
  causes.sort((a, b) => (b.good === win) - (a.good === win) || b.w - a.w);
  const top = causes.slice(0, 3);
  let lesson = 'lesson_none';
  if (surprise) lesson = 'lesson_recon';
  else if (top.some((c) => c.key === 'factor_river' && !c.good)) lesson = 'lesson_ford';
  else if (top.some((c) => c.key === 'cause_our_supply')) lesson = 'lesson_supply';
  else if (top.some((c) => c.key === 'cause_cap')) lesson = 'lesson_cap';
  else if (win && top.some((c) => c.key === 'cause_their_supply')) lesson = 'lesson_siege';
  else if (win && top.some((c) => c.key === 'factor_flank')) lesson = 'lesson_flank';
  return {
    win, hours: (s.tick * 10) / 60, lossPct: lossPct(s), pLost: s.stats.pLost, eLost: s.stats.eLost,
    causes: top, lesson, by: s.cmd ? s.cmd.by : 'player', planId: s.cmd ? s.cmd.plan.id : 'manual',
    est: s.cmd ? s.cmd.est : null,
  };
}
