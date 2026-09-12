"""Read-only, provider-neutral checks for a GM weekly artifact directory."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from decimal import Decimal
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote

import yaml


class UniqueLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError(f'Duplicate YAML key: {key}')
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []
        self.remote_assets = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'a' and attrs.get('href'):
            self.urls.append(attrs['href'])
        if tag in {'img', 'script', 'link', 'iframe'}:
            url = attrs.get('src', attrs.get('href', ''))
            if url.startswith(('http:', 'https:', '//')):
                self.remote_assets.append(url)
            elif url:
                self.urls.append(url)


def validate(root: Path, week: str):
    if not re.fullmatch(r'\d{4}-\d{1,2}-\d{1,2}_wk\d{2}', week):
        raise ValueError('week must use YYYY-M-D_wkNN (not a path)')
    root = root.resolve()
    folder = root / 'logs' / 'weekly' / week[:4] / week
    checks = []

    def record(name, ok, detail=None, optional=False):
        checks.append({'check': name, 'status': 'pass' if ok else ('warning' if optional else 'fail'), 'detail': detail})

    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def relative(base, name):
        # Input manifests produced on Windows can be read on another OS too.
        p = (base / name.replace('\\', '/')).resolve()
        if not p.is_relative_to(root):
            raise ValueError(f'Artifact path outside repository: {name}')
        return p

    required = ['review.md', 'note.md', 'meta.yaml', 'charts.md', 'trade_results.md']
    record('required_artifacts', all((folder / f).is_file() for f in required),
           [f for f in required if not (folder / f).is_file()])
    meta = {}
    try:
        meta = yaml.load((folder / 'meta.yaml').read_text(encoding='utf-8-sig'), Loader=UniqueLoader)
        if not isinstance(meta, dict):
            raise ValueError('meta must be a mapping')
        record('meta_yaml', True)
        record('meta_week', meta.get('week') == week, meta.get('week'))
    except (OSError, ValueError, yaml.YAMLError) as exc:
        record('meta_yaml', False, str(exc))
        meta = {}

    for path in sorted((folder / 'charts').glob('*.yaml')):
        if path.name.endswith('.raw.yaml'):
            continue  # Raw output may be intentionally invalid; preserve rather than repair it here.
        try:
            yaml.load(path.read_text(encoding='utf-8-sig'), Loader=UniqueLoader)
            record('yaml:' + path.name, True)
        except (OSError, ValueError, yaml.YAMLError) as exc:
            record('yaml:' + path.name, False, str(exc))

    manifest_path = folder / 'charts/input_manifest.json'
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding='utf-8-sig'))
            for item in manifest.get('archives', []):
                p = relative(folder, item['archive'])
                record('archive:' + item['archive'], p.is_file() and digest(p) == item['sha256'])
            for item in manifest.get('derived_files', []):
                p = relative(folder, item['path'])
                record('derived:' + item['path'], p.is_file() and digest(p) == item['sha256'])
            for item in manifest.get('source_revisions', []):
                p = relative(folder, item['archive'])
                record('source_revision:' + item['path'], p.is_file() and digest(p) == item['current_sha256'])
                record('initial_hash_history:' + item['path'],
                       manifest['input_checksums'].get(item['path']) == item['initial_sha256'])
            hashes = manifest.get('current_input_checksums', manifest.get('input_checksums', {}))
            record('input_checksums_present', bool(hashes), optional=True)
            for name, expected in hashes.items():
                p = relative(root, name)
                if p.is_file():
                    record('input:' + name, digest(p) == expected,
                           'Mismatch requires source/version review, never silent hash replacement.')
                else:
                    record('input:' + name, False, 'Original unavailable; inspect preserved archive.', optional=True)
        except (OSError, ValueError, KeyError, TypeError) as exc:
            record('manifest', False, str(exc))
    else:
        record('input_manifest', False, 'No manifest; source integrity needs manual review.', optional=True)

    # Schemas vary by week; absent accounting evidence is visible, never a guessed zero.
    ports = [v for k, v in meta.items() if k.startswith('portfolio_snapshot_') and isinstance(v, dict)]
    record('portfolio_evidence', bool(ports), optional=True)
    for index, portfolio in enumerate(ports):
        try:
            positions = portfolio['positions']
            total = sum(Decimal(str(p['value_jpy'])) for p in positions)
            total += Decimal(str(portfolio['sweep_jpy']))
            record(f'portfolio_total:{index}', total == Decimal(str(portfolio['total_assets_jpy'])))
            if 'unrealized_pnl_jpy' in portfolio:
                record(f'portfolio_pnl:{index}', sum(Decimal(str(p['unrealized_pnl_jpy'])) for p in positions)
                       == Decimal(str(portfolio['unrealized_pnl_jpy'])))
            if 'week_change_adjusted_jpy' in portfolio:
                record(f'portfolio_week_change:{index}', sum(Decimal(str(p['week_value_change_jpy'])) for p in positions)
                       == Decimal(str(portfolio['week_change_adjusted_jpy'])))
        except (KeyError, TypeError, ArithmeticError) as exc:
            record(f'portfolio_schema:{index}', False, str(exc))
    bridge = meta.get('weekly_pnl_bridge')
    record('weekly_pnl_bridge_present', isinstance(bridge, dict), optional=True)
    if isinstance(bridge, dict):
        try:
            change = Decimal(bridge['current_unrealized_pt_lot']) - Decimal(bridge['prior_unrealized_pt_lot'])
            record('unrealized_change', change == Decimal(bridge['change_unrealized_pt_lot']))
            record('weekly_pnl_bridge', Decimal(bridge['realized_pt_lot']) + change == Decimal(bridge['change_marked_total_pt_lot']))
        except (KeyError, TypeError, ArithmeticError) as exc:
            record('weekly_pnl_bridge', False, str(exc))
    if isinstance(meta.get('carry_forward'), list):
        ids = [item.get('id') for item in meta['carry_forward']]
        record('carry_forward_unique_ids', all(ids) and len(ids) == len(set(ids)))

    files = sorted(folder.glob('*.md')) + sorted(folder.glob('*.html'))
    bad_links = []
    for p in files:
        text = p.read_text(encoding='utf-8-sig')
        if p.suffix == '.html':
            parsed = Links()
            parsed.feed(text)
            urls = parsed.urls
            record('html_remote_assets:' + p.name, not parsed.remote_assets, parsed.remote_assets, optional=True)
        else:
            urls = [a or b for a, b in re.findall(r'\[[^\]\n]*\]\((?:<([^>]+)>|([^\s\)]+))\)', text)]
        for url in urls:
            if url.startswith(('#', '//')) or re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', url):
                continue
            target = (p.parent / unquote(url.split('#')[0])).resolve()
            if not target.exists():
                bad_links.append({'file': p.name, 'url': url})
    record('local_links', not bad_links, bad_links)
    record('human_html_present', bool(list(folder.glob('CFD_Strategy-*.html'))), optional=True)
    return {'week': week, 'status': 'fail' if any(c['status'] == 'fail' for c in checks) else 'pass',
            'checks': checks, 'warnings': sum(c['status'] == 'warning' for c in checks),
            'scope': 'Local integrity and arithmetic only; source extraction, market interpretation and visual review remain Broker work.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--week', required=True)
    args = parser.parse_args()
    try:
        result = validate(args.root, args.week)
    except (OSError, ValueError, TypeError) as exc:
        result = {'status': 'fail', 'error': str(exc)}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['status'] == 'pass' else 1


if __name__ == '__main__':
    raise SystemExit(main())
