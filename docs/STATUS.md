# Where the work stands (11 Nov 2026, evening)

## Done and in the repository
- Real world map pipeline (`ci/world/build.py`, workflow "Build real world map"): Natural Earth borders in the
  Palestine view (no Israel, Western Sahara in Morocco), true scale (no magnifiers), provinces merged to playable
  sizes with real names, cities with minimum spacing, playable / computer-run / neutral classes, six doctrines.
- Natural land and sea: NASA Blue Marble graded into one green terrain, NASA relief shading, fine texture by land
  type, double-resolution tiles (zoom levels 0-4, `art/world/tiles`, list in `tiles.json`), land shadow on the water,
  lighter shallows, Suez / Panama / Kiel canals and the Turkish straits cut wide enough to see.
- Live world renderer prototype `app/world/index.html`: relation colour ramps measured from CoN, animated waves
  (`waves.jpg`), smooth vector borders by relation (`borders.json`), Arabic labels (Kufam capitals, Alexandria
  cities) with decluttering sized for a phone.
- City prototype `app/map/index.html`: cities baked at 4x detail from regional city blocks (`art/cityblocks`)
  with the 7 buildings x 5 levels x 4 regional styles (`art/buildings`) set into plots, same colour pass as the land.
- Game rules as data: modes (`core/modes.js`: standard, 100 players, nuclear, blitz, Middle East) and doctrines
  (`core/doctrines.js`), both tested.
- Research reports in `docs/research/`: regional doctrines, 206 polish tips, Arabic type and map labels.
- Free fonts (SIL OFL) in `app/fonts`.

## Next steps, in order
1. Check the latest world build: the faint straight line in the Saudi desert should be gone, canals visible;
   compare enemy red with the CoN screenshots.
2. Put the detailed cities (app/map) onto the real world map (app/world): real city positions, regional style per country.
3. Province outlines, glowing routes, unit and resource icons standing on the map (CoN's "game board" feel).
4. Name plates and capital emblem from the research spec; country names curved along the country.
5. Owner decisions still open: playable list (UK, South Korea and others are under the Oman size line; see
   `art/world/classes.md`), six doctrines or five, final font choice.
6. Building models: more detail per level; remove real markings from unit models.
7. First real game screen on the new map, then an APK (the APK workflow is manual for now).

## Housekeeping
- The repository is public so GitHub builds are free. Make it private again when builds are not needed
  (a reminder is set for 1 December).
- Never put the Play signing key or any token in the repository.
