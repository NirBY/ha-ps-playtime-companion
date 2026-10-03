# Compatibility and prerequisites — v0.6.1

## Version scope

| Component | Requirement / evidence |
|---|---|
| Home Assistant Core | Configuration sections and templates validated on **2026.9.4**. Blueprint syntax floor is 2024.10; older releases are not certified by this project. Prefer the tested release or validate on your installed release. |
| Bubble Card | **3.2+**, using standalone pop-ups. This bundle does not use the legacy pop-up-in-stack format. |
| card-mod | Required for layout/RTL styling; install a release compatible with your HA frontend. No independent minimum version has been established. |
| config-template-card | Required for per-user locale selection. Use a release compatible with your HA frontend; no independent minimum version has been established. |
| PS4 firmware | **10.50 was the observed commissioning firmware**. This is not a firmware support matrix. The scheduling code has no firmware-specific payload; other firmware/GoldHEN combinations require their own Rest Mode test. |
| GoldHEN | Must already work on your console and survive Rest Mode in your own tests. No specific GoldHEN build minimum is claimed. |
| PS5 | Not validated or advertised as supported. The repository name is broad; this release targets PS4. |
| TV / HDMI equipment | Must support a tested CEC standby path. No TV brand or model is required or guaranteed. |

Do not update PS4 firmware, sign into PSN, enable an unverified plugin or install a payload merely to satisfy this guide. Preserving your working console environment takes precedence. A successful FTP connection does not establish power-control compatibility.

## Install before this bundle

| Install / configure | Why | Official or upstream instructions |
|---|---|---|
| Home Assistant | Automations, helpers, history and dashboard host | [Install HA](https://www.home-assistant.io/installation/) |
| HACS | Convenient installation of frontend dependencies | [Download HACS](https://hacs.xyz/docs/use/download/download/) and [configure it](https://hacs.xyz/docs/use/configuration/basic/) |
| Bubble Card | Buttons and standalone settings pop-ups | [Bubble Card](https://github.com/Clooos/Bubble-Card#installation) |
| card-mod | Card styling and RTL alignment | [card-mod](https://github.com/thomasloven/lovelace-card-mod#installing) |
| config-template-card | Choose display strings/styles from the viewing user's language | [config-template-card](https://github.com/iantrich/config-template-card#installation) |
| PS4 availability source | An `online` / `offline` sensor used for counting | [Optional PS4 GoldHEN integration](https://github.com/Tech-Morph/HA-PS4-GoldHEN-Integration#setup) or another equivalent source |
| TV integration | A working `media_player.turn_off` action | [HA integration directory](https://www.home-assistant.io/integrations/) — choose your own TV integration |
| TTS provider + speaker (optional) | Spoken reminders | [HA Text-to-speech](https://www.home-assistant.io/integrations/tts/) |

History/recorder must include the availability and daily-time entities. Review [recorder](https://www.home-assistant.io/integrations/recorder/), [history_stats](https://www.home-assistant.io/integrations/history_stats/) and [packages](https://www.home-assistant.io/docs/configuration/packages/). Python is required only for the optional dashboard renderer/tests, not to run the automations in HA.

## Before installation: PS4

1. Confirm GoldHEN is already running reliably; record your own firmware/build privately.
2. Keep HA and the PS4 reachable on the local network; use a stable LAN address/reservation. The PS4 does not need PSN access for FTP monitoring.
3. If using the GoldHEN integration, enable its FTP server (default port **2121**) and verify the availability entity changes correctly. This project does **not** need BinLoader or Klog for counting or CEC control; leave them disabled unless you use separate features that need them. Follow upstream setup requirements for any other integration features.
4. Enable **Settings → System → Enable HDMI Device Link**. Read [Sony's HDMI Device Link documentation](https://manuals.playstation.net/document/en/ps4/settings/devicelink.html); support varies by the connected devices and activity.
5. Save your game, manually enter Rest Mode, verify the steady orange indicator, wake using the controller and verify GoldHEN is still functional. Stop installation if this basic test fails.

## Before installation: TV and HDMI chain

1. Enable the TV's HDMI-CEC / device-link and relevant standby controls, following its own manual. Names differ between manufacturers.
2. Connect PS4 through the HDMI chain you will actually use. Receivers, switches and streaming devices can change CEC behaviour.
3. Add the TV to HA and test its off action while present. Check the actual screen, PS4 LED and any other connected devices. A TV API reporting `off` may not mean the panel is fully black.
4. Run the supplied CEC adapter only after saving the game. Confirm **steady orange on PS4**, then wake with the controller and recheck GoldHEN.
5. Separately test other HDMI devices waking/sleeping. Confirm there is no unwanted wake loop. This bundle does not turn a streaming box on or off.
6. Enable schedule enforcement only after this complete physical test. Otherwise install the dashboard/reminders alone and leave enforcement disabled.

CEC is an interoperability mechanism, not an acknowledgement that PS4 reached Rest Mode. The adapter waits up to 45 seconds for FTP to go offline and reports a failure if it does not; offline is still only a network observation. No hard power cut or working `standby.bin` is included.
