---
type: outcome_record
week: 2026-6-26_wk04
engine: codex-5.5
created: 2026-07-12
source_instruction: scratch/codex/instructions/reverse_lookup_6-26.md
status: draft_for_broker_review
scope: retrieval_observation_verification
verification_window: 2026-6-26_wk04 -> 2026-7-3_wk01
outcome_status: partial_1w_only
canon_write: none
---

# 2026-6-26_wk04 outcome 照合 — reverse lookup / backfill v1 Stage 2-3

## 0. 照合品質メモ

- 本稿は `distilled/2026/distilled-gm-2026-6.md` の `2026-6-26_wk04` を時点Tの読みとして、後続で確認できる唯一の週 `distilled-gm-2026-7.md` の `2026-7-3_wk01` と照合した。
- outcome窓は **1週のみ**。4週先判定は未確定。
- close ベースの週次distilledで見えるものだけを confirmed とし、ヒゲ・日中flash・同日内の同時性が必要なものは `unverified` または `not_confirmed_on_weekly_close` とした。
- 先行 misreads（6-5 / 6-19）は型だけ参照し、6-26は独立判定した。

---

## 1. 時点Tの読み（2026-6-26_wk04）

### 1-1. regime / 大局

- regime: **Equities Down**
  - equities=down
  - volatility=normal
  - oil=slump
  - gold=off
  - crypto=weak
  - yields=rising
- wk03のNeutral / risk-on回帰から、株安・金利上昇方向へ反転。
- 主因として記載されたもの:
  - PCE 4.1%高止まり
  - Goolsbee hawkish 発言
  - Mag7メモリ/ストレージ価格転嫁懸念
  - 米イラン再エスカ
  - VIX 18.41で18超え、Add risk gate再閉鎖

### 1-2. 主要signal / tags

6-26 の時点Tで、今回照合対象として重要だった signal / risk は以下。

| 項目 | 時点Tの読み |
|---|---|
| `rate_hike_fear_pce_goolsbee_hawkish` | PCE高止まり＋FRB高官タカ派で利上げ警戒再点火。株一服・金/BTC逆相関を意識。 |
| `us_curve_2s10s_bear_flattening` | 2Y上昇・10Y低下でbear flattening。利上げ→景気悪化を債券が織り込み始めたサイン。 |
| `mag7_memory_cost_passthrough_selloff` | メモリ価格転嫁懸念でMag7全面安、メモリ株は逆行高。 |
| `iran_reescalation_oil_geopolitical_repricing` | 地政学プレミアム再付与の初動。ただし供給回復ファンダ重しも併記。 |
| `vix_gate_reclosed` | VIX 18.41でAdd risk gate再閉鎖。18近傍の終値定着確認が必要。 |
| `usdjpy_range_162_intervention_watch_continued` | USDJPY 160後半〜162台レンジ。「上がったら売る」。162.20〜162.50上値メド。介入/協調レートチェックで155方向の非対称。 |
| `gold_bottom_zone_buy_dip_vs_machine_off` | 機械=gold off だが boss=大底圏押し目買い。$4,060維持が持越し根拠。 |
| `btc_downtrend_china_quantum_crack` | BTCは売り継続。56,869割れ→56,000。利上げ警戒＋暗号解読懸念。 |
| `nas100_range_break_down_bias` | US100は日足やや下目線。28,957割れ→28,600。29,626超えなら限定上昇のみ逆張り。 |
| `risk:carry_unwind_simultaneous_riskoff_2024_aug` | 円キャリー巻き戻しでNikkei/Nasdaq/BTC同時リスクオフを警戒。 |

### 1-3. 時点Tの主要 close / level

| asset | 6-26 close / level | 時点Tの読み |
|---|---:|---|
| US100 | 29,118.240 | 28,957割れ→28,600下抜け想定。29,626超えなら限定上昇。 |
| USDJPY | 161.805 | 162.20〜162.50上値メド。介入/協調なら155方向。 |
| XAUUSD | 4,078.700 | 週足Fibo38.2 $4,060上。終値割れで撤退根拠崩壊。 |
| WTI | 69.230 | 地政学反発 vs 供給回復ファンダ重し。 |
| VIX | 18.410 | Add risk gate再閉鎖。18超え定着確認。 |
| BTC | 59,721.676 | 戻り売り継続。56,869割れ→56,000。 |
| US2Y / US10Y | 4.225 / 4.451 | 2s10s +22.6bp、bear flattening。 |

---

## 2. outcome（Stage 2-A base + Stage 2-B theme署名）

## 2-A. base層: 6-26 close vs 7-3 close

| asset | 6-26 close | 7-3 close | 変化 | 照合 |
|---|---:|---:|---:|---|
| US100 | 29,118.240 | 29,329.211 | +210.971 / +0.72% | 下抜け想定は **not_confirmed_on_weekly_close**。28,957割れは週次closeでは未確認。むしろ小反発。 |
| USDJPY | 161.805 | 161.337 | -0.468 / -0.29% | 円高方向は小幅に出たが、155方向・159.5割れ級のflashは **not_confirmed_on_weekly_close**。 |
| XAUUSD | 4,078.700 | 4,187.300 | +108.600 / +2.66% | $4,060 close割れは確認されず。金の押し目買い/持越し根拠は1週後closeでは維持。 |
| WTI | 69.230 | 68.780 | -0.450 / -0.65% | 方向は小幅下。地政学反発より供給回復/上値重し側が優勢に見えるが、1週closeのみで深い判定は不可。 |
| US2Y | 4.225 | 4.130 | -0.095 / -2.25% | 2Y低下。6-26の利上げ警戒持続とは逆方向。 |
| US10Y | 4.451 | 4.372 | -0.079 / -1.77% | 10Yも低下。7-3は yields falling / bull flattening 文脈へ移行。 |
| 2s10s | +22.6bp | +24.2bp | +1.6bp | bear flattening継続ではなく、7-3では bull flattening / 長期低下主導として記録。 |
| VIX | 18.410 | 16.150 | -2.260 / -12.28% | Add risk gate は再開。6-26の再閉鎖は1週後に解消。 |
| BTC | 59,721.676 | 61,485.301 | +1,763.625 / +2.95% | 56,869割れ→56,000は週次closeでは未確認。小反発。 |

### 2-A summary

- 1週後の週次closeだけで見ると、6-26の **Equities Down / risk-off continuation** は継続せず、7-3は小反発・VIX低下・金利低下に移った。
- US100 / BTC は下方向を継続せず反発。
- USDJPY は小幅円高だが、深い介入flashや155方向の展開は確認できない。
- Gold は$4,060を終値で割らず、押し目買い/持越し根拠は1週後close上は維持。
- ただし、intradayのヒゲ・flash深度・日中同時性は distilled close だけでは見えないため、該当項目は `unverified` を残す。

### 2-A YAML-style facts

```yaml
outcome_facts:
  verification_window: one_week_only
  levels_stated:
    US100_down_trigger: 28957
    US100_limited_up_trigger: 29626
    USDJPY_upper_zone: 162.20-162.50
    USDJPY_deep_intervention_targets: [159.5, 156, 155]
    gold_floor_close: 4060
    btc_down_trigger: 56869
    VIX_gate: 18
  level_events:
    - asset: US100
      level: 28957
      weekly_close_pierced: false
      evidence: "7-3 close 29329.211 > 28957"
      intraday_pierce: unverified
      required_data: "daily/intraday OHLC for 2026-06-27..2026-07-03"
    - asset: USDJPY
      level: 162.20-162.50
      weekly_close_pierced: false
      evidence: "7-3 close 161.337 < 162.20"
      intraday_pierce: unverified
      required_data: "daily/intraday USDJPY high/low"
    - asset: USDJPY
      level: 159.5
      weekly_close_pierced: false
      evidence: "7-3 close 161.337 > 159.5"
      intraday_pierce: unverified
      required_data: "daily/intraday USDJPY low"
    - asset: XAUUSD
      level: 4060
      weekly_close_pierced: false
      evidence: "7-3 close 4187.300 > 4060"
      intraday_pierce: unverified
      required_data: "daily/intraday XAUUSD low/close"
    - asset: BTC
      level: 56869
      weekly_close_pierced: false
      evidence: "7-3 close 61485.301 > 56869"
      intraday_pierce: unverified
      required_data: "daily/intraday BTC low"
  next_1w_direction:
    US100: up_small
    USDJPY: yen_strengthening_small
    XAUUSD: up
    WTI: down_small
    VIX: down_gate_reopened
    BTC: up
    yields: down
  next_4w_direction: unverified
  trap_candidate: unverified
  trap_reason: "週次closeのみでは pierce/reclaim と event proximity を検出不可"
```

---

## 2-B. theme署名

### 2-B-1. yen_carry_unwind

#### 判定条件との照合

`yen_carry_unwind` の判定条件:

1. USDJPYの急速な円高
2. 同時にリスク資産が下落（US100 / BTC / 半導体など）
3. 引き金がJPY要因に帰せる

| condition | 6-26 -> 7-3 evidence | 判定 |
|---|---|---|
| 1. USDJPY急速円高 | 週次closeでは 161.805 -> 161.337、-0.468円の小幅円高。数円規模ではない。7-3本文には「3つの円高材料で急速円高続伸」とあるが、週次closeだけでは深度・日中速度は見えない。 | `partial_on_narrative / not_confirmed_on_weekly_close` |
| 2. リスク資産同時安 | US100 +0.72%、BTC +2.95%。週次closeでは同時安なし。半導体個別は弱いが、US100全体とBTCは反発。 | `false_on_weekly_close` |
| 3. JPY要因が主語 | 7-3でUSDJPYの円高材料は確認できる。ただし株安主因は韓国発半導体AI個別材料であり、JPY/carryが株安主語とは確認できない。 | `not_confirmed_for_cross_asset_driver` |

#### theme_outcome

```yaml
theme_outcome:
  yen_carry_unwind:
    cross_asset_simultaneous: false_on_weekly_close
    fired_or_latent: latent_on_1w_close
    confidence: medium
    caveat: "intraday同時性は未確認。週次closeでは円高×US100/BTC同時安が出ていない。"
    required_data:
      - "USDJPY daily/intraday OHLC"
      - "US100 daily/intraday OHLC"
      - "BTC daily/intraday OHLC"
      - "半導体指数または主要半導体銘柄の日次推移"
      - "event timestamp: Reuters介入報道 / BOJ利上げ継続要求報道"
```

#### 所見

6-26の `risk:carry_unwind_simultaneous_riskoff_2024_aug` は、1週後のcloseでは **firedではなくlatent**。ただし、7-3本文で「円キャリー巻き戻しがNASDAQ・半導体・cryptoの共通トリガーとして警戒」と再び記載されているため、**地雷としては生存**。発火確認ではなく、待機継続と見るのが安全。

### 2-B-2. jpy_policy_complex / 介入面

| item | 6-26 -> 7-3 evidence | 判定 |
|---|---|---|
| USDJPY上値162.20〜162.50到達 | 7-3 weekly close 161.337。closeでは未到達。 | `not_confirmed_on_weekly_close` |
| 深い円買いflash / 155方向 | 7-3 weekly close 161.337。159.5 / 156 / 155 はcloseで未達。 | `not_confirmed_on_weekly_close` |
| 介入実施 | 7-3本文は「3つの円高材料が重なり**介入なしで**急速円高続伸」と明記。 | `not_confirmed / no_intervention_in_source` |
| 覆面介入/サプライズ円買いリスク | 7-3でもtrap_watchとして継続。 | `risk_persisted` |

```yaml
theme_outcome:
  intervention:
    flash_occurred: not_confirmed_on_available_sources
    flash_depth: unverified
    weekly_close_deep_yen_strengthening: false
    source_note: "7-3 distilled/prediction_seed は介入なしの円高材料を記載。覆面介入リスクは継続監視。"
    required_data:
      - "USDJPY intraday high/low around 2026-06-27..2026-07-03"
      - "official intervention/rate-check confirmation"
      - "NY Fed rate check / coordinated intervention evidence if any"
```

#### 所見

6-26の介入面は **firedではない**。ただし6-19よりも6-26では「IMF残弾1発」「片山-ベッセント会談」「協調rate checkなら深い」という構造論が追加されており、7-3でも「財務省サプライズ介入も辞さない姿勢示唆」「覆面介入リスク」は残っている。よって、介入面は **latent / pressure_persisted**。

### 2-B-3. 6-26株安の駆動: JPYか別要因か

#### 6-26時点T

6-26の株安駆動として本文に明記されたもの:

- PCE 4.1%高止まり
- Goolsbee hawkish
- Mag7メモリ価格転嫁懸念
- イラン再エスカ
- VIX 18超え再閉鎖
- bear flattening / 利上げ→景気悪化織り込み

JPY/carryは **同時リスクオフの警戒** として存在したが、6-26株安そのものの主語としては上記の米金利・Mag7・地政学の方が明示的。

#### 7-3 outcome

7-3では:

- 株安主因は雇用ではなく、韓国発の半導体AI個別材料。
- 雇用未達で利上げ観測やや後退。
- VIX 16.15でAdd risk gate再開。
- yields は falling / bull flattening。
- US100は週次小反発。
- 円キャリー巻き戻しは「最大の地雷 / 共通トリガー」として警戒されるが、実際の週次closeではUS100/BTC同時安なし。

#### 判定

```yaml
driver_attribution:
  6_26_equities_down_driver:
    jpy_as_primary_driver: not_confirmed
    confirmed_drivers_in_source:
      - PCE/Goolsbee hawkish rate_hike_fear
      - Mag7 memory cost passthrough
      - Iran re-escalation/geopolitical repricing
      - VIX gate reclosed
    carry_unwind_role: risk_scenario_not_confirmed_as_driver
  7_3_followup_driver:
    primary_stock_driver: korea_semi_ai_selloff_not_jobs
    jpy_role: USDJPY pressure / latent cross_asset_trigger
    carry_unwind_fired: false_on_weekly_close
```

---

## 3. Stage 3判定（差分一行つき）

### 3-1. classification draft

```yaml
stage_3_classification:
  primary_label: A_regime_misread_partial_1w
  theme_labels:
    jpy_policy_complex: latent_pressure_persisted
    yen_carry_unwind: latent_on_1w_close
  secondary_labels:
    B_timing: unverified_4w_window_missing
    C_swept: unverified_no_intraday_pierce_reclaim_data
    D_lucky: not_applicable
  confidence: medium
```

### 3-2. 判定本文

- **A_regime_misread_partial_1w**:
  - 6-26の `Equities Down` / VIX gate再閉鎖 / NAS100下抜け寄り / BTC戻り売りの1週継続は、7-3 closeでは確認されなかった。
  - 7-3は US100 +0.72%、BTC +2.95%、VIX 18.41 -> 16.15、US2Y/US10Y低下で、risk-off continuation より risk easing / driver swap に近い。
  - ただし1週窓のみで、4週先は未確認。したがって `partial_1w` とする。

- **jpy_policy_complex: latent_pressure_persisted**:
  - USDJPYは小幅円高になり、7-3でも介入/覆面介入リスクは残った。
  - しかし週次closeでは162.20〜162.50到達も、159.5/156/155方向の深い円高も確認できない。
  - 7-3資料は「介入なしで急速円高」と記載しているため、実弾介入発火ではない。

- **yen_carry_unwind: latent_on_1w_close**:
  - 週次closeでは USDJPY小幅円高と同時に US100/BTC が上昇しており、条件2の「リスク資産同時安」は成立しない。
  - 7-3株安主因は半導体AI個別材料で、JPY/carryがクロス資産売りの主語だったとは確認できない。

- **B_timing: unverified**:
  - 4週窓が未取得のため、「読みは合っていたが時間軸がズレただけ」とはまだ言えない。

- **C_swept: unverified**:
  - 週次closeでは pierce/reclaim を検出できない。intraday OHLCが必要。

- **D_lucky: not_applicable**:
  - 結果的中と呼べる主要方向がない。USDJPY小幅円高だけを「介入/carry thesis的中」と扱うと、carry条件2/3を無視した物語化になる。

### 3-3. 当時見えていなかった差分（一行）

6-26時点では PCE/Goolsbee・Mag7メモリ・地政学による risk-off 継続を重く見たが、7-3では雇用未達で金利圧力が後退し、VIX<18へ再開、株安主因も韓国発半導体AI個別材料へ入れ替わった。

---

## 4. 設計フィードバック（所見）

### 4-1. 節点は入口として効いたか

- `jpy_policy_complex` は効いた。
  - 6-26の介入・協調rate check・BOJ/円高圧力・carry連想を一つの入口で拾えた。
  - ただし今回の照合では、介入面とcarry面を分けて latent 判定する必要があった。

- `yen_carry_unwind` は非常に効いた。
  - 条件2「リスク資産同時安」と条件3「円が主語」があるため、6-26→7-3を **firedではなくlatent** と切り分けられた。
  - この条件がなければ、「USDJPYが少し円高 + 半導体弱い」だけでcarry発火と誤読しやすい。

- `same_news_bear_bull_timeframe_split` は6-26照合の主対象ではないが、7-3のdriver swap理解には有用だった。
  - 6-26のMag7メモリ/半導体弱気から、7-3のAnthropic×Samsung短期弱気/中期強気へ、AI半導体材料の時間軸分裂を読む補助になった。

### 4-2. retrievalで困った所

- `regime/Equities_Down` が未整備のため、Equities Downが「RiskOff」とどう違うかを毎回 distilled 本文から読まなければならなかった。
- `system/vix_add_risk_gate` が未整備のため、VIX 18超え/割れの outcome を横断照合しづらい。
- `instrument/us100_levels` が未整備のため、28,957 / 29,626 / 29,089 などの節目の系譜を手で追う必要があった。
- `themes/ai_semi` が未整備のため、6-26のMag7メモリ転嫁と7-3の韓国発半導体AI材料の関係を、indexではなく本文読解で繋いだ。
- intraday OHLC がないため、C_swept / flash / sweep&reclaim はほぼ unverified になる。

### 4-3. 欲しかったノード

1. `regime/Equities_Down.md`
2. `system/vix_add_risk_gate.md`
3. `instruments/us100_levels.md`
4. `themes/ai_semi.md`
5. `patterns/thin_liquidity_flash_trap.md`（ただしこれはintraday証拠が集まってから）

### 4-4. 照合層の要否

**必要。** 今回も、照合なしだと「6-26はcarry_unwind同時リスクオフ警戒週」として強い物語を作れる。しかし7-3 closeで確認すると、US100/BTCは上昇し、VIXは低下し、金利も低下している。outcome層がなければ、この差分が index に反映されない。

---

## 5. 自己監査

### 5-1. 未照合のまま残した箇所

- USDJPYの日中高値・安値、162.20〜162.50到達有無。
- 159.5割れ・156/155方向への intraday flash 有無。
- US100 28,957 や 29,626 の日中貫通/回収。
- Gold $4,060 の intraday割れ有無。
- BTC 56,869 の intraday割れ有無。
- 円高とUS100/BTC/半導体下落が同日・同時間帯に発生したか。
- 半導体個別銘柄の下落がJPY/carry要因だったか、韓国発AI材料だったかの細分。

### 5-2. 物語化しやすかった箇所

1. **USDJPYが小幅円高になったことを介入/carry thesis的中と見なす誘惑**
   - しかし、深いflashもリスク資産同時安も確認できないため、firedとは書かなかった。

2. **6-26の `carry_unwind_simultaneous_riskoff_2024_aug` タグからfiredを期待するバイアス**
   - タグはsetup/警戒であり、outcomeではない。7-3 closeではlatent。

3. **6-5 / 6-19 の latent連続に引きずられるバイアス**
   - 指示どおり、6-26単独証拠で見た。結論は同じくlatent寄りだが、理由は7-3 closeでUS100/BTC上昇・VIX低下・金利低下が確認されたため。

4. **7-3の半導体AI個別売りを6-26のMag7メモリ売りと同一視する誘惑**
   - どちらもAI/半導体弱気だが、6-26はコスト転嫁/インフレ連鎖、7-3は韓国発AIチップ競合/アルゴ規制。driverが違うため同一視しなかった。

5. **C_sweptを付けたくなる箇所**
   - 薄商い・介入・節目があるためtrap候補に見えるが、pierce/reclaim証拠がない。`unverified` とした。

---

## 6. 結論

### 一行判定

2026-6-26_wk04 は、1週後の7-3 closeで見る限り、`Equities Down` 継続・JPY/carry発火ではなく、**risk-off continuation の1w未達 + jpy_policy/carry は latent / pressure persisted**。

### Broker向け要約

- `yen_carry_unwind`: **latent_on_1w_close**。USDJPY小幅円高はあるが、US100/BTCは上昇し、条件2の同時リスク資産安が成立しない。
- `jpy_policy_complex`: **latent_pressure_persisted**。介入/覆面介入リスクは7-3でも残るが、実弾介入・深いflashは資料上not_confirmed。
- Stage 3: **A_regime_misread_partial_1w**。ただし4週窓は未確認のため、B_timingはunverified。
- C_swept: intraday不足でunverified。
- D_lucky: not_applicable。
