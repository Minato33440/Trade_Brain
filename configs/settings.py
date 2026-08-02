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
    "US3M": "^IRX",   # 13週Tビル＝政策金利の近接（front）。3m10s（Fed重視の景気後退カーブ）算出用（2026-06-27追加）
    "US2Y": "^FVX",   # 実体は5年債（^FVX）。2年債の直接取得は困難なため代用。belly。5s10s/3m5s算出に使用
    "VIX": "^VIX",
    "US10Y": "^TNX",
    "BTC/USD": "BTC-USD",
}

# ── ドル円 為替介入 監視設定（単独/協調 判定フラグの機械側ナレッジ） ───────────
# 2026-06-27: IMF残弾＋会談実績を機械側に持たせ、深夜フラッシュの構えを自動化（boss構造論）。
# 2026-08-01: 7/30 協調介入の実施を反映。coord_stage=executed / IMF残弾=0 へ更新。
# 値はboss提供の構造論に基づく。介入実施・会談・残弾は手動で更新する（市場データからは自動検知不可）。
INTERVENTION_WATCH: Dict[str, object] = {
    "pair": "USD/JPY",
    "watch_zone": 161.0,      # 介入後の0.5戻し。ここまでの戻りは戻り売りゾーン（週足終値157.469起点）
    "upper_alert": 162.674,   # 週足レジスタンス。明確に上抜けると介入警戒の剥落＝163.996再試へ
    "down_target": 153.9,     # 157.157（介入後の安値帯）を終値で割った場合の次の下値
    "imf_ammo_remaining": 0,  # 4/30-5/1=1回目、5/6=2回目、7/30=3回目。IMF枠3エピソードを消化
    "imf_window_note": "エピソード3は7/30(木)起点で3営業日=7/31(金)・8/3(月)まで同一回。8/4(火)以降の新規介入は4回目=free-floating分類を逸脱。1回目が6ヶ月ルックバックから外れるのは10月末",
    "last_meeting": "2026-07-30/31 協調介入実施（三村財務官『米国から心理的支援を超える支援』／ベッセント財務長官『円は非常に過小評価』）",
    "coordinated_history": "2026-01 協調rate check=10営業日で2,100pips急落 / 2026-07-30 協調介入=163→158（-3.3%、ドルは2023年1月以来最大の日次下落）",
    "us_participation": "2026-07-31 米財務省が複数行に『介入の可能性、今後の行動に備えよ』と通告（ロイター）。日経・Bloombergが米側のrate check実施を報道。IMF3エピソード枠が縛るのは日本の分類であって米財務省の行動ではない",
    "asymmetry": "日本の残弾は0だが米国の関与により『枠切れ＝無防備』とは限らない。8/4以降のドル円上昇を狙う場合、日付でなく『当局が撃たないことを価格が証明した後』（161回復して叩かれない）を待つ",
    "judgment_note": "単独/協調はNY連銀rate check確認で判定（毎朝チェック）。介入は経験則上24:30以降に入ったことがなく円安は深夜帯。財務省の介入実績公表は8月末",
    # 協調介入の進行段階（手動更新）: 予兆→秒読み→着弾の4段梯子。
    # 価格から自動検知できないため、会談・rate check・実弾が確認された週にここを上げる。
    "coord_ladder": ["unconfirmed", "meeting_held", "rate_check_detected", "executed"],
    "coord_stage": "executed",   # 現在地（7/30 協調実弾。日本の実弾と米側rate checkが同時到達）
    "coord_stage_note": "予兆(meeting_held)→秒読み(rate_check_detected)→着弾(executed)。2026-07-30にmeeting_held→executedへ2段跳躍。次の焦点は『撃てない期間に市場がどこまで戻すか』",
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
