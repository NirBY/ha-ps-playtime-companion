# Validation and commissioning

## Checks performed for this bundle

- Six local tests: Blueprint input references, persistent helper/default coverage, graph aggregation and popup links, repeated quiet-hour guard, non-cascading entity mapping, and a credential/private-host scan.
- The three Blueprints were expanded with real entity inputs. Home Assistant's read-only `validate_config` API accepted the resulting triggers, conditions and actions. This is **not** a complete import/install test of a fresh HA instance.
- Expanded enforcement templates were rendered by HA for 210 weekday/weekend/time/quota cases; all passed.
- Expanded reminder quiet guards were rendered at midnight, 11:59, 12:00, 17:59, 18:00 and 23:59; all passed.
- The live Bubble dashboard rendered without configuration-error cards. Weekday/Friday settings pop-ups and the monthly navigation/chart were checked in the browser.
- The statistics API returned a real daily change record for the active-hours sensor. Historical weeks/months have not yet accumulated. No synthetic past data was created.

No sound, console wake or power action was performed during these configuration/Blueprint checks. Physical CEC behaviour remains specific to the tested hardware; a new user must commission their own Rest Mode action.

## Run portable checks

```sh
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
```

## Before enabling on a new instance

1. Verify helpers have the intended defaults and survive an HA restart.
2. Confirm the console availability sensor and daily hours sensor are correct.
3. Test Rest Mode while present: save the game, confirm the orange LED, wake with the controller and verify GoldHEN.
4. Confirm the provider accepts the configured language and speaker target. Test speech only during the allowed window.
5. Test the quiet guard at/after the end time without overriding conditions.
6. Enable only one enforcement automation and one reminder automation to prevent duplicate actions.
7. Check statistics after the first full day and across local midnight; the installation day can undercount because of the initial statistics baseline.

## Known limits

No full HA version matrix, real month of collected usage, or automated hardware/power test is included. The GitHub CI performs structural tests only. Custom action selectors can contain arbitrary user actions; choosing a delayed announcement means its playback-time quiet guard is the installer's responsibility.

Extra-time update: seven additional templates checked bonus expiry, quota exhaustion, pre-opening/closing boundaries and countdown values. All passed using HA template rendering.

Manual block: 14 on/off combinations across schedule/quota scenarios passed through HA template rendering. No block was activated and no physical power action was sent during this check.
