// Scenario 1: "The Iron Bridge". Hand-made map, 16 x 11 hexes.
// Terrain: . plain  f forest  h hill  m marsh  w river  B bridge  F ford  T town  v village
const TERRAIN = [
  '..ff....w..hh...',
  '.fff....w...hh..',
  '..f....w...f....',
  '......hw..ff....',
  '...h...w..f.....',
  '.v.....B..T.....',
  '....f...w.h.....',
  '...ff...w.f.....',
  '..mm....F..f....',
  '.mm......w.ff...',
  '.........w......',
];
// Main road runs along row 5 from the western depot to the eastern depot.
const ROAD_ROW = 5, ROAD_FROM = 0, ROAD_TO = 15;
// A dirt track leaves the road and runs down to the ford.
const TRACK = [[5, 6], [5, 7], [6, 8], [7, 8], [9, 8], [9, 7]];

export function makeScenario(seed = 1) {
  const h = TERRAIN.length, w = TERRAIN[0].length;
  const terrain = [], road = [];
  for (let r = 0; r < h; r++) for (let c = 0; c < w; c++) {
    terrain.push(TERRAIN[r][c]);
    road.push(r === ROAD_ROW && c >= ROAD_FROM && c <= ROAD_TO ? 1 : TRACK.some((t) => t[0] === c && t[1] === r) ? 2 : 0);
  }
  const unit = (id, side, type, c, r, str, extra = {}) => ({
    id, side, type, c, r, str, maxStr: str, morale: 80, stock: 6, dry: 0, dug: 0,
    order: { type: 'hold' }, prog: 0, broken: 0, alive: true, engaged: false, sigma: 1, ...extra,
  });
  return {
    tick: 0, startHour: 6, rng: seed >>> 0 || 1,
    map: { w, h, terrain, road },
    depots: { p: [0, 5], e: [15, 5] },
    objective: [10, 5],
    places: { town: [10, 5], bridge: [7, 5], ford: [8, 8], village: [1, 5] },
    units: [
      unit('p_inf1', 'p', 'inf', 5, 5, 100),
      unit('p_inf2', 'p', 'inf', 4, 4, 100),
      unit('p_arm', 'p', 'arm', 3, 5, 80),
      unit('p_art', 'p', 'art', 2, 5, 40),
      unit('e_guard', 'e', 'inf', 8, 5, 60, { dug: 30 }),
      unit('e_town', 'e', 'inf', 10, 5, 86, { dug: 30 }),
      unit('e_arm', 'e', 'arm', 11, 4, 66),
      unit('e_art', 'e', 'art', 11, 6, 40),
      unit('e_picket', 'e', 'inf', 10, 7, 30, { dug: 30 }),
    ],
    // What our intelligence believes at the start. conf: 'confirmed' | 'reported'.
    belief: {
      e_guard: { c: 8, r: 5, tick: 0, conf: 'confirmed', type: 'inf', str: 60 },
      e_town: { c: 10, r: 5, tick: 0, conf: 'confirmed', type: 'inf', str: 86 },
      e_art: { c: 11, r: 6, tick: -30, conf: 'reported', type: 'art', str: 40 },
      e_arm: { c: 11, r: 4, tick: -18, conf: 'reported', type: 'arm', str: 66 },
    },
    visible: {},
    battles: {}, battleLog: [], events: [], plan: null, cmd: null,
    stats: { pLost: 0, eLost: 0, pStart: 320 },
    result: null,
  };
}
