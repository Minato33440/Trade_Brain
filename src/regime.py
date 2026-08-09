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

    def _get_prev_1w(name: str) -> Optional[float]:
        """7暦日前以前の最後の終値（週次Δの基準点）。"""
        info = snapshots.get(name) or {}
        return info.get("prev_1w")

    latest_us100, ch_us100 = _get_pair("US100")
    latest_jp225, ch_jp225 = _get_pair("JP225")
    latest_btc, ch_btc = _get_pair("BTC/USD")
    latest_wti, ch_wti = _get_pair("WTI")
    latest_vix, ch_vix = _get_pair("VIX")
    latest_xau, ch_xau = _get_pair("XAU/USD")
    latest_us3m, ch_us3m = _get_pair("US3M")
    latest_us5y, ch_us5y = _get_pair("US5Y")     # 2026-08-09: 旧 "US2Y"（実体は^FVX=5年債）
    latest_us10y, ch_us10y = _get_pair("US10Y")
    latest_us30y, ch_us30y = _get_pair("US30Y")  # 2026-08-09追加（^TYX）
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
        # 2026-08-09: US30Y は意図的に混ぜない（10s30s は判定に使わず、水準/Δ/方向だけ出す）
        changes = [c for c in (ch_us5y, ch_us10y) if c is not None]
        if not changes:
            return "unknown"
        avg = sum(changes) / len(changes)
        if avg <= -0.5:
            return "falling"
        if avg >= 0.5:
            return "rising"
        return "flat"

    def _classify_shape(delta_bp: Optional[float], short_up: bool) -> str:
        """スプレッドのΔと短期側の方向からフラット/スティープの質を判定。"""
        if delta_bp is None:
            return "unknown"
        if delta_bp <= -2.0:
            return "bear_flattening" if short_up else "bull_flattening"
        if delta_bp >= 2.0:
            return "bull_steepening" if not short_up else "bear_steepening"
        return "stable"

    def _curve_2s10s() -> Optional[Dict[str, object]]:
        """4点（3M/5Y/10Y/30Y）でイールドカーブの形状を立体的に判定。

        ★スプレッドの符号はすべて【市場慣行＝長期 − 短期】で統一する（2026-08-09 ボス指摘）。
          指標名（"5s10s"）を読み順のまま引き算に写すと逆になるので注意。
          例: 2s10s が +45bp とは「10Y が 2Y より 45bp 上」の意味。
          ※以前はコメント側だけが3本とも逆順（"US5Y − US10Y" 等）に書かれていた。
            コードが正しくコメントが誤り。コメントに合わせてコードを直すと符号が反転し、
            direction_10s30s の widening/narrowing が入れ替わる（絶対値は同じなので目視で気づけない）。

        - 5s10s（US10Y − US5Y=^FVX）: 既存指標。後方互換で spread_bp/shape に残す。
        - 3m10s（US10Y − US3M=^IRX）: Fed重視の景気後退カーブ。逆イールド接近の主ゲージ。
        - belly_premium: 3M→10Y 直線を5Y満期で補間し実5Yとの差＝belly(5Y)の突出度。
          front=政策(3M)・belly=5Y突出・long=growth(10Y) の構造を可視化。
        - 10s30s（US30Y=^TYX − US10Y）: 超長期のタームプレミアム。2026-08-09追加。
          ★出すのは【水準bp / Δbp（30日・週次の2窓）/ 方向ラベル（週次Δの符号のみ）】だけで、
          レジームラベル・複合スコアには混ぜない（サンプルが4営業日分しかなく閾値を置けないため）。
        yields ラベル（5Y/10Y平均符号で rising/falling に丸める）の補正指標。
        """
        if latest_us5y is None or latest_us10y is None:
            return None
        first_us10y = _get_first("US10Y")

        # ── 5s10s（既存・US5Y=^FVX）──
        spread_5s10s = (latest_us10y - latest_us5y) * 100.0
        first_us5y = _get_first("US5Y")
        d_5s10s: Optional[float] = None
        if first_us5y not in (None, 0) and first_us10y not in (None, 0):
            d_5s10s = spread_5s10s - (first_us10y - first_us5y) * 100.0
        short_up = (ch_us5y is not None and ch_us5y > 0)

        out: Dict[str, object] = {
            "spread_bp": round(spread_5s10s, 1),                 # 後方互換: 5s10s
            "change_bp": (round(d_5s10s, 1) if d_5s10s is not None else None),
            "shape": _classify_shape(d_5s10s, short_up),
            "inverted": spread_5s10s < 0,
        }

        # ── 3m10s（US3M=^IRX front。Fed重視の景気後退カーブ）＋ 3点構造 ──
        if latest_us3m is not None:
            spread_3m10s = (latest_us10y - latest_us3m) * 100.0
            spread_3m5s = (latest_us5y - latest_us3m) * 100.0
            first_us3m = _get_first("US3M")
            d_3m10s: Optional[float] = None
            if first_us3m not in (None, 0) and first_us10y not in (None, 0):
                d_3m10s = spread_3m10s - (first_us10y - first_us3m) * 100.0
            short3_up = (ch_us3m is not None and ch_us3m > 0)

            # belly premium: 満期(年) 3M=0.25 / 5Y=5 / 10Y=10 の直線補間と実5Yの差
            interp_5y = latest_us3m + (latest_us10y - latest_us3m) * ((5.0 - 0.25) / (10.0 - 0.25))
            belly_premium = (latest_us5y - interp_5y) * 100.0
            if belly_premium >= 8.0:
                structure = "belly_elevated"     # 5Y突出＝政策ターミナル織り込みの瘤（hump）
            elif belly_premium <= -8.0:
                structure = "belly_depressed"
            else:
                structure = "linear"

            # 景気後退の主ゲージは 3m10s
            if spread_3m10s < 0:
                recession = "inverted"
            elif spread_3m10s < 25.0:
                recession = "near_inversion"
            else:
                recession = "positive"

            out.update({
                "spread_3m10s_bp": round(spread_3m10s, 1),
                "change_3m10s_bp": (round(d_3m10s, 1) if d_3m10s is not None else None),
                "shape_3m10s": _classify_shape(d_3m10s, short3_up),
                "spread_3m5s_bp": round(spread_3m5s, 1),
                "belly_premium_bp": round(belly_premium, 1),
                "structure": structure,
                "recession_3m10s": recession,
                "points_pct": {
                    "m3": round(latest_us3m, 3),
                    "y5": round(latest_us5y, 3),
                    "y10": round(latest_us10y, 3),
                },
            })

        # ── 10s30s（US10Y − US30Y）: 超長期のタームプレミアム（2026-08-09追加）──
        # ★判定はしない。水準・Δ・方向（符号のみ）の3つだけを出す。
        #   閾値を置かない理由: 手元のサンプルが4営業日分しかなく、線を引くには足りない。
        #   8〜12週ためてから閾値の検討を行う（それまでは人間側で読む）。
        if latest_us30y is not None:
            spread_10s30s = (latest_us30y - latest_us10y) * 100.0   # 長期 − 短期

            def _delta(base_30y: Optional[float], base_10y: Optional[float]) -> Optional[float]:
                if base_30y in (None, 0) or base_10y in (None, 0):
                    return None
                return spread_10s30s - (base_30y - base_10y) * 100.0

            # 2窓を併記する（2026-08-09 ボス指摘）。同じスプレッドでも窓が違えば符号が逆になりうる
            # （30日では拡がり、直近1週では縮む等）。フィールド名に窓を入れて取り違えを防ぐ。
            d_30d = _delta(_get_first("US30Y"), first_us10y)
            d_1w = _delta(_get_prev_1w("US30Y"), _get_prev_1w("US10Y"))

            # ★方向ラベルは【週次Δ】を主にする。
            #   §8-2 の読み筋を導いた観測が日次〜週次の動きだったため。
            #   30日Δで方向を出すと、過去1ヶ月のトレンドが直近の変化を上書きしてしまう。
            if d_1w is None:
                direction = "unknown"
            elif d_1w > 0:
                direction = "widening"
            elif d_1w < 0:
                direction = "narrowing"
            else:
                direction = "flat"
            out.update({
                "spread_10s30s_bp": round(spread_10s30s, 1),
                "change_10s30s_bp_30d": (round(d_30d, 1) if d_30d is not None else None),
                "change_10s30s_bp_1w": (round(d_1w, 1) if d_1w is not None else None),
                "direction_10s30s_1w": direction,
                "y30_pct": round(latest_us30y, 3),
            })
        return out

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
            "watch_zone": watch_zone,                   # zone判定のしきい値（yamlコメント用）
            "upper_alert": latest_usdjpy >= upper_alert,
            "upper_alert_level": upper_alert,
            "imf_ammo_remaining": cfg.get("imf_ammo_remaining"),
            "imf_window_note": cfg.get("imf_window_note"),      # エピソード窓の終期など（手動更新）
            "us_participation": cfg.get("us_participation"),    # 米側の関与（IMF枠の外側）
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
        summary += f", curve={curve['shape']}(5s10s={curve['spread_bp']:+.1f}bp,{_chg_str}"
        if "spread_3m10s_bp" in curve:
            summary += (
                f"; 3m10s={curve['spread_3m10s_bp']:+.1f}bp/{curve['recession_3m10s']}"
                f"; {curve['structure']}"
            )
        if "spread_10s30s_bp" in curve:
            _d1w = curve["change_10s30s_bp_1w"]
            _d1w_str = (f"Δ1w{_d1w:+.1f}bp" if _d1w is not None else "Δ1w n/a")
            _d30 = curve["change_10s30s_bp_30d"]
            _d30_str = (f"Δ30d{_d30:+.1f}bp" if _d30 is not None else "Δ30d n/a")
            # 表示のみ。ラベル判定には使わない
            summary += (
                f"; 10s30s={curve['spread_10s30s_bp']:+.1f}bp,{_d1w_str},{_d30_str}"
                f"/{curve['direction_10s30s_1w']}"
            )
        summary += ")"
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
        "US3M", "US5Y", "VIX", "US10Y", "US30Y", "BTC/USD",
    ]
    panel = {
        "risk": ["US100", "JP225", "BTC/USD"],
        "fear": ["VIX"],
        "inflation": ["WTI", "XAU/USD"],
        "rates": ["US3M", "US5Y", "US10Y", "US30Y"],
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

    # ── 金利カーブ（3点 3M/5Y/10Y）: yields ラベルの丸めを補正する立体形状指標 ──
    if curve is not None:
        lines.append("curve_2s10s:")
        lines.append(f"  spread_bp: {curve['spread_bp']}            # 5s10s（US10Y − US5Y=^FVX）※符号は市場慣行の【長期−短期】")
        if curve.get("change_bp") is not None:
            lines.append(f"  change_bp: {curve['change_bp']}")
        lines.append(f"  shape: {curve['shape']}            # 5s10s の質")
        lines.append(f"  inverted: {str(curve['inverted']).lower()}")
        if "spread_3m10s_bp" in curve:
            pts = curve.get("points_pct") or {}
            lines.append(f"  spread_3m10s_bp: {curve['spread_3m10s_bp']}      # 3m10s（US10Y − US3M=^IRX）=Fed重視の景気後退カーブ・逆イールド主ゲージ")
            if curve.get("change_3m10s_bp") is not None:
                lines.append(f"  change_3m10s_bp: {curve['change_3m10s_bp']}")
            lines.append(f"  shape_3m10s: {curve['shape_3m10s']}")
            lines.append(f"  spread_3m5s_bp: {curve['spread_3m5s_bp']}")
            lines.append(f"  belly_premium_bp: {curve['belly_premium_bp']}      # 5Yの直線補間からの突出度（+=belly elevated/hump）")
            lines.append(f"  structure: {curve['structure']}      # front=政策(3M)/belly=5Y/long=growth(10Y) の形")
            lines.append(f"  recession_3m10s: {curve['recession_3m10s']}      # positive/near_inversion(<25bp)/inverted")
            _y30 = curve.get("y30_pct")
            _pts = f"{{m3: {pts.get('m3')}, y5: {pts.get('y5')}, y10: {pts.get('y10')}"
            _pts += (f", y30: {_y30}}}" if _y30 is not None else "}")
            lines.append(f"  points_pct: {_pts}")
        if "spread_10s30s_bp" in curve:
            lines.append(f"  spread_10s30s_bp: {curve['spread_10s30s_bp']}      # 10s30s（US30Y=^TYX − US10Y）=超長期のタームプレミアム")
            lines.append(f"  change_10s30s_bp_1w: {curve['change_10s30s_bp_1w']}      # 週次Δ（7暦日前以前の最後の終値が基準）")
            lines.append(f"  change_10s30s_bp_30d: {curve['change_10s30s_bp_30d']}      # 30日Δ（構造的ドリフト）")
            lines.append(f"  direction_10s30s_1w: {curve['direction_10s30s_1w']}      # 【週次Δ】の符号のみ（widening/narrowing/flat）。閾値は未設定＝判定はしない")
        lines.append(
            '  note: "スプレッドの符号はすべて市場慣行の【長期−短期】（2s10sが+45bpなら10Yが2Yより45bp上）。'
            '5s10s（US10Y−US5Y=^FVX）は5年がカーブ中腹のため、front=政策(3M)が belly(5Y) より低い順イールド環境では'
            '最もフラットな区間＝5s10sのbear_flatteningは逆イールド接近を過大評価しうる。景気後退の主ゲージは 3m10s（spread_3m10s_bp）で読む。'
            'structure=belly_elevated は政策ターミナル織り込みの瘤＝front低・belly突出・long growth。shape*は短期↑/長期↓のフラット化の質、'
            'recession_3m10s が near_inversion/inverted に入ったら本格警戒。'
            '10s30s は【水準・Δ(週次/30日の2窓)・方向(週次Δの符号のみ)】を出すだけでレジームラベル・複合スコアには混ぜない。'
            'サンプルが4営業日分しかなく閾値を置けないため、8〜12週ためてから閾値の検討を行う。'
            '同じスプレッドでも窓が違えば符号が逆になりうる（30日では拡大・直近1週では縮小 等）ので、必ず窓を明示して引用すること。'
            '★フィード差の注意: 機械(Yahoo ^TYX/^TNX)とBossチャート読みでは同日でも最大約1.9bpずれる（実測 2026-07-31: 機械53.0 vs Boss54.9）。'
            'これは週次Δの絶対値(~0.5-2bp)と同オーダーなので、週次Δの符号はフィード依存になりうる。'
            '方向ラベルは【機械フィード内で完結して】読み、Boss実測の系列と1本の時系列に混ぜない。'
            '読み筋（人間側）: 拡大=タームプレミアム／ソブリン信用の象限で金に追い風、縮小=純粋なディスインフレで金には何も来ない。'
            '★ただし本欄は【事後の記録】であって当日の判定には使えない。CPI等の当日反応は US10Y/US30Y のチャートを直接読み、'
            '30Y−10Y を手で引く（--trade のΔは週次/30日窓のため当日の動きをほぼ拾わない）。"'
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
        lines.append(f"  zone: {intervention['zone']}            # >=watch_zone({intervention['watch_zone']}) で watch")
        lines.append(f"  upper_alert: {str(intervention['upper_alert']).lower()}   # >=upper_alert_level({intervention['upper_alert_level']}) で true")
        lines.append(f"  imf_ammo_remaining: {_yv(intervention['imf_ammo_remaining'])}")
        if intervention.get("imf_window_note"):
            lines.append(f"  imf_window_note: {_yv(intervention['imf_window_note'])}")
        if intervention.get("us_participation"):
            lines.append(f"  us_participation: {_yv(intervention['us_participation'])}")
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
        lines.append(f"  currency_effect_pt: {relative['currency_effect_pt']}   # 通貨効果（+=円安が嵩上げ / -=円高が押し下げ）")
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
