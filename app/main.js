import { makeScenario } from '../core/scenario.js';
import { step, live, unitAt, pathFor, orderMove, orderAttack, orderHold, battleFactors, topFactors, hourOf, isNight, lossPct, STOCK_MAX } from '../core/sim.js';
import { makeBriefing, approve, commanderStep, afterAction, candidatePlans, utility, COMMANDERS } from '../core/commander.js';
import { Renderer } from './render.js';
import { t, setLang, getLang } from './i18n.js';

const $ = (id) => document.getElementById(id);
const PLACE = { en: { bridge: 'Iron Bridge', ford: 'The ford', town: 'Tal Rumman' }, ar: { bridge: 'الجسر الحديدي', ford: 'المخاضة', town: 'تل الرمّان' } };

// ---- A designed error screen instead of a blank page ----
function crash(err) {
  try {
    $('crashTitle').textContent = t('err_title'); $('crashBody').textContent = t('err_body');
    $('crashInfo').textContent = String((err && (err.stack || err.message)) || err).slice(0, 300);
    $('crashBtn').textContent = t('err_reload'); $('crash').hidden = false; $('boot').classList.add('gone');
  } catch (_) { /* nothing more we can do */ }
}
window.addEventListener('error', (e) => crash(e.error || e.message));
window.addEventListener('unhandledrejection', (e) => crash(e.reason));
$('crashBtn').onclick = () => location.reload();

let store = null;
try { store = window.localStorage; store.getItem('x'); } catch (_) { store = null; }
const saved = (k) => { try { return store ? store.getItem(k) : null; } catch (_) { return null; } };
const save = (k, v) => { try { if (store) store.setItem(k, v); } catch (_) { /* optional */ } };

setLang(saved('lang') || ((navigator.language || '').startsWith('ar') ? 'ar' : 'en'));

let seed = Number(saved('seed')) || 13;
let game = makeScenario(seed);
const ui = { mode: 'intro', speed: 1, intent: { why: null, risk: 'balanced', lossCap: 0.3 }, briefing: null, options: null, adjust: 0, selected: null, view: null, manual: false, seenEvents: 0, calledOff: false };
const R = new Renderer($('map'));
R.centerOn(6, 5);
window.__vigil = { get game() { return game; }, ui, R };

// ---- Sheet (the single contextual panel) ----
const sheet = $('sheet');
function setSheet(html) { sheet.innerHTML = html; sheet.classList.toggle('hide', !html); R.padBottom = html && window.innerWidth < 720 ? Math.min(sheet.offsetHeight, window.innerHeight * 0.62) : 0; }
const pct = (v) => Math.round(v * 100) + '%';
const uname = (id) => t('u_' + id);

function renderSheet() {
  const m = ui.mode;
  if (ui.view) return renderView();
  if (m === 'intro') return setSheet(`<div class="eyebrow">${t('cmd_name')}</div><p class="radio">${t('intro_radio')}</p><button class="btn gold" data-act="start">${t('give_order')}</button>`);
  if (m === 'what') return setSheet(`<div class="eyebrow">1 / 3</div><p class="prompt">${t('what_prompt')}</p>`);
  if (m === 'why') return setSheet(`<div class="eyebrow">2 / 3 · ${t('what_town')}</div><p class="prompt">${t('why_prompt')}</p>` +
    ['road', 'destroy', 'cheap'].map((w) => `<button class="choice" data-act="why" data-v="${w}"><b>${t('why_' + w)}</b><small>${t('why_' + w + '_s')}</small></button>`).join(''));
  if (m === 'limits') return setSheet(`<div class="eyebrow">3 / 3</div><p class="prompt">${t('limits_prompt')}</p><div class="label"><span>${t('risk')}</span></div>
    <div class="seg">${['careful', 'balanced', 'bold'].map((r) => `<button data-act="risk" data-v="${r}" class="${ui.intent.risk === r ? 'on' : ''}">${t(r)}</button>`).join('')}</div>
    <div class="label"><span>${t('loss_cap')}</span><b id="capV">${pct(ui.intent.lossCap)}</b></div>
    <input type="range" id="cap" min="10" max="60" step="5" value="${Math.round(ui.intent.lossCap * 100)}">
    <button class="btn gold" data-act="send">${t('send')}</button>`);
  if (m === 'thinking') return setSheet(`<div class="think"><span class="radar"></span><span>${t('thinking')}</span></div>`);
  if (m === 'briefing') {
    const b = ui.briefing, e = b.est;
    return setSheet(`<div class="eyebrow">${t('briefing')} · ${t('cmd_name')}</div><h2 class="plan-name">${t('plan_' + b.planId)}</h2><p class="plan-line">${t('line_' + b.planId)}</p>
      <div class="stats"><div class="stat good"><b>${pct(e.pWin)}</b><small>${t('win')}</small></div><div class="stat bad"><b>${Math.round(e.lossLo * 100)}–${Math.round(e.lossHi * 100)}%</b><small>${t('losses')}</small></div><div class="stat"><b>${t('about')} ${Math.round(e.hours)}${t('hours')}</b><small>${t('took')}</small></div></div>
      <div class="note"><b>${t('risk_label')}:</b> ${t(b.risk)} <span class="conf">${t('confidence')}: ${t('conf_' + b.confidence)}</span></div>
      <div class="adjust"><span>${t('faster')}</span><input type="range" id="adj" min="-2" max="2" step="1" value="${ui.adjust}"><span>${t('safer')}</span></div>
      <div class="row"><button class="btn ghost" data-act="myway">${t('my_way')}</button><button class="btn gold" data-act="approve">${t('approve')}</button></div>`);
  }
  if (m === 'run') {
    if (game.cmd && game.cmd.halted) return setSheet(`<div class="eyebrow">${t('cmd_name')}</div><p class="radio">${t('halted')}</p><div class="row"><button class="btn danger" data-act="withdraw">${t('withdraw')}</button><button class="btn" data-act="raise">${t('raise_cap')}</button></div>`);
    if (ui.manual && !ui.selected) return setSheet(`<p class="prompt" style="margin:0">${t('manual_hint')}</p>`);
    return setSheet('');
  }
  setSheet('');
}

function barRow(label, v, color) { return `<div class="bar"><span>${label}</span><i><u style="width:${Math.max(0, Math.min(100, v * 100))}%;background:${color}"></u></i><b>${Math.round(v * 100)}</b></div>`; }

function renderView() {
  const v = ui.view;
  if (v.type === 'unit') {
    const u = game.units.find((x) => x.id === v.id);
    if (!u || !u.alive) { ui.view = null; ui.selected = R.selected = null; return renderSheet(); }
    if (u.side === 'e' && !game.visible[u.id]) {
      const b = game.belief[u.id]; if (!b) { ui.view = null; return renderSheet(); }
      const age = (game.tick - b.tick) * 10;
      return setSheet(`<button class="close" data-act="close">✕</button><div class="unit-head"><h3>${t('t_' + b.type)}</h3></div>
        <div class="tags"><span class="tag ${b.conf === 'confirmed' && age <= 60 ? 'blue' : 'amber'}">${b.conf === 'confirmed' && age <= 60 ? t('confirmed') : t('reported')}</span><span class="tag">${t('minutes_old', { m: Math.max(0, age) })}</span></div>`);
    }
    const tags = [];
    if (u.engaged) tags.push(`<span class="tag red">${t('engaged')}</span>`);
    if (u.broken) tags.push(`<span class="tag red">${t('broken')}</span>`);
    if (u.dug >= 18) tags.push(`<span class="tag blue">${t('dug')}</span>`);
    if (u.side === 'p') tags.push(u.inSupply ? `<span class="tag blue">${t('in_supply')}</span>` : u.stock > 0 ? `<span class="tag amber">${t('on_stocks', { h: u.stock.toFixed(1) })}</span>` : `<span class="tag red">${t('dry')}</span>`);
    const col = u.side === 'p' ? 'var(--blue)' : 'var(--red)';
    return setSheet(`<button class="close" data-act="close">✕</button><div class="unit-head"><h3>${uname(u.id)}</h3><small>${t('t_' + u.type)}</small></div>
      <div class="bars">${barRow(t('strength'), u.str / u.maxStr, col)}${barRow(t('morale'), u.morale / 80, 'var(--gold)')}${u.side === 'p' ? barRow(t('supply'), u.stock > 0 ? u.stock / STOCK_MAX : 0, 'var(--amber)') : ''}</div><div class="tags">${tags.join('')}</div>`);
  }
  if (v.type === 'battle') {
    const b = game.battles[v.key];
    if (!b) { ui.view = null; return renderSheet(); }
    const ours = b.attackerSide === 'p';
    const odds = ours ? b.last.odds : 1 - b.last.odds;
    const sign = ours ? 1 : -1;
    const rows = b.last.top.top.map((f) => factorRow(t('f_' + f.key), f.lo * sign)).join('') + factorRow(t('other'), b.last.top.other * sign);
    return setSheet(`<button class="close" data-act="close">✕</button><div class="eyebrow">${t('battle_card')} · ${uname(b.defender)}</div>
      <div class="odds"><b>${pct(odds)}</b><div style="flex:1"><div class="label"><span>${t('odds')}</span></div><div class="oddsbar"><i style="width:${odds * 100}%"></i></div></div></div>
      <div class="label"><span>${t('factors')}</span></div>${rows}`);
  }
}
function factorRow(label, lo) {
  const w = Math.min(50, Math.abs(lo) * 45);
  return `<div class="factor"><span>${label}</span><div class="fbar"><i class="${lo >= 0 ? 'pos' : 'neg'}" style="width:${w}%"></i></div></div>`;
}

// ---- Actions ----
sheet.addEventListener('click', (ev) => {
  const b = ev.target.closest('[data-act]'); if (!b) return;
  const a = b.dataset.act, v = b.dataset.v;
  if (a === 'start') { ui.mode = 'what'; R.pulseObjective = true; R.centerOn(8, 5); }
  else if (a === 'why') { ui.intent.why = v; ui.mode = 'limits'; }
  else if (a === 'risk') { ui.intent.risk = v; }
  else if (a === 'send') { ui.mode = 'thinking'; renderSheet(); setTimeout(think, 650); return; }
  else if (a === 'approve') { approve(game, ui.briefing, ui.adjust ? 'adjusted' : 'commander'); ui.mode = 'run'; ui.manual = false; R.pulseObjective = false; R.size = 28; R.centerOn(7, 6); setTimeout(() => R.setArrows([]), 2500); }
  else if (a === 'myway') { ui.mode = 'run'; ui.manual = true; game.cmd = null; game.knownAtPlan = Object.fromEntries(Object.keys(game.belief).map((k) => [k, true])); R.setArrows([]); R.pulseObjective = false; }
  else if (a === 'close') { ui.view = null; ui.selected = R.selected = null; }
  else if (a === 'raise') { game.cmd.lossCap += 0.15; game.cmd.halted = null; game.cmd.fresh = true; }
  else if (a === 'withdraw') { ui.calledOff = true; game.result = { win: false, tick: game.tick, why: 'called_off' }; }
  renderSheet();
});
sheet.addEventListener('input', (ev) => {
  if (ev.target.id === 'cap') { ui.intent.lossCap = Number(ev.target.value) / 100; $('capV').textContent = pct(ui.intent.lossCap); }
  if (ev.target.id === 'adj') { ui.adjust = Number(ev.target.value); pickPlan(); renderSheet(); }
});

function think() {
  const b = makeBriefing(game, { ...ui.intent });
  ui.options = [{ plan: b.plan, est: b.est, planId: b.planId }, ...b.alternatives.map((a) => ({ plan: candidatePlans(game).find((p) => p.id === a.planId), est: a.est, planId: a.planId }))];
  ui.base = b; ui.adjust = 0;
  R.size = Math.max(18, Math.min(26, window.innerWidth / 19)); R.centerOn(7, 6);
  pickPlan(); ui.mode = 'briefing'; renderSheet();
}
// The Adjust dial re-weighs the plans she already worked out; it never hides them.
function pickPlan() {
  const riskKey = { frontal: 'risk_chokepoint', flank: 'risk_supply', siege: 'risk_slow' };
  const scored = ui.options.map((o) => ({ ...o, u: utility(o.est, ui.intent.why, ui.intent.risk, COMMANDERS.haddad, ui.adjust / 2) })).sort((a, b) => b.u - a.u);
  const best = scored[0];
  ui.briefing = { ...ui.base, planId: best.planId, plan: best.plan, est: best.est, risk: riskKey[best.planId], adjust: ui.adjust };
  showArrows(best.plan);
}
function showArrows(plan) {
  const arrows = [];
  const sim = structuredClone(game);
  for (const ph of plan.phases) for (const [id, type, hex] of ph.orders) {
    const u = sim.units.find((x) => x.id === id); if (!u || u.type === 'art') continue;
    if (u.c === hex[0] && u.r === hex[1]) continue;
    const p = pathFor(sim, u, hex, true); if (!p || !p.path.length) continue;
    arrows.push({ path: [[u.c, u.r], ...p.path], color: type === 'attack' ? '#f2c66d' : '#4aa8ff' });
    const end = type === 'attack' ? p.path[p.path.length - 2] || [u.c, u.r] : hex; u.c = end[0]; u.r = end[1];
  }
  R.setArrows(arrows);
}

// ---- Map input: drag to pan, pinch to zoom, tap to select ----
const cv = $('map'); const ptrs = new Map(); let moved = 0, pinch0 = 0, size0 = 0;
cv.addEventListener('pointerdown', (e) => { cv.setPointerCapture(e.pointerId); ptrs.set(e.pointerId, [e.clientX, e.clientY]); moved = 0; if (ptrs.size === 2) { const [a, b] = [...ptrs.values()]; pinch0 = Math.hypot(a[0] - b[0], a[1] - b[1]); size0 = R.size; } });
cv.addEventListener('pointermove', (e) => {
  const p = ptrs.get(e.pointerId); if (!p) return;
  if (ptrs.size === 1) { const dx = e.clientX - p[0], dy = e.clientY - p[1]; R.cx -= dx; R.cy -= dy; moved += Math.abs(dx) + Math.abs(dy); R.clampCam(game.map); }
  ptrs.set(e.pointerId, [e.clientX, e.clientY]);
  if (ptrs.size === 2) { const [a, b] = [...ptrs.values()]; const d = Math.hypot(a[0] - b[0], a[1] - b[1]); const ns = Math.max(18, Math.min(56, (size0 * d) / pinch0)); const k = ns / R.size; R.cx *= k; R.cy *= k; R.size = ns; moved = 99; }
});
const up = (e) => { const had = ptrs.has(e.pointerId); ptrs.delete(e.pointerId); if (had && moved < 10 && ptrs.size === 0) tap(e.clientX, e.clientY); };
cv.addEventListener('pointerup', up); cv.addEventListener('pointercancel', (e) => ptrs.delete(e.pointerId));
cv.addEventListener('wheel', (e) => { const ns = Math.max(18, Math.min(56, R.size * (e.deltaY < 0 ? 1.1 : 0.9))); const k = ns / R.size; R.cx *= k; R.cy *= k; R.size = ns; }, { passive: true });

function tap(px, py) {
  const hex = R.pick(game.map, px, py); if (!hex) return;
  const [c, r] = hex;
  if (ui.mode === 'what') { if (c === game.objective[0] && r === game.objective[1]) { ui.mode = 'why'; renderSheet(); } return; }
  if (ui.mode !== 'run' && ui.mode !== 'briefing' && ui.mode !== 'intro') return;
  const u = unitAt(game, c, r);
  const ghost = Object.entries(game.belief).find(([id, b]) => !game.visible[id] && b.c === c && b.r === r);
  const sel = ui.selected && game.units.find((x) => x.id === ui.selected);
  if (ui.manual && ui.mode === 'run' && sel && sel.side === 'p' && sel.alive && !(u && u.side === 'p')) {
    const enemyHere = (u && u.side === 'e' && game.visible[u.id]) || ghost;
    if (enemyHere) orderAttack(game, sel, [c, r]); else orderMove(game, sel, [c, r]);
    ui.selected = R.selected = null; ui.view = null; renderSheet(); return;
  }
  if (u && (u.side === 'p' || game.visible[u.id])) { ui.selected = R.selected = u.id; ui.view = { type: 'unit', id: u.id }; }
  else if (ghost) { ui.selected = R.selected = ghost[0]; ui.view = { type: 'unit', id: ghost[0] }; }
  else { ui.selected = R.selected = null; ui.view = null; }
  renderSheet();
}

// ---- Top bar ----
$('speed').addEventListener('click', (e) => { const b = e.target.closest('button'); if (!b) return; ui.speed = Number(b.dataset.s); for (const x of $('speed').children) x.classList.toggle('on', x === b); });
$('langBtn').onclick = () => { setLang(getLang() === 'en' ? 'ar' : 'en'); save('lang', getLang()); paintStatic(); renderSheet(); if (!$('report').hidden) showReport(); };
$('battleChip').onclick = () => { const k = $('battleChip').dataset.key; if (k) { ui.view = { type: 'battle', key: k }; renderSheet(); } };
function paintStatic() {
  $('langBtn').textContent = t('lang'); $('cmdName').textContent = t('cmd_name'); $('cmdTrait').textContent = t('cmd_trait'); $('bootSub').textContent = t('loading');
}

function toast(text, cls = '') { const d = document.createElement('div'); d.className = 'toast ' + cls; d.textContent = text; $('toasts').appendChild(d); setTimeout(() => d.remove(), 4300); while ($('toasts').children.length > 3) $('toasts').firstChild.remove(); }
function pumpEvents() {
  for (; ui.seenEvents < game.events.length; ui.seenEvents++) {
    const e = game.events[ui.seenEvents];
    const mine = e.unit && e.unit.startsWith('p_');
    if (e.type === 'spotted') toast(t('ev_spotted', { u: uname(e.unit) }), 'warn');
    else if (e.type === 'battle') toast(e.side === 'p' ? t('ev_battle_p', { u: uname(e.defender) }) : t('ev_battle_e', { u: uname(game.battles[e.hex.join(',')]?.attackers[0] || 'e_arm') }), e.side === 'p' ? '' : 'bad');
    else if (e.type === 'broke') toast(t(mine ? 'ev_broke_p' : 'ev_broke_e', { u: uname(e.unit) }), mine ? 'bad' : 'good');
    else if (e.type === 'destroyed') toast(t('ev_destroyed', { u: uname(e.unit) }), mine ? 'bad' : 'good');
    else if (e.type === 'surrender') toast(t('ev_surrender', { u: uname(e.unit) }), mine ? 'bad' : 'good');
    else if (e.type === 'approved') toast(t('ev_approved'), 'good');
    else if (e.type === 'phase') { const k = 'phase_' + e.plan + '_' + e.phase; if (t(k) !== k) toast(t(k), 'good'); }
    else if (e.type === 'halt') renderSheet();
  }
}

function paintHud() {
  const h = hourOf(game), hh = Math.floor(h), mm = Math.round((h - hh) * 60);
  $('clockTime').textContent = String(hh).padStart(2, '0') + ':' + String(mm).padStart(2, '0');
  $('clockIcon').className = isNight(game) ? 'moon' : 'sun'; $('clockDay').textContent = isNight(game) ? t('night') : t('day');
  const chip = $('battleChip'); const b = Object.values(game.battles)[0];
  if (b && ui.mode === 'run') { const odds = b.attackerSide === 'p' ? b.last.odds : 1 - b.last.odds; chip.hidden = false; chip.dataset.key = b.key; chip.innerHTML = `${t('battle_card')} · <b>${pct(odds)}</b>`; }
  else chip.hidden = true;
}

// ---- After-action report ----
function showReport() {
  const r = afterAction(game); const rep = $('report');
  const head = r.win ? t('victory') : ui.calledOff ? t('called_off') : t('defeat');
  const causes = r.causes.map((c, i) => `<div class="cause ${c.good ? 'good' : ''}"><span class="n">${i + 1}</span><span>${c.key === 'factor_numbers' ? t(c.good ? 'c_numbers_good' : 'c_numbers_bad') : c.key.startsWith('factor_') ? t('f_' + c.key.slice(7)) : t('c_' + c.key)}</span></div>`).join('');
  const by = r.by === 'commander' ? t('by_commander') : r.by === 'adjusted' ? t('by_adjusted') : t('by_player');
  rep.innerHTML = `<div class="rep-wrap"><div class="rep-head ${r.win ? 'win' : 'loss'}"><div class="eyebrow">${t('report')}</div><h1>${head}</h1></div>
    <div class="stats"><div class="stat"><b>${r.hours.toFixed(1)}${t('hours')}</b><small>${t('took')}</small></div><div class="stat bad"><b>${pct(r.lossPct)}</b><small>${t('our_losses')}</small></div><div class="stat good"><b>${Math.round(r.eLost)}</b><small>${t('their_losses')}</small></div></div>
    <div class="card"><h4>${t('causes')}</h4>${causes || `<div class="cause good"><span class="n">1</span><span>${t('lesson_none')}</span></div>`}</div>
    <div class="card"><h4>${t('lesson')}</h4><div style="font-size:16.5px;line-height:1.4">${t(r.lesson)}</div></div>
    <div class="card"><h4>${t('whose')}</h4><div class="kv"><span>${by}</span><b>${r.planId !== 'manual' ? t('plan_' + r.planId) : ''}</b></div>
      ${r.est ? `<div class="kv"><span>${t('predicted')}</span><b>${Math.round(r.est.lossLo * 100)}–${Math.round(r.est.lossHi * 100)}% ${t('losses')}</b></div><div class="kv"><span>${t('actual')}</span><b>${pct(r.lossPct)}</b></div>` : ''}</div>
    ${r.win ? `<div class="card"><h4>${t('earned')}</h4><div class="trait"><span class="medal"></span><span><b>${t('trait_river')}</b><small>${t('trait_river_d')}</small></span></div></div>` : ''}
    <div class="row"><button class="btn ghost" data-act="again">${t('again')}</button><button class="btn gold" data-act="new">${t('new_battle')}</button></div></div>`;
  rep.hidden = false; setSheet('');
}
$('report').addEventListener('click', (e) => {
  const b = e.target.closest('[data-act]'); if (!b) return;
  if (b.dataset.act === 'new') { seed = (seed * 7 + 11) % 100000; save('seed', String(seed)); }
  restart();
});
function restart() {
  game = makeScenario(seed); R.pos = {}; R.setArrows([]); R.selected = null; R.centerOn(6, 5);
  Object.assign(ui, { mode: 'intro', intent: { why: null, risk: 'balanced', lossCap: 0.3 }, briefing: null, options: null, adjust: 0, selected: null, view: null, manual: false, seenEvents: 0, calledOff: false, reported: false });
  $('report').hidden = true; renderSheet();
}

// ---- Loops ----
let acc = 0, lastT = performance.now(), lastSheet = 0;
function frame(now) {
  const dt = Math.min(200, now - lastT); lastT = now;
  if (ui.mode === 'run' && ui.speed > 0 && !game.result && !(game.cmd && game.cmd.halted)) {
    acc += dt * ui.speed;
    let n = 0;
    while (acc >= 520 && n < 4) { acc -= 520; n++; commanderStep(game); step(game); }
    if (n) pumpEvents();
  }
  if (game.result && !ui.reported) { ui.reported = true; pumpEvents(); setTimeout(showReport, 1400); }
  const L = PLACE[getLang()];
  R.draw(game, { labels: [[L.town, game.places.town], [L.bridge, game.places.bridge], [L.ford, game.places.ford]] });
  paintHud();
  if (ui.view && now - lastSheet > 500) { lastSheet = now; renderView(); }
  requestAnimationFrame(frame);
}
window.addEventListener('resize', () => R.resize());
paintStatic(); renderSheet();
step(game); game.tick = 0; // settle supply and vision before the first frame
requestAnimationFrame(frame);
setTimeout(() => $('boot').classList.add('gone'), 1100);
