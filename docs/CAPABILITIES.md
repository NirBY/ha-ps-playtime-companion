# Capabilities: import, setup and examples

All examples use fictional values and generic entity names. Start with [compatibility and dependencies](COMPATIBILITY.md), then install helpers before creating automations. Only import the optional CEC adapter if it fits your hardware.

## Blueprint import buttons

Click the blue button, confirm your own Home Assistant address if asked, preview and import. Create an automation/script from the imported Blueprint and select your entities. Importing does not enable enforcement or operate a device. Commission the Rest Mode action before enabling enforcement.

### Schedule and daily quota enforcement

[![Import blueprint to My Home Assistant](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2FNirBY%2Fha-ps-playtime-companion%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fps4_playtime%2Fenforce.yaml)

[View YAML / manual import URL](https://github.com/NirBY/ha-ps-playtime-companion/blob/main/blueprints/automation/ps4_playtime/enforce.yaml) · [Configured YAML example](../examples/automations.yaml)

**Example:** A fictional weekday allows 12:00–18:00 and 2 hours. A session starting at 17:00 ends at 18:00 even if daily time remains. If the console comes online outside the window, enforcement requests Rest Mode.

### Spoken reminders and quiet hours

[![Import blueprint to My Home Assistant](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2FNirBY%2Fha-ps-playtime-companion%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fps4_playtime%2Freminders.yaml)

[View YAML / manual import URL](https://github.com/NirBY/ha-ps-playtime-companion/blob/main/blueprints/automation/ps4_playtime/reminders.yaml) · [Configured YAML example](../examples/automations.yaml)

**Example:** With a planned end at 17:00, reminders fall at 16:30, 16:50 and 16:59. With speech allowed 12:00–18:00, a reminder at 19:30 is skipped. Choose your own speaker and TTS provider; pass `{{ message }}` to the announcement action.

### CEC Rest Mode adapter

[![Import blueprint to My Home Assistant](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2FNirBY%2Fha-ps-playtime-companion%2Fblob%2Fmain%2Fblueprints%2Fscript%2Fps4_playtime%2Fcec_rest.yaml)

[View YAML / manual import URL](https://github.com/NirBY/ha-ps-playtime-companion/blob/main/blueprints/script/ps4_playtime/cec_rest.yaml) · [Configured YAML example](../examples/scripts.yaml)

**Example:** The script sends turn_off to the selected TV and waits for the console availability sensor to go offline. Confirm a steady orange console LED, then wake with the PS4 controller and verify GoldHEN. Behaviour depends on HDMI-CEC hardware; this is not a standby.bin payload.

The YAML examples use the folder layout from manual installation (`ps4_playtime/...`). URL imports may store Blueprints under a different author folder: use the UI to create the instance, or replace `use_blueprint.path` with the path actually imported. Do not copy an example path blindly.

## Helpers and controls

[![Install helpers](https://img.shields.io/badge/INSTALL-HELPERS_AND_CONTROLS-00b8e6?style=for-the-badge)](INSTALL.he.md#2-helpers-וחיישן-זמן)

1. Copy [the package](../packages/ps4_playtime.yaml) into `/config/packages/` and replace the generic availability sensor with yours.
2. Enable packages in your existing `homeassistant:` configuration, check configuration and restart HA.
3. Run `script.ps4_initialize_defaults` once. Re-running resets preferences. Existing installations should reuse helpers rather than duplicate them.

**Example:** initialize weekday quota to 2 hours, then edit it to 2.5 hours in the dashboard. Later restarts preserve the edited value. Package scripts supply bonus and manual-block controls; no extra Blueprint is needed for these buttons.

## Bubble dashboard

[![Install dashboard](https://img.shields.io/badge/INSTALL-BUBBLE_DASHBOARD-00b8e6?style=for-the-badge)](INSTALL.he.md#4-לוח-bubble)

Install Bubble Card 3.2+, card-mod and config-template-card using the [dependency links](COMPATIBILITY.md). Set your entity names in [the mapping](../dashboard/entities.example.yaml), then run from this repository:

```sh
python -m pip install -r requirements-dev.txt
python tools/render_dashboard.py --mapping dashboard/entities.example.yaml --output dashboard/rendered.yaml
```

Create a dashboard with URL path `ps4-settings`. Paste `dashboard/rendered.yaml` into its Raw configuration editor. Use `--dashboard-path your-dashboard` if choosing another path.

**Example:** a Hebrew HA profile displays RTL; an English or unsupported language displays English LTR. There is no language button. Reload after changing the profile language.

![Fictional English dashboard example](images/demo-en.png)

<details><summary>Hebrew RTL example</summary>

![Fictional Hebrew dashboard example](images/demo-he.png)

</details>

## Weekly and monthly charts

[![Install Weekly and monthly charts](https://img.shields.io/badge/INSTALL-CHARTS-00b8e6?style=for-the-badge)](#helpers-and-controls)

**Install:** included in the dashboard and package above; no separate import.

**Example:** Monday 1 hour, Tuesday 1.5 hours and Wednesday 0.5 hours appear as daily usage in the seven-day chart. Open monthly view for the last 30 days (a rolling window, not a calendar month).

Charts use recorded statistics, not these fictional values. The first day can be partial and missing days do not mean zero usage. No demo history is injected into HA.

## Extra time and countdown

[![Install Extra time and countdown](https://img.shields.io/badge/INSTALL-EXTRA_TIME-00b8e6?style=for-the-badge)](#helpers-and-controls)

**Install:** included in the dashboard and helpers package above; map the bonus script and sensors to your entities.

**Example:** at 16:00 a 2-hour daily quota is exhausted. Press +15 minutes: the available daily allowance increases by 15 minutes, showing 00:15 if closing time is at least 15 minutes away. The countdown reflects the earlier of remaining allowance and closing time. Online time consumes allowance; offline time does not.

Buttons appear only outside allowed hours and/or after quota exhaustion. Adding bonus outside allowed hours does **not** authorize play or extend closing time. Bonus expires at local midnight. Invalid schedules hide the buttons.

## Manual block and release

[![Install Manual block and release](https://img.shields.io/badge/INSTALL-MANUAL_BLOCK-00b8e6?style=for-the-badge)](#helpers-and-controls)

**Install:** included in the package/dashboard; ensure `script.ps4_block_playtime` targets your actual enforcement automation, and update dashboard mapping if renamed.

**Example:** at 15:00 with time remaining, select Block now. Enforcement is enabled, the manual lock is set, and an online console receives the configured Rest Mode action. Block now hides while blocked by schedule/quota or manually. Release manual block clears the manual lock only; it neither wakes the console nor overrides other limits. The lock persists across midnight and restarts until released.

## Editable schedules

[![Install Editable schedules](https://img.shields.io/badge/INSTALL-SCHEDULE_SETTINGS-00b8e6?style=for-the-badge)](#helpers-and-controls)

**Install:** included in the helpers package, enforcement Blueprint and dashboard.

**Example:** open Friday settings, choose 08:00, 5 hours and disable closing time. Play is permitted from 08:00 until quota exhaustion or midnight; Saturday rules then take over. Open speech settings to set 12:00–18:00 and 30/10/1-minute reminders. Quiet hours still apply on weekends. Same-day windows only; invalid windows show a warning.

## Import reference

The blue badges use the official [My Home Assistant Blueprint import redirect](https://my.home-assistant.io/redirect/blueprint_import/). Dashboard and package buttons open installation instructions because these file types are not importable Blueprints.
