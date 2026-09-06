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
    fred_snapshots: Optional[Dict[str, object]] = None,
) -> Tuple[str, str, str]:
    """
    8ペア30日データからレジームを簡易判定し、概要テキストとYAMLスナップショットを返す。

    Args:
        snapshots: Yahoo 側（当日終値ベース）の pair_snapshots
        fred_snapshots: ★FRED 側（別フィード・公表ラグあり）の snapshots。
            src.market.fetch_fred_snapshots() の戻り値をそのまま渡す。
            取得失敗時は {"_error": "..."} が入っており、その旨を明示出力する。
            None（未取得）と取得失敗は区別して扱う。

    Returns:
        (label, summary_text, yaml_text)
    """

    def _num(v: object) -> Optional[float]:
        """★2026-09-06 追加（Boss訂正 2026-08-29 / H-3）— NaN を「欠損」として入口で潰す。

        NaN は比較演算がすべて False になるため、`if x is None` だけを見ている判定関数は
        NaN を素通しし、**分岐を全部すり抜けて末尾の無条件 return に落ちる**。
        2026-08-28 の実例: US100 が NaN だったため
          _equities_regime() → "flat"（unknown ではなく）
          _relative_strength().verdict → "mixed"
        が出た。どちらも【欠損】ではなく【誤ったラベル】で、
        settings.py 冒頭の「欠損は気づかれるが、間違った値は気づかれない」そのものの事故。

        ★是正は関数ごとに if を足すことではない。末尾に無条件 return を持つ判定関数は
          すべて同じ穴を持つので、**値の入口を1箇所に絞って NaN を None に落とす**。
          これで既存の `is None` ガードが全関数で正しく効き、新しい判定関数を足しても
          同じ穴が開かない。回帰は tests/test_regime_nan.py が固定する。
        """
        if v is None:
            return None
        try:
            f = float(v)
        except (TypeError, ValueError):
            return None
        if f != f:          # NaN は自分自身と等しくない
            return None
        return f

    def _get_pair(name: str) -> Tuple[Optional[float], Optional[float]]:
        info = snapshots.get(name) or {}
        return _num(info.get("latest")), _num(info.get("change_30d"))

    def _get_first(name: str) -> Optional[float]:
        info = snapshots.get(name) or {}
        return _num(info.get("first"))

    def _get_prev_1w(name: str) -> Optional[float]:
        """7暦日前以前の最後の終値（週次Δの基準点）。"""
        info = snapshots.get(name) or {}
        return _num(info.get("prev_1w"))

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
        # ⚠️ 2026-09-06 注記（是正B）: このラベルは US5Y と US10Y の30日変化率の平均符号でしか
        #   判定していない。**2年ゾーン（＝利上げ確率の織り込みが出る位置）を見ていない**ため、
        #   フロント主導の局面では Boss 実測と正面から食い違いうる（2026-08-28 が実例）。
        #   政策期待の判断には使わないこと。FRED 由来の curve_fred(2s10s) を併読する。
        changes = [c for c in (ch_us5y, ch_us10y) if c is not None]
        if not changes:
            return "unknown"
        avg = sum(changes) / len(changes)
        if avg <= -0.5:
            return "falling"
        if avg >= 0.5:
            return "rising"
        return "flat"

    def _window_of(*names: str) -> Optional[str]:
        """週次Δが実際に引き算した2日を "YYYY-MM-DD -> YYYY-MM-DD" で返す。

        ★2026-09-06 追加（Boss「注記だけでなく、窓の定義を明示するフィールドを持たせるのが次の一手」）。
        7暦日ルックバックは祝日・欠測で落ちる日が動くため、同じ「週次Δ」でも週によって
        跨ぐ営業日が変わる。**その1日の出入りだけで符号が反転しうる**（2026-09-03 の 2s10s が実例）。
        構成ペアで基準日が食い違う場合は両方を出す——**揃っていないことを隠さない。**
        """
        bases = {(snapshots.get(n) or {}).get("prev_1w_as_of") for n in names}
        nows = {(snapshots.get(n) or {}).get("as_of") for n in names}
        bases.discard(None)
        nows.discard(None)
        if not bases or not nows:
            return None
        b = sorted(bases)[0] if len(bases) == 1 else "/".join(sorted(bases)) + "(★不揃い)"
        n = sorted(nows)[0] if len(nows) == 1 else "/".join(sorted(nows)) + "(★不揃い)"
        return f"{b} -> {n}"

    def _classify_shape(delta_bp: Optional[float], short_up: bool) -> str:
        """スプレッドのΔと短期側の方向からフラット/スティープの質を判定。"""
        if delta_bp is None:
            return "unknown"
        if delta_bp <= -2.0:
            return "bear_flattening" if short_up else "bull_flattening"
        if delta_bp >= 2.0:
            return "bull_steepening" if not short_up else "bear_steepening"
        return "stable"

    def _curve_spreads() -> Optional[Dict[str, object]]:
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
          ★この close-to-close 系列が 10s30s の正本。手読みの値と1本の時系列に混ぜない
          （手読みは取得時刻がスクショ依存で、日次1〜3bpの指標では変化の大半が時刻差になりうる）。
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
            "change_bp_30d": (round(d_5s10s, 1) if d_5s10s is not None else None),
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
                "change_3m10s_bp_30d": (round(d_3m10s, 1) if d_3m10s is not None else None),
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

    def _inflation_compensation() -> Optional[Dict[str, object]]:
        """インフレ補償（ブレークイーブン）を FRED 実測から組み立てる。2026-08-20 追加。

        年輪候補 8-2 の第二条件「金の上昇には ドル安 かつ BEが崩れないこと」の
        BE を、代理ではなく本体で測るためのブロック。
        代理は2回失敗している（10s30s=反例2件で棄却 / 原油=FOMC議事録が明示的に否定）。

        ★このブロックは【判定しない】。
          - _yields_regime() にも label にも、他のどの合成指標にも混ぜない
            （US30Y を混ぜなかったのと同じ理由。サンプルがゼロの指標に判定させると、
              判定が実測より先に固まる＝8-2 で2回やった失敗そのもの）
          - 閾値も置かない。direction は符号のみ。「BEが崩れた」の水準は今決めない
          - 原油との相関も自動計算しない。議事録の観測は1期間分の1事例で、
            まだ自分で確かめていない。機械が相関を出すと検証済みの事実として扱われる

        ★as_of を必ず添える。FRED は Yahoo より1日古い可能性が常にある。
          黙って同じスナップショットに並べると測定窓の不一致を機械に焼き付ける。
        """
        if not fred_snapshots:
            return None
        if "_error" in fred_snapshots:
            return {"_error": fred_snapshots["_error"]}

        def _one(key: str) -> Optional[Dict[str, object]]:
            info = fred_snapshots.get(key)
            if not isinstance(info, dict):
                return None
            latest = info.get("latest")
            if latest is None:
                return None

            def _delta_bp(base: object) -> Optional[float]:
                if base is None:
                    return None
                return round((float(latest) - float(base)) * 100.0, 1)

            d_1w = _delta_bp(info.get("prev_1w"))
            d_30d = _delta_bp(info.get("prev_30d"))
            # 方向は【週次Δの符号のみ】。閾値は未設定＝判定はしない
            if d_1w is None:
                direction = "unknown"
            elif d_1w > 0:
                direction = "widening"
            elif d_1w < 0:
                direction = "narrowing"
            else:
                direction = "flat"
            return {
                "series_id": info.get("series_id"),
                "as_of": info.get("as_of"),
                "pct": round(float(latest), 3),   # 水準は%表記（bpではない）
                "change_bp_1w": d_1w,
                "change_bp_30d": d_30d,
                "direction_1w": direction,
            }

        be5 = _one("US5YBE")
        be5y5y = _one("US5Y5YBE")
        if be5 is None and be5y5y is None:
            return None
        return {"us5y_be": be5, "us5y5y_be": be5y5y}

    def _curve_fred() -> Optional[Dict[str, object]]:
        """★2026-09-06 追加（是正A / Boss決定 2026-08-29）— FRED 単一フィードの 2s10s。

        既存の curve_spreads は front に 3M(^IRX) を使っている。3M は政策金利そのものに
        貼り付いており、利上げ確率の織り込みという情報を構造的に持たない。FF金利が実際に
        動くまで 3M はほとんど動かないので、**利上げ観測でフロントが売られる局面では
        3M は必ず「動かない側」に回り、機械は必ず bull_flattening を出し続ける**。
        これは front の選び方の好みではなく、指標設計に由来する系統的バイアス。

        → front に 2Y を置いたカーブを別に持つ。Yahoo に2年債指数が無いので FRED から取る。

        ★このブロックは curve_spreads と【統合しない】。
          - curve_spreads = Yahoo（^IRX/^FVX/^TNX/^TYX・実行時取得）
          - curve_fred    = FRED（DGS2/DGS10・NY引け基準・公表ラグあり）
          フィードも時刻も違う。1本の系列に混ぜた瞬間、変化の大半が時刻差になる（年輪§8(e)）。
          2つ同時に出るのは重複ではなく、**フィード差を測れる状態を意図的に作っている**。

        ★速報性は解決しない。H.15 は1営業日遅れる（2026-08-28 がまさにその事例）。
          「速い系列（Boss実測・Yahoo）」と「揃った系列（FRED）」を別レイヤーで持つ設計。

        ★判定はしない。水準とΔを出すだけで、label にも _yields_regime() にも混ぜない。
          （US30Y・inflation_compensation と同じ扱い。サンプルがゼロの指標に判定させない）
        """
        if not fred_snapshots or "_error" in fred_snapshots:
            return None
        two = fred_snapshots.get("US2YNOM")
        ten = fred_snapshots.get("US10YNOM")
        if not isinstance(two, dict) or not isinstance(ten, dict):
            return None
        y2, y10 = _num(two.get("latest")), _num(ten.get("latest"))
        if y2 is None or y10 is None:
            return None
        as_of_2, as_of_10 = two.get("as_of"), ten.get("as_of")
        if as_of_2 != as_of_10:
            # 同一フィードでも年限ごとに最終行がずれることがある。ずれたまま引き算しない。
            return {"_date_mismatch": f"DGS2 as_of={as_of_2} / DGS10 as_of={as_of_10}"}

        def _spread_at(k2: str, k10: str) -> Optional[float]:
            b2, b10 = _num(two.get(k2)), _num(ten.get(k10))
            if b2 is None or b10 is None:
                return None
            return (b10 - b2) * 100.0

        now_bp = (y10 - y2) * 100.0
        d_1w = _spread_at("prev_1w", "prev_1w")
        d_30d = _spread_at("prev_30d", "prev_30d")
        # ★週次Δの窓を明示する（Boss「次の一手」2026-09-06）。
        #   7暦日ルックバックは落ちる日が動く。2026-09-03 基準では窓が 8/28 を跨がず 8/27 に落ち、
        #   2s10s が -8.0bp フラット化した 8/28 の1日が窓から外れただけで符号が反転した
        #   （機械 -4.0bp / Boss 窓 +4.0bp）。**符号を読む前に窓を見る**ための欄。
        base_1w = two.get("prev_1w_as_of") or ten.get("prev_1w_as_of")
        window_1w = f"{base_1w} -> {as_of_2}" if base_1w else None
        return {
            "as_of": as_of_2,
            "us2y_pct": round(y2, 3),
            "us10y_pct": round(y10, 3),
            "spread_2s10s_bp": round(now_bp, 1),
            "change_2s10s_bp_1w": None if d_1w is None else round(now_bp - d_1w, 1),
            "change_2s10s_bp_1w_window": window_1w,
            "change_2s10s_bp_30d": None if d_30d is None else round(now_bp - d_30d, 1),
        }

    equities = _equities_regime()
    vol = _vol_regime()
    oil = _oil_regime()
    gold = _gold_regime()
    crypto = _crypto_regime()
    yields_regime = _yields_regime()
    curve = _curve_spreads()
    intervention = _intervention_flag()
    relative = _relative_strength()
    inflation_comp = _inflation_compensation()
    curve_fred = _curve_fred()

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
        _chg = curve["change_bp_30d"]
        _chg_str = (f"Δ30d{_chg:+.1f}bp" if _chg is not None else "Δ30d n/a")
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
    # ★curve_fred（FRED単一フィードの2s10s）は【表示のみ】。ラベル判定には使わない。
    #   as_of を必ず併記する（H.15 は1営業日遅れる＝Yahoo側と同日ではない）。
    if curve_fred is not None and "_date_mismatch" not in curve_fred:
        _f1w = curve_fred["change_2s10s_bp_1w"]
        _f1w_str = (f"Δ1w{_f1w:+.1f}bp" if _f1w is not None else "Δ1w n/a")
        summary += (
            f", curve_fred[as_of {curve_fred['as_of']}]"
            f"(2s10s={curve_fred['spread_2s10s_bp']:+.1f}bp,{_f1w_str})"
        )
    elif curve_fred is not None:
        summary += f", curve_fred=DATE_MISMATCH({curve_fred['_date_mismatch']})"
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
    # インフレ補償（BE）は【表示のみ】。ラベル判定には一切使わない。
    # as_of を必ず併記する（FRED は別フィードで公表ラグがあり、他の値と同日ではない）
    if inflation_comp is not None:
        if "_error" in inflation_comp:
            summary += f", inflation_comp=FETCH_FAILED({inflation_comp['_error']})"
        else:
            _b5 = inflation_comp.get("us5y_be")
            _b55 = inflation_comp.get("us5y5y_be")
            _parts: List[str] = []
            if _b5:
                _d = _b5["change_bp_1w"]
                _ds = (f"Δ1w{_d:+.1f}bp" if _d is not None else "Δ1w n/a")
                _parts.append(f"5yBE={_b5['pct']:.2f}%,{_ds}/{_b5['direction_1w']}")
            if _b55:
                _d = _b55["change_bp_1w"]
                _ds = (f"Δ1w{_d:+.1f}bp" if _d is not None else "Δ1w n/a")
                _parts.append(f"5y5yBE={_b55['pct']:.2f}%,{_ds}/{_b55['direction_1w']}")
            _as_of = (_b5 or _b55 or {}).get("as_of")
            if _parts:
                summary += f", inflation_comp[as_of {_as_of}]({'; '.join(_parts)})"

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
    # ★2026-09-06（H-4）: ペア間で as_of が割れていないかを snapshot 自身に書く。
    #   人間が気づくのを待たない。割れた週は snapshot を開いた瞬間に分かる形にする。
    #   ★24/7 で動く銘柄（暗号資産）は【常に】他と日付が違う。これを SPLIT に数えると
    #     毎週 SPLIT が点灯し、**常時点灯する警告は読まれなくなる**（wk04 の欠測のような
    #     本当に割れた週を見落とす）。既知の別カレンダーは分けて出す。
    _ALWAYS_OFF_CALENDAR = {"BTC/USD"}
    _as_ofs: Dict[str, str] = {}
    _off_cal: Dict[str, str] = {}
    for _n, _i in (snapshots or {}).items():
        _a = (_i or {}).get("as_of")
        if not _a:
            continue
        (_off_cal if _n in _ALWAYS_OFF_CALENDAR else _as_ofs).setdefault(str(_a), []).append(_n)

    lines.append("snapshot_date_integrity:")
    if not _as_ofs:
        lines.append("  status: unknown            # per-pair の as_of が無い（旧形式の snapshot）")
    elif len(_as_ofs) == 1:
        _only = next(iter(_as_ofs))
        lines.append(f"  status: aligned            # ★全ペアの latest が {_only} で揃っている")
        lines.append(f"  as_of: {_only}")
    else:
        lines.append("  status: SPLIT            # ★★ペアごとに latest の日付が割れている。読む前にここを見る")
        for _d in sorted(_as_ofs, reverse=True):
            lines.append(f"  \"{_d}\": [{', '.join(_as_ofs[_d])}]")
        lines.append("  note: \"★★日付が割れた週は、ペアをまたぐ差分（カーブ・スプレッド・相対強度）が【異なる時点の引き算】になる。2026-08-28 は金利4本だけが講演前の 8/27 で、機械のカーブは当週最大のイベントを1本も織り込んでいなかった。割れているときは、どのペアがどの日付かを明示せずに差分を引用しないこと。\"")
    for _d in sorted(_off_cal, reverse=True):
        lines.append(f"  off_calendar_{_d}: [{', '.join(_off_cal[_d])}]   # 24/7銘柄。他と日付が違うのは既知・異常ではない")
    _missing = [n for n, i in (snapshots or {}).items() if _num((i or {}).get("latest")) is None]
    if _missing:
        lines.append(f"  missing: [{', '.join(_missing)}]            # ★取得失敗またはNaN。判定は unknown に落ちる")
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

    # ── 金利カーブ（4点 3M/5Y/10Y/30Y）: yields ラベルの丸めを補正する立体形状指標 ──
    if curve is not None:
        lines.append("curve_spreads:")
        lines.append("  # renamed 2026-08-09: curve_2s10s → curve_spreads / change_bp → change_bp_30d / change_3m10s_bp → change_3m10s_bp_30d")
        lines.append("  #   旧名は 2026-08-09 以前の distilled・週次アーカイブに残っている。同名の別指標ではなく同一指標の旧名。")
        lines.append("  #   （旧 curve_2s10s は中身が 5s10s/3m10s/belly/10s30s で 2s10s を1つも含まなかったための改名）")
        lines.append(f"  spread_bp: {curve['spread_bp']}            # 5s10s（US10Y − US5Y=^FVX）※符号は市場慣行の【長期−短期】")
        if curve.get("change_bp_30d") is not None:
            lines.append(f"  change_bp_30d: {curve['change_bp_30d']}")
        lines.append(f"  shape: {curve['shape']}            # 5s10s の質")
        lines.append(f"  inverted: {str(curve['inverted']).lower()}")
        if "spread_3m10s_bp" in curve:
            pts = curve.get("points_pct") or {}
            lines.append(f"  spread_3m10s_bp: {curve['spread_3m10s_bp']}      # 3m10s（US10Y − US3M=^IRX）=Fed重視の景気後退カーブ・逆イールド主ゲージ")
            if curve.get("change_3m10s_bp_30d") is not None:
                lines.append(f"  change_3m10s_bp_30d: {curve['change_3m10s_bp_30d']}")
            lines.append(f"  shape_3m10s: {curve['shape_3m10s']}      # ⚠️【政策期待の判断には使えない】front=3M は利上げ確率の織り込みを構造的に持たない（→ curve_fred）")
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
            # ★2026-09-06（Boss「次の一手」2026-09-06）: 注記だけでなく【窓そのもの】をフィールドで出す。
            #   7暦日ルックバックは祝日や欠測で落ちる日が動くため、同じ「週次Δ」でも週によって
            #   跨ぐ営業日が変わる。2026-09-03 基準の curve_fred では窓が 8/28 を跨がず 8/27 に落ち、
            #   その1日（2s10s が -8.0bp フラット化した日）の出入りだけで符号が反転した。
            #   ★窓を書いておけば、符号を読む前に窓を確認できる。
            _w10 = _window_of("US30Y", "US10Y")
            if _w10:
                lines.append(f"  change_10s30s_bp_1w_window: {_w10}   # ★実際に引き算した2日。符号を読む前にここを見る")
            lines.append(f"  change_10s30s_bp_30d: {curve['change_10s30s_bp_30d']}      # 30日Δ（構造的ドリフト）")
            lines.append(f"  direction_10s30s_1w: {curve['direction_10s30s_1w']}      # 【週次Δ】の符号のみ（widening/narrowing/flat）。閾値は未設定＝判定はしない")
        lines.append(
            '  note: "スプレッドの符号はすべて市場慣行の【長期−短期】（2s10sが+45bpなら10Yが2Yより45bp上）。'
            '5s10s（US10Y−US5Y=^FVX）は5年がカーブ中腹のため、front=政策(3M)が belly(5Y) より低い順イールド環境では'
            '最もフラットな区間＝5s10sのbear_flatteningは逆イールド接近を過大評価しうる。景気後退の主ゲージは 3m10s（spread_3m10s_bp）で読む。'
            'structure=belly_elevated は政策ターミナル織り込みの瘤＝front低・belly突出・long growth。shape*は短期↑/長期↓のフラット化の質、'
            'recession_3m10s が near_inversion/inverted に入ったら本格警戒。'
            '10s30s は【水準・Δ(週次/30日の2窓)・方向(週次Δの符号のみ)】を出すだけでレジームラベル・複合スコアには混ぜない。'
            '閾値を置かないのはサンプルが4営業日分しかないため。8〜12週ためてから閾値の検討を行う。'
            '同じスプレッドでも窓が違えば符号が逆になりうる（30日では拡大・直近1週では縮小 等）ので、必ず窓を明示して引用すること。'
            '★本欄（機械のclose-to-close系列）が 10s30s の正本。手読みの値と1本の時系列に混ぜない。'
            '理由は【時刻とベンダーの二重の不一致】。手読みはスクショを撮った時刻に依存し（NY引け/ロンドン午後が混在しうる）、'
            'ベンダーも異なる。日次変動が1〜3bpの指標では、変化の大半が時刻差になりうる。'
            '※この2つの誤差源はまだ分離できていない（純粋なベンダー差の比較は同一時刻同士の n=1 のみ）。分離できれば併用可能になる余地は残る。'
            '機械側は毎日同じ時刻・同じベンダーで自動的に積み上がるため、8〜12週の計数はこちらで数える。'
            '読み筋（人間側・★未検証）: 拡大=タームプレミアム／ソブリン信用の象限で金に追い風、縮小=純粋なディスインフレで金には何も来ない。'
            '2026-08-09時点で機械系列による裏づけは無い（7営業日で符号一致5/7だが、金が週で最も上げた8/5に10s30sは縮小）。機構の仮説として保持し、実測の主張はしない。'
            '★本欄は【事後の記録】であって当日の判定には使えない。CPI等の当日反応は【同一日・同一チャートのセッション内前後比較】で見る'
            '（発表直前に 30Y−10Y を読み、反応が落ち着いた頃に同じチャートで再度読み、その2点の差を取る）。'
            '同じ日・同じ時間帯・同じベンダーなので時刻差もベンダー差も入らない。求めているのは当日の変化であって水準ではない。"'
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

    # ── ★FRED 単一フィードの 2s10s（2026-09-06 追加・是正A）──
    #    front に 2Y を置いたカーブ。curve_spreads（Yahoo・front=3M）とは【別ブロック】で、統合しない。
    #    3M は政策金利に貼り付いており利上げ確率の織り込みを構造的に持たないため、
    #    フロント主導の局面では curve_spreads の shape_3m10s が一方向に誤り続ける。
    if curve_fred is not None:
        lines.append("curve_fred:")
        lines.append("  # FRED DGS2/DGS10（NY引け基準・公表ラグあり）。★curve_spreads（Yahoo系）と統合しないこと。")
        lines.append("  # 2つ同時に出るのは重複ではなく、フィード差を測れる状態を意図的に作っている（年輪§8(e)）。")
        if "_date_mismatch" in curve_fred:
            lines.append(f"  _date_mismatch: {_yv(curve_fred['_date_mismatch'])}   # 年限で最終行がずれたため引き算しない")
        else:
            lines.append(f"  as_of: {curve_fred['as_of']}        # ★必須。Yahoo側より1営業日古いことが常にありうる")
            lines.append(f"  us2y_pct: {curve_fred['us2y_pct']}          # DGS2＝政策期待を見る位置のフロント")
            lines.append(f"  us10y_pct: {curve_fred['us10y_pct']}")
            lines.append(f"  spread_2s10s_bp: {curve_fred['spread_2s10s_bp']}      # 符号は市場慣行の【長期−短期】")
            lines.append(f"  change_2s10s_bp_1w: {curve_fred['change_2s10s_bp_1w']}")
            if curve_fred.get("change_2s10s_bp_1w_window"):
                lines.append(f"  change_2s10s_bp_1w_window: {curve_fred['change_2s10s_bp_1w_window']}   # ★実際に引き算した2日。符号を読む前にここを見る")
            lines.append(f"  change_2s10s_bp_30d: {curve_fred['change_2s10s_bp_30d']}")
        lines.append("  note: \"★判定はしない（レジームラベル・複合スコアに混ぜない。閾値も未設定）。curve_spreads の front は 3M で、3M は政策金利そのものに貼り付いており【利上げ確率の織り込みを構造的に持たない】。FF金利が実際に動くまで 3M はほとんど動かないため、利上げ観測でフロントが売られる局面では 3M は必ず『動かない側』に回り、機械は必ず bull_flattening を出し続ける（2026-08-28 が実例: 機械 bull_flattening vs Boss ベアフラットニング）。これは front の選び方の好みではなく指標設計に由来する系統的バイアスであり、shape_3m10s / shape / yields は【政策期待の判断には使えない】。本ブロックがその位置を埋める。⚠️ただし H.15 は1営業日遅れるので速報性は解決しない——『速い系列（Boss実測・Yahoo）』と『揃った系列（FRED）』を別レイヤーで持つ設計。\"")
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

    # ── インフレ補償（BE）: ★FRED＝Yahooとは別フィード・公表ラグあり（2026-08-20 追加）──
    #    年輪候補 8-2 の第二条件「ドル安 かつ BEが崩れないこと」の BE を代理でなく本体で測る。
    #    ★判定はしない（レジームラベル・複合スコアに混ぜない。閾値も未設定。原油との相関も出さない）。
    if inflation_comp is not None:
        lines.append("inflation_compensation:")
        if "_error" in inflation_comp:
            # ★「データ欠損」と「取得失敗」を区別する。黙って欠落させない（2026-08-09 の教訓）
            lines.append(f"  # ERROR: {inflation_comp['_error']}（データ欠損ではなく取得失敗）")
            lines.append("  status: fetch_failed")
        else:
            lines.append("  # FRED（Yahooとは別フィード）。公表ラグがあるため as_of を必ず確認すること。")
            lines.append("  # 他ブロックの価格は当日、ここは as_of の日付。同日として比較しないこと。")
            _be5 = inflation_comp.get("us5y_be")
            _be55 = inflation_comp.get("us5y5y_be")
            if _be5:
                lines.append(f"  us5y_be_as_of: {_be5['as_of']}        # ★必須。他ブロックと不一致でも異常ではない")
                lines.append(f"  us5y_be_pct: {_be5['pct']}                 # 5年BE＝近期インフレ補償（{_be5['series_id']}）。水準は%表記（bpではない）")
                lines.append(f"  change_5ybe_bp_1w: {_be5['change_bp_1w']}           # 週次Δ（bp）")
                lines.append(f"  change_5ybe_bp_30d: {_be5['change_bp_30d']}          # 30日Δ（bp）")
                lines.append(f"  direction_5ybe_1w: {_be5['direction_1w']}      # 週次Δの符号のみ。閾値は未設定＝判定はしない")
            if _be55:
                lines.append(f"  us5y5y_be_as_of: {_be55['as_of']}")
                lines.append(f"  us5y5y_be_pct: {_be55['pct']}               # 5年5年先フォワード＝長期インフレ期待アンカー（{_be55['series_id']}）")
                lines.append(f"  change_5y5ybe_bp_1w: {_be55['change_bp_1w']}")
                lines.append(f"  change_5y5ybe_bp_30d: {_be55['change_bp_30d']}")
                lines.append(f"  direction_5y5ybe_1w: {_be55['direction_1w']}")
            lines.append(
                '  note: "年輪候補8-2の第二条件（金の上昇には ドル安 かつ BEが崩れないこと）を、代理でなく本体で測るブロック。'
                '代理は2回失敗している——10s30s（反例2件で棄却）と原油（8/19公表の7/28-29 FOMC議事録が'
                '「インフレ補償は原油高にほとんど動かず／近期のインフレ補償は6月FOMC後に大きく低下し、その後原油の急騰にもかかわらず小幅にしか戻らなかった」と明示して否定）。'
                '★判定はしない: レジームラベルにも他のどの合成指標にも混ぜず、閾値も置かない（「BEが崩れた」の水準を今決めない）。'
                'サンプルがゼロの指標に判定させると判定が実測より先に固まる＝8-2で2回やった失敗そのもの。8〜12週ためてから検討する。'
                '★原油との相関は自動計算しない。議事録の観測は1期間分の1事例で、まだ自分で確かめていない。'
                '機械が相関を出すと検証済みの事実として扱われる。まず生の系列をためる。'
                '★2本ある理由: 近期(5Y BE)はエネルギー価格の影響を受けやすく、5y5yフォワードはそれを剥いだアンカー。'
                '差が診断になる——5Y BEだけ動いて5y5yが動かない=市場は原油の影響を一時的と見ている / 両方動く=インフレ期待そのものが動いた。'
                '8-2が問いたいのは後者なので1本だけでは判別できない。'
                '★as_of は Yahoo 側より1日古いことが常にありうる（FREDの公表ラグ）。同日として比較しないこと。"'
            )
        lines.append("")

    # ★2026-09-06（H-4）: 値と一緒に per-pair の as_of を出す。
    #   2026-08-28 はペアごとに日付が割れていた（金利4本=8/27 / US100=NaN / 他=8/28）が、
    #   snapshot に日付が無かったため目視で個別に取りに行くまで見えなかった。
    lines.append("snapshot_30d:")
    for name in order:
        info = snapshots.get(name)
        if not info:
            continue
        latest = _num(info.get("latest"))
        change = _num(info.get("change_30d"))
        if latest is None or change is None:
            # ★取得失敗/NaN でも【行は残す】。黙って消えると欠測が見えなくなる。
            lines.append(f'  "{name}":')
            lines.append("    latest: null            # ★未取得または NaN（値が無いことを明示）")
            lines.append(f"    as_of: {info.get('as_of') or 'null'}")
            continue
        lines.append(f'  "{name}":')
        lines.append(f"    latest: {latest:.3f}")
        lines.append(f"    change_pct: {change:.2f}")
        lines.append(f"    as_of: {info.get('as_of') or 'null'}            # ★latest の実日付")
        if info.get("first_as_of"):
            lines.append(f"    change_pct_window: {info['first_as_of']} -> {info.get('as_of')}   # 30日Δの窓")
        if info.get("prev_1w_as_of"):
            lines.append(f"    prev_1w_as_of: {info['prev_1w_as_of']}   # ★週次Δの基準日（7暦日前【以前】なので週により動く）")

    yaml_text = "\n".join(lines) + "\n"
    return label, summary, yaml_text
