---
type: outcome_record
status: draft
week: 2026-6-19_wk03
task: outcome_verification_6-19
engine: codex-5.5
created: 2026-07-06-1532
source: distilled/2026/distilled-gm-2026-6.md#2026-6-19_wk03
verified_against:
  - distilled/2026/distilled-gm-2026-6.md#2026-6-26_wk04
  - distilled/2026/distilled-gm-2026-7.md#2026-7-3_wk01
index_nodes_read:
  - bridges/trade_brain/index/README.md
  - bridges/trade_brain/index/themes/jpy_policy_complex.md
  - bridges/trade_brain/index/themes/yen_carry_unwind.md
  - bridges/trade_brain/index/patterns/same_news_bear_bull_timeframe_split.md
stage: backfill_v1_stage_2_3
tags: [trade_brain, outcome, reverse_lookup, jpy_policy_complex, yen_carry_unwind, intervention]
---

# 2026-6-19_wk03 outcome 照合（reverse lookup std）

## 1. 時点Tの読み

### regime / posture
- 2026-6-19_wk03 は `Neutral`。wk01 の NFP 起点リスクオフ・whipsaw から、6/16-17 ダブル中銀通過＋米イラン停戦/ホルムズ再開でリスクオン回帰。
- VIX は 21.51 → 16.40 へ低下し `Add risk gate` 再開。
- ただし最大リスクは USDJPY 161.80 近辺の介入警戒。リスクオン回帰の中で、JPY政策複合だけが上値追いを止めるキングピンとして残った週。

### 主要 signal
- `usdjpy_intervention_watch_new_kingpin=on`
  - USDJPY 早朝ピーク約 161.68-161.83（約161.80）。2024/4/29 介入直前水準とほぼ同水準。
  - 「いつ介入が入ってもおかしくない」ゾーン。
  - 162 一段上げからの急落（ズドン）リスク。
  - 買い上がりはバイングクライマックス警戒。
  - 159.5 割れで巻き戻し開始 → 156 → 155。
- `us_jp_rate_divergence_yen_pressure=on`
  - US10Y は 4.6% が重く、JP10Y は上昇トレンド継続。日米金利差縮小＝円高圧力。
- `risk:yen_intervention_flash_cascade`
  - 介入・レートチェック起点の円高 flash が、クロス円/日本株/リスク資産へ伝播するリスク。

### 記載レベル
| 対象 | 時点T記載 |
|---|---|
| USDJPY close | 161.289 |
| USDJPY peak / kingpin | 約161.80（2024/4介入直前水準） |
| 上値想定 | 162 一段上げからの急落リスク |
| 下値トリガー | 159.5 割れで巻き戻し開始 |
| 下値目標 | 156 → 155 |
| 関連リスク | 介入/レートチェックによる円高 flash cascade |

## 2. outcome（Stage 2-A base ＋ 2-B theme署名・照合結果）

### Stage 2-A base層: 記載レベル vs 後続実価格

| 資産/指標 | 6-19_wk03 close | 6-26_wk04 close | 7-3_wk01 close | 方向 | 照合 |
|---|---:|---:|---:|---|---|
| USDJPY | 161.289 | 161.805 | 161.337 | 1週後は円安、2週後はほぼ横ばい/小幅円高 | 159.5割れ・156/155到達なし。深い円高 flash は未発生 |
| US100 | 30,406.189 | 29,118.240 | 29,329.211 | 1週後 -4.2%、2週後小反発 | 株安は出たが主因は PCE/グールズビー/メモリ転嫁/イランで JPY主語ではない |
| BTC/USD | 62,896.473 | 59,721.676 | 61,485.301 | 1週後下落、2週後小反発 | 6-26は下落したが円高同時性なし。7-3は反発 |
| VIX | 16.400 | 18.410 | 16.150 | 18超え再閉鎖後、18割れ再開 | 6-26にリスクオフ寄り、7-3に再沈静 |
| US10Y | 4.487 | 4.451 | 4.372 | 低下継続 | 4.6%上抜けではなく、長期金利は重い |

#### USDJPY レベル照合
- 6-19 の主要警戒水準 161.80 は、翌週 6-26 close 161.805 として維持/小幅上抜け扱い。ただし distilled 上で実弾介入や急落 flash の記録はない。
- 6-26 では `160後半〜162円台のレンジ`、`162.20-162.50上値メド`、`上がったら売る` が継続。介入警戒は残存したが、価格は 159.5 を割らず、156/155 方向の深い回収もなし。
- 7-3 では USDJPY 161.337。wk04比 -0.468 の円高で、本文には「木曜3円高材料」「介入なしで急速円高続伸」とある。ただし weekly close では 6-19 比 +0.048 とほぼ横ばいで、6-19 が想定した 159.5割れ→156→155 の深度には届いていない。
- よって base層判定は「方向リスクは残存/一部顕在化、深度とブレイク条件は未達」。

### Stage 2-B theme署名: jpy_policy_complex / 介入面

```yaml
theme_outcome:
  intervention:
    flash_occurred: false_or_unverified
    flash_depth: null
    level_16180_retested_or_held: true
    level_1595_break: false
    targets_156_155_reached: false
    notes:
      - 6-26 close 161.805で161.80近辺を維持。実弾介入/急落flashの記録なし。
      - 7-3は介入なし急速円高続伸の記載があるが、weekly closeは161.337で159.5割れ未達。
      - Reuters/財務省姿勢/日銀利上げ継続要求など、介入警戒を補強する新材料は後続で出た。
```

- 介入面は **不発寄りの latent**。161.80 という入口節点は後続週でも有効だったが、6-19 時点で警戒した「162一段上げからのズドン」「159.5割れ→156→155」は、6-26/7-3 close ベースでは確認できない。
- ただし 7-3 には「介入なしで急速円高続伸」「薄商いで覆面介入リスク増幅」があり、介入警戒テーマそのものは消えず、むしろ後続材料で補強された。

### Stage 2-B theme署名: yen_carry_unwind

```yaml
theme_outcome:
  yen_carry_unwind:
    cross_asset_simultaneous: false
    fired_or_latent: latent
    condition_2_simultaneity: false
    condition_3_jpy_as_subject: false
    notes:
      - 6-26にUS100/BTC/VIX悪化は出たが、USDJPYは161.805へ円安維持。円高×リスク資産同時安ではない。
      - 6-26の駆動はPCE4.1%、グールズビー・タカ派、Mag7メモリ転嫁、米イラン再エスカ。
      - 7-3はUSDJPYが小幅円高でもUS100/BTCは小反発、VIXも16.15へ低下。risk-off同時性なし。
```

- 6-26 は `Equities Down` で、表面上は risk-off だが、JPY が主語ではない。
- carry_unwind ノード判定条件2「同時にリスク資産が下落」と条件3「引き金がJPY要因」を同時に満たさない。
- したがって 6-19 の `yen_intervention_flash_cascade` は、後続2週の実挙動では **fired ではなく latent**。

### Stage 2-B 補足: same_news_bear_bull_timeframe_split
- 6-19照合の主対象ではないが、7-3では Anthropic×Samsung をめぐる `same_news_bear_bull_timeframe_split` が発火。
- これはJPY介入面とは別ノードで、6-26/7-3の株安・半導体材料を JPY主語の carry_unwind と誤結合しないための切り分け材料として効いた。

## 3. Stage 3判定（差分一行つき）

### 判定
- label: **B_timing / latent（介入面）** ＋ **A_regime_misread_partial（carry_unwind伝達の外挿部分）**
- C_swept: **なし**。159.5割れ→回収の sweep、または介入flash後のreclaim は、提供ソース内で確認できない。
- D_lucky: **なし**。6-26の株安は結果だけ見ると「リスクオフ警戒が当たった」ように見えるが、駆動がJPYではないため lucky 的中として採用しない。むしろ「同じ下落でも主語が違う」事例。

### 理由
- 介入警戒そのものは正しい入口だった。161.80は後続 6-26 でも維持され、6-26には片山-ベッセント会談/IMF残弾/協調レートチェック非対称性、7-3には財務省サプライズ介入姿勢報道など、後続材料が追加された。
- しかし、6-19時点で想定された深い円高 flash（159.5割れ→156→155）は少なくとも 6-26/7-3 close では発生していない。
- 6-26 のリスク資産下落を carry_unwind と読むのは誤り。USDJPYは円安高値圏で、駆動は米インフレ/利上げ警戒/メモリ/地政学。yen_carry_unwind 条件2・3に不合格。

### 当時見えていなかった差分（一行）
6-19時点では「161.80＝即flash」の非対称を重く見たが、後続で見えた差分は **実弾介入ではなく、IMF残弾1発・片山-ベッセント会談・財務省サプライズ介入姿勢報道が、161-162レンジを長く踏ませながら警戒だけを増幅する構造** だった。

## 4. 設計フィードバック（所見）

### 節点は入口として効いたか
- `jpy_policy_complex`: 効いた。介入面だけでなく、BOJ/日米金利差/協調レートチェック/残弾という政策複合に自然に広がった。6-19→6-26→7-3の連続性を読む入口として有効。
- `yen_carry_unwind`: 効いた。6-26の株安を「円キャリー巻き戻し」と誤認しないため、条件2（同時性）と条件3（円が主語）が明確なフィルターになった。
- 介入面: 効いたが、現行 `jpy_policy_complex` 内の面だけだと、単独実弾介入・協調レートチェック・覆面介入/サプライズ姿勢報道の深度差がやや粗い。

### retrieval で困った所
- JP225の後続 close が 6-26 で snapshot8ペア外。日本株への伝播は定性的記載に依存し、carry_unwind の同時性を機械判定しにくい。
- 7-3本文に「木曜3円高材料」「介入なしで急速円高続伸」とあるが、週次 close だけでは intraday の flash 深度・高値からの下落幅を測れない。
- 6-19の「162一段上げからの急落」は、close照合だけだと発生/不発が荒くなる。高値・安値・時間帯つき足データが欲しい。

### 欲しかったのに無いノード
- `mof_intervention_flash` または `coordinated_rate_check_asymmetry`: 6-26で出た IMF残弾1発・片山-ベッセント会談・1月協調rate check 2,100pips のような「単独介入 vs 協調弾」の深度差を扱うサブノード。
- `thin_liquidity_intervention_flash_trap`: 米休場/薄商い/覆面介入/節目sweep をまとめる pattern。backfill v1にも候補として記載あり。
- `jp225_fx_adjusted_relative_strength`: 円安薄化粧と実質相対強度を切り分ける instrument/system 寄りノード。

### 照合層の要否
- 必要。6-26の equities down を、照合層なしで読むと 6-19の「介入flash cascadeが来た」と物語化できてしまう。
- 実際は USDJPY が円安高値圏のままで、risk-off主語は米PCE/利上げ警戒/メモリ/イラン。outcome署名がないと `risk:carry_unwind_simultaneous_riskoff_2024_aug` タグに引っ張られる。

## 5. 自己監査

- 未照合: intraday の USDJPY 高値・安値・急落幅は distilled の close と本文記述だけでは検証不能。`flash_occurred` は「提供ソース内では未確認/不発寄り」とし、断定的な tick 判定はしていない。
- 未照合: JP225の 6-26 close が snapshot8ペア外のため、円高×日本株下落の同時性は機械判定していない。
- 薄い根拠: 7-3の「介入なしで急速円高続伸」を 6-19の介入面の一部顕在化として扱ったが、週次 close では深度が浅く、実際の intraday 3円高の始点/終点は本文から完全復元できない。
- アナロジー抑制: 2024/4介入直前水準、2024/8 carry_unwind replay は参照されたが、後続実価格が条件未達のため fired とは書かなかった。
- ソース外情報: 外部ニュース・実価格は追加していない。distilled 6月/7月、index ノード、backfill v1、先行 specimen の範囲のみで照合した。
