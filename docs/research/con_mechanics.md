# Conflict of Nations (now "Supremacy: World War 3"): exact mechanics, with numbers

Compiled 12 Nov 2026 for the Vigil design. Every number links to its source (reference-style links; the URL list is at the bottom).
Read the "reliability" notes: the community wikis are partly years old, and the game has been rebalanced roughly monthly since 2025.

**Name change.** Since April 2025 the game is sold as "Supremacy: World War 3 (formerly Conflict of Nations: World War 3)". It is one game in the "Supremacy Franchise" with Supremacy 1914 and Call of War 1942, after Bytro and Dorado merged into Twin Harbour Interactive ([gamedev-franchise]). Official patch notes now appear under playsupremacy.com/news/world-war-3. The same engine runs Call of War (CoW). Where only CoW data exists, this file says so and marks it **(CoW, sister game)**.

**Source reliability.**
- Patch notes on playsupremacy.com (2025–2026) are official and current. They override older wiki values.
- conflictofnations.wiki.gg is the active community wiki; many pages were copied from the old Fandom wiki and last edited 2020–2023.
- conflictnations-wiki.pages.dev is a mirror of the old official wiki (wiki.conflictnations.com, linked from Bytro's help centre ([help-units])). Good for rules, weak on numbers.
- Reddit could not be read directly (the search tool returned almost no Reddit pages; one Reddit mirror gave the Feb 2025 patch notes). Steam discussions and reviews were used for player complaints instead.
- Gaps are listed in section 10.

---

## 1. Game speeds, day length, match length, victory

| Item | Value | Source |
|---|---|---|
| Speeds offered | 1x ("normal") and 4x. The flagship 2025 scenario World Divided Domination runs in 1x and 4x. No other speeds found for CoN. | [help-4x], [fractured], [wiki-beginner] |
| 1x day | 1 game day = 24 real hours. A "1 day" build takes 24 h. | [help-4x] |
| 4x day | Time runs 4× faster. A "1 day" build takes 6 real hours; a 12 h move takes 3 h. The UI still shows the 1x durations (players find this confusing). | [help-4x] |
| Hourly combat on 4x | Combat "every hour" at 1x (section 2) therefore means every 15 real minutes at 4x. This is the source of the common "units fire every 15 minutes" statement. Inferred from the two sources. | [wiki-combat-old], [help-4x] |
| Players per map | Up to 140 on the largest map (Steam page, 2026); up to 100 (old wiki); 72 on World Divided Domination; an older review said 26 max (outdated). | [steam], [wiki-beginner], [fractured], [mmoreviews] |
| Match length | "Several weeks to months" for standard scenarios (Bytro help). One player reports a win after 75 days. | [help-length], [steam-p2w] |
| Win check | A player wins if their VP are above the map threshold at the 0:00 day change. | [wiki-victory] |
| End otherwise | Game ends when VP target is reached or when "Retire" is chosen; Retire becomes available when 5 or fewer players are still active. | [wiki-rules] |
| VP per province | Every non-city province = 1 VP. City VP depends on population and buildings (one guide: city VP equals its population). | [wiki-vp], [touchtap] |
| Gold reward | Every active player gets Gold equal to their VP at game end, win or lose. A solo win on the WW3 map gives 1,850 Gold, matching the 1,850 VP threshold. | [wiki-victory], [steam-p2w] |
| Coalition win | Coalition needs more VP than a solo win; members' VP count together. Since Aug 2025 a coalition is recognised as winner when a member holds the majority of VP at retirement. | [wiki-coalition], [pn-2508] |

**VP thresholds by map** (wiki table; coalition sizes 1–5) ([wiki-victory]):

| Map | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Europe 1990 | 1,250 | 1,750 | 2,000 | – | – |
| Flashpoint Europe | 1,500 | 1,845 | 2,250 | – | – |
| World War 2020 | 1,750 | 2,853 | 4,183 | 5,355 | 6,003 |
| World War 3 | 1,850 | 2,960 | 4,255 | 5,365 | 5,920 |
| Middle East Crisis | 1,000 | – | – | – | – |
| Overkill | 2,300 | 3,450 | 5,060 | 6,440 | 7,130 |
| World Redux / 4x | 1,500 / 2,000 | 1,800 / 2,400 | 1,995 / 2,660 | – | – |
| Rising Tides | 5,475 | 6,225 | 7,275 | 8,150 | 8,600 |
| Z | 1,950 | 2,925 | 4,290 | 5,460 | 6,045 |
| Cyber Black | 3,200 | 5,800 | 7,200 | – | – |

Note the coalition multiplier is far below linear (WW3: 5 players need 3.2× a solo player, not 5×), so coalitions are strongly rewarded.

**Domination mode (World Divided Domination, Dec 2025)** ([fractured]): no conquest victory. Control Points (CPs) pay VP to the holder every 6 real hours, and the VP are permanent ([wiki-campaign]). Thresholds 3,000 / 6,000 / 9,000 VP for 1 / 2 / 3-player coalitions. CP types pay 60 (A), 20 (B, C, E) or 4 (D) VP per day. A, B, C, E start garrisoned by neutral "Enforcers" (2 Enforcers + 1 AFV/CRV/Corvette). Starting army per player: 1 Mountain Infantry + 1 Air Superiority Fighter + 1 Combat Recon Vehicle in the capital, 2 Motorized Infantry in each other city.

Other scenario VP rules ([wiki-campaign]): Rising Tides has 10 Strategic Sites worth 500 VP each and complexes worth 50 VP when a dome is charged (24 h to recharge, needs population 4). Overkill has 12 strategic sites (500 VP plus 500–1,000 resources each). Blood & Oil: refineries 100 VP, a canal gate gives 16,000 money to a sole owner.

---

## 2. Combat

### 2.1 Timing (attack cycles)

| Rule | Value | Source |
|---|---|---|
| Combat round | "Combat rounds are calculated every hour" (1x). | [wiki-combat-old] |
| First tick | Happens immediately when units meet; then repeats hourly. | [wiki-combat-old] |
| Meeting engagement (both moving) | Each side attacks with its offensive stats and is hit back once per tick. | [wiki-combat-old] |
| Attack vs entrenched defender | A stack entrenched on a province centre "is not performing offensive actions"; only the attacker conducts attack rounds, the defender only defends (returns defensive damage). One summary of the same page said the attacker strikes twice per tick; the verbatim text did not confirm "twice", so treat as unverified. | [wiki-combat-old] |
| After a stack dies | The attack timer drops to 1 minute so the next target is engaged quickly (fix Feb 2026, includes sea mines). | [pn-2602] |
| Timer display | Units have an attack timer / "attack progress bar" (Cruiser and Frigate bar fixed Aug 2026); anti-air has a separate reload timer display (May 2026). | [pn-2608], [pn-2605] |
| Peace during combat | If two nations make peace mid-combat, combat does not stop and war is declared again when the combat timer reaches 0. | [wiki-combat] |
| (CoW, sister game) | Standard round 60 min for all units; melee and ranged both fire once per 60 min; units always defend every time they are attacked; direct air strikes deal full damage per strike and can repeat more than once an hour if the base is close; patrols deal a share of damage every 15 min (25% under 1 h rounds, 50% once rounds became 30 min). Player answers, 2020. | [cow-reload], [cow-patrol] |

### 2.2 Damage model

- Each unit has an **attack and a defence strength rating against each armour class** (not a flat damage value). Ratings depend on attacking vs defending and on the target's armour class; research level raises them ([wiki-sbr], [wiki-units-old]).
- **Armour (HP) classes** ([wiki-armor], [wiki-hp]): Soft, Hard, Fixed Wing, Rotary Wing, Naval (surface), Submarine, Missile; plus Population and Building as non-unit HP classes. A newer "Drone" class exists: UAV HP type changed from Fixed Wing to Drone in Aug 2026 ([pn-2608]).
- **Final strength modifier** = terrain modifier × army boost (officers, season units) × doctrine boost × army stacking penalty × missing-health penalty ([wiki-strmod]).
- **Missing-health penalty** = 0.25 + 0.75 × (current HP / max HP). A unit at half health fights at 62.5% ([wiki-strmod]).
- Army strength and HP are the sum of the units in it ([wiki-army]).
- **Echelons** decide who takes damage: 1st echelon (front) takes the most, 2nd less, 3rd (rear) the least when stacked with others. No percentages published ([wiki-combat-old]). Lists: 1st ground = MBT, Tank Destroyer, Mech Inf, AFV, Mercenaries, Elite MBT, Elite Railgun; 2nd ground = ACV, Mobile Artillery, MRL, Naval/Airborne Inf, National Guard, Mobile AA, Tank Officer; 3rd ground = Motorized Inf, Mobile SAM, Towed Artillery, CRV, UGV, Mobile Radar, TDS, Special Forces, officers. 1st air = Air Superiority fighters, Gunship, Attack Helicopter; 1st sea = Destroyers; 3rd sea = Carrier, Ballistic sub, Elite sub, Elite Frigate ([wiki-combat-old]).
- **Overkill** (damage beyond what kills a target) was reduced about 25% in Feb 2025; devs warned some units would become much stronger ([pn-2502]).
- A teacher-wiki index lists community documents "Damage Distribution Weight" and "Full Damage Calculation", but the linked Google Docs could not be opened from this environment ([teacher]).

### 2.3 Example ratings (attack / defence)

| Unit (doctrine) | vs Soft | vs Hard | Def vs Air (fixed / rotary) | vs Building | vs Population | HP | Source |
|---|---|---|---|---|---|---|---|
| Motorized Inf L1 (East/EU) | 3.0 / 3.8 | 2.0 / 2.5 | 0.3 / 0.6 (1.0 / 1.3 with MANPADS) | 0.1 | 2.0 | 15 | [wiki-motinf] |
| Motorized Inf L7 | 6.5 / 8.1 | 4.5 / 5.6 | 1.6 / 1.9 | 0.2 | 2.0 | 24–25 | [wiki-motinf] |
| Mechanized Inf T1 (EU) | 4.0 / 5.0 | 5.0 / 6.3 | 1.3 / 1.9 | 0.1 | 2.0 | 22 | [wiki-mechinf] |
| Mechanized Inf T3 (EU) | 8.0 / 11.0 | 9.0 / 11.3 | 3.1 / 3.7 | 0.2 | 2.0 | 35 | [wiki-mechinf] |
| Airmobile Inf T1 / T3 (EU) | 5.0 / 3.3 → 9.0 / 6.0 | 3.0 / 2.0 → 5.0 / 3.3 | 0.3–1.0 / 0.7 | 0.1–0.2 | 2.0 | 15 → 20 | [wiki-airmob] |
| Special Forces T1 / T3 | 7 / 4.7 → 13 / 9 | 4.0 / 2.7 → 8 / 5.3 | 0.7–2.3 / 1.3–3.3 | 0.2 | 2.0 | 15 → 20 | [wiki-sf] |
| Main Battle Tank L1 (EU) | 9 / 9 | 8 / 8 | – / 1.0 | 0.3 (now 0.5) | 3.0 | 45 | [wiki-mbt], [pn-2606] |
| Main Battle Tank L7 (EU) | 13 / 13 | 13 / 13 | – / 2.0 | 0.4 (now 4.5) | 3.0 | 55 | [wiki-mbt], [pn-2606] |
| Heavy Bomber L1–L7 (Jun 2026) | 5.5 → 10 | 2.5 → 4.5 | – | – | – | 25 → 45 | [pn-2606] |
| Stealth Bomber (Jun 2026) | 11 | 6 | – | – | – | 40 | [pn-2606] |
| Mobile Radar | 0.5 vs any unit | | | | | | [wiki-inf] |

Pattern: defenders get about 25% more than attackers for infantry (3.0 atk / 3.8 def); tanks are symmetric; airborne and special forces are attack-heavy. Building damage of most land units is tiny (0.1–0.4) until the June 2026 change made tanks real building killers ([pn-2606]).

### 2.4 Ranges, sight and radar (map distance units, same scale for all)

| Item | Value | Source |
|---|---|---|
| Infantry sight | 25 → 40 since Aug 2026 (Motorized, Airborne, Mechanized, Marines); mountain sight bonus (was 35) removed | [pn-2608], [wiki-motinf] |
| MBT sight | 25 | [wiki-mbt] |
| Special Forces sight | 40 (50 in mountains); T1/T2/T3 now 40/50/60 | [wiki-sf], [pn-2512] |
| CRV sight | 40/50/60 by tier (Dec 2025) | [pn-2512] |
| Infantry attack range (T3 Motorized) | 20 | [wiki-motinf] |
| Towed Artillery range (final tier) | 75; fires only at stationary units | [wiki-towart], [wiki-towart-old] |
| Frigate ranged anti-air range | 150 | [wiki-frigate] |
| AWACS radar | 175/200/225/250/275/300 by level (Aug 2026) | [pn-2608] |
| Naval AWACS radar / combat range | 250/300 radar; combat range cut 1,500 → 1,000 (Oct 2025) | [pn-2608], [pn-2510] |
| Mobile Radar | 125/150/175/200/200/225/250 | [pn-2608] |
| Radar Station (building) | 100/125/175/200 | [pn-2608] |
| Coastal Battery T3 radar | 125 → 75 (Jun 2026) | [pn-2606] |
| UAV view / patrol circle | View 50–55; patrol circle 40/30/20/20/20/20 (was 50) | [pn-2602] |

Radar detects units by **signature type** (Ground, Fixed Wing, Rotary Wing, Naval) and **size** (HIGH or LOW). A radar that sees LOW also sees HIGH of that type. Units with no signature (infantry) are invisible to radar and must be seen ([wiki-fov], [levelwinner]). Stealth units are invisible within sight range and only revealed by matching "Reveal Stealth" units (ground/air/naval) or by combat ([wiki-fov]).

### 2.5 Terrain modifiers

Ten land/sea terrains: Open Ground, Mountains, Forest, Urban, Suburban (same as Urban), Jungle, Tundra, Desert, High Seas, Coastal Waters; plus "In Flight" (air units: higher HP/ATK/DEF) and "On the Ground" (lower) ([wiki-terrain]). Terrain changes attack, defence, speed, HP and sight per unit type ([wiki-combat-old]).

| Unit | Open | Mountain | Forest | Urban | Jungle | Tundra | Desert | Source |
|---|---|---|---|---|---|---|---|---|
| MBT atk/def % | +50 / +25 | −50 / −25 | 0 / 0 | −25 / −25 (L7: 0) | −50 / −25 | 0 | +25 / +25 | [wiki-mbt] |
| Mech Inf atk/def % | +50 / +25 | −50 / −25 | −25 / 0 | – | −50 / −25 | +25 / 0 | – | [wiki-mechinf] |
| Motorized Inf atk/def % | – | −25 atk | +25 def | +35 def (was +25) | −25 atk | −25 def | – | [wiki-motinf], [pn-2604] |
| Special Forces atk/def % | – | +50 / +25 | – | – | +50 / +25 | – | – | [wiki-sf] |
| National Guard def % | – | – | – | +25 (was +50) | – | – | +25 | [pn-2604] |

### 2.6 Stacking (army size)

| Rule | Value | Source |
|---|---|---|
| Max stack with no penalty | Land 10, Air 5, Sea 5 (wiki, Oct 2023) | [wiki-eff] |
| Conflicting official note | Patch 2509-10 fixed the army panel "stating a maximum size of 10 units instead of the actual limit of 5". Unit types not stated. Either land is now 5, or the fix concerned air/sea panels. **Unresolved.** One 2020 guide also says 10 for land. | [pn-2509], [levelwinner] |
| Combat penalty above limit | Effectiveness = 1 − 0.56 × ln(N / Nmax) (community-fitted; validated for air and sea up to 11 units, Oct 2023). Example: 15 land units → 0.77; 20 → 0.61. | [wiki-eff] |
| Speed penalty (naval, measured) | 5–10 ships: 100% ocean / 75% shallow; 11 ships: 85% / 50% | [wiki-eff] |
| Army speed | Speed of slowest unit | [wiki-army] |
| Officers | One active officer per type; buffs units of matching armour type in the same stack | [help-units], [wiki-strmod] |

### 2.7 Entrenchment, city and province defence

| Item | Value | Source |
|---|---|---|
| Entrenchment | Automatic when a stack sits on a province centre; lost when it moves. In cities it reduces damage taken by 25%. | [wiki-combat-old], [wiki-prov] |
| Combat Outpost (province) L1/L2/L3 | Unit damage −33/−50/−65%; with entrenchment −45/−57/−69%; morale +10/+13/+15%; HP 10/15/20 | [wiki-co] |
| Underground Bunkers (city) L1–L5 | Unit damage −33/−43/−56/−68/−73%; with entrenchment −45/−52/−61/−71/−75% (L5 entrenchment now 83%); morale +5/+10/+20/+35/+50%; HP 20/40/75/100/125 | [wiki-bunker], [pn-2606] |
| Bunker population shield | Was 2/4/6/8/10, now 5/6/8/10/10 (Jun 2026). Bunkers and Combat Outposts now also shield other buildings of the same level. | [pn-2606] |
| Stacking of reductions | Damage reductions stack "inversely additively" | [wiki-bunker] |
| Design note | Units are balanced toward defence; players entrench before logging off. | [wiki-beginner] |

### 2.8 Healing, retreat, morale in combat

- Healing per day: cities +1 base per unit, plus Military Hospital +1 to +5; provinces +0 base, Field Hospital +1/+2/+3; ships in coastal waters +2 (only out of combat); aircraft on a carrier in coastal waters 2 HP/day ([wiki-combat-old], [wiki-fh]). Healing updates hourly ([wiki-fh]).
- Retreat: only ground and naval units; costs HP, gives a big speed boost and makes the unit hard to hit (no numbers) ([wiki-combat-old]).
- Morale does not directly scale combat strength in the sources; it drives production, mobilization speed and revolts (section 6.3). Heavy bombers and WMDs damage morale ([help-units], [levelwinner]).

---

## 3. Air units

| Rule | Value | Source |
|---|---|---|
| Refuel at Air Base / Airfield | 15 min at full HP; time = 15 min / (base HP %). At the 40% minimum it is 37.5 min. | [wiki-refuel], [wiki-airbase] |
| Fuel timer | Starts when the plane leaves base; a patrol closer to base lasts longer. When it runs out the plane flies to its base automatically (unless current order needs it longer). | [wiki-fov], [wiki-refuel] |
| Fuel range examples | UAV "fuel range" 750/1500/3000 → 750/750/1500/1500/1500/3000 by level (Feb 2026) | [pn-2602] |
| Home base | Aircraft always refuel at their originating base. Sending them to a place with no airbase makes them land at the nearest airport and continue by truck ("ferrying"); a successful ferry makes the new airport the permanent base. | [wiki-fov] |
| Base destroyed | Airborne planes seek nearest airport or crash; planes parked there are "grounded" (speed 0, no orders) until the airport is rebuilt. Carrier sunk = same. | [wiki-fighters-old], [wiki-fov] |
| Patrol | Blue circle; hostile units entering it are attacked automatically. Strike fighters on patrol auto-attack any ground target they cross. Aircraft can no longer patrol outside the map (Jul 2026). | [wiki-fov], [wiki-sf-strike], [pn-2607] |
| Patrol damage cadence | Not published for CoN. (CoW: share of damage every 15 min.) | [cow-patrol] |
| Air Base | L1–L5 build 24/26/28/30/32 h; HP 10–30; operational at 40%; production +5…+25%; unlocks: L1 gunship, UAV, ASF; L2 airmobile, attack heli, strike fighter; L3 naval strike, naval patrol, heavy bomber; L4 AWACS; L5 stealth units | [wiki-airbase] |
| Airfield (province) | One level; 21 h; 700 supplies, 900 components, 800 fuel, 2,500 money; HP 10; works above 40% HP | [wiki-airfield] |
| Embark / disembark by air | Embark 30 min; disembark 1 h / (base HP %) (2.5 h at 40%) | [wiki-airbase] |
| Airlift | Free transport plane between friendly airbases/airfields; unit is defenceless while flying. Towed artillery airlift range 10,000, air assault 500 (map units). | [levelwinner], [wiki-towart] |
| Air assault | Unit moves by helicopter; if it attacks, the first combat tick is an air attack. Airmobile destination must be within range of a friendly airbase/airfield; carriers do not extend it. | [wiki-towart-old], [levelwinner], [wiki-airmob] |
| Missile loads | Strike fighter 1 cruise missile; heavy bomber 3 cruise missiles per 12 h; higher-tier UAV 1; cruiser and naval officer 2 | [wiki-sf-strike], [wiki-hb], [levelwinner] |
| Carrier | 5 naval aircraft; needs Naval Base L5 + Arms Industry L1 | [levelwinner], [wiki-carrier] |
| Stealth aircraft / UAV | Invisible to most radar; do not declare war when crossing foreign airspace | [wiki-fixed] |
| Helicopters vs planes | Helicopters fly low (nap-of-the-earth), cannot be targeted by SAMs or TDS radar; almost any other AA can hit them. Mobile SAM "does not engage low flying helicopters". Coastal battery lost its anti-helicopter value in Jun 2026. Helicopter refuel rules were not found. | [help-units], [wiki-gunship], [wiki-sam], [pn-2606] |
| Ground units vs air | Land units cannot attack aircraft in flight (no "attack plane" order for infantry); they only defend with AA values. | [levelwinner] |
| Anti-air modes | Point Defence: AA inside the target stack defends every time, no cooldown. AA Envelope: AA protecting a nearby unit goes on cooldown between defences. | [wiki-combat-old] |
| Missiles | Only cruise missiles can track units; ballistic and ICBM hit province centres only. Cruise and ballistic can be shot down by anything that can hit fixed-wing; ICBMs only by TDS. ICBM carries nuclear only. | [wiki-combat-old], [levelwinner] |

**Missile damage vs ships (Feb 2025 nerf)** ([pn-2502]): ICBM 400–475 → 175/200/225/300; ballistic nuclear 250–375 → 70–140; ballistic conventional 80–150 → 35–80; ballistic chemical 20–40 → 5–20. Splash radius: ICBM 50 → 25 (45 at top tier); ballistic conventional 10–15 → 5–15; cruise conventional 5–10 (top tier 20). Counter-missile values raised: TDS 12–17, frigate 2.5–8, carrier 3–7, cruiser up to 2.5.

---

## 4. Naval

| Rule | Value | Source |
|---|---|---|
| Sea movement | Sea zones joined by a network of lines with "≈" node marks (owner's screenshots). | internal: docs/research/con_map_study.md |
| Ports | Coastal cities spawn with a harbour that cannot be destroyed; pontoons give provinces a landing point (one per province). Naval units come from Naval Bases. | [wiki-city], [wiki-pontoon] |
| Naval Base L1–L5 | Build 24/9/30/32/34 h (as listed); HP 10–25; embark time −5/−10/−20/−40/−50%; production +5…+20%; operational at 40% HP | [wiki-navbase] |
| Naval Base unlocks | L2 naval inf, corvette, frigate; L3 destroyer, attack sub; L4 cruiser, ballistic sub; L5 carrier | [wiki-navbase] |
| Landing | Naval Infantry and Amphibious Combat Vehicles land on any coast; others need a port (anchor icon), pontoon or land border | [levelwinner], [wiki-inf-old] |
| Embarked land units | Become a Transport Ship: speed 2.51 on high seas, 1.30 coastal; HP drops to 12 for all land units | [wiki-motinf], [wiki-mbt] |
| Transport Boat (Marines/ACV, Aug 2026) | HP 12/15/20 by tier; coastal and river speed 1.3/2/3 | [pn-2608] |
| Rivers | Some maps have navigable rivers with river harbours; destroyers were banned from rivers in WDD (Mar 2026) | [pn-2603], [pn-2506] |
| Corvette | Half HP on high seas; "not recommended after the first week" | [wiki-corvette], [levelwinner] |
| Attack submarine | Half HP in shallow water (Submarine Commander exempt); sonar, stealth, reveal stealth; Eastern doctrine terrain penalty 25% → 15% | [levelwinner], [help-units], [pn-2604] |
| Fleets | Always identified when inside sight range (no "?") | [wiki-fov] |
| Naval healing | +2 HP/day in coastal waters, only out of combat | [wiki-combat-old] |
| Patrol Boat (Jun 2025) | New unit from a Level 1 harbour; radar at T2; final tier stealthy | [pn-2506] |

---

## 5. Movement

- **Model.** CoN units move between province centres; terrain of each province sets speed. The game uses pathfinding over a link graph (patch notes mention "a missing river link near Bucharest" and "units taking an unnecessarily long route to Vienna") ([pn-2603], [pn-2506]).
- **Speed values are unitless multipliers** shown per terrain; the wiki gives no km/h base ([wiki-motinf2]). A designer cited "a Main Battle Tank with 70 HP and 2.5 speed" as too strong, showing speed ~1–2.5 is the normal band ([doctrine]).

| Unit | Open | Mountain | Forest | Urban | Jungle | Tundra | Desert | High seas | Coastal | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| Motorized Inf L1 → L5+ | 1.00 → 1.50 | 0.33 → 0.49 | 0.66 → 0.99 | 0.50 → 0.75 | 0.33 → 0.49 | 0.66 → 0.99 | 1.00 → 1.50 | 2.51 | 1.30 | [wiki-motinf] |
| Mech Inf EU T1 → T3 | 1.10 → 1.40 | 0.36 → 0.46 | 0.73 → 0.92 | 0.55 → 0.70 | 0.36 → 0.46 | 0.73 → 0.92 | 1.10 → 1.40 | 2.51 | 1.30 | [wiki-mechinf] |
| MBT L1 → L7 | 1.30 → 1.50 | 0.43 → 0.49 | 0.86 → 0.99 | 0.65 → 0.75 | 0.43 → 0.49 | 0.86 → 0.99 | 1.30 → 1.50 | 2.51 | 2.51 | [wiki-mbt] |
| Special Forces T1 / T2 | 1.30 / 1.50 | 0.86 / 0.99 | – | – | 0.65 / 0.75 | 0.86 / 0.99 | 1.30 / 1.50 | 2.51 | 1.30 | [wiki-sf] |
| National Guard L1–L7 | 1.3/1.3/1.5/1.7/2.0/2.3/2.3 (Apr 2026); capped 0.35 in hostile provinces | | | | | | | | | [pn-2604] |

Ratios to copy or improve: mountains and jungle = 1/3 of open speed; forest and tundra = 2/3; cities = 1/2 ([wiki-motinf]).

| Movement rule | Value | Source |
|---|---|---|
| Foreign/hostile territory | Speed 66% (raised from 50% in Feb 2025); National Guard 25% | [pn-2502] |
| Roads / railways | No buildable roads or rails in CoN. The only infrastructure is **Military Logistics** (province, one level): +150% ground speed in that province, 3 h build, 250 supplies + 250 components + 250 fuel + 500 money, destroyed on conquest | [wiki-ml] |
| CRV in stack | Army speed +5/5/5/10/10/15/20% by level (Dec 2025) | [pn-2512] |
| Crossing water | Ground units embark to Transport Ship at ports/naval bases (or any coast for marines/ACV); embark time cut by naval base level | [wiki-navbase], [wiki-embark] |
| Exclusivity | A unit cannot embark by sea and by air at the same time | [wiki-embark] |
| Vehicles across a country | "Several hours" to cross a starting country | [touchtap] |

---

## 6. Economy

### 6.1 Resources

Supplies, Components, Fuel, Electronics, Rare Materials, Manpower, Money; plus premium Gold ([wiki-res]). Uses: supplies for most research/building and infantry; components for armour, ships, aircraft; fuel for upkeep of all units and for construction; electronics for buildings (not bunkers) and vehicle units; rare materials for strong units, all research and arms industries; manpower for every unit and for annexing. All but manpower, money and gold can be traded at the market for money ([wiki-res]). Since Feb 2025 armoured research costs components instead of supplies ([pn-2502]).

### 6.2 Production

| Rule | Value | Source |
|---|---|---|
| Production caps (after all bonuses) | Homeland city 100%; annexed city 50%; occupied city 25%; provinces 50% | [wiki-res], [wiki-prod] |
| Conquered provinces | Cash and manpower raised 25% → 33% (Feb 2025) | [pn-2502] |
| Provinces | Usually money and manpower; rare resources need a Local Industry to collect | [touchtap] |
| Local Industry (May 2026) | Supplies/components cost 400/450/500 (was 750/900/1000); build 12/21/30 h; bonus +50/100/200% | [pn-2605] |
| Arms Industry L1–L5 | Wiki: build 9/24/30/36/48 h. Feb 2026 patch then cut L2–5 cost by ~33% and raised L3–5 build time by ~20%. Production +10…+50%; flat money +100…+200; L1 unlocks everything except infantry, CRV, officers | [wiki-arms], [pn-2602] |
| Recruiting Office (Oct 2025) | Manpower +50/75/100/150/250% (was +5…+25%); flat +50/75/100/150/200 (was 200); mobilization speed +10/25/45/70/100%; build 30 min / 26 / 28 / 30 / 32 h | [pn-2510], [wiki-recruit] |
| Population levels (Oct 2025) | Manpower +30/75/100/150/165/180/190/200/225/250% for levels 1–10; L9 resource bonus 25%, L10 35%; growth time −15% | [pn-2510] |
| Military Hospital (Oct 2025) | Population growth +25/75/125/175/225% | [pn-2510] |
| Batch production (Jan 2026) | x20 (Arms L1), x30 saves 12.5% (Arms L3 + Secret Lab L1), x40 saves 25% (Arms L5 + Secret Lab L2) | [pn-2601] |
| Annex City | 18 h; 4,250 supplies, 3,750 components, 2,500 fuel, 1,500 rare, 1,750 electronics, 1,250 manpower, 10,000 money; raises city output 25% → 50% and allows mobilization | [wiki-annex] |
| Combat Outpost / Mercenary Outpost | Mobilization speed bonus moved into provinces; mercenary outpost +100% → +0/25/50% (Jul 2026) | [pn-2607] |
| Captured province | Ongoing construction and production stop on capture (May 2026); most buildings are destroyed on conquest | [pn-2605], [wiki-prov] |

### 6.3 Morale

| Rule | Value | Source |
|---|---|---|
| Production vs morale | Output = morale × 0.8 + 0.25. 25% → 45%; 70% → 81%; 90% → 97%; 100% → 105% | [wiki-morale] |
| Build/mobilization time | 100% time above 90% morale; 133% below 25%; in between 1 / (0.75 + 0.25 × (m − 25)/65) | [wiki-morale] |
| Start morale | 70% everywhere | [wiki-morale] |
| Target morale | Homeland city 90%, annexed/occupied city 60%, province 100% (another page says annexed target 75%) | [wiki-morale], [wiki-prov] |
| Revolt | Possible at ≤33% (City page says <35%); 50% chance at 25%; new occupied cities start at 25%, liberated homeland cities at 55%; provinces never revolt; troops lower the chance | [wiki-morale], [wiki-city] |
| Modifiers | War with x nations −2x (max −25); distance to HQ −5x; adjacent enemy provinces −5x; enemy units present −1; HQ lost −20 everywhere; resource shortage up to −50; civilian casualties up to −30, decays 1/3 per day; relocate HQ +25; neighbours at 100% +3 per city, +1 per province | [wiki-morale] |
| Update | Morale changes once per in-game day | [touchtap] |

### 6.4 Buildings (city vs province)

City: Army Base, Air Base, Naval Base, Recruiting Office, Arms Industry, Secret Weapons Lab (replaced by "Hospital" for pharmaceuticals in the loadout system), Military Hospital, Underground Bunkers, Annex City. Province: Combat Outpost, Airfield, Field Hospital, Local Industry, Pontoon, Military Logistics ([wiki-buildings], [loadout]). Building HP 10–30 for most; operational at 40% ([wiki-airbase], [wiki-prov]).

| Building | Levels | Build time per level | Key cost (L1) | Effect | Source |
|---|---|---|---|---|---|
| Army Base | 5 | 90 s / 28 / 32 / 34 / 36 h | 250 sup, 250 comp, 500 fuel, 250 elec, 2,000 money | L1 inf, CRV, mobile AA; L2 armour, mech/naval inf, towed art; L3 SF, mob art, SAM; L4 MRL; L5 TDS | [wiki-armybase] |
| Air Base | 5 | 24 / 26 / 28 / 30 / 32 h | 750 sup, 1,000 comp, 1,000 fuel, 500 elec, 2,750 money | see section 3 | [wiki-airbase] |
| Naval Base | 5 | 24 / 9 / 30 / 32 / 34 h | – | see section 4 | [wiki-navbase] |
| Arms Industry | 5 | 9 / 24 / 30 / 36 / 48 h | 400 sup, 350 comp, 225 rare, 350 fuel, 250 elec, 1,250 money | +10…+50% output | [wiki-arms] |
| Recruiting Office | 5 | 0.5 / 26 / 28 / 30 / 32 h | 250 each + 1,350 money | manpower, mobilization speed | [wiki-recruit] |
| Underground Bunkers | 5 | 9 / 12 / 16 / 26 / 36 h (Jun 2026), cost −20% | 500 sup, 750 comp, 750 fuel, 2,000 money (pre-cut) | damage reduction, morale, shields | [wiki-bunker], [pn-2606] |
| Combat Outpost | 3 | 1 / 4.5 / ? h | 500 sup, 750 comp, 2,000 money | damage reduction, morale | [wiki-co] |
| Field Hospital | 3 | 9 / 18 / 27 h | 750 sup, 750 comp, 1,250 money | +1/2/3 HP per day, morale +10/13/15% | [wiki-fh] |
| Airfield | 1 | 21 h | 700 sup, 900 comp, 800 fuel, 2,500 money | air ops from province | [wiki-airfield] |
| Military Logistics | 1 | 3 h | 250/250/250 + 500 money | +150% ground speed | [wiki-ml] |
| Local Industry | 3 | 12 / 21 / 30 h | 400 sup/comp | +50/100/200% | [pn-2605] |
| Upkeep | – | – | – | most buildings 100–140 money per day | [wiki-armybase], [wiki-bunker] |

### 6.5 Research

| Rule | Value | Source |
|---|---|---|
| Slots | 2 research slots | [touchtap] |
| First research | Motorized Infantry basic tier 1 min 30 s; several early items (Army Base L1, Recruiting Office L1, NG, ASF, Corvette, CRV research) ~30 min | [wiki-inf], [levelwinner] |
| Day gates | New research unlocks "almost every day"; real days gate tech | [wiki-research], [mmoreviews] |
| Doctrine first days (Jan 2026) | Mech Inf 1, Special Forces 4, SF Veteran 2, AFV 1, MBT 1, Tank Destroyer 1, Mobile Artillery 3, SAM 2, TDS 5, Gunship 1, Attack Heli 2, Strike Fighter 1, AWACS 5, Heavy Bomber 3 | [pn-2601] |
| Unit level gates (examples) | Motorized EU: L1 day 1, engine day 4, MANPADS day 7 (East day 6), advanced day 12, engine II day 16, modern day 22, armour day 26. Airmobile: day 1, 5, 11, 14 (T2), 17, 21, 25 (T3). Special Forces: day 5, 8, 15 (T2), 20, 27 (T3). Mech Inf EU: T2 day 11, T3 day 22. | [wiki-motinf], [wiki-airmob], [wiki-sf], [wiki-mechinf] |
| Tiers | T1 1980s–early 1990s, T2 2000s, T3 ultra-modern | [wiki-inf] |
| Research cost example | Air Superiority Fighter L4: 1,900 supplies, 1,900 rare, 4,000 money | [wiki-asf] |
| Doctrines | Western (highest HP, highest cost), European (middle), Eastern (lowest HP, cheapest); since Oct 2025 each unit's doctrine gives distinct perks (e.g. Attack Heli: West +20% hard dmg, EU +33% soft, East +50% ship) | [wiki-doctrine], [pn-2601], [doctrine] |
| Veterans | Research requirement removed; unlocked by player rank (Dec 2025) | [pn-2512] |

### 6.6 Unit cost and time examples

| Unit | Cost (L1/T1) | Upkeep per day | Mobilization | Source |
|---|---|---|---|---|
| Motorized Inf | 650 sup, 350 comp, 850 manpower, 1,000 money | 50 sup, 25 mp, 25 fuel, 70 money | 18 h (L7 1 day) | [wiki-motinf] |
| Mechanized Inf | 500 sup, 950 comp, 1,000 mp, 1,750 money | 60–65 sup, 20–25 mp, 25–30 fuel, 80–85 money | 20 h → 25 h | [wiki-mechinf] |
| Special Forces | 1,100 comp, 1,000 mp, 500 elec, 1,750 money | 70 sup, 30 mp, 20 fuel, 90 money | 24 h → 28 h | [wiki-sf] |
| Airmobile Inf | 1,250 comp, 1,000 mp, 550 elec, 1,500 money | 65 sup, 45 mp, 50 fuel, 85 money | 23 h → 26 h | [wiki-airmob] |
| Mercenaries | 2,500/4,000/7,000 money, 1,150/1,400/1,700 mp | 175 → 425 money | quick | [pn-2604] |
| National Guard | no Army Base needed; HP scales with city morale | – | 8–10 h | [wiki-inf-old], [levelwinner] |

---

## 7. Unit list by category

Categories ([wiki-units-old], [wiki-inf]): Infantry (Motorized, Mechanized, Naval/Marines, Airmobile, Special Forces, National Guard, Mercenaries, Insurgents, Enforcers); Armoured (Combat Recon Vehicle, AFV, Amphibious Combat Vehicle, MBT, Tank Destroyer); Support (Towed Artillery, Mobile Artillery, MRL, Mobile AA, Mobile SAM, Theater Defense System, Mobile Radar); Helicopters (Gunship, Attack, ASW); Fighters (Air Superiority, Naval ASF, Stealth ASF, Strike, Naval Strike, Stealth Strike, UAV); Heavies (Naval Patrol, AWACS, Naval AWACS, Heavy Bomber, Stealth Bomber); Naval (Corvette, Frigate, Destroyer, Cruiser, Carrier, Patrol Boat); Submarines (Attack, Ballistic Missile); Missiles (cruise, ballistic, ICBM × conventional, chemical, nuclear warheads); Officers (one per type); Deployables (UGV, loitering munitions); season "Elite" units; Satellites.

Typical stat ranges from the sources:
- HP: infantry 15–35; tanks 45–55; bombers 25–45; land units at sea 12 ([wiki-motinf], [wiki-mechinf], [wiki-mbt], [pn-2606]).
- Attack vs own class: infantry 3–13, tanks 9–13, bombers 5.5–11 vs soft (section 2.3).
- Speed: 1.0–2.3 on open ground; 0.33–0.5 in mountains; 2.51 at sea.
- Levels: 7 levels in 3 tiers for most units.
- Mobilization: 18 h to 1 day 4 h at 1x.
- Deployables: Special Forces carry 1 UGV (reload 18/12/6 h by tier) and 1 loitering munition (12/8/6 h) ([wiki-sf]).

---

## 8. Diplomacy, coalitions, spies, fog of war

| Rule | Value | Source |
|---|---|---|
| Diplomatic states | Peace, Right of Way, Share Intel, War. No trade embargo. | [levelwinner] |
| Border crossing | At peace, units entering foreign land start a war, except stealth aircraft and UAVs (and since Jun 2026 L1–2 Special Forces Veterans do not) | [levelwinner], [wiki-fixed], [pn-2606] |
| Coalition size | 1–5; Flashpoint Europe and Cyber Black max 3; WW3 and Overkill max 5; many event maps 3 | [wiki-coalition], [wiki-campaign] |
| Coalition rules | Shared map (cannot be removed); members cannot attack each other; leaving takes 48 h (1x) or 96 h (4x); leader leaving disbands in 48 h | [wiki-coalition] |
| Share Intel / coalition sight | Owned provinces and those of coalition or intel partners give full sight | [wiki-fov] |
| Fog of war | Hostile armies in your territory are fully shown; elsewhere they appear as "?" until a scout unit or combat reveals them; fleets always identified in sight | [wiki-fov] |
| Spies | Recruit 10,000 money; max 3 per enemy city/province; missions once per day | [wiki-intel] |
| Spy salaries per day | Idle/Counter-ops 250; Intelligence 2,000; Corruption 4,000 (cuts output, embezzles, or −10% morale); Sabotage 4,000 (damages buildings, delays construction/mobilization) | [wiki-intel] |
| Spy failure | Caught spies may reveal employer; unpaid spies abroad defect | [wiki-intel] |
| Officers | Max one active per type | [help-units] |
| Chat | In-game chat added to the Modern Client in Nov 2026 | [pn-2611] |

---

## 9. Player complaints and what strong players exploit

### 9.1 Complaints (with evidence)

1. **Pay-to-win.** Gold speeds up construction, mobilization and research, so spenders take an early lead and snowball ([mmoreviews]). A Steam thread describes a spender buying back lost units and building airfields instantly, losing 80 units by day 17 and still pressing on ([steam-p2w]). Counter-view: skilled players claim they beat €500–1,000 spenders ([steam-p2w]).
2. **Players quit early.** "Most opponents leave by the end of week one" while a win took 75 days ([steam-p2w]). Bytro support is "not obliged" to replace inactive players ([wiki-rules]).
3. **Very slow pace.** Actions take hours; ships take real days to cross oceans ([mmoreviews]).
4. **Automated combat with little tactical choice**; outcome set by composition, strength and money ([mmoreviews]).
5. **Unequal starts**: location and neighbours decide much ([mmoreviews]).
6. **Joining takes a slot before you can see which nations are free** ([mmoreviews]).
7. **Confusing timers on 4x**: UI shows 1x durations ([help-4x]).
8. **Hidden or changing numbers.** Doctrine changes are missed by players, so devs promised to show them in unit descriptions ([doctrine]); a wrong stack-size text stayed in the UI until Sep 2025 ([pn-2509]).
9. **Meta is ranged and air, melee is weak.** Designers admit melee units "struggle against highly skilled, active players" and players feel forced into resource-heavy meta builds ([doctrine]).
10. **Constant rebalancing.** Monthly patches change core values (e.g. stack text, recruiting office +5% → +50%) ([pn-2510]).
11. Steam score: 72% positive of 3,196 reviews overall, but 52% of recent 40 (mixed) ([steam]).

### 9.2 What top players do (directly sourced unless marked "inferred")

- Entrench on province centres before logging off; defence is favoured ([wiki-beginner]); stack bunkers/outposts for up to 75–83% damage reduction ([wiki-bunker], [pn-2606]).
- Keep stacks at the no-penalty limit (10 land / 5 air / 5 sea) and split beyond it ([wiki-eff]).
- Use stealth planes and UAVs to scout or strike without triggering war ([wiki-fixed]).
- Strike airbases: planes on a destroyed base are grounded and planes in the air may crash; a base under 40% HP stops working and refuels slowly ([wiki-fighters-old], [wiki-refuel]). (In CoW, rocketing an airbase made patrolling planes return to refuel, reported as a bug ([cow-airbase]).)
- Artillery only hits stationary units, so moving targets are safe from it (inferred from [wiki-towart-old]).
- Ballistic missiles hit only province centres; units off-centre or moving avoid them; cruise missiles track units ([wiki-combat-old]).
- Saturate AA envelopes: an AA unit guarding neighbours has a cooldown, so several strikes in a row get through (inferred from [wiki-combat-old]).
- Join many games, spot heavy spenders, leave or form coalitions against them ([steam-p2w]).
- Coalitions need far fewer VP per member than solo (section 1), so most winners play in coalitions (inferred from [wiki-victory]).

### 9.3 Design takeaways for Vigil (our inference)

- Show exact countdowns in real time for both speeds; never show 1x times on a 4x map.
- Publish every modifier (stack penalty curve, echelon shares, terrain) in-game.
- Add a reason to stay: AI takeover of quitters with a handover to new players; shorter scenario lengths.
- Give melee units a role (e.g. only melee captures; debuffs from support) so the meta is not only artillery and air.
- Keep defence advantage but limit the "log off and entrench" wall with visible counters.

---

## 10. Gaps and contradictions

- **Stack limit**: wiki says land 10 / air 5 / sea 5; official patch 2509-10 says the limit is 5 (unit types unstated) ([wiki-eff], [pn-2509]).
- **Attacker strikes per tick vs entrenched defender**: one or two per hour; not confirmed.
- **Patrol damage frequency and share in CoN**: not published; CoW uses every 15 min at a reduced share ([cow-patrol]).
- **Aircraft speed and fuel timers** (fighters, bombers): only UAV fuel range found ([pn-2602]).
- **Naval unit stats** (destroyer, cruiser, carrier HP/damage) not found on any readable page.
- **Morale target for annexed cities**: 60% ([wiki-morale]) vs 75% ([wiki-prov]); revolt threshold 33% vs 35% ([wiki-city]).
- **Recruiting Office and bunker numbers** on the wiki predate Oct 2025 / Jun 2026 patches; the patch values above override them.
- **Damage formula** (exact way strength turns into HP loss and how damage is split across a stack) is in community Google Docs that could not be opened here ([teacher]).
- **Inactivity / AI takeover rules** for CoN were not found.

---

## Sources

[gamedev-franchise]: https://www.gamedeveloper.com/press-release/three-games-two-studios-one-franchise-over-90-million-players-combined-introducing-the-supremacy-franchise
[help-4x]: https://bytro.helpshift.com/hc/en/6-supremacy-ww3/faq/323-why-doesn-t-the-speed-change-on-4x-maps
[help-length]: https://bytro.helpshift.com/hc/en/6-supremacy-ww3/faq/110-how-long-does-my-game-round-last
[help-units]: https://bytro.helpshift.com/hc/en/6-supremacy-ww3/faq/106-what-can-you-tell-me-about-units
[steam]: https://store.steampowered.com/app/784950
[steam-p2w]: https://steamcommunity.com/app/784950/discussions/0/3488626756876088876
[mmoreviews]: https://mmoreviews.com/?p=54867
[levelwinner]: https://www.levelwinner.com/?p=37118
[touchtap]: https://www.touchtapplay.com/conflict-of-nations-ww3-beginners-guide-tips-tricks-to-starting-out/
[teacher]: https://docs.google.com/document/d/1YOf7EURzh4lNNwFTuPTIAd0wBkMMIEXSiTltJm8XTGM/mobilebasic
[fractured]: https://playsupremacy.com/en/news/world-war-3/fractured-domination
[doctrine]: https://playsupremacy.com/en/news/world-war-3/doctrine-overhaul
[loadout]: https://playsupremacy.com/en/news/ww3-loadout-system
[pn-2502]: https://red.ks32.dev/r/ConflictofNations
[pn-2506]: https://playsupremacy.com/en/news/ww3-patch-notes-2506-17
[pn-2508]: https://playsupremacy.com/en/news/world-war-3/patchnotes-250819
[pn-2509]: https://playsupremacy.com/en/news/PATCH-NOTES
[pn-2510]: https://playsupremacy.com/en/news/patch-notes-2510-07
[pn-2512]: https://playsupremacy.com/en/news/world-war-3/patchnotes-2512-10
[pn-2601]: https://playsupremacy.com/en/news/world-war-3/patchnotes-2601-21
[pn-2602]: https://playsupremacy.com/en/news/world-war-3/patchnotes-2602-18
[pn-2603]: https://playsupremacy.com/en/news/world-war-3/patchnotes-2603-11
[pn-2604]: https://playsupremacy.com/en/news/world-war-3/patchnotes-2604-23
[pn-2605]: https://www.playsupremacy.com/en/news/world-war-3/patchnotes-2605-20
[pn-2606]: https://playsupremacy.com/en/news/world-war-3/patchnotes-2606-17
[pn-2607]: https://playsupremacy.com/en/news/world-war-3/patchnotes-260708
[pn-2608]: https://www.playsupremacy.com/en/news/world-war-3/patchnotes-2608-19
[pn-2611]: https://www.playsupremacy.com/en/news/world-war-3/patchnotes-2611-11
[wiki-combat]: https://conflictofnations.wiki.gg/wiki/Combat
[wiki-armor]: https://conflictofnations.wiki.gg/wiki/Armor_Type
[wiki-hp]: https://conflictofnations.wiki.gg/wiki/HP_Class
[wiki-sbr]: https://conflictofnations.wiki.gg/wiki/Strength_Base_Rating
[wiki-strmod]: https://conflictofnations.wiki.gg/wiki/Strength_Modifiers
[wiki-eff]: https://conflictofnations.wiki.gg/wiki/Efficiency
[wiki-army]: https://conflictofnations.wiki.gg/wiki/Army
[wiki-terrain]: https://conflictofnations.wiki.gg/wiki/Terrain
[wiki-refuel]: https://conflictofnations.wiki.gg/wiki/Refueling
[wiki-fixed]: https://conflictofnations.wiki.gg/wiki/Fixed_Wing_Aircraft
[wiki-asf]: https://conflictofnations.wiki.gg/wiki/Air_Superiority_Fighter
[wiki-sf-strike]: https://conflictofnations.wiki.gg/wiki/Strike_Fighter
[wiki-hb]: https://conflictofnations.wiki.gg/wiki/Heavy_Bomber
[wiki-carrier]: https://conflictofnations.wiki.gg/wiki/Aircraft_Carrier
[wiki-gunship]: https://conflictofnations.wiki.gg/wiki/Helicopter_Gunship
[wiki-sam]: https://conflictofnations.wiki.gg/wiki/Mobile_SAM_Launcher
[wiki-corvette]: https://conflictofnations.wiki.gg/wiki/Corvette
[wiki-frigate]: https://conflictofnations.wiki.gg/wiki/Frigate
[wiki-towart]: https://conflictofnations.wiki.gg/wiki/Towed_Artillery
[wiki-inf]: https://conflictofnations.wiki.gg/wiki/Infantry
[wiki-motinf]: https://conflictofnations.wiki.gg/wiki/Motorized_Infantry
[wiki-motinf2]: https://conflictofnations.wiki.gg/wiki/Motorised_Infantry
[wiki-mechinf]: https://conflictofnations.wiki.gg/wiki/Mechanized_Infantry
[wiki-airmob]: https://conflictofnations.wiki.gg/wiki/Airmobile_Infantry
[wiki-sf]: https://conflictofnations.wiki.gg/wiki/Special_Forces
[wiki-mbt]: https://conflictofnations.wiki.gg/wiki/Main_Battle_Tank
[wiki-doctrine]: https://conflictofnations.wiki.gg/wiki/Doctrine
[wiki-res]: https://conflictofnations.wiki.gg/wiki/Resources
[wiki-morale]: https://conflictofnations.wiki.gg/wiki/Morale
[wiki-vp]: https://conflictofnations.wiki.gg/wiki/Victory_Points
[wiki-victory]: https://conflictofnations.wiki.gg/wiki/Victory
[wiki-city]: https://conflictofnations.wiki.gg/wiki/City
[wiki-coalition]: https://conflictofnations.wiki.gg/wiki/Coalition
[wiki-intel]: https://conflictofnations.wiki.gg/wiki/Intelligence
[wiki-buildings]: https://conflictofnations.wiki.gg/wiki/Buildings
[wiki-airbase]: https://conflictofnations.wiki.gg/wiki/Air_Base
[wiki-airfield]: https://conflictofnations.wiki.gg/wiki/Airfield
[wiki-armybase]: https://conflictofnations.wiki.gg/wiki/Army_Base
[wiki-navbase]: https://conflictofnations.wiki.gg/wiki/Naval_Base
[wiki-arms]: https://conflictofnations.wiki.gg/wiki/Arms_Industry
[wiki-recruit]: https://conflictofnations.wiki.gg/wiki/Recruiting_Office
[wiki-bunker]: https://conflictofnations.wiki.gg/wiki/Underground_Bunkers
[wiki-co]: https://conflictofnations.wiki.gg/wiki/Combat_Outpost
[wiki-fh]: https://conflictofnations.wiki.gg/wiki/Field_Hospital
[wiki-ml]: https://conflictofnations.wiki.gg/wiki/Military_Logistics
[wiki-pontoon]: https://conflictofnations.wiki.gg/wiki/Pontoon
[wiki-annex]: https://conflictofnations.wiki.gg/wiki/Annex_City
[wiki-embark]: https://conflictofnations.wiki.gg/wiki/Embarkation
[wiki-combat-old]: https://conflictnations-wiki.pages.dev/Combat.html
[wiki-units-old]: https://conflictnations-wiki.pages.dev/Units.html
[wiki-inf-old]: https://conflictnations-wiki.pages.dev/Infantry.html
[wiki-fighters-old]: https://conflictnations-wiki.pages.dev/Fighters.html
[wiki-towart-old]: https://conflictnations-wiki.pages.dev/Towed_Artillery.html
[wiki-fov]: https://conflictnations-wiki.pages.dev/Field_of_View.html
[wiki-prov]: https://conflictnations-wiki.pages.dev/Provinces.html
[wiki-prod]: https://conflictnations-wiki.pages.dev/Production.html
[wiki-research]: https://conflictnations-wiki.pages.dev/Research.html
[wiki-beginner]: https://conflictnations-wiki.pages.dev/Beginner_Intro.html
[wiki-campaign]: https://conflictnations-wiki.pages.dev/Campaign_Types.html
[wiki-rules]: https://conflictnations-wiki.pages.dev/Rules.html
[cow-reload]: https://www.playsupremacy.com/en/forums/call-of-war-1942/call-of-war-1942-questions-and-answers/how-many-reloading-time-does-it-take-for-each-unit-when-attacking-e72926ca
[cow-patrol]: https://www.playsupremacy.com/en/forums/call-of-war-1942/call-of-war-1942-questions-and-answers/how-does-patrolling-damage-work-82f0ca09
[cow-airbase]: https://www.playsupremacy.com/en/forums/call-of-war-1942/call-of-war-1942-bug-reports/critical-airforce-now-useless-planes-now-returning-to-refuel-when-airbase-rocketed-instead-of-carrying-on-patrol-aea9d565

Note on [pn-2502]: the February 2025 patch notes (2502-19) were read through a Reddit mirror of r/ConflictofNations, not the official site.
Note on [pn-2611]: the 11 Nov 2026 patch (2611-11, chat and Start/Queue buttons) is known only from its summary on the game page and news list; the patch page itself was not opened.
