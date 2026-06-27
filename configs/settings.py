"""REX_Trade_System 共通設定（ティッカー定義・定数・パス）。

全モジュールはここから定数を import する。
ティッカーの追加・変更はこのファイルだけで完結させる。
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple

# ── プロジェクトルート ────────────────────────────────
ROOT_DIR: Path = Path(__file__).resolve().parents[1]

# ── ティッカー定義 ────────────────────────────────────
# 対話モード（get_market_snapshot）用
CORE_TICKERS: Dict[str, str] = {
    "USD/JPY": "USDJPY=X",
    "EUR/USD": "EURUSD=X",
    "XAU/USD (金)": "GC=F",
    "BTC/USD": "BTC-USD",
    "VIX": "^VIX",
    "US10Y": "^TNX",
    "US2Y": "^FVX",   # 実体は5年債。2年債の直接取得は困難なため代用
    "JP10Y": "^TNX",   # 日本10年債は直接取得困難。US10Yで代用（暫定）
}

FULL_TICKERS: Dict[str, str] = {
    **CORE_TICKERS,
    "GBP/JPY": "GBPJPY=X",
    "AUD/JPY": "AUDJPY=X",
    "US100 (ナスダック)": "^NDX",
    "SP500": "^GSPC",
    "JP225 (日経)": "^N225",
    "Copper (銅)": "HG=F",
    "WTI": "CL=F",
    "JP2Y": "^FVX",   # 仮置き
}

# --trade 用 ペア（レジーム判定の入力）
# 2026-06-27: JP225（^N225）を実測パネルに追加（boss市況の主役が機械snapshotに無いねじれを解消）。
TRADE_PAIRS: Dict[str, str] = {
    "USD/JPY": "USDJPY=X",
    "US100": "^NDX",
    "JP225": "^N225",
    "XAU/USD": "GC=F",
    "WTI": "CL=F",
    "US2Y": "^FVX",   # 実体は5年債（^FVX）。2年債の直接取得は困難なため代用。2s10s算出も実質5s10s
    "VIX": "^VIX",
    "US10Y": "^TNX",
    "BTC/USD": "BTC-USD",
}

# ── ドル円 為替介入 監視設定（単独/協調 判定フラグの機械側ナレッジ） ───────────
# 2026-06-27: IMF残弾＋会談実績を機械側に持たせ、深夜フラッシュの構えを自動化（boss構造論）。
# 値はboss提供の構造論に基づく。介入実施・会談・残弾は手動で更新する（市場データからは自動検知不可）。
INTERVENTION_WATCH: Dict[str, object] = {
    "pair": "USD/JPY",
    "watch_zone": 161.5,      # この水準以上で介入警戒ゾーン（boss: 161台半ば到達済み）
    "upper_alert": 162.2,     # この水準以上で上値アラート（boss: 162.20-162.50戻り売りメド）
    "down_target": 155.0,     # 協調弾発動時の深い円高ターゲット
    "imf_ammo_remaining": 1,  # IMF枠の協調介入 残弾（5/6が2回目の実弾、11月まであと1回）
    "last_meeting": "2026-06-23 片山-ベッセント会談（協調レートチェックの布石）",
    "coordinated_history": "2026-01 協調rate check=10営業日で2,100pips急落",
    "asymmetry": "最後の協調弾が出たら155方向へ深く長い／出る前は161-162で踏まれる",
    "judgment_note": "単独/協調はNY連銀rate check確認で判定（毎朝チェック）。介入は経験則上24:30以降に入ったことがなく円安は深夜帯",
    # 協調介入の進行段階（手動更新）: 予兆→秒読み→着弾の4段梯子。
    # 価格から自動検知できないため、会談・rate check・実弾が確認された週にここを上げる。
    "coord_ladder": ["unconfirmed", "meeting_held", "rate_check_detected", "executed"],
    "coord_stage": "meeting_held",   # 現在地（6/23 片山-ベッセント会談済＝予兆フェーズ）
    "coord_stage_note": "予兆(meeting_held)→秒読み(rate_check_detected=NY連銀rate check確認)→着弾(executed=実弾)。rate_check_detectedで戦略軸が『162待ち伏せ売り』→『155-156底打ち確認』へ切替",
}

# ── GMニュースフィルタ用キーワード ────────────────────
GM_TITLE_KEYWORDS: Tuple[str, ...] = (
    "株",
    "株式",
    "市場",
    "金融",
    "為替",
    "円安",
    "円高",
    "円相場",
    "ドル安",
    "ドル高",
    "ドル円",
    "金利",
    "利上げ",
    "利下げ",
    "米国",
    "日本",
    "中東",
    "イラン",
    "ホルムズ海峡",
    "ウクライナ",
    "ロシア",
    "FRB",
    "日銀",
    "ECB",
    "原油",
    "金価格",
    "地政",
    "BRICS",
    "CBDC",
    "債券",
    "インフレ",
    "景気",
    "GDP",
    "欧州",
    "中国",
    "相場",
    "下落",
    "高騰",
    "利回り",
    "テロ",
    "戦争",
    "制裁",
    "株価",
)

# ── ログ出力先（ROOT_DIR 基準で統一） ─────────────────
LOGS_DIR: Path = ROOT_DIR / "logs"
PNG_DATA_DIR: Path = ROOT_DIR / "png_data"
TEXT_LOG_DIR: Path = LOGS_DIR / "text_log"

# ── parquet データ保存先（data_fetch.fetch_multi_tf が使用） ───
RAW_DATA_DIR: Path = ROOT_DIR / "data" / "raw"
