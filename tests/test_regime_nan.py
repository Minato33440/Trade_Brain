"""NaN が「欠損」ではなく【誤ったラベル】に化けないことを固定するテスト。

実行:  python tests/test_regime_nan.py        （pytest 不要。本リポには pytest が入っていない）
       pytest tests/test_regime_nan.py        （入れた場合はこちらでも収集される）

★背景（2026-08-28 の実測事故）
    Yahoo 側の欠測で US100 の値が NaN になった週、機械は次を出した:

        regime.equities            = "flat"     ← unknown ではなく
        relative_strength.verdict  = "mixed"    ← 算出不能ではなく

    NaN は比較演算がすべて False になるため、`if x is None` だけを見ている判定関数は
    NaN を素通しし、**分岐を全部すり抜けて末尾の無条件 return に落ちる**。
    どちらの出力も「値が無い」ではなく「間違った値」で、
    settings.py 冒頭の《欠損は気づかれるが、間違った値は気づかれない》そのものの事故。

★Boss訂正（2026-08-29）
    「これは上の2関数だけの問題ではない。末尾に無条件 return を持つ判定関数は
      すべて同じ穴を持つ。個別に if を足すのは対症療法。
      監査範囲は終端フォールバックを持つ判定関数の悉皆、
      是正は各判定関数に NaN を食わせて unknown が返ることを確認するテストを1本書く。
      **関数ごとに if を足すのではなく、テストが穴の一覧を出す形にする。**」

    → 実装側は `build_regime_snapshot._num()` で入口を1箇所に絞って NaN を None に落とす。
      本テストはその回帰を固定し、**新しい判定関数を足したときに穴が開いたら落ちる**。
"""

from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.regime import build_regime_snapshot  # noqa: E402

NAN = float("nan")

PAIRS = [
    "US100", "JP225", "BTC/USD", "WTI", "VIX", "XAU/USD",
    "US3M", "US5Y", "US10Y", "US30Y", "USD/JPY",
]

# 判定キーと、「値が無いとき」に出てよい語。ここに無い語が出たら誤ったラベル。
TERMINAL_LABELS = {
    "equities": {"unknown"},
    "volatility": {"unknown"},
    "oil": {"unknown"},
    "gold": {"unknown"},
    "crypto": {"unknown"},
    "yields": {"unknown"},
}


def _snapshots(value):
    """全ペアを同じ値で埋めた pair_snapshots を作る。"""
    return {
        p: {"latest": value, "change_30d": value, "first": value, "prev_1w": value}
        for p in PAIRS
    }


def _labels(yaml_text: str) -> dict:
    """regime ブロックの key: value を素朴に拾う（PyYAML 非依存）。"""
    out = {}
    in_regime = False
    for line in yaml_text.splitlines():
        if line.startswith("regime:"):
            in_regime = True
            continue
        if in_regime:
            if line and not line.startswith(" "):
                break
            m = re.match(r"\s+(\w+):\s*(\S+)", line)
            if m:
                out[m.group(1)] = m.group(2).strip('"')
    return out


def _yaml_for(value):
    _, _, yaml_text = build_regime_snapshot(
        date(2026, 8, 1), date(2026, 8, 28), _snapshots(value)
    )
    return yaml_text


def test_missing_inputs_never_become_a_label():
    """None でも NaN でも、判定は unknown に落ちること。

    ★NaN のケースが本命。None は「もともと通っていた経路」で、
      2つを同じ表明で縛ることで **NaN が None と同じ扱いになった**ことを示す。
    """
    for name, missing in (("none", None), ("nan", NAN)):
        labels = _labels(_yaml_for(missing))
        bad = {
            k: labels.get(k)
            for k, allowed in TERMINAL_LABELS.items()
            if labels.get(k) not in allowed
        }
        assert not bad, (
            f"[{name}] 欠損入力が【誤ったラベル】に化けている（終端フォールバックに落ちた）: "
            f"{bad}。判定関数の末尾に無条件 return があり、入口で欠損を潰せていない。"
        )


def test_relative_strength_is_absent_not_mixed():
    """相対強度は算出不能なら【出さない】こと。verdict: mixed を出さない。

    2026-08-28 は us100_30d / nominal / fx_adj がすべて nan のまま
    `verdict: mixed` が出力された。mixed は「拮抗している」という意味を持つラベルで、
    「計算できなかった」ではない。
    """
    for name, missing in (("none", None), ("nan", NAN)):
        yaml_text = _yaml_for(missing)
        assert "relative_strength:" not in yaml_text, (
            f"[{name}] 入力が欠損なのに relative_strength ブロックが出力されている。"
        )
        assert "verdict: mixed" not in yaml_text, f"[{name}] verdict: mixed が出ている。"


def test_nan_and_none_produce_the_same_regime_block():
    """NaN と None が同じ出力になること（＝NaN が特別扱いを失っている）。

    ★これが本丸。個別の if を足していく是正では、直し忘れた関数だけ差分が残る。
      ブロック全体の一致で縛れば、**新しい判定関数を足したときに穴が開いたら落ちる。**
    """
    a, b = _labels(_yaml_for(None)), _labels(_yaml_for(NAN))
    diff = {k: (a.get(k), b.get(k)) for k in set(a) | set(b) if a.get(k) != b.get(k)}
    assert not diff, (
        f"NaN と None で regime ラベルが異なる＝どこかの判定関数がまだ NaN を素通ししている: {diff}"
    )


def test_partial_nan_only_affects_the_missing_pair():
    """1ペアだけ NaN でも、そのペアの判定だけが unknown になること。

    全欠損だけを見ていると「全部 unknown を返すだけの関数」でもテストが通ってしまう。
    健全な値が残っている軸は正しく判定され続けることを併せて固定する。
    """
    snaps = _snapshots(None)
    snaps["VIX"] = {"latest": 14.5, "change_30d": -2.5, "first": 14.9, "prev_1w": 15.1}
    snaps["US100"] = {"latest": NAN, "change_30d": NAN, "first": NAN, "prev_1w": NAN}

    _, _, yaml_text = build_regime_snapshot(date(2026, 8, 1), date(2026, 8, 28), snaps)
    labels = _labels(yaml_text)
    assert labels.get("volatility") == "normal", (
        f"健全な入力まで unknown に潰れている: volatility={labels.get('volatility')}"
    )
    assert labels.get("equities") == "unknown", (
        f"NaN の US100 が誤ったラベルに化けている: equities={labels.get('equities')}"
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
        # ★「テストが穴の一覧を出す」— 落ちた表明をまとめて並べる
        print(f"{len(failures)} / {len(tests)} failed:")
        for name, msg in failures:
            print(f"\n--- {name}\n{msg}")
        return 1
    print(f"{len(tests)} / {len(tests)} passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
