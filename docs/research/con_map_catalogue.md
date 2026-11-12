# CoN map catalogue: measured, layer by layer, zoom by zoom

Written 12 Nov 2026. This extends `con_map_study.md` (read that first; numbers there are not repeated unless refined).
Source: the owner's ~155 phone screenshots (1080 × 2400), of which ~100 show the map, plus the 20 normalised
study shots. Everything below was measured with Python (PIL / numpy / scipy / scikit-image / OpenCV) and then
checked by eye on 1:1 and 2–4× crops. Colours are sRGB as stored in the JPEGs (JPEG noise is about ±3).
"L" = luminance 0.299R + 0.587G + 0.114B. "px" = pixels on the 1080-wide phone screen.

Screen layout used for all measuring: map area is y = 316…2258 (status bar above, tab bar below), minus the
left icon stack (x < 175, y < 920), the gold offer badge (x > 880, y < 700) and the bottom-right unit button.

## 0. Zoom ladder (what is on screen at each step)

The best evidence is the owner's new Afghanistan/Pakistan series: six shots of the same area at six zooms.
SIFT registration between neighbours gives exact zoom ratios (2.07×, 2.52×, 1.77×, 1.33×, 1.51×) with
**0.0° rotation and one uniform scale**. So the camera is straight top-down (orthographic); there is no tilt and no
perspective. The px/km below come from fitting 9 city positions to their real coordinates (Mercator) in the
1.18 px/km shot and chaining the ratios. Long baselines agree to ±7% (median 1.18 px/km over 25 city pairs > 500 km).

| zoom name | px/km (lat ~32°) | screenshot | country names | city names | borders | province layer | pins / markers | terrain look |
|---|---|---|---|---|---|---|---|---|
| world | 0.09–0.13 | 74ebc1a2, apac | yes, H 15–27 px | no | country 2.5–3 px | no | no | dark land, coastal halo, big sea depth patches, map edge visible |
| continent | 0.21–0.26 | a4b784e6, eurasia | yes, H 25–47 | no | country 3 px | no | no | forest clumps readable as dots |
| region | ~0.5 | caspian, tr_iq | yes, H 55–80 (biggest) | no | country 3.5 px | no | no | clumps and mountain ridges clear |
| country | 0.6–0.75 | 716496a7, algeria, india_s | **gone** | yes, with level "(5)", H ≈ 35 | country 3.5 px | 0.66: none; 0.75: sea/land network and ≈ marks start | 0.75: first resource pins | — |
| province (far) | ~1.2 | 945c1ce6 | no | H ≈ 41 | country 4.5 px | faint province borders (+35 L), network lines, centre markers | pins, small 3D buildings | city patches with blocks |
| province (near) | 1.5–1.6 | 13021611, iraq_close | no | H ≈ 46 | country 5–5.5 px + glow | **bright** province borders (+90 L) | all | relief, farm fields appear |
| close | ~2.4 | 51559e37 | no | H ≈ 55 | country 7 px + glow | bright, 3–3.5 px | all | photo-like relief |
| city | ~4–5 | sydney, Alice Springs shots | no | H 55–90 | — | — | 3D city, port, buildings | city drawn as 3D blocks |

Rules that come out of this:
- **Country names and city names never show together.** Country names vanish between 0.5 and 0.66 px/km, exactly
  when city names appear.
- Text, pins, markers and line widths are **screen-sized**: they grow only slowly while the map grows 26×.
  City name height fits H ≈ 41 × (z / 1.18)^0.35 px. Markers grow ~7% per 1.33× zoom step.
- The province layer fades in over ~1.2 → 1.5 px/km (borders go from +35 to +90 L contrast).

## 1. Land colour by owner (median, p10, p90)

Measured over all land pixels of each owner class, labels/lines/coast masked out.

| owner | world (0.09–0.13) | continent / region (0.2–0.5) | country (0.6–0.75) | province (1.2–2.4) | city close |
|---|---|---|---|---|---|
| own (green) | (115,183,91) p10 (96,147,74) p90 (138,202,106) | (98,159,78) p10 (80,128,62) p90 (119,172,90) | (97,154,78) p10 (77,118,58) p90 (117,169,90) | (99,154,79) p10 (83,133,66) p90 (117,164,88) | (109,152,86) |
| enemy (red) | (80,28,22) p10 (69,21,17) p90 (99,37,28) | (68,23,16) p10 (58,19,12) p90 (83,29,22) | (65,21,15) p10 (50,12,9) p90 (82,29,23) | (59,18,13) p10 (32,3,1) p90 (104,36,34) | Sydney (50,19,16) |
| ally (pale olive) | (109,129,91) p10 (72,86,66) p90 (134,158,107) | — | — | — | — |
| neutral / stranger (dark slate-green) | (30,54,46) p10 (21,40,35) p90 (44,67,59) | (26–29,48–50,41–42) p10 (16,34,29) p90 (40–48,61–66,54–60) | (19–23,41–43,33–37) | (16–31,34–53,29–45) | (39,49,53) |

- Each owner is **one hue**; terrain changes only light/dark and texture, never hue.
- Land gets slightly **darker as you zoom in** (neutral L: 46 world → 41 continent → 37 country → 28–31 close). Red does
  the same (L 43 → 34 → 28).
- Own green is far brighter (L ≈ 130) than everything else (neutral L ≈ 40, red L ≈ 35). Ally olive sits between (L ≈ 119).

## 2. Terrain inside the land

### 2.1 What the texture is
The land is one painted, satellite-like texture (canopy, relief, fields) tinted by the owner colour. Even "smooth"
ground carries a very low-contrast leafy mottle (visible only when contrast is stretched). Three looks sit on top:

| look | how it looks | measured colour (neutral / green / red) |
|---|---|---|
| smooth ground | flat, soft mottle, small-patch std of L 3–6 | (30,51,41) / (100,160,80) / (66,22,16) |
| forest clump | rounded "cauliflower" blob of tree crowns, darker, with light specks on crown tops; on neutral land it is **bluish-teal** (B − G ≈ +4, ground is −11) | (28–33,44–57,42–61) / (88,132,67) / (67,20,14) |
| mountain | painted ridges, lit faces light, valleys dark, only along real ranges | (24–27,42–46,38–41) / — / (60,16,14) |
| farmland (close zoom only) | tan/olive rectangles 15–40 px, appear from ~1.5 px/km | olive/tan, ±10 L from ground |

Forest clumps are about **15% darker** than smooth ground in the same owner colour.

### 2.2 How much of the land is which (random-point sampling, judged by eye, 40 points each)

| shot (zoom, owner) | smooth | forest clumps | mountains | notes |
|---|---|---|---|---|
| eurasia (0.21, neutral) | 67% | 28% | 5% | clumps read as dark dots 20–40 px |
| caspian (0.5, neutral; Zagros/Caucasus) | 60% | 8% | 33% | mountains only on the ranges |
| aus_e (0.6, own + enemy) | 50% | 35% | 15% | green half 48% forest (coastal forest), red half 21% |
| iran_close (1.5, neutral) | 41% | 0% | 59% | 15% of all points fell on city patches; fields visible |

Sampling error at 40 points is about ±8 points. So: smooth ground is always the largest share (40–70%), forest
clumps are 0–35% depending on the real region, mountains appear only where real ranges are.

### 2.3 Clump size
- Single clumps: 20–40 px at 0.21 px/km, 50–80 px at 0.5 px/km, i.e. **~100–190 km across**, irregular, lobed edges.
- In real forest regions they merge into big connected masses (one in aus_e is ~250 × 330 px at 0.6 px/km ≈ 450 km).
- Clumps are separated by smooth ground; they never form an even carpet.

### 2.4 Rivers and lakes (close zoom)
- Big rivers (Tigris, Euphrates, Indus) show from ~1.2 px/km as a dark blue-grey ribbon 10–15 px wide with a lighter edge.
- "≈" marks (three wavy strokes) sit on the river where a network line crosses it (river crossing).

## 3. Sea

### 3.1 Colours (median, p10, p90), open ocean shots where both layers are on screen

| layer | colour | L |
|---|---|---|
| coastal / shallow band | (60,88,106) p10 (43–57,73–86,93–97) p90 (68–79,101–116,122–137) | 80–85 |
| deep water | (13–29,43–58,72–82) p10 (1–14,29–43,57–69) p90 (26–41,58–70,85–94) | 37–52 |
| dark depth patches (inside deep) | (2–16,31–46,59–72) | ~30 |
| enclosed / shallow seas (Black Sea rim, Caspian, Persian Gulf) | band colour (56–61,78–86,89–98) | 75–80 |
| close zoom open sea (1.5 px/km) | deep (14,45,72); band (64,90,103) | 38 / 84 |

### 3.2 The band follows real shallow water, not a fixed buffer
- Band width from the coast varies 3× inside one view (world: IQR 210–630 km, median ~390–450 km;
  India south median 360 km, IQR 257–478 km).
- Visual check: the band fills the whole Sunda shelf (Indochina–Borneo–Java), the Arafura Sea (Australia–New
  Guinea), the Arctic shelf north of Russia, the Persian Gulf, and the rim of the Black Sea, but is narrow off steep
  coasts. That is the real continental shelf. **Use bathymetry (≈ 0–200 m depth), not a distance buffer.**
- Its outer edge is polygonal (straight segments) at close zoom.

### 3.3 Band edge softness
Profile across the band/deep edge (median L, every 5 px):
- a **step of ~20 L over ±5 px** (fairly crisp at every zoom), then
- a **long slow fall of another 10–15 L over 50+ px** into deep water.
Close up, the band behaves like a translucent grey-cyan layer: the ripples still show through it, muted.

### 3.4 Dark depth patches
- Cover 17–32% of deep water in open-ocean views (11% in eurasia). Patch size 200–400 px at 0.09–0.75 px/km
  (very large, cloud-like, soft edged, no hard outline). Almost none at 1.5 px/km (they are larger than the screen).

### 3.5 Ripples
- Short horizontal white-cyan flecks (1–2 px tall, 2–6 px long), wind-ripple pattern.
- Dominant period **23–43 px at every zoom** from 0.09 to 1.5 px/km: the ripple texture is effectively screen-sized.
- Contrast grows when zooming in: std of fine detail 2–6 L at world zoom, 10–12 L at 1.5 px/km.
- Enclosed seas show brighter, more sparkly ripples in their deep centre (Black Sea).

### 3.6 Coastline rim (aligned perpendicular transects, 250–1050 profiles per shot)
| zoom | land side | rim | water side |
|---|---|---|---|
| world → region (≤ 0.5) | flat (L 43–48) | **dark line 1–2 px, L ≈ 32** (−11 vs land, −45 vs water); often looks dashed/broken | soft darkening, water reaches its level by +6–8 px |
| country / close (≥ 0.75) | land brightens slightly toward the coast over ~10 px | **thin light line 1–2 px** (L ≈ 80–82, near-white on green) | small dip (−5 L) at +3…+6 px, then water |
- Close up the coast is visibly **low-poly**: straight segments roughly 40–120 px long at 0.75 px/km (~50–150 km).

## 4. Lines

All bright lines are **white drawn at ~35–40% opacity**, not opaque grey: on neutral land (L 35) they peak at
(117,124,122); on own green (99,154,79) the same lines peak at (152,194,135), i.e. ground + 0.33 × (255 − ground).

| line | zoom | width (FWHM) | contrast | colour / extras |
|---|---|---|---|---|
| country border | world → country (0.09–0.75) | 2.5–3.5 px | +70…+90 L | peak (113–118,123–124,120–122) |
| country border | 1.2 px/km | 4.5 px | +90 | |
| country border | 1.6 px/km | 5–5.5 px | +90 | soft light glow ~8–10 px each side (+15…20 L), then a darker band out to ~20 px |
| country border | 2.4 px/km | 7 px | +100 | same glow |
| province border | 1.2 px/km | 2–3 px | **+35** (faint) | same white, very weak |
| province border | ≥ 1.5 px/km | 3–3.5 px | **+90** | peak ~(120,130,127), no glow |
| network line (province centre to centre) | ≥ ~0.75 px/km | 2–3 px | **+25…+35** | (55,70,66) on neutral land; dead straight |
| sea-zone network line | ≥ ~0.75 px/km | 3.5–5.5 px | +25…+45 | (90–100,117,127) on the band |
| enemy territory edge | 0.6 px/km | 3–4 px | — | bright red (180–186,45–53,40–44) on the enemy side |
| enemy territory edge | ~1.3 px/km | ~8 px incl. glow | — | core (155,21,28) up to (217,81,64), red glow 10–15 px into enemy land |
| map edge | world | 3–4 px core | — | cyan (84,220,231) / (42,164,175), outer glow 3–4 px, crisp inner side |

Province borders are irregular polylines; network lines are straight and run marker to marker, crossing
province borders. The two are easy to confuse at 1.2 px/km because both are faint there.

## 5. Labels

| label | zoom | height H (rotation-aware, 1–99% of ink) | rotation |
|---|---|---|---|
| country | world | 15–27 px | −9…−17° |
| country | continent | 25–47 px (sized by country) | −9…−14° |
| country | region | 55–80 px; long names may curve (some at +10…+20°) | mostly −11…−14° |
| city (with level) | 0.66 | 34–35 px | −14…−16° |
| city | 1.18 | 40–46 px (median 41) | −15° |
| city | 1.57 | 45–51 px (median 46) | −15° |
| city | 2.36 | 54–56 px | −15…−17° |

- "Rotation" = baseline turned clockwise (the right end is lower). City names use a fixed ~−15°; this is a
  style choice, not camera tilt (the camera has no tilt).
- City label placement: centred horizontally under the city (dx −4…−14 px) with the label centre **below the city
  centre by ~62 px at 0.66, ~93 px at 1.18, ~115 px at 1.57 px/km** (about 1.8–2.5 label heights).
- White fill (L ≈ 229), soft dark shadow; no outline box.

## 6. Cities

| zoom | look | size | darkness / texture vs surrounding land |
|---|---|---|---|
| ≤ 0.5 | no symbol at all | — | — |
| 0.66 | dark textured blob, looks like a forest clump | ~100 px | — |
| 1.18 (neutral) | bluish dark patch of tiny blocks | radius ~80 px (≈ 135 km across) | L −15…−18%, B > G (19–21,37–39,38–40) vs ground (25,47,39), fine texture 2× (std 7.5–9.4 vs 4–5) |
| 1.5 (Baghdad, neutral) | dense block patch, irregular soft outline | ~200–300 px | L −10% (45–49 vs 50–53), texture std 12–16 vs 10 |
| ~2 (own green city) | cluster of 3D blocks with light tops and dark shadows | radius ~160–175 px | L −10% (119–123 vs 135), texture std 10–11 vs 3–4 |
| 4–5 (Sydney) | full 3D city in owner colour, port, airfield | fills screen | — |

Cities are spread apart from their real positions: city pairs closer than 250 km are drawn at 1.3–2.4× the
true distance (Kabul–Jalalabad: 118 km real, drawn as 240 km), while pairs over 500 km are accurate to ±7%.

## 7. Afghanistan / Pakistan provinces (new shots)

Scale: 945c1ce6 = 1.18 px/km, 13021611 = 1.57, 51559e37 = 2.36 (see section 0). Kabul–Kandahar is drawn 519 px
at 1.18 px/km = 439 km (real 458 km). Kabul–Jalalabad is drawn 283 px = 240 km (real ~118 km): spread apart.

| quantity | measured |
|---|---|
| province area (interior polygons, 24 polygons in two shots) | median **15,500 km²** (IQR 12,000–23,000); mean ~17,000 km² once three merged pairs are removed |
| province size on screen | ~280 × 280 px bounding box at 1.57 px/km; equivalent diameter ~210 px = ~140 km |
| spacing between province centres | median 103–130 km (p10 ~80, p90 ~150) |
| province centres per area (1.18 px/km shot) | 44 centres in the middle box (8 cities + 36 markers); about 1 per 23,000 km² (some markers hidden by labels, so the true figure is lower) |
| cities | Afghanistan 6 (Herat, Mazar-i-Sharif, Kunduz, Kabul, Jalalabad, Kandahar, all level 5). Pakistan 7 seen (Peshawar 5, Islamabad 6, Lahore 5, Multan 5, Quetta 5, Hyderabad 5, Karachi 5) |
| **estimated province count** | **Afghanistan ≈ 35 (30–42); Pakistan ≈ 45 (38–55)** |

The count is an estimate (area ÷ mean province area). No screenshot shows either whole country at a zoom where
province borders are drawn. One more shot of each country at ~1.2–1.5 px/km would allow an exact count.

Lines in these shots: the Afghanistan–Pakistan border is 4.5 px (1.18), 5–5.5 px (1.57) and 7 px (2.36), white ~40%,
with a soft glow. Province borders are 2–3 px and faint at 1.18, then 3–3.5 px and bright at 1.57 and above.
Network lines are 2–3 px, +25…+35 L, (55,70,66).

Province-centre markers (flat grey icons, colour ~(96,112,112), L 100–118, soft dark shadow):

| marker | size at 1.18 → 1.57 px/km | where seen | likely meaning |
|---|---|---|---|
| tall triangle with two side bars | 43–44 × 27 → 46 × 28 px | Hindu Kush, Zagros, Scandinavia | hills / mountains |
| flat chevron with a dot on top | 37 × 16 → 39 × 17 px | plains | plains |
| two house roofs | ~50 × 30 px | next to big cities (Baghdad, Kabul) | urban / suburb province |
| palm trees | ~60 × 40 px | south India | jungle / tropical |
| snowflake | ~40 px | north Scandinavia | arctic |

About half of the markers in the Afghanistan shots are the tall type and half the flat type (20 / 21). Each centre
links to roughly 4–6 neighbours by network lines.

## 8. Clouds, haze and map edge

- **No camera haze**: land brightness does not change from top to bottom of the screen in any shot.
- **Cloud wisps** float over the map at mid and close zoom (e.g. over Kabul/Mazar, over Uzbekistan): soft,
  translucent, 300–600 px; they lift L by +20…+35 and drop colour saturation ~25%.
- **Map edge** (world zoom): a cyan line (84,220,231) with a 3–4 px outer glow. Beyond it:
  - north: flat warm grey-brown (61,57,51), p10 (56,52,46), p90 (66,62,56), no clouds;
  - south: dark warm grey (44,42,38) with scattered grey cumulus puffs (up to ~(74,73,69)) and faint horizontal scanlines.

## 9. Base map vs gameplay UI

| base map (art) | gameplay UI (drawn by game state) |
|---|---|
| land texture, owner tint, forest clumps, mountains, fields | resource pins (green crate, gear, red fuel can, rocket, circuit board) with soft green halo |
| sea band, deep water, depth patches, ripples | unit flags with nation flag + stack number |
| coast rim, country borders | radar / air-range circles (green and blue arcs) |
| province borders, network lines, province-centre markers, ≈ marks | small 3D building sprites around cities (army bases etc.) |
| city patches and 3D cities | selection highlight (white thick network lines, red province outline) |
| labels (country, city + level) | convoy / route lines (dark blue polyline), enemy-edge glow follows ownership |
| map edge, off-map clouds | world-view city dots coloured by owner (red / cyan / green) |

## 10. What a reproduction most often gets wrong (by evidence, most important first)

1. **Coastal band as a fixed-distance buffer.** CoN's band is the real shallow shelf (Sunda, Arafura, Gulf, Arctic):
   width varies 3× in one view. Use bathymetry; keep the edge a crisp ~10 px step plus a long soft fade.
2. **Lines as opaque grey, or scaling with the map.** Borders are white at ~35–40% opacity and keep a screen width
   (3 px far, 4.5→7 px close for country borders). On green land they must look pale green, not grey.
3. **Province borders and network lines treated as one line type.** Borders: irregular, 3 px, +90 L (close).
   Network: straight, marker to marker, 2–3 px, +30 L. Borders are faint until ~1.5 px/km.
4. **Showing country names and city names together.** CoN swaps them between 0.5 and 0.66 px/km.
5. **Terrain changing hue.** Every owner is one hue; forest is ~15% darker (bluish on neutral land), mountains are
   relief shading. Smooth ground stays 40–70% of land; forest 0–35% only where real forest is; mountains only on ranges.
6. **Wrong coast rim for the zoom.** Far: 1–2 px dark rim (L ≈ 32) + 6–8 px shadow on the water side.
   Close: thin light rim and low-poly straight coast segments.
7. **Labels that scale with the map, or that sit on the city.** City names grow only ~z^0.35 (35→55 px over 3.6×
   zoom), sit centred below the city by ~1.8–2.5 label heights, and are turned ~15° clockwise.
8. **Ripples that grow with zoom.** Keep the ripple period ~25–40 px on screen at every zoom; raise only contrast
   (2–6 L far, 10–12 L close).
9. **Missing deep-water depth patches**, or patches with hard edges: 17–32% of deep water, 200–400 px soft blobs,
   ~(2–16,31–46,59–72).
10. **Cities at exact real positions.** CoN pushes close cities apart (×1.3–2.4 under 250 km) so patches and names fit.
11. **Province layer too dense or too sparse.** CoN provinces are ~15,000 km² median (~140 km across), centres
    ~100–130 km apart; each centre has a terrain marker.
12. **Camera tilt or haze.** The view is pure top-down with no haze; atmosphere comes only from drifting cloud wisps.

## Method notes (for re-checking)

Scripts live in the session scratchpad `catalogue/` folder: `seaprof.py` / `sea.py` (sea layers, band edge,
depth patches, ripples), `trans.py` (aligned coast transects), `ridges.py` and `lprof.py` (line widths by
perpendicular profiles), `labels2.py` (rotation-aware label height), `rel.py` (owner colours), `psheet.py`
(random-point terrain sheets judged by eye), `reg.py` (SIFT zoom ratios), `fit.py` (px/km from city
coordinates), `mark.py` / `dens.py` / `prov.py` (markers, province density and polygons), `city.py` (city patches).
Limits: JPEG compression softens 1-px features by ~0.5 px. Terrain shares come from 40-point samples (±8 points).
Province counts are extrapolated, not counted.
