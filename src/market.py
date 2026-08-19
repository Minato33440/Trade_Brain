"""市場データ取得・スナップショット生成モジュール。

yfinance によるリアルタイム/ヒストリカルデータ取得、
フォーマット出力を担当する。
"""
from __future__ import annotations

import csv
import io
import urllib.request
from datetime import date, datetime, timedelta
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
            try:
                cutoff = data.index[-1] - pd.Timedelta(days=7)
                prior = data.loc[:cutoff]
                if not prior.empty:
                    prev_1w = float(prior.iloc[-1])
            except Exception:
                prev_1w = None
            output_lines.append(
                f"{name}: 最新 {latest:.3f} (30日変化: {change_30d:+.2f}%)"
            )
            df_all[name] = data
            pair_snapshots[name] = {
                "latest": latest,
                "first": first,        # 30日前の始値（カーブの30日Δ算出に使用）
                "prev_1w": prev_1w,    # 7暦日前以前の最後の終値（カーブの週次Δ算出に使用）
                "change_30d": change_30d,
            }
        else:
            output_lines.append(f"{name}: データ取得失敗")

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

            out[name] = {
                "series_id": series_id,
                "latest": float(ser.iloc[-1]),
                "as_of": last_ts.date().isoformat(),   # ★公表ラグがあるので必ず添える
                "prev_1w": _at_or_before(7),
                "prev_30d": _at_or_before(days),
            }
    except Exception as e:  # noqa: BLE001 - 分類のためにクラス名を残して伝播させる
        return {"_error": f"{type(e).__name__}: {e}"}
    return out
