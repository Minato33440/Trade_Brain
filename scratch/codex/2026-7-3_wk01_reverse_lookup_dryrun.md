---
type: reverse_lookup_dryrun_report
week: 2026-7-3_wk01
engine: codex-5.5
created: 2026-07-05
source_instruction: scratch/codex/instructions/reverse_lookup_dryrun.md
status: completed
scope: retrieval_observation_only
outcome_status: unverified_all
---

# index 逆引き 通し稽古 — 2026-7-3_wk01

## 0. 前提と制約

- 本レポートは retrieval と観測のみ。index ノード粒度の修正、canon/index/distilled への書込は行っていない。
- 参照した入口ノード:
  - `jpy_policy_complex`
  - `yen_carry_unwind`
  - `same_news_bear_bull_timeframe_split`
  - regime 文脈: `RiskOff` 近傍。ただし現週の機械regimeは `Equities Down`。
- 参照した現在状態:
  - `scratch/claude/2026-7-3_wk01_prediction_seed.md`
  - `distilled/2026/distilled-gm-2026-7.md` wk01
- 参照した主な過去週:
  - `distilled-gm-2026-6.md`: 6-5_wk01 / 6-19_wk03 / 6-26_wk04
  - `distilled-gm-2026-5.md`: 5-1_wk01 / 5-8_wk02
- 成否はすべて **未照合**。本稿では「当時の読み」と「現在との差分」だけを扱う。

---

## 1. 現在状態の同定（入口に使った node と根拠）

### 1-1. 現在の局面要約

2026-7-3_wk01 は、機械regime上は `Equities Down` だが、全面RiskOffというより、内部品質は以下の複合状態だった。

- 株安主因は雇用統計ではなく、韓国発の半導体AI個別材料。
- VIX は 16.15 で18割れ、Add risk gate は再開。
- US100は29,089を両義の節目とするトライアングルレンジ。
- USDJPYは3つの円高材料で急速円高したが、本流は円安トレンド継続。162.268上抜け監視。
- 米休場・薄商いにより、覆面介入/サプライズ円買いの trap_watch が立っている。
- 円キャリー巻き戻しが、NASDAQ・半導体・cryptoの共通トリガーとして警戒されている。
- Anthropic×Samsung AIチップ報道は、boss市況では短期弱気、X市況では中期強気に読まれた。

### 1-2. 入口に使った node

| node | 使った理由 | 根拠 |
|---|---|---|
| `jpy_policy_complex` | USDJPY 162近辺、介入警戒、BOJ利上げ継続要求報道、円キャリー巻き戻しが同時に出ているため | prediction_seed の USDJPY節、distilled 7月 wk01 の `us_holiday_thin_liquidity_covert_intervention_risk` |
| `yen_carry_unwind` | JPY要因がNASDAQ・半導体・cryptoの共通トリガーとして明示されているため | index nodeの7-3_wk01格上げ記述、distilled 7月 wk01 `risk:yen_carry_unwind_riskoff_trigger` |
| `same_news_bear_bull_timeframe_split` | Anthropic×Samsung AIチップ報道が短期弱気 / 中期強気に時間軸分裂しているため | distilled 7月 wk01 `x_sentiment_gold_ai_bull_jpy_bear` と pattern node 初出インスタンス |
| RiskOff近傍 | 機械regimeは Equities Down だが、介入flash・carry-unwind・US100節目割れ時の下落加速がRiskOff経路へ接続するため | 6-5 / 6-26 のRiskOff寄り週と照合 |

---

## 2. 引けた過去週と各々の当時の読み（成否＝未照合）

### 2-1. 2026-6-26_wk04 — 直近の介入警戒 / Equities Down / carry-unwind再演警戒

**成否: 未照合。**

当時の読み:

- regime は `Equities Down`。wk03のリスクオン回帰から、株安・金利上昇方向へ反転。
- ドル円は161.805、160後半〜162レンジ。「上がったら売る」が基本。
- 162.20〜162.50が上値メド。為替介入・レートチェックリスクが継続。
- 介入の非対称性が明示されていた。
  - IMF枠の残弾は1発。
  - 6/23片山-ベッセント会談が協調レートチェックの布石。
  - 協調弾が出たら155方向へ深く長いが、出る前は161〜162で踏まれる。
- `risk:carry_unwind_simultaneous_riskoff_2024_aug` が立っており、Nikkei / Nasdaq / BTC の同時リスクオフを警戒。
- US100は29,118で、日足やや下目線。28,957割れ→28,600の下抜け想定。
- BTCは利上げ警戒＋量子/暗号解読懸念で戻り売り。
- Goldは機械=offだがboss=大底圏買いで、金とBTCの分離が明示。

現在との接続:

- 現在もUSDJPYは161〜162台の介入警戒圏に近く、162.268が監視線。
- 現在も半導体/AI材料が株式の局所ドライバー。
- 現在もBTCはAIチップ/暗号解読連想で反発ロング見送り。
- 6-26は「利上げ警戒＋Mag7メモリ転嫁＋地政学再エスカ」が主因、現在は「韓国発半導体AI個別材料＋薄商い＋介入警戒」が主因。

### 2-2. 2026-6-19_wk03 — 介入警戒キングピン / リスクオン回帰との綱引き

**成否: 未照合。**

当時の読み:

- regime は `Neutral`。6/16-17ダブル中銀通過と米イラン停戦/ホルムズ再開でリスクオン回帰。
- VIX 16.4でAdd risk gate再開。
- ただし新キングピンはドル円介入警戒。
- 早朝161.68〜161.83ピークは、2024年4月29日の介入直前とほぼ同水準。
- 162一段上げからの急落、買い上がりのバイングクライマックスを警戒。
- 月曜は米休場明けで薄商いの振り回し注意。
- US100は30,406まで戻ったが、30,900周辺で一旦の下落を利用する逆張り短期。
- BTCは下落相場で戻り売り目線。

現在との接続:

- 現在もVIX<18で、表面は全面RiskOffではない。
- 現在も米休場/薄商いがあり、介入flashのtrap_watchが立っている。
- 6-19は「リスクオン回帰の中に介入警戒が刺さる」局面、現在は「半導体AI個別売りの中に介入警戒が刺さる」局面。
- どちらも、見た目のregimeだけではなく、JPY政策複合を別軸で読む必要がある。

### 2-3. 2026-6-5_wk01 — yen_carry_unwind が全資産の増幅器になった週

**成否: 未照合。**

当時の読み:

- regime は `Neutral` だが、内部は「リスクオフ・whipsaw」入り。
- NFP 172Kサプライズで、金利上昇・VIX急騰・半導体distributionが発生。
- `yen_carry_unwind_amplifier=on`。
- USDJPY 160.293、円ショート満タン、160介入水準、BOJ 6/15-16利上げ観測が重なり「今週のキングピン」。
- 円キャリー巻き戻しがBTC・日本株・半導体・金に連鎖する増幅器とされた。
- BTCは60,000割れ、19ヶ月安値。独立妙味なし、円キャリー・Nasdaqと完全連動で監視のみ。
- VIX 21.51でAdd risk gate閉。

現在との接続:

- 現在もJPY要因がNASDAQ・半導体・cryptoの共通トリガーとして警戒されている。
- ただし現在はVIX 16.15でAdd risk gate再開中で、6-5ほど構造的RiskOffではない。
- 6-5は米金利上昇/雇用サプライズがリスクオフを主導。現在は雇用未達で利上げ観測後退、株安主因は半導体AI個別材料。
- したがって、現在に6-5をそのまま重ねると、未照合アナロジーから過度なRiskOff物語を作る危険がある。

### 2-4. 2026-5-1_wk01 / 2026-5-8_wk02 — BOJ/介入経路と2024年8月アナログの基礎週

**成否: 未照合。**

当時の読み:

- 5-1では4/30に5.4兆円介入。160.50→155.55→156.57。IMFルール上、第2弾介入の可能性大。
- BOJ 6/16利上げがメインイベントとして設定され、2024年8月型リスクオフ再来が想定された。
- `risk:6_16_yen_carry_unwind_btc` が立ち、BTCにも円キャリー巻き戻しリスクが接続。
- 5-8では介入の主軸が「財務省介入」から「BOJ利上げ加速」へシフト。
- `risk:boj_hike_2024_aug_replay` が明示され、2024年8月アナログが強化された。

現在との接続:

- 現在もUSDJPY高値圏・BOJ利上げ経路・介入警戒が同時にあるため、`jpy_policy_complex` の入口としては自然。
- ただし5月は「6/16本番へ向けた事前準備/予告」色が強く、現在は6/16通過後の残弾/覆面介入/協調可能性の局面。
- したがって、5月アナログは構造の由来を読むには有効だが、現在の発火タイミング判断には6-19/6-26の方が近い。

### 2-5. 2026-7-3_wk01 自身 — same_news_bear_bull_timeframe_split 初出

**成否: 未照合。**

当時/現在の読み:

- `event:anthropic_samsung_ai_chip_partnership` が、boss市況では短期弱気材料、X市況では中期強気材料として読まれた。
- boss市況: 半導体AI競合懸念 → 木曜急落の主因。
- X市況: AI計算需要が巨大で各社が自前チップを作る → AI infra需要の巨大さの証左。
- 和解軸は時間軸。
  - 短期: 価格ショック/競合懸念。
  - 中期: AI計算需要/infra需要。
- US100 29,089 も、割れで下落加速 vs 押し目買い好機という両義の節目になっている。

現在との接続:

- このパターンは過去週を引くというより、現在週から恒久化された第一号pattern。
- retrieval上は「今のニュースを単一方向に潰さない」ための監査ノードとして機能した。

---

## 3. 差分（類似＋反証セット）

### 3-1. JPY政策複合: 今 vs 6-26

**類似:**

- どちらもUSDJPYが161〜162近辺で、介入/レートチェック/覆面介入の警戒が中心。
- どちらも上値を買い上がるより、戻り高値売り・サイズ管理・flash警戒が優先。
- どちらもJPY要因が株式/BTCへ波及しうる構造を持つ。

**反証/違い:**

- 6-26はPCE高止まり・FRB高官タカ派・bear flattening・Mag7メモリ転嫁が重なった、よりマクロ寄りのEquities Down。
- 7-3は雇用未達で利上げ観測は後退し、株安主因は韓国発半導体AI個別材料。VIXも18割れでAdd risk gate再開。
- よって、6-26のRiskOff深度をそのまま7-3に移植すると、現在の「半導体個別売り＋押し目買い余地」を潰す危険がある。

### 3-2. carry-unwind: 今 vs 6-5

**類似:**

- どちらもJPY要因が、NASDAQ・半導体・BTCなどの高ベータ資産に波及する構図。
- どちらも2024年8月型の円キャリー巻き戻しアナログが参照可能。
- どちらもBTCは独立妙味ではなく、リスク資産/JPY要因との連動で読む必要がある。

**反証/違い:**

- 6-5はVIX 21.51、Add risk gate閉、NFPサプライズで金利上昇。リスクオフの実体がかなり濃い。
- 7-3はVIX 16.15、Add risk gate再開。雇用未達で利上げ観測後退。半導体以外は底堅い。
- したがって、現在はcarry-unwindを「発火済み」と見るより、「薄商い・介入flash時に全資産へ伝播する地雷」として扱う方が自然。

### 3-3. 介入警戒: 今 vs 6-19

**類似:**

- どちらもVIX<18で表面上はリスクオン/低ボラ寄り。
- どちらも薄商い・休場明け・USDJPY高値圏があり、介入flashがtrapとして機能しやすい。
- どちらも「買い上がりは危険、上値からの急落に備える」読み。

**反証/違い:**

- 6-19はホルムズ再開/停戦期待でリスクオン回帰が主背景。
- 7-3は半導体AI競合懸念で株安だが、非半導体への資金シフトがある。
- 6-19は日経7万円超の過熱と介入警戒の綱引き、7-3はUS100 29,089の両義節目と半導体/非半導体の分岐が中心。

### 3-4. 同一ニュース時間軸分裂: 今 vs 通常のai_semi週

**類似:**

- 5月後半〜6月にかけて、AI/半導体/量子テーマは強気材料として何度も働いてきた。
- 一方で、6-5や6-26では半導体distributionやMag7メモリ転嫁が売り材料にもなった。
- つまりAI/半導体は常に単純強気ではなく、金利・コスト・競合・時間軸で反対方向に割れる。

**反証/違い:**

- `same_news_bear_bull_timeframe_split` は、単なる「AIテーマが強い/弱い」ではなく、**同一ニュース**を複数ソースが反対方向に読むことが条件。
- そのため、過去のai_semi週を雑に全部引くと粒度が粗すぎる。今回のpattern nodeは、ai_semiバケツよりも監査用途として鋭い。

---

## 4. 設計フィードバック（Broker/Boss向け・所見）

### 4-1. 節点の粒度

| node | 所見 |
|---|---|
| `jpy_policy_complex` | 入口としては **適切〜やや粗い**。今回のように介入・BOJ・carryが同時に匂う局面では、まずこの複合ノードに入るのが自然。ただし、retrieval後は `mof_intervention` / `boj_rate_path` / `yen_carry_unwind` のどの面が主語かを手で分ける必要がある。 |
| `yen_carry_unwind` | 入口として **適切**。JPY政策複合を全資産へ繋ぐ伝達帯として、今回のNASDAQ・半導体・BTC警戒に直接効いた。判定条件が3つあるため、米発RiskOffとの切り分けにも使える。 |
| `same_news_bear_bull_timeframe_split` | 入口というより **監査ノードとして非常に有効**。同一材料を片側に潰さず、短期/中期の時間軸に分ける指示が明確。今回のAnthropic×Samsung報道にはほぼそのまま刺さった。 |

### 4-2. retrieval摩擦

困った点:

- `RiskOff` regime node がまだ物理化されていないため、regime起点の逆引きは `index_feed_raw.md` や distilled 本文の記憶/検索に依存した。
- `jpy_policy_complex` は週リストを示してくれるが、各週の中で「介入面」「BOJ面」「carry面」の濃淡を読むには distilled 本文へ戻る必要がある。
- `ai_semi` のtheme node が未整備のため、Anthropic×Samsung報道と過去の半導体distribution / AIテーマ週を横断するには手作業が必要だった。
- `instrument/us100_levels` が未整備なので、US100 29,089と過去の27,989 / 28,957 / 30,900等の節目比較は本文から拾う必要があった。

欲しかったノード:

- `regime/RiskOff.md` または `regime/Equities_Down.md`
- `themes/ai_semi.md`
- `instruments/us100_levels.md`
- `system/vix_add_risk_gate.md`
- `patterns/thin_liquidity_flash_trap.md`（米休場/薄商い/介入flash/節目sweepを束ねる監査パターン候補）

### 4-3. 照合層の要否

**かなり必要。**

理由:

- 6-5 / 6-19 / 6-26 のどれも、現在週とかなり似た断片を持っている。
- outcome未照合のまま引くと、「似た断片」だけで説得力ある物語が作れる。
- 特に `yen_carry_unwind` は強い物語生成力があるため、発火済みなのか、地雷として待機なのかを outcome / 実測で分けないと過剰RiskOffに寄りやすい。
- `same_news_bear_bull_timeframe_split` も、短期/中期の両方があり得るため、時間窓別のoutcome照合がないと「どちらも正しかった風」になりやすい。

Backfill Stage2-3 は、少なくとも以下の粒度で必要だと感じた。

- 介入警戒週: USDJPY高値圏から実際にflashしたか / しなかったか
- carry-unwind週: USDJPY円高とUS100/BTC/半導体下落が同時発生したか
- ai_semi分裂週: 短期の売りが何日続き、中期の買いがどの時間窓で復活したか
- VIX gate週: <18 / >18 のゲートが実際の株式exposure調整に効いたか

### 4-4. engine差の所見: claude が設計した index を codex が入口から引けたか

**一行判定: 引けた。ただし regime / ai_semi / instrument が未整備な部分では、claude側の暗黙知または distilled本文読解に依存した。**

具体所見:

- `jpy_policy_complex` と `yen_carry_unwind` は、定義・週リスト・運用含意が明確で、codex側でも入口として使えた。
- `same_news_bear_bull_timeframe_split` は判定条件が機械寄りで、特に使いやすかった。
- 一方で、指示書にある `regime=RiskOff` は、実際の現在週が `Equities Down` であるため、どの程度RiskOff近傍として扱うかは本文読解で補った。
- `ai_semi弱強割れ` は pattern node によって現在週は読めたが、過去のai_semi系譜を引くindex nodeがないため、過去比較はやや手作業になった。
- `2024aug/apr replay` はnode内で参照されているが、2024年本文が今回の直接入力にはなく、2026年側の「2024_aug_replay」タグを介した間接参照に留まった。

---

## 5. 自己監査（未検証アナロジーを組んだ箇所）

以下は、outcome未照合のままアナロジーを組んだ箇所。

1. **6-26 → 7-3 の介入警戒アナロジー**
   - どちらもUSDJPY 161〜162台・介入警戒だが、6-26時点の介入警戒が実際にどの程度効いたかは未照合。
   - 7-3にそのまま重ねると、過度に円高flashを期待する物語になり得る。

2. **6-5 → 7-3 の yen_carry_unwind アナロジー**
   - 6-5はVIX>21でかなりRiskOff、7-3はVIX<18。
   - carry-unwindを共通トリガーとして読むことは有効だが、発火済み扱いにすると物語化が強すぎる。

3. **2024年8月 replay の間接利用**
   - 2024年8月そのものの本文は今回読んでいない。
   - 2026年distilled内の `2024_aug_replay` タグや記述を介して使っただけ。
   - そのため、2024年アナログの正確な差分は未検証。

4. **Anthropic×Samsung報道の短期/中期分裂**
   - patternとしては明確だが、短期売りが何日で収束し、中期強気がいつ効くかは未照合。
   - 時間軸を分けることで一見整ったが、outcomeがないと「どちらも正しい」物語に逃げやすい。

5. **US100 29,089 の両義節目**
   - 割れで下落加速 vs 押し目買い好機という読みは現在週のseedにあるが、実際にどちらが優勢になるかは未照合。
   - 過去のUS100節目ノードが未整備のため、過去の同型レベル挙動との照合はできていない。

---

## 6. 通し稽古の結論

### 節点は効いたか

**効いた。** まず `jpy_policy_complex` に入り、そこから `yen_carry_unwind` を全資産伝達帯として読む流れは自然だった。`same_news_bear_bull_timeframe_split` は、Anthropic×Samsung報道を片側に潰さない監査ノードとして特に強かった。

### 照合層は要るか

**要る。強く要る。** outcome未照合のままでも、6-5 / 6-19 / 6-26 からかなり説得力のあるアナロジーが作れてしまう。特に介入・carry-unwind・AI半導体のような強い物語生成力を持つノードは、backfill Stage2-3 がないと「もっともらしいが未検証」のまま戦略へ流れやすい。

### codexで引けたか

**引けた。** ただし、現在整備済みの3ノードは使えた一方、regime / ai_semi / us100_levels / vix_gate は未整備のため、distilled本文への手戻りが多かった。claudeの暗黙知依存を減らすには、次の物理ノード候補は `system/vix_add_risk_gate`、`themes/ai_semi`、`instruments/us100_levels`、`regime/Equities_Down or RiskOff` が有力。
