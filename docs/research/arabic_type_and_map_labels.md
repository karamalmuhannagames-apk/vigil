# Arabic Type and Map Labels: Research and Spec

How to make Arabic text on a satellite-imagery war map look premium, custom-made and crisp on Android phones. Covers (1) free Arabic typefaces we can bundle, (2) how good maps and games label things, (3) city markers and name plates, and (4) a spec a developer can build straight from.

Context from the code as it stands: `app/style.css` loads **Rajdhani** (Latin) and **Tajawal** Medium/Bold; `app/render.js` draws labels with `strokeText` (stroke `rgba(8,12,20,0.85)`, width 4) and then `fillText` (`#fff3d0`), and caps the device pixel ratio at 2.5. The advice below builds on that rather than replacing it wholesale.

Verification notes: licences, weights and file sizes were checked on each family's Fontsource page (which mirrors Google Fonts metadata and file provenance) or its GitHub repo, linked in each row. File sizes are for the unsubsetted TTF as Google Fonts ships it. Comments on legibility and character are design judgements from the specimens. Test them on a real phone over our own satellite tiles before locking anything in.

---

## 1. Arabic typefaces we can ship

### 1.1 Licence rule

Every family below except Thmanyah is under the **SIL Open Font License 1.1**. The OFL lets us bundle the files inside the APK, use them commercially, and subset or convert them to WOFF2 for our own use. The one restriction that matters to us: if we *modify* a font and distribute it, we must not ship it under the original *Reserved Font Name*. Subsetting for our own app is standard practice, but rename the subset's family name to be safe (e.g. `VigilKufam`). Keep `OFL.txt` for each family in `app/fonts/licenses/` and credit the fonts in the in-game credits.

**Thmanyah: not suitable for bundling.** Its official FAQ says it can be used commercially, including in apps, but it also says the licence "does not allow modifying the font files, renaming them, or creating derivative works", that redistributing the files is not allowed, and that files "may not be uploaded, hosted, or made available for download except through the official source" ([Thmanyah Font for Everyone](https://ask.thmanyah.com/hc/en-001/articles/45993930027281-Thmanyah-Font-for-Everyone)). An APK *is* redistribution, and we could not subset it. Only use it after getting written permission through their support chat.

### 1.2 Candidate table

| Family | Licence (verified) | Weights / axes | Latin companion | Small-size legibility on busy imagery | Character | TTF size |
|---|---|---|---|---|---|---|
| **Kufam** | OFL 1.1 ([GitHub](https://github.com/originaltype/kufam), [Fontsource](https://fontsource.org/fonts/kufam/about)) | Variable `wght` 400–900 + matching **italic** file | Made with it (Artur Schmal), and both scripts are in sync. The Latin lowercase borrows from early Kufi, and the caps from Amsterdam signage | Good at 14 dp+; heavy, compact, built for signage and wayfinding | **Modern-military Kufi.** Wael Morcos's Arabic is "inspired by 7th-century Kufi inscriptions" | 419 KB (+427 KB italic) |
| **Cairo** | OFL 1.1 ([GitHub](https://github.com/Gue3bara/Cairo), [Fontsource](https://fontsource.org/fonts/cairo/about)) | Variable `wght` 200–**1000**, `slnt` −11…11 | Extends Titillium Web (square, technical) | Very good, with a large body and open counters | Kufi-based, technical/military. Very widely used on Arab websites, so less distinctive | 585 KB |
| **Readex Pro** | OFL 1.1 ([GitHub](https://github.com/ThomasJockin/readexpro), [Fontsource](https://fontsource.org/fonts/readex-pro/about)) | Variable `wght` 160–700, **`HEXP` (hyper-expansion) 0–100** | Lexend, designed for reading fluency | **Excellent.** Arabic by Nadine Chahine and others; designed for legibility ([Material Design blog](https://material.io/blog/readex-pro-legibility-arabic-type-design)) | Clean, modern, neutral | 272 KB |
| **IBM Plex Sans Arabic** | OFL ([METADATA.pb](https://raw.githubusercontent.com/google/fonts/2796410152d4f9524b68ed46e69c1b60f8e0f7c3/ofl/ibmplexsansarabic/METADATA.pb), [Fontsource](https://fontsource.org/fonts/ibm-plex-sans-arabic/about)) | 7 static: 100–700 | IBM Plex Sans (excellent, engineered) | Very good | Corporate-engineered, "command console" | ≈230–241 KB **per weight** |
| **Noto Kufi Arabic** | OFL 1.1 ([GitHub notofonts/arabic](https://github.com/notofonts/arabic), [Fontsource](https://fontsource.org/fonts/noto-kufi-arabic/about)) | Variable `wght` 100–900 | Pair with Noto Sans | Good, sturdy | Plain Kufi, neutral and safe | 424 KB |
| **Noto Sans Arabic** | OFL 1.1 ([Fontsource](https://fontsource.org/fonts/noto-sans-arabic/about)) | Variable `wght` 100–900, **`wdth` 62.5–100** | Noto Sans | Very good; the condensed width helps fit long names | Neutral UI | 825 KB |
| **Noto Naskh Arabic** | OFL 1.1 ([Fontsource](https://fontsource.org/fonts/noto-naskh-arabic/about)) | Variable `wght` 400–700 | Noto Serif/Sans | Fair; Naskh needs more size on screens | Classic book style | 300 KB |
| **Tajawal** (current) | OFL 1.1 ([GitHub](https://github.com/googlefonts/tajawal), [Fontsource](https://fontsource.org/fonts/tajawal/about)) | 7 static: 200–900 | Geometric Latin, adequate | Fair to good. Low, wide body; thin joins at small sizes | Geometric-modern (Boutros) | **≈54–61 KB per weight** (smallest) |
| **Almarai** | OFL 1.1 ([GitHub](https://github.com/googlefonts/Almarai), [Fontsource](https://fontsource.org/fonts/almarai/about)) | 4 static: 300, 400, 700, 800 | Basic | Good | Friendly, rounded (Boutros) | ≈146–164 KB per weight |
| **Alexandria** | OFL 1.1 ([GitHub](https://github.com/Gue3bara/Alexandria), [Fontsource](https://fontsource.org/fonts/alexandria/about)) | Variable `wght` 100–900 | **Montserrat** (designed as its Arabic companion) | Good | Geometric poster style, confident | ≈325 KB |
| **Changa** | OFL 1.1 ([GitHub](https://github.com/googlefonts/changa-vf), [Fontsource](https://fontsource.org/fonts/changa/about)) | Variable `wght` 200–800 | Built in (Eduardo Tunni), squarish | Good when bold; narrow forms | Square/condensed, arcade-military | 129 KB |
| **Reem Kufi** | OFL 1.1 ([GitHub](https://github.com/aliftype/reem-kufi), [Fontsource](https://fontsource.org/fonts/reem-kufi/about)) | Variable `wght` 400–700 | Josefin Sans (light, elegant) | Poor below 16 dp | **Ceremonial Fatimid Kufi** (early Kufi models on the Fatimid grid) | 124 KB |
| **El Messiri** | OFL 1.1 ([GitHub](https://github.com/Gue3bara/El-Messiri), [Fontsource](https://fontsource.org/fonts/el-messiri/about)) | Variable `wght` 400–700 | Philosopher (Jovanny Lemonad) | Fair | Calligraphic-modern, elegant | 135 KB |
| **Lalezar** | OFL 1.1 ([GitHub](https://github.com/BornaIz/Lalezar), [Fontsource](https://fontsource.org/fonts/lalezar/about)) | 1 weight (400, very heavy) | Built in | Headline only | Bold poster/propaganda style (Persian street-sign roots) | 283 KB |
| **Baloo Bhaijaan 2** | OFL 1.1 ([GitHub](https://github.com/EkType/Baloo2), [Fontsource](https://fontsource.org/fonts/baloo-bhaijaan-2/about)) | Variable `wght` 400–800 | Baloo 2 | Good | Soft and bubbly; too cartoon for a war game | 279 KB |
| **Rubik** | OFL 1.1 ([GitHub](https://github.com/googlefonts/rubik), [Fontsource](https://fontsource.org/fonts/rubik/about)) | Variable `wght` 300–900 + italic; Arabic by Omaima Dajani | Rubik (rounded corners) | Good | Rounded, casual-tech | 351 KB (+347 KB italic) |
| **Vazirmatn** | OFL 1.1 ([GitHub](https://github.com/rastikerdar/vazirmatn), [Fontsource](https://fontsource.org/fonts/vazirmatn/about)) | Variable `wght` 100–900 | Roboto (merged by build script); a "Non-Latin" build exists | Very good | Neutral Persian-first UI face (Persian letter forms and digits are the default focus) | 236 KB |
| **Amiri** | OFL 1.1 ([GitHub](https://github.com/aliftype/amiri), [Fontsource](https://fontsource.org/fonts/amiri/about)) | 400/700 + italics | Serif Latin | Poor on maps | Classical Naskh (Bulaq press) | ≈400–420 KB per style |
| **Aref Ruqaa** | OFL 1.1 ([repo metadata](https://awesome.ecosyste.ms/projects/github.com%2Faliftype%2Faref-ruqaa)) | 400/700 (+ Ink colour variant) | Based on AMS Euler | Poor on maps | Handwritten Ruqaa, like a field order or decree | n/a |

### 1.3 What the table means for us

- **Display (country names, capitals, headers):** **Kufam** is the best fit. It is Kufi, heavy, compact and built for signage. It has a real matched Latin and an italic (useful for "in motion", alerts and timers). It is far less common than Cairo or Tajawal, so it will feel more custom. **Cairo** is the fallback if Kufam's Latin feels too quirky in English mode: it goes up to weight 1000 and its Titillium Latin reads as "military technical". Its downside is that it is everywhere.
- **Text (UI, small map labels, numbers):** **Readex Pro**. It is the only candidate designed specifically around legibility research. Its Arabic has a generous body and open counters that survive a halo at 11–13 dp, its Latin (Lexend) is clean, and the `HEXP` axis lets us **widen country-scale labels without letter-spacing** (see 2.3). One 272 KB variable file covers every weight. **IBM Plex Sans Arabic** is the runner-up, but static files cost ≈235 KB per weight.
- **Flavour faces, used sparingly:** Reem Kufi for the title screen and logo (ceremonial Fatimid Kufi); Aref Ruqaa for "handwritten" commander dispatches and treaty documents; Lalezar for propaganda-poster splash screens. **Never use these on the map.**
- **Retire Tajawal from map labels.** Its thin joins break up under a dark halo at small sizes. Keep it only as a tiny last-resort fallback (59 KB).

### 1.4 Download sources

| Use | Family | Source |
|---|---|---|
| Display | Kufam | https://github.com/originaltype/kufam (files `Kufam[wght].ttf`, `Kufam-Italic[wght].ttf`), or Google Fonts https://fonts.google.com/specimen/Kufam |
| Text | Readex Pro | https://github.com/ThomasJockin/readexpro, or https://fonts.google.com/specimen/Readex+Pro |
| Display fallback | Cairo | https://github.com/Gue3bara/Cairo |
| Title/logo | Reem Kufi | https://github.com/aliftype/reem-kufi |
| Dispatches | Aref Ruqaa | https://github.com/aliftype/aref-ruqaa |
| Runner-up text | IBM Plex Sans Arabic | https://github.com/googlefonts/plex |

### 1.5 Packaging the fonts

1. **Subset, but keep the shaping features.** Run fonttools `pyftsubset` with `--layout-features='*'` (or at least `init,medi,fina,isol,rlig,liga,calt,ccmp,mark,mkmk,kern,curs`) and `--unicodes` covering Arabic (U+0600–06FF, U+0750–077F, U+FB50–FDFF, U+FE70–FEFF), Basic Latin, Latin-1 punctuation, U+200C–200F, U+2066–2069 and U+0640. **Dropping the GSUB/GPOS features breaks Arabic joining.** Output to WOFF2 (Chromium-based WebView supports it). Expect roughly 40–60% savings.
2. **Bundle locally.** Never fetch fonts from the network at runtime. Serve the assets through the same origin as the game (e.g. Android's `WebViewAssetLoader`), so `@font-face` and canvas see them immediately.
3. Declare variable fonts with weight ranges so `ctx.font = '800 20px Kufam'` picks the right instance:
   ```css
   @font-face { font-family: 'Kufam'; src: url('fonts/Kufam-subset.woff2') format('woff2'); font-weight: 400 900; font-display: block; }
   @font-face { font-family: 'Readex Pro'; src: url('fonts/ReadexPro-subset.woff2') format('woff2'); font-weight: 160 700; font-display: block; }
   ```
   Use `font-display: block` for in-game fonts (loading is under our control), not `swap`, so a frame never paints in a fallback font.

---

## 2. Map label design

### 2.1 Halo, shadow or plate?

- **Halo (outline):** the cartographic standard. Esri's guidance is to make halos as subtle as possible: reduce the width until the halo stops working, then add a little back. Avoid pure white unless the background is white. Match or neutralise the halo colour to the background, and up to 50% transparency is fine. Esri also cites the WCAG 4.5:1 contrast ratio as the target halos help reach ([Esri, Polishing your halo](https://www.esri.com/arcgis-blog/products/arcgis-living-atlas/mapping/polishing-your-halo)). Mapbox's guide likewise says halos should lift labels while staying "subtle so it isn't obvious" ([Mapbox cartography guide](https://amyleew.gitbooks.io/cartography-guide/typography.html)).
- **Soft shadow/glow:** cartography sources quoted by Red Blob Games say thick outlines look heavy. Thinner, blurred or contrast-dependent halos (including an outline colour *sampled from the map underneath*) look better ([Red Blob Games, map typography](https://www.redblobgames.com/x/2428-map-typography/)).
- **Plate (background pill/tag):** guarantees legibility on any imagery and gives a "game UI" look. Use plates for things you *act on* (cities, units) and halos for things you *read* (country, sea and region names).

**Our rule:** satellite imagery is mostly mid-dark (sea, forest, steppe), with bright exceptions (desert, snow, cloud). So the default is **light warm text + thin dark halo + soft dark glow**. On bright terrain the halo gets darker and wider automatically (see 4.4). Plates are used only for cities and interactive objects.

**Arabic-specific halo warning.** Arabic glyphs overlap at their joins. With a **semi-transparent** stroke (`rgba(...,0.85)` as in `render.js` now), each glyph's stroke is painted separately, so the overlaps double up and show darker blobs at every join. This is the canvas cousin of the CSS issue "Text stroke cuts joining glyphs apart", which the W3C Arabic layout group logs as failing in Blink, Gecko and WebKit ([w3c/alreq #220](https://github.com/w3c/alreq/issues/220)). Fix: stroke with an **opaque** colour into an offscreen label sprite, then fill on top (so the fill hides any stroke drawn over a join), and apply transparency to the *whole sprite* with `globalAlpha` when blitting. Never draw a stroke *after* the fill on Arabic text.

### 2.2 Letter spacing: never on Arabic

- Arabic is cursive. Letter-spacing pulls joined letters apart. Android's own text engine (Minikin) disabled letterspacing for cursive-connected scripts back in 2015 because "the appearance of letterspacing with scripts with cursive connections is poor" ([Minikin commit e8721b2](https://android.googlesource.com/platform/frameworks/minikin/+/e8721b2)). Chrome 137 (desktop, Android and **Android WebView**) shipped "Ignore Letter Spacing in Cursive Scripts" for CSS ([blink-dev intent](https://groups.google.com/a/chromium.org/g/blink-dev/c/K_tGT0tTJoM)). Do not rely on that for canvas, though: the thread does not confirm canvas behaviour. Always set `ctx.letterSpacing = '0px'` for Arabic.
- Engines that implement spacing by drawing **one character at a time** break shaping completely: each letter is drawn in its isolated form. That is exactly what bitmap-font and per-glyph engines do. Defold users report Arabic coming out "left-to-right and disjointed" with wrong (isolated/medial) forms, and the suggested fix is HarfBuzz shaping ([Defold forum](https://forum.defold.com/t/arabic-rtl-i18n-support/23626)). Canvas `fillText` itself shapes correctly *only when given the whole string*; it exposes no shaping output, so per-glyph layout needs HarfBuzz (e.g. harfbuzzjs) ([article on canvas shaping](https://www.besthub.dev/articles/accurate-text-measurement-and-rendering-in-canvas-with-font-shaping-and-harfbuzz-34dfbf9d0d67)).
- **Latin labels** (English mode) may use tracking on area labels (country/sea names in caps, +8–15%). Mapbox warns tracking is "often overdone" ([guide](https://amyleew.gitbooks.io/cartography-guide/typography.html)).
- **How to make an Arabic country name span a wide country:**
  1. Bigger size and heavier weight first.
  2. A wider font instance: Readex Pro `HEXP` axis, or a wider font. Noto Sans Arabic has a `wdth` axis, but only *condensed* (62.5–100), which is useful for squeezing long names into small countries.
  3. Wider *word* spaces between words (always safe).
  4. Kashida/tatweel (U+0640) only as a last resort, and at most one or two per word, placed between two connecting letters. The W3C notes simple tatweel insertion is "generally regarded as ugly" ([W3C, Approaches to full justification](https://w3c.github.io/i18n-drafts/articles/typography/justification.en)). Kufam's extenders look fine with one kashida in the longest connection; test per name.

### 2.3 Country names curved along the shape

Paradox-style (HOI4/EU) country names arc across the territory. The robust algorithm is the **skeleton/medial-axis** method: build an approximate skeleton from a Voronoi diagram of the polygon's vertices, prune skeleton edges with low clearance (distance to the border), find long paths, fit a circular arc, then maximise label size along the arc while keeping it centred and preferring large radii. It labels about 120 countries in under 2 s in C++ ([Krumpe & Mendel, *Computing Curved Area Labels in Near-Real Time*](https://arxiv.org/pdf/2001.02938)). Other games do simpler things: *Ages of Conflict* stretches big nation names "across the land" sized by nation area, keeps the old style for tiny nations, and lets players turn it off ([devlog v3.4.0](https://jokupelle.itch.io/ages-of-conflict/devlog/808754/v340-land-occupation-big-nation-names-terrain-view)).

For us:
- **Precompute** arcs for the starting countries offline (in `ci/`) and store `{cx, cy, radius, startAngle, endAngle, maxSizeDp}` per country in `political.json`. On conquest, recompute **on the device** with a cheap approximation: the pole of inaccessibility (polylabel) as the centre, the principal axis (PCA of province centroids) as direction, and a gentle arc whose sagitta is ≤ 8% of chord length. Run it in a frame budget or a worker.
- **Curving Arabic without breaking joins:** Red Blob describes two methods. "Wrapping" places each letter on the path; "warping" bends a rendered rectangle ([Red Blob](https://www.redblobgames.com/x/2428-map-typography/)). **For Arabic, wrap per word or per joined cluster, never per letter.** In practice: render the whole shaped word into an offscreen strip, then slice it into narrow vertical columns (2–3 device px) and draw each column rotated and positioned along the arc. That is a column-warp, which keeps every join intact. Keep the total bend ≤ 25°.
- Rendering order: country names sit **under** city plates and units, at 80–90% opacity, so they read as "printed on the map".
- Only show curved names at world/continent zoom. When zoomed in, a country name either shrinks to a straight label at the centre of the viewport part of the country, or hides.

### 2.4 How the reference games and maps do it (observations)

- **Google Maps:** labels appear contextually rather than all at once (the early map was a "Christmas tree" that would "fall over"). Point labels are vertically centred on their marker and extend left or right, moving above or below when crowded ([Creative Bloq interview](https://www.creativebloq.com/netmag/google-maps-design-secrets-revealed-41411310)).
- **Mapbox/MapLibre:** priority comes from layer order and `symbol-sort-key`; collision is controlled by `text-allow-overlap`/`ignore-placement`; and `text-variable-anchor` tries an ordered list of anchors before hiding a label, with the original anchor tried first after a zoom ([Mapbox label placement](https://docs.mapbox.com/help/dive-deeper/optimize-map-label-placement/)). Mapbox GL needs a separate ICU-in-WebAssembly plugin to shape Arabic and run bidi, because its GPU glyph pipeline does not shape on its own ([mapbox-gl-rtl-text](https://www.github.com/mapbox/mapbox-gl-rtl-text)). This matters if we ever move labels to WebGL glyph atlases.
- **HOI4:** the political map fades in as you zoom out, with terrain plus borders at close zoom, and cities light up at night ([HOI4 Dev Diary 11](https://forum.paradoxplaza.com/forum/threads/hoiiv-developer-diary-11-map-graphics-no-counters-discussion.814718/)). Country names arc across territory (see 2.3).
- **CoN / Supremacy / Call of War:** cities are special provinces where units mobilise. Conquered cities have lower morale and can revolt under 35% morale ([CoN wiki: City](https://conflictofnations.wiki.gg/wiki/City)). That state deserves to be visible on the plate (see section 3). The common complaint about CoN is cluttered displays, which our earlier `polish_tips.md` already addresses.
- **Civilization VI:** a city "banner" is a plate showing name, population and status icons in the owner's colours. That is the pattern we adapt in section 3, with a military rather than storybook skin.

### 2.5 Keeping Arabic crisp on canvas in Android WebView

| Problem | Cause | Fix |
|---|---|---|
| Blurry text | Canvas backing store at CSS size | `canvas.width = cssW * dpr; canvas.height = cssH * dpr; ctx.setTransform(dpr,0,0,dpr,0,0)` ([web.dev High DPI Canvas](https://web.dev/articles/canvas-hidipi); [MDN devicePixelRatio](https://developer.mozilla.org/en-US/docs/Web/API/Window/devicePixelRatio)). Keep the existing 2.5 cap for performance |
| Shimmering while panning | Labels at fractional pixels | Snap the label sprite origin: `x = Math.round(x*dpr)/dpr` |
| First frames in fallback font | Canvas does not trigger or await webfont loads | Before the first map draw: `await Promise.all([document.fonts.load('800 20px Kufam','مصر'), document.fonts.load('600 14px "Readex Pro"','القاهرة 123')])`. Pass **Arabic sample text**, because with `unicode-range` subsets the browser only loads the face for characters you mention. Then clear the label-sprite cache on `document.fonts.onloadingdone` ([MDN CSS Font Loading API](https://developer.mozilla.org/docs/Web/API/CSS_Font_Loading_API); [Konva custom font notes](https://konvajs.org/zh-Hans/docs/sandbox/Custom_Font.html)) |
| Disconnected letters | Per-character drawing, letter-spacing, or a stroke on top | Always call `fillText` with the **whole string**; `letterSpacing='0px'`; opaque stroke first, then fill (2.1) |
| Faux bold gaps | Synthetic emboldening when the weight is not loaded | Ship real weights/variable fonts. WebKit had a bug with *disconnected Arabic glyphs for emboldened webfonts* ([WebKit 251753](https://lists.webkit.org/pipermail/webkit-unassigned/2023-February/1085727.html)) |
| Mixed Arabic + numbers reorder strangely | Bidi | Set `ctx.direction = 'rtl'` for Arabic labels and `'ltr'` for English. Wrap embedded numbers or Latin names in isolates: `'⁨' + n + '⁩'` |
| Fonts missing in a worker | `OffscreenCanvas` in a worker has its own font set | Load via `self.fonts.add(new FontFace(...))` inside the worker. Worker fonts landed later in some engines ([WebKit 224178](https://bugs.webkit.org/show_bug.cgi?id=224178)). Simplest is to rasterise label sprites on the main thread |
| Jank from `shadowBlur` | Blur is recomputed every frame | **Cache every label as a sprite** (offscreen canvas) keyed by `text|font|size|style|dprBucket`. Redraw only when the zoom band changes. Blit with `drawImage` |
| `ctx.filter` on text | Engine bugs historically (e.g. Firefox fillText ignored filters, [Bugzilla 1304539](https://bugzilla.mozilla.org/show_bug.cgi?id=1304539)) | Don't depend on `ctx.filter` for halos; use stroke + `shadowBlur` in the sprite |

Arabic looks smaller than Latin at the same point size because Arabic letters have a smaller body relative to their ascenders and descenders ([Alex Strick quoting Thomas Phinney](https://alexstrick.com/personal/2017-03-12-why-are-arabic-fonts-so-small.html)). **Set Arabic labels about 12–15% larger than their Latin equivalents** (the spec in section 4 already does this).

### 2.6 Collision and decluttering

Greedy placement in priority order, one pass per frame (or whenever the camera moves more than ~4 dp):

1. Sort candidates by `priority = basePriority + boosts`.
   - Base priority: player's own capital 100, selected object 95, country names 90 (at Z0–Z1), enemy capitals 85, other capitals 80, cities under attack 75, own cities 70, major cities 60, minor cities 40, sea/region names 30, province names 20.
   - Boosts: +15 if part of the current order or route, +10 if it has an alert.
2. For each candidate, try anchors in order. **For Arabic: left of the marker, then right, then above, then below** (the text's starting edge sits beside the marker). For English: right, left, above, below. Mirror the order in RTL layouts.
3. Collision test against a uniform grid spatial index (cell ≈ 64 dp) of placed boxes, each padded by 3 dp (labels) or 6 dp (plates).
4. **Hysteresis:** a label placed last frame keeps its anchor if still valid, and only a *higher* priority label can evict it. Fade in/out over 180 ms. Avoid labels flickering on and off during pinch zoom.
5. Markers are never dropped for their own labels. If the name does not fit, the city pip stays and the name hides (tap reveals it).
6. Cap the visible plate count per zoom band (Z2: 40, Z3: 80, Z4: 140) so mid-range phones stay smooth.

### 2.7 Eastern vs Western digits

- Usage differs by region: the Maghreb uses Western digits only; Egypt, Sudan and the UAE use both; Saudi Arabia increasingly favours Western digits; Iran and Afghanistan use Eastern (Persian) digits ([Wikipedia: Eastern Arabic numerals](https://en.wikipedia.org/wiki/Eastern_Arabic_numerals)). Eastern Arabic-Indic digits are U+0660–0669. Persian ones are separate code points U+06F0–06F9.
- **Recommendation:** default to **Western digits (0–9)** on the map and in combat numbers, for scan speed and consistency with unit stats. Offer a setting "الأرقام: 123 / ١٢٣". Format with `Intl.NumberFormat('ar-u-nu-latn')` or `('ar-u-nu-arab')` explicitly, never bare `'ar'`, so the result does not depend on ICU defaults. Use **tabular figures** (`font-variant-numeric: tabular-nums`, or pad in canvas) for countdowns so timers don't jitter.

---

## 3. City markers and name plates

### 3.1 Shape language: "Kufi geometry meets military stencil"

Make it feel Arabic through **geometry**, not clichés (no lanterns, arches or palm trees). Square Kufi is built on a grid of squares and 45° cuts, and the eight-pointed star (two overlapping squares, as in ۞ Rub el Hizb) is pan-Arab and geometric. Military language adds stencil cuts, chevrons and NATO frame shapes. The overlap between the two is **squares, 45° chamfers and eight-pointed stars**, and the whole marker system is built from those.

- **Plate:** a dark-glass rectangle with **45° chamfered corners** (4 dp cut), not a rounded pill. Rounded pills read as "social app". Chamfers read as "military hardware" and echo Kufi cuts.
- **Relation tab:** a coloured end-cap on the plate's starting edge (right side in Arabic, left in English), carrying the **relation frame shape** taken from NATO joint military symbology. Friendly = rectangle, hostile = diamond, neutral = square, unknown = quatrefoil ([Wikipedia: NATO Joint Military Symbology](https://en.wikipedia.org/wiki/NATO_Joint_Military_Symbology)). Shape carries the meaning, colour reinforces it, so colour-blind players are covered by design.
- **Capital:** an **eight-pointed star** (two squares rotated 45°) in gold above the plate, plus a 2 dp gold rule along the plate's top edge. The player's own capital adds a slow 4 s "breathing" glow.
- **City size:** pips under the name (●, ●●, ●●●), or the plate grows one height step per tier.
- **Emblems** (12 dp monochrome icons inside the plate, after the name, max 2): anchor = port, chevron-wing = airbase, drop = oil, atom = nuclear, crenellation = fortified (count = level), radar arc = radar.
- **State overlays:**
  - Occupied: a diagonal **hatched corner** in the occupier's colour.
  - Low morale / revolt risk (<35%, as in CoN): plate border pulses amber.
  - Under attack: a red sweep around the plate edge and a small crossed-sabres glyph.
  - Fog / unknown owner: the plate turns grey glass with a quatrefoil tab and a "؟" mark.
- **Terrain-adaptive glass:** plate fill is 82% opaque, so a hint of the satellite image shows through, plus a 1 px inner highlight on the top edge for a "premium bevel".

### 3.2 Relation colours (colour-blind aware)

Based on the Okabe-Ito colour-universal-design palette (orange `#E69F00`, sky blue `#56B4E9`, bluish green `#009E73`, yellow `#F0E442`, blue `#0072B2`, vermillion `#D55E00`, reddish purple `#CC79A7`) ([reference](https://dev.conceptviz.app/fr/blog/okabe-ito-palette-hex-codes-complete-reference)), adjusted for contrast on dark satellite imagery. Each relation **also** has a unique shape and a lightness step, so it never relies on hue alone:

| Relation | Colour | Shape (tab/pip) | Lightness |
|---|---|---|---|
| Self (player) | Gold `#F2C14E` | Rectangle + small star notch | Lightest |
| Ally / coalition | Sky blue `#4DA8E8` | Rectangle | Light |
| At war (enemy) | Vermillion `#E0522A` | Diamond, solid | Mid |
| Hostile, not at war | Vermillion outline `#E0522A` on dark fill | Diamond, outline only | Mid |
| Neutral | Steel grey `#A9B1BA` | Square | Mid-light |
| Unknown / fog | Reddish purple `#C77DB0` | Quatrefoil | Mid |

Offer a "high contrast" toggle that swaps ally to `#56B4E9`, enemy to `#D55E00` and self to `#F0E442` (pure Okabe-Ito), and thickens tab outlines to 2 dp.

### 3.3 Reference examples to study

- HOI4's political-to-terrain fade and night lights (Dev Diary 11, above). Copy the *zoom-driven fade* idea.
- Civilization VI city banners (plate + owner colours + status icons). Copy the *information layout*, not the storybook skin.
- Google Maps' contextual label density and left/right placement around markers (Creative Bloq, above).
- Mapbox variable anchors with priority (Mapbox guide, above). This is the declutter model.
- NATO APP-6 frames for relation shapes (Wikipedia, above). Instantly "military" and colour-blind safe.

---

## 4. Implementation spec

All sizes are in **dp** (1 dp = 1 CSS px in our WebView with `width=device-width`). Multiply by `dpr` only when sizing canvas backing stores and sprites.

### 4.1 Fonts

| Role | Arabic | Latin (English mode) | Weights used |
|---|---|---|---|
| Display: country names, capitals at Z0–Z1, screen headers | Kufam | Kufam | 700, 800 (+ italic 700 for alerts) |
| Text: UI, city names, numbers, sea names | Readex Pro | Readex Pro (Lexend Latin) | 400, 500, 600, 700 |
| Fallback stack | `'Kufam', 'Cairo', 'Readex Pro', sans-serif` / `'Readex Pro', 'Tajawal', sans-serif` | same | n/a |
| Flavour (not on map) | Reem Kufi (title), Aref Ruqaa (dispatches) | n/a | 700 / 400 |

Rajdhani can stay for big Latin-only HUD numerals if the team likes it. Readex Pro covers everything otherwise, and dropping Rajdhani saves a download.

### 4.2 Zoom bands and label sizes

Zoom bands: **Z0** world, **Z1** continent, **Z2** region (one large country fills the screen), **Z3** theatre (a few provinces), **Z4** tactical.

| Label | Font / weight | Z0 | Z1 | Z2 | Z3 | Z4 |
|---|---|---|---|---|---|---|
| Country name (AR) | Kufam 800 | 13–22 (by area) | 18–30 | 24–34 @ 60% opacity | hidden | hidden |
| Country name (EN, caps, tracking +10%) | Kufam 700 | 11–19 | 16–26 | 21–30 @ 60% | hidden | hidden |
| Capital name (AR / EN) | Readex Pro 600 | major powers only, 12 / 11 | 13 / 12 | 15 / 13 | 16 / 14 | 17 / 15 |
| Major city (AR / EN) | Readex Pro 500 | hidden | hidden | 13 / 11.5 | 14 / 12.5 | 15 / 13 |
| Minor city / province (AR / EN) | Readex Pro 500 | hidden | hidden | hidden | 12 / 11 | 13 / 11.5 |
| Sea / ocean (AR / EN) | Readex Pro 400, `HEXP` 60 (AR) | 13 / 12 | 15 / 13 | 14 / 12 | 12 / 11 | hidden |
| Plate numbers (troops, timers) | Readex Pro 600, tabular | n/a | n/a | 11 | 12 | 12 |
| **Absolute minimum** | n/a | Arabic **11 dp**, Latin **10 dp** | | | | |

Country name size inside a band = `clamp(min, k * sqrt(screenAreaOfCountry), max)`, then the arc fit (2.3) may reduce it further.

### 4.3 Colours

```js
export const LABEL = {
  text:        '#F4EEDD', // warm ivory, primary label fill
  textDim:     '#B9C2CC', // secondary (province names, numbers)
  sea:         '#9CC4DE', // sea/ocean names, 75% opacity, no hard halo
  countryFill: '#F3EAD3', // country names, drawn at 0.85 opacity
  halo:        '#070B11', // opaque stroke colour (alpha applied to whole sprite)
  glow:        'rgba(0,0,0,0.55)',
  plate:       'rgba(13,19,27,0.82)', // #0D131B dark glass
  plateEdge:   'rgba(255,255,255,0.10)', // 1px inner top highlight
  capitalGold: '#E9C46A',
  capitalStar: '#F2C14E',
  self:    '#F2C14E',
  ally:    '#4DA8E8',
  enemy:   '#E0522A',
  neutral: '#A9B1BA',
  unknown: '#C77DB0',
  alertAmber: '#FFB020',
  attackRed:  '#FF4D3D',
};
```

### 4.4 Halo and glow

| Label class | Stroke (opaque `#070B11`, `lineJoin='round'`, drawn **before** fill) | Glow (`shadowBlur`, colour `rgba(0,0,0,0.55)`) | Sprite alpha |
|---|---|---|---|
| Small labels ≤ 13 dp | width = `0.24 × size` (≈ 3 dp at 12 dp) | none | 0.92 |
| Labels 14–18 dp | width = `0.20 × size` (≈ 3.2 dp at 16 dp) | 3 dp | 0.95 |
| Country names | width 2 dp | 10 dp | 0.85 |
| Sea names | none | 6 dp, `rgba(0,10,25,0.6)` | 0.75 |

Note: canvas `lineWidth` is centred on the outline, so only half shows outside the glyph. The widths above are the `lineWidth` value.

**Adaptive bright-terrain boost:** keep a 1/16-scale luminance copy of the satellite base. For each label box, average luminance L. If L > 0.55 (desert, snow, cloud), multiply stroke width by 1.3 and glow alpha by 1.4 (cap 0.8). If L < 0.15 (deep ocean), reduce the stroke to 0.8×. Store the result in the sprite cache key.

### 4.5 Plates and markers

| Element | Spec |
|---|---|
| City plate | Height 18 dp (Z2), 20 dp (Z3), 22 dp (Z4); horizontal padding 8 dp; chamfer 4 dp at all four corners; fill `LABEL.plate`; 1 dp border in relation colour at 70%; 1 px top highlight `LABEL.plateEdge`; drop shadow 0/2 dp blur 6 dp `rgba(0,0,0,0.5)` (baked in sprite) |
| Relation tab | Square end-cap = plate height, on the text's starting side (right in AR); filled relation colour; contains the relation shape glyph at 60% of the tab height in `#0D131B` |
| Capital plate | +2 dp height; 2 dp `capitalGold` rule along the top edge; eight-pointed star 16 dp (Z2) / 18 dp (Z3+) centred above the plate, gap 3 dp, fill `capitalStar`, 1.5 dp `#070B11` outline; own capital adds a glow pulse (alpha 0.25→0.6, 4 s ease-in-out) |
| City pip (when the name is hidden) | 8 dp relation shape (rectangle/diamond/square/quatrefoil), 1.5 dp dark outline; capitals use a 12 dp star |
| Emblems | 12 dp monochrome `#F4EEDD` at 85%, 4 dp gap, max 2 per plate, after the name |
| Size tier | 1–3 pips (3 dp dots, 2 dp gap) centred under the plate, `#F4EEDD` 70% |
| Occupied | 10 dp hatched triangle in the plate corner opposite the tab, occupier colour, 45° hatch at 3 dp pitch |
| Low morale (<35%) | Border colour `alertAmber`, pulse 1.2 s |
| Under attack | 2 dp `attackRed` sweep that travels around the plate perimeter every 1.5 s + 12 dp crossed-sabres glyph |
| Hit area | ≥ 48 × 48 dp regardless of plate size |
| Label fade | 180 ms in/out; anchor hysteresis as in 2.6 |

### 4.6 Rendering checklist

1. Await `document.fonts.load(...)` with Arabic sample text for every face/weight before the first map draw.
2. Make all labels and plates sprites (offscreen canvas) at `dpr` scale. Cache key: `text|font|weight|size|class|relation|lumBucket|dprBucket`. LRU limit ~600 sprites.
3. In each sprite: `ctx.direction` set per language; `letterSpacing='0px'` for Arabic; opaque stroke → fill → (glow via `shadowBlur` on a stroke pass under it); numbers wrapped in U+2068/U+2069.
4. Blit sprites at integer device pixels; apply opacity with `globalAlpha` on the blit, never with an rgba stroke.
5. Curved country names: column-warp a pre-shaped word strip along the stored arc (2–3 px columns), never per letter.
6. Declutter: priority sort → anchor tries → grid collision → hysteresis → per-band caps.
7. Digits: Western by default via `Intl.NumberFormat('ar-u-nu-latn')`, with an Eastern option `('ar-u-nu-arab')`.
8. Subset fonts with `--layout-features='*'` and rename the subset family; ship `OFL.txt` files and credit the fonts.
9. If labels ever move to WebGL glyph atlases: shape first (HarfBuzz/ICU, as Mapbox's RTL plugin does) or keep using canvas-rendered sprites as textures.

---

## Sources

- Thmanyah licence FAQ: https://ask.thmanyah.com/hc/en-001/articles/45993930027281-Thmanyah-Font-for-Everyone
- Kufam: https://github.com/originaltype/kufam, https://fontsource.org/fonts/kufam/about
- Cairo: https://github.com/Gue3bara/Cairo, https://fontsource.org/fonts/cairo/about
- Readex Pro: https://github.com/ThomasJockin/readexpro, https://fontsource.org/fonts/readex-pro/about, https://material.io/blog/readex-pro-legibility-arabic-type-design
- IBM Plex Sans Arabic: https://raw.githubusercontent.com/google/fonts/2796410152d4f9524b68ed46e69c1b60f8e0f7c3/ofl/ibmplexsansarabic/METADATA.pb, https://fontsource.org/fonts/ibm-plex-sans-arabic/about
- Noto Arabic: https://github.com/notofonts/arabic, https://fontsource.org/fonts/noto-kufi-arabic/about, https://fontsource.org/fonts/noto-sans-arabic/about, https://fontsource.org/fonts/noto-naskh-arabic/about
- Tajawal: https://fontsource.org/fonts/tajawal/about
- Almarai: https://fontsource.org/fonts/almarai/about
- Alexandria: https://github.com/Gue3bara/Alexandria, https://fontsource.org/fonts/alexandria/about
- Changa: https://fontsource.org/fonts/changa/about
- Reem Kufi: https://github.com/aliftype/reem-kufi, https://fontsource.org/fonts/reem-kufi/about
- El Messiri: https://fontsource.org/fonts/el-messiri/about
- Lalezar: https://fontsource.org/fonts/lalezar/about
- Baloo Bhaijaan 2: https://fontsource.org/fonts/baloo-bhaijaan-2/about
- Rubik: https://fontsource.org/fonts/rubik/about
- Vazirmatn: https://github.com/rastikerdar/vazirmatn, https://fontsource.org/fonts/vazirmatn/about
- Amiri: https://fontsource.org/fonts/amiri/about
- Aref Ruqaa: https://awesome.ecosyste.ms/projects/github.com%2Faliftype%2Faref-ruqaa
- Esri, Polishing your halo: https://www.esri.com/arcgis-blog/products/arcgis-living-atlas/mapping/polishing-your-halo
- Mapbox cartography guide (typography): https://amyleew.gitbooks.io/cartography-guide/typography.html
- Mapbox label placement: https://docs.mapbox.com/help/dive-deeper/optimize-map-label-placement/
- mapbox-gl-rtl-text: https://www.github.com/mapbox/mapbox-gl-rtl-text
- Red Blob Games, map typography: https://www.redblobgames.com/x/2428-map-typography/
- Krumpe & Mendel, curved area labels: https://arxiv.org/pdf/2001.02938
- Ages of Conflict devlog: https://jokupelle.itch.io/ages-of-conflict/devlog/808754/v340-land-occupation-big-nation-names-terrain-view
- Google Maps design (Creative Bloq): https://www.creativebloq.com/netmag/google-maps-design-secrets-revealed-41411310
- HOI4 Dev Diary 11: https://forum.paradoxplaza.com/forum/threads/hoiiv-developer-diary-11-map-graphics-no-counters-discussion.814718/
- CoN wiki, City: https://conflictofnations.wiki.gg/wiki/City
- W3C alreq #220 (stroke cuts joins): https://github.com/w3c/alreq/issues/220
- W3C justification article: https://w3c.github.io/i18n-drafts/articles/typography/justification.en
- Minikin letterspacing commit: https://android.googlesource.com/platform/frameworks/minikin/+/e8721b2
- Blink intent, ignore letter spacing in cursive scripts: https://groups.google.com/a/chromium.org/g/blink-dev/c/K_tGT0tTJoM
- Defold Arabic support thread: https://forum.defold.com/t/arabic-rtl-i18n-support/23626
- Canvas shaping + HarfBuzz: https://www.besthub.dev/articles/accurate-text-measurement-and-rendering-in-canvas-with-font-shaping-and-harfbuzz-34dfbf9d0d67
- WebKit 251753 (disconnected Arabic with synthetic bold): https://lists.webkit.org/pipermail/webkit-unassigned/2023-February/1085727.html
- WebKit 224178 (FontFace in workers): https://bugs.webkit.org/show_bug.cgi?id=224178
- Firefox 1304539 (fillText and filters): https://bugzilla.mozilla.org/show_bug.cgi?id=1304539
- web.dev High DPI Canvas: https://web.dev/articles/canvas-hidipi
- MDN devicePixelRatio: https://developer.mozilla.org/en-US/docs/Web/API/Window/devicePixelRatio
- MDN CSS Font Loading API: https://developer.mozilla.org/docs/Web/API/CSS_Font_Loading_API
- Konva custom font in canvas: https://konvajs.org/zh-Hans/docs/sandbox/Custom_Font.html
- Why Arabic looks small: https://alexstrick.com/personal/2017-03-12-why-are-arabic-fonts-so-small.html
- Eastern Arabic numerals: https://en.wikipedia.org/wiki/Eastern_Arabic_numerals
- NATO Joint Military Symbology: https://en.wikipedia.org/wiki/NATO_Joint_Military_Symbology
- Okabe-Ito palette: https://dev.conceptviz.app/fr/blog/okabe-ito-palette-hex-codes-complete-reference
