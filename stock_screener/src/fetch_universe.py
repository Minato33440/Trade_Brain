"""
Step 2: グロース市場ユニバース確定

条件① 上場10年以内（2016-01-01 以降）
条件③ 時価総額300億円未満（直近終値 × 発行済株数）

使用法:
    python src/fetch_universe.py

出力:
    stock_screener/data/universe_growth_YYYYMMDD.csv
    stock_screener/logs/fetch_universe_YYYYMMDD.log
"""
import sys
import time
import logging
from datetime import datetime
from pathlib import Path

import pandas as pd

# src/ と同階層なので直接 import
sys.path.insert(0, str(Path(__file__).parent))
from jquants_client import JQuantsClient

# ── パス定義 ────────────────────────────────────────────────────────────────
HERE = Path(__file__).parent.parent          # stock_screener/
DATA_DIR = HERE / "data"
LOG_DIR = HERE / "logs"
DATA_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

RUN_DATE = datetime.now().strftime("%Y%m%d")

# ── 定数 ────────────────────────────────────────────────────────────────────
GROWTH_MARKET_CODES = {"0113", "113"}
GROWTH_NAME_KEYWORDS = ["グロース", "growth", "Growth"]
LISTING_DATE_MIN = "2016-01-01"
MARKET_CAP_MAX = 30_000_000_000          # 300億円

# J-Quants マスタで発行済株数に使われる可能性のあるフィールド名
SHARES_FIELDS = [
    "IssuedShares",
    "NumberOfIssuedAndOutstandingShares",
    "issued_shares",
    "number_of_issued_and_outstanding_shares",
]

# 終値フィールド名候補（優先順）
CLOSE_FIELDS = ["C", "AdjC", "Close", "AdjustmentClose", "close", "adjustment_close"]


# ── ロギング設定 ─────────────────────────────────────────────────────────────
def setup_logging() -> logging.Logger:
    log = logging.getLogger("fetch_universe")
    log.setLevel(logging.DEBUG)
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%H:%M:%S")

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)

    log_file = LOG_DIR / f"fetch_universe_{RUN_DATE}.log"
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)

    log.addHandler(ch)
    log.addHandler(fh)
    return log


# ── ヘルパー ─────────────────────────────────────────────────────────────────
def _find_col(df: pd.DataFrame, *candidates: str) -> str | None:
    """candidates を順に試して最初に存在するカラム名を返す。"""
    for c in candidates:
        if c in df.columns:
            return c
    return None


def _is_growth(row: pd.Series) -> bool:
    code = str(row.get("MarketCode", "")).strip().lstrip("0")
    if code == "113":
        return True
    name = str(row.get("MarketCodeName", ""))
    return any(kw in name for kw in GROWTH_NAME_KEYWORDS)


def _extract_shares_from_master(row: pd.Series) -> float | None:
    """マスタ行から発行済株数を取り出す。"""
    for field in SHARES_FIELDS:
        val = row.get(field)
        if val is not None and str(val).strip() not in ("", "nan", "None"):
            try:
                return float(val)
            except (ValueError, TypeError):
                pass
    return None


def _extract_shares_from_fins(fins: list[dict]) -> float | None:
    """fins/summary リストから最新期の発行済株数を取り出す。"""
    for rec in sorted(fins, key=lambda r: str(r.get("FiscalYear", "")), reverse=True):
        for field in SHARES_FIELDS:
            val = rec.get(field)
            if val is not None and str(val).strip() not in ("", "nan", "None"):
                try:
                    return float(val)
                except (ValueError, TypeError):
                    pass
    return None


def _jq_to_yf_code(jq_code: str) -> str:
    """J-Quants 5桁コード → Yahoo Finance コード (例: 43850 → 4385.T)。"""
    return jq_code[:-1] + ".T"


def _get_shares_yfinance(codes: list[str], log: logging.Logger) -> dict[str, float | None]:
    """yfinance で発行済株数を一括取得（fins/summary 代替）。"""
    import yfinance as yf
    result: dict[str, float | None] = {}
    for i, code in enumerate(codes, 1):
        if i % 50 == 0:
            log.info("  yfinance 取得中: %d / %d", i, len(codes))
        yf_code = _jq_to_yf_code(code)
        try:
            fi = yf.Ticker(yf_code).fast_info
            shares = getattr(fi, "shares", None)
            result[code] = float(shares) if shares else None
        except Exception:
            result[code] = None
        time.sleep(0.3)
    found = sum(1 for v in result.values() if v is not None)
    log.info("  yfinance 完了: %d / %d 件取得", found, len(codes))
    return result


# ── メイン処理 ───────────────────────────────────────────────────────────────
def main() -> None:
    t0 = time.time()
    log = setup_logging()
    log.info("=== Step 2: グロース市場ユニバース確定 開始 ===")

    client = JQuantsClient()

    # ── STEP 1: 全上場銘柄取得 ────────────────────────────────────────────────
    log.info("全上場銘柄リストを取得中 (/equities/master)...")
    master_records = client.get_listed_master()
    if not master_records:
        log.error("銘柄マスタが空です。APIキーとエンドポイントを確認してください")
        sys.exit(1)

    master_df = pd.DataFrame(master_records)
    log.info("[INFO] 全上場銘柄: %d 銘柄", len(master_df))
    log.debug("マスタカラム: %s", list(master_df.columns))

    # ── STEP 2: グロース市場フィルタ ─────────────────────────────────────────
    # V2 API は短縮フィールド名を返す: MarketCode → Mkt, MarketCodeName → MktNm
    market_col = _find_col(master_df, "Mkt", "MarketCode", "market_code", "marketcode")
    if market_col is None:
        log.error(
            "MarketCode フィールドが見つかりません。利用可能カラム: %s",
            list(master_df.columns),
        )
        sys.exit(1)

    # MarketCode が "0113" or "113"、または MarketCodeName にグロースを含む
    growth_mask = master_df[market_col].astype(str).str.strip().isin(GROWTH_MARKET_CODES)
    name_col_mkt = _find_col(master_df, "MktNm", "MarketCodeName", "market_code_name")
    if name_col_mkt and not growth_mask.any():
        # コードで引っかからない場合は名称でフォールバック
        growth_mask = master_df[name_col_mkt].astype(str).apply(
            lambda n: any(kw in n for kw in GROWTH_NAME_KEYWORDS)
        )
        if growth_mask.any():
            log.debug("グロース市場を %s フィールドでフォールバック検出", name_col_mkt)

    if not growth_mask.any() and name_col_mkt:
        log.error(
            "グロース市場の銘柄が0件です。%s のサンプル値: %s",
            market_col,
            master_df[market_col].unique()[:10].tolist(),
        )
        sys.exit(1)

    growth_df = master_df[growth_mask].copy()
    log.info("[INFO] グロース市場: %d 銘柄", len(growth_df))

    # ── STEP 3: 条件① 上場日フィルタ（2016年以降） ────────────────────────────
    # 【Free プラン制約】/equities/master の Date フィールドは全銘柄共通の
    # effective date であり上場日ではない。履歴マスタ取得も非対応。
    # → 条件① は自動適用不可。グロース市場全銘柄をそのまま cond1_df とし、
    #   CSV の listing_date カラムは空欄で出力する。
    # → Light プラン以上 or 外部データソース（EDINET 等）でフォローアップ推奨。
    log.warning(
        "【条件①スキップ】J-Quants V2 Free プランでは上場日が取得できません。"
        "グロース市場 %d 銘柄をすべて条件①通過とみなして続行します。"
        "（Light プラン以上または EDINET データで事後フィルタ推奨）",
        len(growth_df),
    )
    cond1_df = growth_df.copy()
    date_col = None  # 上場日データなし
    log.info("[INFO] 条件①通過（上場2016年以降）: %d 銘柄 ※Free プラン制約によりスキップ", len(cond1_df))

    # ── STEP 4: 直近終値取得 ──────────────────────────────────────────────────
    price_date = client.latest_available_date()
    log.info(
        "終値取得日: %s（Freeプラン %d 週遅延）",
        price_date,
        12,
    )
    log.info("日次株価を一括取得中 (/equities/bars/daily?date=%s)...", price_date)

    quotes = client.get_daily_quotes_by_date(price_date)
    if not quotes:
        log.error(
            "株価データが取得できませんでした（date=%s）。"
            "営業日・Free プランの利用可能日付範囲を確認してください",
            price_date,
        )
        sys.exit(1)

    quotes_df = pd.DataFrame(quotes)
    log.debug("株価カラム: %s", list(quotes_df.columns))

    close_col = _find_col(quotes_df, *CLOSE_FIELDS)
    if close_col is None:
        log.error(
            "終値フィールドが見つかりません。利用可能カラム: %s", list(quotes_df.columns)
        )
        sys.exit(1)

    q_code_col = _find_col(quotes_df, "Code", "code") or "Code"
    q_date_col = _find_col(quotes_df, "Date", "date") or "Date"

    quotes_clean = (
        quotes_df[[q_code_col, q_date_col, close_col]]
        .rename(columns={q_code_col: "_code", q_date_col: "close_date", close_col: "close_price"})
        .copy()
    )
    quotes_clean["close_price"] = pd.to_numeric(quotes_clean["close_price"], errors="coerce")

    # ── STEP 5: マスタと株価を結合 ───────────────────────────────────────────
    m_code_col = _find_col(cond1_df, "Code", "code") or "Code"
    merged = cond1_df.merge(quotes_clean, left_on=m_code_col, right_on="_code", how="left")
    merged = merged.drop(columns=["_code"], errors="ignore")

    # ── STEP 6: 発行済株数取得（優先順位: マスタ → fins/summary → yfinance） ──
    shares_col_in_master = next(
        (c for c in merged.columns if c in SHARES_FIELDS), None
    )

    if shares_col_in_master and pd.to_numeric(merged[shares_col_in_master], errors="coerce").notna().any():
        log.info("発行済株数: マスタデータから取得（フィールド: %s）", shares_col_in_master)
        merged["shares_outstanding"] = pd.to_numeric(
            merged[shares_col_in_master], errors="coerce"
        )
    else:
        codes = merged[m_code_col].tolist()
        shares_map: dict[str, float | None] = {}

        # ── (a) fins/summary を試みる ──────────────────────────────────────
        log.info(
            "マスタに発行済株数なし → /fins/summary を試みます（%d 銘柄）",
            len(codes),
        )
        fins_fail_count = 0
        for i, code in enumerate(codes, 1):
            if fins_fail_count >= 3:
                log.warning(
                    "fins/summary が連続 3 件失敗 → yfinance にフォールバック"
                )
                break
            if i % 50 == 0:
                log.info("  fins/summary: %d / %d", i, len(codes))
            try:
                fins = client.get_fins_summary(str(code))
                val = _extract_shares_from_fins(fins)
                shares_map[str(code)] = val
                fins_fail_count = 0  # 成功したらリセット
            except Exception as exc:
                log.debug("  fins/summary 失敗 (code=%s): %s", code, exc)
                shares_map[str(code)] = None
                fins_fail_count += 1

        fins_ok = sum(1 for v in shares_map.values() if v is not None)

        # ── (b) fins/summary で取れなかった銘柄を yfinance で補完 ──────────
        missing_codes = [c for c in codes if shares_map.get(str(c)) is None]
        if missing_codes:
            log.info(
                "yfinance で補完取得（%d 銘柄 × 0.3秒 ≈ %d 秒）...",
                len(missing_codes),
                int(len(missing_codes) * 0.3) + 1,
            )
            yf_map = _get_shares_yfinance([str(c) for c in missing_codes], log)
            shares_map.update(yf_map)

        total_ok = sum(1 for v in shares_map.values() if v is not None)
        log.info(
            "発行済株数取得完了: %d / %d 件（fins/summary=%d, yfinance補完=%d）",
            total_ok, len(codes), fins_ok, total_ok - fins_ok,
        )
        merged["shares_outstanding"] = merged[m_code_col].astype(str).map(shares_map)

    # ── STEP 7: 時価総額計算 + 条件③フィルタ ────────────────────────────────
    no_shares = merged["shares_outstanding"].isna()
    no_price = merged["close_price"].isna()

    skipped_shares = no_shares & ~no_price
    skipped_price = no_price

    if skipped_shares.any():
        log.warning("発行済株数が取得できない銘柄を除外: %d 銘柄", skipped_shares.sum())
        for code in merged.loc[skipped_shares, m_code_col].tolist()[:20]:
            log.debug("  除外（発行済株数なし）: %s", code)

    if skipped_price.any():
        log.warning("終値が取得できない銘柄を除外: %d 銘柄", skipped_price.sum())

    valid = merged[~no_shares & ~no_price].copy()
    valid["shares_outstanding"] = pd.to_numeric(valid["shares_outstanding"], errors="coerce")
    valid["market_cap_jpy"] = valid["close_price"] * valid["shares_outstanding"]

    universe = valid[valid["market_cap_jpy"] < MARKET_CAP_MAX].copy()
    log.info("[INFO] 条件③通過（時価総額300億未満）: %d 銘柄  ← 最終ユニバース", len(universe))

    if universe.empty:
        log.warning("最終ユニバースが0件です。条件・データを確認してください")
        sys.exit(0)

    # ── STEP 8: CSV 保存 ──────────────────────────────────────────────────────
    name_col = _find_col(
        universe,
        "CoName", "CompanyName", "company_name", "Name", "name",
        "CoNameEn", "CompanyNameEnglish", "company_name_english",
    )

    out = pd.DataFrame(
        {
            "code": universe[m_code_col].values,
            "name": universe[name_col].values if name_col else [""] * len(universe),
            "market": universe[market_col].values if market_col in universe.columns else [""] * len(universe),
            "listing_date": (
                pd.to_datetime(universe[date_col], errors="coerce").dt.strftime("%Y-%m-%d")
                if date_col and date_col in universe.columns
                else [""] * len(universe)
            ),
            "close_price": universe["close_price"].values,
            "close_date": universe["close_date"].values,
            "shares_outstanding": universe["shares_outstanding"].astype("int64").values,
            "market_cap_jpy": universe["market_cap_jpy"].astype("int64").values,
        }
    )
    out = out.sort_values("market_cap_jpy").reset_index(drop=True)

    out_path = DATA_DIR / f"universe_growth_{RUN_DATE}.csv"
    out.to_csv(out_path, index=False, encoding="utf-8-sig")
    log.info("CSV 保存: %s", out_path)

    # ── 完了サマリ ────────────────────────────────────────────────────────────
    elapsed = time.time() - t0
    log.info("[INFO] 処理時間: %.1f 秒", elapsed)
    log.info("=== 完了 ===")

    if len(universe) > 300:
        log.warning(
            "最終ユニバース %d 銘柄は想定（数十〜百数十）を大幅に超えています。"
            "フィルタ条件・MarketCode 値を確認してください",
            len(universe),
        )
    elif len(universe) < 10:
        log.warning(
            "最終ユニバース %d 銘柄は想定より少ないです。"
            "price_date=%s が営業日か、データ取得に問題がないか確認してください",
            len(universe),
            price_date,
        )


if __name__ == "__main__":
    main()
