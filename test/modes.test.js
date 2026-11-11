import { test } from 'node:test';
import assert from 'node:assert/strict';
import { resolveMode, countryClass, MODES } from '../core/modes.js';

test('every mode resolves and validates', () => {
  for (const id of Object.keys(MODES)) assert.ok(resolveMode(id).id === id);
});

test('modes inherit and override deeply', () => {
  const m = resolveMode('world100');
  assert.equal(m.players.max, 100);
  assert.equal(m.players.fillWithAI, true);          // inherited from base
  assert.equal(resolveMode('nuclear').units.nuclear, true);
  assert.equal(resolveMode('standard').units.nuclear, false);
});

test('owner rules for countries', () => {
  const m = resolveMode('standard');
  assert.equal(countryClass(m, { iso: 'BHR', area_km2: 780 }), 'neutral');
  assert.equal(countryClass(m, { iso: 'QAT', area_km2: 11600 }), 'ai');
  assert.equal(countryClass(m, { iso: 'JOR', area_km2: 89000 }), 'playable');
  assert.equal(countryClass(m, { iso: 'OMN', area_km2: 309000 }), 'playable');
});

test('pay to win cannot be switched on', () => {
  assert.throws(() => resolveMode({ id: 'bad', monetisation: { payToWin: true } }));
});
