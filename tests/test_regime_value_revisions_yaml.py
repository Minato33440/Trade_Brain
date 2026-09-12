"""改訂ありのsnapshotも有効なYAMLであることを固定する回帰テスト。

実行（requirements-test.txt の PyYAML が必要）:
    python tests/test_regime_value_revisions_yaml.py

市場データ取得の本番依存は変更しない。初回は既存の PyYAML 6.0.3 を持つ
ローカル Python で検証した。テスト用依存は requirements-test.txt に分離する。

背景:
    snapshot_date_integrity.value_revisions が sequence として始まった直下に
    note mapping を出していたため、改訂が発生した週だけ ParserError となった。
"""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.regime import build_regime_snapshot  # noqa: E402


PAIRS = [
    "USD/JPY", "US100", "JP225", "XAU/USD", "WTI",
    "US3M", "US5Y", "VIX", "US10Y", "US30Y", "BTC/USD",
]


def _snapshots(revisions):
    snapshots = {
        pair: {
            "latest": 100.0,
            "first": 99.0,
            "prev_1w": 99.5,
            "change_30d": 1.0,
            "as_of": "2026-09-11",
            "first_as_of": "2026-08-13",
            "prev_1w_as_of": "2026-09-04",
        }
        for pair in PAIRS
    }
    if revisions:
        snapshots["_value_revisions"] = revisions
    return snapshots


def _render(revisions):
    _, _, text = build_regime_snapshot(
        date(2026, 8, 13), date(2026, 9, 12), _snapshots(revisions)
    )
    return text


def test_zero_revisions_remains_parseable_and_omits_block():
    doc = yaml.safe_load(_render([]))
    assert "value_revisions" not in doc["snapshot_date_integrity"]


def test_multiple_revisions_remain_parseable_and_preserve_history():
    revisions = [
        {
            "pair": "USD/JPY",
            "date": "2026-09-04",
            "first": 156.2209930419922,
            "now": 155.66000366210938,
            "delta": -0.560989,
            "delta_pct": -0.3591,
            "first_seen": "2026-09-06T17:48",
        },
        {
            "pair": "XAU/USD",
            "date": "2026-09-04",
            "first": 4476.60009765625,
            "now": 4429.7998046875,
            "delta": -46.800293,
            "delta_pct": -1.0454,
            "first_seen": "2026-09-06T17:48",
        },
    ]

    doc = yaml.safe_load(_render(revisions))
    integrity = doc["snapshot_date_integrity"]
    records = integrity["value_revisions"]
    assert len(records) == 2
    assert records[0]["pair"] == "USD/JPY"
    assert records[0]["first"] == revisions[0]["first"]
    assert records[0]["now"] == revisions[0]["now"]
    assert records[1]["pair"] == "XAU/USD"
    assert records[1]["first_seen"] == revisions[1]["first_seen"]
    assert "初回値は台帳側で保持" in integrity["value_revisions_note"]


def _main() -> int:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for test in tests:
        test()
        print(f"  PASS  {test.__name__}")
    print(f"{len(tests)} / {len(tests)} passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
