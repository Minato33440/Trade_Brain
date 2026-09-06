"""確定済みの値が後から変わったことを検出できることを固定するテスト。

実行:  python tests/test_value_ledger.py        （pytest 不要。本リポには pytest が入っていない）
       pytest tests/test_value_ledger.py        （入れた場合はこちらでも収集される）

★背景（2026-09-06 の実測事故）
    `GC=F`（機械の XAU/USD）が、**同じ 2026-09-04 の終値**として1時間以内に

        12:32 実行        4,429.800   （Boss 現物 4,431.07 との差 -1.27）
        約1時間後の再実行  4,476.600   （差 +45.53）

    を返した。**+46.80 / +1.06%。日付は両方とも正しい。値だけが変わった。**
    `fast_info.lastPrice` が 4,476.60 と一致していたため、**ライブ気配が最終バーを
    上書きしている**のが濃厚（ロールなら価格差はもっと不規則になるはずで、
    +46.80 が当日の値動きの範囲に収まっているのが傍証。⚠️ただし断定はしない）。

★これまでに塞いだ層との関係

    | 故障 | 症状 | 検出手段 |
    |---|---|---|
    | 2026-08-28 | 日付が割れる | H-4（per-pair as_of） |
    | 2026-08-28 | NaN が誤ラベル化 | H-3（`build_regime_snapshot._num()`） |
    | **2026-09-06** | ★**日付は正しいが値が変わる** | ★**本テストが守る層** |

    ★**確定した値が後から変わるので、一度取った値と後で取った値を照合しないと分からない。**
    H-3 も H-4 も、単発のスナップショットの中だけを見ているので原理的に捕まえられない。
"""

from __future__ import annotations

import sys
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.market import record_and_check_values  # noqa: E402

TODAY = date.today()
D1 = TODAY - timedelta(days=3)
D2 = TODAY - timedelta(days=2)


def _series(pairs):
    idx = pd.to_datetime([d for d, _ in pairs])
    return pd.Series([v for _, v in pairs], index=idx)


def test_first_observation_records_and_reports_nothing():
    ledger = {}
    revs = record_and_check_values("XAU/USD", _series([(D1, 4429.8)]), ledger, "t0")
    assert revs == [], f"初回観測で改訂が出ている: {revs}"
    assert ledger["XAU/USD|" + D1.isoformat()]["value"] == 4429.8


def test_same_value_again_is_not_a_revision():
    ledger = {}
    record_and_check_values("XAU/USD", _series([(D1, 4429.8)]), ledger, "t0")
    revs = record_and_check_values("XAU/USD", _series([(D1, 4429.8)]), ledger, "t1")
    assert revs == [], f"同じ値なのに改訂が出ている（常時点灯の元）: {revs}"


def test_changed_value_is_detected():
    """★本命。2026-09-06 の GC=F と同じ形を再現する。"""
    ledger = {}
    record_and_check_values("XAU/USD", _series([(D1, 4429.8)]), ledger, "12:32")
    revs = record_and_check_values("XAU/USD", _series([(D1, 4476.6)]), ledger, "13:40")

    assert len(revs) == 1, f"確定済みの値が変わったのに検出されていない: {revs}"
    r = revs[0]
    assert r["first"] == 4429.8 and r["now"] == 4476.6
    assert round(r["delta"], 2) == 46.80
    assert round(r["delta_pct"], 2) == 1.06
    assert r["first_seen"] == "12:32", "初回観測の時刻が失われている"


def test_first_value_is_never_overwritten():
    """★改訂は積む。初回値は上書きしない（遡及編集の禁止と同じ扱い）。"""
    ledger = {}
    record_and_check_values("XAU/USD", _series([(D1, 4429.8)]), ledger, "t0")
    record_and_check_values("XAU/USD", _series([(D1, 4476.6)]), ledger, "t1")
    record_and_check_values("XAU/USD", _series([(D1, 4500.0)]), ledger, "t2")

    rec = ledger["XAU/USD|" + D1.isoformat()]
    assert rec["value"] == 4429.8, f"初回値が上書きされている: {rec['value']}"
    assert [x["value"] for x in rec["revisions"]] == [4476.6, 4500.0], (
        "改訂の履歴が積まれていない"
    )


def test_todays_bar_is_never_ledgered():
    """★当日の足は台帳に入れない — 動いて当たり前で、入れると毎回改訂が出る。

    ★**常時点灯する条件は警告にしない**（Boss 2026-09-06）。
      H-4 で 24/7 銘柄を `off_calendar_*` に分けたのと同じ一般則。
      これを外すと、毎日「値が変わった」が出て**本当に変わった日を見落とす。**
    """
    ledger = {}
    revs = record_and_check_values("BTC/USD", _series([(TODAY, 79800.0)]), ledger, "t0")
    assert revs == [] and ledger == {}, "当日の足が台帳に入っている（常時点灯の原因）"

    # 当日の足が動いても改訂にはならない
    revs = record_and_check_values("BTC/USD", _series([(TODAY, 79900.0)]), ledger, "t1")
    assert revs == [] and ledger == {}


def test_nan_is_not_a_value():
    """NaN は「値が変わった」ではなく「値が無い」。台帳に入れない（H-3 と同じ扱い）。"""
    ledger = {}
    revs = record_and_check_values("US100", _series([(D1, float("nan"))]), ledger, "t0")
    assert revs == [] and ledger == {}, "NaN が値として台帳に入っている"


def test_float_noise_does_not_fire():
    """浮動小数の表現ゆらぎで誤検知しない（相対許容差）。"""
    ledger = {}
    record_and_check_values("US10Y", _series([(D1, 4.784)]), ledger, "t0")
    revs = record_and_check_values("US10Y", _series([(D1, 4.784 + 1e-12)]), ledger, "t1")
    assert revs == [], f"表現ゆらぎで改訂が出ている: {revs}"


def test_multiple_dates_are_tracked_independently():
    ledger = {}
    record_and_check_values("WTI", _series([(D1, 89.0), (D2, 91.0)]), ledger, "t0")
    revs = record_and_check_values("WTI", _series([(D1, 89.0), (D2, 92.5)]), ledger, "t1")
    assert len(revs) == 1 and revs[0]["date"] == D2.isoformat(), (
        f"変わった日付だけが出ていない: {revs}"
    )


def _main() -> int:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failures = []
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
        except AssertionError as e:
            failures.append((t.__name__, str(e)))
            print(f"  FAIL  {t.__name__}")
    print()
    if failures:
        print(f"{len(failures)} / {len(tests)} failed:")
        for name, msg in failures:
            print(f"\n--- {name}\n{msg}")
        return 1
    print(f"{len(tests)} / {len(tests)} passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
