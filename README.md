# Vigil (codename)

A modern-war strategy game for phones. Design documents live outside this repository.

- `core/`  the simulation and the commander's brain. Pure JavaScript, deterministic, no dependencies.
- `app/`   the game screens (canvas map, panels, Arabic and English).
- `test/`  automatic tests. Run with `npm test`.
- `ci/`    build helpers and the balance report (`node ci/balance.mjs`).
- `android/` the Android wrapper that turns the game into an APK.
