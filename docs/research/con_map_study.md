# World map study: Conflict of Nations vs ours

Written 11–12 Nov 2026 from about 150 CoN screenshots the owner took on his phone (1080 × 2400). All numbers below
were measured from those images, not guessed. CoN is the reference. The rule for this study: copy what CoN does
best (land, sea, colours, balance) exactly; change only text and symbols (for legal distance); make a change only
when it is clearly better than CoN, never just to be different.

## 1. Scale (how big the world is on screen)

Measured with known distances between real cities in the screenshots:

| CoN view (screenshot) | screen pixels per km | what you see |
|---|---|---|
| world (Europe + Africa) | ~0.09 | half the world, country names only |
| continent (Eurasia) | ~0.21 | country names, borders, coastal sea bands |
| region (Caspian / Iran) | ~0.5 | big country names, woods and mountains readable |
| country (Algeria, India south) | ~0.5–0.75 | province names with level, e.g. "وهران(5)" |
| province (Iraq close) | ~1.5 | city patches, resource pins, province lines |
| city (Sydney close) | ~4–5 | the city as a 3D block, buildings, port |

- CoN cities are **exaggerated about 4–5 times**: Baghdad's patch is about 300 px across at 1.5 px/km, so about 200 km wide.
- Our map uses the same real geography. At latitude 33° one world pixel is about 4.1 km, so at our zoom z on a 1080-px
  phone screen: px/km ≈ 0.585 × z. That puts CoN's views at our z ≈ 0.15, 0.36, 0.85, 1.0–1.3, 2.5 and 7–8.
- **Ours vs CoN:** the zoom range matches. Our capital patch is 24 world px radius, about 200 km wide, so it also
  matches. What did not match: the deepest zoom (ours stops at 7, CoN goes a little further), and at mid zoom our
  names and lines were smaller than CoN's (see 5).

## 2. Land

| feature | CoN (measured) | ours before tonight | decision |
|---|---|---|---|
| ground | calm, softly mottled; fine-grain contrast tiny (luminance std 1.6–3 in flat land) | busy: relief wrinkles and texture everywhere | copy: calm ground |
| mountains | only on real ranges (Zagros, Alborz, Atlas, Caucasus); broad, soft, painted ridges; plains totally flat | crumpled noise over every country | copy: ranges only, broad and soft |
| woods | separate dark clumps, about 100–150 km across, roughly 10–20% of land; dense only in real forests (taiga, Congo) | first a carpet of trees, then too many clumps | copy: few clumps, dense only in real forest |
| desert | same colour as the rest of the owner's land, just smoother | false "forests" on Gulf coasts | fixed: no forest inside deserts |
| colour | one hue per owner, terrain in light and dark only | done (measured colour stops) | keep, never change |
| coast | crisp, with a thin dark rim on the water side | soft, slightly wobbly when close | keep the rim, smoother coast at deep zoom |

Measured land colours (median): own green (100,159,79), stranger slate in flat desert (16,36,31), stranger in Iraq
(39,61,52), stranger mountains (27,46,41), enemy red (61,20,16), ally pale olive (from the Algeria shot, earlier stops).

## 3. Sea

| feature | CoN (measured) | ours | decision |
|---|---|---|---|
| coastal water | lighter grey-blue band, median (80,109,131) open coast / (64,90,103) enclosed seas; soft edge; about 250–380 km wide | band of about 255 km, round halos round islands (fixed) | copy |
| deep water | (21–25, 54–55, 81–83), with big slow darker patches (depth) | done tonight | copy |
| ripples | fine wind ripples, low contrast, everywhere | yes, a little strong | calmer |
| sea zones | network lines and "≈" node marks between sea zones | none yet | later, with the game (it is gameplay) |

## 4. Borders and lines

| feature | CoN | ours before | decision |
|---|---|---|---|
| country borders | light grey-white line, about 3–4 px on a 1080 screen, dark soft edge, between **all** countries | most were missing (raster gaps hid shared borders) | fixed in the build; draw all |
| province borders | thin light lines, about 2 px, clearly visible from country zoom in | almost invisible | stronger now |
| enemy front | red line with a red glow | yes | keep |

## 5. Names (text is where we differ on purpose)

| feature | CoN | ours | decision |
|---|---|---|---|
| country names | big (about 90 px tall at region zoom), sized by country, curved along the land, white with a soft shadow | straight, sized by country | keep ours straight (legal distance), but as big as CoN's |
| city names | about 45–50 px tall at every zoom, with the level, "بغداد(6)", slightly tilted | about 34 px, no level | bigger (~48 px), level later from game data |
| font | rounded Arabic sans | IBM Plex Sans Arabic | keep Plex (owner's choice) |

## 6. Cities

| feature | CoN | ours | decision |
|---|---|---|---|
| far | no city symbols at all, names only | names only (stars removed) | keep |
| mid | dark textured patch in the owner's colour, irregular soft outline | patch, round with a ring | irregular outline, no ring |
| close | the city as 3D blocks, buildings, port, airport, in the owner's colour | regional blocks + buildings | keep, with plots for the player's buildings |
| crowding | small countries still get room | same size everywhere (fixed tonight: size by country and neighbours) | keep the fix |
| our own touch | — | capital landmark model (mosque, cathedral, capitol, pagoda) | keep, scaled to the room |

## 7. Honest list: where we can be better than CoN without changing the concept

1. **Legibility of small Arab states.** CoN crowds the Gulf (Qatar, Bahrain, UAE names overlap). Our no-overlap layout plus city size by room is already better here.
2. **Arabic text quality.** CoN's curved text breaks letter joins in places and squeezes names. Straight, well-spaced Plex reads better on a phone.
3. **Real geography where it matters.** CoN's woods and mountains are decoration. Ours come from real forest and elevation data, so a player can trust that the Zagros is mountains (good for future terrain combat bonuses).
4. **Region style.** Our cities and landmarks change by region. CoN uses one style everywhere.

Not better, so not changing: colours, sea, the calm ground, the dark rim on coasts, and the city patches. Those are CoN's strengths and we copy them.

## 8. Fix order for tonight

1. Borders: all countries, CoN style. (build)
2. Calm land: ranges only, few woods, no desert forests. (build)
3. Names and lines at CoN's size: city names about 48 px, province lines visible. (viewer)
4. City patches: irregular outline, darker, no ring, sized by room. (viewer)
5. Deep zoom a little further, with sharper painting when very close. (viewer)
6. Side-by-side at matched px/km for: Iraq close, Caspian region, Algeria country, India south, Australia east. An independent reviewer judges; anything worse than CoN is redone.
