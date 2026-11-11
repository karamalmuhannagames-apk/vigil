# Polish Tips: small details that make the game feel premium

A field guide of small, concrete details collected from player reviews, developer postmortems, platform guidelines and UX research on Conflict of Nations, Call of War, Supremacy 1914, Hearts of Iron IV, Crusader Kings III, Civilization, Polytopia, Clash of Clans, Rise of Kingdoms, Rusted Warfare, Apex/Call of Duty and others. Tips are **ranked by impact within each category** (most important first). Each one is one or two lines and actionable, with a source where one exists. Tips without a link are standard industry practice or direct inferences from the linked complaints.

Total: **206 tips** in 15 categories, plus a **Top 25** at the end. Accessibility tips (colour-blind safety, tap-target size, reduced motion, volume and haptic controls) are placed where they apply instead of in a separate section.

**What players say about CoN, our closest rival** (this shaped the ranking): praise goes to strategic depth, unit variety, real-world-based units, good mobile graphics and no ads. The main complaints are crashes and freezes, pay-to-win pop-ups, slow timers and endless menu clicking, a steep learning curve with text-heavy tutorials, lag even on high-end phones, cluttered troop displays, no music, and loud sound effects with no volume control ([GameBrain review digest](https://gamebrain.co/game/conflict-of-nations-ww3)). For Call of War, reviewers single out dull auto-resolved battles, a weak tutorial, gold speed-ups, a slow pace and unpenalised nukes ([F2P.com](https://www.f2p.com/?p=36088)). Each of those is a chance for us to win.

---

## 1. First minutes and onboarding (discover by exploring, no nagging pop-ups)

1. **No commander pop-ups telling the player what to do.** Teach through the world: the first city glows softly, the first idle unit "breathes", and the first enemy border pulses once. Players skip text walls ([Roblox onboarding guide](https://create.roblox.com/docs/en-us/production/game-design/onboarding-techniques)).
2. **Just-in-time hints, only when the player is stuck.** Measure how long most players take to find something, then show a gentle highlight *after* that time (Roblox's example: most players found the button within 10 s, so the hint appears at 11 s). Hints that come too early insult; hints that come too late lose players.
3. **Start in a short, fast, low-stakes "first war"** (10–15 minutes, accelerated time) against a weak computer-controlled neighbour, so the whole loop of build, move, fight and capture happens in the first session. Call of War players asked for exactly this ([F2P.com](https://www.f2p.com/?p=36088)).
4. **Progressive disclosure:** hide whole systems until they matter. Show diplomacy after the first contact, the market after the first surplus, and nuclear research only mid-game. CK3 cut its 67 tutorial messages to a third and revealed panels in stages ([Game Developer](https://gamedeveloper.com/design/deep-dive-refreshing-the-crusader-kings-iii-tutorial-mode-through-optimized-ux)).
5. **Nested tooltips (tooltips inside tooltips):** every game term in any text is tappable and opens its own definition. CK3's biggest learnability win ([PC Gamer](https://pcgamer.com/the-crusader-kings-3-team-is-working-hard-to-make-the-game-easier-to-learn)).
6. **An "Issues" tray instead of nagging:** a small badge collects long-running problems ("2 cities have no defence", "Oil running out in 3 h") with a one-tap jump. The player pulls information; it is never pushed ([PC Gamer on CK3](https://pcgamer.com/the-crusader-kings-3-team-is-working-hard-to-make-the-game-easier-to-learn)).
7. **Make the game learnable from inside the game.** HOI4's #1 complaint is that you must learn it from YouTube and wikis ([HOI4 review digest](https://vaporlens.app/app/394360/hearts_of_iron_iv.md)). Add an in-game encyclopedia with short animated clips for each unit and mechanic.
8. **Unit cards teach counters:** each card shows "Strong against / Weak against" icons and one plain sentence (see `regional_doctrines.md` section 7). Players learn rock-paper-scissors without a lesson.
9. **Preview every outcome before it is committed:** dragging an attack shows the predicted result ("Likely win, ~20% losses") and arrival time. That beats any tutorial at teaching combat.
10. **Celebrate the first time for each thing** (first capture, first plane, first alliance) with a short medal moment and sound, never a modal window that blocks play.
11. **Telemetry on the funnel:** log where new players stop in the first 30 minutes, and A/B test onboarding changes as CK3 did, keeping the old version to compare retention ([Game Developer](https://gamedeveloper.com/design/deep-dive-refreshing-the-crusader-kings-iii-tutorial-mode-through-optimized-ux)).
12. **Playtest with people outside the team** (kids, parents, non-gamers) to beat the "curse of knowledge" (same source).
13. **Let veterans skip onboarding instantly** with a single "I know strategy games" choice at the start, which can be changed later in settings.
14. **Polytopia rule:** one or two matches should give a complete sense of the game ([COGconnected](https://cogconnected.com/review/battle-polytopia-review/)). Design the first real match so that is true.
15. **Ask permission for notifications only after a meaningful action** (e.g. the first unit starts a 2-hour march), with an in-game explanation of the value. Asking at first launch fails ([Pushwoosh](https://www.pushwoosh.com/blog/game-app-push-notifications/)).
16. **Never ask for a rating during onboarding.** Ask after a win or a satisfying moment, at most once every few weeks.

## 2. Map readability and cartography

17. **Collision-aware labels:** the label engine drops lower-priority labels when they overlap (country > capital > city > province), and tries several anchor positions before dropping one ([Mapbox label placement](https://docs.mapbox.com/help/dive-deeper/optimize-map-label-placement/)).
18. **Zoom-dependent detail levels (LOD):** world zoom shows countries, coalitions and fronts; region zoom shows cities, army stacks and supply lines; local zoom shows buildings, individual units and terrain. Never show everything at once.
19. **Aggregate units at far zoom:** many units become one stack badge with a count and a strength bar. CoN players complain about cluttered troop displays ([GameBrain](https://gamebrain.co/game/conflict-of-nations-ww3)).
20. **Relation colours safe for colour-blind players:** never encode ally/enemy by red-versus-green alone. Pair colour with shape (shield = ally, chevron = enemy, circle = neutral) and offer presets for deuteranopia, protanopia and tritanopia. 8–10% of males have red-green difficulty ([Game Accessibility Guidelines](https://gameaccessibilityguidelines.com/ensure-no-essential-information-is-conveyed-by-a-fixed-colour-alone/)).
21. **Default two-team palette: blue versus orange**, with a light/dark difference between them (same source).
22. **Country fill at low opacity, borders strong:** a satellite map needs translucent political tint (about 25–35%) so terrain stays readable, and crisp borders with a subtle outer glow in the owner's colour.
23. **Front lines drawn as a living line** (animated hatch or soft glow) between warring countries, so "where is the war?" is answered at a glance.
24. **Text halos:** every map label gets a soft dark or light halo matching the terrain behind it, so labels stay readable over desert, sea and snow.
25. **Label size by importance, not just by zoom:** capitals are 1.3× city size, and the player's own cities get a small badge.
26. **Ghost previews for orders:** planned paths are dashed in the player's colour, with an arrival-time chip on the destination.
27. **Show enemy vision ranges and air-defence circles on demand** (a tap-and-hold "intel" lens), not permanently.
28. **Fog of war that looks like weather, not a black box:** desaturated, slightly blurred terrain with "last seen" ghost markers and how old they are ("3 h ago").
29. **Distinct unit silhouettes at every zoom** (owner requirement): tank versus IFV versus SPAA must differ by shape, not only colour.
30. **Night/day terminator line (optional):** a soft day/night shade sweeping the real world map is a cheap premium-feeling touch, and it helps players think about time zones.
31. **Sea lanes, straits and canals visibly marked** (Hormuz, Suez, Malacca, Bosporus), with status icons when closed, to support the owner's "close the strait" standing order.
32. **Pinch-zoom snaps gently to "level" steps** so the LOD swaps don't flicker.
33. **No label rotation for Arabic text at steep angles:** keep Arabic labels horizontal, or along gentle curves only. Shaped Arabic on tight curves breaks letter joins (see section 4).
34. **Province and city names in the player's language, with one tap to show the other language** (Arabic ↔ English). Teaches geography and helps coalition chat.
35. **A minimal minimap in a corner**, showing alerts as pulses, tappable to jump.
36. **Distance and time ruler:** long-press between two points shows distance and travel time per unit type.

## 3. Interface and controls (mobile-first)

37. **Every tap target ≥ 48 × 48 dp, spaced ≥ 8 dp apart** ([Google accessibility](https://support.google.com/accessibility/android/answer/7101858?hl=en)). Small, fiddly buttons are the fastest way to feel cheap.
38. **Cut menu clicking:** any common action should take ≤ 2 taps from the map. Reviewers hate CoN's repetitive menu clicking ([GameBrain](https://gamebrain.co/game/conflict-of-nations-ww3)).
39. **Contextual radial menu on long-press** (move, attack, patrol, hold, standing order), like Apex's context-sensitive ping that picks the right default action for what was tapped ([Game Developer](https://gamedeveloper.com/design/respawn-played-with-muted-mics-to-get-i-apex-legends-i-smart-comms-system-just-right)).
40. **Order queues and standing orders** ("patrol here", "shoot anything over my airspace", "close this strait") so players don't have to wake up at night.
41. **Bulk actions:** "upgrade all cities of type X", "repair all", "build the same in every city". This removes most grind.
42. **Undo for 5 seconds** on non-combat orders (a mistaken move or build). Mobile thumbs make mistakes.
43. **Thumb-zone layout:** primary actions in the bottom third. Mirror the whole layout in Arabic (section 4).
44. **One global "back" behaviour** (system back gesture closes the top panel, never exits the game without confirming).
45. **Panels slide in over the map; the map stays visible and live behind them.** Never a full-screen menu for a quick action.
46. **Numbers that animate** (counting up or down) when resources change, with green/red flashes paired with arrows ▲▼ (colour-blind safe).
47. **Timers show both duration and clock time:** "2 h 15 m (arrives 21:40)". Players plan their day around clock time.
48. **Search everywhere:** a single search box finds countries, cities, players, units and encyclopedia entries, in Arabic or English.
49. **Smart defaults:** remember the last chosen production queue, filters and sort orders per screen.
50. **Empty states that teach:** an empty "Alliances" tab shows what an alliance gives you and a single button to find one.
51. **Consistent iconography:** one icon set, one stroke weight, one corner radius. Mixed icon styles read as amateur.
52. **Loading screens with real value:** live map of your nation, intel summary ("while you were away…"), never generic tips.
53. **Landscape and portrait both supported** (portrait for quick checks on the go, landscape for battles).
54. **Pull-to-refresh is not needed; state must just be live.** If data is stale, show a small "syncing" dot, never a spinner over everything.
55. **Haptic and sound confirmation on every committed order** (sections 6 and 7) so a single glance is never needed to confirm.

## 4. Arabic-native experience and RTL

56. **Design in Arabic first, then English**, not the other way round. Ubisoft's RTL rework of Smurfs reached 1.5 M Arab players, with higher revenue than the English version ([LocalizeDirect](https://www.localizedirect.com/posts/arabic-game-localization)).
57. **Mirror the whole layout in Arabic:** navigation, back arrows, progress bars (fill right-to-left), sliders, list order, the side text fields sit on, and checkbox side ([Material Design bidirectionality](https://m1.material.io/usability/bidirectionality.html)).
58. **Know what NOT to mirror:** clocks and circular progress (always clockwise), media play buttons, numbers, phone numbers, charts and graphs, physical objects, and icons implying right-handed holding (search magnifier) (same source). The **map itself is never mirrored**: north stays north.
59. **Numerals: pick one system per locale and never mix.** Maghreb uses Western digits (0–9). Egypt, Sudan and the UAE use both. Saudi Arabia increasingly favours Western digits ([Wikipedia: Eastern Arabic numerals](https://en.wikipedia.org/wiki/Eastern_Arabic_numerals)). **Default to Western digits** (clearer in a numbers-heavy strategy game) with a setting for Eastern digits (٠١٢٣٤٥٦٧٨٩) ([typography tripwires](https://appscreenshotstudio.com/blog/arabic-app-store-screenshots-4-typography-tripwires-2026)).
60. **Never let prices or timers flip:** a shipped game displayed $4.99 as "$99.4" in Arabic. Check every price, timer and ratio ([PocketGamer.biz](https://www.pocketgamer.biz/cruise-to-the-east-how-to-successfully-localize-a-game-into-arabic/)).
61. **Wrap every player name, number and English word inside Arabic sentences in Unicode bidi isolates** (FSI…PDI). This stops "Player123 captured الرياض at 14:00" from scrambling ([W3C](https://www.w3.org/International/questions/qa-bidi-unicode-controls)).
62. **Use a real shaping engine** (HarfBuzz or equivalent) for all text, including map labels rendered in GL. Mapbox had to add ICU shaping and bidi to get Arabic labels right ([Mapbox blog](https://blog.mapbox.com/improving-arabic-and-hebrew-text-in-map-labels-fd184cf5ebd1)). Disconnected Arabic letters are an instant "cheap port" signal ([LocalizeDirect](https://www.localizedirect.com/posts/arabic-game-localization)).
63. **Arabic UI font choices with proper shaping:** Noto Sans/Kufi Arabic, IBM Plex Sans Arabic, Tajawal, Cairo, Changa or Reem Kufi for headings ([font guide](https://medium.com/@harbbaraa15/the-comprehensive-guide-for-arabic-web-font-8c6e382a7119), [typography tripwires](https://appscreenshotstudio.com/blog/arabic-app-store-screenshots-4-typography-tripwires-2026)). Pair each Arabic face with a Latin face of matching weight and x-height.
64. **Never letter-space, italicise or slant Arabic.** Letter-spacing breaks joins, and fake italics slant the connections wrongly. Use weight or a second typeface for emphasis ([Thoughtbot](https://thoughtbot.com/blog/do-not-use-obliques-in-arabic.md), [Arabic typography guide](https://freezil-website-wjfnk.kinsta.page/blog/arabic-typography-guide.html)).
65. **Arabic needs more vertical room:** add 10–15% line height over Latin and avoid Arabic body text under ~14 pt equivalent (same guide). Budget about 25% more horizontal space for Arabic strings.
66. **Avoid gender traps in UI text:** address the player with verbal nouns (masdar), e.g. "شراء" (buying), not "اشترِ" (masculine "buy!"), so text fits everyone ([PocketGamer.biz](https://www.pocketgamer.biz/cruise-to-the-east-how-to-successfully-localize-a-game-into-arabic/)). If the player chooses a leader gender, use it for story and news text.
67. **Arabic plurals have six forms** (zero, one, two, few, many, other). Use ICU MessageFormat with all six. "3 دبابة" is wrong, "3 دبابات" is right, and "دبابتان" (two tanks) is better than "2 دبابة" ([Loxily](https://loxily.com/en/blog/icu-plural-game-localization)).
68. **Modern Standard Arabic for UI; a light touch of dialect only in flavour lines** (news chatter, soldier barks), and only if reviewed by native speakers. Write a style guide so dialect doesn't creep in ([PocketGamer.biz](https://www.pocketgamer.biz/cruise-to-the-east-how-to-successfully-localize-a-game-into-arabic/)).
69. **Translators must play the game first**, with context per string (who speaks, to whom, max length). Minecraft Legends had to pull its Arabic version after layout and translation errors ([LocalizeDirect](https://www.localizedirect.com/posts/arabic-game-localization)).
70. **Arabic has no capital letters,** so mark proper names consistently (e.g. quotation marks «» or bold) in long texts (same source).
71. **Arabic country and city names from a trusted standard** (UN Arabic names, Arab League usage, local official names), with the commonly used everyday form. "الولايات المتحدة" not a literal translation.
72. **Map labels: Arabic labels slightly larger** than Latin at the same zoom (Arabic counters are smaller at equal point size), with halo and no tight curves (see #33).
73. **Arabic has no casual abbreviations like "Res." or "Def.".** Never truncate Arabic words with "…" to fit a button. Design buttons to fit full words, and decide large-number short forms once in the style guide (e.g. "12.5 ألف" / "3 مليون" in Arabic, "12.5K" in English).
74. **Test mixed strings:** Arabic sentence + English unit nickname + number + percentage + player name. This is the single most common broken-RTL bug.
75. **Arabic voice lines recorded natively**, not translated scripts read stiffly. Arabic lines run longer than English, so time cut-scenes for Arabic ([LocalizeDirect](https://www.localizedirect.com/posts/arabic-game-localization)).
76. **Culturally aware live events:** Ramadan (quieter schedules, iftar-time events), Eid, national days. Respect norms: no alcohol, gambling imagery or pork references, and modest character art ([PocketGamer.biz](https://www.pocketgamer.biz/cruise-to-the-east-how-to-successfully-localize-a-game-into-arabic/)).
77. **Respect the local weekend:** most Arab countries rest on Friday–Saturday, the UAE moved to Saturday–Sunday in 2022, and Europe and the Americas use Saturday–Sunday. Schedule "weekend events" per region, not globally.
78. **Date formats:** offer Gregorian and Hijri display for event calendars in the Arabic locale.
79. **News system in natively written Arabic**, not translated from English. The owner already flagged CoN's English-to-Arabic news as feeling off.
80. **Arabic chat must work perfectly:** RTL input, mixed-language messages, emoji, and bidi isolation of names and links.
81. **Native-speaker QA pass on every build that touches text**, not just at launch.

## 5. Visual polish and "juice"

82. **Every state change animates** with easing (in, out or both), never instant pops ([GameAnalytics on juice](https://www.gameanalytics.com/blog/squeezing-more-juice-out-of-your-game-design)). Cheap games teleport; premium games ease.
83. **Battles look like battles:** when armies meet, show tracer fire, smoke, small explosions and units recoiling, not two icons sitting next to each other. Dull auto-battles are Call of War's #1 complaint ([F2P.com](https://www.f2p.com/?p=36088)).
84. **Hold key frames on impact:** a few frames of pause plus a flash on a kill makes destruction land (GameAnalytics).
85. **Gentle screen shake only for big moments** (artillery barrage nearby, missile hit on your city). Never constant; respect the reduced-motion setting.
86. **Lingering battle scars:** craters, smoke columns and burned ground stay on the map for a few hours, so the world remembers the war.
87. **Living map ambience:** cloud shadows drifting, ship wakes, aircraft contrails, city lights at night. These are cheap shaders that make the map breathe.
88. **City growth is visible:** sprites change as buildings upgrade (matches the owner's per-level building sprites plan).
89. **Consistent lighting direction** across every unit and building sprite. Mixed shadows instantly reveal art stitched together from different sources.
90. **Unit art in one rendering style:** same camera angle, same lens, same colour grade. Mixed styles were the root of the owner's "photo cut-out" disappointment.
91. **Damage states on units:** a health bar under 50% adds smoke; under 25% adds fire.
92. **Micro-animations on idle UI:** subtle shimmer on a ready button, a breathing glow on research completion. Keep them under 2 per screen.
93. **Typography hierarchy:** max 2 typefaces per script, max 4 sizes per screen, numbers in tabular (fixed-width) digits so timers don't wobble.
94. **Premium transitions:** a short (150–250 ms) shared-element zoom when opening a city or unit from the map.
95. **No placeholder art in release builds.** One grey box in a shop screenshot undoes a hundred polished screens.

## 6. Sound design

96. **Separate volume sliders** (music, effects, voices, UI, alerts) and a master mute. CoN reviewers complain that effects are too loud with no volume control and that there's no music ([GameBrain](https://gamebrain.co/game/conflict-of-nations-ww3)).
97. **Sound categories players can learn:** each family (UI, economy, combat, alerts) has its own recognisable timbre, and specific events within a family are distinct, as League of Legends does ([Game Developer](https://gamedeveloper.com/audio/how-i-league-of-legends-i-communicates-action-through-audio-clues)).
98. **One unified click for generic buttons** (owner requirement), plus distinct sounds for the market, bombardment, bombing, infantry battle, unit death, kill, and important alerts like "ship spotted".
99. **Alerts carry information through sound alone:** a player with the phone face-down should be able to tell "enemy spotted" from "construction done" (same source).
100. **Thematic sounds that suggest function:** a coin chime for trade, a radio crackle for intel, a siren for an air raid (same source).
101. **Silence before big moments** (a half-second dip before a nuclear launch sound) for drama ([GameAnalytics](https://www.gameanalytics.com/blog/squeezing-more-juice-out-of-your-game-design)).
102. **Ambient soundscape under the music:** distant wind, radio chatter, gulls at sea zoom, city hum at city zoom (same source).
103. **Adaptive music:** calm when at peace, tense when an enemy is near, battle stems during combat. Change it at phrase boundaries, never abruptly.
104. **Spatial audio on the map:** battles off-screen to the left are heard slightly to the left.
105. **Unit acknowledgement barks** in the region's language flavour (Arabic for MENA units, etc.), short, with variety (4–6 per action) so they never repeat back-to-back.
106. **Mix ducking:** alerts and voices duck the music automatically.
107. **Compression on mobile speakers:** test every sound on a cheap phone speaker. Bass-only explosions vanish there, so add mid-range crack.
108. **Audio respects the phone:** pause when a call comes in, follow the silent switch and Do Not Disturb, and resume smoothly.
109. **Short sounds for frequent events, longer and richer sounds for rare events** (the same rule as for haptics).

## 7. Haptics

110. **Less is more:** frequent events get very subtle haptics, important events stronger ones. Users who find haptics excessive switch them off entirely ([Android haptics principles](https://developer.android.com/develop/ui/views/haptics/haptics-principles)).
111. **Prefer crisp predefined effects** (`EFFECT_CLICK`, `HapticFeedbackConstants.CONFIRM`) over legacy one-shot buzzes, which keep ringing 20–50 ms after the input and feel cheap (same source).
112. **If the only option is buzzy, use none** for touch feedback (same source).
113. **Same haptic for the same kind of action everywhere** so players learn the language (same source).
114. **Haptics in sync with sound and visuals.** Out-of-sync feedback makes the phone feel broken (same source).
115. **Build-up ticks** when dragging an order line to a target: amplitude rises as it snaps (same source).
116. **Distinct "heavy" haptic only for critical alerts** (city under attack, nuke detected), with a setting to turn haptics off by category.

## 8. Notifications and respecting real life (asynchronous play)

117. **Player-controlled notification categories** (attack on my city, unit arrived, research done, alliance chat, market) with sensible defaults, mostly off except attacks.
118. **Quiet hours by default** (e.g. 23:00–07:00 local), with an exception only for "your capital is under attack" if the player opts in.
119. **Never push while the player is in the game.** Use in-game toasts instead ([Pushwoosh](https://www.pushwoosh.com/blog/game-app-push-notifications/)).
120. **No repeated pushes on the same topic**, even if unopened ([Pushwoosh](https://www.pushwoosh.com/blog/game-app-push-notifications/)).
121. **Smart batching:** "3 units arrived, research finished" as one push, not three.
122. **Every push deep-links** to the exact place on the map or panel.
123. **Notification text in the player's language and digits**, with names isolated for bidi (section 4).
124. **Offline protection model inspired by Clash of Clans:** after a heavy defeat, a short protection window, and a "village guard" style buffer against disconnects ([TouchArcade](https://toucharcade.com/2015/11/24/clash-of-clans-town-hall-11-update-specifics-on-how-shields-work/)). Adapt it carefully to real-time wars (e.g. a short "regroup" window for newly lost cities).
125. **"While you were away" report** on return: the 3–5 most important events, ranked, each with one tap to act. Not a 200-line log (the owner dislikes CoN's news reporting every small detail).
126. **Deployable computer-controlled commanders** for night or work hours, with clear rules ("defend only", "hold the line", "counter-attack within 50 km"). This solves CoN's "must be online 24/7" pain ([GameBrain](https://gamebrain.co/game/conflict-of-nations-ww3)).
127. **Day/night speed options per server** (some servers slow down at night in the server's region).
128. **Email or other fallback** only if the player explicitly opts in ([Pushwoosh](https://www.pushwoosh.com/blog/game-app-push-notifications/)).

## 9. Performance and stability

129. **Stability first:** crashes, freezes, black screens and disconnects are CoN's most common complaint ([GameBrain](https://gamebrain.co/game/conflict-of-nations-ww3)). Ship crash reporting and fix the top crash every release.
130. **Cap at 30 fps by default on the map** (60 fps option). 60 fps can use about 1.75× the power of 30 fps ([GameOptim data](https://dev.to/gameoptim/mobile-game-power-optimization-why-30-fps-vs-60-fps-can-double-energy-usage-real-data-breakdown-110n)). A strategy map rarely needs 60.
131. **Match the display refresh rate to the frame rate** (frame pacing, e.g. Swappy). 90/120 Hz screens running at 30 fps waste battery ([Android power guide](https://developer.android.com/games/optimize/power)).
132. **Use the Android Thermal API** to lower effects before the phone throttles (same source).
133. **Honour Android Game Mode** (performance versus battery) (same source).
134. **Prefer Vulkan where available** (same source).
135. **Tile-streamed satellite map** with compressed textures (ASTC/ETC2), loaded by zoom level and on-screen area only.
136. **Instancing and atlases for units:** thousands of units in one draw call. Rusted Warfare is praised for running huge unit counts smoothly even on modest hardware ([review digest](https://vaporlens.app/app/647960/rusted_warfare_rts)).
137. **Low-end device mode:** fewer particles, no cloud shadows, simpler water. Auto-select it on first launch by device class.
138. **Cold start under 5 seconds to the map** on a mid-range phone. Defer non-critical downloads.
139. **Small install, assets on demand:** keep the initial APK lean and download high-res unit art per region as needed.
140. **Network resilience:** queue orders while offline and sync on reconnect, with clear "pending" markers. Never lose an order silently.
141. **Measure power, not only frame time,** with the Android Studio power profiler ([Android power guide](https://developer.android.com/games/optimize/power)).
142. **Lag-free late game:** HOI4's late-game lag ruins its best part ([HOI4 digest](https://vaporlens.app/app/394360/hearts_of_iron_iv.md)). Load-test 100-player servers on day 20+ states, not just fresh maps.

## 10. Combat clarity, reports and feedback

143. **Battle reports in three layers:** a one-line headline ("Victory at Basra: enemy lost 2 tanks, you lost 1 IFV"), a summary card, and full detail on demand.
144. **Explain why:** each report shows the top 3 factors (terrain +20%, air support, doctrine +5%). This turns defeats into lessons.
145. **Replays of big battles** (a short time-lapse on the map).
146. **Kill and loss counters per unit** (veteran badges after N kills) for attachment and pride.
147. **Clear damage numbers** that float up briefly in battle, colour-blind safe (with ▲▼ icons).
148. **Predicted versus actual:** show the pre-battle estimate next to the result, to build trust in the forecast.
149. **No hidden modifiers:** every bonus that affects combat is visible somewhere on the unit or battle card.
150. **Nuclear and strategic strikes get their own sober presentation** (a warning siren, a slower cinematic, a clear diplomatic consequence). Call of War players hate unpenalised nukes ([F2P.com](https://www.f2p.com/?p=36088)).
151. **Spotting alerts with a mini-thumbnail** of what was spotted ("Destroyer spotted near Hormuz").
152. **Supply lines visible and simple:** a coloured line showing healthy, strained or cut supply, instead of hidden numbers.

## 11. Social, diplomacy and communication

153. **Ping system for coalitions:** tap the map to say "attack here", "defend here", "need air cover", with automatic localised text. This works without typing or voice, as Apex proved ([Game Developer](https://gamedeveloper.com/design/respawn-played-with-muted-mics-to-get-i-apex-legends-i-smart-comms-system-just-right)). EA's marketing chief said the ping system was designed "to eliminate opportunity for toxicity" and partly credited the positive community for the game's "excellent" retention ([MMOBomb](https://mmobomb.com/news/ea-apex-legends-retention-due-part-ping-system-reducing-toxicity)).
154. **Pings auto-translate:** an Arabic player's ping shows in English for an English ally.
155. **Structured diplomacy proposals** (peace, trade, right of passage, shared vision) as clear cards with terms and expiry, not free text.
156. **Treaties show a reliability history** ("broke 2 treaties this match"). Social pressure without bans.
157. **Coalition shared planning layer:** allies can draw arrows on a shared overlay.
158. **Chat moderation:** a profanity filter in Arabic and English (Arabic filters need dialect variants), mute and report in one tap.
159. **Rich in-game news as diplomacy:** official statements, propaganda and outlet bias (the owner's plan). Let players issue statements from templates.
160. **Friend invites into the same server** and "play with friends" matchmaking. Rusted Warfare players say playing with friends is the highlight ([review digest](https://vaporlens.app/app/647960/rusted_warfare_rts)).
161. **Mentor badge:** experienced players who help newcomers in coalition get cosmetic recognition.
162. **End-of-match recap shared as an image** (map time-lapse, stats) for social media. Free marketing.

## 12. Retention without pay-to-win

163. **Session-friendly pacing:** offer speed rounds (4×, 10×) alongside classic. Call of War players asked for Civ-style speed settings ([F2P.com](https://www.f2p.com/?p=36088)); CoN players complain about hours-long waits ([GameBrain](https://gamebrain.co/game/conflict-of-nations-ww3)).
164. **Matches that end:** clear victory conditions and a hard maximum length, so a match never rots in an inactive endgame.
165. **Inactive players replaced by a competent computer-controlled player** after a grace period, so coalitions don't collapse and borders don't become free real estate.
166. **Season profile:** a cross-match record (wins, ranked rating, achievements, medals) that persists and gives long-term purpose.
167. **Cosmetic progression earned by playing** (flags, unit skins, HQ decorations), never stat boosts.
168. **Ranked ladders with skill-based placement**, so new players fight new players.
169. **Daily "commander's briefing":** one optional small challenge per day, no streak punishment. Missing a day costs nothing.
170. **Quarterly major updates, small weekly live events.** Polytopia's studio ships a major update each quarter and discards about 90% of tested ideas ([PocketGamer.biz](https://www.pocketgamer.biz/aggressive-mobile-game-monetisation-pushes-loyal-players-to-churn-says-battle-of-polytopia-ceo)).
171. **Short, finishable modes for busy days** (30–60-minute skirmish). Polytopia's ~30-turn games are its secret ([COGconnected](https://cogconnected.com/review/battle-polytopia-review/)).
172. **Comeback mechanics for losing players** (partisans, foreign aid offers, a coalition-joining window), so losing early still has a meaningful role.

## 13. Fair monetisation

173. **No paid speed-ups of combat-relevant timers, and no paid resources.** These are the core of pay-to-win complaints for CoN and Call of War ([GameBrain](https://gamebrain.co/game/conflict-of-nations-ww3), [F2P.com](https://www.f2p.com/?p=35989)).
174. **Sell non-consumables:** cosmetics, extra country-art sets, quality-of-life conveniences that don't affect combat, and one-time unlocks (the owner's permanent alliance purchase). Polytopia sells only non-consumables, prices transparently, and has 20 M+ organic downloads ([PocketGamer.biz](https://www.pocketgamer.biz/aggressive-mobile-game-monetisation-pushes-loyal-players-to-churn-says-battle-of-polytopia-ceo)).
175. **Show real-money prices, not just gems.** Players list hidden real prices and multiple currencies as problematic ([Tampere Play Lab summary of Petrovskaya & Zendle](https://blogs.tuni.fi/playlab/game-research-highlights/spenders-game-problematic-monetisation-as-seen-by-players/)). If a premium currency exists, have only one, and show the local-currency equivalent next to it.
176. **No pop-up offers interrupting play.** Shop offers live in the shop. CoN reviewers specifically hate frequent purchase pop-ups ([GameBrain](https://gamebrain.co/game/conflict-of-nations-ww3)).
177. **No loot boxes.** If any randomised item is ever sold, Google Play requires disclosing the odds before purchase ([Fenwick](https://fenwick.com/insights/publications/google-play-now-requires-disclosure-of-loot-box-odds)), and some countries restrict them.
178. **Never charge for basic quality of life** (inventory space, order queues, essential info). Players rank this among the most problematic practices ([Tampere Play Lab](https://blogs.tuni.fi/playlab/game-research-highlights/spenders-game-problematic-monetisation-as-seen-by-players/)).
179. **No FOMO countdown offers** or "last chance" stacking (same source).
180. **Preview cosmetics before buying** (3D or animated view on the actual map).
181. **Optional subscription only for cosmetics and convenience,** clearly listed. Gold-only rounds should not exist as a pay barrier ([F2P.com](https://www.f2p.com/?p=35989)).
182. **Fair-play guarantee page in the store listing and in game:** "Money never buys power. Here is what we sell."
183. **Gifting with anti-abuse limits** (cosmetics only, account age minimum).
184. **Regional pricing** (purchasing-power-adjusted for Egypt, Morocco, Jordan and others), and support for local payment methods popular in MENA (carrier billing, local wallets).
185. **Refund-friendly tone:** a clear "contact us" path in the shop. Generous fixes build loyalty.

## 14. Anti-cheat and multi-account ("farm") detection

186. **Don't ban on shared IP alone.** Families, cafés, dorms and mobile carriers share IPs, so innocent players get hit while abusers just use VPNs ([WarEra analysis](https://warera.io/articles/why-same-ip-bans-are-a-weak-and-outdated-way-to-detect-multi-accounts--90c13f)).
187. **Layered risk score** from device fingerprint, login timing, account creation clusters, session switching, and the resource-transfer graph (same source).
188. **Transfer-graph analysis:** flag one-way flows (account A repeatedly gifting or selling below market to account B), accounts that never fight each other, and "suicide" accounts that hand cities over (same source).
189. **Behavioural fingerprints for account sharing:** compare an account's recent play style with its own baseline. A League of Legends study detected 80% of deliberate style changes with server logs only ([arXiv 2608.09132](https://arxiv.org/pdf/2608.09132)).
190. **Delay or cap large transfers** between accounts that share technical signals, instead of instant bans ([WarEra](https://warera.io/articles/why-same-ip-bans-are-a-weak-and-outdated-way-to-detect-multi-accounts--90c13f)).
191. **Human review before permanent bans**, with an appeal path (same source).
192. **New-account restrictions:** no gifting or market sales below a world-price floor until the account has played X hours or finished a match.
193. **Market price floors and ceilings** relative to the world price (the owner's plan), which also makes feeding via the market useless.
194. **Server-authoritative simulation:** the client only sends orders and never decides outcomes. This makes most hacks impossible.
195. **One account per player per server rule, stated clearly.** CoN removes multi-accounters from the round and may suspend all accounts ([CoN rules](https://conflictnations-wiki.pages.dev/Rules.html)).
196. **Declare-a-household option** for families on one Wi-Fi, which lowers the IP weight but doesn't exempt them from transfer analysis.
197. **Publish ban waves (counts, not names)** so honest players see enforcement happening.

## 15. Live-ops modes, events and marketing

198. **A rotating playlist of distinct maps and modes**, following CoN's event maps (Overkill 100 players, Blood & Oil 50 players with strategic sites, Domination control points, Rising Tides) ([CoN campaign types](https://conflictnations-wiki.pages.dev/Campaign_Types.html)), each with one clear twist:
    - **100-player World War** (flagship, classic speed)
    - **Speed Round** (4× or 10×, finishes in 1–3 days)
    - **Blitz Weekend** (2-hour skirmish, ranked)
    - **Nuclear Round** (nukes researched early, but strong fallout and diplomacy penalties)
    - **Resource War** (oil and rare-earth sites decide victory)
    - **Regional theatres** (Middle East, Europe, Pacific) for shorter matches
    - **Coalition vs Coalition** (fixed teams, tournament format)
    - **Historical "what-if"** scenarios
199. **Each mode has its own short explainer card** (three lines and an image) before joining.
200. **Seasonal ranked ladder per mode**, reset quarterly with cosmetic rewards.
201. **Community tournaments with in-game brackets** and spectator mode.
202. **Event calendar visible weeks ahead**, so coalitions can plan.
203. **Regional server start times** that fit Gulf, Levant, Maghreb and Europe evenings.
204. **Limit concurrent events to 1–2**, as CoN does with its event maps (same source). Too many split the player base.
205. **Post-event stats and a "hall of fame"** for winners.
206. **Honest ads:** gameplay shown in ads must be the real game. The UK ASA ruled war-strategy ads misleading for showing features not in the game, and small-print disclaimers don't fix it ([ASA](https://asa.org.uk/news/don-t-hate-the-player-hate-the-game-play-misleading-gameplay-in-videogame-ads.html)). Misleading ads poison reviews ("this isn't the game in the ad").

---

## Top 25 highest-impact tips

1. **Stability before everything:** crash reporting, fix the top crash each release (#129). CoN's #1 complaint.
2. **Money never buys power:** no paid speed-ups of combat timers, no paid resources (#173). This removes the biggest complaint category for CoN and Call of War.
3. **Design in Arabic first, with a full RTL mirror** that knows what not to mirror (#56–58).
4. **Real Arabic text shaping and bidi isolation everywhere**, including map labels and chat (#61–62). Broken Arabic = instant "cheap port".
5. **No pop-up commander tutorials;** teach through the world plus just-in-time hints after measured stuck time (#1–2).
6. **Order queues, standing orders and deployable computer-controlled commanders** so nobody has to be online 24/7 (#40, #126).
7. **Zoom-based levels of detail and collision-aware labels** (#17–19). The map is the game; clutter kills it.
8. **Colour-blind-safe relations** (colour + shape, blue/orange default, presets) (#20–21).
9. **Battles that look and sound like battles,** not icons parked side by side (#83).
10. **Outcome preview before committing an attack** (#9). Teaches combat and builds trust.
11. **Nested tooltips plus an in-game encyclopedia** so the game is learnable without YouTube (#5, #7).
12. **Separate volume sliders, a distinct per-event sound language, and music** (#96–99).
13. **30 fps cap with frame pacing and the Thermal API**: cool phone, long battery life (#130–132).
14. **Speed rounds and matches with a guaranteed end** (#163–164).
15. **Inactive players replaced by a competent computer-controlled player** (#165).
16. **Multi-account detection by layered risk score and transfer graphs, not IP bans** (#186–190).
17. **Real prices shown, one currency at most, no interrupting offers, no loot boxes** (#175–177).
18. **"While you were away" ranked summary**, not an exhaustive log (#125).
19. **Coalition ping system with auto-translation** (#153–154).
20. **Western digits by default with an Eastern-digit option; never flip prices or timers** (#59–60).
21. **Six-form Arabic plurals and gender-neutral masdar UI text** (#66–67).
22. **Quiet hours and category-controlled notifications; no pushes while in game** (#117–119).
23. **Battle reports that explain why** (top 3 factors, predicted vs actual) (#144, #148).
24. **Every tap target ≥ 48 dp, ≤ 2 taps from the map for common actions** (#37–38).
25. **One art style, one lighting direction, no placeholder art in release** (#89–90, #95). The small things that make everything look cheap.
