---
type: outcome_record
status: draft
week: 2026-6-19_wk03
task: outcome_verification_6-19_strict
engine: codex-5.5
created: 2026-07-06
source:
  - "distilled/2026/distilled-gm-2026-6.md#2026-6-19_wk03"
verified_against:
  - "distilled/2026/distilled-gm-2026-6.md#2026-6-26_wk04"
  - "distilled/2026/distilled-gm-2026-7.md#2026-7-3_wk01"
index_nodes_read:
  - "bridges/trade_brain/index/README.md"
  - "bridges/trade_brain/index/themes/jpy_policy_complex.md"
  - "bridges/trade_brain/index/themes/yen_carry_unwind.md"
  - "bridges/trade_brain/index/patterns/same_news_bear_bull_timeframe_split.md"
tags: [trade_brain, outcome, backfill_v1, jpy_policy_complex, intervention, carry_unwind, strict]
---

# 2026-6-19_wk03 reverse lookup strict — outcome_record

## 1. 時点Tの読み

2026-6-19_wk03 の主軸は、ダブル中銀通過後のリスクオン回帰を認めつつ、**新キングピンを USDJPY 161.80 介入警戒へ移した週**だった。

- regime: Neutral（equities=up / volatility=normal / oil=slump / gold=off / crypto=weak / yields=falling）。wk01 のリスクオフ・whipsaw から、6/16-17 ダブル中銀通過＋米イラン停戦/ホルムズ再開でリスクオン回帰。
- 主要 signal:
  - `usdjpy_intervention_watch_new_kingpin=on`: 早朝 161.68-161.83（約161.80）ピークが 2024/4/29 介入直前水準に近い。162 一段上げからの急落（ズドン）リスク、買い上がりはバイングクライマックス警戒。
  - `yen_intervention_flash_cascade` / `risk:yen_intervention_flash_cascade`: 実弾介入・レートチェックに伴う円高 flash を警戒。
  - `us_jp_rate_divergence_yen_pressure=on`: 日米金利差縮小方向が円高圧力と整合。
  - `nas100_cup_handle_range_30900_short=watch`: US100 はリスクオン回帰しつつ 30,900 周辺を火傷ゾーンとして短期逆張り。
- 記載レベル:
  - USDJPY: close 161.289、早朝ピーク約161.80。162 一段上げから急落リスク。159.5 割れで巻き戻し → 156 → 155。
  - US100: close 30,406。30,900 周辺で一旦の下落を利用する短期逆張り。
  - JP225: 71,053.49、72,800-73,000 青丸危険ゾーン。
  - VIX: 16.4、Add risk gate 再開。ただし介入警戒による突発スパイク余地。

## 2. outcome（Stage 2-A base ＋ 2-B theme署名・照合結果）

### Stage 2-A base層（後続週 close）

| 資産/指標 | 6-19_wk03 時点T | 6-26_wk04 outcome | 7-3_wk01 outcome | 照合 |
|---|---:|---:|---:|---|
| USDJPY | 161.289（早朝ピーク約161.80） | 161.805 | 161.337 | 162 近傍高止まりは継続。7-3 は円高方向だが 159.5 割れなし、156/155 方向の深い巻き戻しなし。 |
| US100 | 30,406.189 | 29,118.240 | 29,329.211 | 6-26 に -4.2% 下落。30,900 火傷ゾーン/短期下落警戒は結果方向としては有効。ただし主因は介入でなく PCE・Goolsbee・Mag7 メモリ転嫁・イラン再エスカ。 |
| BTC/USD | 62,896.473 | 59,721.676 | 61,485.301 | 6-26 に下落、7-3 に反発。円高同時発火ではなく、BTC 独自弱材料・利上げ警戒・量子/暗号解読懸念が主因として記載。 |
| VIX | 16.400 | 18.410 | 16.150 | 6-26 に Add risk gate 再閉鎖、7-3 に再開。ボラ上昇は起きたが、介入 flash 主導ではない。 |
| regime | Neutral / equities=up | Equities Down | Equities Down（内部品質は小反発＋VIX低下） | wk04 は risk-on 回帰から反転。方向警戒は有効だが driver は別。 |

記載レベル照合:

- USDJPY 161.80: 6-26 close 161.805 で高値圏は維持。これは「介入警戒ゾーンにいた」事実を補強するが、**実際の深い円高 flash ではない**。
- USDJPY 162 一段上げ: 6-26 に 160後半〜162レンジ・162.20-162.50上値メド継続と記載されたが、後続 close では 162 明確上抜けは確認できない。
- USDJPY 159.5 → 156 → 155: 6-26 / 7-3 close では未到達。7-3 に「介入なしで急速円高続伸」はあるが、close は 161.337 で深度不足。
- US100 30,900 short/watch: 6-26 close 29,118 へ下落し、結果方向は合致。ただし driver は USDJPY介入ではなく米PCE・Fed高官・Mag7メモリ転嫁・イラン再エスカ。
- VIX>18: 6-26 に 18.41 で再閉鎖。これは risk 管理面では有効な後続確認。

### Stage 2-B theme署名

#### jpy_policy_complex / 介入面（主役）

```yaml
intervention:
  flash_occurred: false
  flash_depth: null
  partial_pressure_observed: true
  evidence:
    - "6-26 USDJPY close 161.805: 161.80高値圏に滞在し介入警戒継続"
    - "7-3 USDJPY close 161.337: wk04比-0.468の円高。本文は『介入なしで急速円高続伸』と記載"
    - "ただし159.5割れ・156/155方向・実弾介入flashは確認されない"
```

判定: **介入面は latent / shallow pressure**。時点Tの「介入警戒ゾーン」という入口は効いたが、指示書の主軸である「162 一段上げからの急落」「159.5割れ→156→155」は、6-26 / 7-3 close では未発生。

#### yen_carry_unwind

```yaml
yen_carry_unwind:
  cross_asset_simultaneous: false
  fired_or_latent: latent
  condition_2_simultaneity: false
  condition_3_jpy_as_subject: false
  evidence:
    - "6-26: US100/BTCは下落したが、USDJPYは161.289→161.805で円安。円高×リスク資産同時安ではない"
    - "6-26 driverはPCE4.1%、Goolsbee hawkish、Mag7 memory cost、Iran re-escalation"
    - "7-3: USDJPYは161.805→161.337へ円高だが、US100は+0.7%、BTCは+3.0%、VIXは18.41→16.15でrisk-on寄りに改善"
```

切り分け:

- 条件2（同時性）: 不成立。6-26 はリスク資産安だが円高でなく、7-3 は円高だがリスク資産同時安でない。
- 条件3（円が主語）: 不成立。6-26 の下落主因は米インフレ/Fed/メモリ/地政学であり、JPY 要因ではない。
- outcome: **latent**。6-5 と同様、setup/警戒はあっても fired ではない。

#### same_news_bear_bull_timeframe_split

6-19 の主対象ではないが、7-3 outcome では `Anthropic×Samsung` 材料に対して短期弱気（boss）と中期強気（X市況）が分裂しており、index pattern は有効に読める。ただしこれは 6-19 の介入/carry outcome 判定の主証拠ではなく、7-3 の equities down 内部品質を説明する補助文脈に留める。

## 3. Stage 3判定（差分一行つき）

```yaml
stage_3:
  labels:
    - A_regime_misread
    - B_timing
    - D_lucky
  not_label:
    - C_swept
  summary: "介入警戒ゾーンという入口は正しかったが、実際の後続下落/ボラ復元はJPY介入・carry_unwindではなく、PCE/Fed・Mag7メモリ・イラン再エスカ主導。US100下落警戒は結果方向だけ当たり、主因は外れ。"
  unseen_difference: "当時見えていなかった差分は、161-162高値圏が即flashを生むのではなく、介入残弾/協調レートチェックの非対称を抱えたまま、先に米インフレ・メモリ・地政学がrisk-offを駆動したこと。"
```

判定理由:

- **A_regime_misread**: 6-19 の regime は「リスクオン回帰＋介入警戒の綱引き」だったが、6-26 の Equities Down は主に PCE/Goolsbee・Mag7メモリ・イラン再エスカで発生。介入/carry を主役に置いた driver 読みは外れ。
- **B_timing**: USDJPY 161-162 の介入警戒自体は後続週でも継続し、7-3 には「介入なし急速円高続伸」「覆面介入リスク」が残った。しかし深い 159.5→156→155 はこの照合窓では未発火。
- **D_lucky**: US100 30,900 火傷ゾーン・上値追い厳禁・VIX再上昇注意は、6-26 の US100 下落/VIX18超えという結果方向に合った。ただし的中理由は介入 flash/carry_unwind ではない。
- **C_swept ではない**: 162 上抜け後の明確な pierce + reclaim、または介入 flash による罠狩りの証拠が、与えられた close ベース資料にはない。

## 4. 設計フィードバック（所見）

### 節点は入口として効いたか

- `jpy_policy_complex`: **効いた**。6-19 は典型的に介入面・BOJ経路・carry 伝達帯を同時に読むべき週で、USDJPY 161.80 を入口に後続 6-26 / 7-3 の非対称管理まで追えた。
- `yen_carry_unwind`: **強く効いた**。条件2（円高×リスク資産同時安）と条件3（円が主語）で、6-26 の risk-off を carry_unwind と誤認せずに済んだ。これは物語化防止に有効。
- 介入面: **入口としては効いたが outcome 層が必要**。161-162 高値圏滞在だけでは fired とは呼べない。`flash_occurred` と `partial_pressure_observed` を分ける必要がある。
- `same_news_bear_bull_timeframe_split`: 6-19 照合の主軸ではないが、7-3 の株安内部品質（短期弱気 vs 中期強気）を読む補助線としては有効。

### retrieval で困った所

- 「flash」の深度定義が close 資料だけでは薄い。指示書は close 照合を指定しているが、介入 flash は intraday のヒゲ・分足で起きるため、close だけだと発生/不発の判定が粗い。
- JP225 の 6-26 close 実測が snapshot8ペア外で欠落。6-19 の青丸 72,800-73,000 照合は厳密には未完。
- 6-19 から 7-3 にかけて「介入なし急速円高続伸」とあるが、何円幅・どの時間窓かが distilled の close だけでは確定できない。

### 欲しかったのに無いノード

- `mof_intervention_flash_outcome` または `thin_liquidity_intervention_flash_trap`: 介入面について、価格水準だけでなく「発生時刻・薄商い・ヒゲ深度・回収」を判定する outcome ノード。
- `us_inflation_fed_repricing_riskoff`: 6-26 の本当の下落 driver（PCE/Goolsbee/Fed再利上げ警戒）を carry_unwind と切り分けるための rates/Fed 系ノード。
- `memory_cost_mag7_selloff`: 6-26 の Mag7 メモリ転嫁株安を ai_semi 側で切るノード。

### 照合層の要否

必要。6-19 は setup だけ読むと「161.80介入警戒→risk-off」の物語が非常に作りやすいが、outcome では **risk-off は来たが JPY 主語ではなかった**。Stage 2-B の theme署名がなければ、6-26 を carry_unwind fired と誤登録する危険が高い。

## 5. 自己監査

- 未照合: intraday の USDJPY 高値・安値・ヒゲ深度、162.20-162.50 への実到達、159.5 割れの intraday 有無は、distilled の close ベース資料だけでは検証していない。
- 未照合: JP225 の 6-26 close が資料内にないため、72,800-73,000 青丸拒否の成否は判定していない。
- 薄い根拠: 7-3 の「介入なし急速円高続伸」を partial pressure と呼んだが、これは本文記述と close 差分（161.805→161.337）に基づく補助判定であり、flash 判定ではない。
- アナロジー抑制: 2024/4介入直前水準・2024/8 carry_unwind replay は時点Tの読みとして記録したが、outcome 判定には使わず、6-26 / 7-3 の実記載に限定した。
- 物語化リスク: US100下落と USDJPY高値圏を結びつけると carry_unwind に見えるが、条件2/3により不成立とした。
