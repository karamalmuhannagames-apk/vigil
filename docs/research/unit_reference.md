# Unit reference numbers: real-world data and proposed game values

Compiled 12 Nov 2026 for the Vigil design. Part A gives real-world reference numbers for each unit type, with a source for each. Part B gives the rules used to turn them into game values. Part C gives the proposed game values for a 4x match (1 game day = 6 real hours).

**How to read the sources.** Every number links to a source (reference-style links; the URL list is at the bottom).
- **[v]** means the number was read from the source page while compiling this file.
- **[u]** means the page is the standard reference for that number, but it could not be fetched this session (af.mil, navy.mil and Wikipedia blocked or failed automated reads). The value is the widely published figure. Check it before treating it as final.
- "n/s" means no source gave a number. Any value shown there is a design estimate.

**Units.** km/h for real speeds. "Map km/h" means kilometres moved on the true-scale map per *real* hour of play at 4x. kn = knots (1 kn = 1.852 km/h). nm = nautical miles. "Real min" means real minutes of play.

---

## Part A — Real-world reference numbers

Each type uses one or two systems that represent it. Regional variants (Russian, Chinese and other equivalents) differ slightly but sit in the same band.

### A1. Ground manoeuvre units

| Unit type | Reference system | Speed (road / off-road) | Range | Fire / reload | Carried | Sensor / weapon reach | Source |
|---|---|---|---|---|---|---|---|
| Infantry, foot | US Army foot march doctrine | 4 km/h normal road pace; ~1.6 km/h cross-country; 32 km/day normal march, more than that is a forced march [v] | Day march 20–32 km [v] | — | — | n/s (eyesight, small arms ~0.5 km) | [march-rates], [fm7-10] |
| Infantry, motorized | JLTV / trucks | ~113 km/h top (70 mph) [u]; tow truck for an M777: 88 km/h road, 24 km/h cross-country [v] | ~480 km (300 mi) [u] | — | 4 troops (JLTV) [u] | n/s | [jltv], [m777-bae] |
| Infantry, mechanized (wheeled APC) | Stryker ICV | ~100 km/h road [v] | ~500 km (312 mi) [v] | — | 2 crew + 9 infantry [v] | MG / 40 mm GL | [stryker] |
| IFV | M2 Bradley | 66 km/h road; 7.2 km/h swimming [v] | 483 km [v] | — | 6 infantry + 3 crew; twin TOW launcher [v] | TOW reach 3.75 km [v] | [bradley] |
| Main battle tank | M1A2 Abrams | 68 km/h road [v]; ~48 km/h cross-country [u] | 425 km [v] | Loader-limited, several rounds a minute (n/s) | 120 mm gun | n/s (thermal sight, ×10 narrow field of view [v]) | [abrams], [abrams-wiki] |

### A2. Artillery, rockets and missiles

| Unit type | Reference system | Speed | Weapon range | Fire / reload | Tubes / load | Source |
|---|---|---|---|---|---|---|
| SP artillery | PzH 2000 | >60 km/h road; >420 km range [v] | 40 km base-bleed; up to 54 km with V-LAP [v] | 3 rounds in 10 s burst; up to 10 rounds/min [v] | 60 shells on board [v] | [pzh] |
| Towed artillery | M777 155 mm | Towed 88 km/h road / 24 km/h cross-country [v] | 24.7 km unassisted, >30 km assisted [v]; 24 / 30 km [v] | 4–5 rds/min rapid, 2 rds/min sustained [v]. **Emplace <3 min, displace 2–3 min** [v] (Ukrainian crews ~80 s [v]) | 1 gun | [m777-bae], [m777-au], [m777-ua] |
| MLRS (light, wheeled) | M142 HIMARS | 85 km/h road; 480 km range [v] | GMLRS 70–84 km, ER GMLRS ~150 km, ATACMS 300 km, PrSM >500 km [v] | Self-reload with its own crane [v] (time n/s; same pods as M270, see next row) | **1 pod: 6 GMLRS, or 1 ATACMS, or 2 PrSM** [v] | [himars] |
| MLRS (heavy, tracked) | M270 | 64 km/h road; 438 km operational range [v] | Same family; ATACMS 165–300 km [v] | **12 rockets in under 60 s; reload 4 min, 3 min on the M270A1** [v] | 2 pods × 6 = 12 [v] | [m270] |
| MLRS (legacy) | BM-21 Grad | 75 km/h road [v] | ~20 km [v] | 40 rockets in 20 s (spec table); **reload 5–10 min** (sources differ) [v] | 40 tubes [v] | [grad] |
| Ballistic missile, short range | 9K720 Iskander-M | TEL up to 70 km/h; 1,100 km road range [v] | ~500 km (9M723) [v] | **Ready ~16 min from the march, ~5 min if already stationary; both missiles within 1 min; reload ~16 min** [v]. Missile ~2.1–2.5 km/s [v] | **2 per TEL** [v]; reload vehicle carries 2 [v] | [iskander-csis], [iskander-rusi] |
| Ballistic missile, medium range | DF-21 (CSS-5) | Road-mobile TEL, "short launch time" [v] | Up to 2,150 km; DF-21D 1,450–1,550 km [v] | Reload n/s | 1 per TEL [u] | [df21] |
| Cruise missile launcher (land attack) | Typhon / Mid-Range Capability | Tractor-trailer; must stand upright to fire; Army calls it "a bit too large" [v] | Tomahawk Block IV/V: 1,600 km, high subsonic [v] | Reload n/s | **4 cells per launcher, 4 launchers per battery** [v]; fires Tomahawk and SM-6 [v] | [typhon], [tomahawk] |
| Cruise missile launcher (coastal) | K-300P Bastion-P | Mobile truck launcher [v] | Oniks 300 km [v] | n/s | **2 missiles per launcher**, 2 launchers per battery [v] | [bastion] |

### A3. Air defence

| Unit type | Reference system | Missile range / altitude | Radar / sensor | Reaction, salvo and reload | Missiles per launcher | Source |
|---|---|---|---|---|---|---|
| SAM, short range (MANPADS) | FIM-92 Stinger | 4.8 km, 3.8 km altitude [v] | IR seeker | Manual reload (time n/s) | 1 per tube | [stinger] |
| SAM, short range (vehicle) | Avenger | Stinger up to 8 km (as stated) [v] | FLIR | **8 missiles reloaded in under 3–4 min** [v]; vehicle 60 mph [v] | 8 in 2 pods [v] | [avenger] |
| SAM/gun, short range | Pantsir-S1 | Missile 1–12 km, alt 5–8 km (army-technology figures; later versions claim ~20 km); guns 4 km [v] | **Detects at ≥30 km, tracks at ≥24 km** [v] | **Reaction 5–6 s** [v]; reload n/s | 12 missiles [v] | [pantsir] |
| SAM, medium range | Buk-M2 | 3–50 km, 15 m–25 km altitude [v] | **9S18M1 search radar 160 km; launcher's own radar 120 km** [v] | **Reaction 10 s (system), 5 s (launcher); deploys in 5 min; reload from loader vehicle 13 min (15 min self-reload)** [v] | **4 per launcher**; loader carries 8 [v] | [buk] |
| SAM, long range | Patriot (PAC-2/PAC-3) | 40–160 km, 24 km altitude [v] | Radar ~100 km as stated by RFE/RL [v] (real figure higher; classified) | Missile ready in <9 s [v]. **Reload: crews have 1 hour; certified crew did it in 53 min** [v] | **M901: 4 PAC-2; M902: 16 PAC-3 CRI or 4 PAC-2; M903: 12 MSE, 16 CRI, 6 MSE + 8 CRI, or 4 PAC-2** [v] | [patriot-reload], [pac3], [patriot-rferl] |
| SAM, long range | S-400 Triumf | 48N6DM 250 km; 40N6 400 km (claimed); 9M96 up to 120 km [v] | **91N6E acquisition radar 600 km; tracks 300 targets, engages 36** [v] | **Deploys in 5 min** [v]. Reload ~50 min by the book, 25–30 min for good crews (secondary source) [v] | **4 heavy missiles per launcher, or up to 16 9M96** [v] | [s400], [s400-apa], [s400-reload] |
| Anti-air gun | Flakpanzer Gepard | 3.5 km (4.5 km with FAPDS ammo) [v] | Search and tracking radar 15 km [v] | 550 rds/min per barrel, 2 barrels [v] | 640 HE + 40 AP ready [v]; 65 km/h, 550 km range [v] | [gepard] |

### A4. Aircraft

| Unit type | Reference system | Speed | Radius / range | Turnaround / sortie rate | Load | Sensor | Source |
|---|---|---|---|---|---|---|---|
| Attack helicopter | AH-64 Apache | Cruise 265 km/h, max 293 km/h [v] | **Radius ~150 km on internal fuel, ~300 km with 1 external tank**; ferry 1,900 km; endurance 2.5 h [v] | **FARP refuel and rearm ~20 min** [v]; rearming alone 10–30 min [v] | Up to 16 Hellfire, effective past 8 km [v] | Longbow radar: classifies 128 targets, ready to attack in 30 s [v] | [apache], [farp-dvids], [farp-aam] |
| Transport helicopter | UH-60 Black Hawk; CH-47F Chinook | UH-60 cruise 282 km/h, max 294 km/h [v]; CH-47 cruise 160 kn (296 km/h) [v] | UH-60 range ~590 km [v] (so radius ~295 km) | n/s | UH-60: 11 troops [v]; CH-47: 33 troops, 26,000 lb sling load [v] | — | [uh60], [ch47] |
| Fighter | F-16C; Gripen | F-16 Mach 2 (1,500 mph at altitude) [v] | F-16 ferry >2,002 mi (3,220 km); air-to-surface mission >500 mi (860 km) out and back [v] | **Gripen air-to-air turnaround including fuel and weapons: under 10 min, 1 technician + 5 conscripts** [v] | — | n/s | [f16], [gripen] |
| Strike fighter | F-35A | Mach 1.6 [v] | **Combat radius >1,093 km (590 nm) on internal fuel; range >2,200 km** [v] | **Normal ("cold") turn ~3 h; "hot" refuel-and-rearm goal 90 min, possibly 25 min** [v] | 8,160 kg payload, 9 g [v] | n/s | [f35], [f35-ict] |
| Bomber | B-52H; B-2 | B-52 650 mph (1,046 km/h) [v]; B-2 high subsonic [v] | **B-52 range 8,800 mi (14,160 km)** [v]; **B-2 ~6,000 nm (9,600 km)** unrefuelled [v] | n/s (hours) | B-52: up to 20 cruise missiles (12 outside + 8 inside) [v]; B-2: ~60,000 lb [v] | — | [b52], [b2] |
| AWACS | E-3 Sentry | Cruise 360 mph (580 km/h) [v] | **More than 8 h unrefuelled** [v] | n/s | 4 flight crew + 13–19 mission crew [v] | **Radar >250 mi (~400 km) against low flyers, farther against high ones** [v] | [e3] |
| Tanker | KC-135 | 530 mph (853 km/h) [v] | **1,500 mi (2,419 km) with 150,000 lb of fuel to give away**; ferry 17,766 km [v] | n/s | Up to 200,000 lb fuel to give away [v] | — | [kc135] |
| Drone, recon (HALE) | RQ-4 Global Hawk | ~575 km/h (310 kn) [u] | Endurance 30+ h [u] | — | Sensors only | High-altitude radar and EO/IR [u] | [rq4] |
| Drone, armed MALE | MQ-9 Reaper; Bayraktar TB2 | MQ-9 cruise ~370 km/h [u]; TB2 70–120 kn (130–222 km/h) [v] | MQ-9 range 1,850 km (2,590 km ER) [v]; **TB2: 27 h endurance, datalink under 300 km** [v] | n/s | MQ-9: Hellfire, GBU-12/38/49/54 [v]; TB2: 4 smart munitions, 150 kg payload [v] | EO/IR (TB2 can carry an AESA radar instead) [v] | [mq9], [tb2] |
| Drone, loitering munition | Switchblade 600 | Cruise 104 km/h, dash 160 km/h [v] | **40+ km, 90 km with a relay; 40+ min loiter** [v] | **Set up in under 10 min from its tube** [v]; single use | 1 per tube | EO/IR | [sb600] |
| Drone, long-range one-way attack | Shahed-136 / Geran-2 | 185 km/h max [v] | ~2,500 km claimed [v] | Rocket-boosted launch [v] | ~40 kg warhead [v] | — | [shahed] |
| Drone, FPV | Ukrainian/Russian battlefield FPV | 60–100 km/h cruise, 100–150 km/h in the dive [v, low confidence] | **~20 km for battlefield FPVs; fibre-optic 10–20 km standard, claims of 42 km** [v]; radio link 5–15 km, 10–20 min of flight [v, low confidence] | Single use | ~2 kg payload (RPG-7/RKG-3 grenades); large types >7 kg [v] | Camera | [fpv-ctc], [fpv-uwa] |

### A5. Ships and submarines

| Unit type | Reference system | Speed | Range / endurance | Weapons / cells | Sensor | Source |
|---|---|---|---|---|---|---|
| Corvette | Karakurt (Project 22800) | 30 kn [v] | 2,500 nm, or 15 days [v] | Kalibr and Oniks cruise missiles [v] (8-cell launcher [u]); Pantsir-M close-in air defence [v] | n/s | [karakurt], [karakurt-wiki] |
| Frigate | FREMM (French Aquitaine class) | 27 kn max; cruise 15.6 kn [v] | 6,000 nm at 15 kn [v] | 16 Aster SAM cells + 16 MdCN cruise missile cells + 8 Exocet [v]; Aster 30 ~120 km [v] | Héraklès multifunction radar [v] | [fremm] |
| Destroyer | Arleigh Burke (DDG-51) | >30 kn [v] | n/s | **96 Mk 41 cells** [v]; Standard Missile, Tomahawk, ESSM, ASROC, 5-inch gun, 2 MH-60R helicopters [v] | **SPY-1D tracks >100 targets at >100 nm (185 km)** [v] | [ddg-navy], [ddg-sf] |
| Cruiser | Ticonderoga (CG-47); Kirov | Tico 32.5 kn [v]; Kirov 31 kn [v] | **Tico 6,000 nm at 20 kn, 3,300 nm at 30 kn** [v]; Kirov nuclear | **Tico 122 cells** [v]; Kirov 20 Granit + 96 S-300F SAM [v] | SPY-1A/B [v] | [cg-navy], [cg-sf], [kirov] |
| Aircraft carrier | Nimitz; Gerald R. Ford | 30+ kn [v] | Nuclear (decades) | Nimitz ~60+ aircraft, Ford 75+ [v] | Embarked E-2 AEW (n/s) | [cvn] |
| — carrier sortie rate | Nimitz / Ford | | | **Nimitz 120 sorties per 12-h flying day, 240 per 24-h surge; Ford 160 / 270** [v] | | [dote-cvn78] |
| Attack submarine | Virginia (SSN-774) | 25+ kn submerged [v] | Nuclear | **4 torpedo tubes; 12 VLS (early boats) or 2 × 6 payload tubes; VPM boats add 4 × 7 Tomahawk** [v] | n/s (passive sonar) | [ssn] |
| — heavy torpedo | Mk 48 ADCAP | ~40–55 kn [v] | **~50 km at 40 kn, ~39 km at 55 kn** [v] | 650 lb warhead [v] | Wire-guided plus own sonar | [mk48-fas], [mk48-navy] |
| Ballistic missile submarine | Ohio (SSBN) | 20+ kn [u] | Nuclear; patrols of months [u] | 20 Trident II D5 tubes (24 originally), 4 torpedo tubes [u]; D5 range >7,400 km [u] | n/s | [ssbn], [ohio-wiki] |
| Landing ship (dock) | San Antonio LPD-17 | >22 kn [v] | n/s | 650–800 troops; 2 LCAC or 1 LCU + 14 amphibious assault vehicles; helicopters or MV-22 [v] | — | [lpd] |
| Landing ship (assault) | Wasp LHD / America LHA | 20+ kn [v] | n/s | 1,687 troops + 184 surge; 3 LCAC or 2 LCU; helicopters, F-35B, MV-22 [v] | — | [lhd] |

### A6. What the real data says (takeaways for the design)

1. **Reloading the launcher is never the real limit.** HIMARS/M270 pods reload in 3–5 min, Grad in 5–10 min, Iskander in ~16 min, Buk in 13 min. What actually limits fire is the missile stock, the trip back to resupply, and the need to move away before counter-battery fire arrives. So long game cooldowns for missile launchers are realistic as a stand-in for logistics and counter-battery survival, even though the reload itself is fast.
2. **Heavy SAM reloads are the slow ones:** Patriot ~1 h, S-400 ~25–50 min. A big air-defence battery that has fired everything stays empty for a long time. This supports a "magazine" mechanic for air defence: a few engagements, then a long reload. Swarming an AD site with several strikes in a row then becomes the attacker's counter.
3. **Set-up time is real and short:** towed guns <3 min, Buk 5 min, S-400 5 min, Iskander 5 min from a halt. A "deploy before you can fire" delay is a cheap, realistic way to make shoot-and-scoot and ambushing moving columns matter.
4. **How fast aircraft turn around varies hugely by type:** Gripen <10 min (built for dispersed road bases), Apache at a FARP ~20 min, F-35 ~3 h cold or 25–90 min hot, bombers hours. The owner's 5 / 7 / 4 min values are therefore already a ~2–6x squeeze of the fast real cases. They are fine as game values.
5. **Carrier deck rate:** ~2 sorties per aircraft per 12-h day on a Nimitz (120 sorties / ~60 aircraft), and more on a Ford. A carrier should launch and recover slightly slower than a land base, not faster.
6. **Speed ratios to keep:** in real life a tank column (~35 km/h march), a jet (~850–900 km/h cruise), a helicopter (~260 km/h) and a ship transiting (~18–20 kn ≈ 35 km/h) are roughly 1 : 25 : 7.5 : 1. A playable game must squeeze the air end. Part B squeezes it to ~1 : 13 : 3.7 : 1.6 (ships get an ocean bonus, as in CoN, where ships move ~1.3–1.7x faster than tanks; see `con_mechanics.md`).
7. **FPV drones reach only 5–20 km.** On a world map that is inside one node. Model FPVs as a weapon carried by infantry or drone teams (an attack with a bonus against armour), not as a unit that flies across the map. Loitering munitions (40–90 km) are a short-range missile fired from a launcher. Shahed-type drones (2,000+ km) are a slow, cheap cruise missile.

---

## Part B — Conversion rules (real → game)

Time base: 4x, so 1 real hour of play = 4 game hours. A real 1-hour event takes 15 real minutes.

| Rule | Formula | Why |
|---|---|---|
| Ground movement | Game map km/h = **real sustained march speed × 4** (not top speed) | Truly 4x. Columns average ~35–45 km/h, not their top speed. |
| Foot infantry floor | 40 map km/h (real 4 km/h × 4 = 16 would be unplayable) | 16 map km/h means 9 real hours between two cities 150 km apart. 40 keeps foot troops the slowest, at ~1/3.5 of a tank. |
| Ships and submarines | **Real transit speed × 4 × 1.5** (ocean bonus) | CoN-like ratio: ships ~1.6x tanks. Oceans are large, and a carrier group crossing the Atlantic in ~25 real hours is about one game week. |
| Aircraft | **Real cruise speed × 2** (half the time compression) | Keeps jets ~13x faster than tanks without letting a fighter cross a continent between two combat ticks. |
| Missiles in flight | Ballistic: very fast (minutes); cruise missiles and one-way drones: real × 2 like aircraft | Leaves a window to intercept slow cruise missiles and drones. Ballistic missiles are fast and hard to stop, as in real life. |
| Terrain (link penalty) | Tracked ×0.7, wheeled ×0.5, foot ×0.6 on rough links (mountain, forest, urban); roads you build lift wheeled units most | Real ratios: Abrams 48/68 ≈ 0.7; truck towing an M777 24/88 ≈ 0.3 (softened to 0.5); foot 1.6/4 = 0.4 (softened to 0.6). |
| Reloads and logistics | ~real time ÷ 3, then set by balance; never compressed the full 4x | The full 4x would make reloads trivial (Patriot 15 min, Buk 3 min). Dividing by about 3 matches the owner's aircraft numbers (Gripen 10 → 5 min for fighters). |
| Deploy time | ~real set-up time, rounded to whole real minutes | Makes shoot-and-scoot and catching units on the move matter. |
| Weapon and sensor ranges | Real value where it fits a world map; capped where it would cover a whole region | S-400 40N6 at 400 km would cover a mid-size country from one site, so it is capped (upgrade path to 250 km). |

---

## Part C — Proposed game values (4x, true-scale map)

Owner rules applied:
- Ground units, ships and submarines attack every **15 real min, 12 at max upgrade**.
- Air defence has a shorter cooldown, and upgrades shorten it further.
- Missile launchers have long cooldowns. Each tube has its own cooldown, and a launcher may fire several ready tubes in one order.
- Aircraft cycle = fly there + fly back + refuel/rearm. Refuel/rearm is 5 min for fighters, 7 min for larger planes and 4 min for helicopters.

### C1. Ground units

| Unit | Move (map km/h) | Rough-link factor | Attack cooldown (base → max) | Attack range | Deploy before firing | Vision (km) | Real anchor |
|---|---|---|---|---|---|---|---|
| Infantry, foot | 40 | 0.6 | 15 → 12 | Contact | — | 15 | 4 km/h march [march-rates] |
| Infantry, motorized | 180 | 0.5 | 15 → 12 | Contact | — | 20 | ~45 km/h convoy, trucks 88 km/h top |
| Infantry, mechanized (APC) | 170 | 0.5 | 15 → 12 | Contact | — | 20 | Stryker 100 km/h top |
| IFV | 150 | 0.7 | 15 → 12 | Contact (ATGM reach 4 km) | — | 25 | Bradley 66 km/h, TOW 3.75 km |
| Main battle tank | 140 | 0.7 | 15 → 12 | Contact | — | 25 | Abrams 68 km/h road |
| SP artillery | 140 | 0.7 | 15 → 12 | 40 km (50 at max) | 1 min | 20 | PzH 2000: 40 km, 54 km V-LAP |
| Towed artillery | 120 | 0.5 | 15 → 12 | 30 km (40 at max) | 3 min | 15 | M777: emplace <3 min, 24.7–30+ km |
| Drone team (FPV) | 180 | 0.5 | 15 → 12 | 15 km (bonus vs armour) | 1 min | 20 | FPV 5–20 km [fpv-ctc] |

### C2. Missile launchers (each tube cools down on its own)

| Unit | Move | Tubes | Cooldown per tube (base → max) | Range (base → max) | Deploy | Missile speed on map | Real anchor |
|---|---|---|---|---|---|---|---|
| MLRS | 160 | 2 pods | 30 → 22 min | 80 → 150 km | 1 min | Rocket, ~instant (<1 min) | M270: 2 pods, reload 3–4 min; GMLRS 70–84 km, ER 150 km |
| Ballistic missile, short range | 160 | 2 | 60 → 45 min | 500 km | 4 min | ~6,000 map km/h (500 km in ~5 min) | Iskander: 2 per TEL, 500 km, ~5 min from halt, salvo <1 min |
| Ballistic missile, medium range | 130 | 1 | 120 → 90 min | 1,800 → 2,150 km | 6 min | ~10,000 map km/h | DF-21 up to 2,150 km |
| Cruise missile launcher | 140 | 4 | 45 → 35 min | 1,600 km land attack (anti-ship variant: 2 tubes, 300 → 500 km) | 6 min (stands upright) | 1,800 map km/h (Tomahawk ~880 km/h × 2) | Typhon 4 cells; Tomahawk 1,600 km; Bastion 2 × 300 km |
| Loitering munition launcher | 180 | 4 | 20 → 15 min | 40 → 90 km (relay upgrade) | 2 min | 200 map km/h; loiters 10 min near the target | Switchblade 600: 40/90 km, 104 km/h, 40 min loiter |
| One-way attack drone launcher | 150 | 4 | 60 → 45 min | 2,000 km | 3 min | 370 map km/h (easy to intercept) | Shahed 185 km/h, ~2,500 km |

A launcher may fire any number of its ready tubes in one order (for example, both Iskander missiles together, as in reality <1 min apart). Each fired tube then starts its own cooldown. The UI shows one timer per tube.

### C3. Air defence (shorter cooldown; magazine plus reload)

| Unit | Move | Engagement cooldown (base → max) | Engagements before reload | Magazine reload (base → max) | Air range (base → max) | Radar (km) | Deploy | Real anchor |
|---|---|---|---|---|---|---|---|---|
| Anti-air gun | 150 | 3 → 2 min | 10 | 6 → 4 min | 5 km (point defence of its node) | 15 | — | Gepard: 3.5–4.5 km, radar 15 km, 640 rds |
| SAM, short range (Stinger/Avenger/Pantsir) | 170 | 5 → 3 min | 4 (2 missiles each) | 8 → 6 min | 20 km | 35 | 1 min | Avenger 8 missiles, reload <3–4 min; Pantsir 12 missiles, radar 30 km |
| SAM, medium range (Buk/NASAMS) | 140 | 6 → 4 min | 4 | 10 → 7 min | 50 km | 120 → 160 | 2 min | Buk 4 per launcher + loader 8, reload 13 min, 50 km, radar 160 km |
| SAM, long range (Patriot/S-400) | 110 | 8 → 5 min | 6 | 20 → 15 min | 150 → 250 km (vs ballistic missiles: 40 km) | 300 → 400 | 5 min | Patriot reload 53–60 min; S-400 deploys in 5 min, reload 25–50 min, 250 km (48N6DM), radar 600 km |

Every value here is under the 15-min ground cooldown, as the owner rule requires. The magazine gives attackers a counter: several strikes in a row empty a site, and its reload window is the time to hit it.

### C4. Aircraft (cycle = out + back + refuel/rearm)

| Unit | Speed (map km/h) | Strike radius (base → max) | Refuel/rearm | Weapons per sortie | Vision / radar (km) | Real anchor |
|---|---|---|---|---|---|---|
| Fighter | 1,800 | 800 → 1,000 km | 5 min (4 at max airbase, proposal) | Air-to-air, 1 strike | 80 | F-16 Mach 2; ~860 km out and back; Gripen turn <10 min |
| Strike fighter | 1,700 | 1,000 → 1,200 km | 5 min | 1 strike (heavy) | 80 | F-35A radius 1,093 km |
| Bomber | 1,400 | 3,500 → 4,500 km | 7 min | 1 heavy strike or a stand-off missile salvo | 50 | B-52 range 14,160 km; B-2 9,600 km |
| AWACS | 1,100 | Stays on station 60 min | 7 min | — | 400 (air), 250 (ground) | E-3 580 km/h, radar ~400 km, 8 h |
| Tanker | 1,600 | 2,400 km; extends friendly radius +30% inside its zone | 7 min | — | 30 | KC-135 853 km/h, 2,419 km with 150k lb to give away |
| Attack helicopter | 520 | 150 → 300 km | 4 min | 1 strike (Hellfire 8 km) | 30 | Apache 265 km/h, radius 150 / 300 km |
| Transport helicopter | 540 | 300 km (air assault) | 4 min | Carries 1 infantry unit | 20 | UH-60 282 km/h, range 590 km; CH-47 296 km/h |
| Drone, recon (HALE) | 1,100 | 5,000 km; 4 h on station | 7 min | — | 150 | RQ-4 575 km/h, 30+ h |
| Drone, armed (MALE) | 400 | 300 km (1,000 with a satellite-link upgrade); 2 h on station | 4 min (proposal) | 2 light strikes | 60 | TB2 27 h, link <300 km, 4 munitions; MQ-9 1,850 km |

**Worked cycle times** (out + back + refuel):

| Aircraft | Target distance | Flight | Refuel | Cycle |
|---|---|---|---|---|
| Fighter | 200 km | 13 min | 5 | **18 min** |
| Fighter | 500 km | 33 min | 5 | **38 min** |
| Strike fighter | 1,000 km | 71 min | 5 | **76 min** |
| Bomber | 3,000 km | 257 min | 7 | **~4.4 h** (most of a game day) |
| Attack helicopter | 50 km (from a FARP) | 12 min | 4 | **16 min** |
| Attack helicopter | 150 km | 35 min | 4 | **39 min** |
| Armed MALE drone | 150 km | 45 min | 4 | **49 min** (it usually loiters instead) |

So aircraft close to the front cycle at about the ground rhythm (15–20 min) but hit harder. Deep strikes take much longer. Forward bases and helicopter FARPs are worth building.

**Carrier rules (proposal).** The deck launches or recovers 1 air unit per real minute (2 per minute at max upgrade). Refuel/rearm on a carrier is +1 min over a land base (fighters 6, larger types 8). This matches the real data: Nimitz deck rate ~2 sorties per aircraft per 12 h, Ford ~+33%.

### C5. Ships and submarines

| Unit | Speed (map km/h) | Main attack cooldown | Missile tubes (cooldown each) | Strike range | Ship air defence | Vision / sonar (km) | Real anchor |
|---|---|---|---|---|---|---|---|
| Corvette | 200 | 15 → 12 | 2 × 60 min | 300 km anti-ship; 1,500 km land attack (Kalibr) | Short-range SAM 20 km, 5 → 3 min | 100 | Karakurt 30 kn, 2,500 nm, Kalibr/Oniks, Pantsir-M |
| Frigate | 210 | 15 → 12 | 2 × 60 min | 200 km anti-ship; 1,000 km land attack (MdCN) | Medium-range SAM 100 km, 6 → 4 min | 200 (sonar 50) | FREMM 27 kn, 16 Aster + 16 MdCN + 8 Exocet; Aster 30 120 km |
| Destroyer | 220 | 15 → 12 | 4 × 60 min | 1,600 km Tomahawk; 200 km anti-ship | Long-range SAM 150 km, 6 → 4 min, 8 engagements | 300 | Burke 30+ kn, 96 cells, SPY-1D >185 km |
| Cruiser | 220 | 15 → 12 | 6 × 60 min | 1,600 km; 550 km heavy anti-ship (Kirov variant) | Long-range SAM 150 km, 6 → 4 min, 10 engagements | 300 | Tico 32.5 kn, 122 cells; Kirov 20 Granit + 96 S-300F |
| Aircraft carrier | 220 | — (its air wing attacks) | — | Air wing radius | Point defence 10 km | 150 (+ its aircraft) | Nimitz/Ford 30+ kn, 60–75+ aircraft, 120–270 sorties a day |
| Attack submarine | 190 (submerged) | 15 → 12 (torpedo 40 km) | 2 × 60 min (land attack 1,600 km) | 40 km torpedo | — | Sonar 60 (n/s; estimate) | Virginia 25+ kn, 4 tubes, 12 VLS; Mk 48 ~50 km |
| Ballistic missile submarine | 150 | 15 → 12 (torpedo, self-defence) | 4 × 240 min, **only in nuclear modes** | 7,400+ km | — | Sonar 40 | Ohio 20 Trident II D5; D5 >7,400 km |
| Landing ship | 170 | 15 → 12 (gun / helicopters) | — | — | Short-range point defence | 60 | LPD >22 kn, 650–800 troops; LHD 20+ kn, 1,687 troops |

Torpedo speed on the map: ~400 map km/h (55 kn × 4), so a 40-km shot arrives in ~6 min. That is long enough for the target to show a "torpedo in the water" alert.

---

## Part D — Open points for the owner

1. **Foot infantry at 40 map km/h** breaks pure realism on purpose (real 4x would be 16). Alternative: drop foot infantry as a mobile unit and treat it as garrison or militia that rides trucks when ordered to move far.
2. **Long-range SAM range cap of 150 → 250 km.** The real S-400 claim is 400 km, but that would cover whole small countries (Jordan, Palestine, the Gulf states) from one site.
3. **SSBN missiles only in nuclear modes.** In the standard mode the SSBN is a slow, stealthy submarine with torpedoes, or it is removed.
4. **Ship missile "tubes" are salvos, not single cells.** A Burke's 96 cells become 4 salvo tubes with a 60-min cooldown each. Otherwise ships would outclass every missile launcher on land.
5. **Drones and refuel:** the owner rule lists fighters, larger planes and helicopters only. This file proposes 4 min for MALE drones and 7 min for HALE drones.
6. **Max-upgrade airbase reducing refuel by 1 min** (5 → 4, 7 → 6, 4 → 3) is a proposal. The owner only set the base values.
7. Numbers marked [u] (JLTV, RQ-4, MQ-9 speed, Ohio, Karakurt cell count, Abrams cross-country) should be checked by hand on the linked pages before final balance.

---

## Sources

[march-rates]: https://www.armyheritage.org/wp-content/uploads/ref-bibs/subjects/Marching/Marching%20Rates.pdf
[fm7-10]: https://www.globalsecurity.org/military/library/policy/army/fm/7-10/apph.htm
[jltv]: https://en.wikipedia.org/wiki/Joint_Light_Tactical_Vehicle
[stryker]: https://www.army-technology.com/projects/stryker/
[bradley]: https://www.army-technology.com/projects/bradley/
[abrams]: https://www.armyrecognition.com/military-products/army/main-battle-tanks/main-battle-tanks/m1a2-abrams-main-battle-tank
[abrams-wiki]: https://en.wikipedia.org/wiki/M1_Abrams
[pzh]: https://knds.com/products/systems/pzh-2000
[m777-bae]: https://www.baesystems.com/dam/jcr:460e123c-94b6-4bea-a619-eed32a8b87a7
[m777-au]: https://army.gov.au/equipment/artillery/m777-155mm-lightweight-towed-howitzer
[m777-ua]: https://en.defence-ua.com/news/m777_displacement_in_80_seconds_ukrainian_artillerymen_show_how_its_done-4070.html
[himars]: https://armyrecognition.com/military-products/army/artillery-vehicles-and-weapons/multiple-launch-rocket-systems/himars-m142-high-mobility-rocket-missile-launcher-data
[m270]: https://www.army-technology.com/projects/mlrs/
[grad]: https://man.fas.org/dod-101/sys/land/row/bm-21.htm
[iskander-csis]: https://missilethreat.csis.org/missile/ss-26-2/
[iskander-rusi]: https://rusi.org/explore-our-research/publications/commentary/iskander-m-and-iskander-k-technical-profile
[df21]: https://missilethreat.csis.org/missile/df-21/
[typhon]: https://www.everycrsreport.com/reports/IF12135.html
[tomahawk]: https://www.navy.mil/Resources/Fact-Files/Display-FactFiles/Article/2169229/tomahawk-cruise-missile/
[bastion]: https://www.army-technology.com/features/russias-coastal-defence-systems-supporting-limited-naval-capabilities/
[stinger]: https://missiledefenseadvocacy.org/defense-systems/fim-92-stinger/
[avenger]: https://www.army-technology.com/projects/avenger/
[pantsir]: https://www.army-technology.com/projects/pantsyr/
[buk]: https://en.missilery.info/node/1080
[patriot-reload]: https://www.afcent.af.mil/News/Article/218380/deployed-patriot-reload-crew-certifiably-ready
[pac3]: https://sustainability.lockheedmartin.com/content/dam/lockheed-martin/mfc/documents/pac-3/23-07402-IAMD-PAC-3-MSE-Overview-R2.pdf
[patriot-rferl]: https://www.rferl.org/a/32188849.html
[s400]: https://www.army-technology.com/projects/s-400-triumph-air-defence-missile-system/
[s400-apa]: https://ausairpower.net/APA-S-400-Triumf.html
[s400-reload]: https://www.wionews.com/photos/how-long-does-it-take-to-reload-an-s-400-launcher-1787906654977
[gepard]: https://www.weaponsystems.net/system/69-Gepard
[apache]: https://migflug.com/aircraft/ah-64-apache/
[farp-dvids]: https://dvidshub.net/news/222370/farp-operations-keep-apaches-flying-shooting
[farp-aam]: https://armyaviationmagazine.com/maximizing-farp-efficiency-in-large-scale-combat-operations/
[uh60]: https://migflug.com/aircraft/uh-60-black-hawk/
[ch47]: https://www.army.mil/article/137584/ch_47_chinook_helicopter
[f16]: https://www.shaw.af.mil/About-Us/Fact-Sheets/Display/Article/663884/f-16c-fighting-falcon/
[gripen]: https://www.saab.com/newsroom/stories/2018/july/gripens-smart-support-solution
[f35]: https://www.lockheedmartin.com/content/dam/lockheed-martin/aero/f35/documents/fg15-1280_001_f-35a_pc_final.pdf
[f35-ict]: https://www.airandspaceforces.com/maintainers-hot-ict-f-35/
[b52]: https://www.airandspaceforces.com/weapons/b-52/
[b2]: https://www.afgsc.af.mil/About/Fact-Sheets/Article/630717/b-2-spirit/
[e3]: https://www.tinker.af.mil/About-Tinker/Fact-Sheets/Display/Article/384781/e-3-sentry-awacs/
[kc135]: https://www.altus.af.mil/About-Us/Fact-Sheets/Display/Article/352094/kc-135-stratotanker
[rq4]: https://www.af.mil/About-Us/Fact-Sheets/Display/Article/104516/rq-4-global-hawk/
[mq9]: https://www.af.mil/About-Us/Fact-Sheets/Display/Article/104470/mq-9-reaper/
[tb2]: https://bayraktartech.az/en/page/bayraktar-tb2/
[sb600]: https://www.avinc.com/lms/switchblade-600
[shahed]: https://www.rferl.org/a/32091316.html
[fpv-ctc]: https://ctc.westpoint.edu/wp-content/uploads/2025/07/CTC-SENTINEL-072025_cover-article.pdf
[fpv-uwa]: https://ukraine-war-analytics.com/analysis/fpv-drone-war-ukraine.html
[karakurt]: https://www.bairdmaritime.com/amp/story/security/naval/naval-ships/vessel-review-burya-cruise-missile-capable-stealth-corvette-for-russian-navy
[karakurt-wiki]: https://en.wikipedia.org/wiki/Karakurt-class_corvette
[fremm]: https://seaforces.org/marint/French-Navy/Destroyer-Frigate/Aquitaine-FREMM-class.htm
[ddg-navy]: https://www.navy.mil/Resources/Fact-Files/Display-FactFiles/Article/2169871/destroyers-ddg-51/
[ddg-sf]: https://seaforces.org/usnships/ddg/Arleigh-Burke-class.htm
[cg-navy]: https://www.navy.mil/Resources/Fact-Files/Display-FactFiles/Article/2169861/cruisers-cg
[cg-sf]: https://www.seaforces.org/usnships/cg/Ticonderoga-class.htm
[kirov]: https://www.naval-technology.com/projects/kirov/
[cvn]: https://www.navy.mil/Resources/Fact-Files/Display-FactFiles/Article/2169795/aircraft-carriers-cvn/
[dote-cvn78]: https://www.dote.osd.mil/Portals/97/pub/reports/FY2011/navy/2011cvn78.pdf
[ssn]: https://www.navy.mil/Resources/Fact-Files/Display-FactFiles/Article/2169558/attack-submarines-ssn/
[mk48-fas]: https://man.fas.org/dod-101/sys/ship/weaps/mk-48.htm
[mk48-navy]: https://www.navy.mil/Resources/Fact-Files/Display-FactFiles/Article/2167907/mk-48-heavyweight-torpedo/
[ssbn]: https://www.navy.mil/Resources/Fact-Files/Display-FactFiles/Article/2169580/ballistic-missile-submarines-ssbn/
[ohio-wiki]: https://en.wikipedia.org/wiki/Ohio-class_submarine
[lpd]: https://www.navy.mil/Resources/Fact-Files/Display-FactFiles/Article/2222713/amphibious-transport-dock-lpd/
[lhd]: https://www.navy.mil/Resources/Fact-Files/Display-FactFiles/Article/2169814/amphibious-assault-ships-lhdlhar/
