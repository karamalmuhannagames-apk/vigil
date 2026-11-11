// Regional doctrines: small attack/defence flavour per unit branch, from docs/research/regional_doctrines.md.
// Values are percent. Every doctrine sums to zero, so no region is stronger overall; never a new ability.
// Modes can switch this off (mode.units.regionalStats = false).
const B = ['infantry', 'armour', 'artillery', 'airdef', 'air', 'navy', 'heli', 'drone', 'missile'];
const row = (...pairs) => Object.fromEntries(B.map((b, i) => [b, {atk: pairs[i][0], def: pairs[i][1]}]));

export const DOCTRINES = {
  mena:     {name: {en: 'Middle East & North Africa', ar: 'الشرق الأوسط وشمال أفريقيا'},
             mod: row([0, 0], [0, 0], [-5, 0], [10, 0], [0, 0], [-10, 0], [-5, 0], [10, -5], [5, 0])},
  europe:   {name: {en: 'Europe', ar: 'أوروبا'},
             mod: row([5, 0], [5, 5], [-5, -5], [-5, -5], [5, 0], [5, 5], [0, 0], [-5, 0], [-5, 0])},
  eurasia:  {name: {en: 'Eurasia', ar: 'أوراسيا'},
             mod: row([0, -5], [0, -5], [10, 0], [5, 5], [-10, 0], [-5, -5], [5, -5], [5, 0], [5, 0])},
  asia:     {name: {en: 'Asia', ar: 'آسيا'},
             mod: row([0, 5], [-5, 0], [5, 0], [0, 5], [-5, -5], [5, 0], [-5, -5], [0, 0], [5, 0])},
  americas: {name: {en: 'Americas & Oceania', ar: 'الأمريكتان وأوقيانوسيا'},
             mod: row([0, 0], [0, 5], [-5, 0], [-10, -5], [10, 5], [5, 5], [5, 0], [-5, 0], [-5, -5])},
  africa:   {name: {en: 'Africa', ar: 'أفريقيا'},
             mod: row([5, 0], [-5, 0], [5, 0], [0, 0], [-5, -5], [-5, 0], [5, 0], [5, 0], [0, 0])},
};

export const BRANCHES = B;

// damage multiplier for an attack, given attacker and defender doctrines and branches
export function doctrineFactor(atkDoc, atkBranch, defDoc, defBranch, enabled = true) {
  if (!enabled) return 1;
  const a = DOCTRINES[atkDoc]?.mod[atkBranch]?.atk || 0;
  const d = DOCTRINES[defDoc]?.mod[defBranch]?.def || 0;
  return (1 + a / 100) * (1 - d / 100);
}
