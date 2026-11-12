// Economy numbers: production, buildings, research. Per real hour unless noted (game day = 6 real hours).
// Output is multiplied by happiness output (P2) and ownership (E4).

export const RES = ['money', 'manpower', 'food', 'oil', 'steel', 'chips', 'rare'];

// City base output per real hour, by city size (capital, major, minor).
export const CITY_OUTPUT = {
  capital: { money: 300, manpower: 120, food: 150, oil: 50, steel: 80, chips: 40, rare: 15 },
  major: { money: 200, manpower: 80, food: 100, oil: 35, steel: 60, chips: 25, rare: 10 },
  minor: { money: 120, manpower: 50, food: 70, oil: 25, steel: 40, chips: 15, rare: 5 },
};

// Each province gives a little money and manpower plus one main resource from the real land under it
// (farmland -> food, oil fields -> oil, mines -> steel or rare metals, industrial belts -> chips).
export const PROVINCE_OUTPUT = { base: { money: 15, manpower: 6 }, main: { food: 30, oil: 35, steel: 25, chips: 12, rare: 8 } };

// City buildings. Cost of level 1; each next level costs x1.7 and takes the time in B4.
export const BUILDINGS = {
  factory: { cost: { money: 1500, steel: 500, chips: 100 }, effect: 'unlocks vehicles and launchers by level (units "needs"); each level -8% build time for factory units; +10% steel and chips from the city' },
  barracks: { cost: { money: 800, steel: 200 }, effect: 'unlocks infantry and towed guns; each level -8% build time for barracks units; +10% manpower from the city' },
  airport: { cost: { money: 1800, steel: 600, chips: 200 }, effect: 'unlocks aircraft by level; heals aircraft (H3); refuel -5% per level (A5); holds 4 squadrons per level' },
  port: { cost: { money: 1600, steel: 700, chips: 100 }, effect: 'unlocks ships by level; heals ships (H2); boarding; +10% money from trade per level' },
  hospital: { cost: { money: 1000, steel: 200, chips: 50 }, effect: 'levels 1-3: +1.5% healing per hour per level (H4); +3% happiness per level' },
  airDefence: { cost: { money: 1400, steel: 400, chips: 300 }, effect: 'protects the city (D11)' },
  bunker: { cost: { money: 1200, steel: 800 }, effect: 'cuts damage to units in the city 15% per level (B6)' },
};
export const PROVINCE_BUILDINGS = {
  smallAirfield: { cost: { money: 600, steel: 200 }, effect: 'helicopters and drones only; refuel like a level 1 airport' },
  fieldHospital: { cost: { money: 400, steel: 100 }, effect: '+1% healing per hour in the province' },
  miniPort: { cost: { money: 500, steel: 300 }, effect: 'boarding only (M9)' },
  road: { cost: { money: 300, steel: 150 }, effect: 'per line, more for long lines; +50% speed, +100% at level 2 (M11)' },
  radar: { cost: { money: 700, chips: 250 }, effect: '300 km radar (I2)' },
  outpost: { cost: { money: 300, steel: 100 }, effect: 'units here dig in at once; +20 km view' },
};
export const levelCost = (base, level) => Object.fromEntries(Object.entries(base).map(([r, v]) => [r, Math.round(v * 1.7 ** (level - 1) / 50) * 50]));

// Research: unlocking a unit (level 1) costs 1.2x the unit's money cost plus chips; each next level x1.35.
// Time: 3 h (level 1) rising to 12 h (top level).
export function researchCost(unit, level) {
  const m = unit.cost.money * 1.2 * 1.35 ** (level - 1);
  return { money: Math.round(m / 50) * 50, chips: Math.round((unit.cost.chips || 100) * 1.5 * 1.35 ** (level - 1) / 50) * 50, hours: [3, 4.5, 6.5, 9, 12][level - 1] };
}
