# Research: Easy to learn, deep to master, and profitable with no pay-to-win

Prepared for: modern-war RTS for Android (Arabic-first, real-world map, up to 60 players, ~15-day matches, 1 game day = 6 real hours).
Date of research: 12 Nov 2026.

**How to read this file**
- Every number has a source (listed at the end, numbered [S#]).
- **[UNCERTAIN]** = the source is weak, only a headline was seen, or the figure is an estimate by a third party.
- **[ASSUMPTION]** = my own modelling input, not a researched fact.
- **[NOT FOUND]** = I searched and could not find a reliable figure.
- Research limits: Steam's review API, Google Play pages and Reddit were blocked to my tools, so complaint patterns come from Steam discussion threads, the App Store page, the official Supremacy forums and press. Near the end the page-fetch tool hit a usage limit, so a few items (marked) rely on search-result headlines only.

---

## Executive summary (one page)

1. **Our main rival is now "Supremacy: World War 3"** (renamed from Conflict of Nations in April 2025). It belongs to Stillfront through Twin Harbour Interactive (the merged Bytro + Dorado). The Supremacy franchise (1914, Call of War, WW3, and likely the new Warhammer 40k title) made **SEK 894M in the 12 months to Q2 2026** [S3], roughly **USD 85–95M** [UNCERTAIN: depends on the exchange rate]. In the **US alone, on mobile**, Sensor Tower measured WW3 at **~$186K–$417K per week** (2023–2025) [S5][S6][S7].
2. **The top complaints about it are all fixable:** gold buys speed-ups, morale and units in the middle of a match ("A none paying player will never win, never") [S8][S9]; new players get wiped out in their first days [S8]; the game "doesn't teach you" [S10]; and convenience features (build queues, rally points, alliance creation, shared intel) sit behind the **Security Council subscription** [S11]. That last point makes the game *harder* for free players, not just slower.
3. **The "easy without removing depth" playbook is well proven.** The core moves are: an accelerated bot match first; unlocking systems one at a time over the first matches (Marvel Snap); an advisor with Full / Warnings-only / Off settings (Civ VII); cutting tutorial text by about two-thirds (Crusader Kings III); free auto-queues and doctrine presets; rookie-only matches; AI replacing inactive players; and after-action reports. Section A4 lists 24 techniques.
3b. **Supply chain (owner's worry).**
   - The rival has *no* supply lines, just a national resource pool [S60].
   - HOI4's deep rework confused players for months [S63].
   - Fix: **3 layers**. (1) Automatic "connected = supplied" with territory tint and blinking cut-off areas (Company of Heroes 2, Unity of Command). (2) One-tap forward depots and a "Fix bottleneck" button (HOI4). (3) Interdiction and airlifts unlocked later. Gentle penalties. Details in A5.
4. **Retention targets.** Strategy games average **D1 25% / D7 8% / D30 3%** (Mistplay via Segwise) [S14]. The best 4X games reach **D1 42% / D7 17% / D30 8%** (Whiteout Survival, Naavik via GameGrowthAdvisor) [S15]. MENA D1 is around **20–21%** (Adjust) [S16]. Target D1 ≥35%, D7 ≥12%, D30 ≥5%.
5. **Fair monetisation can earn well.** When Clash of Clans added the Gold Pass, spending **rose 58% in the first 30 days**, and 2019 revenue grew 27% year on year [S27]. Clash Royale's pass reportedly lifted weekly revenue **178%** [S28, UNCERTAIN: headline only]. Fortnite made **$9.1B in 2018–2019** from cosmetics and its pass [S29]. Polytopia sells only non-consumable tribes and skins, with no currency, and keeps 600–700K MAU after 8.5 years [S31].
6. **MENA fits this game.** Strategy was the **#1 genre by revenue in the Middle East in 2024 (+38% YoY)** (Sensor Tower) [S19], and **22.5% of top-grossing revenue on Google Play in MENA** in H1 2024 (Apptica) [S20]. Players in the Gulf pay with mada, carrier billing (STC, Mobily, Zain, Virgin) and gift cards [S17][S18]. Ramadan and Eid lift gaming installs by +24% and +27% (Adjust) [S22].
7. **Recommended plan (Section B5):** 14 products covering cosmetics, a Commander Pass, a "Command Staff" convenience subscription that never touches match power, coalition cosmetics, gifting, private-match hosting, a supporter pack, seasonal Ramadan/Eid/national-day bundles, and opt-in rewarded ads that never pay out in-match resources. Modelled **gross** revenue: **low ~$0.09M/yr, mid ~$1.3M/yr, high ~$9M/yr**. All inputs are stated assumptions.

---

# PART A — Making a deep strategy game easy (without removing features)

## A1. What new players of Conflict of Nations / Supremacy WW3 complain about

**Context on the rival**
- Renamed "Supremacy: World War 3 (formerly Conflict of Nations)" in April 2025, when Bytro and Dorado merged into Twin Harbour Interactive (150+ staff, part of Stillfront). The three Supremacy games had **>2M MAU combined in March 2025** [S1].
- Google Play: 15.1M+ installs, 186K ratings, 4.31★; released 3 Sep 2020 [S12]. App Store (US): 4.7★ from 77K ratings [S10].
- **What gold does** (official help centre): "raise morale for provinces and troops", "speed up unit recruitment and construction", "reduce enemy morale directly" [S13]. Each of these changes who wins a match.
- **What the Security Council subscription does** (Steam DLC page): "mobilization and construction queuing", "enhanced artillery fire-control system", "player alliance creation", "unit rally point setting", "multiplayer shared intelligence", "more simultaneously active matches" [S11]. App Store prices: 30 days $9.99, 60 days $14.99. Gold packs run from $1.99 to $119.99, and there is a $4.99 starter pack [S10]. A Steam bundle sells 760,000 gold plus 12 months of Security Council for $199.99 [S11].

**Complaint patterns, with quotes**

| Pattern | Evidence (verbatim where available) |
|---|---|
| **1. Gold = pay-to-win, especially mid-match** | "getting attacked on the 4th a 7th day from players paying for gold speeding up their builds" and "A none paying player will never win, never." (Steam thread, 2019) [S8]. "money in the hands of a player with more than zero skill can completely unbalance the game" (and this from a defender of the game). "it costs nearly 1000 gold to build 1 infantry unit". A whale "instantly buys stacks of units"; "People will and do spend thousands on a single match" (Steam thread, 2022–24) [S9]. App Store reviewer: the game is "kind of p2w" and "these problems discourage me from playing it" [S10]. On the Call of War forum (same company, same gold model): "money always wins!!!" and "It is a serious problem and it is massively putting me off from playing" [S32]. |
| **2. New players get wiped out early ("farmed")** | "i lasted 2 days before i was wiped out" [S8]. Several players in the thread say they quit: "do not see the point in this" [S8]. |
| **3. The game does not teach itself** | App Store reviewer: the game "doesn't teach you how to do this itself" [S10]. Call of War forum: "There is too much dependence on Gold conveyed in the tutorial" [S32]. Reddit r/ConflictofNations posts are mostly "How do I get better at the game and get better stats", "First time playing as India any tips?" and "How do I fight with another player?" [S33]. Basic know-how is clearly not getting through. |
| **4. Real-time research and mobilisation are tiring** | App Store reviewer dislikes "the gold spending stuff" and the real-time research and mobilisation, and also complains that "players can be toxic" and asks for a block option [S10]. |
| **5. Inactive or abandoning allies** | "Chad leaving" (Reddit, an ally quits mid-game) [S33]. Abandoned slots are re-offered to new players **only before Day 5** [S34], so later gaps stay empty. |
| **6. Community wants gold-free modes** | "Can't you just introduce a separate game mode for people who want to play without gold use?" One player wants paid "premium only" matches with no gold, and another would "rather pay for a game like this upfront" [S8]. "there should be an option to make non-gold maps" [S32]. The developer's 2019 answer was gold-free **Elite Alliance matches, open only at Rank 25+** [S8]. So the fair mode is locked away from exactly the new players who need it. |
| **7. Bugs, lag, QoL** | "will start lagging" after a while [S10]. "still filled with bugs and much needed QoL improvements" [S9]. |

**Balance note:** some veterans argue gold does not decide games: "you'd need to spend at least 500 € in a round to beat an experienced player" and "most whales are really bad players" [S9]. Even that defence admits money changes outcomes. In a 60-player diplomacy game, *perceived* unfairness is enough to drive churn.

**What this means for us:**
(a) Sell nothing that changes a match: no speed-ups, morale, units, resources or intel.
(b) Make every convenience the rival charges for **free** (queues, rally points, alliance creation, shared intel). That is a marketing line in itself.
(c) Protect players in their first matches.
(d) Fill gaps left by inactive players with AI.
(e) Teach through play, not a wall of text.

## A2. How successful complex games teach and hide complexity

| Game | What they do | Source |
|---|---|---|
| **Marvel Snap** | Unlock order is designed to teach. Cards with "on reveal" and "ongoing" abilities arrive in sequence so players learn combos (Iron Man/Punisher → Spectrum; Ironheart/Wolfsbane/White Tiger → Odin). Instead of adding a mulligan for bad opening hands, they made one card always appear in the opening hand, and mulligan requests stopped. | [S35] |
| **Crusader Kings III** (Paradox) | Progressive disclosure: interface panels revealed in stages. Tutorial cut from **67 text boxes to about 1/3**. Narrative onboarding events. Explanatory tooltips on events. Outside staff playtested it to beat the "curse of knowledge". Telemetry showed finishing the tutorial "wasn't a major determining factor" in retention, so teaching must continue *after* the tutorial. | [S36] |
| **Civilization VII** | Tutorial switched on automatically in the first game. Four advisors, each covering one area (and players can listen to just one). Small default "continent-plus" map for learning. Three guidance levels: Tutorial on → **"Only Warnings"** (advisors speak only when a problem is coming) → Off. The developers themselves play with warnings on. | [S37] |
| **The Battle of Polytopia** | "A minimalism of experience". Aim to "make the complex feel simple". Depth is layered and revealed as players learn. The CEO criticises Age of Empires Mobile for a tutorial "about three times longer than a typical mobile session". | [S30] |
| **Whiteout Survival / Last War** | A simple idle or minigame front sits before the 4X layer (Frozen City in front of Whiteout). Ads show what new players actually play first, so ad creatives are honest and conversion is high. | [S38] |
| **Rise of Kingdoms** | Advisor character guides the step-by-step tutorial (experienced players can skip ahead). Quests give constant direction. Smoother onboarding and UI than first-generation 4X. Over $2B lifetime revenue. | [S39][S38] |
| **Clash of Clans** | Opens with action (goblins attack you) instead of a name screen. Tutorial runs a little over 6 minutes, with about 80 seconds of action and the longest battle around 40 s. The name prompt comes late, and the author links the keyboard interruption to churn. | [S40] |
| **Clash Royale** | Lower trophy levels reportedly contain more bot opponents, so new players can practise and win [UNCERTAIN: Supercell has not commented]. Slow, gradual tutorial for a card MOBA. | [S41][S42] |
| **Grand-strategy newcomers (Afterworld, Paradox-style)** | Survival-first progression, visible automation, light goal structure "to establish direction without reducing the game to a checklist". "a game cannot become completely easy and still remain a grand strategy game". | [S43] |
| **4X genre (GameRefinery)** | Guild tasks (members help with timers), guild shop and guild gifts (in over 92% of top-200 4X games). Social systems keep people playing. Newer titles invest in colourful, approachable UI and visuals. | [S44] |
| **Supremacy WW3 itself** | New accounts start on tutorial maps (Battleground USA, Flashpoint, Global Conflict) with many small AI countries [S34]. Gold-free Elite matches are locked behind Rank 25 [S8]. | [S34][S8] |

[NOT FOUND] Usable public sources on the onboarding of Northgard, Total Battle, Warpath, Hearts of Iron IV, Supremacy 1914 and Civilization mobile. HOI4 is mostly cited as the example of a steep curve (a Steam player with 8,000 hours says "the first 1,000 hours are just the tutorial") [S45].

## A3. Retention numbers and first-session length

| Benchmark | D1 | D7 | D30 | Source |
|---|---|---|---|---|
| Strategy genre (Mistplay data) | 25.4% | 8.1% | 3.1% | [S14] |
| All mobile games, top 25% (GameAnalytics 2025 report, 2024 data) | 26.5–27.7% (iOS 31–33%, Android 25–27%) | top 25%: 7–8%; median 3.4–3.9% | D28: 75% of games below 3% | [S46] |
| Whiteout Survival (iOS US, 2024) | 42% | 17% | 8% | Naavik via [S15] |
| Last War (iOS US, 2024) | 34% | 11% | 4% | Naavik via [S15] |
| MENA games D1 (Adjust 2025) | ~20% (Saudi 21%, UAE 21%) | – | – | Adjust via [S16] |

**Session norms (GameAnalytics) [S46]:** median session 5–6 min (top 25%: 8–9 min). Midcore games average 6–7 sessions a day. Median daily playtime is 22 min. Multiplayer games lead on session length.

**Tutorial completion target:** 70–80% of players should finish. One F2P game had only 40% finish. A 120-step tutorial lost players at invisible loading steps, and fixing that raised D1 by 10% (devtodev) [S47]. Players should understand why the game is fun "within two to three minutes" (GameAnalytics) [S48].

**Monetisation per active user, for comparison:** Whiteout ARPDAU $1.08 and Last War $2.47 (iOS US, Naavik via [S15]). Stillfront group ARPDAU is SEK 2.14 (about $0.21–0.23 [UNCERTAIN: FX]) on 6.7M DAU / 33.6M MAU, so **DAU/MAU ≈ 0.20** [S3].

**What drives these numbers:**
- **D1:** first-session fun and a clear goal for tomorrow.
- **D7:** social bonds (coalition), match progress, daily objectives.
- **D30:** meta-progression across matches, seasons, coalitions, rank.

A 15-day match helps D7 and D30 (players are invested in "their" war) but hurts D1 (slow start) and the end of each match (churn at match end, and when a player starts losing). **Target: first guided session of 8–12 minutes ending on a win, D1 ≥35%, D7 ≥12%, D30 ≥5%** [ASSUMPTION: set between the genre average and Whiteout].

## A4. 24 concrete techniques to apply

Each technique is tied to an example game and a source.

1. **"Boot Camp" accelerated bot match (20–30 min).** A small map against 3–5 AI nations, with time running 20–40× faster so the player goes through a whole game cycle (build → research → attack → peace) in one sitting. *Example:* Supremacy's tutorial maps full of small AI countries [S34]. Clash Royale's bot-heavy low ranks [S41].
2. **Rookie-only matches for the first 2–3 real games.** Restrict them to accounts below rank X, with stronger AI filling the empty slots. *Example/contrast:* Supremacy gates its fair Elite matches behind Rank 25 [S8]. Do the opposite and protect beginners.
3. **Unlock systems match by match.** Match 1: land units, economy, basic diplomacy. Match 2: air and the full research tree. Match 3: navy, espionage, missiles and coalitions. Veterans can "test out" with a quiz or skip. *Example:* Marvel Snap's teaching unlock order [S35]. CK3's staged panels [S36].
4. **Unlock features by game day inside each match** for new players: day 1 economy, day 2 army, day 3 diplomacy. The full UI is always one "Advanced" toggle away. *Example:* CK3 progressive disclosure [S36]. Polytopia's layered depth [S30].
5. **First guided session no longer than one normal session (8–12 min), ending in a victory.** *Example:* Polytopia CEO on Age of Empires Mobile's tutorial being 3× a session [S30]. GameAnalytics session norms [S46]. Clash of Clans' ~6-minute tutorial [S40].
6. **Action first, account and name later.** Start with an invasion to repel. Ask for the name and login after the first win. *Example:* Clash of Clans' goblin attack and the churn from its late name prompt [S40]. GameAnalytics "no paywall, ad or signup first" [S48].
7. **Cut tutorial text by two-thirds.** Teach with arrows, highlights and doing. Each box holds one sentence in Arabic and English. *Example:* CK3 went from 67 boxes to about 1/3 [S36].
8. **"Chief of Staff" advisor with three levels: Full guidance, Warnings only (default from match 2), Off.** *Example:* Civ VII advisors and "Only Warnings" [S37]. Rise of Kingdoms' advisor character [S39].
9. **Problem warnings, not lectures.** "Province X is undefended and an enemy army arrives in 3 h", "Research slot idle", "Factory idle", "Low fuel". Tap a warning to fix it. *Example:* Civ VII warnings mode [S37].
10. **Free auto-queues, rally points, templates and "repeat production" for everyone.** Players can then sleep without losing, which removes the main way people get "farmed". *Contrast:* Supremacy puts queuing and rally points behind a paid subscription [S11].
11. **Doctrine presets ("recommended builds").** For example Defensive, Balanced, Air Power, Naval. Each auto-suggests research and production, and every suggestion can be edited. Later the player can save their own doctrines. *Example:* new Supremacy players keep asking for build orders ("How do I get better… stats") [S33]. Marvel Snap's teaching starter progression [S35].
12. **Guaranteed viable start.** Balanced starting provinces and a starter army template, so the first days cannot be lost to a bad spawn. *Example:* Marvel Snap's opening-hand fix [S35].
13. **Beginner protection that cannot be bought.** In rookie matches nobody can declare war on a newcomer for the first ~2 game days (12 real hours). After that, the protected player receives an AI "guarantor" alliance. *Example:* the "wiped out in 2 days" complaints [S8].
14. **AI takes over inactive nations immediately** (defensive AI), and new players can join any match where an AI-run nation is available, not just before Day 5. *Contrast:* Supremacy only re-offers abandoned slots before Day 5 [S34].
15. **After-action report ("why did I lose / win").** Explain each battle in one screen: counters, terrain, morale, air cover, supply, plus "what to do next time". The full version stays free. *Example:* Chess.com sells analysis tools inside premium [S49]. We give learning tools away free, because good players stay.
16. **Nested tooltips and an in-game encyclopedia** (tap any term for its definition; long-press for numbers). *Example:* CK3 added explanatory tooltips to core events [S36].
17. **Narrative onboarding events.** Short story events (an "Arab coalition intelligence brief") that teach a mechanic the player will use often. *Example:* CK3 narrative tutorial events [S36].
18. **A 10-minute "Skirmish" mode** (1 vs 3 AI, accelerated) that serves as a funnel, a practice space and the honest ad creative. *Example:* Whiteout Survival's Frozen City front and honest ads [S38].
19. **Mentor coalitions.** New players are offered an "Academy" coalition with veterans who earn cosmetic rewards when their rookies finish a match. *Example:* 4X guild tasks and guild gifts [S44].
20. **Clear goals after the tutorial.** Daily "orders" that teach one thing each (build an airbase, sign a trade deal), plus a 7-day "Officer Academy" track with cosmetic rewards. *Example:* GameAnalytics tip "set goals after the tutorial" [S48]. Rise of Kingdoms' quest flow [S39].
21. **Funnel every tutorial step with analytics.** Target 70–80% completion and look for invisible drop-offs such as loading screens. *Example:* devtodev case, where fixing loading steps raised D1 10% [S47].
22. **Small default map and fewer rivals in the first real match** (e.g., a 20-player Middle East theatre before the 60-player world map). *Example:* Civ VII's small learning map [S37].
23. **Smart notifications built for 15-day matches,** with timing adjusted in Ramadan (activity peaks late at night and before dawn). Add "night defence stance" orders. *Example:* Ramadan activity patterns [S23].
24. **Playtest with outsiders and keep the old tutorial for A/B testing.** *Example:* CK3 brought in staff from other teams and kept the old tutorial for comparison [S36].

## A5. Supply chain: how other games make supply easy to understand, or automatic (owner's extra question)

### What the reference games do

| Game | Supply model | What makes it readable or hard | Source |
|---|---|---|---|
| **Supremacy WW3 (the rival)** | **No supply lines at all.** Seven resources go into one national pool. Fuel and manpower pay unit upkeep, and resources can be bought on a market. Overexpansion means you cannot afford to maintain units. | Very simple, but no logistics strategy. The only lever is "economy". There is no cutting enemy lines and no rewarding encirclement. | [S60] |
| **Company of Heroes 2** | Each map sector **must be connected to your base** to produce resources. A cut-off sector stays yours but produces nothing. The base cannot be lost. | **Cut-off sectors blink on the map.** One binary rule ("connected or not"), shown with one visual cue. | [S61] |
| **Unity of Command (I/II)** | A few supply sources. Supply runs along connected rail, and each rail tile projects supply over a range depending on terrain. Capturing a depot or rail tile cuts off every unit in its radius. A limited number of **supply drops** per turn can rescue cut-off units. | Supply is the core of strategy ("think in terms of territory, not unit matchups"). Unit icons show supply status. **The case study criticises hiding supply behind an overlay**: important information should be visible by default, and a marker at the edge of the safe zone is suggested. | [S62] |
| **Hearts of Iron IV (since patch 1.11 / No Step Back, 2021)** | Capital → railways (trains) → supply hubs → trucks (motorisation extends hub range) → divisions. Routes work at the level of their **weakest segment**. Out of supply means no reinforcements, no fuel, attrition. | Deep, but it confused players. A Steam thread 6 months after release says most of the anger targets supply, and the "upgrade railways" button "doesn't work half the time" [S63]. The fix that helped: an **"Upgrade bottlenecks" button** on supply nodes [S64]. Paradox also **removed a weather/terrain/distance penalty because it "compounded in a hard-to-predict way"** and replaced it with fixed hub ranges [S65]. | [S63][S64][S65][S66] |
| **Board wargames (survey)** | Spectrum from simplest to hardest: (1) trace a line of supply of N hexes to a road or rail link back to a source (simple, "doesn't bog the game down"); (2) supply points spent to activate HQs (scarcity creates choices); (3) moving fixed numbers of trucks with fuel and ammo (Operational Combat Series: **~60 pages of rules**, hard to learn). | The more you model transport, the harder the game is to learn. Tracing to a source gives most of the strategic value. | [S67] |
| **RTS design discussion** | Ideas: units look ragged when starving, a pipeline line from base to army whose thickness shows flow (but it clutters the screen), strategic-map check for a clear line home, visible supply trucks (risk of micromanagement). | Show supply with visuals players read at a glance, and avoid making them micromanage trucks. | [S68] |

### Recommended "Supply in 3 layers" design

The rule behind this: keep the depth (encirclement, interdiction, choke points) but make the **default automatic and visible**.

1. **Layer 1 – Automatic, always on (every player, match 1).**
   - Supply flows by itself from any friendly city through **connected friendly territory**, using one CoH-style rule: "connected = supplied".
   - No trucks or convoys to manage.
   - Your own territory is tinted by supply state (full / stretched / cut off), always visible and not hidden in an overlay (Unity of Command lesson).
   - A cut-off area **blinks** (CoH2).
   - Every unit card shows a single supply pip (green / yellow / red).
2. **Layer 2 – One-tap fixes.**
   - Supply strength drops with distance from the nearest city or depot along fixed, predictable ranges, never compounding hidden penalties (HOI4 lesson).
   - Building a **forward depot** extends the range.
   - The advisor warns: "3rd Armoured will run out of fuel in 6 h. Build a depot at X, or pull back?" The player taps once to do it.
   - A **"Fix bottleneck" button** finds and queues the upgrade (HOI4 lesson).
3. **Layer 3 – Advanced, unlocked in match 2 or 3.**
   - Interdiction: air strikes and missiles on depots and rail.
   - A limited number of **airlift / supply drops** per game day to save encircled units (Unity of Command).
   - Naval supply for islands.
   - Optional convoy view for experts. **Never** require players to micromanage trucks (avoid the OCS / HOI4 trap).
4. **Gentle, readable penalties.**
   - Out of supply means slower reinforcement first, then a slow attack penalty, then attrition after about one game day. Never instant death.
   - Players asleep during a 15-day match then have time to react. Push notification: "Army cut off."
5. **Teach it through a story.** One Boot Camp mission: "Cut the enemy's road and watch their army weaken". Players learn the value of supply by *using* it against the AI before they suffer from it.
6. **AI-run allies and inactive nations use the same automatic supply,** so no part of the map breaks when a player is away.
7. **Never sell supply.** No paid instant resupply, extra depots or airlift charges. That would be pay-to-win.

**Uncertainty note:** I found no hard retention data showing how supply complexity affects churn. The evidence is design case studies, patch rationale and player threads.

---

# PART B — Profit with no pay-to-win

## B1. How Conflict of Nations / Supremacy WW3 makes money, how much, and the criticism

- **Products:** gold packs ($1.99–$119.99), Security Council subscription ($9.99 / 30 days, $14.99 / 60 days), $4.99 starter pack [S10], and large Steam bundles (e.g., 760K gold + 12 months Security Council for $199.99) [S11]. Gold buys morale, speed-ups and enemy morale reduction [S13]. The subscription adds queues, rally points, alliance creation, shared intel and more simultaneous matches [S11]. A creator-code programme pays creators **5% of webshop purchases** [S33], which shows the company pushes **web-shop sales** (lower fees than Google Play).
- **Revenue (Sensor Tower, US only, mobile):**
  - Q4 2023 (unified): weekly revenue grew to **~$417K** in the week of 25 Dec. Weekly actives went from 52K to ~78K [S5].
  - Q1 2025 (unified): stabilised around **$186K/week** [S6].
  - Q2 2025 (iOS): rose to **$221K/week**, with ~64K active users [S7].
  - That implies about **$10–22M a year from US mobile alone** [UNCERTAIN: my extrapolation from weekly snapshots].
- **Franchise:** Stillfront reports Supremacy net revenue of SEK 214M in Q2 2026 (−2% organic), **SEK 894M over the last 12 months**, and SEK 880M in FY2025 [S3]. Supremacy drove the return to organic growth in Stillfront's Europe business area in Q3 2025 [S4]. Stillfront lists MENA among its main markets [S1][S3].
- AppGoblin's estimate of "$10K+ monthly, 128K MAU" for the Google Play app [S12] conflicts strongly with Sensor Tower and Stillfront figures. **[UNCERTAIN: treat as unreliable.]**
- **The P2W criticism** (see A1): gold changes match outcomes. Whales spend "thousands on a single match". New players are attacked by gold buyers on days 4–7. Gold-free play is gated at Rank 25. The developer's defence: "without our monetisation, we cannot offer a free game of this caliber" [S8].

## B2. Fair monetisation models that earn well

| Model | Example and figures | Lesson for us |
|---|---|---|
| **Season / battle pass** | Clash of Clans Gold Pass (2019): **+58% spending in its first 30 days**; Apr–Dec 2019 revenue +32% ($453M → $597M); 2019 total $727M (+27% YoY), the first growth since 2015 (Sensor Tower) [S27]. Clash Royale Pass Royale: weekly revenue reportedly **+178%** [S28, UNCERTAIN: headline only]. Passes appear in ~60% of the top-20% grossing mobile games (GameRefinery 2022) [S50]. In 4X, passes "aren't the biggest revenue source but raise LTV", typical prices €5 or €21 [S44]. Brawl Pass about €11.99, and each pass pays back Gems worth half of the next one [S51]. | Pass = the most reliable fair product. Put only cosmetics and cosmetic currency in it. Partial refund in soft currency keeps players subscribed. |
| **Cosmetics** | Fortnite **$5.8B (2018) + $3.7B (2019) = $9.1B** (Epic, court documents) [S29]. Brawl Stars removed loot boxes (Dec 2022) and saw a temporary spike, with a simpler core loop [S51]. Brawl Stars is about $1.4B lifetime (data.ai, via Naavik) [S51]. | Military cosmetics (camo, unit skins, HQ looks, flags) fit the theme naturally. |
| **Non-consumable content and premium factions** | Polytopia: 4 of 16 tribes free, others paid, plus tribe skins. "Only non-consumables, no in-game currency". 20M+ downloads, 600–700K MAU after 8.5 years. The CEO admits lifetime value per player is "much lower" than top F2P games [S31]. | Trust and longevity come at the cost of a lower ceiling. Mix this with a pass and a subscription for recurring revenue. |
| **Convenience / insight subscription** | Chess.com: 150M members and **$100M+ revenue**. Premium gives no ads, unlimited lessons and analysis. The author estimates **~1–1.5% of users pay** [S49, UNCERTAIN: estimate]. | Sell learning, statistics, extra match slots and identity, never in-match power. |
| **Cosmetics plus storage/convenience (PC)** | Path of Exile / GGG: net profit about €95.3M for a 15-month FY2025, mostly from Path of Exile 2's paid early access. Ongoing sales are cosmetics and stash tabs [S52]. | A paid "Founder / Early Access" supporter pack at launch works for fair games. |
| **Ethics as brand** | Warframe removed an "insanely profitable" pet re-roll that worked like "a slot machine" [S53]. | Avoid randomised paid items entirely. |
| **Marvel Snap** | $50M in its first months (AppMagic) [S35]. Headlines: more than $116M in the first year on mobile, and "$275M+" by the second anniversary [S54, UNCERTAIN: headline only]. | Pass plus cosmetics can scale (though Snap also sells card progression). |
| **League of Legends** | [NOT FOUND] No reliable official revenue figure (only blogs). Known model: champions earnable for free, skins paid. | — |

**What counts as P2W, a rule we can write into the design doc:**
> "If two players of equal skill and equal play time meet in a match, nothing either of them bought may change who is more likely to win."

- **Forbidden:** resources, speed-ups, units, morale, intel or vision, protection, extra build slots, research time, and **automation that non-payers do not get** (queues, rally points). The rival's subscription crosses this line [S11].
- **Allowed:** cosmetics, identity, statistics and replays, more *simultaneous* matches, hosting private matches, a cosmetic pass, gifting, coalition cosmetics, early access to *cosmetic* seasons.
- **Grey zone to avoid:** paid name changes mid-match, paid "re-roll start", paid matchmaking advantages, paid "unit unlocks" in ranked play.

## B3. MENA market specifics

**Size and spending**
- MENA-3 (Saudi Arabia, UAE, Egypt): **$2.0B in 2024** (+4%), forecast $2.7–2.9B by 2028–29. 70.3M players, 94% play on mobile (Niko/Xsolla) [S17][S55].
- Revenue split 2024: Saudi Arabia 59.1%, UAE 33.7%, Egypt 7.2%. **ARPU** (per player, not per payer): Saudi $54.89, UAE $84.60, Egypt $3.39 (Niko via GGA) [S16].
- 63.4% of respondents have spent money on games [S17]. **ARPPU (per payer) by country: [NOT FOUND]**.
- GCC 2023: $2.24B, 33.7M players, ARPU $66.34. Saudi Arabia has 49.5% of revenue and 61.7% of players. Forecast $3.24B by 2028 (Niko and the Saudi Esports Federation) [S18].
- Middle East player spending in 2024: $1.2B (+18%). **Strategy was #1 by revenue and grew +38%** (Sensor Tower at Dubai GameExpo) [S19]. MENA H1 2024: strategy held **22.46% of Google Play top-grossing revenue** (#1) and 13.94% on iOS (#2). Whiteout Survival was the #3 grossing game in the region (Apptica) [S20].
- Strategy takes 25% of global mobile game revenue and was the only genre growing in revenue, downloads and time spent (Sensor Tower via PocketGamer.biz) [S38].
- **Kuwait and Jordan:** [NOT FOUND] No reliable country spend or ARPPU figures. Kuwait's downloads grew +12% in H1 2024 [S20].

**Payments**
- Saudi Arabia: credit card penetration 25.4%, **mada 93%**, PayPal 52% [S17]. Google Play carrier billing works with Mobily, STC, Zain and Virgin, and Google Pay has run on mada since Sep 2025. UAE carrier billing: du and Etisalat (carrier caps may apply). Egypt: Vodafone, e&, Meeza, InstaPay [S16].
- GCC payment methods: credit card 61.2%, digital wallet 54.5%, debit 53.6%, **gift / top-up cards 41.7%**, cash 29.9%, phone bill 20.8% [S18].
- **53% have bought from game web shops**. Reasons: faster (40.7%), familiar payment (37%), extra rewards (35.9%), discounts (34%) [S17]. The rival already runs a web shop with creator codes [S33].

**Localisation**
- 40.9% of Gulf players call Arabic localisation important, and **75% say seeing Arab culture in games is important** [S18].
- 57% would consider quitting a game with content they find religiously or culturally offensive [S56].
- **Implications:** full Arabic UI and voice, right-to-left layout, Arabic store page. Arab military cosmetics (regional camo patterns, regional landmark HQ skins). Careful handling of borders and religious symbols on the real-world map [ASSUMPTION: border depiction is a known sensitivity, no specific source fetched].

**Ramadan and Eid**
- Gaming installs **+24% during Ramadan and +27% around Eid al-Fitr** compared with the 2025 average (Adjust) [S22].
- Middle East in-app revenue during Ramadan 2025: $1.70B across all app categories (+18.6% YoY). Gaming sessions were flat. The gaming IAP figure of "3.26%" is unclear (AppsFlyer) [S21, UNCERTAIN].
- Activity moves late: peaks after iftar and through the night. Revenue and DAU spike during Ramadan, and the 3 days of Eid are a strong sales window (Tamatem) [S23, older 2017 source].
- **Action:** a Ramadan season with lantern map theme and Eid bundles, push timing moved to the evening, and possibly shorter real-time days in Ramadan matches. Also plan National Days: Saudi National Day 23 Sep, UAE 2 Dec, Kuwait 25 Feb [dates are general knowledge].

**Pricing localisation**
- Set native SAR, AED and EGP price tiers rather than converting from USD. Egypt needs much cheaper entry offers. Keep low starter packs that fit inside carrier-billing caps [S16, advice, unsourced].
- 43.9% say low prices would make them start spending [S17]. SAR is pegged at 3.75 per USD.
- Gulf consumer prices include VAT (Saudi Arabia 15%, UAE 5%), so net revenue is below list price [UNCERTAIN: check who remits VAT under Google Play for each country].

## B4. Google Play fees, legal and policy points

- **Service fee (outside AU/EEA/JP/UK/US):** 15% on the first $1M of annual earnings for developers enrolled in the 15% tier, 30% above that. **Auto-renewing subscriptions: 15%** regardless of revenue [S24].
- **AU/EEA/JP/UK/US:** a new structure is rolling out from **30 Jun 2026** (EEA, UK, US) and 30 Sep 2026 (AU, JP). Subscriptions 10% + 5% billing fee. Other transactions 20% + 5% for new installs. First $1M: 10% + 5% [S24]. **Enrol in the 15% tier on day one.**
- **Loot boxes:** Google Play requires that apps offering randomised virtual items from a purchase "must clearly disclose the odds of receiving those items in advance of purchase" (since 2019) [S25]. Europe is moving towards a loot box crackdown in 2026 [S57, UNCERTAIN: headline only]. Gambling (maysir) is also a religious sensitivity in the Gulf. **Recommendation: sell no randomised items for money. Anything random must be free, with odds shown.**
- **Age rating (Saudi Arabia / UAE):** Saudi Arabia has used its own age ratings since 2016 (now the General Authority for Media Regulation, GAMR). It added a 21+ tier in 2025 (GTA V). Games with strong violence, sexual content, drugs or culturally offensive themes were historically banned or required edits [S56].
- **Chat and moderation (Saudi):** in Sep 2025 Roblox, under a binding agreement with GAMR, blocked over 300,000 experiences, **disabled text and voice chat in the Kingdom**, and reportedly agreed to hire Arabic moderators [S26]. A 60-player diplomacy game lives on chat, so plan for Arabic moderation, profanity filters, block/report, and age-aware chat settings from day one. The rival's reviewers also complain about toxic messages [S10].
- **Play policies to follow** [UNCERTAIN: from general knowledge of the Play policy centre; I could not fetch the current text]:
  - Subscriptions must clearly show price, renewal period, trial terms and how to cancel.
  - Ads must not be unexpected full-screen interruptions or disguised. Rewarded ads must be opt-in.
  - If the game appeals to children, the Families policy and certified ad SDKs apply.
  - Use Google Play Billing for in-app digital goods (web shops follow their own country rules).

## B5. Recommended monetisation plan

**Principle:** sell **identity, convenience between matches, and support**, never power inside a match. Make all of the rival's paywalled QoL (queues, rally points, alliance creation, shared intel) free. That is the headline message: "everything the competitor charges for is free here".

Prices: USD and suggested SAR store tier (SAR ≈ USD × 3.75, rounded to a .99 price point). Egypt gets its own lower tiers.

| # | Product | Price | What it gives | Why it is not P2W |
|---|---|---|---|---|
| 1 | **Rookie Bundle** (one-time, first 7 days) | $0.99 / SAR 3.99 | A camo set, profile frame, 300 Medals (cosmetic currency) | Cosmetic only. Low price fits carrier-billing caps and converts first-time payers. |
| 2 | **Founder / Supporter Pack** (launch year only) | $9.99 / SAR 37.99 | "Founder" title, gold name plate, 3 unit skins, 1 map theme, coalition banner, credit in the game | Cosmetic and recognition. Follows the Path of Exile-style supporter / early-access pattern [S52]. |
| 3 | **Commander Pass** (season of ~30 days, about 2 matches) | Free track + Premium $4.99 / SAR 18.99 | About 50 tiers: skins, emotes, frames, Medals. Premium returns ~50% of its price in Medals if finished | Cosmetics only. Follows the CoC Gold Pass result [S27] and the Brawl Pass refund loop [S51]. |
| 4 | **Commander Pass Elite** | $9.99 / SAR 37.99 | Premium pass + 10 tier skips + an exclusive animated unit skin | Tier skips unlock cosmetics only. |
| 5 | **Command Staff subscription** (auto-renew, monthly) | $4.99 / SAR 18.99 (yearly $39.99 / SAR 149.99) | 5 simultaneous matches instead of 2, full career statistics, match replays and the spectator "war room", 2 private-match host tickets a month, a monthly cosmetic, profile badge, cosmetic-only XP bonus | More matches and better analytics do not change any single match. All in-match QoL stays free. The 15% subscription fee helps margin [S24]. |
| 6 | **Unit skins** (by unit class or full army sets) | $1.99–$4.99 / SAR 7.99–18.99 | Desert, urban, digital, regional camo patterns. Veteran unit models | Same stats and same silhouette size. Units stay readable to enemies. |
| 7 | **HQ and capital looks** | $2.99–$5.99 / SAR 11.99–22.99 | Capital and city building styles (Gulf, Levant, Nile, modern glass) | Visual only. |
| 8 | **Map themes** | $2.99–$5.99 / SAR 11.99–22.99 | Night ops, satellite, paper war-room, Ramadan lanterns | Client-side visual. Must not hide information (readability rules). |
| 9 | **Flags, emblems, name colours, frames, titles** | $0.99–$2.99 / SAR 3.99–11.99 (flag editor unlock $2.99) | Custom nation flag, emblem packs, coloured name in chat and the diplomacy screen | Identity. Matters a lot in a 60-player diplomacy game. |
| 10 | **Diplomacy emotes and voice lines** (Arabic and English) | $0.99–$2.99 / SAR 3.99–11.99 | Stickers, animated signatures for treaties, war-declaration animations | Social and fun. Chat is moderated. |
| 11 | **Coalition cosmetics** | $4.99–$14.99 / SAR 18.99–54.99 (crowdfundable by members) | Coalition banner, shared border pattern, coalition HQ skin, coalition victory monument | Group identity. Follows the 4X guild-gift pattern [S44]. |
| 12 | **Gifting** | Any pass or skin | Buy a pass or skin for a friend or coalition member (Eid gifting) | Cosmetic. Social, and fits Eid customs. |
| 13 | **Private Match Host Ticket** | $1.99 / SAR 7.99 each (2 a month included in Command Staff) | Host a private 10–60 player match with custom map region, speed and rules (no AI, no navy, etc.) | Everyone inside is equal. No cash prizes, which avoids gambling law. |
| 14 | **Seasonal bundles** (Ramadan, Eid al-Fitr, Eid al-Adha, Saudi/UAE/Kuwait national days) | $2.99–$9.99 / SAR 11.99–37.99 | Themed skins, map theme, frame | Cosmetic. Uses the Ramadan and Eid demand spikes [S22][S23]. |
| 15 | **Medals (cosmetic currency) packs** | $0.99–$49.99 / SAR 3.99–184.99 | Direct-price currency for the cosmetic shop. Fixed prices, nothing random | Cosmetic only. Show the real-money price beside every item (Polytopia's transparency point [S31]). |
| + | **Rewarded ads** (opt-in, max ~5 a day) | — | Watch to get Medals, extra pass XP, or double end-of-match cosmetic reward | Never resources, speed-ups or anything inside a match. No forced interstitials. |
| + | **Web shop** (Phase 2) | Same items, +10% bonus Medals | Lower fees, local payment methods (mada, wallets, InstaPay) | Same cosmetic items. 53% of MENA-3 players already buy in web shops [S17]. Check local tax and consumer law. |

**Never sell:** gold-style speed-ups, morale, units, resources, research, intel or vision, peace protection, paid revive or re-roll, randomised paid crates.

### Revenue estimate model

Formula:
- MAU = DAU ÷ 0.20 (the Stillfront portfolio ratio [S3])
- Monthly IAP = MAU × monthly payer conversion × monthly ARPPU
- Ads = DAU × ad ARPDAU × 30
- Gross = IAP + Ads
- Net ≈ Gross × (1 − store fee) × (1 − VAT share). Store fee: 15% on the first $1M a year and on subscriptions, 30% on IAP above $1M.

| Input | Low | Mid | High | Basis |
|---|---|---|---|---|
| Average DAU (year 1) | 10,000 | 50,000 | 200,000 | [ASSUMPTION]. For scale: the rival had ~52–78K weekly actives in the US alone (Q4 2023) [S5]. |
| MAU (DAU / 0.2) | 50,000 | 250,000 | 1,000,000 | [S3] ratio |
| Monthly payer conversion | 1.5% | 3.0% | 4.5% | [ASSUMPTION]. Chess.com is estimated at ~1–1.5%; freemium "often 2–5%" [S49]. Fair models convert more casual buyers but fewer whales. |
| Monthly ARPPU | $8 | $12 | $15 | [ASSUMPTION]. Pass $4.99–9.99 + subscription $4.99 + occasional cosmetics. Gulf ARPU is high ($55–85 a year per player) [S16]. No whales by design. |
| Ad ARPDAU (rewarded, opt-in) | $0.005 | $0.010 | $0.015 | [ASSUMPTION]. No sourced MENA strategy eCPM found [NOT FOUND]. |
| **Monthly IAP** | $6,000 | $90,000 | $675,000 | calculated |
| **Monthly ads** | $1,500 | $15,000 | $90,000 | calculated |
| **Monthly gross** | **$7,500** | **$105,000** | **$765,000** | calculated |
| **Yearly gross** | **~$90K** | **~$1.26M** | **~$9.2M** | calculated |
| Implied ARPDAU | $0.025 | $0.07 | $0.13 | Compare: Stillfront ~$0.21–0.23; Whiteout $1.08 [S3][S15]. Ours is lower because there are no whales. |
| Rough net after store fees (before VAT) | ~$77K | ~$1.0M | ~$6.8M | 15% on the first $1M and on subscriptions, 30% on IAP above that [ASSUMPTION: ~25% of IAP is subscription] |

**Sensitivities and caveats**
- Revenue scales linearly with DAU. DAU depends on UA spend and retention (A3).
- Each +1 point of payer conversion in the mid case adds about $30K a month.
- The high case is roughly the size of the rival's **US-mobile-only** revenue [S5–S7] and far below the Supremacy franchise's ~$85–95M a year [S3].
- UA costs are **not** included. MENA game CPI rose about 15% in 2025 (Adjust via [S16]). A real 4X/strategy CPI benchmark: [NOT FOUND] [S15].
- **Risk:** a no-whale model caps lifetime value (Polytopia's CEO admits this [S31]). Recurring products (pass + subscription) and high retention have to carry the business.
- **Upside:** "No pay-to-win" is a strong differentiator against a rival whose reviews focus on P2W, and cheaper retention may offset the lower ARPPU.

**Launch sequence**
1. Soft launch in Jordan or Egypt to test onboarding cheaply (Egypt has 43% of MENA installs [S20]).
2. Then Saudi Arabia, UAE and Kuwait, timed to open about 3–4 weeks before Ramadan.
3. Founder Pack only in the first year.
4. Commander Pass from season 1. Command Staff subscription from month 2. Web shop in Phase 2.

---

## Sources

S1. Game Developer (press release), "Three Games, Two Studios, One Franchise — Over 90 Million Players Combined: Introducing the Supremacy Franchise" (Apr 2025) — https://www.gamedeveloper.com/press-release/three-games-two-studios-one-franchise-over-90-million-players-combined-introducing-the-supremacy-franchise
S2. PocketGamer.biz, "Stillfront's Dorado Games and Bytro Labs join forces to launch the Supremacy franchise" — https://www.pocketgamer.biz/stillfronts-dorado-games-and-bytro-labs-join-forces-to-launch-the-supremacy-franchise
S3. Stillfront, Interim Report Q2 2026 (PDF) — https://storage.mfn.se/3dd9c6e4-fa13-4a0a-9402-25e3113bcd94/report-interim-report-q2-2026.pdf
S4. Stillfront, Quarterly Report Q3 2025 (PDF) — https://storage.mfn.se/bc539ad4-c081-454d-ab0d-702d84c462e2/stillfront-quarterly-report-q3-2025.pdf
S5. Sensor Tower, "Q4 2023 Unified Top 5 Military Games Revenue US" — https://sensortower.com/blog/2023-q4-unified-top-5-military%20games-revenue-us-600f8d2b241bc16eb89ce40d
S6. Sensor Tower, "Q1 2025 Unified Top 5 Military Games Revenue US" — https://sensortower.com/blog/2025-q1-unified-top-5-military%20games-revenue-us-600f8d2b241bc16eb89ce40d
S7. Sensor Tower, "Q2 2025 iOS Top 5 Military Games Revenue US" — https://sensortower.com/blog/2025-q2-ios-top-5-military%20games-revenue-us-600f8d2b241bc16eb89ce40d
S8. Steam Community, Supremacy: World War 3 discussion (2019–2020, pay-to-win / new players thread) — https://steamcommunity.com/app/784950/discussions/0/2952595757881235764
S9. Steam Community, Supremacy: World War 3 discussion (2022–2024, "entirely pay to win" thread) — https://steamcommunity.com/app/784950/discussions/0/3488626756876088876
S10. Apple App Store, Supremacy: World War 3 (US listing, IAP prices and reviews) — https://apps.apple.com/us/app/id1510997559?l=en-us
S11. Steam, "SUPREMACY: WORLD WAR 3 – Army Pack" (Security Council benefits) — https://store.steampowered.com/app/800222
S12. AppGoblin, Supremacy: World War 3 (Google Play stats) — https://appgoblin.info/apps/com.doradogames.conflictnations.worldwar3
S13. Bytro Help Center, "What is Gold currency?" — https://bytro.helpshift.com/hc/en/6-conflict-of-nations/faq/104-what-is-gold-currency/
S14. Segwise, "Mobile Game User Retention 2026: Benchmarks by Genre" (citing Mistplay) — https://segwise.ai/blog/mobile-gaming-app-user-retention-strategies
S15. GameGrowthAdvisor, "Strategy/4X mobile game growth & monetization 2026" (citing Naavik, Sensor Tower, Liftoff) — https://gamegrowthadvisor.com/blog/2026-08-25-strategy-4x-mobile-game-growth-monetization-2026/
S16. GameGrowthAdvisor, "MENA gaming market entry guide 2026" (citing Niko Partners, Adjust, Google Play Help) — https://gamegrowthadvisor.com/blog/2026-05-28-mena-gaming-market-entry-guide-2026/
S17. Game Dev Reports, "Xsolla & Niko Partners: MENA-3 Market Research" — https://gamedevreports.substack.com/p/xsolla-and-niko-partners-mena-3-market
S18. Game Dev Reports, "Niko Partners & Saudi Esports Federation: Gulf Countries Market, User Preferences, and Localization" — https://gamedevreports.substack.com/p/niko-partners-and-saudi-esports-federation
S19. PocketGamer.biz, "Middle East fastest-growing market for game revenue and downloads in 2024" (Sensor Tower) — https://www.pocketgamer.biz/middle-east-fastest-growing-market-for-game-revenue-and-downloads-in-2024
S20. PocketGamer.biz, "MENA market hits 7.9 billion downloads and $1.78 billion revenue in H1 2024" (Apptica) — https://www.pocketgamer.biz/mena-market-hits-79-billion-downloads-and-178-billion-revenue-in-h1-2024
S21. AppsFlyer newsroom, Ramadan app revenue 2025 — https://www.appsflyer.com/company/newsroom/pr/ramadan-app-revenue/
S22. Adjust, "Ramadan app trends" — https://www.adjust.com/blog/ramadan-app-trends/
S23. PocketGamer.biz (Tamatem), "What makes Ramadan the hottest month for mobile games in the MENA" (2017) — https://www.pocketgamer.biz/what-makes-ramadan-the-hottest-month-for-mobile-games-in-the-mena
S24. Google Play Console Help, "Service fees" — https://support.google.com/googleplay/android-developer/answer/112622?hl=en
S25. Fenwick, "Google Play Now Requires Disclosure of Loot Box Odds" (2019) — https://fenwick.com/insights/publications/google-play-now-requires-disclosure-of-loot-box-odds
S26. PocketGamer.biz, "Why the Savvy-Roblox deal lands differently in Saudi Arabia" — https://www.pocketgamer.biz/why-the-savvy-roblox-deal-lands-differently-in-saudi-arabia/
S27. Twinfinite, "Clash of Clans enjoys revenue resurgence in 2019 thanks to its battle pass model" (Sensor Tower) — https://twinfinite.net/news/clash-of-clans-enjoys-revenue-resurgence-in-2019-thanks-to-its-battle-pass-model/
S28. WN Hub, "The appearance of the battle pass in Clash Royale increased the weekly revenue of the game by 178%" (headline only) — https://wnhub.io/news/finance/item-15937
S29. PC Gamer, "Fortnite raked in $9.1 billion over two years" — https://pcgamer.com/fortnite-raked-in-dollar91-billion-over-two-years
S30. Mobidictum, Christian Lövstedt (Midjiwan) on Polytopia minimalism — https://mobidictum.com/christian-lovstedt-midjiwan-polytopia-minimalism/
S31. PocketGamer.biz, "Aggressive mobile game monetisation pushes loyal players to churn, says Battle of Polytopia CEO" — https://www.pocketgamer.biz/aggressive-mobile-game-monetisation-pushes-loyal-players-to-churn-says-battle-of-polytopia-ceo
S32. Supremacy forums (Call of War), "The role of Gold: a serious problem" — https://www.playsupremacy.com/en/forums/call-of-war-1942/call-of-war-1942-suggestions-criticism/the-role-of-gold-a-serious-problem-da376358
S33. r/ConflictofNations (mirror, hot posts, 2025) — https://red.ks32.dev/r/ConflictofNations/hot
S34. Conflict of Nations wiki (community), "Campaign Types" — https://conflictnations-wiki.pages.dev/Campaign_Types.html
S35. Mobilegamer.biz, "Second Dinner reveals the secrets of Marvel Snap's onboarding and card design" — https://mobilegamer.biz/second-dinner-reveals-the-secrets-of-marvel-snaps-onboarding-and-card-design/
S36. Game Developer, "Deep Dive: Refreshing the Crusader Kings III tutorial mode through optimized UX" — https://gamedeveloper.com/design/deep-dive-refreshing-the-crusader-kings-iii-tutorial-mode-through-optimized-ux
S37. Game8, "Civilization 7 Tutorial Recommended for Veterans and Newcomers Alike" — https://game8.co/articles/latest/civilization-7-tutorial-recommended-for-veterans-and-newcomers-alike
S38. PocketGamer.biz, "From Game of War to Last Asylum: The evolution of 4X monetisation" — https://www.pocketgamer.biz/from-game-of-war-to-last-asylum-the-evolution-of-4x-monetisation
S39. Udonis, "Rise of Kingdoms analysis" — https://blog.udonis.co/mobile-marketing/mobile-games/rise-of-kingdoms-analysis
S40. Game Developer, "Clash of Clans vs Boom Beach, Part 1: The Hook" — https://www.gamedeveloper.com/business/clash-of-clans-vs-boom-beach-part-1-the-hook
S41. Esports.net, "Does Clash Royale have bots?" — https://www.esports.net/news/mobile-games/does-clash-royale-have-bots/
S42. PocketGamer.biz, "FTUE: Clash Royale" — https://www.pocketgamer.biz/ftue-clash-royale/
S43. GameLuster, "Afterworld Targets a Gentler Start for Paradox Grand Strategy" — https://gameluster.com/afterworld-game-accessibility/
S44. GameRefinery, "What Drives Success in 4X Strategy/SLG Games? Part 2" — https://www.gamerefinery.com/what-drives-success-in-4x-strategy-slg-games-part-2
S45. Gamepressure, "One player on Steam spends 8,000 hours in difficult strategy game…" — https://www.gamepressure.com/newsroom/steam-player-spends-8000-hours-in-difficult-strategy-game-says-fi/z88718
S46. Game Dev Reports, "GameAnalytics: Mobile gaming benchmarks in 2025" — https://gamedevreports.substack.com/p/gameanalytics-mobile-gaming-benchmarks
S47. devtodev, "How To Optimize Your Game Tutorial" — https://www.devtodev.com/resources/articles/how-to-optimize-your-game-tutorial
S48. GameAnalytics, "Tips for a great first-time user experience (FTUE) in F2P games" — https://gameanalytics.com/blog/tips-for-a-great-first-time-user-experience-ftue-in-f2p-games
S49. Sherwood News, "How the Chess.com empire makes more than $100M a year" — https://sherwood.news/culture/how-the-chess-com-empire-makes-more-than-usd100m-a-year/
S50. PocketGamer.biz, "GameRefinery: Battle pass implementation in top grossing mobile games" (2022) — https://www.pocketgamer.biz/gamerefinery-battle-pass-implementation-in-top-grossing-mobile-games/
S51. Naavik, "Brawl Stars deconstruction" — https://naavik.co/deep-dives/brawl-stars-deconstruction/
S52. Mein-MMO, "Developers of Path of Exile 2 reveal how much they have earned…" — https://mein-mmo.de/en/developers-of-path-of-exile-2-reveal-how-much-they-have-earned-have-quadrupled-their-profits,1574405/
S53. Game Informer, "Why Digital Extremes removed an insanely profitable microtransaction from Warframe" — https://gameinformer.com/b/news/archive/2018/03/23/why-digital-extremes-removed-insanely-profitable-microtransaction-from-warframe.aspx
S54. PocketGamer.biz, "Marvel Snap surpasses $275 million as it celebrates second anniversary" (headline only) — https://pocketgamer.biz/marvel-snap-surpasses-275-million-as-it-celebrates-second-anniversary ; Game Dev Reports, "AppMagic: Marvel Snap earned more than $116M on mobile devices in the first year" (headline only) — https://gamedevreports.substack.com/p/appmagic-marvel-snap-earned-more
S55. PocketGamer.biz, "MENA-3 games market set to reach $2.8bn by 2029" — https://www.pocketgamer.biz/mena-3-games-market-set-to-reach-28bn-by-2029
S56. Niko Partners, "Grand Theft Approval: A turning point for MENA game regulations" (Jul 2025) — https://substack.nikopartners.com/p/grand-theft-approval-a-turning-point
S57. Malay Mail, "Europe's crackdown on loot boxes could change gaming for millions of children" (Jul 2026, headline only) — https://www.malaymail.com/news/tech-gadgets/2026/07/05/europes-crackdown-on-loot-boxes-could-change-gaming-for-millions-of-children/226386
S58. PocketGamer.biz, "Supercell revenue declines 4% to $3bn in 2025" — https://www.pocketgamer.biz/supercell-revenue-declines-4-to-3bn-in-2025
S59. PocketGamer.biz, "More than 65% of MENA gaming revenue comes from mobile" (BCG, 2023) — https://www.pocketgamer.biz/more-than-65-of-mena-gaming-revenue-comes-from-mobile
S60. Conflict of Nations wiki (wiki.gg), "Fuel" — https://conflictofnations.wiki.gg/wiki/Fuel
S61. Gamepressure, "Company of Heroes 2: Territory" — https://www.gamepressure.com/companyofheroes2/territory/ze516b
S62. Game Developer, "Design Case Study: Unity of Command" — https://gamedeveloper.com/design/design-case-study-unity-of-command
S63. Steam Community, Hearts of Iron IV discussion on the supply system (May 2022) — https://steamcommunity.com/app/394360/discussions/0/3279194170706938928
S64. EIP Gaming, "How Supply Works in Hearts of Iron IV" — https://staging2.eip.gg/hoi4/guides/heres-how-supply-works-in-hearts-of-iron-iv
S65. AltChar, "Hearts of Iron IV changes the hub to province supply distribution" — https://www.altchar.com/game-news/hearts-of-iron-iv-changes-the-hub-to-province-supply-distribution-assRE3A00KXi
S66. PCGamesN, "Here's your final look at Hearts of Iron 4's new supply system – now with trains" — https://www.pcgamesn.com/hearts-of-iron-iv/supply-trains
S67. Meeple Mountain, "How Wargames Model Logistics" — https://www.meeplemountain.com/articles/how-wargames-model-logistics/
S68. GameDev.net forum, "RTS Issue: Making Supply Graphically Intuitive" — https://www.gamedev.net/forums/topic/478984-rts-issue-making-supply-graphically-intuitive/
