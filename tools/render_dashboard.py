"""Render a portable dashboard without connecting to Home Assistant."""
import argparse
from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]

def render(value, mapping, dashboard_path):
    if isinstance(value, str):
        # One pass prevents A -> B -> C accidental chained replacements.
        pattern = re.compile('|'.join(re.escape(k) for k in sorted(mapping, key=len, reverse=True))) if mapping else None
        if pattern:
            value = pattern.sub(lambda m: mapping[m.group()], value)
        return value.replace('/ps4-settings/', '/' + dashboard_path + '/')
    if isinstance(value, list):
        return [render(v, mapping, dashboard_path) for v in value]
    if isinstance(value, dict):
        return {k: render(v, mapping, dashboard_path) for k, v in value.items()}
    return value

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mapping', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--dashboard-path', default='ps4-settings')
    args = parser.parse_args()
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)+', args.dashboard_path):
        parser.error('Dashboard path must be lowercase and contain a hyphen.')
    mapping = yaml.safe_load(args.mapping.read_text(encoding='utf-8'))
    if not isinstance(mapping, dict) or not all(isinstance(k, str) and isinstance(v, str) and re.fullmatch(r'[a-z_]+\.[a-z0-9_]+', v) for k, v in mapping.items()):
        parser.error('Mapping must contain entity_id: entity_id pairs.')
    data = yaml.safe_load((ROOT/'dashboard/bubble.yaml').read_text(encoding='utf-8'))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(yaml.safe_dump(render(data, mapping, args.dashboard_path), allow_unicode=True, sort_keys=False), encoding='utf-8')
    print(f'Dashboard written to {args.output}')

if __name__ == '__main__':
    main()
