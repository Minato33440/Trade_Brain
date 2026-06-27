"""レジーム判定ロジック。

8ペア30日データからマクロ・レジームを簡易判定し、
ラベル・サマリー・YAMLスナップショットを生成する。
"""
from __future__ import annotations

from datetime import date
from typing import Dict, List, Optional, Tuple

try:
    from configs.settings import INTERVENTION_WATCH
except Exception:  # pragma: no cover - フォールバック（設定欠落でも回帰しない）
    INTERVENTION_WATCH = {}


def build_regime_snapshot(
    start_date: date,
    end_date: date,
    snapshots: Dict[str, Dict[str, float]],
) -> Tuple[str, str, str]:
    """
    8ペア30日データからレジームを簡易判定し、概要テキストとYAMLスナップショットを返す。

    Returns:
        (label, summary_text, yaml_text)
    """

    def _get_pair(name: str) -> Tuple[Optional[float], Optional[float]]:
        info = snapshots.get(name) or {}
        return info.get("latest"), info.get("change_30d")

    def _get_first(name: str) -> Optional[float]:
        info = snapshots.get(name) or {}
        return info.get("first")

    latest_us100, ch_us100 = _get_pair("US100")
    latest_jp225, ch_jp225 = _get_pair("JP225")
    latest_btc, ch_btc = _get_pair("BTC/USD")
    latest_wti, ch_wti = _get_pair("WTI")
    latest_vix, ch_vix = _get_pair("VIX")
    latest_xau, ch_xau = _get_pair("XAU/USD")
    latest_us2y, ch_us2y = _get_pair("US2Y")
    latest_us10y, ch_us10y = _get_pair("US10Y")
    latest_usdjpy, ch_usdjpy = _get_pair("USD/JPY")

    def _equities_regime() -> str:
        if ch_us100 is None:
            return "unknown"
        if ch_us100 <= -1.5:
            return "down"
        if ch_us100 >= 1.5:
            return "up"
        return "flat"

    def _vol_regime() -> str:
        if ch_vix is None or latest_vix is None:
            return "unknown"
        if latest_vix >= 25 and ch_vix >= 20:
            return "spike"
        if latest_vix <= 15 and ch_vix <= -10:
            return "calm"
        return "normal"

    def _oil_regime() -> str:
        if ch_wti is None:
            return "unknown"
        if ch_wti >= 20:
            return "surge"
        if ch_wti <= -20:
            return "slump"
        return "range"

    def _gold_regime() -> str:
        if ch_xau is None:
            return "unknown"
        if ch_xau >= 2:
            return "bid"
        if ch_xau <= -2:
            return "off"
        return "range"

    def _crypto_regime() -> str:
        if ch_btc is None:
            return "unknown"
        if ch_btc <= -5:
            return "weak"
        if ch_btc >= 5:
            return "strong"
        return "range"

    def _yields_regime() -> str:
        changes = [c for c in (ch_us2y, ch_us10y) if c is not None]
        if not changes:
            return "unknown"
        avg = sum(changes) / len(changes)
        if avg <= -0.5:
            return "falling"
        if avg >= 0.5:
            return "rising"
        return "flat"

    def _curve_2s10s() -> Optional[Dict[str, object]]:
        """2s10s スプレッドとフラット化/スティープ化の形状を判定。

        注: US2Y は ^FVX（5年債）proxy のため、実質は 5s10s。
        snapshot regime の yields ラベル（2Y/10Y平均の符号で rising/falling に丸める）が
        ベアフラットニング（短期↑/長期↓）を見落とすのを補正する指標。
        """
        if latest_us2y is None or latest_us10y is None:
            return None
        spread_now_bp = (latest_us10y - latest_us2y) * 100.0
        first_us2y = _get_first("US2Y")
        first_us10y = _get_first("US10Y")
        delta_bp: Optional[float] = None
        if first_us2y not in (None, 0) and first_us10y not in (None, 0):
            spread_prev_bp = (first_us10y - first_us2y) * 100.0
            delta_bp = spread_now_bp - spread_prev_bp

        short_up = (ch_us2y is not None and ch_us2y > 0)
        if delta_bp is None:
            shape = "unknown"
        elif delta_bp <= -2.0:
            shape = "bear_flattening" if short_up else "bull_flattening"
        elif delta_bp >= 2.0:
            shape = "bull_steepening" if not short_up else "bear_steepening"
        else:
            shape = "stable"
        return {
            "spread_bp": round(spread_now_bp, 1),
            "change_bp": (round(delta_bp, 1) if delta_bp is not None else None),
            "shape": shape,
            "inverted": spread_now_bp < 0,
        }

    def _intervention_flag() -> Optional[Dict[str, object]]:
        """ドル円水準と設定（IMF残弾・会談実績）から介入監視フラグを生成。

        単独/協調の別は価格から自動検知できないため coordinated=unconfirmed の足場のみ。
        NY連銀 rate check の確認で手動確定する運用（settings.INTERVENTION_WATCH を更新）。
        """
        cfg = INTERVENTION_WATCH or {}
        if latest_usdjpy is None or not cfg:
            return None
        watch_zone = float(cfg.get("watch_zone", 161.5))
        upper_alert = float(cfg.get("upper_alert", 162.2))
        zone = "watch" if latest_usdjpy >= watch_zone else "calm"
        ladder = cfg.get("coord_ladder") or [
            "unconfirmed", "meeting_held", "rate_check_detected", "executed",
        ]
        stage = cfg.get("coord_stage", "unconfirmed")
        stage_idx = ladder.index(stage) if stage in ladder else 0
        return {
            "level": round(latest_usdjpy, 3),
            "zone": zone,
            "upper_alert": latest_usdjpy >= upper_alert,
            "imf_ammo_remaining": cfg.get("imf_ammo_remaining"),
            "last_meeting": cfg.get("last_meeting"),
            "coord_stage": stage,                       # 4段梯子の現在地（手動更新）
            "coord_stage_idx": stage_idx,               # 0=unconfirmed .. 3=executed
            "coord_ladder": ladder,
            "coord_stage_note": cfg.get("coord_stage_note"),
            "down_target": cfg.get("down_target"),
            "asymmetry": cfg.get("asymmetry"),
            "history": cfg.get("coordinated_history"),
            "judgment_note": cfg.get("judgment_note"),
        }

    def _relative_strength() -> Optional[Dict[str, object]]:
        """JP225 vs US100 の相対強度を共通通貨（USD換算）で分解。

        円建てJP225の上昇が「構造（割安リレーティング）」か「通貨（円安の嵩上げ）」かを分離。
        為替・日米金利のボラが高い環境では相対は共通通貨で読むべき、という運用要請に対応。
        """
        if (
            latest_jp225 is None or ch_jp225 is None
            or latest_usdjpy is None or ch_us100 is None
        ):
            return None
        first_jp225 = _get_first("JP225")
        first_usdjpy = _get_first("USD/JPY")
        jp_usd_30d: Optional[float] = None
        if first_jp225 not in (None, 0) and first_usdjpy not in (None, 0):
            jp_usd_now = latest_jp225 / latest_usdjpy
            jp_usd_first = first_jp225 / first_usdjpy
            if jp_usd_first:
                jp_usd_30d = (jp_usd_now / jp_usd_first - 1.0) * 100.0
        if jp_usd_30d is None:
            return None
        currency_effect = ch_jp225 - jp_usd_30d
        nominal_spread = ch_jp225 - ch_us100
        fx_adj_spread = jp_usd_30d - ch_us100
        # verdict: FX調整後もアウトパフォームがどれだけ残るか
        if abs(nominal_spread) < 1e-6:
            verdict = "neutral"
        else:
            retention = fx_adj_spread / nominal_spread
            if nominal_spread > 0 and retention >= 0.7:
                verdict = "structure_led"
            elif nominal_spread > 0 and retention <= 0.3:
                verdict = "currency_led"
            else:
                verdict = "mixed"
        return {
            "jp225_jpy_30d": round(ch_jp225, 2),
            "jp225_usd_30d": round(jp_usd_30d, 2),
            "currency_effect_pt": round(currency_effect, 2),
            "us100_30d": round(ch_us100, 2),
            "jp_vs_us_nominal_pt": round(nominal_spread, 2),
            "jp_vs_us_fx_adj_pt": round(fx_adj_spread, 2),
            "verdict": verdict,
        }

    equities = _equities_regime()
    vol = _vol_regime()
    oil = _oil_regime()
    gold = _gold_regime()
    crypto = _crypto_regime()
    yields_regime = _yields_regime()
    curve = _curve_2s10s()
    intervention = _intervention_flag()
    relative = _relative_strength()

    if vol == "spike" and oil == "surge":
        label = "Geopolitical Risk-Off + Energy Shock"
    else:
        parts: List[str] = []
        if equities == "down":
            parts.append("Equities Down")
        if vol == "spike":
            parts.append("Volatility Spike")
        if oil == "surge":
            parts.append("Oil Surge")
        if gold == "bid":
            parts.append("Gold Bid")
        if not parts:
            label = "Neutral"
        else:
            label = " / ".join(parts)

    summary = (
        f"label={label}, equities={equities}, volatility={vol}, "
        f"oil={oil}, gold={gold}, crypto={crypto}, yields={yields_regime}"
    )
    if curve is not None:
        _chg = curve["change_bp"]
        _chg_str = (f"Δ{_chg:+.1f}bp" if _chg is not None else "Δn/a")
        summary += f", curve={curve['shape']}(2s10s={curve['spread_bp']:+.1f}bp,{_chg_str})"
    if intervention is not None:
        summary += (
            f", intervention={intervention['zone']}"
            f"(imf_ammo={intervention['imf_ammo_remaining']},stage={intervention['coord_stage']})"
        )
    if relative is not None:
        summary += (
            f", jp_rs={relative['verdict']}"
            f"(fx_adj{relative['jp_vs_us_fx_adj_pt']:+.1f}pt)"
        )

    # YAMLスナップショット文字列を構築
    order = [
        "USD/JPY", "US100", "JP225", "XAU/USD", "WTI",
        "US2Y", "VIX", "US10Y", "BTC/USD",
    ]
    panel = {
        "risk": ["US100", "JP225", "BTC/USD"],
        "fear": ["VIX"],
        "inflation": ["WTI", "XAU/USD"],
        "rates": ["US2Y", "US10Y"],
        "liquidity": [],
        "credit": [],
    }

    lines: List[str] = []
    lines.append(f"# {end_date:%Y_%m_%d}_snapshot.yaml")
    lines.append("")
    lines.append("date:")
    lines.append(f"  start: {start_date.isoformat()}")
    lines.append(f"  end: {end_date.isoformat()}")
    lines.append("")
    lines.append("panel:")
    for key, names in panel.items():
        if names:
            joined = ", ".join(names)
            lines.append(f"  {key.capitalize()}: [{joined}]")
    lines.append("")
    lines.append("regime:")
    lines.append(f'  label: "{label}"')
    lines.append(f"  equities: {equities}")
    lines.append(f"  volatility: {vol}")
    lines.append(f"  oil: {oil}")
    lines.append(f"  gold: {gold}")
    lines.append(f"  crypto: {crypto}")
    lines.append(f"  yields: {yields_regime}")
    lines.append("")

    # ── 金利カーブ（2s10s）: yields ラベルの丸めを補正する形状指標 ──
    if curve is not None:
        lines.append("curve_2s10s:")
        lines.append(f"  spread_bp: {curve['spread_bp']}")
        if curve["change_bp"] is not None:
            lines.append(f"  change_bp: {curve['change_bp']}")
        lines.append(f"  shape: {curve['shape']}")
        lines.append(f"  inverted: {str(curve['inverted']).lower()}")
        lines.append(
            '  note: "US2Y=^FVX(5y proxy)のため実質5s10s。5年はカーブ中腹で政策金利直結度が2年より低く、'
            '真の2s10sはこれより寝ている可能性大＝bear_flatteningが出たら警戒方向に一段割り引いて読む（逆イールド寸前の恐れ）。'
            'bear_flattening=短期↑/長期↓＝利上げ→景気悪化の織り込み。yields ラベルの補正指標。'
            '将来 ^IRX(3M) で 3m10s（Fed重視の景気後退カーブ）に差し替え/併記候補"'
        )
        lines.append("")

    # ── ドル円 介入監視（単独/協調 判定フラグ） ──
    if intervention is not None:
        def _yv(v: object) -> str:
            if v is None:
                return "null"
            if isinstance(v, bool):
                return str(v).lower()
            if isinstance(v, (int, float)):
                return str(v)
            return f'"{v}"'
        lines.append("intervention_watch:")
        lines.append("  pair: USD/JPY")
        lines.append(f"  level: {intervention['level']}")
        lines.append(f"  zone: {intervention['zone']}            # >=watch_zone(161.5) で watch")
        lines.append(f"  upper_alert: {str(intervention['upper_alert']).lower()}")
        lines.append(f"  imf_ammo_remaining: {_yv(intervention['imf_ammo_remaining'])}")
        lines.append(f"  last_meeting: {_yv(intervention['last_meeting'])}")
        _ladder = intervention.get("coord_ladder") or []
        lines.append(f"  coord_stage: {intervention['coord_stage']}   # 予兆→秒読み→着弾の4段（手動更新）")
        lines.append(f"  coord_stage_idx: {intervention['coord_stage_idx']}            # 0=unconfirmed..3=executed")
        lines.append(f"  coord_ladder: [{', '.join(str(s) for s in _ladder)}]")
        lines.append(f"  coord_stage_note: {_yv(intervention['coord_stage_note'])}")
        lines.append(f"  down_target: {_yv(intervention['down_target'])}")
        lines.append(f"  asymmetry: {_yv(intervention['asymmetry'])}")
        lines.append(f"  history: {_yv(intervention['history'])}")
        lines.append(f"  judgment_note: {_yv(intervention['judgment_note'])}")
        lines.append("")

    # ── 相対強度（JP225 vs US100 を共通通貨で分解：構造 vs 通貨）──
    if relative is not None:
        lines.append("relative_strength:")
        lines.append(f"  jp225_jpy_30d: {relative['jp225_jpy_30d']}")
        lines.append(f"  jp225_usd_30d: {relative['jp225_usd_30d']}        # JP225/USDJPY のΔ（通貨効果を除去）")
        lines.append(f"  currency_effect_pt: {relative['currency_effect_pt']}   # 円安が嵩上げした分")
        lines.append(f"  us100_30d: {relative['us100_30d']}")
        lines.append(f"  jp_vs_us_nominal_pt: {relative['jp_vs_us_nominal_pt']}")
        lines.append(f"  jp_vs_us_fx_adj_pt: {relative['jp_vs_us_fx_adj_pt']}   # 本物の相対強度（FX調整後）")
        lines.append(f"  verdict: {relative['verdict']}   # structure_led=割安リレーティング主導 / currency_led=円安主導 / mixed")
        lines.append("")

    lines.append("snapshot_30d:")
    for name in order:
        info = snapshots.get(name)
        if not info:
            continue
        latest = info.get("latest")
        change = info.get("change_30d")
        if latest is None or change is None:
            continue
        lines.append(f'  "{name}":')
        lines.append(f"    latest: {latest:.3f}")
        lines.append(f"    change_pct: {change:.2f}")

    yaml_text = "\n".join(lines) + "\n"
    return label, summary, yaml_text
