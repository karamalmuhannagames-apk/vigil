# Small Things: gameplay and quality-of-life details from other games

Compiled 12 Nov 2026 for the Vigil design. This is the third file in the research set:
- `con_mechanics.md` covers Conflict of Nations numbers. Nothing from it is repeated here.
- `polish_tips.md` covers presentation polish (sound, haptics, Arabic, labels, juice, generic monetisation). Where an item here builds on a polish tip, it says "extends polish #N" and does not repeat it.
- This file covers **mechanics and QoL rules** taken from other games and from player feedback, each with a source.

**Vigil frame used for the "Vigil take" column** (from the brief and earlier design notes): real world map, up to 60 players, matches last weeks, slowest speed 4x, so **1 game day = 6 real hours and 1 game hour = 15 real minutes**. Ground units fight on a 15-minute tick (12 at max upgrade). Aircraft must return to base to refuel and rearm. Ground units move on a network of lines through cities; aircraft ignore it; ships use a sea network. Coalitions share units and orders. No pay-to-win.

**How to read the source column.** Each key links to the source list at the bottom.
- **R** = the page was opened and read in this session; the detail is taken from it.
- **S** = the page was found by search and its title matches the topic, but it was not read in full. The detail is a well-known mechanic of that game. Check it before quoting it as fact.

The "Vigil take" column is our proposal, not a sourced fact. Every item is small enough to decide in one meeting.

**Totals:** 304 rows in 20 categories, about 275 of them distinct (the rest point to a related row in another category, so each category reads on its own). Then the 40 most valuable at the end. Ten categories have fewer than 15 rows (economy, queues, diplomacy, coalition, accessibility, ergonomics, away play, fairness, retention, performance) because the sources read did not support more; `polish_tips.md` already covers much of accessibility, ergonomics and performance.

---

## 1. Unit orders and queues (O)

| # | Detail | Game | Why players like / hate it | Vigil take | Src |
|---|---|---|---|---|---|
| O1 | **Order chaining**: hold Shift to queue move → attack → move; each runs after the last. | StarCraft II, WARNO | Lets you give a whole plan once instead of babysitting each leg. | "Add leg" button while a stack is selected; up to 8 legs; each leg shows its own arrival clock time. | [sc2-unit], [warno] |
| O2 | **Two move verbs**: plain Move ignores enemies; **Hunt** moves and engages anything spotted on the way. | WARNO | Players can choose between "get there" and "clear the way" without micromanaging. | "Transit" (do not stop, only defend) vs "Advance" (stop and fight on contact). Default: Advance. | [warno] |
| O3 | **Fire stances**: Return Fire only fires when fired upon or spotted. | WARNO | Stops ambushers giving away their position; stops accidental wars. | Three stances per stack: Engage / Return fire / Hold fire. Shown as a small icon on the stack. | [warno] |
| O4 | **Fire stance was a paid feature** ("Fire Control" in High Command) in Bytro games. | Call of War, Supremacy 1914 | Veterans called the build queue and fire control the reason to subscribe; free players felt handicapped. | All stances and queues free for everyone. | [bytro-hc] |
| O5 | **Stance switching exploit closed**: stealth units could escape melee by switching fire-control mode; patched. | Call of War (2026) | Exploits around stance switching feel cheap to the victim. | A stance change takes effect at the next combat tick, never mid-tick. | [cow-2606] |
| O6 | **Unload at position**: a transport drops its passengers at a chosen point, as a queued order. | WARNO | Avoids landing in the wrong place because you were offline. | Amphibious and air-transport orders accept a drop point as a queued leg. | [warno] |
| O7 | **Evacuate**: one key pulls aircraft out of the battle and back to base. | WARNO | Saves planes from a lost fight with one input. | "RTB now" on any air group, plus a global "All air RTB" in the air panel. | [warno] |
| O8 | **Fire on position**: shoot at a point with no visible target. | WARNO | Lets players hit suspected positions under fog. | Artillery and cruise missiles may target a province centre under fog at reduced accuracy (e.g. 50%). | [warno] |
| O9 | **Double-tap a unit selects all visible units of that type.** | WARNO | Fast mass selection without box-drawing. | Double-tap a stack icon selects all stacks of the same main type in view. | [warno] |
| O10 | **Control groups + camera bookmarks** (save camera spot, jump back). Optional "exclusive" groups so a unit is in only one group. | Age of Empires IV | Pros use them constantly; exclusivity stops units being in two groups by mistake. | 6 "Task Force" slots on the bottom bar and 4 map bookmarks (e.g. "Hormuz", "Home"). A stack belongs to one Task Force. | [aoe4-s1] |
| O11 | **Alert**: unit sleeps but wakes when enemies come near. | Civilization VII | No need to re-check idle guards; the game tells you when they matter. | "Sentry" order: the stack holds and sends one alert only when an enemy enters its sight. | [civ7] |
| O12 | **Heal**: unit sleeps until fully healed, then wakes. | Civilization VII | Removes a recurring chore. | "Rest until X% HP, then resume queue" (X = 50/75/100). | [civ7] |
| O13 | **Assemble / Deploy Army**: a commander packs nearby units into one army at no movement cost and unpacks them around itself. | Civilization VII | Moving 6 units as 1 cuts late-game clicks. | An officer can "absorb" adjacent stacks into one army in one tap; "Split back" restores the original stacks. | [civ7] |
| O14 | **Defensive Perimeters**: all nearby land units fortify at once. | Civilization VII | One tap instead of six. | "Dig in all" on a multi-selection. | [civ7] |
| O15 | **Focus Fire**: nearby ranged units all attack the same target. | Civilization VII | Concentrated fire is the main tactic; one order makes it easy. | "Focus" mark on an enemy stack: all your artillery and air in range prioritise it. | [civ7] |
| O16 | **Overrun**: if combined strength is at least 5× the defender, the defender is removed instantly. | Civilization VII | Removes tedious mop-up of hopeless defenders. | If attacker strength ≥ 5× defender, resolve in one tick instead of waiting several 15-min ticks. | [civ7] |
| O17 | **Upgrade All Units** in one action if gold is enough. | Civilization VII | Upgrading one by one was hated busywork. | "Upgrade all in this stack" and "Upgrade all of type X" buttons. | [civ7] |
| O18 | **Battle plans**: draw a front line and an offensive arrow; divisions execute on their own; a planning bonus builds while they wait. | Hearts of Iron IV | Makes 100+ divisions manageable. Players also complain the AI executes plans badly and opaquely. | "Front order" for a Task Force: hold the line between two cities; units auto-fill gaps. Always show *why* a unit is moving (tap → "filling gap at Mosul"). | [hoi4-dd45], [hoi4-bp] |
| O19 | **Fallback line**: units retreat to a pre-drawn line if the front breaks. | Hearts of Iron IV | Gives defensive depth without being online. | Optional "If pushed out, fall back to city X" on any Front order. | [hoi4-dd45] |
| O20 | **One-button retreat**: squad runs home to base, player loses control during it. | Company of Heroes | Keeping veterans alive builds attachment; the risk of losing control is part of the choice. | "Retreat to nearest friendly city" with auto-route; cannot be cancelled for 1 game hour. | [blendo], [coh2] |
| O21 | **Reinforce keeps veterancy** and is cheaper than a new squad, but only near a base, halftrack or upgraded bunker. | Company of Heroes | Rewards preserving units; refill points become targets. | "Refill" a damaged stack in your own city at 60–70% of new-unit cost, keeping XP. | [coh2] |
| O22 | **Hold position**: units do not chase retreating enemies. | StarCraft II | Stops your army being lured out. | Entrenched stacks never pursue; a stack on "Advance" pursues at most 1 link. | [sc2-unit] |
| O23 | **Patrol between points** (not only a circle). | StarCraft II | Covers a border or sea lane. | Naval and air "patrol route" between 2–4 points, alongside the existing circle patrol. | [sc2-micro] |
| O24 | **Rally point for new units**: new troops auto-merge into a chosen army. | Stellaris ("Rally Troops") | No hand-moving every new unit. | Each city has a rally setting: "stay", "go to city X", or "join stack Y". | [stel-295] |
| O25 | **Deploy in orbit / auto-garrison**: troops for a frontier planet stay deployed without manual landing. | Stellaris | Fewer chores. | City setting "garrison new infantry here" up to N units. | [stel-295] |
| O26 | **Weapon release authorization**: how many weapons per target; "one target at a time" vs "all weapons on first target". | Command: Modern Operations | Prevents a strike group wasting all its missiles on the first boat. | Strike setting "salvo per target": 1 / 2 / all. Default 2. | [cmo-107] |
| O27 | **Separate rules for strikers and escorts** in the same package. | Command: Modern Operations | Escorts protect, strikers strike; mixing rules was a common failure. | When an air package has fighters and bombers, each role keeps its own stance. | [cmo-107] |
| O28 | **Radar on only at the attack point**, then off again. | Command: Modern Operations | Hides the strike until the last moment. | Optional "silent approach" for strike aircraft: invisible to radar until 1 link from target, but cannot react to interceptors before that. | [cmo-107] |
| O29 | **Unordered units hold**; all orders resolve simultaneously. | Diplomacy | Nobody loses a unit for forgetting it; units never wander. | A stack with no order is always "Hold & defend", entrenching automatically after 1 game hour. | [dip-rules] |
| O30 | **Support order**: a unit adds strength to another unit's attack without moving. | Diplomacy | Coordinated attacks without exact timing. | "Support" order: an artillery or air stack automatically joins a named friendly stack's attack when that stack engages. | [dip-rules] |
| O31 | **Order budget** (Orders per turn): every move costs an Order, so each turn is "guns and butter". Escalating costs were too hard to compute; doubling was fine. | Old World | Forces real choices and stops "move every unit" tedium. | Never use escalating costs players must compute; if anything costs more, make it exactly double. | [ow-orders] |
| O32 | **Designers resisted adding rules** because each one burdens players; fatigue was added only because unlimited movement broke the game. | Old World | Players prefer few rules that matter. | Every new order type must remove a chore or open a real choice; otherwise cut it. | [ow-orders] |
| O33 | **Players ignored group selection** in testing and used single taps; zooming in to make units bigger was rejected. | Hypemasters (mobile RTS) | Box-select is a PC habit that does not survive on phones. | Tap = select, tap another = add, tap empty map = clear. Box-select hidden behind a button. | [hype] |
| O34 | **Short callsigns** for units that look alike ("boxes on wheels"). | Hypemasters | Players could not tell identical tanks apart. | Auto names like "3rd Armoured (Basra)", editable, shown on the stack label at mid zoom. | [hype] |
| O35 | **Nameplate shows reload progress.** | Hypemasters | Players time their actions to the reload. | A thin ring around each stack fills toward the next 15-min combat tick. | [hype] |
| O36 | **Auto-explore** for scouts. | Civilization VII | Scouting is a chore after the first few turns. | Recon units: "scout this area" inside a drawn box, returning when fuel or HP is low. | [civ7] |
| O37 | **Skip / next unit** cycles units that still need orders. | Civilization VII | Nothing gets forgotten. | "Next idle stack" button with a badge count; idle = no order and not entrenched by choice. | [civ7] |
| O38 | **Reverse**: vehicle backs up to keep its front armour toward the enemy. | WARNO | Small tactical skill that experts love. | Map to a "fighting withdrawal": the stack pulls back at half speed but keeps returning fire, unlike the fast retreat. | [warno] |
| O39 | **Spread out**: grouped units move apart. | WARNO | Reduces splash damage. | "Disperse" order: the stack takes 50% less missile splash but loses its entrench bonus while dispersed. | [warno] |
| O40 | **Shift-queue attack targets** so ranged units fire at them in order. | StarCraft II | Kills priority targets first. | Artillery target list: up to 3 enemy stacks in priority order. | [sc2-unit] |

## 2. Timers and notifications (T)

| # | Detail | Game | Why players like / hate it | Vigil take | Src |
|---|---|---|---|---|---|
| T1 | **Toasts** for low-priority news (build done, system surveyed) appear and vanish on their own. | Stellaris | Keeps the screen clear of modal windows. | Three levels only: toast (vanishes), banner (stays until tapped), alarm (sound + push). | [stel-295] |
| T2 | **Per-message settings**: Ctrl-click any toast to change how it is shown or turn it off. | Stellaris | Players tune noise exactly where it annoys them. | Long-press any toast → "How should I tell you about this?" with the three levels plus Off. | [stel-295] |
| T3 | **Players complained notifications pulse too long or never stop.** | Stellaris | Constant pulsing reads as nagging. | A notification pulses at most 3 times, then sits still. | [stel-pulse] |
| T4 | **State-change notifications for owners** with the timer for the next stage. | EVE Online | Owners can plan a defence days ahead. | Every city state change (under siege, bunker breached, falling) notifies the owner and coalition with the next-stage clock time. | [eve-cit] |
| T5 | **UI time limits**: warn in more than one way before expiry; at least 20 s to extend; adjustable to 10× the default or off. | Xbox Accessibility Guideline 116 | Players with motor or cognitive needs miss short timers. | Proposal, invite and ceasefire offers last at least 1 game day (6 h), with a warning 1 h before expiry. | [xag116] |
| T6 | **Timed on-screen text adjustable** (Halo chat 5–120 s) or kept until dismissed. | XAG 116 (Halo Infinite, Gears 5) | Fast readers and slow readers both served. | Setting: toasts stay 4 s / 8 s / until tapped. | [xag116] |
| T7 | **Push only for useful events** (builds done, fleets arrived); intrusive pushes hurt the experience. | Fishlabs (Galaxy on Fire Alliances) | Players disable all pushes after a few useless ones. | Default-on pushes: under attack, city lost, stack destroyed, coalition request. Everything else off by default. | [fishlabs] |
| T8 | **Queue coverage bar**: shows how much of the 24 h window the skill queue fills. | EVE Online | Tells you at a glance if you will be idle while asleep. | Under every queue: "Covered until 03:10 — then idle". Turns amber when coverage is under 6 h (1 game day). | [eve-queue] |
| T9 | **Inactivity status only updated once a day**, so a player can be gone ~3 days before being marked. | Call of War | Allies cannot tell if a partner is just quiet or gone. | Show "last active: 2 h ago" (rounded) to coalition members in real time. | [cow-inactive] |
| T10 | **Permanent infobox when 3 days of sitter allowance remain.** | Travian | No surprise loss of access. | Any countdown that removes rights (vacation, inactivity, coalition leave) warns at 3 game days and 1 game day. | [travian-sit] |
| T11 | **Vacation ends one hour after you play in a game.** | Warzone | Clear rule; but players forget and lose protection. | If a player acts while on away mode, show "Away mode ends in 60 min — keep it?" instead of a silent rule. | [war-vac] |
| T12 | **Jump to last alert** key; cycling through recent alerts. | StarCraft II | You can react without hunting the map. | Tap a banner to jump; an "alerts" button keeps the last 10 with jump buttons. | [sc2-cam] |
| T13 | **Escalation clock**: DEFCON 5 → 1 on a fixed timetable; nuclear launches only legal at DEFCON 1. | DEFCON | Everyone knows when the deadly phase starts; builds tension. | Nuclear-round mode: a visible world escalation clock; WMDs unlock at a known time for everyone. | [defcon] |
| T14 | **Results visible the moment you return.** | Galactic Reign | The payoff of a decision comes on the next visit. | The first screen after reopening is a 3–5 line result list (extends polish #125). | [galactic] |
| T15 | **Boot time set per game, separate for "direct boot" and "auto boot".** | Warzone | Players know the rules before joining. | Lobby card shows the inactivity rule in plain words: "AI takes over after 2 game days without orders". | [war-boot] |
| T16 | **Fixed 24 h turn timer; expired players are flagged.** | Polytopia | Simple and predictable. | A small hourglass badge on a coalition partner who has given no orders for 1 game day. | [poly-mp] |
| T17 | **Event times that clash with real life**: alliance events start when you wanted to relax. | Last War | Social pressure makes the game feel like a job. | No mandatory fixed-time events. Any timed coalition objective uses a window the coalition picks. | [orcz], [wardawgg] |
| T18 | **"Sleep time" requests**: players of a weeks-long real-time game asked for protection while asleep. | Neptune's Pride | The top pain of long real-time games is losing while asleep. | Personal quiet window (see W2) plus away orders (section 15). | [np-sleep] |
| T19 | **Outsiders see only the current state and its timer**, not the owner's schedule. | EVE Online | Hides defensive planning from enemies. | Enemies see "under siege, 3 h left"; only the owner's coalition sees repair and reinforcement timings. | [eve-cit] |
| T20 | **Missile alerts with time to impact.** | DEFCON | A visible flight gives the defender a moment of counterplay. | Incoming missile: banner with target city and ETA; interceptors in range listed. | [defcon] |

## 3. Combat feedback (C)

| # | Detail | Game | Why players like / hate it | Vigil take | Src |
|---|---|---|---|---|---|
| C1 | **Killmail**: victim, time, place, each attacker's damage, ship and weapon; top damage and final blow highlighted; estimated value. | EVE Online | Players study losses and brag about kills; it is the backbone of the community. | Battle report lists each enemy stack's share of damage, top contributor, and the value lost on each side. | [eve-km] |
| C2 | **Killmails can be shared as a link in chat.** | EVE Online | Coalitions discuss a fight around the same evidence. | "Share to coalition chat" on every battle report; opens the report for everyone in the coalition. | [eve-km] |
| C3 | **"Save fitting" from a killmail.** | EVE Online | Learn from the enemy's build. | On your own loss report: "Rebuild this stack" re-queues the same units in your nearest city. | [eve-km] |
| C4 | **Replays reveal hidden composition**, so even a loss gives intel. | Galactic Reign | Losing still pays something; players come back. | The losing side always sees the attacker's full composition in the report. | [galactic] |
| C5 | **Watchable battle videos** were a core feature. | Galactic Reign | Players share and rewatch fights. | A 10-second map replay of the ticks of any battle from the report. | [galactic] |
| C6 | **Losses feel learnable** because the next match can be played differently. | Galactic Reign | Keeps players returning after a loss. | Every report ends with one plain line: "Main reason: enemy had air cover; you had no AA." (extends polish #144). | [galactic] |
| C7 | **Auto-resolve balance-of-power bar** shown before you commit. | Total War | Players decide whether to fight; complaints arise when the bar and result disagree. | Long-press an enemy stack shows an odds bar without committing; log predicted vs actual (extends polish #9, #148). | [tw-ar] |
| C8 | **Directional cover, firing arcs, and front/rear armour are visible in the world.** | Company of Heroes | "Instantly readable": no hidden numbers. | Province badge shows its modifier in words: "Mountain: defender +25%". | [blendo] |
| C9 | **Status icons**: suppressed flashes yellow, pinned flashes red; cover is shown by dot colour *and* a shield icon. | Company of Heroes | Players see trouble without opening menus; colour is backed by shape. | Max 3 status icons per stack: entrenched, out of supply, retreating, under air attack. Each has a unique shape. | [coh2] |
| C10 | **Unit card shows cumulative buffs and debuffs.** | Age of Empires IV | Players want to see the final number, not guess. | Unit card shows "Final strength 82% = terrain −25% × supply −10% × officer +15%". | [aoe4-s1] |
| C11 | **False effects removed**: a nuke blast animation played even when the bomber was shot down. Patched. | Call of War (2026) | Fake explosions destroy trust in what the map shows. | An impact effect only plays when the strike lands; interceptions get their own "intercepted" effect. | [cow-2606] |
| C12 | **Displayed range must equal real range**: ranged units now hit at the edge of their shown range. | Call of War (2026) | Players feel cheated when the circle lies. | Range circles are drawn from the same number the server uses; unit tests compare them. | [cow-2606] |
| C13 | **Invalid orders silently failed**: planes vanished when sent to patrol beyond range. Patched. | Call of War (2026) | Losing units to a UI bug is the worst feeling. | Out-of-range orders are refused before sending, with "nearest valid point" offered. | [cow-2606] |
| C14 | **Buyout warning**: you are alerted when an opponent can afford to buy you out. | Offworld Trading Company | Gives the threatened player time to react. | "Danger" alert when an enemy stack within 2 links is strong enough to take your city. | [otc-wiki] |
| C15 | **Portrait fills red as damage is taken.** | Hypemasters | Health readable without numbers. | Stack icon has a health ring; below 50% it turns amber, below 25% red, with a shape change for colour-blind safety. | [hype] |
| C16 | **Wounded vs dead split**: hospitals convert some deaths into wounded who can be healed. | Rise of Kingdoms | Losses feel less final; a reason to build hospitals. | Report splits "destroyed" and "damaged, repairable"; a damaged unit that retreats to a city with a hospital is not lost. | [rok-hosp] |
| C17 | **Defence replay and revenge**: see the attack on your base while offline; strike back within 12 h. | Clash of Clans | Turns a loss into a story and a goal. | Offline defence gets a replay; report has "Strike back" that pre-selects your nearest strong stacks. | [coc-2025] |
| C18 | **Persistent battlefield scars** change routes and cover. | Company of Heroes | The map remembers what happened. | Destroyed bridges or rail links stay cut until repaired (extends polish #86 from visual to rule). | [blendo] |
| C19 | **Sober scoring**: DEFCON counts the dead in millions. | DEFCON | The tone makes nuclear use feel heavy. | Nuclear strike reports show civilian losses and the morale effect plainly. | [defcon] |
| C20 | **Combat timer bar per unit** (attack progress). | Call of War / CoN (see con_mechanics) | Already in CoN; players asked for it on all units. | Every stack and every enemy stack in sight shows its next-tick countdown. | [cow-2606] |

## 4. Air, naval and missile handling (A)

| # | Detail | Game | Why players like / hate it | Vigil take | Src |
|---|---|---|---|---|---|
| A1 | **"Winchester"**: after firing all weapons, aircraft turn off radar and head for the egress point automatically. | Command: Modern Operations | No wasted time over the target; realistic. | Strike aircraft with no munitions left RTB at once; their "ready again at" time appears on the base. | [cmo-107] |
| A2 | **Fuel planning**: reserve fuel and maximum strike radius are planned before launch. | Command: Modern Operations | Prevents planes running dry. | When ordering a strike, draw two rings: "can reach" and "can reach and return". Orders past the return ring need a confirm. | [cmo-107] |
| A3 | **Strike force waits in port** and sorties only when an enemy fleet is detected. | Hearts of Iron IV | Works while you are offline. | "Reaction force" order for a fleet or air group: sorties at any enemy entering a chosen zone, returns after. | [hoi4-navy] |
| A4 | **Convoy raiding**: submarines target convoys only. | Hearts of Iron IV | Clear role, avoids subs dying to warships. | Submarine stance "raid trade only": avoids warships, attacks transports and trade ships. | [hoi4-navy] |
| A5 | **Minelaying slows enemy ships**; minesweeping removes mines. | Hearts of Iron IV | Area denial without constant presence. | Mines in a strait: ships passing take damage and slow; supports the owner's "close the strait" idea. Visible to coalition only. | [hoi4-navy] |
| A6 | **50% naval supremacy needed for an invasion.** | Hearts of Iron IV | Landings need preparation; no surprise D-Day from nowhere. | Amphibious landing shows a "sea control" meter for the target zone; under 50% → landing takes double time. | [hoi4-navy] |
| A7 | **Task forces in a fleet share mission regions.** | Hearts of Iron IV | Clear zone ownership. | Naval groups have one assigned sea zone shown as a tinted area. | [hoi4-navy] |
| A8 | **Air missions per air region** (air superiority, close air support, interception). | Hearts of Iron IV | Hundreds of planes managed with a few choices. | "Air cover over region" order: fighters cycle refuel trips automatically to keep the region covered as long as possible. | [hoi4-air] |
| A9 | **Rebase** aircraft to a base or carrier with free slots. | Civilization VII | Slot count visible before moving. | Rebase list shows each base's free slots and distance. | [civ7] |
| A10 | **Temporary forward airbase** set up by an air commander. | Civilization VII | Extends air reach as the front moves. | A "forward strip" province building, quick (1 game day), low HP, can host 2 squadrons. | [civ7] |
| A11 | **Aerial reconnaissance** fully reveals an area for one turn. | Civilization VII | Intel that expires creates rhythm. | Recon flight reveals an area for 1 game hour; then targets become "last seen" ghosts with age. | [civ7] |
| A12 | **Silos switch mode**: air-defence mode or launch mode, not both; launching reveals the silo. | DEFCON | Every launch is a trade-off. | SAM/missile sites: "defend" or "launch" mode; switching takes 1 game hour; a launch reveals the site to the target nation. | [defcon] |
| A13 | **Submarines reveal themselves when launching missiles.** | DEFCON | Stealth has a price. | A ballistic sub that launches is visible to the target for 1 game hour. | [defcon] |
| A14 | **Carriers switch modes** (fighters, bombers, anti-sub). | DEFCON | Simple role choice on one platform. | Carrier mode: "air cover" or "strike"; aircraft follow that mode by default. | [defcon] |
| A15 | **Black-market prices rise with each purchase**, warning rivals. | Offworld Trading Company | Spam of the strongest weapon is self-limiting and visible. | Each WMD built raises the cost of the next by e.g. 20%; a nation's WMD count shows as a vague band ("few/several/many") to all. | [otc-wiki] |
| A16 | **Helicopters change altitude**: low vs high. | WARNO | Simple risk choice. | Keep CoN's low-flying helicopter rule; show it as an icon so players know SAMs ignore them (see con_mechanics). | [warno] |
| A17 | **Doctrine separate from mission**: you set behaviour rules once, missions reuse them. | Command: Modern Operations | Experts set rules once and stop micromanaging. | Per-nation "air doctrine" defaults (salvo size, RTB at % fuel, engage helicopters yes/no) applied to every new squadron. | [cmo-107] |
| A18 | **Patrols must not vanish when ordered out of range.** | Call of War (2026) | Bug lost whole squadrons. | Patrol orders are clipped to the reachable ring with a visible note. | [cow-2606] |

## 5. Logistics and supply (L)

| # | Detail | Game | Why players like / hate it | Vigil take | Src |
|---|---|---|---|---|---|
| L1 | **Supply throughput is capped by the weakest link** on the route. | Hearts of Iron IV | Teaches players where to invest; upgrading a non-bottleneck does nothing. | Tapping a supply line highlights its bottleneck link in amber. | [hoi4-sup] |
| L2 | **Captured rail is inherited at its level, degraded by fighting.** | Hearts of Iron IV | Long advances get harder by themselves. | Captured links work at 50% for 1 game day, then repair. | [hoi4-sup] |
| L3 | **Undersupply hits in stages**: speed first, then organisation, combat, reinforcement, then attrition. | Hearts of Iron IV | Players see trouble coming and can react before units die. | 3 visible stages: amber (−speed), orange (−attack), red (attrition HP loss). | [hoi4-sup] |
| L4 | **Plan offensives around the next usable supply hub**, not the farthest objective. | Hearts of Iron IV | Gives offensives a shape. | Cities act as hubs; the order preview shows "supply OK until Kirkuk". | [hoi4-sup] |
| L5 | **Interdiction**: hitting supply can stop an offensive without a battle. | Hearts of Iron IV | A real role for air and special forces. | Bombing a link degrades it for 1 game day; the defender sees which link was hit. | [hoi4-sup] |
| L6 | **Motorised hubs extend supply but consume vehicles** exposed to attrition. | Hearts of Iron IV | Trade-off rather than free bonus. | "Supply convoy" support unit extends supply 2 links but can be destroyed. | [hoi4-sup] |
| L7 | **Territory cut-off**: resource points only produce when connected to your base through your own territory. | Company of Heroes | Simple and visible: like cutting an electric line. | Provinces cut off from all your cities produce nothing until reconnected; the line network makes this readable. | [coh2], [blendo] |
| L8 | **Attrition outside your borders unless a supply wagon is near.** | Rise of Nations | Deep raids cost something; borders matter. | Stacks more than 3 links beyond your or your coalition's territory lose 1 HP per game day unless a supply unit is with them. | [ron-wagon] |
| L9 | **Out-of-supply artillery reloads at 50–66% speed.** | Rise of Nations | Readable penalty tied to one unit type. | Out-of-supply artillery fires every 30 min instead of 15. | [ron-wagon] |
| L10 | **Each extra supply wagon costs more** (+40 food/timber per wagon, capped). | Rise of Nations | Stops spam of support units. | Support units (supply, radar, officers) get rising cost per copy, capped at 2×. | [ron-wagon] |
| L11 | **Destroying a supply wagon pays a bounty.** | Rise of Nations | Gives raiders a target. | Killing a supply unit gives a small money reward. | [ron-wagon] |
| L12 | **Supply wagons only supply their own nation, not allies.** | Rise of Nations | Keeps allies separate. | Decision needed. Recommendation: coalition members share supply (matches "share all units"). | [ron-wagon] |
| L13 | **Move by rail**: instant travel along the rail network to a connected station. | Civilization VII | Fast redeploy in your own territory feels great. | Built "logistics links" between your own cities give ×2.5 speed (CoN's +150%) and show as a solid line. | [civ7] |
| L14 | **Roads reduce order cost of moving troops**, rewarding linking the front to the core. | Old World | Infrastructure has a clear payoff. | Same as L13: show the time saved in the build preview ("saves 2 h per crossing"). | [ow-orders] |
| L15 | **Reinforcement only near a base, halftrack or upgraded bunker.** | Company of Heroes | Forward refill points matter. | Refill only in own cities or next to a field hospital/supply unit. | [coh2] |

## 6. Economy and trade UX (E)

| # | Detail | Game | Why players like / hate it | Vigil take | Src |
|---|---|---|---|---|---|
| E1 | **Dynamic market**: heavy buying pushes the price up; rivals can build production to profit from the spike. | Offworld Trading Company | The market itself is a battlefield. | World price moves with buy/sell volume; the market tab shows a 7-game-day sparkline. | [otc-wiki] |
| E2 | **Requested: price-triggered auto-sell above a ceiling and auto-buy below a floor.** | Offworld Trading Company (player request) | Players hate dumping whole stockpiles at bad prices. | Standing market orders: "sell 500 oil if price > X", "buy fuel if < Y". Max 5 active. | [otc-sug] |
| E3 | **Requested: futures contracts** (fixed price, future date) with public announcement. | Offworld Trading Company (player request) | Adds planning and bluffing. | Simpler version: recurring deals between players ("200 fuel per game day for 5 days") shown to both coalitions. | [otc-sug] |
| E4 | **Auto-buy when short** for a build. | Offworld Trading Company | One tap instead of four. | "Buy missing and build" button showing total extra cost before confirming. | [otc-auto] |
| E5 | **Market prices visible before you build** production. | Offworld Trading Company | Informed choices. | The building card shows "this city's oil output ≈ N money per game day at today's price". | [otc-prices] |
| E6 | **Goon squad protects one structure** from sabotage. | Offworld Trading Company | Defensive choice with a clear scope. | Counter-intelligence assigned to one city; visible only to the owner. | [otc-wiki] |
| E7 | **Guild help**: members tap to shorten each other's build and research timers. | Rise of Kingdoms and most 4X | Daily social touchpoint; players feel useful. | Coalition "help" on a build: −1% per help, max 10 helps. Only coalition members; counts in farm-detection graph. | [gr-4x] |
| E8 | **Guild currency shop** (earned by helping) buys items such as 12 h shields. | Top 4X games | Rewards cooperation. | Coalition score buys cosmetic coalition banners only, never power. | [gr-4x] |
| E9 | **Marketplace frozen during vacation**: no sending or receiving resources. | Kingdoms (Travian) | Closes a feeding loophole. | Away mode freezes gifts and trades to and from that player. | [kingdoms-vac] |
| E10 | **Troops still eat during vacation**; check food before leaving. | Kingdoms (Travian) | Players were caught out. | Away mode preview: "Upkeep during 2 days away: 4,800 fuel — you have 3,100" with a warning. | [kingdoms-vac] |
| E11 | **Production and tribute frozen during vacation, then doubled for the same length afterwards** (Boost Phase). | Kingdoms (Travian) | Returning players are not punished. | See W10 for away mode; do not add the double boost in a war game (too exploitable). | [kingdoms-vac] |
| E12 | **Buyout race**: alerted when you can be bought out, rivals not alerted about you. | Offworld Trading Company | Asymmetric warnings create tension. | Not used; Vigil warnings are symmetric to avoid confusion. | [otc-wiki] |

## 7. Building and research queues (Q)

| # | Detail | Game | Why players like / hate it | Vigil take | Src |
|---|---|---|---|---|---|
| Q1 | **Skill queue up to 50 items, as long as all start within 24 h.** Devs feared a year-long queue would let players go inactive. | EVE Online | Offline progress without letting accounts run unattended for months. | Research queue holds as many items as fit in the next 2 game days (12 h). Enough for a night's sleep, not a week. | [eve-queue] |
| Q2 | **Reorder by drag; bar shows how much of the window is filled.** | EVE Online | Easy to plan around sleep. | Drag to reorder any queue; coverage bar (see T8). | [eve-queue] |
| Q3 | **Global build queue** HUD: all queued units and upgrades across buildings; click to select, Ctrl-click to cancel. | Age of Empires IV | One place to see everything. | "All production" screen listing every city's queue; long-press an item to cancel or move it. | [aoe4-s1] |
| Q4 | **Queue visibility toggle**: hidden / upgrades only / all. | Age of Empires IV | Keeps the HUD clean. | The production strip can show "units", "buildings", or "all". | [aoe4-s1] |
| Q5 | **Queues build as resources allow** (the High Command queue). | Call of War, Supremacy 1914 | Players called it the most valuable premium feature. | Free. A waiting item shows "waiting for 300 fuel (≈ 2 h at current income)". | [bytro-hc] |
| Q6 | **Build queues and waypoints do not count as activity** for inactivity checks. | Call of War | Stops "zombie" accounts kept alive by long queues. | Same rule, stated openly in the help text. | [cow-inactive] |
| Q7 | **Army builder spreads construction across a sector's planets**; Ctrl-click queues more. | Stellaris | One order fills many factories. | "Build 6 infantry in region" splits across cities with free slots; units meet at the rally point. | [stel-295] |
| Q8 | **Fleet templates with copy button**; Fleet Manager shows 12 fleets instead of 6. | Stellaris | Templates remove repetitive building. | Stack templates ("Armoured Brigade = 3 MBT + 2 Mech + 1 SAM"); "Build template" in one tap; copy and edit. | [stel-295] |
| Q9 | **Fleet manager and designer merged in one sidebar** with tabs. | Stellaris | Fewer places to look. | Production, templates and upgrades live in one panel with tabs. | [stel-295] |
| Q10 | **Upgrade all units at once.** | Civilization VII | No one-by-one chores. | See O17. | [civ7] |
| Q11 | **Merge two identical units into a higher tier.** | Top War | Very easy to learn; casual players love it. | Not used (wrong genre), but the lesson stands: one clear upgrade verb. | [topwar] |
| Q12 | **Vacation freezes troop training.** | Kingdoms (Travian) | Fair: no progress while protected. | Away mode pauses nothing, since it gives no protection (see W10). | [kingdoms-vac] |

## 8. Diplomacy UX (D)

| # | Detail | Game | Why players like / hate it | Vigil take | Src |
|---|---|---|---|---|---|
| D1 | **War exhaustion 0–100%** from occupations, losses and time; a side at 100% cannot reject a status-quo peace. | Stellaris | Ends wars that drag on with no result. | Each side of a war has a war-weariness bar; at 100% for 1 game day, the other side may impose a "keep what you hold" peace. | [stel-93] |
| D2 | **Status quo peace = keep what you hold**, not a white peace. | Stellaris | Fair end to a stalemate. | Same as D1. | [stel-93] |
| D3 | **Fighting for a few border systems wears you down faster than fighting for independence**; more claims → faster exhaustion. | Stellaris | Big war goals have a cost. | Declare war goals (cities) at war start; each extra goal adds +10% weariness speed. | [stel-93] |
| D4 | **Grievances become demands; war support drops; at 0 war support a side must surrender.** | Humankind | War needs a reason; endless wars end. | Diplomatic incidents (border violation, broken treaty) create grievances shown in the diplomacy card; grievances raise your war support. | [hk-griev], [hk-war] |
| D5 | **Concede vote**: if all but one vote concede, the game ends. **Extend vote**: 2/3 can extend a phase by 4 days. | vDiplomacy | Groups can end or pause a game democratically. | Late game: if all remaining players but one coalition vote "concede", that coalition wins. | [vdip] |
| D6 | **Anonymous games**: names hidden. | vDiplomacy | Stops pre-made friends and grudges from outside the game. | Optional ranked mode with hidden player names until the end. | [vdip] |
| D7 | **Reliability rating**: how reliably you enter orders and finish games. | webDiplomacy / vDiplomacy | Players avoid unreliable allies. | Profile shows "finished 9 of 10 matches"; shown on coalition invites. | [vdip], [webdip-rr] |
| D8 | **Gunboat (no-press) variant**: no chat at all. | Diplomacy community | Players who dislike chat or language barriers still play. | "No chat" mode: only structured proposals and pings (works across Arabic/English). | [gunboat] |
| D9 | **Coalitions of neighbours form against fast expanders.** | Europa Universalis IV | Strong anti-snowball; but players still find ways to break out. | AI nations join a "containment pact" against any player above X% of the map. | [acoup], [eu4-dd11] |
| D10 | **Rogue players ignoring non-aggression pacts drive many players away.** | Last War | Broken trust kills servers. | NAPs as formal treaties; breaking one costs morale for 1 game day and shows on the breaker's record (extends polish #156). | [wardawgg] |
| D11 | **Claims cost influence; several claims on the same target strengthen it.** | Stellaris | Allies negotiate who gets what before war. | Coalition members mark which city each wants; conflicts show before the war. | [stel-93] |
| D12 | **Defenders can always pick "Humiliate"** as a war goal. | Stellaris | Defenders get something from winning. | A successful defender gets a prestige and morale bonus. | [stel-93] |

## 9. Coalition tools (K)

| # | Detail | Game | Why players like / hate it | Vigil take | Src |
|---|---|---|---|---|---|
| K1 | **Ping chat can be switched off.** | Age of Empires IV | Spammy teammates are muted without leaving. | Per-member mute for pings. | [aoe4-s1] |
| K2 | **Owners see full timers; outsiders only current state.** | EVE Online | Coalitions plan together; enemies stay blind. | Coalition members see each other's city timers and queues. | [eve-cit] |
| K3 | **Coordinated Attack**: nearby infantry and cavalry attack one target with +2 strength. | Civilization VII | Rewards timing attacks together. | "Joint strike": several members' stacks set to arrive at one clock time; +10% attack if they hit within the same tick. | [civ7] |
| K4 | **Rally / join a rally**: players commit marches to a leader's attack. | Rise of Kingdoms | Core social mechanic in mobile 4X. | "Operations": a leader creates an operation (target + time); members commit stacks; leader sees list and ETAs. | [rok-march] |
| K5 | **Weekly alliance duel** ("co-opetition"). | Last War | Engagement driver; also social pressure to spend. | Optional weekly coalition objectives with cosmetic rewards only. | [naavik] |
| K6 | **Guild gifts** in over 92% of top 4X games, mostly sold as IAP bundles. | Top 4X games | Common; buyers feel generous. | If coalition gifts exist, they are cosmetic only. | [gr-4x] |
| K7 | **Social IAP that unlocks when others reach a target** (Gift Pack Rush). | Top War | Effective pressure; players dislike pressure. | Do not copy. | [topwar] |
| K8 | **Customisable side menu order and hotkeys.** | Stellaris | Players put their own priorities first. | Bottom bar slots are rearrangeable. | [stel-295] |
| K9 | **Battle reports shareable as links** (see C2). | EVE Online | Shared evidence. | See C2. | [eve-km] |
| K10 | **Guild tasks**: members help each other's timers for guild currency. | Top 4X games | Daily social habit. | See E7. | [gr-4x] |
| K11 | **Account sitters**: trusted players manage your account. | Travian | Coalitions survive absences. | See I5 and W8. | [travian-sit] |
| K12 | **Temporarily hand your country to another player.** | vDiplomacy | No abandoned seats. | See I8. | [vdip] |

## 10. Anti-snowball and comeback (S)

| # | Detail | Game | Why players like / hate it | Vigil take | Src |
|---|---|---|---|---|---|
| S1 | **Victory-point drain**: holding most victory points drains the other side; equal holdings stop the drain. | Company of Heroes | Clear, comeback-friendly scoring. | Domination mode: VP flows only from points held more than 1 game day. | [coh2] |
| S2 | **Attrition outside borders** (see L8). | Rise of Nations | Natural brake on runaway expansion. | See L8. | [ron-wagon] |
| S3 | **Escalating cost per extra support unit** (see L10). | Rise of Nations | Brake on spam. | See L10. | [ron-wagon] |
| S4 | **Escalating price for strongest weapons** (see A15). | Offworld Trading Company | Brake on the leader's best tool. | See A15. | [otc-wiki] |
| S5 | **Shield after heavy loss**: 8 h automatic shield if 30%+ of loot is stolen; attacking while shielded does not reduce it. | Clash of Clans | Stops a player being farmed to zero. | Real-time war cannot use invulnerability. Instead: after losing 30% of cities within 1 game day, recruitment speed +50% for 1 game day ("national mobilisation"). | [coc-2025] |
| S6 | **Revenge within 12 h** on whoever took 30%+. | Clash of Clans | Gives losers an immediate goal. | Losing a city to a nation gives +10% attack against that nation's stacks inside your former borders for 2 game days. | [coc-2025] |
| S7 | **Beginner's protection** for new accounts. | Travian / Kingdoms | New players get to learn. | Replacement players who take over an AI nation mid-match get 1 game day of protection from city captures. | [travian-bp], [kingdoms-bp] |
| S8 | **Bashing rule**: limit on attacks against the same target per day. | OGame | Stops farming one victim. | Not for war, but for rewards: no XP or loot from hitting the same AI or inactive nation more than N times per game day. | [ogame-bash] |
| S9 | **Several kinds of advantage** (points, fleet, economy, information) keep matches open. | Galactic Reign | One lead does not decide everything. | Keep VP, economy and intel as separate paths to strength. | [galactic] |
| S10 | **Clear end condition** stops a long one-sided endgame. | Galactic Reign | Nobody wants to grind a decided match. | Concede vote (D5) + VP threshold + hard max length. | [galactic] |
| S11 | **War exhaustion and forced peace** (see D1). | Stellaris | Ends stalemates. | See D1. | [stel-93] |
| S12 | **AI containment coalitions** (see D9). | Europa Universalis IV | Brake on leaders. | See D9. | [acoup] |
| S13 | **Server death spiral** without merges. | Last War | Losers leave, then everyone leaves. | Fixed-length matches end before the spiral; a new match starts fresh. | [wardawgg] |
| S14 | **Small map variant** with shorter travel and fewer neutrals. | Call of War (Smallworld) | Faster, more decisive matches. | Regional maps for 20–30 players as a fast mode. | [cow-2512] |

## 11. AFK and inactive handling (I)

| # | Detail | Game | Why players like / hate it | Vigil take | Src |
|---|---|---|---|---|---|
| I1 | **Inactive after 2–3 days**; status updated once a day; queues, waypoints and just viewing the map do not count. | Call of War | Clear-ish rule; but the daily update hides quitters for days. | Inactive = no real order for 2 game days (12 h). AI takes over at once, not at day change. | [cow-inactive] |
| I2 | **AI at tick 47 if never showed up; after 72 ticks (hours) of inactivity otherwise; 3 missed turns in turn-based.** Creator can reinstate. | Neptune's Pride | Different rules for no-shows and quitters. | No-show by match hour 2 → replaced from a waiting list. Quitter → AI, then offered to a replacement player. | [np-ai] |
| I3 | **Direct boot** (any player may boot after a deadline) vs **auto boot** (system boots). | Warzone | Players like control; groups use direct boot to give friends slack. | System-only. Players cannot remove each other. | [war-boot] |
| I4 | **Vacation**: up to 10 days, 7 per year; protects from boot; ends 1 h after playing; must leave ladders first. | Warzone | Lets people travel without losing games. | Away mode: up to 2 days (8 game days) per match, protects from AI takeover only (not from attack). | [war-vac] |
| I5 | **Sitter allowance**: 14-day bank; +1 per day the owner is active, −1 per day only a sitter is; warning at 3 days. | Travian | Lets friends help without accounts being run entirely by someone else; tightened to fight multi-accounts. | Coalition "deputy" can issue orders for an absent member, drawing from a 2-game-day bank refilled by the owner's own activity. | [travian-sit] |
| I6 | **Vacation activation phase**: 48 h (24 h on speed worlds) during which you can be attacked and cannot attack. | Kingdoms (Travian) | Stops "emergency vacation" to dodge an attack. | Away mode starts 1 game hour after you set it. | [kingdoms-vac] |
| I7 | **Missed orders → civil disorder and the phase is extended** so a replacement can be found; may lock games. | vDiplomacy | Keeps games alive; long locks annoy. | Never pause the world; AI holds the seat until a replacement joins. | [vdip] |
| I8 | **Country switch**: temporarily send your game to another player. | vDiplomacy | Personal emergencies covered. | "Hand to a coalition member" for up to 1 game day, logged. | [vdip] |
| I9 | **Reliability shown on profile** (see D7). | webDiplomacy | Social pressure to finish. | See D7. | [webdip-rr] |
| I10 | **Expired player flagged; others may boot; no auto kick; games stuck if host never starts.** | Polytopia | Stuck games were a common complaint. | Match starts on schedule regardless of any single player. | [poly-mp] |
| I11 | **Requested: a flag for potential AFK players.** | Neptune's Pride | Allies want to know before relying on someone. | Hourglass badge (T16). | [np-afk] |
| I12 | **Eliminated player stayed listed as active.** | Call of War (anecdote) | Misleading player list. | Eliminated → spectator with full-map view (like AoE IV, see N10); removed from the "active" count. | [cow-inactive] |
| I13 | **Account sitting rules** (who may play for whom, for how long). | OGame | Formal rules prevent abuse. | Write the deputy rule (I5) into the game rules page. | [ogame-sit] |
| I14 | **Boot rate counted on profile**; method changed after complaints. | Warzone | Reputation for quitting. | Profile shows "abandoned 1 of 10". | [war-bootrate] |
| I15 | **Anxiety about being offline 8 h and returning to a zeroed base.** | Last War | The top fear in real-time 4X. | Away orders and AI commander (section 15). | [wardawgg] |

## 12. Onboarding without tutorials (N)

| # | Detail | Game | Why players like / hate it | Vigil take | Src |
|---|---|---|---|---|---|
| N1 | **Over 60% of the first 4–5 minutes is a minigame that matches the ads**, then it fades. D30 retention was about half of a rival's, blamed on ad/game mismatch. | Last War | Easy start; but players feel tricked. | The first minutes are the real game, at real scale (extends polish #206). | [naavik] |
| N2 | **Class icons** so players learn one class system, not every unit. | Hypemasters | Faster learning with many units. | Every unit card has one class icon (armour, infantry, artillery, AA, air, naval) used everywhere. | [hype] |
| N3 | **Reduce elements to monitor at once.** | Hypemasters | Overload loses new players. | At match start, show only cities, own stacks and borders; unlock layers as they matter (extends polish #4). | [hype] |
| N4 | **Menus grouped by what the player wants to do** ("I want to do X" vs "I want to know X"), not by system. | Frostpunk (console) | Easier to find actions. | Two main buttons: "Act" (build, move, trade) and "Know" (intel, reports, stats). | [fp-con] |
| N5 | **One button always closes, one always confirms.** | Frostpunk (console) | Muscle memory. | Close is always top-corner X (mirrored in Arabic); confirm always bottom, full width. | [fp-con] |
| N6 | **UI reworked after beta feedback because the game is already demanding.** | Frostpunk 2 | Complex games need the simplest UI. | Budget a full UI pass after the first external playtest. | [fp2-ui] |
| N7 | **Easy to learn, rewards strategic use.** | Supremacy 1914 (reviews) | The genre's appeal when done right. | Target: rules a newcomer gets in one match; depth from combinations. | [gb-s1914] |
| N8 | **Explore the full map after elimination or game end; fog revealed to eliminated players.** | Age of Empires IV | Players learn what they missed. | End-of-match and eliminated players see the whole map and a time-lapse. | [aoe4-s1] |
| N9 | **Losses feel learnable** (see C6). | Galactic Reign | Keeps learners. | See C6. | [galactic] |
| N10 | **Tapping an object opens its menu directly.** | Fishlabs | No hunting through menus. | Tap city → city card; tap stack → stack card; long-press → radial. | [fishlabs] |
| N11 | **Resist adding rules** (see O32). | Old World | Each rule is a learning cost. | See O32. | [ow-orders] |
| N12 | **Small map with fewer neutral distractions** for faster play. | Call of War (Smallworld) | Good first map. | First-match map: regional, 10–15 players, 4x. | [cow-2512] |
| N13 | **Merge mechanic as an easy on-ramp.** | Top War | Lowers the barrier for casual players. | One-verb upgrades (O17) serve the same purpose. | [topwar] |
| N14 | **15-unit cap and 15-minute sessions** chosen to fit mobile. | Hypemasters | Sized for phones. | First match: few units, first session goal reachable in 15 minutes. | [hype] |

## 13. Accessibility (X)

| # | Detail | Game | Why players like / hate it | Vigil take | Src |
|---|---|---|---|---|---|
| X1 | **Time limits only when essential; can be extended or switched off; warnings before expiry.** | XAG 116 | Inclusive by default. | See T5. | [xag116] |
| X2 | **On-screen text duration adjustable up to 10× or until dismissed.** | XAG 116 | Slow readers and dyslexic players. | See T6. | [xag116] |
| X3 | **UI narration and a Strong Contrast mode.** | Age of Empires IV | Low-vision players can play. | High-contrast mode for map labels and borders; screen-reader labels on all buttons. | [aoe4-s1] |
| X4 | **Left-thumb use is a third of one-handed use** (33% left, 67% right). | Hoober study | Left-handers get a cramped UI. | "Left-hand layout" setting mirrors the action bar (separate from Arabic RTL). | [hoober] |
| X5 | **Users change grip every few seconds; don't put dangerous actions where a grip shift is needed.** | Hoober study | Mis-taps during grip changes. | Destructive actions (disband, nuke, leave coalition) never sit in a corner; always need a hold-to-confirm. | [hoober] |
| X6 | **Fingers hide labels under the touch point.** | Hoober study | Players can't read what they're pressing. | Tooltips and drag readouts appear above the finger, offset 60 dp. | [hoober] |
| X7 | **Audio cues need a visual equivalent** (subtitles, visual indicators). | XAG 105 | Deaf and muted-phone players. | Every alert sound has an icon and banner. | [xag105] |
| X8 | **Input: remappable controls, hold vs toggle options.** | XAG 107 | Motor accessibility. | Long-press duration setting (300/500/800 ms); no required multi-finger gestures except pinch, which has button alternatives. | [xag107] |
| X9 | **Redundant encoding**: cover shown by dot colour *and* a shield icon. | Company of Heroes | Colour-blind players. | Every colour-coded state also has a shape (extends polish #20). | [coh2] |
| X10 | **One-finger zoom**: double-tap, hold, drag up/down. | Google Maps | One-handed and motor-impaired users can zoom. | Support it on the war map; also a zoom slider option. | [gmaps] |
| X11 | **Ping chat toggle.** | Age of Empires IV | Sensory overload control. | See K1. | [aoe4-s1] |
| X12 | **Callsigns plus class icon** make identification independent of colour. | Hypemasters | Colour-blind safe. | See O34, N2. | [hype] |

## 14. Phone ergonomics (P)

| # | Detail | Game | Why players like / hate it | Vigil take | Src |
|---|---|---|---|---|---|
| P1 | **Grips when touching**: one-handed 49%, cradled 36%, two-handed 15%. | Hoober study (1,333 observations) | Most use is one thumb. | Core map actions reachable by one thumb in the bottom 40% of the screen. | [hoober] |
| P2 | **Two-handed use is 90% portrait.** | Hoober study | Even two-handed players often stay in portrait. | Support portrait for checking and quick orders (extends polish #53). | [hoober] |
| P3 | **Test prototypes in the hand**, in each likely grip. | Hoober study | Desk testing misses reach problems. | Every UI review includes a one-handed test on a 6.7" and a 5.8" phone. | [hoober] |
| P4 | **Map gestures set**: double-tap zoom in, two-finger tap zoom out, rotate, pitch, quick zoom. | Mapbox SDK | Players already know these from map apps. | Enable double-tap in, two-finger-tap out, one-finger quick zoom. Disable rotate and pitch by default (north always up). | [mapbox] |
| P5 | **Camera snapping** (three separate snapping mechanics) makes a big difference. | Frostpunk (console) | Imprecise input feels precise. | Order lines snap to the nearest city, stack or sea node within 40 dp. | [fp-con] |
| P6 | **Two radial menus**: one for global actions, one for context actions. | Frostpunk (console) | Less hunting. | Long-press empty map = global radial (build, market, intel); long-press a unit = order radial (extends polish #39). | [fp-con] |
| P7 | **No precise aiming or fast reactions** needed. | Fishlabs | Strategy fits touch when it avoids twitch input. | No action needs a fast tap; every order can be planned and confirmed. | [fishlabs] |
| P8 | **Every decision of a turn fits in 5–10 minutes.** | Galactic Reign | Fits a commute or a break. | A full check-in (read report, set orders) takes under 5 minutes for a mid-size nation. Measure it. | [galactic] |
| P9 | **15-minute target session.** | Hypemasters | Phone-sized sessions. | Same target for active play. | [hype] |
| P10 | **Do not zoom the camera to make units tappable.** | Hypemasters | Constant zooming is tiring. | Tap targets are sized in screen space, not world space (stack icons ≥ 48 dp at every zoom). | [hype] |
| P11 | **Users switch grips constantly**, so no gesture should depend on one grip. | Hoober study | Gestures fail when grip changes. | Every gesture has a button alternative. | [hoober] |

## 15. Away play: orders that run while you sleep (W)

| # | Detail | Game | Why players like / hate it | Vigil take | Src |
|---|---|---|---|---|---|
| W1 | **Offline training through a queue.** | EVE Online | Progress while living your life. | See Q1. | [eve-queue] |
| W2 | **Owner-chosen vulnerability window**: reinforcement timers always end inside the defender's chosen hours. | EVE Online | The biggest fairness tool for multi-timezone wars. | Each player picks a 6 h "prime time" daily. The **final capture stage** of their capital (and maybe their 2 biggest cities) can only complete inside that window or after 1 game day of siege, whichever is first. | [eve-cit] |
| W3 | **Defender advantage in contests**: attacker needs 60 min, defender 10 min to reset. | EVE Online | Rewards showing up to defend. | Recapturing your own city during a siege takes 1/3 the time of capturing it. | [eve-cit] |
| W4 | **Battle plans execute on their own** (see O18). | Hearts of Iron IV | Works while asleep. | See O18. | [hoi4-dd45] |
| W5 | **Strike force sorties on detection** (see A3). | Hearts of Iron IV | Navy defends while you sleep. | See A3. | [hoi4-navy] |
| W6 | **Alert wakes units when enemies approach** (see O11). | Civilization VII | No idle guard missed. | See O11. | [civ7] |
| W7 | **Automation modules you switch on and off** (e.g. explore, survey); hover shows which are enabled. | Stellaris | Players trust automation they can read. | AI commander uses visible toggles: "defend cities", "counter-attack within 2 links", "keep air cover", "never cross borders", "retreat at 30% HP". The stack label shows which are on. | [stel-295] |
| W8 | **Sitters / deputies** (see I5). | Travian | Friends cover your absence. | See I5. | [travian-sit] |
| W9 | **Timers and delayed outcomes**: issue commands, close the app, come back later. | Fishlabs | Async fits mobile. | Every order type works with the app closed; nothing needs the app open to complete. | [fishlabs] |
| W10 | **Vacation freezes production and blocks attacks on you** (Travian); vacation only blocks booting (Warzone). | Kingdoms, Warzone | Full protection is abused in war games; boot-only protection is fair. | Away mode gives **no** immunity; it only stops AI takeover and turns on the AI commander with your chosen toggles. | [kingdoms-vac], [war-vac] |
| W11 | **Offline anxiety** (see I15). | Last War | Main pain point. | Away orders + AI commander + morning report. | [wardawgg] |
| W12 | **Weapon release rules apply without the player** (see O26, A17). | Command: Modern Operations | Units behave sensibly alone. | Doctrine defaults apply to AI commander actions too. | [cmo-107] |
| W13 | **New units auto-join a chosen army** (see O24). | Stellaris | Production keeps flowing to the front. | See O24. | [stel-295] |

## 16. Fairness, anti-cheat and anti-multi-account (H)

| # | Detail | Game | Why players like / hate it | Vigil take | Src |
|---|---|---|---|---|---|
| H1 | **Sitter rules tightened to fight multi-accounts**: access tied to the owner's own activity. | Travian | Sitting had been used to run extra accounts. | Deputy bank (I5) refills only from the owner's own play. | [travian-sit] |
| H2 | **Marketplace frozen during vacation.** | Kingdoms (Travian) | Stops feeding via "vacationing" farm accounts. | See E9. | [kingdoms-vac] |
| H3 | **Cannot enter vacation while holding a Wonder or under beginner protection.** | Kingdoms (Travian) | Closes stacking of protections. | Away mode not allowed while holding a victory site or during replacement protection. | [kingdoms-vac] |
| H4 | **48 h activation delay** before vacation starts (see I6). | Kingdoms (Travian) | No dodge-by-vacation. | See I6. | [kingdoms-vac] |
| H5 | **Vacation ends 1 h after you play.** | Warzone | Cannot play while "away". | Acting ends away mode after 60 min (T11). | [war-vac] |
| H6 | **Viewing the map does not count as activity**; only real actions do. | Call of War | Stops logged-in zombies. | Same rule. | [cow-inactive] |
| H7 | **Owner schedules hidden from outsiders and from the API.** | EVE Online | Third-party tools cannot reveal weak hours. | Prime-time windows (W2) are never exposed outside the coalition. | [eve-cit] |
| H8 | **Anonymous games** (see D6). | vDiplomacy | Reduces out-of-game teaming. | See D6. | [vdip] |
| H9 | **Ranked mode: daily attack caps, no skipping targets.** | Clash of Clans | Removes cherry-picking weak targets. | Ranked matches: no leaving and re-joining to pick a better start; country assigned by draft. | [coc-2025] |
| H10 | **Players report multi-accounting in forums; staff handle it manually.** | Warzone | Slow and inconsistent. | Automated risk score + human review (extends polish #186–191). | [war-multi] |
| H11 | **Multi-account detection FAQ published** (what is checked, what is allowed). | FACEIT | Transparency reduces false-ban anger. | Publish a short "what counts as multi-accounting" page with household rules. | [faceit] |
| H12 | **Stance-switch exploit closed** (see O5). | Call of War | Exploits feel unfair. | See O5. | [cow-2606] |
| H13 | **Hidden information, not randomness**, drives uncertainty. | Galactic Reign | Losses feel fair. | Keep combat randomness small (±10%); uncertainty comes from fog. | [galactic] |
| H14 | **Shadow base**: attacking a shielded base hits a copy with no losses for either side. | Clash of Clans | Lets attackers play without harming protected players. | Not applicable to a shared real-time map. | [coc-2025] |

## 17. Monetisation players accept vs hate (M)

| # | Detail | Game | Why players like / hate it | Vigil take | Src |
|---|---|---|---|---|---|
| M1 | **Acceptance by model**: cosmetics 62%, monthly subscription 53%, one-time unlocks 42%, microtransactions 32%, battle pass 25%, ads for rewards 17%. | PBBG player survey 2024 (long-session browser games) | Closest audience to weeks-long strategy. | Lead with cosmetics + optional subscription (convenience, cosmetic) + one-time unlocks (the permanent alliance). | [pbbg] |
| M2 | **About 5% of players spend**; 58.5% of respondents spend nothing per month. | PBBG survey, AppFollow | Plan the economy around few payers. | Revenue model must work with ~5% payers buying cosmetics. | [pbbg], [appfollow] |
| M3 | **Battle pass ~$10 with real content = fair; over $20 = expensive; non-expiring passes praised; limited-time passes draw FOMO complaints.** | App store reviews (AppFollow) | Clear price bands. | One season pass ≤ $5–10, cosmetic, never expires. | [appfollow] |
| M4 | **Weekly subscriptions appear "constantly" in negative reviews; monthly gets less pushback.** | App store reviews (AppFollow) | Weekly feels predatory. | Monthly only. | [appfollow] |
| M5 | **Forced interstitial ads cause immediate uninstalls; ads that force sound when the phone is muted are hated.** | App store reviews (AppFollow) | Breaks trust instantly. | No interstitials. If any rewarded ad exists, muted by default and cosmetic reward only. | [appfollow] |
| M6 | **Warning sign: 20–25%+ of reviews mentioning price or ads negatively.** | AppFollow (rule of thumb) | Early alarm. | Track this in review monitoring after launch. | [appfollow] |
| M7 | **Recharge rewards**: daily spend target (~€14) for 5 days unlocks legendary items; 7-day mini pass €20–30; VIP shop. | Rise of Kingdoms | Big revenue; seen as whale-only. | Do not copy any spend-target rewards or VIP. | [gr-4x] |
| M8 | **VIP levels boost construction, research and march speed**; pay gap grows with server age. | Last War | Top quit reason. | No VIP levels at all. | [wardawgg] |
| M9 | **Packs up to $99.99, $24.99 monthly pass, loot boxes, a screen full of offer icons.** | Last War | "Pay-to-win"; reviewer: 7/10 fun, 4/10 fairness. | One shop button; no offer icons on the map. | [orcz] |
| M10 | **Very high ARPDAU ($2.47) but D30 retention 4% vs a rival's 8%.** | Last War vs Whiteout Survival | Aggressive monetisation and misleading ads can coexist with weak retention. | Optimise for retention first; a weeks-long match needs players who stay. | [naavik] |
| M11 | **Rewarded ads give extra units** (unusual in the genre). | Top War | Ads affect power. | Never. | [topwar] |
| M12 | **Purchasable shields have cooldowns** (1 day/4-day cooldown, 2 days/7, 1 week/35). | Clash of Clans | Caps how much money can buy. | If any convenience is sold, put a cooldown on it. | [coc-2025] |
| M13 | **Holiday crates from operations and rewarded ads that can drop atomic bombers.** | Call of War (Dec 2025) | Power in crates is the classic pay-to-win complaint. | No power in crates; no crates at all. | [cow-2512] |
| M14 | **Premium currency can be earned in play** (liked); but "microtransactions are the only way to win" (hated). | Supremacy 1914 reviews | Earnable currency softens, but does not fix, pay-to-win. | Earnable currency buys cosmetics only. | [gb-s1914] |
| M15 | **Build queue and fire control behind premium.** | Call of War, Supremacy 1914 | Players see QoL paywalls as unfair. | All QoL free (see Q5, O4). | [bytro-hc] |
| M16 | **Weekly alliance duel creates social pressure to spend.** | Last War | Social pressure to pay is resented. | Coalition rewards are cosmetic (K5). | [naavik] |

## 18. Retention features players liked or hated (R)

| # | Detail | Game | Why players like / hate it | Vigil take | Src |
|---|---|---|---|---|---|
| R1 | **All top 200 grossing 4X games run recurring live events.** | Top 4X games | Gives a sense of progression between matches. | Rotating modes and a seasonal profile (extends polish #198). | [gr-4x] |
| R2 | **Milestone rewards for the 1st, 3rd and 6th victory** in a recurring mode, not daily streaks. | Rise of Kingdoms | Rewards play without punishing missed days. | Season rewards at 1, 3, 6 match finishes. No login streaks. | [gr-4x] |
| R3 | **Returning players get a 48 h shield.** | Clash of Clans | Welcomes lapsed players back. | Lapsed players get a free "veteran returns" cosmetic and priority seat in the next match (no in-match power). | [coc-2025] |
| R4 | **Killboards** make kills public and famous. | EVE Online | Fame keeps players. | End-of-match hall of fame: top commander, best defence, biggest battle. | [eve-km] |
| R5 | **Tiny delight actions** ("Pet the Dog", cosmetic and repeatable). | Civilization VII | Players love small useless joys. | One hidden, harmless delight (e.g. tapping your capital at night lights the skyline). | [civ7] |
| R6 | **Music and feeling like a national leader** are praised. | Supremacy 1914 reviews | Atmosphere matters to long-session players. | Leader-perspective news and music (extends polish #103). | [gb-s1914] |
| R7 | **Seasons gave clear revenue lifts.** | Last War | Seasons refresh interest. | Quarterly seasons with new maps and cosmetics. | [naavik] |
| R8 | **Anticipation of each new turn** is the hook. | Galactic Reign | The return visit is exciting. | Morning report reveals results like opening a letter: headline first, details after. | [galactic] |
| R9 | **Post-game map exploration** (see N8). | Age of Empires IV | Players love reviewing a finished match. | Time-lapse replay of the whole match. | [aoe4-s1] |
| R10 | **Steady progression and clean, readable presentation** praised. | Last War | Readability keeps casual players. | Keep the map clean (polish §2). | [orcz] |
| R11 | **Weekend fast map (8x).** | Call of War | Short, exciting break from long matches. | Weekend 8x regional matches. | [cow-2512] |
| R12 | **Guild tasks** (helping each other) become a daily habit. | Top 4X games | Social habit. | Coalition help (E7). | [gr-4x] |

## 19. What made people quit (Z)

| # | Detail | Game | Lesson | Vigil take | Src |
|---|---|---|---|---|---|
| Z1 | **Pay gap grows as a server ages**; pay gates stall free players. | Last War | Fairness decays over time in persistent servers. | Fixed-length matches, no persistent power. | [wardawgg] |
| Z2 | **Toxic alliance leaders and rogue whales** ignoring pacts. | Last War | A few players can empty a server. | Treaty records (D10), mute/report, coalition caps per server. | [wardawgg] |
| Z3 | **Required online times for events feel like unpaid work.** | Last War | Obligation kills fun. | No mandatory fixed-time events (T17). | [wardawgg] |
| Z4 | **Server death spiral**: drama → top players leave → rewards dry up → collapse. | Last War | Persistent worlds rot. | Matches end; new match = fresh start (S13). | [wardawgg] |
| Z5 | **Timers lengthen and costs rise; stamina becomes a bottleneck.** | Last War | Slowing progress is felt as a squeeze to pay. | Timers stay in the same band all match. | [orcz] |
| Z6 | **"The game asks how much your patience is worth, not how skilled you are."** | Last War (review) | Skill must decide outcomes. | Design pillar. | [orcz] |
| Z7 | **Slow pacing, repetition, stability errors, removed flag and leader customisation.** | Supremacy 1914 | Removing features players liked hurts. | Keep player customisation (flag style, leader portrait) from launch. | [gb-s1914] |
| Z8 | **Ads that do not match the game** halve 30-day retention. | Last War | Bait-and-switch churns. | Honest ads (polish #206). | [naavik] |
| Z9 | **Invites not arriving, stuck games, friend codes changing after an update.** | Polytopia (multiplayer launch) | Social plumbing bugs kill multiplayer. | Friend codes never change; invite delivery tested every release. | [poly-mp] |
| Z10 | **Newcomer feedback lists confusion in a weeks-long real-time game.** | Neptune's Pride | Long games need clear first days. | First-match map and explained timers (N12, T8). | [np-newbie] |
| Z11 | **Fear that a year-long queue makes players drift away.** | EVE Online (developer) | Too much automation can make players leave. | Queues cover nights, not weeks (Q1). | [eve-queue] |
| Z12 | **Games locked waiting for replacements.** | vDiplomacy | Pauses kill momentum. | Never pause (I7). | [vdip] |
| Z13 | **Players leave by the end of week one** in CoN (see con_mechanics §9). | Conflict of Nations | Dead matches. | AI takeover plus replacement players (I1, I2). | — |

## 20. Performance on low-end phones (F)

| # | Detail | Game | Why players like / hate it | Vigil take | Src |
|---|---|---|---|---|---|
| F1 | **Google Play "bad behaviour" thresholds**: user-perceived crash rate 1.09% and ANR rate 0.47% overall; 8% on any single phone model. Above them, store visibility drops. | Android vitals | Crashes cost discovery, not just reviews. | Release gate: crash < 0.5%, ANR < 0.25%, no model above 4%. | [vitals] |
| F2 | **Memory thresholds for games**: on 4 GB phones, 2.25 GB in the foreground; 6 GB → 2.75 GB; 8 GB → 3.5 GB. | Android vitals | Exceeding them gets the game killed. | Budget 1.5 GB total on 4 GB phones (leaves headroom); 1 GB on 3 GB phones. | [vitals] |
| F3 | **Bitmap memory**: 200 MB in background, 400 MB cached. | Android vitals | Big textures get the app evicted when switching apps. | Drop high-res map tiles when backgrounded; reload on resume. | [vitals] |
| F4 | **Minimum spec pinned to an old GPU (iPad 3) for years.** | World of Tanks Blitz | Huge audience on old devices. | Pick one reference low-end phone (e.g. a 3 GB Android) and test every build on it. | [wotb] |
| F5 | **"Give the player a switch for almost every graphics feature."** | World of Tanks Blitz | Players tune for their phone. | Settings for water waves, clouds, unit animations, city detail, frame cap. | [wotb] |
| F6 | **Bake environment lighting; only tanks are dynamically lit**; lightmaps only beyond a distance. | World of Tanks Blitz | Big savings for small visual cost. | Map lighting baked into tiles; only units and effects are dynamic. | [wotb] |
| F7 | **Enemy outlines drawn with a stencil mesh instead of post-processing.** | World of Tanks Blitz | Cheap highlight. | Selection outlines and glows via sprites or stencil, never full-screen post effects. | [wotb] |
| F8 | **"Can still run on a potato."** | Unciv | A loved promise in reviews and forks. | State the minimum phone on the store page. | [unciv] |
| F9 | **Lag, freezing, forced restarts, error codes** in reviews. | Supremacy 1914 | Stability complaints dominate. | Every error message says what to do, not a code (e.g. "Connection lost, your orders are saved. Retrying..."). | [gb-s1914] |

---

## The 40 most valuable items

Ranked by how much each fixes a known pain of CoN-style games for the least design cost.

1. **W2 – Defender's prime-time window** (EVE): the final capture of a capital completes only in the defender's chosen hours or after a long siege. The best fix for "lost my capital while asleep".
2. **W10 – Away mode gives no immunity**, only stops AI takeover and turns on your AI commander (Warzone vs Travian lesson).
3. **W7 – AI commander with visible toggles** ("defend cities", "counter-attack within 2 links", "retreat at 30%") (Stellaris automation modules).
4. **I1 – Inactivity = 2 game days with no real orders; AI takes over at once**; queues and map viewing don't count (CoW).
5. **I2 – Separate no-show and quitter rules**, with replacement players from a waiting list (Neptune's Pride).
6. **I5 – Coalition deputy with an activity-linked bank** (Travian sitter allowance).
7. **Q5/O4 – Build queues and fire stances free** (were premium in Bytro games).
8. **O1 – Order chaining** with per-leg arrival times (StarCraft II, WARNO).
9. **O2 – Two move verbs: Transit vs Advance** (WARNO Hunt).
10. **O3 – Three fire stances per stack** (WARNO, Bytro).
11. **O11 – Sentry: hold and alert only when an enemy enters sight** (Civ VII Alert).
12. **O24 – City rally points and auto-join stack** (Stellaris).
13. **Q8 – Stack templates, one-tap build** (Stellaris).
14. **Q7 – "Build N in region" spreads over cities** (Stellaris army builder).
15. **T8/Q1 – Queue coverage bar, queues sized to cover one night** (EVE).
16. **T2 – Long-press any toast to change how you're told about it** (Stellaris).
17. **T7 – Pushes default-on only for attacks, losses and coalition requests** (Fishlabs).
18. **C1/C2 – Battle report with each attacker's damage share, shareable in coalition chat** (EVE killmail).
19. **C4 – Losers always see the attacker's full composition** (Galactic Reign).
20. **C11/C12/C13 – Effects, ranges and orders must never lie** (Call of War 2026 bug fixes).
21. **C10 – Unit card shows the final strength formula** (AoE IV).
22. **A1 – Winchester auto-RTB with "ready again at" time** (CMO).
23. **A2 – "Reach" and "reach and return" rings on strike orders** (CMO).
24. **A3 – Reaction force: fleet or air group sorties when an enemy enters a zone** (HOI4 strike force).
25. **A12 – SAM/missile sites switch defend/launch mode; a launch reveals the site** (DEFCON).
26. **A15 – Each WMD costs more than the last** (OTC black market).
27. **L1/L3 – Supply bottleneck highlighted; three visible stages of undersupply** (HOI4).
28. **L7 – Provinces cut off from all your cities produce nothing** (Company of Heroes).
29. **L8 – Attrition more than 3 links beyond friendly territory without a supply unit** (Rise of Nations).
30. **D1 – War weariness; at 100% the other side can impose "keep what you hold"** (Stellaris).
31. **D9 – AI containment pact against any player above X% of the map** (EU4).
32. **D7 – Reliability ("finished 9 of 10") on profiles and coalition invites** (webDiplomacy).
33. **K4 – Coalition "Operations": leader sets target and time, members commit stacks** (RoK rally).
34. **K3 – Joint strike bonus for stacks arriving in the same tick** (Civ VII Coordinated Attack).
35. **S5 – After heavy losses, faster recruitment instead of immunity** (Clash of Clans shield, adapted).
36. **E2 – Standing market orders (sell above / buy below)** (OTC player request).
37. **X5/X6 – Destructive actions never in corners and need hold-to-confirm; readouts above the finger** (Hoober).
38. **P4 – Map-app gestures: double-tap in, two-finger tap out, one-finger zoom; no rotation** (Mapbox, Google Maps).
39. **F1/F2 – Release gates below Android vitals thresholds; 1.5 GB memory budget on 4 GB phones** (Google Play).
40. **M1/M3/M8 – Cosmetics + monthly sub + one-time unlocks; ≤$10 non-expiring pass; no VIP levels** (PBBG survey, AppFollow, Last War quit reasons).

---

## Gaps

- **Reddit** threads could not be read directly; player feedback came from review digests, Steam/forum threads and analyst articles instead.
- **HOI4 battle plan details** (O18, O19) come from the dev-diary title and well-known behaviour; the dev diary page was blocked by a browser check.
- **Humankind war support numbers** (D4): the guide page failed to load; the mechanic is well known but numbers are not given here.
- **Several S-marked sources** (DEFCON, Total War auto-resolve, OGame bashing, Mapbox gestures, XAG 105/107) were located by search and not read in full.
- **No source was found** for Supremacy 1914 or CoN inactivity rules beyond the 2017 Call of War thread.
- **Warpath, Total Battle, Rise of Kingdoms combat** details are thin; their pages returned little usable content.

---

## Sources

R = read this session. S = located by search, not read in full.

[acoup]: https://acoup.blog/2021/05/07/collections-teaching-paradox-europa-universalis-iv-part-ii-red-queens/
[aoe4-s1]: https://www.ageofempires.com/news/age-of-empires-iv-season-one-update-release-notes/
[appfollow]: https://appfollow.io/blog/what-mobile-game-players-want-monetization-insights-from-app-store-reviews
[blendo]: https://www.blendogames.com/news/post/2017-05-25-on-company-of-heroes/
[bytro-hc]: https://www.playsupremacy.com/en/forums/call-of-war-1942/call-of-war-1942-questions-and-answers/high-command-5d31dfc2
[civ7]: https://civilization.fandom.com/wiki/List_of_unit_actions_in_Civ7
[cmo-107]: https://command.matrixgames.com/?p=3598
[coc-2025]: https://www.fragster.com/clash-of-clans-october-2025-update-battle-modes-shield-rework-more/
[coh2]: https://www.coh2.org/guides/5732/company-of-heroes-2-basic-concepts-and-glossary
[cow-2512]: https://playsupremacy.com/en/news/call-of-war-1942/release-notes-20251216
[cow-2606]: https://playsupremacy.com/en/news/call-of-war-1942/release-notes-june-30th-2026
[cow-inactive]: https://www.playsupremacy.com/en/forums/call-of-war-1942/call-of-war-1942-questions-and-answers/how-long-until-a-player-goes-inactive-eb521b59
[defcon]: https://www.wikiwand.com/en/articles/Defcon_(video_game)
[dip-rules]: https://en.wikibooks.org/wiki/Diplomacy/Rules
[eu4-dd11]: https://admin-forum.paradoxplaza.com/forum/developer-diary/dev-diary-11-stopping-the-snowball.896247/page-5
[eve-cit]: https://www.eveonline.com/news/view/citadels-sieges-and-you
[eve-km]: https://wiki.eveuniversity.org/Killmail
[eve-queue]: https://eveonline.com/article/more-queue-queue
[faceit]: https://support.faceit.com/hc/en-us/articles/9494394217116-Multi-Account-Detection-FAQ
[fishlabs]: https://www.gamedeveloper.com/business/commanding-troops-on-touch-devices-why-mobile-is-the-perfect-platform-for-strategy-mmos
[fp-con]: https://gamedeveloper.com/design/the-simple-most-difficult-challenge-of-bringing-frostpunk-to-consoles
[fp2-ui]: https://www.pcgamesn.com/frostpunk-2/ui-improvements
[galactic]: https://gamedeveloper.com/design/galactic-reign-competitive-depth-on-mobile-platforms
[gb-s1914]: https://gamebrain.co/game/supremacy-1914
[gmaps]: https://www.technipages.com/how-to-zoom-on-google-maps-with-one-finger
[gr-4x]: https://www.gamerefinery.com/what-drives-success-in-4x-strategy-slg-games-part-2
[gunboat]: https://burdonvale.nfshost.com/octopus/gunboat.html
[hk-griev]: https://humankind.fandom.com/wiki/Grievance_and_Demand
[hk-war]: https://primagames.com/gaming/humankind-diplomacy-war-score-war-support-guide
[hoi4-air]: https://admin-forum.paradoxplaza.com/forum/developer-diary/dev-corner-hydrodynamics.1779310/latest
[hoi4-bp]: https://admin-forum.paradoxplaza.com/forum/threads/im-trying-to-get-into-hoi4-is-the-battle-plan-a-feature-that-all-players-play-around-instead-of-using-is-there-a-nice-guide-to-using-it.1827856
[hoi4-dd45]: https://forum.paradoxplaza.com/forum/threads/hearts-of-iron-iv-45th-development-diary-19th-of-february-2016.909353/
[hoi4-navy]: https://noobfeed.com/articles/hearts-of-iron-iv-guide-navy-tips-and-tricks
[hoi4-sup]: https://guildorder.com/games/hoi4/wiki/supply-and-logistics
[hoober]: https://uxmatters.com/mt/archives/2013/02/how-do-users-really-hold-mobile-devices.php
[hype]: https://medium.com/hypemasters/mobile-rts-interface-the-story-of-how-hypemasters-rediscovered-the-genre-dc7fbaa5b05c
[kingdoms-bp]: https://support.kingdoms.com/en/articles/4-beginner-s-protection
[kingdoms-vac]: https://support.kingdoms.com/en/articles/179-vacation-mode
[mapbox]: https://docs.mapbox.com/android/maps/guides/user-interaction/gestures.md
[naavik]: https://naavik.co/digest/how-last-war-is-winning-the-4x-game/
[np-afk]: https://forum.ironhelmet.com/t/flag-to-indicate-potential-afks/4098
[np-ai]: https://forum.ironhelmet.com/t/when-does-someone-turn-into-ai/1158
[np-newbie]: https://forum.ironhelmet.com/t/a-bunch-of-collected-feedback-from-a-newbie/5320
[np-sleep]: https://forum.ironhelmet.com/t/solution-for-sleep-time-is-needed/4226
[ogame-bash]: https://ogame.fandom.com/wiki/Bashing?oldid=8494
[ogame-sit]: https://ogame.fandom.com/wiki/Account-sitting
[orcz]: https://orcz.com/last-war-survival-game-review-is-it-actually-fun-or-just-aggressively-monetized/
[otc-auto]: https://www.stardock.com/games/article/478636/auto-buy-behavior-in-release-build
[otc-prices]: https://www.stardock.com/games/article/477228/offworld-market-prices-prior-to-building
[otc-sug]: https://www.stardock.com/games/article/483980/price-based-trading-stockpiling-options-ui-features
[otc-wiki]: https://en.wikipedia.org/wiki/Offworld_Trading_Company
[pbbg]: https://makeitbigingames.com/2024/09/monetization-in-pbbgs-insights-and-survey-results-part-2/
[poly-mp]: https://statelyplay.com/2018/01/16/battle-of-polytopia-going-multiplayer
[rok-hosp]: https://riseofkingdomsguides.com/hospital/
[rok-march]: https://riseofkingdomsguides.com/rise-of-kingdoms-troop-capacity-and-march-queue-guide/
[ron-wagon]: https://riseofnations.fandom.com/wiki/Supply_Wagon
[sc2-cam]: https://dignitas.gg/articles/Using-Camera-Hotkeys-in-SC2
[sc2-micro]: https://liquipedia.net/starcraft2/Micro_(StarCraft)
[sc2-unit]: https://news.blizzard.com/en-us/article/4552957/game-guide-unit-control
[stel-295]: https://admin-forum.paradoxplaza.com/forum/developer-diary/stellaris-dev-diary-295-armies-sectors-messages-and-more.1578373
[stel-93]: https://admin-forum.paradoxplaza.com/forum/developer-diary/stellaris-dev-diary-93-war-peace-and-claims.1054054
[stel-pulse]: https://admin-forum.paradoxplaza.com/forum/threads/stellaris-notifications-pulse-too-long-or-dont-stop.1584673
[topwar]: https://gamerefinery.com/top-war-battle-game-a-quick-glimpse-on-the-4x-strategy-hit
[travian-bp]: https://support.travian.com/support/solutions/articles/7000060689
[travian-sit]: https://blog.travian.com/2021/03/stricter-rules-for-sitter-accounts
[tw-ar]: https://steamcommunity.com/app/1142710/discussions/0/3832045251561220120
[unciv]: https://www.Github.com/yairm210/Unciv
[vdip]: https://vdiplomacy.net/features.php
[vitals]: https://developer.android.com/games/optimize/vitals
[war-boot]: https://war.app/wiki/Boot
[war-bootrate]: https://war.app/Forum/712320-boot-rate-count-method-changed
[war-multi]: https://warzone.com/Forum/759837-cheating-player-using-multiple-accounts
[war-vac]: https://war.app/wiki/Vacation
[wardawgg]: https://wardawgg.pages.dev/guides/why-players-quit-guide
[warno]: https://gameplay.tips/guides/warno-ultimate-controls-guide-selecting-units-controlling-the-camera-and-giving-orders.html
[webdip-rr]: https://www.webdiplomacy.net/contrib/phpBB3/viewtopic.php?p=28014
[wotb]: https://80.lv/articles/world-of-tanks-blitz-mobile-game-development-at-wargaming
[xag105]: https://learn.microsoft.com/en-us/gaming/accessibility/xbox-accessibility-guidelines/105
[xag107]: https://learn.microsoft.com/en-us/gaming/accessibility/xbox-accessibility-guidelines/107
[xag116]: https://learn.microsoft.com/en-us/gaming/accessibility/xbox-accessibility-guidelines/116

**Read status of each source.**
- **R (read):** acoup, aoe4-s1, appfollow, blendo, bytro-hc, civ7, cmo-107, coc-2025, coh2, cow-2512, cow-2606, cow-inactive, eve-cit, eve-km, eve-queue, fishlabs, fp-con, fp2-ui, galactic, gb-s1914, gr-4x, hoi4-navy, hoi4-sup, hoober, hype, kingdoms-vac, naavik, np-ai, orcz, otc-sug, otc-wiki, pbbg, poly-mp, rok-march, ron-wagon, sc2-unit, stel-295, stel-93, topwar, travian-sit, unciv, vdip, vitals, war-boot, war-vac, wardawgg, warno, wotb, xag116.
- **S (located, not read in full):** defcon, dip-rules, eu4-dd11, faceit, gmaps, gunboat, hk-griev, hk-war, hoi4-air, hoi4-bp, hoi4-dd45, kingdoms-bp, mapbox, np-afk, np-newbie, np-sleep, ogame-bash, ogame-sit, otc-auto, otc-prices, rok-hosp, sc2-cam, sc2-micro, stel-pulse, travian-bp, tw-ar, war-bootrate, war-multi, webdip-rr, xag105, xag107.

Notes on specific claims:
- [otc-sug] is a player suggestion thread, not a shipped feature; E2 and E3 are labelled that way.
- [hoi4-air] is a naval dev diary; it is used only as a pointer for HOI4's air-region mission system, which is well known but not confirmed from that page.
- The Clash of Clans shield and revenge numbers (S5, S6, M12) come from a third-party summary of the October 2025 update, not Supercell's own notes.
- Last War revenue and retention figures (M10) are Sensor Tower estimates quoted by Naavik.
