import importlib.util
from pathlib import Path
import re
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
class Input(str):
    pass
class Loader(yaml.SafeLoader):
    pass
Loader.add_constructor('!input', lambda loader, node: Input(loader.construct_scalar(node)))

def walk(value):
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)

class BundleTests(unittest.TestCase):
    def test_automatic_locale_and_generic_labels(self):
        text = (ROOT/'dashboard/bubble.yaml').read_text(encoding='utf-8')
        dashboard = yaml.safe_load(text)
        objects = [x for x in walk(dashboard) if isinstance(x, dict)]
        self.assertNotIn('Family Speaker', text)
        self.assertFalse(any(x.get('icon') == 'mdi:translate' for x in objects))
        wrappers = [x for x in objects if x.get('type') == 'custom:config-template-card']
        self.assertTrue(wrappers)
        self.assertTrue(all("this.hass.locale?.language" in x['variables'][0] and "'en'" in x['variables'][0] for x in wrappers))

    def test_bonus_controls_are_conditionally_visible(self):
        dashboard = yaml.safe_load((ROOT/'dashboard/bubble.yaml').read_text(encoding='utf-8'))
        cards = [x for x in walk(dashboard) if isinstance(x, dict) and x.get('type')=='conditional' and 'ps4_add_playtime' in str(x)]
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0]['conditions'], [{'condition':'state','entity':'binary_sensor.ps4_extra_time_available','state':'on'}])
        package = yaml.safe_load((ROOT/'packages/ps4_playtime.yaml').read_text(encoding='utf-8'))
        template = package['template'][0]['binary_sensor'][0]['state']
        self.assertIn('not allowed or', template)
        self.assertIn('used >= hours', template)

    def test_blueprint_inputs_resolve(self):
        for path in (ROOT/'blueprints').rglob('*.yaml'):
            blueprint = yaml.load(path.read_text(encoding='utf-8'), Loader=Loader)
            defined = set(blueprint['blueprint']['input'])
            used = {str(x) for x in walk(blueprint) if isinstance(x, Input)}
            self.assertFalse(used - defined, (path, used-defined))
            self.assertIn(blueprint['blueprint']['domain'], ['automation','script'])

    def test_persistent_helpers_and_defaults(self):
        package = yaml.safe_load((ROOT/'packages/ps4_playtime.yaml').read_text(encoding='utf-8'))
        entities = {f'{domain}.{key}' for domain in ['input_datetime','input_number','input_boolean'] for key in package[domain]}
        actions = package['script']['ps4_initialize_defaults']['sequence']
        self.assertEqual(entities, {a['target']['entity_id'] for a in actions})
        for domain in ['input_datetime','input_number','input_boolean']:
            for config in package[domain].values():
                self.assertNotIn('initial', config)

    def test_chart_and_popup_navigation(self):
        dashboard = yaml.safe_load((ROOT/'dashboard/bubble.yaml').read_text(encoding='utf-8'))
        objects = [x for x in walk(dashboard) if isinstance(x, dict)]
        charts = [x for x in objects if x.get('type')=='statistics-graph']
        self.assertEqual({x['days_to_show'] for x in charts}, {7,30})
        for chart in charts:
            self.assertEqual(chart['stat_types'], ['change'])
            self.assertEqual(chart['period'], 'day')
        popups = [x for x in objects if x.get('card_type')=='pop-up']
        self.assertEqual(len(popups), 5)
        hashes = {x['hash'] for x in popups}
        links = {x['navigation_path'] for x in objects if x.get('action')=='navigate' and x.get('navigation_path','').startswith('#')}
        self.assertEqual(hashes, links)
        self.assertTrue(all(x.get('cards') for x in popups))

    def test_quiet_guard_immediately_precedes_announcement(self):
        config = yaml.load((ROOT/'blueprints/automation/ps4_playtime/reminders.yaml').read_text(encoding='utf-8'), Loader=Loader)
        self.assertEqual(config['conditions'][0], config['actions'][-2])
        self.assertIn('today_at(start) <= now() < today_at(end)', config['actions'][-2]['value_template'])
        self.assertEqual(config['actions'][-1]['choose'][0]['sequence'], 'announcement_actions')

    def test_mapping_is_non_cascading(self):
        spec = importlib.util.spec_from_file_location('renderer', ROOT/'tools/render_dashboard.py')
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        result = mod.render({'text':'sensor.a sensor.b','path':'/ps4-settings/monthly'}, {'sensor.a':'sensor.b','sensor.b':'sensor.c'}, 'my-ps4')
        self.assertEqual(result, {'text':'sensor.b sensor.c','path':'/my-ps4/monthly'})

    def test_no_credentials_or_private_hosts(self):
        pattern = re.compile(r'eyJ[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]+\.|192\.168\.\d+\.\d+|https?://[^\s/]+\.synology\.me')
        for path in ROOT.rglob('*'):
            if path.is_file() and path.suffix in {'.yaml','.yml','.md','.py','.txt'}:
                self.assertIsNone(pattern.search(path.read_text(encoding='utf-8')), str(path))

if __name__ == '__main__':
    unittest.main()
