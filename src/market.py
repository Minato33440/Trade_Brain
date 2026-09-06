"""市場データ取得・スナップショット生成モジュール。

yfinance によるリアルタイム/ヒストリカルデータ取得、
フォーマット出力を担当する。
"""
from __future__ import annotations

import csv
import io
import json
import urllib.request
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
import yfinance as yf

from configs.settings import (
    CORE_TICKERS,
    FRED_CSV_URL,
    FRED_SERIES,
    FULL_TICKERS,
    TRADE_PAIRS,
)
from src.data_fetch import fetch_market_data


def get_market_snapshot(full_mode: bool = False) -> Dict[str, Dict[str, Any]]:
    """対話モード用: 直近5日のスナップショットを取得。"""
    tickers = FULL_TICKERS if full_mode else CORE_TICKERS
    snapshot: Dict[str, Dict[str, Any]] = {}
    for name, symbol in tickers.items():
        try:
            data = yf.download(symbol, period="5d", progress=False)

            if data.empty:
                snapshot[name] = {"error": "データ空 (yfinanceから空DF返却)"}
                continue

            close_series = data["Close"]
            if close_series.empty:
                snapshot[name] = {"error": "Close列が空"}
                continue

            latest = float(close_series.iloc[-1])
            prev = float(close_series.iloc[-2]) if len(close_series) >= 2 else None
            change_pct = ((latest - prev) / prev * 100) if prev is not None else 0.0
            snapshot[name] = {
                "latest": round(latest, 4 if "/" in name or "VIX" in name else 2),
                "change_pct": round(change_pct, 2),
            }
        except Exception as e:
            snapshot[name] = {"error": str(e)}
    return snapshot


def get_current_market_snapshot(
    tickers: Optional[List[str]] = None,
) -> Dict[str, Dict[str, Any]]:
    """チャット内で市場データをフェッチ（yfinance優先、Polygonフォールバック）。"""
    if tickers is None:
        tickers = ["USDJPY=X", "GC=F"]
    end_d = date.today()
    start_d = end_d - timedelta(days=7)
    snapshot: Dict[str, Dict[str, Any]] = {}
    for ticker in tickers:
        data = fetch_market_data(ticker, start_d, end_d)
        if data is not None and not data.empty:
            latest = float(data.iloc[-1])
            change = (
                (float(data.iloc[-1]) - float(data.iloc[-2]))
                / float(data.iloc[-2])
                * 100
                if len(data) >= 2
                else 0.0
            )
            snapshot[ticker] = {
                "latest": round(latest, 4 if "=X" in ticker or "=F" in ticker else 2),
                "change_pct": round(change, 2),
            }
        else:
            snapshot[ticker] = {"error": "Data fetch failed"}
    return snapshot


def format_snapshot(snapshot: Dict[str, Dict[str, Any]]) -> str:
    """スナップショットをテキスト表示用にフォーマット。"""
    lines = ["トレードモード起動！ 最新市場スナップショット（yfinanceより）:"]
    lines.append(f"現在時刻: {datetime.now().strftime('%Y/%m/%d %H:%M JST')}")
    lines.append("")

    groups = {
        "為替": [k for k in snapshot if ("/" in k and "JPY" in k) or "USD" in k],
        "指数": [k for k in snapshot if "US100" in k or "SP500" in k or "JP225" in k],
        "商品・暗号": [
            k
            for k in snapshot
            if "XAU" in k or "BTC" in k or "Copper" in k or "WTI" in k
        ],
        "金利・ボラ": [k for k in snapshot if "Y" in k or "VIX" in k],
    }

    for group_name, keys in groups.items():
        if any(k in snapshot for k in keys):
            lines.append(f"【{group_name}】")
            for key in keys:
                if key in snapshot:
                    info = snapshot[key]
                    if "error" in info:
                        lines.append(
                            f"{key}: 取得失敗 → {info['error'][:100]}..."
                        )
                    else:
                        lines.append(
                            f"{key}: {info['latest']} (前日比 {info['change_pct']:+.2f}%)"
                        )
            lines.append("")

    lines.append("ボス、この状況で何が気になる？ シフトの予兆？ ポジション考えようか？")
    return "\n".join(lines)


# ── 確定値の改訂検出（★2026-09-06 追加 / Rex提案・Boss 2026-09-06）──────────
#
# ★これまでに塞いだ層と、塞げていなかった層:
#
#   | 故障 | 症状 | 検出手段 |
#   |---|---|---|
#   | 2026-08-28 | 日付が割れる | H-4（per-pair as_of） |
#   | 2026-08-28 | NaN が誤ラベル化 | H-3（build_regime_snapshot._num()） |
#   | **2026-09-06** | ★**日付は正しいが値が変わる** | ★**本ブロック** |
#
# 2026-09-06、`GC=F` が同じ 2026-09-04 の終値として1時間以内に
#   4,429.800 → 4,476.600（+46.80 / +1.06%）
# を返した。**日付は両方とも正しい。値だけが変わった。**
# `fast_info.lastPrice` が 4,476.60 と一致していたため、
# **ライブ気配が最終バーを上書きしている**のが濃厚
# （★ロールなら価格差はもっと不規則になるはずで、+46.80 が当日の値動きの範囲に
#   収まっているのが傍証。⚠️ただし断定はしない）。
#
# ★**確定した値が後から変わるので、一度取った値と後で取った値を照合しないと分からない。**
# → (ticker, date) をキーに初回観測値を台帳へ持ち、次回取得時に突き合わせる。
#
# ★設計上の要点:
#   1) **初回値は絶対に上書きしない。** 改訂は revisions に積む（遡及編集の禁止と同じ扱い）。
#   2) ★**未確定の足は台帳に入れない。** 当日（および将来日）のバーは動いて当たり前で、
#      入れると毎回改訂が出る——**常時点灯する条件は警告にしない**（H-4 で 24/7 銘柄を
#      off_calendar に分けたのと同じ一般則。Boss 2026-09-06）。
#   3) 浮動小数の表現ゆらぎで誤検知しないよう相対許容差を置く。

_VALUE_LEDGER_PATH = Path(__file__).resolve().parents[1] / "data" / "observed_values.json"
_REVISION_RTOL = 1e-6


def _load_value_ledger() -> Dict[str, Any]:
    try:
        return json.loads(_VALUE_LEDGER_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}
    except Exception:
        # ★壊れていても取得は止めない。台帳は安全網であって取得の前提ではない。
        return {}


def _save_value_ledger(ledger: Dict[str, Any]) -> None:
    try:
        _VALUE_LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
        body = json.dumps(ledger, ensure_ascii=False, indent=1, sort_keys=True)
        _VALUE_LEDGER_PATH.write_text(body + chr(10), encoding="utf-8")
    except Exception:
        pass


def record_and_check_values(
    name: str, series: pd.Series, ledger: Dict[str, Any], seen_at: str
) -> List[Dict[str, Any]]:
    """(name, date) ごとの終値を台帳と突き合わせ、変わっていたら改訂として返す。

    ★確定済みの足（当日より前）だけを対象にする。当日の足は動いて当たり前なので、
      入れると毎回改訂が出て **警告が常時点灯し、読まれなくなる**。
    """
    today = date.today()
    revisions: List[Dict[str, Any]] = []
    for ts, val in series.items():
        d = ts.date()
        if d >= today:
            continue                      # ★未確定の足は台帳に入れない
        v = float(val)
        if v != v:                        # NaN は値ではない
            continue
        key = name + "|" + d.isoformat()
        rec = ledger.get(key)
        if rec is None:
            ledger[key] = {"value": v, "first_seen": seen_at}
            continue
        base = float(rec["value"])
        if abs(v - base) <= max(_REVISION_RTOL * abs(base), 1e-9):
            continue
        rev = {
            "seen": seen_at,
            "value": v,
            "delta": round(v - base, 6),
            "delta_pct": round((v / base - 1.0) * 100.0, 4) if base else None,
        }
        rec.setdefault("revisions", []).append(rev)   # ★初回値は上書きしない
        revisions.append({
            "pair": name,
            "date": d.isoformat(),
            "first": base,
            "first_seen": rec.get("first_seen"),
            "now": v,
            "delta": rev["delta"],
            "delta_pct": rev["delta_pct"],
        })
    return revisions


def fetch_trade_data(
    days: int = 30,
) -> Tuple[pd.DataFrame, Dict[str, Dict[str, float]], str]:
    """
    --trade 用: TRADE_PAIRS の30日データを取得し、
    DataFrame・ペアスナップショット・テキストサマリーを返す。
    """
    end_date = date.today()
    start_date = end_date - timedelta(days=days)

    df_all = pd.DataFrame()
    pair_snapshots: Dict[str, Dict[str, float]] = {}
    ledger = _load_value_ledger()
    seen_at = datetime.now().isoformat(timespec="minutes")
    all_revisions: List[Dict[str, Any]] = []
    output_lines = [
        f"取得期間: {start_date} 〜 {end_date} (JST基準)",
        "",
    ]

    for name, ticker in TRADE_PAIRS.items():
        data = fetch_market_data(ticker, start_date, end_date)
        if not data.empty:
            latest = float(data.iloc[-1])
            first = float(data.iloc[0])
            change_30d = (latest - first) / first * 100
            # 週次基準点: 最新営業日から7暦日前【以前】の最後の終値。
            # 位置指定(-6)ではなく日付基準にするのは、祝日で営業日数が週により変わるため。
            prev_1w: Optional[float] = None
            prev_1w_as_of: Optional[str] = None
            try:
                cutoff = data.index[-1] - pd.Timedelta(days=7)
                prior = data.loc[:cutoff]
                if not prior.empty:
                    prev_1w = float(prior.iloc[-1])
                    prev_1w_as_of = str(prior.index[-1].date())
            except Exception:
                prev_1w = None
                prev_1w_as_of = None
            # ★2026-09-06 追加（H-4 / Boss 2026-09-06「実装推奨」）— per-pair の as_of。
            #   2026-08-28 は Yahoo の欠測で金利4本だけが 8/27、US100 は NaN という
            #   【ペアごとに日付が割れた】snapshot になったが、snapshot 側に per-pair の
            #   日付が無かったため、その事実は目視で個別に取りに行くまで見えなかった。
            #   ★実害が出たのは「発見が遅れた」ことであって、値が間違っていたことではない。
            #   日付を値と一緒に持てば、割れたその週に機械の出力だけで気づける。
            as_of = str(data.index[-1].date())
            first_as_of = str(data.index[0].date())
            output_lines.append(
                f"{name}: 最新 {latest:.3f} (30日変化: {change_30d:+.2f}%) [as_of {as_of}]"
            )
            all_revisions.extend(
                record_and_check_values(name, data, ledger, seen_at)
            )
            df_all[name] = data
            pair_snapshots[name] = {
                "latest": latest,
                "first": first,        # 30日前の始値（カーブの30日Δ算出に使用）
                "prev_1w": prev_1w,    # 7暦日前以前の最後の終値（カーブの週次Δ算出に使用）
                "change_30d": change_30d,
                # ★以下3つが H-4。値と測定日を必ず一緒に持ち回る。
                "as_of": as_of,                 # latest の実日付
                "first_as_of": first_as_of,     # 30日Δの基準日
                "prev_1w_as_of": prev_1w_as_of, # ★週次Δの基準日。7暦日前【以前】なので週により動く
            }
        else:
            output_lines.append(f"{name}: データ取得失敗")

    _save_value_ledger(ledger)
    if all_revisions:
        # ★黙って直さない。確定済みの日付の値が変わったこと自体を出力に出す。
        output_lines.append("")
        output_lines.append("★★ 確定済みの値が変わった（台帳との照合）:")
        for r in all_revisions:
            output_lines.append(
                f"  {r['pair']} {r['date']}: {r['first']} -> {r['now']}"
                f" ({r['delta']:+} / {r['delta_pct']:+}%)"
                f"  初回観測 {r['first_seen']}"
            )
        pair_snapshots["_value_revisions"] = all_revisions  # type: ignore[assignment]

    return df_all, pair_snapshots, "\n".join(output_lines)


# ── FRED 取得（★Yahooとは別ソース・別経路・公表ラグあり）────────────────
# 2026-08-20 追加。インフレ補償（ブレークイーブン）の実測。
# Yahoo 側の関数とは意図的に分離している。同じ経路に混ぜると
# 「別フィードであること」がコード上見えなくなり、測定窓の不一致を焼き付ける。

def fetch_fred_series(series_id: str, days: int = 30) -> "pd.Series":
    """FRED の CSV を取得し、直近 days 日分の Series（index=日付, 値=float）を返す。

    ★失敗時は例外を送出する（握り潰さない）。呼び出し側で捕捉し、
      「データ欠損」ではなく「取得失敗」として区別可能な形で出すこと。

    CSV仕様（2026-08-20 実測）:
      - ヘッダは "observation_date,<SERIES_ID>"（"DATE" ではない）
        → 列名に依存せず【位置】で読む
      - 欠損は空フィールドで返る（祝日の行は存在し、値だけが空）
        旧APIの "." 表記も念のため許容する
      - 非営業日を含むため、窓は必ず【日付基準】で取る（位置指定 iloc[-7] は不可）
    """
    url = FRED_CSV_URL.format(series_id=series_id)
    with urllib.request.urlopen(url, timeout=30) as resp:
        raw = resp.read().decode("utf-8-sig")

    reader = csv.reader(io.StringIO(raw))
    header = next(reader, None)
    if not header or len(header) < 2:
        raise ValueError(f"FRED CSV のヘッダが不正: {series_id} -> {header!r}")

    idx: List[pd.Timestamp] = []
    vals: List[float] = []
    for row in reader:
        if len(row) < 2:
            continue
        d_raw, v_raw = row[0].strip(), row[1].strip()
        # 欠損: 空文字 / "." / その他の非数値
        if not v_raw or v_raw == ".":
            continue
        try:
            v = float(v_raw)
        except ValueError:
            continue
        try:
            d = pd.Timestamp(d_raw)
        except Exception:
            continue
        idx.append(d)
        vals.append(v)

    if not idx:
        raise ValueError(f"FRED CSV に有効な観測値が無い: {series_id}")

    ser = pd.Series(vals, index=pd.DatetimeIndex(idx), name=series_id).sort_index()
    cutoff = ser.index[-1] - pd.Timedelta(days=days)
    return ser.loc[ser.index >= cutoff]


def fetch_fred_snapshots(days: int = 30) -> Dict[str, Any]:
    """FRED_SERIES 全系列のスナップショットを返す。

    成功時: {name: {"latest", "as_of", "prev_1w", "prev_30d"}}
    失敗時: {"_error": "<例外クラス名>: <メッセージ>"}
            ★None を返さないのは「データ欠損」と「取得失敗」を区別するため。
              呼び出し側は _error を見て `null  # ERROR: ...` を出力する。

    窓は fetch_trade_data の prev_1w と同方針で【日付基準】。
    非営業日の行が無い／祝日値が空なので、位置指定では窓がずれる。
    """
    out: Dict[str, Any] = {}
    try:
        for name, series_id in FRED_SERIES.items():
            ser = fetch_fred_series(series_id, days=days)
            last_ts = ser.index[-1]

            def _at_or_before(delta_days: int) -> Optional[float]:
                prior = ser.loc[ser.index <= last_ts - pd.Timedelta(days=delta_days)]
                return float(prior.iloc[-1]) if not prior.empty else None

            def _date_at_or_before(delta_days: int) -> Optional[str]:
                """★2026-09-06 追加（Boss「次の一手」）— Δの【基準日そのもの】を返す。

                7暦日ルックバックが実際にどの営業日に落ちるかは、祝日・欠測・公表ラグで動く。
                2026-09-03 基準の DGS2/DGS10 では窓が 8/28 を跨がず 8/27 に落ち、
                **2s10s が -8.0bp フラット化した 8/28 の1日が外れただけで週次Δの符号が反転した**。
                値の隣に日付を置いておけば、符号を読む前に窓を確認できる。
                """
                prior = ser.loc[ser.index <= last_ts - pd.Timedelta(days=delta_days)]
                return prior.index[-1].date().isoformat() if not prior.empty else None

            out[name] = {
                "series_id": series_id,
                "latest": float(ser.iloc[-1]),
                "as_of": last_ts.date().isoformat(),   # ★公表ラグがあるので必ず添える
                "prev_1w": _at_or_before(7),
                "prev_1w_as_of": _date_at_or_before(7),     # ★週次Δの基準日
                "prev_30d": _at_or_before(days),
                "prev_30d_as_of": _date_at_or_before(days), # 30日Δの基準日
            }
    except Exception as e:  # noqa: BLE001 - 分類のためにクラス名を残して伝播させる
        return {"_error": f"{type(e).__name__}: {e}"}
    return out
