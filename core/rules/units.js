// Unit data: the single source of truth for the game and the rules doc (Game Rules: Every Detail).
// Kinds of target: soft, armoured, plane, helicopter, drone, missile, ship, sub, building, population.
// Values are level 1. Each upgrade level adds about 8% to attack, defence and health.
// Costs: money, manpower, steel, oil, chips, rare (rare metals). Build time in real minutes.
// Upkeep per game day (6 real hours) is derived in upkeep() below.

export const KINDS = ['soft', 'armoured', 'plane', 'helicopter', 'drone', 'missile', 'ship', 'sub', 'building', 'population'];

const k = (s) => Object.fromEntries(s.split(' ').filter(Boolean).map((p) => { const [a, b] = p.split('='); return [a, +b]; }));

// id, name, kind, health, speed (1-50 scale), attack, defence, cost, build minutes, needs (building and level)
export const UNITS = [
  { id: 'U1', name: 'Infantry', ar: 'مشاة', kind: 'soft', hp: 15, speed: 10, atk: k('soft=3 armoured=1.8 helicopter=0.4 building=0.2 population=2'), def: k('soft=3.6 armoured=2.6 helicopter=0.6'), l3: ['helicopter'], cost: k('money=600 manpower=500 steel=100'), min: 140, needs: 'barracks1' },
  { id: 'U2', name: 'Motorized infantry', ar: 'مشاة آلية', kind: 'soft', hp: 16, speed: 12, atk: k('soft=3 armoured=2.3 helicopter=0.4 building=0.1 population=2'), def: k('soft=3.8 armoured=2.9 helicopter=0.6'), l3: ['helicopter'], cost: k('money=700 manpower=500 steel=200 oil=100'), min: 180, needs: 'barracks1' },
  { id: 'U3', name: 'Mechanized infantry', ar: 'مشاة ميكانيكية', kind: 'armoured', hp: 22, speed: 11, atk: k('soft=4 armoured=3 helicopter=0.6 building=0.2 population=1.5'), def: k('soft=4 armoured=3.8 helicopter=0.8'), l3: ['helicopter'], cost: k('money=1000 manpower=600 steel=350 oil=150 chips=50'), min: 240, needs: 'barracks2' },
  { id: 'U4', name: 'Infantry fighting vehicle', ar: 'مركبة قتال مشاة', kind: 'armoured', hp: 24, speed: 10, atk: k('soft=5.5 armoured=3.5 helicopter=1.5 drone=0.5 building=0.3 population=1'), def: k('soft=4.5 armoured=4 helicopter=1.5 drone=0.5'), cost: k('money=1200 manpower=400 steel=500 oil=200 chips=120'), min: 270, needs: 'factory1' },
  { id: 'U5', name: 'Main battle tank', ar: 'دبابة قتال رئيسية', kind: 'armoured', hp: 34, speed: 9, atk: k('soft=6 armoured=6 building=0.5 population=1'), def: k('soft=5 armoured=5.5'), cost: k('money=1600 manpower=400 steel=800 oil=300 chips=150 rare=30'), min: 330, needs: 'factory2' },
  { id: 'U6', name: 'Self-propelled artillery', ar: 'مدفعية ذاتية الحركة', kind: 'armoured', hp: 18, speed: 9, atk: k('soft=5 armoured=3 ship=1.5 building=1 population=2'), def: k('soft=1.2 armoured=1'), cost: k('money=1500 manpower=300 steel=600 oil=250 chips=150'), min: 300, needs: 'factory2', ranged: 45 },
  { id: 'U7', name: 'Towed artillery', ar: 'مدفعية مقطورة', kind: 'soft', hp: 14, speed: 8, atk: k('soft=4.5 armoured=2 ship=1 building=0.8 population=2'), def: k('soft=1 armoured=0.8'), cost: k('money=900 manpower=400 steel=300 oil=50 chips=50'), min: 210, needs: 'barracks1', ranged: 35 },
  { id: 'U8', name: 'Rocket artillery', ar: 'راجمة صواريخ', kind: 'armoured', hp: 16, speed: 10, atk: k('soft=8 armoured=5 ship=2 building=3 population=4'), def: k('soft=0.8 armoured=0.6'), cost: k('money=1700 manpower=300 steel=600 oil=250 chips=250 rare=20'), min: 330, needs: 'factory2', ranged: 115, salvoMin: 45 },
  { id: 'U9', name: 'Short-range ballistic launcher', ar: 'منصة صواريخ باليستية قصيرة المدى', kind: 'armoured', hp: 14, speed: 10, atk: k('soft=22 armoured=22 building=30 population=15'), def: k('soft=0.5 armoured=0.5'), cost: k('money=2400 manpower=300 steel=600 oil=300 chips=400 rare=80'), min: 420, needs: 'factory3', missile: 'srbm' },
  { id: 'U10', name: 'Medium-range ballistic launcher', ar: 'منصة صواريخ باليستية متوسطة المدى', kind: 'armoured', hp: 14, speed: 8, atk: k('soft=35 armoured=35 building=45 population=25'), def: k('soft=0.5 armoured=0.5'), cost: k('money=3200 manpower=300 steel=800 oil=400 chips=600 rare=150'), min: 510, needs: 'factory4', missile: 'mrbm' },
  { id: 'U11', name: 'Cruise missile launcher', ar: 'منصة صواريخ كروز', kind: 'armoured', hp: 14, speed: 9, atk: k('soft=18 armoured=18 ship=20 building=25 population=10'), def: k('soft=0.5 armoured=0.5'), cost: k('money=2600 manpower=300 steel=600 oil=300 chips=500 rare=100'), min: 420, needs: 'factory3', missile: 'cruise' },
  { id: 'U12', name: 'Loitering drone launcher', ar: 'منصة مسيّرات انتحارية', kind: 'armoured', hp: 14, speed: 12, atk: k('soft=8 armoured=8 ship=4 building=4 population=2'), def: k('soft=0.5 armoured=0.5'), cost: k('money=1600 manpower=200 steel=400 oil=200 chips=400 rare=40'), min: 300, needs: 'factory2', missile: 'loiter' },
  { id: 'U13', name: 'Anti-air gun', ar: 'مدفع مضاد للطائرات', kind: 'armoured', hp: 14, speed: 10, atk: k('soft=1 armoured=0.5 plane=2 helicopter=4 drone=3 missile=1'), def: k('soft=1 armoured=0.5 plane=2 helicopter=4 drone=3 missile=1'), cost: k('money=900 manpower=300 steel=300 oil=100 chips=100'), min: 210, needs: 'barracks1', aaShots: 1 },
  { id: 'U14', name: 'Short-range air defence', ar: 'دفاع جوي قصير المدى', kind: 'armoured', hp: 15, speed: 11, atk: k('plane=3.5 helicopter=4 drone=4 missile=2'), def: k('soft=0.5 armoured=0.5 plane=3.5 helicopter=4 drone=4 missile=2'), cost: k('money=1400 manpower=250 steel=400 oil=150 chips=300 rare=30'), min: 270, needs: 'factory1', aaShots: 2 },
  { id: 'U15', name: 'Medium-range air defence', ar: 'دفاع جوي متوسط المدى', kind: 'armoured', hp: 16, speed: 9, atk: k('plane=4.5 drone=3 missile=3'), def: k('soft=0.5 armoured=0.5 plane=4.5 drone=3 missile=3'), cost: k('money=2200 manpower=250 steel=500 oil=200 chips=500 rare=80'), min: 360, needs: 'factory3', aaShots: 3 },
  { id: 'U16', name: 'Long-range air defence', ar: 'دفاع جوي بعيد المدى', kind: 'armoured', hp: 16, speed: 7, atk: k('plane=5.5 drone=3 missile=4'), def: k('soft=0.5 armoured=0.5 plane=5.5 drone=3 missile=4'), cost: k('money=3000 manpower=300 steel=600 oil=250 chips=700 rare=150'), min: 480, needs: 'factory4', aaShots: 4 },
  { id: 'U17', name: 'Fighter', ar: 'مقاتلة', kind: 'plane', hp: 18, speed: 50, atk: k('soft=0.5 armoured=0.8 plane=5 helicopter=4 drone=3 ship=0.5 building=0.5'), def: k('plane=5 helicopter=2 drone=2'), cost: k('money=2600 manpower=150 steel=500 oil=500 chips=600 rare=120'), min: 420, needs: 'airport1' },
  { id: 'U18', name: 'Strike fighter', ar: 'مقاتلة هجومية', kind: 'plane', hp: 20, speed: 47, atk: k('soft=4 armoured=4.5 plane=2 helicopter=2 drone=1.5 ship=4 building=2.5 population=1'), def: k('plane=2.5 helicopter=1.5 drone=1.5'), cost: k('money=2800 manpower=150 steel=600 oil=550 chips=600 rare=120'), min: 450, needs: 'airport2', missile: 'air' },
  { id: 'U19', name: 'Bomber', ar: 'قاذفة', kind: 'plane', hp: 26, speed: 40, atk: k('soft=6 armoured=6 ship=5 building=7 population=4'), def: k('plane=1.5'), cost: k('money=3600 manpower=200 steel=900 oil=800 chips=700 rare=180'), min: 540, needs: 'airport3', missile: 'air' },
  { id: 'U20', name: 'AWACS', ar: 'طائرة إنذار مبكر', kind: 'plane', hp: 16, speed: 32, atk: {}, def: k('plane=0.5'), cost: k('money=2800 manpower=150 steel=500 oil=600 chips=900 rare=150'), min: 480, needs: 'airport3' },
  { id: 'U21', name: 'Tanker', ar: 'طائرة تزويد بالوقود', kind: 'plane', hp: 18, speed: 38, atk: {}, def: {}, cost: k('money=2000 manpower=150 steel=600 oil=800 chips=300 rare=50'), min: 420, needs: 'airport2' },
  { id: 'U22', name: 'Attack helicopter', ar: 'مروحية هجومية', kind: 'helicopter', hp: 16, speed: 30, atk: k('soft=4 armoured=5 helicopter=1.5 drone=1 ship=2 building=0.5 population=1'), def: k('soft=1.5 armoured=1.5 helicopter=1.5 drone=1'), cost: k('money=2000 manpower=150 steel=450 oil=350 chips=400 rare=60'), min: 360, needs: 'airport1' },
  { id: 'U23', name: 'Transport helicopter', ar: 'مروحية نقل', kind: 'helicopter', hp: 14, speed: 31, atk: {}, def: {}, cost: k('money=1300 manpower=150 steel=350 oil=300 chips=150 rare=20'), min: 270, needs: 'airport1' },
  { id: 'U24', name: 'Recon drone', ar: 'مسيّرة استطلاع', kind: 'drone', hp: 6, speed: 34, atk: {}, def: {}, cost: k('money=900 manpower=50 steel=150 oil=100 chips=350 rare=30'), min: 180, needs: 'airport1' },
  { id: 'U25', name: 'Armed drone', ar: 'مسيّرة مسلحة', kind: 'drone', hp: 8, speed: 29, atk: k('soft=3 armoured=3.5 ship=1.5 building=0.5 population=0.5'), def: {}, cost: k('money=1400 manpower=50 steel=250 oil=150 chips=450 rare=50'), min: 240, needs: 'airport1', missile: 'air' },
  { id: 'U26', name: 'Corvette', ar: 'كورفيت', kind: 'ship', hp: 22, speed: 26, atk: k('soft=1.5 armoured=1.5 plane=1 helicopter=1 drone=1 missile=0.5 ship=5 sub=3 building=0.5 population=1'), def: k('plane=1 helicopter=1 drone=1 missile=0.5 ship=5 sub=3'), cost: k('money=2000 manpower=300 steel=900 oil=300 chips=300 rare=30'), min: 330, needs: 'port1' },
  { id: 'U27', name: 'Frigate', ar: 'فرقاطة', kind: 'ship', hp: 30, speed: 26, atk: k('soft=2 armoured=2 plane=3.5 helicopter=2 drone=2.5 missile=2.5 ship=7 sub=5.5 building=1 population=2'), def: k('plane=3.5 helicopter=2 drone=2.5 missile=2.5 ship=7 sub=5.5'), cost: k('money=2600 manpower=400 steel=1200 oil=400 chips=500 rare=80'), min: 420, needs: 'port2' },
  { id: 'U28', name: 'Destroyer', ar: 'مدمرة', kind: 'ship', hp: 36, speed: 25, atk: k('soft=2 armoured=2 plane=2 helicopter=1.5 drone=1.5 missile=1.5 ship=9 sub=6.5 building=1 population=2'), def: k('plane=2 helicopter=1.5 drone=1.5 missile=1.5 ship=9 sub=6.5'), cost: k('money=3000 manpower=500 steel=1500 oil=500 chips=600 rare=100'), min: 480, needs: 'port3' },
  { id: 'U29', name: 'Cruiser', ar: 'طراد', kind: 'ship', hp: 46, speed: 25, atk: k('soft=2.5 armoured=2.5 plane=4.5 helicopter=2 drone=3 missile=3 ship=11 sub=7.5 building=1.5 population=2.5'), def: k('plane=4.5 helicopter=2 drone=3 missile=3 ship=11 sub=7.5'), cost: k('money=3600 manpower=600 steel=2000 oil=600 chips=800 rare=150'), min: 570, needs: 'port4' },
  { id: 'U30', name: 'Aircraft carrier', ar: 'حاملة طائرات', kind: 'ship', hp: 50, speed: 24, atk: {}, def: k('plane=2 helicopter=1 drone=1.5 missile=1 ship=3 sub=2'), cost: k('money=5000 manpower=800 steel=2800 oil=900 chips=900 rare=250'), min: 600, needs: 'port5' },
  { id: 'U31', name: 'Attack submarine', ar: 'غواصة هجومية', kind: 'sub', hp: 26, speed: 23, atk: k('ship=7.5 sub=5'), def: k('ship=7.5 sub=5'), cost: k('money=2700 manpower=300 steel=1200 oil=400 chips=600 rare=150'), min: 480, needs: 'port3' },
  { id: 'U32', name: 'Missile submarine', ar: 'غواصة صواريخ', kind: 'sub', hp: 30, speed: 20, atk: k('ship=5 sub=3.5'), def: k('ship=4 sub=3.5'), cost: k('money=3800 manpower=350 steel=1400 oil=500 chips=800 rare=200'), min: 570, needs: 'port4' },
  { id: 'U33', name: 'Landing ship', ar: 'سفينة إنزال', kind: 'ship', hp: 20, speed: 22, atk: {}, def: k('ship=0.5'), cost: k('money=1500 manpower=300 steel=800 oil=300 chips=150'), min: 300, needs: 'port1' },
];

// Cost of one reload (one missile or one salvo), paid when the tube refills.
export const MISSILE_COST = {
  salvo: k('money=100 steel=40'),
  loiter: k('money=150 chips=60'),
  air: k('money=150 chips=60 rare=10'),
  cruise: k('money=400 chips=150 rare=30'),
  srbm: k('money=500 steel=100 chips=150 rare=50'),
  mrbm: k('money=800 steel=150 chips=250 rare=100'),
};

// Upkeep per game day: money 5% of money cost, food 8% of manpower, oil 5% of oil cost (vehicles, planes, ships).
export function upkeep(u) {
  const c = u.cost;
  const r = { money: Math.round((c.money || 0) * 0.05), food: Math.round((c.manpower || 0) * 0.08) };
  if (c.oil) r.oil = Math.round(c.oil * 0.05);
  return r;
}

export const byId = Object.fromEntries(UNITS.map((u) => [u.id, u]));
