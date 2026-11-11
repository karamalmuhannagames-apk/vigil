// Game modes. Every match is built from ONE mode object, so a new mode after launch is a few lines of data,
// never new engine code. The engine reads only these fields; anything not set comes from BASE.
// Modes can extend another mode ("extends") and override any field, at any depth.

export const BASE = {
  id: 'base',
  name: { en: 'World War', ar: 'الحرب العالمية' },
  map: { id: 'world', region: null },              // region: null = whole world, or a list of country codes / art regions
  players: { max: 60, minToStart: 20, fillWithAI: true },
  speed: 1,                                        // 1 = one game day per real day; 4 = four times faster
  countries: {
    playableMinKm2: 100000,                        // owner's rule: Oman-like and bigger are playable
    neutralMaxKm2: 6000,                           // Bahrain-like: neutral land, 2 free infantry, anyone can take it
    alwaysPlayable: ['JOR', 'PSE'],
    smallStateBonus: true,                         // small playable states get a starting bonus so they are fun
  },
  economy: { scale: 4, startMultiplier: 1, upkeep: true, worldMarket: true },
  research: { slots: 2, dayGates: true, levelCap: 5 },
  diplomacy: { coalitionsMax: 6, coalitionsAllowed: true, passage: true, chatDeals: true, warIsMutual: true },
  units: { regionalStats: true, maxLevel: 5, nuclear: false, chemical: false },
  happiness: { enabled: true, revolts: true },
  ai: { aggression: 'defensive', attackOnlyUnderThreat: true },
  fog: { enabled: true, newsAgencies: true },
  victory: { type: 'points', share: 0.6, coalitionShared: true, timeLimitDays: 60 },
  monetisation: { payToWin: false },              // never true: listed so no mode can quietly turn it on
};

export const MODES = {
  standard: { extends: 'base', id: 'standard' },
  world100: {
    extends: 'standard', id: 'world100', name: { en: 'Great War: 100 players', ar: 'الحرب الكبرى: ١٠٠ لاعب' },
    players: { max: 100, minToStart: 40 },
    countries: { playableMinKm2: 40000 },          // more seats: smaller countries become playable
  },
  nuclear: {
    extends: 'standard', id: 'nuclear', name: { en: 'Nuclear Round', ar: 'الجولة النووية' },
    units: { nuclear: true }, research: { levelCap: 6 }, victory: { timeLimitDays: 45 },
  },
  blitz: {
    extends: 'standard', id: 'blitz', name: { en: 'Blitz (4x speed)', ar: 'الحرب الخاطفة (سرعة ×٤)' },
    speed: 4, players: { max: 30, minToStart: 10 }, victory: { timeLimitDays: 20 },
  },
  mena: {
    extends: 'standard', id: 'mena', name: { en: 'Middle East', ar: 'الشرق الأوسط' },
    map: { region: ['gulf'] }, players: { max: 25, minToStart: 8 },
    countries: { playableMinKm2: 20000 },
  },
};

const isObj = (v) => v && typeof v === 'object' && !Array.isArray(v);
function merge(a, b) {
  const out = { ...a };
  for (const [k, v] of Object.entries(b || {})) out[k] = isObj(v) && isObj(a[k]) ? merge(a[k], v) : v;
  return out;
}

export function resolveMode(idOrObj, modes = MODES) {
  const seen = new Set();
  const chain = (m) => {
    if (typeof m === 'string') {
      if (m === 'base') return BASE;
      if (seen.has(m)) throw new Error('mode loop at ' + m);
      seen.add(m);
      if (!modes[m]) throw new Error('unknown mode ' + m);
      m = modes[m];
    }
    const parent = m.extends ? chain(m.extends) : BASE;
    const { extends: _, ...own } = m;
    return merge(parent, own);
  };
  const mode = chain(idOrObj);
  validateMode(mode);
  return mode;
}

export function validateMode(m) {
  const err = (msg) => { throw new Error(`mode ${m.id}: ${msg}`); };
  if (!(m.players.max >= 2 && m.players.max <= 200)) err('players.max must be 2..200');
  if (m.players.minToStart > m.players.max) err('minToStart above max');
  if (!(m.speed > 0 && m.speed <= 10)) err('speed must be 0..10');
  if (m.countries.neutralMaxKm2 >= m.countries.playableMinKm2) err('neutral line must be below the playable line');
  if (m.monetisation.payToWin) err('pay to win is never allowed');
  if (!m.name?.en || !m.name?.ar) err('needs an English and an Arabic name');
  return true;
}

// which role a country gets in this mode (playable / ai / neutral)
export function countryClass(mode, c) {
  const k = mode.countries;
  if (k.alwaysPlayable.includes(c.iso) || c.area_km2 >= k.playableMinKm2) return 'playable';
  return c.area_km2 < k.neutralMaxKm2 ? 'neutral' : 'ai';
}
