# Regional Doctrines: unit variants by world region

Research brief for regional unit variants: what real armed forces in each region are known for, a balanced modifier table, naming policy (real vs fictional names, with legal research), suggested names per region, and the "what this kind specializes in" text for unit cards (English + Arabic).

Status: proposal, November 2026. All numbers are starting values for playtesting, not final balance.

---

## 0. Summary

1. **Use six doctrines, not four.** The research supports splitting out **Eurasia** (Russia and the post-Soviet states) from Asia. It also supports giving **sub-Saharan Africa** its own doctrine instead of lumping it with the Americas: African forces fight very differently from the US-led Americas (light infantry, helicopters, imported Turkish/Chinese drones, small navies). Africa and Eurasia can share art with other regions at launch (see section 2) if the art budget is tight.
2. **Europe is not "the offensive doctrine."** The evidence says Europe's strengths are **quality** (tanks, fighters, warships, training) and its weaknesses are **depth**: ammunition, air-defence numbers, deep-strike missiles, drones ([IFRI via The Defense Post](https://thedefensepost.com/2025/11/04/europe-struggle-war-russia/), [IISS](https://www.iiss.org/globalassets/media-library---content--migration/files/publications---free-files/strategic-dossier/pds-2025/chapters/iiss_progress-and-shortfalls-in-europes-defence_2025_ch-3_integrated-air-and-missile-defence.pdf)). So the table below makes Europe exactly neutral overall: small plus on quality branches, small minus on depth branches.
3. **Modifiers are ±5% (sometimes ±10%) on attack or defence only.** No new abilities. Each region's 18 numbers add up to **exactly 0**. A second check, **weighted by how often each branch is used**, comes out between −1.0 and +2.0 for every region, so no region is stronger overall.
4. **Names: don't use real trademarks.** Use a generic class name ("Main Battle Tank") as the main label, plus a fictional nickname with a regional feel. A US court protected Call of Duty's realistic Humvees in 2020 ([Finnegan](https://www.finnegan.com/en/insights/blogs/incontestable/in-legal-warfare-over-humvee-trademarks-the-first-amendment-goes-beyond-the-call-of-duty-in-dismissing-am-generals-claims.html)). But the US Supreme Court narrowed that defence in 2023 ([Skadden](https://www.skadden.com/insights/publications/2023/06/supreme-court-sharply-limits-applicability)), and the real risk for a small studio is a Google Play takedown, not a court case ([Google Play IP policy](https://support.google.com/googleplay/android-developer/answer/9888072?hl=en)).
5. **Lesson from CoN and Call of War:** doctrine stat bonuses there caused years of "which doctrine is overpowered" arguments, and the developer had to nerf bonuses based on win-rate data ([Call of War forum](https://www.playsupremacy.com/en/forums/call-of-war-1942/call-of-war-1942-general-discussion/why-pan-asian-is-the-only-doctrine-without-a-built-in-solution-to-its-handicap-53448d27)). Keep our numbers small, show them openly on the unit card, and track win rate per doctrine from day one.

---

## 1. How other games did it (and what to avoid)

| Game | What doctrines do | Lesson |
|---|---|---|
| **Conflict of Nations** | Three doctrines (Western, Eastern, European). Western: highest hitpoints, highest research and build cost. Eastern: lowest hitpoints, cheapest. European: in between ([CoN wiki](https://conflictofnations.wiki.gg/wiki/Doctrine)). They also change which research comes early. Eastern gets MBTs, SAMs and gunships early. European gets mechanized infantry, tank destroyers and strike fighters. Western gets armoured combat vehicles, theatre defence, attack helicopters and AWACS ([CoN wiki mirror](https://conflictnations-wiki.pages.dev/Military_Doctrine.html)). | Doctrine = visual identity + small trade-off is a proven model players accept. CoN uses HP and cost; we use attack and defence, as the owner asked. |
| **Call of War 1942** | Axis +15% power and +15% HP but +10% cost. Comintern −15% cost and −25% upkeep but −10% power. Pan-Asian −10% HP but terrain and speed bonuses ([forum thread](https://www.playsupremacy.com/en/forums/call-of-war-1942/call-of-war-1942-general-discussion/why-pan-asian-is-the-only-doctrine-without-a-built-in-solution-to-its-handicap-53448d27)). | Players multiply bonuses (power × HP), so +15%/+15% really means about +32%. Pan-Asian's terrain bonus was nerfed from 25% to 20% after win-rate data. **Takeaway:** keep each modifier ≤10%, never stack attack and defence bonuses on the same branch without a matching minus elsewhere, and publish the numbers. |

---

## 2. Region definitions (doctrine ↔ art)

| Doctrine id | Art set | Countries (summary) | Why |
|---|---|---|---|
| `mena` | `gulf` | Arab League states (incl. Sudan, Somalia, Mauritania, Djibouti), Turkey, Iran | The game is Arabic-native, so this is the "home" art set. Turkey and Iran sit here because their drone and missile programmes define the region's military picture ([CSIS Missile Threat](https://missilethreat.csis.org/country/iran), [ESD](https://euro-sd.com/2025/07/articles/45450/key-programmes-bolster-turkiyes-defence-export-boom/)). Israel is not in the game, so no Merkava/Iron Dome lookalikes. |
| `europe` | `europe` | EU, UK, Norway, Switzerland, Western Balkans, **Ukraine**, Moldova, Georgia | Ukraine is post-Soviet, but its army is now largely Western-equipped (Leopard, Patriot, Western howitzers). Recommend `europe`, with a few Soviet-legacy art pieces as optional skins. |
| `eurasia` | `asia` at launch → own set later | Russia, Belarus, Kazakhstan, Central Asian states, Armenia, Azerbaijan, Mongolia | **Split supported by research.** Distinct doctrine: artillery-centred ("Russian forces manoeuvre to fire, Western forces fire to manoeuvre", [RUSI](https://rusi.org/explore-our-research/publications/commentary/russias-artillery-war-ukraine-challenges-and-innovations)), the world's densest air defence network ([RUSI via Euromaidan Press](https://euromaidanpress.com/2025/12/15/russias-air-defense-stops-90-of-ukraines-attacks-its-supply-chain-is-the-weak-link/)), weak air force and navy. Soviet-lineage equipment also *looks* different from Chinese, Korean or Indian kit (T-90 vs Type 99 vs K2), so it deserves its own art set once budget allows. |
| `asia` | `asia` | China, India, Pakistan, Japan, both Koreas, Taiwan (if present), Southeast Asia, Afghanistan, Bangladesh, Sri Lanka, Nepal | Region of missiles and growing navies ([Pentagon via Air & Space Forces](https://www.airandspaceforces.com/china-now-tops-us-in-shipbuilding-missiles-and-air-defense-dod-says/), [Lowy](https://www.lowyinstitute.org/the-interpreter/asia-escalating-missile-race)). |
| `americas` | `americas` | USA, Canada, Latin America, Caribbean, **Australia, New Zealand, Pacific islands** | Australia and New Zealand use US-pattern equipment (Abrams, F-35, Super Hornet, Black Hawk), so they fit this art and doctrine better than Asia's. Caveat: Latin America inherits a US-flavoured doctrine. That's acceptable at ±5–10%, but see option B below. |
| `africa` | `eurasia`/`asia` art at launch (Soviet/Chinese kit, desert/jungle paint) → own set later | Sub-Saharan Africa (minus Arab League members) | **Separate doctrine supported by research.** At least 31 African states have bought military drones, Turkey is the top supplier, and the TB2 is the most popular combat drone ([Africa Center](https://africacenter.org/spotlight/drone-proliferation-africa-destabilizing/)). Forces are light and infantry-centred, with small navies. Giving Africa the US carrier/air-power bonuses would be wrong. Their equipment is mostly Soviet/Chinese lineage (T-72, BM-21, Mi-24), so borrowing Eurasia/Asia art is visually honest. |

**Option B (if six doctrines feel like too much):** five doctrines, with Latin America moved from `americas` to `africa` under a shared "Global South / light forces" doctrine. Colombia runs the largest helicopter force in South America for counter-insurgency ([24/7 Wall St](https://247wallst.com/military/2024/10/11/colombias-helicopter-force-is-built-to-battle-guerrilla-forces/)). That matches the light/helicopter profile better than the US carrier profile. Not recommended for launch, because Latin American players may prefer to match the US art.

---

## 3. What each region is actually known for (research notes per branch)

Each note is the real-world basis for a modifier in section 4. **Evidence strength:** **S** = strong, multiple authoritative sources. **M** = moderate. **W** = weak or inference. Only S/M evidence earns a ±10.

### 3.1 MENA (`mena`)
- **Air defence (S):** Gulf states have built layered Patriot/THAAD defences and have combat experience intercepting large salvos. Qatar reported intercepting 98 of 101 ballistic missiles in one day, and the UAE reported more than 800 threats intercepted ([HSToday](https://www.hstoday.us/subject-matter-areas/counterterrorism/iran-war-and-the-impressive-transformation-of-arab-gulf-states-defense-capabilities/)). A possible US sale of 730 PAC-3 MSE interceptors to Saudi Arabia (~$9B) is in the same source.
- **Drones (S):** Baykar, citing a CNAS report, says Turkey holds about 65% of the global UAV export market, and the TB2/Akinci are in 35 countries ([ESD](https://euro-sd.com/2025/07/articles/45450/key-programmes-bolster-turkiyes-defence-export-boom/)). Iran's Shahed-131/136 were exported to Russia ([CSIS](https://missilethreat.csis.org/country/iran)). Drones are cheap and attritable, so: high attack, low durability.
- **Missiles (S):** Iran has "the largest and most diverse missile arsenal in the Middle East" ([CSIS](https://missilethreat.csis.org/country/iran)).
- **Armour (M):** Egypt fields at least 4,000 MBTs including about 1,200 co-produced M1A1s, the largest fleet in the region. Its doctrine is focused on "defending the borders" ([Carnegie](https://carnegieendowment.org/middle-east/research/2019/02/the-egyptian-military-a-slumbering-giant-awakes)). Big fleets are mostly about numbers, not quality per unit, so armour is left at 0.
- **Navy (M):** Carnegie calls Egypt's navy historically its weakest branch. Gulf navies are small and coastal → negative.
- **Helicopters / artillery (W):** no stand-out regional emphasis. A small negative pays for the strengths above.

### 3.2 Europe (`europe`)
- **Armour (S):** the Leopard 2 is used by about 18 countries ([GlobalSecurity](https://www.globalsecurity.org/military/world/europe/leopard2-users.htm)), alongside Leclerc and Challenger. Europe is known for well-protected, high-quality tanks.
- **Air force and navy (S):** IFRI judges Europe superior to Russia "in aerospace and at sea" ([The Defense Post](https://thedefensepost.com/2025/11/04/europe-struggle-war-russia/)). UK and French carriers and SSNs, plus strong air-defence frigates and destroyers.
- **Infantry (M):** small but professional, well-trained armies. 20 of 30 European NATO/EU members have professional ground forces under 15,000 troops (same source). That means quality per unit, not mass.
- **Artillery depth (S, negative):** "critical shortfalls in depth and ammunition stockpiles" (same source).
- **Air defence (S, negative):** Europe lacks adequate integrated air and missile defence "across nearly all threat types". Short-range and very-short-range stocks have gaps almost everywhere, and terminal missile defence depends on US Patriot ([IISS](https://www.iiss.org/globalassets/media-library---content--migration/files/publications---free-files/strategic-dossier/pds-2025/chapters/iiss_progress-and-shortfalls-in-europes-defence_2025_ch-3_integrated-air-and-missile-defence.pdf)).
- **Missiles / deep strike (M, negative):** Europe lacks "responsive deep-strike systems", and missile production is "vastly inferior" to what a war with Russia would need (IISS, IFRI).
- **Drones (M, negative):** Korean and Turkish suppliers fill European gaps ([Militarnyi](https://militarnyi.com/?p=438900)). Ukraine is the exception.

### 3.3 Eurasia (`eurasia`)
- **Artillery (S):** artillery is Russia's main source of lethality, and reports attribute about 70% of Ukrainian casualties to it ([RUSI](https://rusi.org/explore-our-research/publications/commentary/russias-artillery-war-ukraine-challenges-and-innovations)). This is the region's signature: +10 attack.
- **Air defence (S):** "the densest, most sophisticated and most integrated air defence networks in the world". The success rate of Ukrainian GMLRS strikes fell to about 8% in 2025 ([RUSI via Euromaidan Press](https://euromaidanpress.com/2025/12/15/russias-air-defense-stops-90-of-ukraines-attacks-its-supply-chain-is-the-weak-link/), advertorial page, RUSI data).
- **Missiles (S):** Russia moved to "mass precision" strike ([RUSI](https://www.rusi.org/explore-our-research/publications/research-papers/evolution-russias-precision-strike-adopting-mass-precision)).
- **Drones (S):** over 1.5 million UAVs produced in 2024, and Shahed/Geran output of up to 2,700 a month ([IISS](https://www.iiss.org/globalassets/media-library---content--migration/files/publications---free-files/strategic-dossier/pds-2025/chapters/iiss_progress-and-shortfalls-in-europes-defence_2025_ch-3_integrated-air-and-missile-defence.pdf)).
- **Helicopters (M):** in 2023 the Ka-52 was a major threat to Ukrainian armour, striking from about 10 km with laser-guided anti-tank missiles. But the UK MoD reported about 35 of Russia's 90 pre-war Ka-52s lost ([Forces News](https://www.forcesnews.com/technology/aircraft/ukrainian-tanks-face-increasing-threat-putins-vulture-attack-helicopter)). So: + attack, − defence.
- **Air force (S, negative):** Russia lost control of the skies over Ukraine within about nine days. Its pilots fly under 100 hours a year, and its air force was subordinated to ground commanders ([CSIS](https://www.csis.org/analysis/air-superiority-twenty-first-century-lessons-iran-and-ukraine)).
- **Navy (S, negative):** about 30% of the Black Sea Fleet was lost or damaged, largely to cheap sea drones ([National Security Journal](https://nationalsecurityjournal.org/circling-the-drain-russia-has-lost-30-of-its-black-sea-fleet/)).
- **Armour (M, negative defence):** heavy tank losses, a refurbished stored fleet that is less capable, and production of about 200–250 tanks a year ([ESD](https://euro-sd.com/?p=29595)). This mirrors CoN's "Eastern = lowest hitpoints".
- **Infantry (M, negative defence):** costly mass-assault tactics. Infantry is plentiful but fragile.

### 3.4 Asia (`asia`)
- **Navy (S):** the Pentagon calls China's navy "the largest in the world" (about 350 ships) ([Air & Space Forces](https://www.airandspaceforces.com/china-now-tops-us-in-shipbuilding-missiles-and-air-defense-dod-says/)). It has three carriers, with the Fujian commissioned in November 2025 ([War on the Rocks](https://warontherocks.com/2026/01/latest-pentagon-report-chinas-military-advancing-amid-churn/)). Japan and Korea field Aegis-type destroyers.
- **Missiles (S):** China has the largest land-based ballistic and cruise missile force, about 1,250 ground-launched missiles (2020 report, same source). Missiles are also being built up in India (BrahMos, Agni), North and South Korea (Hyunmoo) and Japan (stand-off missiles) ([Lowy](https://www.lowyinstitute.org/the-interpreter/asia-escalating-missile-race)).
- **Air defence (S):** China's air defence is "among the best in the world, if not the best… robust and redundant" (Air & Space Forces, above).
- **Artillery (S):** South Korea's K9 howitzer and Chunmoo rocket launcher are being bought across Europe, with Poland, Norway, Finland and Romania all buying K9s ([Militarnyi](https://militarnyi.com/?p=438900)). China fields modern PCH191 rocket artillery (War on the Rocks).
- **Infantry (M):** huge armies (China, India, both Koreas, Pakistan). Defensive mountain and jungle terrain dominates many borders.
- **Armour (M, negative attack):** much of the region is mountain, jungle and island terrain. China and India have even built new **light** tanks for high altitude (Type 15, Zorawar). Lighter armour means a smaller punch on average.
- **Air force and helicopters (M/W, negative):** limited recent high-end air-combat experience and smaller attack-helicopter arms. Strike emphasis goes to missiles instead of manned deep strike. This is a judgement call and should be watched in playtests.
- **Drones (M, neutral):** China is a major drone exporter and is testing launchers for 200-drone swarms ([CNA](https://www.cna.org/our-media/indepth/2025/09/china-readies-drone-swarms-for-future-war)), but the rest of the region varies a lot. Left at 0.

### 3.5 Americas (`americas`)
- **Air force (S):** the US way of war is built on air superiority. The Mitchell Institute calls it "a core condition that must once again be secured" ([Mitchell Institute](https://www.mitchellaerospacepower.org/app/uploads/2025/06/MI_Forum_57-Reclaiming-Air-Superiority-FINAL.pdf)). Stealth, AWACS and tankers add survivability, hence the defence bonus.
- **Navy (S):** 11 aircraft carriers, more than China, the UK, France, India, Spain and Italy combined ([19FortyFive](https://www.19fortyfive.com/2026/03/the-u-s-navy-has-the-most-aircraft-carriers-on-earth-and-thats-nowhere-near-enough/)).
- **Helicopters (M):** US Army aviation (Apache, Black Hawk) is a central part of US ground doctrine (general knowledge, no single source cited here). Colombia has the largest helicopter force in South America, 258 helicopters built for counter-insurgency ([24/7 Wall St](https://247wallst.com/military/2024/10/11/colombias-helicopter-force-is-built-to-battle-guerrilla-forces/)).
- **Armour (M):** Abrams crew survivability is a design priority → small defence bonus.
- **Air defence (S, negative):** the US Army divested most of its short-range air defence in the early 2000s, betting that the Air Force would always hold the sky. CRS says defence of manoeuvre forces against air threats "is currently limited" ([CRS](https://www.everycrsreport.com/files/2020-07-23_R46463_22bc5a0026e35a59ace3228b6cb05d1288936cb0.html)).
- **Artillery (M, negative):** "Western forces fire to manoeuvre". Artillery supports, while air power is the main fire ([RUSI](https://rusi.org/explore-our-research/publications/commentary/russias-artillery-war-ukraine-challenges-and-innovations)).
- **Missiles (M, negative):** in 2020 the US had only one ground-launched ballistic missile type with a range under 300 km and no ground-launched cruise missiles ([Air & Space Forces](https://www.airandspaceforces.com/china-now-tops-us-in-shipbuilding-missiles-and-air-defense-dod-says/)). This is being fixed now, so keep it small.
- **Drones (M, negative):** the Pentagon's Replicator programme exists to "counter the PLA's mass with mass of our own" ([USNI News](https://news.usni.org/2023/08/28/depsecdef-hicks-dod-wants-thousands-of-drones-to-counter-chinas-military-mass-advantage)), an admission of a mass-drone gap.

### 3.6 Africa (`africa`)
- **Infantry (M):** light-infantry, counter-insurgency forces. The Africa Center stresses that "drones cannot occupy or govern territory" and that ground forces still decide outcomes ([Africa Center](https://africacenter.org/spotlight/drone-proliferation-africa-destabilizing/)).
- **Drones (S):** 31+ countries have bought drones. There were 484 drone strikes in 2024, Turkey has 32 agreements on the continent, and the TB2 is the most popular combat drone (same source).
- **Helicopters (M):** helicopters (Mi-24/Mi-17 family) carry much of the mobility in large, road-poor countries. Inference, consistent with the light-force profile.
- **Artillery (W):** BM-21-type rocket artillery is everywhere. Small plus to balance.
- **Armour, air force, navy (M, negative):** older armour fleets, small fighter fleets, coastal navies.

---

## 4. Proposed modifier table

Format: **attack / defence**, in percent. "Attack" = damage dealt, "defence" = damage taken reduced. Empty = 0/0.

| Branch | MENA (`mena`) | Europe | Eurasia | Asia | Americas | Africa |
|---|---|---|---|---|---|---|
| Infantry | 0 / 0 | **+5** / 0 | 0 / **−5** | 0 / **+5** | 0 / 0 | **+5** / 0 |
| Armour | 0 / 0 | **+5 / +5** | 0 / **−5** | **−5** / 0 | 0 / **+5** | **−5** / 0 |
| Artillery & rockets | **−5** / 0 | **−5 / −5** | **+10** / 0 | **+5** / 0 | **−5** / 0 | **+5** / 0 |
| Air defence | **+10** / 0 | **−5 / −5** | **+5 / +5** | 0 / **+5** | **−10 / −5** | 0 / 0 |
| Air force | 0 / 0 | **+5** / 0 | **−10** / 0 | **−5 / −5** | **+10 / +5** | **−5 / −5** |
| Navy | **−10** / 0 | **+5 / +5** | **−5 / −5** | **+5** / 0 | **+5 / +5** | **−5** / 0 |
| Helicopters | **−5** / 0 | 0 / 0 | **+5 / −5** | **−5 / −5** | **+5** / 0 | **+5** / 0 |
| Drones | **+10 / −5** | **−5** / 0 | **+5** / 0 | 0 / 0 | **−5** / 0 | **+5** / 0 |
| Missiles | **+5** / 0 | **−5** / 0 | **+5** / 0 | **+5** / 0 | **−5 / −5** | 0 / 0 |
| **Sum attack** | +5 | 0 | +15 | 0 | −5 | +5 |
| **Sum defence** | −5 | 0 | −15 | 0 | +5 | −5 |
| **Raw total** | **0** | **0** | **0** | **0** | **0** | **0** |
| **Usage-weighted net** | +2.0 | +1.0 | +0.5 | 0.0 | −1.0 | +2.0 |

**Usage weights** (guesses for how much each branch decides matches): infantry 1.4, armour 1.3, artillery 1.2, air defence 1.0, air force 1.0, drones 0.9, helicopters 0.8, missiles 0.7, navy 0.6 (map-dependent). On this scale a ±2 net is roughly ±0.1% average strength. Replace the weights with real usage data after the first beta.

**Character of each doctrine (for the doctrine-select screen):**
- **MENA:** "Shield and swarm". Best air defence and drone strikes, strong missiles; weak at sea.
- **Europe:** "Quality over quantity". Superb tanks, jets and warships; thin artillery, air defence and missile stocks.
- **Eurasia:** "Fire and steel rain". Hardest-hitting artillery and dense air defence; fragile units and a weak air force and navy. (Attack-heavy, durability-light, like CoN's Eastern doctrine.)
- **Asia:** "Missiles and fleets". Growing navies, missiles, artillery and dug-in infantry; lighter armour and smaller helicopter arms.
- **Americas:** "Command of the air and sea". Best air force, carriers and helicopters; neglected short-range air defence, artillery and ground-launched missiles.
- **Africa:** "Light, fast, hard to pin down". Strong infantry, helicopters, drones and rocket artillery; small air force and navy.

### 4.1 One-line justifications (for designers and for an optional "Why?" tooltip)

| Region | Branch | Mod | Real-world basis | Source |
|---|---|---|---|---|
| MENA | Air defence | +10 atk | Combat-proven layered Patriot/THAAD; Qatar intercepted 98 of 101 ballistic missiles in one day | [HSToday](https://www.hstoday.us/subject-matter-areas/counterterrorism/iran-war-and-the-impressive-transformation-of-arab-gulf-states-defense-capabilities/) |
| MENA | Drones | +10 atk / −5 def | Turkey's TB2/Akinci and Iran's Shahed define global drone warfare; cheap, attritable airframes | [ESD](https://euro-sd.com/2025/07/articles/45450/key-programmes-bolster-turkiyes-defence-export-boom/), [CSIS](https://missilethreat.csis.org/country/iran) |
| MENA | Missiles | +5 atk | Iran has the largest, most diverse missile arsenal in the region | [CSIS](https://missilethreat.csis.org/country/iran) |
| MENA | Navy | −10 atk | Historically the weakest branch (Egypt); small coastal Gulf navies | [Carnegie](https://carnegieendowment.org/middle-east/research/2019/02/the-egyptian-military-a-slumbering-giant-awakes) |
| MENA | Helicopters, artillery | −5 atk | No regional emphasis; Gulf militaries invest in air power and air defence first | Inference from the sources above |
| Europe | Armour | +5 / +5 | Leopard 2 / Leclerc / Challenger: well-protected, accurate | [GlobalSecurity](https://www.globalsecurity.org/military/world/europe/leopard2-users.htm) |
| Europe | Air force | +5 atk | Superior to Russia in aerospace (Rafale, Typhoon, Gripen, F-35 users) | [IFRI via Defense Post](https://thedefensepost.com/2025/11/04/europe-struggle-war-russia/) |
| Europe | Navy | +5 / +5 | Superior at sea; carriers, SSNs, air-defence destroyers | same |
| Europe | Infantry | +5 atk | Small, professional, well-trained armies | same |
| Europe | Artillery | −5 / −5 | "Critical shortfalls in depth and ammunition stockpiles" | same |
| Europe | Air defence | −5 / −5 | IAMD inadequate across nearly all threat types; short-range gaps everywhere | [IISS](https://www.iiss.org/globalassets/media-library---content--migration/files/publications---free-files/strategic-dossier/pds-2025/chapters/iiss_progress-and-shortfalls-in-europes-defence_2025_ch-3_integrated-air-and-missile-defence.pdf) |
| Europe | Missiles, drones | −5 atk | Lacks responsive deep strike; buys Korean and Turkish to fill gaps | IISS; [Militarnyi](https://militarnyi.com/?p=438900) |
| Eurasia | Artillery | +10 atk | Artillery is the main source of lethality; ~70% of Ukrainian casualties | [RUSI](https://rusi.org/explore-our-research/publications/commentary/russias-artillery-war-ukraine-challenges-and-innovations) |
| Eurasia | Air defence | +5 / +5 | Densest integrated AD network in the world | [RUSI via EP](https://euromaidanpress.com/2025/12/15/russias-air-defense-stops-90-of-ukraines-attacks-its-supply-chain-is-the-weak-link/) |
| Eurasia | Missiles, drones | +5 atk | "Mass precision"; millions of drones a year | [RUSI](https://www.rusi.org/explore-our-research/publications/research-papers/evolution-russias-precision-strike-adopting-mass-precision), IISS |
| Eurasia | Helicopters | +5 / −5 | Ka-52 deadly in 2023, but ~35 of 90 lost | [Forces News](https://www.forcesnews.com/technology/aircraft/ukrainian-tanks-face-increasing-threat-putins-vulture-attack-helicopter) |
| Eurasia | Air force | −10 atk | Failed to win air superiority; <100 flight hours a year | [CSIS](https://www.csis.org/analysis/air-superiority-twenty-first-century-lessons-iran-and-ukraine) |
| Eurasia | Navy | −5 / −5 | ~30% of the Black Sea Fleet lost or damaged | [NSJ](https://nationalsecurityjournal.org/circling-the-drain-russia-has-lost-30-of-its-black-sea-fleet/) |
| Eurasia | Armour, infantry | −5 def | Heavy losses, refurbished older stock, mass-assault tactics | [ESD](https://euro-sd.com/?p=29595) |
| Asia | Navy | +5 atk | World's largest navy by ship count; Aegis fleets in Japan and Korea | [Air & Space Forces](https://www.airandspaceforces.com/china-now-tops-us-in-shipbuilding-missiles-and-air-defense-dod-says/) |
| Asia | Missiles | +5 atk | Largest land-based missile force; regional missile race | same; [Lowy](https://www.lowyinstitute.org/the-interpreter/asia-escalating-missile-race) |
| Asia | Artillery | +5 atk | K9/Chunmoo bought across Europe; PCH191 | [Militarnyi](https://militarnyi.com/?p=438900) |
| Asia | Air defence | +5 def | Chinese IADS "robust and redundant" | Air & Space Forces |
| Asia | Infantry | +5 def | Huge armies, mountain and jungle borders | Inference |
| Asia | Armour | −5 atk | Light tanks for mountains and jungle (Type 15, Zorawar) | Inference |
| Asia | Air force, helicopters | −5 / −5 | Less recent high-end air combat; strike role given to missiles | Inference (watch in testing) |
| Americas | Air force | +10 / +5 | Doctrine built on air superiority; stealth, AWACS, tankers | [Mitchell](https://www.mitchellaerospacepower.org/app/uploads/2025/06/MI_Forum_57-Reclaiming-Air-Superiority-FINAL.pdf) |
| Americas | Navy | +5 / +5 | 11 carriers | [19FortyFive](https://www.19fortyfive.com/2026/03/the-u-s-navy-has-the-most-aircraft-carriers-on-earth-and-thats-nowhere-near-enough/) |
| Americas | Helicopters | +5 atk | Helicopter-centred army aviation (US); largest helicopter force in South America (Colombia) | [24/7 Wall St](https://247wallst.com/military/2024/10/11/colombias-helicopter-force-is-built-to-battle-guerrilla-forces/) |
| Americas | Armour | +5 def | Crew survivability focus | Inference |
| Americas | Air defence | −10 / −5 | Short-range AD divested in the 2000s | [CRS](https://www.everycrsreport.com/files/2020-07-23_R46463_22bc5a0026e35a59ace3228b6cb05d1288936cb0.html) |
| Americas | Artillery | −5 atk | "Fire to manoeuvre"; air power is the main fire | RUSI |
| Americas | Missiles | −5 / −5 | Few ground-launched missiles until recently | Air & Space Forces |
| Americas | Drones | −5 atk | Replicator created to close the mass-drone gap | [USNI](https://news.usni.org/2023/08/28/depsecdef-hicks-dod-wants-thousands-of-drones-to-counter-chinas-military-mass-advantage) |
| Africa | Drones | +5 atk | TB2 most popular; 484 strikes in 2024 | [Africa Center](https://africacenter.org/spotlight/drone-proliferation-africa-destabilizing/) |
| Africa | Infantry, helicopters, artillery | +5 atk | Light, mobile, counter-insurgency forces; Grad-type rocket artillery everywhere | Africa Center + inference |
| Africa | Armour, navy | −5 atk | Older armour; coastal navies | Inference |
| Africa | Air force | −5 / −5 | Small fighter fleets | Inference |

### 4.2 Implementation rules
1. **Apply after the base stat and before terrain.** Never let doctrine + terrain + research add up to more than +25% on one stat. Clamp it.
2. **Show it plainly** on the unit card as a small chip: "Doctrine: +5% attack" / "العقيدة: +5% هجوم". Hidden bonuses breed conspiracy theories.
3. **Track win rate by doctrine × map** from the first beta. Bytro adjusted Pan-Asian after win-rate data, and we should plan to do the same. A doctrine >2 points above the average win rate over 1,000+ matches gets a 5% nudge.
4. **Doctrine follows the country**, not the player account. Players pick a country, so the doctrine comes for free. No extra decision for beginners.
5. **No doctrine changes research access.** CoN does that; it adds complexity the owner wants to avoid. Doctrine = art + small numbers only.

---

## 5. Unit naming: real names or fictional names?

### 5.1 What other games do

| Game | Approach |
|---|---|
| **Conflict of Nations** | Generic class names ("Main Battle Tank", "Attack Helicopter") with doctrine-specific art clearly based on real vehicles ([CoN wiki](https://conflictofnations.wiki.gg/wiki/Doctrine)). |
| **Call of Duty (recent titles)** | Fictional gun names (e.g. "Krig 6", "Kastov 762") to avoid licensing costs and manufacturer restrictions and to keep freedom to balance stats ([Kakuchopurei](https://www.kakuchopurei.com/?p=219136)). Real vehicle shapes are still used (hence the Humvee case). |
| **Battlefield / EA** | In 2013 EA stopped licensing guns but kept real guns, saying "A book doesn't pay for saying the word 'Colt'" ([Engadget](https://www.engadget.com/2013/05/08/ea-kills-licensing-deals-with-gun-makers-keeps-those-guns-in-ga/)). Bell/Textron then sued EA over helicopters in *Battlefield 3*. EA settled privately and the case was dismissed ([Engadget](https://www.engadget.com/2013/08/16/ea-settles-battlefield-3-and-textron-helicopter-lawsuit/)). Even a giant chose to pay rather than fight. |
| **War Thunder / Armored Warfare / World of Tanks** | Real vehicle designations (often generic military designations like "M1A2", "T-90A"). War Thunder players noticed some manufacturer names (BMW, General Electric) quietly removed from module names ([War Thunder forum](https://forum.warthunder.com/t/manufacturer-names-gone/337604)). That suggests brand names are riskier than military designations. |

### 5.2 Legal picture (not legal advice; get a lawyer's sign-off before launch)
- **AM General v. Activision (S.D.N.Y., March 31, 2020):** the court dismissed all of AM General's claims over Humvees in Call of Duty. Under the *Rogers* test, realistic military vehicles had "artistic relevance" in a modern-warfare game, and the use did not explicitly mislead, even though 16% of surveyed viewers showed some confusion ([Finnegan](https://www.finnegan.com/en/insights/blogs/incontestable/in-legal-warfare-over-humvee-trademarks-the-first-amendment-goes-beyond-the-call-of-duty-in-dismissing-am-generals-claims.html)).
- **Jack Daniel's v. VIP Products (US Supreme Court, 2023):** *Rogers* does **not** apply when a mark is used as a source identifier for your own goods. Early dismissal is now harder ([Skadden](https://www.skadden.com/insights/publications/2023/06/supreme-court-sharply-limits-applicability)). Naming a purchasable unit pack "Abrams Pack" or putting "Leopard" in store art could count as source-identifying use.
- **Outside the US**, there is no *Rogers* test. EU and Gulf trademark law is generally less protective of "artistic use".
- **The practical risk is Google Play.** Its policy: "We don't allow apps that infringe on others' trademarks… your app may be suspended", with a complaint form for rights holders ([Google Play](https://support.google.com/googleplay/android-developer/answer/9888072?hl=en)). One complaint can freeze a launch for weeks, whoever would win in court.

### 5.3 Recommendation
1. **Main label = generic class name**, localized: "Main Battle Tank" / "دبابة قتال رئيسية". This is what beginners need anyway.
2. **Second label = fictional nickname with a regional feel** (tables below), e.g. "Bastion" / "باستيون". Arab media really do transliterate foreign weapon names ("أبرامز", "ليوبارد"), so transliterated foreign nicknames feel native. MENA units get real Arabic words.
3. **Art = clearly inspired by real families, never an exact replica.** Mix features (a Leopard-style turret on a different hull, changed road wheels, our own camouflage and markings). No manufacturer logos, no real unit insignia, no real tail numbers.
4. **Never put a real product name** in the store listing, ads, shop items, achievements or file names. Internal art briefs can name the inspiration. The "Real reference" column below is **internal only**.
5. **Clear every nickname before launch**: search WIPO Global Brand Database, USPTO and EUIPO for the exact word in classes 9 (software), 28 (games), 12 (vehicles) and 13 (weapons). The tables avoid every conflict found during this research (e.g. Lynx, Puma, Boxer, Panther, Griffon, Rooivalk, Ratel, Anka, Saqr, Jobaria, Rabdan, Zulfiqar, Shahab, Ra'ad, Barq, Thuraya, Iron Dome are all real products, so none are used). But the check was not exhaustive.
6. **Israeli systems are excluded** (no Merkava, Iron Dome, Heron or Hermes lookalikes), because Israel is not in the game.

---

## 6. Suggested names per region

Columns: **Kind** | **Real reference (internal art brief only, never shown)** | **In-game nickname (EN)** | **Arabic display**. Names follow one theme per region so a player can tell the region from the name alone:
- Americas: English words (fortifications and native wildlife)
- Europe: Latin words; ships named after Latin virtues
- Eurasia: Russian words, transliterated
- Asia: pan-Asian wildlife and seas (deliberately not tied to one nation, to avoid China/India/Japan rivalry)
- MENA: Arabic words; ships named after Arabic star names
- Africa: pan-African wildlife and landmarks (Swahili or English)

### 6.1 Americas
| Kind | Real reference | EN | AR |
|---|---|---|---|
| Main battle tank | M1A2 Abrams | Bastion | باستيون |
| IFV | M2 Bradley | Halberd | هالبرد |
| Wheeled recon | Stryker / LAV-25 | Bluetick | بلوتيك |
| SP howitzer | M109A7 | Anvil | أنفِل |
| MLRS | M142 HIMARS / M270 | Firestorm | فايرستورم |
| SPAA | M-SHORAD | Picket | بيكيت |
| Mobile SAM | NASAMS | Lookout | لوك آوت |
| Strategic SAM / ABM | Patriot / THAAD | Citadel | سيتاديل |
| Air-superiority fighter | F-22 | Peregrine | بيريغرين |
| Strike fighter | F-35 / F-15E | Vanguard | فانغارد |
| Strategic bomber | B-2 / B-21 | Nightjar | نايت جار |
| Attack helicopter | AH-64 | Rattler | راتلر |
| Utility helicopter | UH-60 | Packhorse | باك هورس |
| Armed drone (MALE) | MQ-9 | Buzzard | بازارد |
| Loitering munition | Switchblade | Yellowjacket | يلو جاكيت |
| Frigate | Constellation-class | Cascade-class | فئة كاسكيد |
| Destroyer | Arleigh Burke | Meridian-class | فئة ميريديان |
| Attack submarine | Virginia | Tidewater-class | فئة تايدووتر |
| Aircraft carrier | Nimitz / Ford | Monarch-class | فئة مونارك |
| Cruise missile | Tomahawk | Longshot | لونغ شوت |
| Ballistic missile | ATACMS / PrSM | Highpoint | هاي بوينت |

### 6.2 Europe
| Kind | Real reference | EN | AR |
|---|---|---|---|
| Main battle tank | Leopard 2A8 / Leclerc / Challenger 3 | Ferrum | فيروم |
| IFV | CV90 / Puma | Hoplite | هوبلايت |
| Wheeled recon | Boxer / VBCI / Centauro | Vesper | فيسبر |
| SP howitzer | PzH 2000 / CAESAR / Archer | Bombarde | بومبارد |
| MLRS | MARS II / M270 MLRS | Fulmen | فولمن |
| SPAA | Skyranger / Gepard | Custos | كوستوس |
| Mobile SAM | IRIS-T SLM / CAMM | Scutum | سكوتوم |
| Strategic SAM / ABM | SAMP/T | Murus | موروس |
| Air-superiority fighter | Eurofighter Typhoon | Gerfalcon | جيرفالكون |
| Strike fighter | Rafale / Gripen | Stiletto | ستيليتو |
| Long-range strike aircraft (Europe has no heavy bombers) | Tornado (heavy-strike art) | Morrigan | موريغان |
| Attack helicopter | Tiger | Basilisk | بازيليسك |
| Utility helicopter | NH90 | Stork | ستورك |
| Armed drone (MALE) | Eurodrone | Buteo | بوتيو |
| Loitering munition | Warmate | Aculeus | أكوليوس |
| Frigate | FREMM / Type 26 | Constantia-class | فئة كونستانتيا |
| Destroyer | Type 45 / Horizon | Fortitudo-class | فئة فورتيتودو |
| Attack submarine | Astute / Suffren | Silentium-class | فئة سيلينتيوم |
| Aircraft carrier | Queen Elizabeth / Charles de Gaulle | Fortuna-class | فئة فورتونا |
| Cruise missile | Storm Shadow / Taurus | Spatha | سباثا |
| Ballistic missile (no real conventional equivalent) | Generic | Trebuchet | تريبوشيه |

### 6.3 Eurasia
| Kind | Real reference | EN | AR |
|---|---|---|---|
| Main battle tank | T-90M / T-72B3 | Kremen | كريمين |
| IFV | BMP-3 | Barsuk | بارسوك |
| Wheeled recon | BTR-82A | Sych | سيتش |
| SP howitzer | 2S19 Msta / 2S35 | Romashka | روماشكا |
| MLRS | Tornado-S / TOS-1A | Purga | بورغا |
| SPAA | Pantsir / Tor | Yozh | يوج |
| Mobile SAM | Buk-M3 | Strazh | ستراج |
| Strategic SAM / ABM | S-400 | Svod | سفود |
| Air-superiority fighter | Su-35 | Krechet | كريتشيت |
| Strike fighter | Su-34 | Shtyk | شتيك |
| Strategic bomber | Tu-160 / Tu-22M3 | Voron | فورون |
| Attack helicopter | Ka-52 / Mi-28 | Strekoza | ستريكوزا |
| Utility helicopter | Mi-8/17 | Los | لوس |
| Armed drone (MALE) | Orion | Filin | فيلين |
| Loitering munition | Lancet / Geran | Komar | كومار |
| Frigate | Admiral Gorshkov | Onega-class | فئة أونيغا |
| Destroyer / cruiser | Udaloy / Slava | Taymyr-class | فئة تايمير |
| Attack submarine | Yasen | Baikal-class | فئة بايكال |
| Aircraft carrier | Kuznetsov | Rodina-class | فئة رودينا |
| Cruise missile | Kalibr / Kh-101 | Sever | سيفير |
| Ballistic missile | Iskander-M | Taran | تاران |

### 6.4 Asia
| Kind | Real reference | EN | AR |
|---|---|---|---|
| Main battle tank | Type 99A / K2 / Type 10 / Arjun | Gaur | غاور |
| IFV | ZBD-04 / K21 | Takin | تاكين |
| Wheeled recon | ZBL-08 / Type 16 | Muntjac | مونتجاك |
| SP howitzer | PLZ-05 / K9 | Monsoon | مونسون |
| MLRS | PHL-16 / Pinaka / Chunmoo | Squall | سكوال |
| SPAA | PGZ-09 / K30 | Hornbill | هورنبيل |
| Mobile SAM | HQ-16 / Akash | Drongo | درونغو |
| Strategic SAM / ABM | HQ-9 / L-SAM | Summit | سَميت |
| Air-superiority fighter | J-20 / Su-30MKI | Falconet | فالكونيت |
| Strike fighter | J-16 / KF-21 | Krait | كرايت |
| Strategic bomber | H-6K / H-20 | Kite | كايت |
| Attack helicopter | Z-10 / LCH Prachand | Gharial | غاريال |
| Utility helicopter | Z-20 / Dhruv | Serow | سيرو |
| Armed drone (MALE) | Wing Loong II / CH-4 | Pallas | بالاس |
| Loitering munition | Generic | Cicada | سيكادا |
| Frigate | Type 054A / Mogami | Mekong-class | فئة ميكونغ |
| Destroyer | Type 055 / Sejong the Great | Coral-class | فئة كورال |
| Attack submarine | Type 093 / Soryu | Mariana-class | فئة ماريانا |
| Aircraft carrier | Fujian / Vikrant | Pacifica-class | فئة باسيفيكا |
| Cruise missile | CJ-10 / BrahMos | Arrowhead | أروهيد |
| Ballistic missile | DF-15 / Hyunmoo-2 / Agni | Starfall | ستارفول |

### 6.5 MENA (Arabic names first; English is a transliteration)
| Kind | Real reference | AR | EN |
|---|---|---|---|
| Main battle tank | M1A2S / Leclerc / Altay / T-90S | الجبل | Al-Jabal |
| IFV | BMP-3 / Tulpar | الوعل | Al-Wa'l |
| Wheeled recon | Patria AMV / Pars | الفنك | Al-Fanak |
| SP howitzer | T-155 Firtina / K9 | المِرزم | Al-Mirzam |
| MLRS | TRG-300 / Fajr | الوابل | Al-Wabil |
| SPAA | Korkut / Pantsir-S1 | اليقظ | Al-Yaqiz |
| Mobile SAM | Hisar / Khordad 15 | الحارس | Al-Haris |
| Strategic SAM / ABM | Patriot / THAAD / Bavar-373 | السور | As-Sur |
| Air-superiority fighter | F-15SA / Typhoon | الحُرّ (the saker/peregrine of Arab falconry) | Al-Hurr |
| Strike fighter | Rafale / F-16 Block 60 | السهم | As-Sahm |
| Strategic bomber (no real regional equivalent) | Su-24 / Tornado art | النسر | An-Nasr |
| Attack helicopter | T129 ATAK / AH-64 | الزنبور | Az-Zunbur |
| Utility helicopter | UH-60 / T625 | الرحّال | Ar-Rahhal |
| Armed drone (MALE) | TB2 / Akinci / Shahed-129 | الرخم | Ar-Rakhm |
| Loitering munition | Shahed-136 / Kargu | الدبّور | Ad-Dabbur |
| Frigate | MEKO A-200 / Istif | فئة سهيل | Suhail-class |
| Destroyer | TF-2000 (planned) | فئة الشِّعرى | Ash-Shi'ra-class |
| Attack submarine | Type 209/214 | فئة الدبران | Ad-Dabaran-class |
| Aircraft / drone carrier | Mistral (Egypt) / TCG Anadolu | فئة الجوزاء | Al-Jawza'-class |
| Cruise missile | SOM / Hoveyzeh | الرمح | Ar-Rumh |
| Ballistic missile | Tayfun / Fateh-110 / Khorramshahr | المذنَّب | Al-Mudhannab |

### 6.6 Africa
| Kind | Real reference | EN | AR |
|---|---|---|---|
| Main battle tank | T-72 / VT4 / Olifant | Tembo | تيمبو |
| IFV | BMP-2 / Ratel-type | Nyati | نياتي |
| Wheeled recon | Rooikat / Type 92 | Duiker | دويكر |
| SP howitzer | G6 / 2S1 | Baobab | باوباب |
| MLRS | BM-21 Grad | Harmattan | هارماتان |
| SPAA | ZU-23 / ZSU-23-4 | Weaver | ويفر |
| Mobile SAM | S-125 / Chinese export SAM | Hamerkop | هاميركوب |
| Strategic SAM / ABM | Generic export long-range SAM | Kilima | كيليما |
| Air-superiority fighter | Su-27/30 / MiG-29 | Lanner | لانر |
| Strike fighter | JF-17 / A-29 Super Tucano | Boomslang | بومسلانغ |
| Long-range strike | Generic | Marabou | مارابو |
| Attack helicopter | Mi-24/35 | Genet | جينيت |
| Utility helicopter | Mi-17 | Okapi | أوكابي |
| Armed drone (MALE) | TB2 / Wing Loong | Lappet | لابيت |
| Loitering munition | Generic | Tsetse | تسي تسي |
| Frigate | Valour-class (MEKO A-200) | Zambezi-class | فئة زامبيزي |
| Destroyer | Generic | Kalahari-class | فئة كالاهاري |
| Attack submarine | Type 209 | Tanganyika-class | فئة تنجانيقا |
| Aircraft carrier | Generic | Serengeti-class | فئة سيرينغيتي |
| Cruise missile | Generic | Assegai | أسيغاي |
| Ballistic missile | Scud-type | Ngoma | نغوما |

Known risks to check first: "Filin", "Komar", "Assegai", "Vanguard", "Citadel", "Firestorm" and "Summit" are common words with possible prior uses in defence or games. Clear them, or swap in a backup word from the same theme.

---

## 7. Unit card text: "what this kind specializes in"

One plain sentence per kind for kids and genre newcomers, in English and Arabic. The Arabic describes the unit, never the player, so no masculine/feminine forms are needed.

### Infantry
| Kind | English | العربية |
|---|---|---|
| Motorized infantry | Cheap, quick-to-train soldiers on trucks; best at holding cities, forests and hills, but weak against tanks in the open. | مشاة على شاحنات، رخيصة وسريعة التجهيز؛ تتفوق في التمسك بالمدن والغابات والتلال، لكنها تضعف أمام الدبابات في الأرض المكشوفة. |
| Mechanized infantry (IFV) | Soldiers who fight from armoured vehicles with cannons; they keep up with tanks and clear out enemy infantry. | مشاة تقاتل من مركبات مدرعة مسلحة بمدافع؛ تواكب الدبابات وتطهّر مواقع مشاة العدو. |
| Airborne | Light troops dropped behind enemy lines to seize airports, bridges and cities by surprise. | قوات خفيفة تُنزَل خلف خطوط العدو للاستيلاء المفاجئ على المطارات والجسور والمدن. |
| Marines | Infantry trained to land from ships; the best unit for capturing coasts and islands. | مشاة مدرَّبة على الإنزال من السفن؛ أفضل وحدة لاقتحام السواحل والجزر. |
| Special forces | Small elite teams that sneak, scout and sabotage; strong in rough terrain, fragile in open battle. | فرق نخبة صغيرة للتسلل والاستطلاع والتخريب؛ قوية في الأرض الوعرة، هشة في المعارك المفتوحة. |
| National guard / reserves | Low-cost local defenders that make every city expensive to capture. | مدافعون محليون منخفضو الكلفة يجعلون احتلال أي مدينة باهظ الثمن. |

### Armour
| Kind | English | العربية |
|---|---|---|
| Main battle tank | The heavy spearhead: thick armour and a big gun to break through lines and win fights in open ground. | رأس الحربة الثقيل: درع سميك ومدفع كبير لاختراق الخطوط وحسم القتال في الأرض المكشوفة. |
| Wheeled recon vehicle | Fast armoured car that spots enemies from far away and raids weak rear areas. | مدرعة سريعة على عجلات تكشف العدو من بعيد وتُغير على المؤخرات الضعيفة. |
| Tank destroyer | Hunts tanks with long-range guided missiles from hidden positions; poor at holding ground. | صائد دبابات يطلق صواريخ موجَّهة بعيدة المدى من مواقع مخفية؛ ضعيف في التمسك بالأرض. |

### Artillery & rockets
| Kind | English | العربية |
|---|---|---|
| Towed artillery | Cheap long-range guns that pound targets from behind the front, but they are slow to move. | مدافع بعيدة المدى رخيصة تقصف الأهداف من خلف الجبهة، لكنها بطيئة الحركة. |
| Self-propelled howitzer | Armoured gun that fires, moves, and fires again before the enemy can answer. | مدفع مدرع يُطلق ثم يغيّر موقعه ويُطلق مجدداً قبل أن يرد العدو. |
| Multiple rocket launcher (MLRS) | Fires a devastating rocket salvo over a wide area, then needs time to reload. | يُطلق رشقة صواريخ مدمّرة على مساحة واسعة، ثم يحتاج وقتاً لإعادة التذخير. |

### Air defence
| Kind | English | العربية |
|---|---|---|
| Self-propelled anti-air (SPAA) | Travels with your army and shreds nearby helicopters, drones and low-flying jets. | يرافق قواتك ويمزّق المروحيات والمسيّرات والطائرات المنخفضة القريبة. |
| Mobile SAM | Guards a whole region's sky against jets and cruise missiles at medium range. | يحمي سماء منطقة كاملة من الطائرات وصواريخ كروز على مدى متوسط. |
| Strategic air & missile defence | Long-range shield for cities that can intercept ballistic missiles. | درع بعيد المدى للمدن قادر على اعتراض الصواريخ الباليستية. |

### Air force
| Kind | English | العربية |
|---|---|---|
| Air-superiority fighter | Wins control of the sky by hunting enemy aircraft. | تنتزع السيطرة على الأجواء بمطاردة طائرات العدو. |
| Strike fighter | Fast jet that bombs ground targets and ships, and can still defend itself in the air. | مقاتلة سريعة تقصف الأهداف البرية والسفن، وتستطيع الدفاع عن نفسها في الجو. |
| Stealth fighter | Hard to detect; slips past air defences to hit key targets first. | يصعب رصدها؛ تتسلل عبر الدفاعات الجوية لتضرب الأهداف الحيوية أولاً. |
| Strategic bomber | Carries huge payloads deep into enemy land to destroy cities and industry. | تحمل حمولات ضخمة إلى عمق أراضي العدو لتدمير المدن والصناعة. |
| AWACS | Flying radar that reveals everything in the air and on the ground around it. | رادار طائر يكشف كل ما حوله في الجو وعلى الأرض. |

### Helicopters
| Kind | English | العربية |
|---|---|---|
| Attack helicopter | Flies low to destroy tanks and vehicles fast, but is easy prey for anti-air. | تحلّق على ارتفاع منخفض لتدمير الدبابات والمركبات بسرعة، لكنها فريسة سهلة للدفاع الجوي. |
| Utility / transport helicopter | Moves troops quickly over rivers, mountains and front lines. | تنقل الجنود بسرعة فوق الأنهار والجبال وخطوط الجبهة. |
| Anti-submarine helicopter | Ship-based helicopter that hunts submarines. | مروحية تنطلق من السفن لمطاردة الغواصات. |

### Drones
| Kind | English | العربية |
|---|---|---|
| Recon drone | Cheap eye in the sky that watches an area for a long time. | عين رخيصة في السماء تراقب منطقة لفترة طويلة. |
| Armed drone (MALE) | Patrols for hours and strikes vehicles and artillery with precision. | تجوب الأجواء لساعات وتضرب المركبات والمدفعية بدقة. |
| Loitering munition | Circles over the battlefield, then dives into its target and is used up. | تحوم فوق ساحة المعركة ثم تنقضّ على هدفها وتُستهلَك بالضربة. |
| Naval drone | Small crewless boat that rams and damages large warships. | زورق صغير بلا طاقم يصطدم بالسفن الحربية الكبيرة ويُلحق بها الضرر. |

### Navy
| Kind | English | العربية |
|---|---|---|
| Corvette | Small, cheap warship that guards coasts and hunts submarines. | سفينة حربية صغيرة ورخيصة تحرس السواحل وتطارد الغواصات. |
| Frigate | All-round escort that protects fleets from submarines and aircraft. | سفينة مرافقة متعددة المهام تحمي الأساطيل من الغواصات والطائرات. |
| Destroyer | Heavy escort with powerful air defence and long-range missiles. | سفينة مرافقة ثقيلة ذات دفاع جوي قوي وصواريخ بعيدة المدى. |
| Attack submarine | Hidden underwater hunter that sinks ships and cuts supply lanes. | صيّاد خفي تحت الماء يُغرق السفن ويقطع خطوط الإمداد. |
| Ballistic-missile submarine | Hides deep in the ocean carrying strategic missiles; a second-strike deterrent. | تختبئ في أعماق المحيط حاملةً صواريخ استراتيجية؛ أداة ردع للضربة الثانية. |
| Aircraft carrier | Floating airbase that takes your air power anywhere at sea. | قاعدة جوية عائمة تمدّ قوتك الجوية إلى أي مكان في البحر. |
| Amphibious assault ship | Carries marines and helicopters to land them on enemy shores. | تحمل مشاة البحرية والمروحيات لإنزالها على شواطئ العدو. |

### Missiles
| Kind | English | العربية |
|---|---|---|
| Cruise missile | Flies low and precise to destroy one high-value target. | يطير على ارتفاع منخفض وبدقة عالية لتدمير هدف واحد عالي القيمة. |
| Ballistic missile | Very fast and hard to intercept; hits cities and bases from far away. | سريع جداً ويصعب اعتراضه؛ يضرب المدن والقواعد من مسافات بعيدة. |
| Coastal anti-ship battery | Shore launcher that closes sea lanes to enemy ships. | منصة ساحلية تُغلق الممرات البحرية أمام سفن العدو. |
| Strategic (nuclear) missile | Can wipe out a city and turn a war, but using it costs heavily in diplomacy and fallout. | سلاح قادر على محو مدينة وتغيير مسار الحرب، لكن استخدامه يكلّف ثمناً دبلوماسياً وإشعاعياً باهظاً. |

**Writing rules used:** ≤ 22 words in English; Arabic in Modern Standard Arabic (the localisation guides recommend MSA across the Arab world, [PocketGamer.biz](https://www.pocketgamer.biz/cruise-to-the-east-how-to-successfully-localize-a-game-into-arabic/)); no jargon without a hint of what it means. Each line says one strength and, where relevant, one weakness. That teaches counters without a tutorial pop-up.

---

## 8. Open questions for the owner
1. Six doctrines (recommended) or five (Option B: Latin America joins Africa as "light forces")?
2. Is a "Why?" tooltip showing the real-world justification wanted? It's educational and builds trust, but it mentions real countries' weaknesses, which some players may take personally. Suggest wording it as "inspired by" plus strengths first.
3. Do Arabic players see foreign nicknames transliterated (recommended, matches Arab media) or translated into meaning-words?
