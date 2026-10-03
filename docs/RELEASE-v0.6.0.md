# v0.6.0 — Public configuration bundle

Initial public release of PS4 Playtime Companion.

- Schedule/quota enforcement, quiet-hour reminders and optional CEC Rest Mode script Blueprints.
- Bubble dashboard with automatic English/Hebrew display language, countdown and 7/30-day activity charts.
- Date-scoped bonus minutes and persistent manual block with conditional controls.
- English/Hebrew installation material, prerequisite links, compatibility matrix and architecture flowchart.
- Clearly labelled fictional demo screenshots; no personal screenshots, credentials or household data included.

Validated on Home Assistant Core 2026.9.4. Requires Bubble Card 3.2+, card-mod and config-template-card. PS4 firmware 10.50 was the observed commissioning firmware; other firmware/GoldHEN/CEC combinations require their own physical tests. This release does not claim PS5 support or bundle a working standby.bin.

Install prerequisites and complete the PS4/TV checks in `docs/COMPATIBILITY.md` before enabling enforcement. Existing users should add missing helpers/scripts and update templates without re-running the defaults initializer.
