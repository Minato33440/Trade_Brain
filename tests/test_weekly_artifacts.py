import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

import yaml

spec = importlib.util.spec_from_file_location('weekly_validator', Path(__file__).resolve().parents[1] / 'scripts/validate_weekly_artifacts.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class WeeklyValidationTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.week = '2027-1-8_wk02'
        self.folder = self.root / 'logs/weekly/2027' / self.week
        (self.folder / 'charts').mkdir(parents=True)
        for name in ['review.md', 'note.md', 'charts.md', 'trade_results.md']:
            (self.folder / name).write_text('# Fixture\n', encoding='utf-8')
        self.meta = {'week': self.week, 'weekly_pnl_bridge': {
            'realized_pt_lot': '20.1', 'prior_unrealized_pt_lot': '12.3',
            'current_unrealized_pt_lot': '7.2', 'change_unrealized_pt_lot': '-5.1',
            'change_marked_total_pt_lot': '15.0'}}
        self.save()

    def save(self):
        (self.folder / 'meta.yaml').write_text(yaml.safe_dump(self.meta), encoding='utf-8')

    def run_check(self):
        return module.validate(self.root, self.week)

    def test_other_year_decimal_bridge_and_missing_optional_evidence(self):
        result = self.run_check()
        self.assertEqual(result['status'], 'pass')
        self.assertGreater(result['warnings'], 0)

    def test_realized_is_not_marked_week_change(self):
        self.meta['weekly_pnl_bridge']['change_marked_total_pt_lot'] = '20.1'
        self.save()
        self.assertEqual(self.run_check()['status'], 'fail')

    def test_duplicate_yaml_key_is_rejected(self):
        with (self.folder / 'meta.yaml').open('a', encoding='utf-8') as stream:
            stream.write('week: 2027-1-15_wk03\n')
        self.assertEqual(self.run_check()['status'], 'fail')

    def test_archived_input_tamper_is_rejected(self):
        artifact = self.folder / 'charts/source.txt'
        artifact.write_bytes(b'original')
        manifest = {'archives': [{'archive': 'charts/source.txt', 'sha256': hashlib.sha256(b'original').hexdigest()}]}
        (self.folder / 'charts/input_manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
        artifact.write_bytes(b'changed')
        self.assertEqual(self.run_check()['status'], 'fail')

    def test_broken_relative_link_is_rejected(self):
        (self.folder / 'review.md').write_text('[evidence](charts/missing.json)', encoding='utf-8')
        self.assertEqual(self.run_check()['status'], 'fail')

    def test_week_cannot_escape_repository(self):
        with self.assertRaises(ValueError):
            module.validate(self.root, '../outside')


if __name__ == '__main__':
    unittest.main()
