# Trade-Main

## GM 2025-11_to_12 (Archive)
- Archive: Trade_Record/_archive/source_threads_v1/acv-gm-2025-11_to_12.md
- Raw: Trade_Record/_archive/source_threads_v1/raw/
- Note: day-to-day ops are tracked via STATUS.md and weekly logs.

## Purpose (Σ:UCAR-Trade / GM)
- 週次の相場環境・判断更新点を distilled として時系列ストックし、
  将来UCARが経年データから必要要素を抽出してGM分析の材料にする（トレード効率化）。

## How to Navigate (3-layer map)
- Current location: Trade_Record/STATUS.md
- Weekly index (yearly): logs/weekly/YYYY/_index.md
- Weekly folder (yearly): logs/weekly/YYYY/YYYY-MM-DD_wkNN/
  - note.md: background / narrative (long OK)
  - meta.yaml: tags / events (machine-readable)
  - review.md: Weekly Review (result + next plan)
- distilled: distilled/YYYY/

## Workflow (weekly loop)
- Week start / midweek:
  - Append "Weekly Brief" to STATUS.md (short)
- Week end (Fri close):
  - Write "Weekly Review" into weekly folder (review.md)
  - Add 1-line link to yearly _index.md
  - (Optional) extract distilled items for distilled/

## Monday AM（12/22）ラベル付け（※行動トリガー禁止）
- 月曜朝は薄商いで“狩り”混入率が高いので、**A/B/Cの寄り推定**だけ行う（売買判断はしない）。
- 実際の行動は **終値ゲート**で決定（Tokyo close / NY close）。
- テンプレは note.md 冒頭「Monday AM Check」欄を使用（コピペ運用）。
- logging:
  - 月曜朝ラベル → note.md
  - 終値結果（Tokyo/NY）→ note.md Facts欄
  - 週末まとめ → review.md


  # Trade-Main.md | GM Playbook (Week Start)
updated: 2025-12-22 09:40 JST

目的：
- BOJ後のリスクオン回帰局面で「押し目買い先着」を狙う。
- ただし薄商い×ヘッドライン×オプション要因での“行って来い/急落”を想定し、
  終値ゲートで事故を避ける。

運用原則（固定）：
1) 判定は終値優先（暫定＝東京引け / 最終＝NY引け）
2) 追いかけ買い禁止（指値先着）
3) リスクオフ判定は「3点灯（同日）」を最重視
4) 2243/2638はベータが高いので、分割＋弾（現金）を常に確保

今週の主テーマ：
- クリスマスラリー継続の“本物/偽物”を見分ける週。
- USDJPYが高値圏のため、急伸→急落（介入警戒の形）にも備える。

ゲート（最重要）：
- NY引け：
  - USDJPY: 156.59（割れ＝円高再点火） / 157.703（上抜け維持＝上伸び余地）
  - SPX: 6,667（終値割れ＝リスクオフ濃厚）
  - BTC: 84k（終値割れ＝リスクオフ加速の合図になりやすい）
- 東京引け：
  - JP225: 48,657 → 47,377（終値割れ＝リスクオフ点灯）
  - 2243: 2,514 / 2,387
  - 2638: 2,320 / 2,268

3シナリオ即応：
A) 円高急落（リスクオフ連鎖）
- 条件：USDJPY NY終値で156.59割れ（ヒゲではなく終値）
- 行動：追加買い停止、弾温存。サポ割れ終値連続なら拾い直しモードへ。

B) 行って来い（狩り→終値レンジ回帰）
- 条件：重要ライン割れがヒゲで終わり、終値で回帰
- 行動：指値のみ。成行禁止。買い戻しは終値確認後に限定。

C) 事実買い上抜け（リスクオン継続）
- 条件：USDJPY 157.703上抜け維持＋米株の引け確認＋ETF終値確認（2243=2692/2638=2458）
- 行動：追いかけず、浅押し（4H21MA）or 深押し（サポ帯）で再構築。

ヘッジ利確（小さく・ルール化）：
- 目的：押し目弾を増やす（コアは崩さない）
- 目安：2243/2638 各10〜20口
- トリガー：確認ライン近辺で失速 / 米株が確認してこない / USDJPYが加速し過ぎて形が崩れる


# Trade-Main.md — GM Playbook / Operating Manual
updated: 2026-01-03 (JST)

> NOTE: Key gates/levels are “snapshot”. Source of truth is STATUS.md.

## GM 2025-11_to_12 (Archive)
- Archive: Trade_Record/_archive/source_threads_v1/acv-gm-2025-11_to_12.md
- Raw: Trade_Record/_archive/source_threads_v1/raw/
- Note: day-to-day ops are tracked via STATUS.md and weekly logs.

## Purpose (Σ:UCAR-Trade / GM)
- 週次の相場環境・判断更新点を distilled として時系列ストックし、
  将来UCARが経年データから必要要素を抽出してGM分析の材料にする（トレード効率化）。

## How to Navigate (3-layer map)
- Current location: Trade_Record/STATUS.md
- Weekly index (yearly): logs/weekly/YYYY/_index.md
- Weekly folder: logs/weekly/YYYY/<week_id>/
  - note.md: rolling note（facts-first）
  - meta.yaml: tags / regime / levels（machine-readable）
  - review.md: week summary + next plan
  - charts.md + charts/: chart snapshots + level-change reasons
- distilled (monthly): distilled/YYYY/distilled-gm-YYYY-M.md

## Workflow (weekly loop)
- Week start: note.md に macro/regime をドラフト（Monday AM label を冒頭に）
- Mid-week: meta.yaml に signals / bias を追加（event-driven）
- Week end: review.md に result / next をまとめ、distilled/YYYY.md に判断変更点を抽出
- Monthly: distilled/YYYY-MM.md を集約（検索用）

## Weekly Conventions
- Regime: risk-on / risk-off / cautious / etc.（+sub notes）
- Key gates: Add/Reduce risk conditions
- Links: intra-folder relative

## 2026 Weekly Index
### 2026-1-3_wk52（2025-12-29 → 2026-01-03）
- Regime: risk-on (cautious) / thin liquidity
- 1行：年末年始の薄商いで“上げるが踏み切らない”モード。次週イベント待ち。
- Key gates:
  - Add risk: US100 daily close > 25,670 and 21MA holds（押し目のみ／追わない）
  - Reduce risk: US100 daily close < 23,692 OR USDJPY < 154.7
- Links:
  - [note](./2026-1-3_wk52/note.md)
  - [meta](./2026-1-3_wk52/meta.yaml)
  - [review](./2026-1-3_wk52/review.md)
  - [charts](./2026-1-3_wk52/charts/charts.md)

### 2026-1-10_wk01（2026-01-05 → 2026-01-10）
- Regime: risk-on_cautious（rotation accelerating / low vol）
- 1行：回転加速＋低ボラで株が崩れにくいが、金利粘りで追撃を控えめに。
- Key gates:
  - Add risk: 押し目のみ
  - Reduce risk: VIX上抜け or 金利再上昇
- Links:
  - [note](./2026-1-10_wk01/note.md)
  - [meta](./2026-1-10_wk01/meta.yaml)
  - [review](./2026-1-10_wk01/review.md)
  - [charts](./2026-1-10_wk01/charts/charts.md)

### 2026-1-17_wk02（2026-01-13 → 2026-01-17）
- Regime: risk-on_cautious（rotation + low vol, but yields sticky & gold bid）
- 1行：金利が落ちにくい＋金が崩れにくい＝“ヘッジと追撃”の難易度が上がる週。
- Key signals: yields_sticky / gold_bid / breadth_weakening / jan_flow_support / earnings_risk_Feb
- Links:
  - [note](./2026-1-17_wk02/note.md)
  - [meta](./2026-1-17_wk02/meta.yaml)
  - [review](./2026-1-17_wk02/review.md)
  - [charts](./2026-1-17_wk02/charts/charts.md)

### 2026-1-24_wk03（2026-01-19 → 2026-01-24）
- Regime: risk-on_cautious（risk-on継続だがJPYショック＋Goldブレイクでヘッジ需要が可視化）
- 1行：薄い板×イベント週。終値ゲートと分割以外はやらない週（追撃禁止）。
- Key gates:
  - Add risk: US100 > 25,670 を終値で確認 → 押しで21MAが支える
  - Reduce risk: US100 D1 close < 23,692 または USDJPY < 154.7
- Links:
  - [note](./2026-1-24_wk03/note.md)
  - [meta](./2026-1-24_wk03/meta.yaml)
  - [review](./2026-1-24_wk03/review.md)
  - [charts](./2026-1-24_wk03/charts/charts.md)

### 2026-2-6_wk01（2026-02-02 → 2026-02-06）
- Regime: US risk_off（tech-led） / JP risk_on（election） / USDJPY_breakout / intervention_tailrisk / oil_bid
- 1行：DC過剰投資懸念でMSFT等が崩れ、米株は損切り連鎖。日本は選挙期待で強いが、米株失速と円安の“介入リスク”が次の揺れ。
- Key gates:
  - Add risk: US100 25,011（=直近終値）を維持しつつ 21MAを回復、かつ VIX < 20（押し目のみ／追撃禁止）
  - Reduce risk: US100 daily close < 23,913（下げ加速：22,223〜21,264視野）／JP225 < 51,141／USDJPY < 154.747（調整） or 159.348上抜け後の急反落（介入）／US10Y > 4.30 or US2Y > 3.67（テック逆風）
- Links:
  - [note](./2026-2-6_wk01/note.md)
  - [meta](./2026-2-6_wk01/meta.yaml)
  - [review](./2026-2-6_wk01/review.md)
  - [charts](./2026-2-6_wk01/charts/charts.md)

### 2026-2-13_wk02（2026-02-09 → 2026-02-13）
- Regime: US risk_off_cautious（tech稲穂 + employment_upside → rate_cut_delay） / JP risk_on_overheat（election_afterglow） / USDJPY_sticky_high / geopolitics_watch (Iran) / VIX_rise
- 1行：雇用上方修正＋MSFT好決算なのにSaaS売られ米国株リスクオフ兆候、日本株オン継続だが連動下落警戒。トランプFRBタカ派指名＋イラン悪化でボラ増。
- Key gates:
  - Add risk: US100 24,000維持しつつ25,000回復＆VIX<18（押し目限定／追撃禁止）
  - Reduce risk: US100 daily close < 24,000（損切り連鎖加速：23,000視野）／JP225 < 55,000／USDJPY < 155.0（介入/巻き戻し） or 160.0上抜け後急落／US10Y > 4.30 or VIX>22定着
- Links:
  - [note](./2026-2-13_wk02/note.md)
  - [meta](./2026-2-13_wk02/meta.yaml)
  - [review](./2026-2-13_wk02/review.md)
  - [charts](./2026-2-13_wk02/charts/charts.md)

## Distilled Logs (monthly)
- 2026-01: distilled/2026/distilled-gm-2026-1.md
- 2026-02: distilled/2026/distilled-gm-2026-2.md
- 2026-03: distilled/2026/distilled-gm-2026-3.md
- 2026-04: distilled/2026/distilled-gm-2026-4.md
- 2026-05: distilled/2026/distilled-gm-2026-5.md
- 2026-06: distilled/2026/distilled-gm-2026-6.md
- 2026-07: distilled/2026/distilled-gm-2026-7.md

## 3-scenario response（週の骨格）
A) Risk-on confirmation（上抜け“本物”）
- 条件：US100 > 25,670 を終値で確認 → 押しで21MAが支える
- 行動：追わずに押し待ちで分割追加（AIベータも同様）

B) Whipsaw / itte-koi（狩り→回帰）
- 条件：重要ライン割れがヒゲで終わり、終値で回帰
- 行動：指値のみ。投げない。買い戻し/追加は終値確認後

C) Risk-off re-ignition（失速）
- 条件：US100 D1 close < 23,692 または USDJPY < 154.7
- 行動：追加停止。現金+ゴールド寄りへ。日本ベータから先に軽くする選択を検討

## Monday AM label（行動トリガー禁止）
- 月曜朝は薄商いで“狩り”が混入しやすい。
- A/B/C の寄り推定だけを note.md 冒頭に記録し、行動は終値ゲートで決める。

### 2026-3-7_wk02（2026-03-02 → 2026-03-07）
- Regime: risk_off_acceleration（employment_weak + geopol_explosion + financial_shock / gold_strong_bid / btc_resilient）
- 1行：雇用下方修正でドル円下落/US100サポート死守、イラン本格化でWTI+43.62%/Gold+5.86%ヘッジ爆発、SaaSファンド解約停止で激震警戒。
- Key gates:
  - Add risk: US100 24643維持＋24700回復＆VIX<25（深押し限定／追撃禁止）
  - Reduce risk: US100 daily close <23913 OR VIX>30定着 OR WTI>100 OR Gold<4900
- Links:
  - [note](./logs/weekly/2026/2026-3-7_wk02/note.md)
  - [meta](./logs/weekly/2026/2026-3-7_wk02/meta.yaml)
  - [review](./logs/weekly/2026/2026-3-7_wk02/review.md)
  - [charts](./logs/weekly/2026/2026-3-7_wk02/charts/charts.md)

### 2026-3-20_wk04（2026-03-16 → 2026-03-20）
- Regime: Geopolitical Risk-Off + Energy Shock（FOMC_hold_hawkish + US_China_postponed + IEA_oil_6months + WTI_extreme_volatile + USDJPY_v_recovery + JP225_below_fib236）
- 1行：FOMC据え置き＋タカ派・米中延期・イスラエル湾岸爆撃でリスクオフ再加速。US100月足Fibo23.6ネック割り込みFibo38.2（22,200$）視野。WTI極端乱高下（119.50→76→100）、XAU4,500$急落。USDJPY V字（159.90→157.50→157.92）。完全凍結・弾薬最大温存。
- Key gates:
  - Add risk: 米中首脳会談再設定確認後 US100 22,200$維持かつ反発確認（追撃禁止）
  - Reduce risk: US100 daily close <22,200 OR VIX>30定着 OR WTI再高騰（ホルムズ再封鎖）
- Links:
  - [note](./logs/weekly/2026/2026-3-20_wk04/note.md)
  - [meta](./logs/weekly/2026/2026-3-20_wk04/meta.yaml)
  - [review](./logs/weekly/2026/2026-3-20_wk04/review.md)
  - [charts](./logs/weekly/2026/2026-3-20_wk04/charts.md)

### 2026-3-27_wk05（2026-03-23 → 2026-03-27）
- Regime: Geopolitical Risk-Off + Energy Shock（VIX_30_breach + US100_fib382_approaching + USDJPY_toward_161 + WTI_near_100 + stagflation_week_ahead + iran_4_6_deadline）
- 1行：VIX 31.05でwk04 Reduce gate発動水準到達。US100 23,132でFib38.2（22,222）まで約900pt。USDJPY 159.7で161円射程。4/6イラン期限・4/3雇用統計が最大の節目。2シナリオ（一段安→急反発 / 金融危機連鎖）踏まえ完全凍結継続。
- Key gates:
  - Add risk: US100 22,000〜22,222底打ち確認＋VIX鎮静（<27）＋イラン緊張緩和（追撃禁止）
  - Reduce risk: US100 daily close <22,000 OR VIX>35定着 OR WTI急騰（120$）OR イラン本格軍事衝突
- Links:
  - [note](./logs/weekly/2026/2026-3-27_wk05/note.md)
  - [meta](./logs/weekly/2026/2026-3-27_wk05/meta.yaml)
  - [review](./logs/weekly/2026/2026-3-27_wk05/review.md)
  - [charts](./logs/weekly/2026/2026-3-27_wk05/charts.md)

### 2026-4-10_wk02（2026-04-07 → 2026-04-11）
- Regime: Neutral（equities=up / volatility=normal / oil=range / gold=off / crypto=range / yields=rising）← Equities Down/Oil Surge から転換
- 1行：株高5材料（空爆抑制・米イラン協議・米中首脳会談期待・台湾2027先送り・ウクライナ終結期待）が一気に出てリスクオン転換。VIX 23.87→19.23（Add risk gate<20 到達）、US100 24,045→25,116（+4.5%）、WTI 112$→95.6$（エスカレーション・プレミアム剥落）。4/11（土）米・イラン協議結果次第で月曜の方向性が決まる。「条件付き解凍・分割限定」。
- Key gates:
  - Add risk: 4/11協議結果確認（合意 or 前向き）+ VIX<20維持 + US100 25,000維持（追撃禁止・分割限定）
  - Reduce risk: US100 D1 close <24,300 OR VIX>25再到達 OR 協議決裂報道
- Links:
  - [note](./logs/weekly/2026/2026-4-10_wk02/note.md)
  - [meta](./logs/weekly/2026/2026-4-10_wk02/meta.yaml)
  - [review](./logs/weekly/2026/2026-4-10_wk02/review.md)
  - [charts](./logs/weekly/2026/2026-4-10_wk02/charts.md)

### 2026-4-17_wk03（2026-04-14 → 2026-04-18）
- Regime: Gold Bid（equities=up / volatility=normal / oil=range / gold=bid / crypto=strong / yields=falling）← Neutral から転換
- 1行：ホルムズ海峡全面開放報道（4/17深夜）でリスクオンが加速。US100 25,116→26,672（+6.2%）と「青丸2」レジスタンス突破。WTI 95.63→83.85（-12.4%）エスカレーションプレミアム完全剥落。VIX 17.48でAdd risk環境が深化。Regime「Neutral」→「Gold Bid」へ（株+金同時上昇の特殊局面）。4/22停戦期限・4/28日銀（利上げなし確認）・4/29 GW介入リスクが次週の三大焦点。
- Key gates:
  - Add risk: VIX<18維持 + WTI<90$確認 + US100 26,000維持（追撃禁止・分割限定）
  - Reduce risk: US100 D1 close <25,800 OR VIX>22再到達 OR WTI>90$急騰 OR 停戦破綻報道
- Links:
  - [note](./logs/weekly/2026/2026-4-17_wk03/note.md)
  - [meta](./logs/weekly/2026/2026-4-17_wk03/meta.yaml)
  - [review](./logs/weekly/2026/2026-4-17_wk03/review.md)
  - [charts](./logs/weekly/2026/2026-4-17_wk03/charts.md)

### 2026-4-24_wk04（2026-04-21 → 2026-04-25）
- Regime: Gold Bid（equities=up / volatility=normal / oil=range / gold=bid / crypto=strong / yields=falling）← 継続。WTI 90$gate超過・VIX 18.71と微超過。
- 1行：US100 27,303（wk03比+2.4%）でターゲット達成。TINA相場（米国産油No.1）継続も「上は追わない、押し目を待つ」フェーズへ移行。WTI 94.4$（90$gate超過）・Gold 4,722$（「トレード困難」）・VIX 18.71と3指標が微超過。4/28日銀ハト派確認・4/29 GW介入リスクが最大焦点。ユニチカ（3103）・SBG押し目・Silver代替が次週テーマ。
- Key gates:
  - Add risk: BOJ植田ハト派確認後 + VIX<20維持 + US100 26,000維持（追撃禁止・押し目限定）
  - Reduce risk: US100 D1 close <25,800 OR VIX>22 OR WTI>98.45$急騰 OR 植田タカ派（6/16示唆）
- Links:
  - [note](./logs/weekly/2026/2026-4-24_wk04/note.md)
  - [meta](./logs/weekly/2026/2026-4-24_wk04/meta.yaml)
  - [review](./logs/weekly/2026/2026-4-24_wk04/review.md)
  - [charts](./logs/weekly/2026/2026-4-24_wk04/charts.md)

### 2026-5-1_wk01（2026-04-27 → 2026-05-01）
- Regime: Neutral（equities=up / volatility=normal / oil=range / gold=range / crypto=strong / yields=rising）← wk04「Gold Bid」から転換。4/30介入5.4兆円・VIX 16.99でAdd risk gate達成・Gold range転換。
- 1行：4/28 BOJハト派確認（VIX→16.99・Add risk gate <18達成）直後、4/30に5.4兆円介入（160.50→155.55→156.57）が発動。S&P500 4月単月2020年以来最大上昇・Nasdaq総合25,000台史上初で5週陽線過熱圏。次の大本命は6/16日銀利上げ（148.67ターゲット）。5/4〜5/6第2弾介入での154.00〜154.50 USDJPY押し目が5月最優先アクション。
- Key gates:
  - Add risk: VIX<18維持 + 介入底（154.00〜154.50）確認後 + US100 26,000維持（追撃禁止・分割限定）
  - Reduce risk: US100 D1 close <26,000 OR VIX>22 OR WTI>110$再急騰 OR 第2弾介入後も底なし下落
- Links:
  - [note](./logs/weekly/2026/2026-5-1_wk01/note.md)
  - [meta](./logs/weekly/2026/2026-5-1_wk01/meta.yaml)
  - [review](./logs/weekly/2026/2026-5-1_wk01/review.md)
  - [charts](./logs/weekly/2026/2026-5-1_wk01/charts.md)

### 2026-5-8_wk02（2026-05-04 → 2026-05-08）
- Regime: Neutral（equities=up / volatility=normal / oil=range / gold=range / crypto=strong / yields=rising）← wk01継続。WTI 101→95ドル低下・JP225史上最大+5.58%・BTC 80,000突破が主な変化点。
- 1行：GW中の第2弾介入（5月計約4.68兆円）は効果3円に留まり円安抑制の主軸が「介入」→「日銀利上げ加速」へシフト。5/7 JP225 史上最大+5.58%（US100+5.5%のGW明けキャッチアップ）で過熱感。BTC 80,000突破。5/11ベッセント来日・日銀異例会談が最大焦点。USDJPY 157.25からの戻り売りが「ボーナスステージ」。
- Key gates:
  - Add risk: VIX<18維持 + JP225押し目（58,500〜60,051圏）確認後 + US100過熱解消後（追撃禁止）
  - Reduce risk: US100 D1 close <27,500 OR VIX>22 OR BOJ利上げ加速で日本株崩れ連鎖 OR US10Y>4.4%定着
- Links:
  - [note](./logs/weekly/2026/2026-5-8_wk02/note.md)
  - [meta](./logs/weekly/2026/2026-5-8_wk02/meta.yaml)
  - [review](./logs/weekly/2026/2026-5-8_wk02/review.md)
  - [charts](./logs/weekly/2026/2026-5-8_wk02/charts.md)

### 2026-5-15_wk03（2026-05-11 → 2026-05-15）
- Regime: Neutral（equities=up / volatility=normal / oil=range / gold=off / crypto=strong / yields=rising）← wk02継続も内部はリスクオフ前傾（gold range→off・VIX<18→>18 Add risk gate閉・US10Y 4.4%突破）。
- 1行：週末にかけ世界的債券パニック→リスクオフ進行（US10Y 4.568%・JP10Y 2.7%・日本トリプル安）。VIX 18.43でAdd risk gate閉、US10Y 4.595で4.4%分水嶺突破（wk02 Reduce risk条件成立）。Gold 4,720→4,544急落（gold=off）。米中首脳会談成功（H200中国10社解禁・ボーイング200機・大豆・LNG）で5/21 NVDA決算まで「下げたら買い」上目線。月曜ブラックマンデー→火曜下押し→水曜反発のリズム想定で押し目買い（株）×戻り売り（ドル円158後半→156）の二刀流。
- Key gates:
  - Add risk: 閉（VIX 18.43>18）。再開＝VIX<18回帰 + 月曜深押しの押し目確認 + US10Y 4.4%回帰
  - Reduce risk: US10Y>4.4%定着（成立中）OR JP10Y>2.9% OR US100 D1 close<27,989 OR VIX>22
- Links:
  - [note](./logs/weekly/2026/2026-5-15_wk03/note.md)
  - [meta](./logs/weekly/2026/2026-5-15_wk03/meta.yaml)
  - [review](./logs/weekly/2026/2026-5-15_wk03/review.md)
  - [charts](./logs/weekly/2026/2026-5-15_wk03/charts.md)


## Weekly Brief | 2026-4-3_wk01（2026-03-30 → 2026-04-03）
created: 2026-04-05 (JST)

### Macro / Regime
- Regime（system）: Equities Down / Oil Surge（equities=down / volatility=normal / oil=surge / gold=off / crypto=range / yields=rising）
- **VIX 23.87** でwk05（31.05）から低下。ただし地政学エスカレーション最高水準で週明け再上昇警戒。
- **US100 24,045$** → 23,900$週足ネックを若干上回って終了。48h期限後の確認が最重要。
- **WTI 112$（土曜）** → 金曜103.5比+8.5$。トランプ48h最後通牒＋JASSM-ER全在庫中東投入で急騰。
- **XAUUSD 4,702$** → 安全資産買い本格化。wk05比+178$。
- **US10Y 4.313 / US2Y 3.948** → 債券フライト。US2Y 4%割れ。
- **トランプ48h最後通牒（4/4）**: 軍事行動の直前シグナル。イランは反発。4/6-7が最大分岐点。
- **NATO脱退検討**: 欧米同盟への波及リスク。

### Position / Orders
- Core：Gold（4,702$・安全資産移行確認）/ エネルギー（WTI保有継続）/ 防衛継続保有。
- Mode：完全凍結継続。4/6-7 48h期限通過まで絶対NO-GO。
- 弾薬温存：期限通過後の停戦合意確認 + US100維持 + VIX<20全条件確認後のみ初動。

### Key Levels (close-based)
- US100: 24,045 / R=24,643 / S=23,900（週足ネック）/ 22,222（Fib38.2）/ 22,000
- JP225: TBD / S=36,000〜35,000（サポート帯）
- USDJPY: 159.632 / R=160.0（レートチェック）/ 161.0（NOBUターゲット）
- WTI: 112.060（土曜）/ 103.5（金曜）/ R=120.0（介入水準）/ S=100.0
- XAUUSD: 4,702.7 / S=4,574（wk05終値）/ 4,100
- VIX: 23.87 / US10Y: 4.313 / US2Y: 3.948

### Gates（最重要：終値で判定）
- Add risk ONLY if: 4/6-7 48h期限通過後に停戦合意確認 + US100 24,045$週足維持 + VIX<20（追撃禁止）
- Reduce / pause if: US100 D1 close <23,400 OR VIX>30再到達 OR WTI>120$ OR JASSM-ER実際に使用
- Hedge gate: Gold 4,702$維持 / エネルギー / 防衛継続

### This Week Focus（行動: 4/6-4/10）
- 完全凍結継続。4/6-7 トランプ48h最後通牒期限通過まで絶対NO-GO。
- 4/6-7（月-火）: 48h期限の停戦合意 or 軍事拡大の確認。最大の地政学分岐点。
- 4/10（木）米国CPI: WTI急騰背景の物価指標。スタグフレーション確認度に注目。
- US100 24,045$の偽ブレイク or 本物上抜けの週足確認。

### Signals (weekly, fixed keys)
- us10y_accel: easing（4.313。債券フライトで低下中）
- hy_oas_widening: alert（地政学エスカレーション最高水準）
- vix_spike: easing（23.87。低下も週明け再上昇警戒）
- wti_shock: on（112$土曜 / 金曜103.5$ / エスカレーション・プレミアム）
- eps_revision_chain: watch（4/10 CPI・WTI急騰背景のインフレ確認）

## Previous (archived briefs)
- Weekly Brief | 2026-3-27_wk05（2026-03-23 → 2026-03-27）
  - see: logs/weekly/2026/2026-3-27_wk05/

## Weekly Brief | 2026-3-27_wk05（2026-03-23 → 2026-03-27）
created: 2026-03-29 (JST)

### Macro / Regime
- Regime: Geopolitical Risk-Off + Energy Shock（第5週継続）
- VIX 31.05でwk04設定のReduce risk gate（VIX>30定着）が発動水準に到達。
- US100 23,132.77 → Fib38.2（22,222）まで約900pt。NOBUターゲット22,000が視野。
- USDJPY 159.704で円安継続。NOBUターゲット161円が射程。
- WTI 99.64で100$近辺高止まり。エネルギーショック構造継続。
- XAUUSD 4,524.3で短期調整継続。4,500サポート注視。
- イラン/ガザ: 戦闘停止に向けた動き。4/6前後に米・イラン攻撃延期期限（最大節目）。

### Position / Orders
- Core：Gold / エネルギー（WTI 100$近辺）/ 防衛（ゴールデンドーム関連）継続保有。
- Mode：完全凍結継続。VIX>30到達・4/6イラン期限まではNO-GO。
- 弾薬温存：US100 22,000〜22,222底打ち確認待ち。
- 長期ポートフォリオ：売り不要。安値での積立加速を検討。

### Key Levels (close-based)
- US100: 23,132.77 / S=22,222（Fib38.2）/ 次=21,264 / テールリスク=20,000
- JP225: S=36,000〜35,000 / 3/30権利落ち注意
- USDJPY: 159.704 / R=161.0（NOBUターゲット）/ S=149〜150（急落シナリオ）
- WTI: 99.640 / R=106（NOBUターゲット）/ S=68〜70
- XAUUSD: 4,524.3 / S=4,500 / VIX: 31.050 / US10Y: 4.440

### Gates（最重要：終値で判定）
- Add risk ONLY if: US100 22,000〜22,222底打ち確認＋VIX<27＋イラン緊張緩和（追撃禁止）
- Reduce / pause if: US100 D1 close <22,000 OR VIX>35定着 OR WTI急騰（120$）OR イラン本格衝突
- Hedge gate: Gold 4,500サポート / エネルギー / 防衛継続

### This Week Focus（行動: 3/30-4/4）
- 完全凍結継続。4/6イラン期限通過まではNO-GO徹底。
- 4/3（金）雇用統計 + ISMサービス業PMI：スタグフレーション確認の最重要指標。
- 3/30（月）権利落ち：ギャップダウン想定。成行で動かない。
- US100 22,000〜22,222接近時の底打ちサイン（TACO仮説）を日足終値で確認。

### Signals (weekly, fixed keys)
- us10y_accel: on（4.440%）
- hy_oas_widening: alert（プライベートクレジット デフォルト懸念）
- vix_spike: on（31.05 / 30超え確定）
- wti_shock: on（99.64 / 100$高止まり）
- eps_revision_chain: watch（4/3雇用統計待ち）

## Previous (archived briefs)
- Weekly Brief | 2026-3-20_wk04（2026-03-16 → 2026-03-20）
  - see: logs/weekly/2026/2026-3-20_wk04/


## Weekly Brief | 2026-3-20_wk04（2026-03-16 → 2026-03-20）
created: 2026-03-21 (JST)

### Macro / Regime
- Regime: Geopolitical Risk-Off + Energy Shock
- FOMC（3/19）政策金利据え置き＋タカ派発言。イラク侵攻インフレ加速懸念継続。米中首脳会談延期でリスクオフ再加速。
- IEA声明：湾岸諸国エネルギー輸出の復旧に半年見通し→原油高長期化シナリオ（180$予測アナリストも）。
- イスラエルによる湾岸諸国空爆・エネルギー施設破壊継続。米軍中東に海兵隊数千人追加派遣。
- WTI極端乱高下（119.50→76→100）。XAU週足Fibo23.6→日足押し安値4,500$まで急落。
- US100 月足Fibo23.6の週足ネックライン割り込み終値→Fibo38.2（22,200$）視野。
- JP225 週足ワントップから急落、Fibo23.6実体割り込み終値（日米首脳会談・防衛セクターで相対堅調）。
- USDJPY：159.90（週高値）→157.50（日銀牽制急落）→157.924（金曜終値）V字。VIX 26.78高止まり。

### Position / Orders
- Core：Gold / エネルギー（WTI 100$回復確認）/ 防衛（日米共同開発・ゴールデンドーム関連）継続保有。
- Mode：完全凍結継続。米中首脳会談再設定確認まではNO-GO。
- 弾薬温存：US100 Fibo38.2（22,200$）/ JP225 深押し待機継続。
- USDJPY：V字回復確認済み。介入急落（～3円）は一過性対処方針継続。

### Key Levels (close-based)
- US100: 23,898.154（週終値）/ S=22,200（Fibo38.2）/ 次=21,264
- JP225: Fibo23.6実体割り込み終値 / S=54,814
- USDJPY: 157.924（金曜NY終値）/ 週高159.90 / 週安157.50
- WTI: 98.230 / S=95.0 / R=100.0（施設復旧半年で高止まり）
- XAUUSD: 4,574.9（日足押し安値4,500$付近）
- US2Y: 4.012 / US10Y: 4.391 / VIX: 26.780

### Gates（最重要：終値で判定）
- Add risk ONLY if: 米中再設定確認後 US100 22,200$維持かつ反発（追撃禁止）
- Reduce / pause if: US100 D1 close <22,200 OR VIX>30定着 OR WTI再急騰
- Hedge gate: Gold 4,500$押し目・エネルギー・防衛継続

### This Week Focus（行動: 3/23-27）
- 完全凍結継続。米中首脳会談再設定の有無を最重視。
- WTI 100$定着 or 調整を確認（エネルギー保有判断）。
- 日銀4月タカ派発言内容に注意（円高加速リスク）。
- VIX 26.78の30超え定着 or 鎮静を日足終値で確認。

### Signals (weekly, fixed keys)
- us10y_accel: on（FOMC据え置き・タカ派でUS10Y 4.391%）
- hy_oas_widening: alert（プライベートクレジット リスクオフ型新商品波及）
- vix_spike: on（26.78 高止まり）
- wti_shock: on（極端乱高下・100$回復・施設復旧半年）
- eps_revision_chain: watch（米中延期の影響・日銀4月タカ派）

## Previous (archived briefs)
- Weekly Brief | 2026-3-13_wk03（2026-03-09 → 2026-03-13）
  - see: logs/weekly/2026/2026-3-13_wk03/


## Weekly Brief | 2026-4-17_wk03（2026-04-14 → 2026-04-18）
created: 2026-04-18 (JST)

### Macro / Regime
- Regime: Gold Bid（equities=up / volatility=normal / oil=range / gold=bid / crypto=strong / yields=falling）← wk02「Neutral」から転換。
- ホルムズ海峡全面開放（4/17深夜）でリスクオンが加速。US100 25,116→26,672（+6.2%）と「青丸2」（25,45x）を突破。WTI 95.63→83.85（-12.4%）、VIX 19.23→17.48。Goldは4,857$で高値更新中。
- TSMC四半期純利益+60%（過去最高）。日銀4/28利上げなしほぼ確定（高市首相圧力封じ確認）。

### Position / Orders
- Core：Gold（4,857$・Gold Bid継続）/ WTI（83.85$・リバウンド局面・利確検討）/ 防衛継続保有。
- Mode：Add risk継続。VIX<18 + WTI<90$ + US100 26,000維持を前提に分割限定。追撃禁止。

### Key Levels (close-based)
- US100: 26,672 / R=27,250→27,000 / S=26,500→26,000→25,800
- JP225: 過去最高値60,051接近 / S=58,000
- USDJPY: 158.584 / S=156.50 / R=161.0（介入警戒・GW）
- WTI: 83.85 / 76.98再訪想定 / 90ドル超えは株高否定シグナル
- XAUUSD: 4,857 / 目標5,060〜5,070
- VIX: 17.48 / US10Y: 4.246 / US2Y: 3.838

### Gates（最重要：終値で判定）
- Add risk ONLY if: VIX<18維持 + WTI<90$確認 + US100 26,000維持（追撃禁止・分割限定）
- Reduce / pause if: US100 D1 close <25,800 OR VIX>22再到達 OR WTI>90$急騰 OR 停戦破綻報道
- Hedge gate: Gold 4,857$ / WTI利確検討 / 防衛継続

### This Week Focus（行動: 4/21-4/25）
- **4/22 停戦期限**: 延長合意 or 決裂で週明けの方向性が決まる（最重要確認事項）。
- **US100 27,000〜27,250pt**: 到達時の調整 or 突破確認。
- **4/28 日銀会合**: 利上げなし確認→円安バイアス再確認。
- **4/29 GW**: USD/JPY 161円接近時の政府介入リスク。JPYロングは慎重に。

### Signals (weekly, fixed keys)
- us10y_accel: falling（4.246。yields=falling）
- hy_oas_widening: easing（Gold Bid環境でリスクプレミアムさらに縮小）
- vix_spike: add_risk_deep（17.48）
- wti_shock: declining（83.85$。ホルムズ解放でプレミアム完全剥落）
- eps_revision_chain: positive（TSMC+60%好決算）

## Previous (archived briefs)
- Weekly Brief | 2026-4-10_wk02（2026-04-07 → 2026-04-11）

## Weekly Brief | 2026-4-10_wk02（2026-04-07 → 2026-04-11）
created: 2026-04-12 (JST)

### Macro / Regime
- Regime: Neutral（equities=up / volatility=normal / oil=range / gold=off / crypto=range / yields=rising）← wk01「Equities Down / Oil Surge」から大転換。
- 株高5材料（トランプ空爆抑制指示・米イラン停戦協議4/11・米中首脳会談期待5/14-15・台湾有事2027先送り・ウクライナ終結期待）が一気に出てリスクオン転換。
- VIX 23.87→19.23（Add risk gate<20 到達）。US100 24,045→25,116（+4.5%）。WTI 112$→95.6$（エスカレーション・プレミアム剥落）。
- CPI 3.3%（予想下振れ）/ コアCPI 2.6%。TSMC 35%増収。ダウ輸送株指数ATH（先行指標ポジティブ）。
- JP225 一目均衡表の雲を上抜け（強気シグナル）。金融庁：国内金融機関プライベートクレジット保有「限定的」→国内金融危機リスク後退。
- **最大リスク**: 4/11（土）米・イラン停戦協議（パキスタン）の決裂→月曜急落・VIX再上昇。

### Position / Orders
- Core：Gold（4,771$）/ エネルギー（WTI 95.6$ / 保有継続）/ 防衛継続保有。
- Mode：条件付き解凍。VIX<20 + 4/11協議結果確認後に分割限定エントリー。追撃禁止。
- 月・火買い→水曜売り抜けパターンを念頭に短期対応。

### Key Levels (close-based)
- US100: 25,116 / R=25,454（青丸2レジスタンス）/ S=24,800→24,773→24,300（押し目）
- JP225: 上値58,930（合意シナリオ）/ 利確58,400 / 下落転換55,698 / S=53,936
- USDJPY: 159.245 / S=156.54（3H足）/ R=159.39→160.50（急落警戒）
- WTI: 95.63 / 80$台不回帰継続（停戦不信シグナル）
- XAUUSD: 4,771 / 地政学リスクヘッジ底堅い
- VIX: 19.23（Add risk gate<20 達成）/ US10Y: 4.317 / US2Y: 3.939

### Gates（最重要：終値で判定）
- Add risk ONLY if: 4/11協議結果（合意 or 前向き）確認 + VIX<20維持 + US100 25,000維持（追撃禁止・分割限定）
- Reduce / pause if: US100 D1 close <24,300 OR VIX>25再到達 OR 協議決裂報道
- Hedge gate: Gold 4,771$ / エネルギー継続 / 防衛継続

### This Week Focus（行動: 4/14-4/18）
- **月曜（4/14）寄り付き前**: 4/11（土）米・イラン協議結果を必ず確認してから対応判断。
- **US100 25,45x付近「青丸2」レジスタンス**: 突破 or 跳ね返り確認。月・火買い→水曜売りパターン活用。
- **4/28日銀会合**: 利上げ期待ヘッドラインで円高急落リスク。JPY関連は慎重に。
- **WTI 80$台回帰**: 停戦への市場信頼度の目安として継続監視。

### Signals (weekly, fixed keys)
- us10y_accel: stable（4.317。FRB利下げ困難で高止まり継続）
- hy_oas_widening: easing（地政学プレミアム剥落で改善方向）
- vix_spike: gate_open（19.23。Add risk gate<20 到達。土日イベント次第）
- wti_shock: easing（95.6$。プレミアム剥落。80$不回帰は停戦不信シグナル継続）
- eps_revision_chain: positive（CPI下振れ / TSMC好決算 / 輸送株ATH）

## Previous (archived briefs)
- Weekly Brief | 2026-4-3_wk01（2026-03-30 → 2026-04-03）
  - see: logs/weekly/2026/2026-4-3_wk01/


## Weekly Brief | 2026-4-24_wk04（2026-04-21 → 2026-04-25）
created: 2026-04-25 (JST)

### Macro / Regime
- Regime: Gold Bid（equities=up / volatility=normal / oil=range / gold=bid / crypto=strong / yields=falling）← wk03から継続。WTI 90$gate超過・VIX 18.71と微超過も「TINA相場」構造は継続。
- US100 27,303$（wk03比+2.4%）。wk03ターゲット27,000〜27,250を達成。ボス「上は追わない、押し目を待つ」。26,400（赤丸）→26,840フロー。上値28,000。
- WTI 94.4$（wk03 83.85比+12.6%・90$gate超過）。ボス「下落相場ベース」。93.55$割れで88.74$フロー。
- Gold 4,722$（wk03 4,857比-2.8%）。ボス「キングゴールドはトレードできない状況」。Silver代替（71.50→75.08）。
- 4/21日経新聞：4/28日銀利上げなし確定報道。4/24日本CPI+1.5%（世界最低水準）。利上げ見送り正当化。
- ChatGPT 5.5リリース（Claude・Gemini 3を抜いてNo.1）。Arm半導体自製化でSBG+68%急騰（過熱→5,197押し目待ち）。
- AI相場循環最終局面：ガラスコア部材（日本電気硝子・AGC・ユニチカ3103）に資金シフト。

### Position / Orders
- Core：Gold（4,722$・短期調整中）/ Silver代替（71.50→75.08）/ 防衛継続保有。
- Mode：上値追い禁止。「下がったら買う」TINA戦略。4/28植田会見確認後に整理。追撃禁止。
- WTI: 93.55$割れ確認後にポジション調整検討（下落相場基調）。
- USDJPY: 159.02-159.40フロー利用。160円接近は触らない（GW介入リスク）。

### Key Levels (close-based)
- US100: 27,303 / R=28,000 / フロー=26,400→26,840 / S=26,000→25,800
- JP225: 目標61,370円 / 押し目50,867円 / 上値59,100円
- USDJPY: 159.333 / フロー=159.02→159.40 / 介入警戒=160.00 / 介入後=150台
- WTI: 94.400 / 98.45超えで103$フロー / 93.55割れで88.74$フロー
- XAUUSD: 4,722.300 / Gold「トレード困難」/ Silver=71.50→75.08
- VIX: 18.710 / US10Y: 4.310 / US2Y: 3.920

### Gates（最重要：終値で判定）
- Add risk ONLY if: BOJ植田ハト派確認後 + VIX<20維持 + US100 26,000維持（追撃禁止・押し目限定）
- Reduce / pause if: US100 D1 close <25,800 OR VIX>22 OR WTI>98.45$急騰 OR 植田タカ派（6/16利上げ示唆）
- Hedge gate: Silver（71.50→75.08）/ Gold保有継続（トレード停止）/ 防衛継続

### This Week Focus（行動: 4/27-）
- **4/28（月）日銀会合**: 利上げなし確定。植田総裁会見15:30のトーン（6/16利上げ示唆有無）が最大焦点。
- **4/29（火）昭和の日GW**: USDJPY 160円接近時の政府為替介入リスク（片山金融相「断固たる措置」）。
- **NASDAQ 26,400→26,840フロー**: 押し目の有無と深さを確認。「上は追わない」。
- **WTI 93.55$割れ**: 88.74$フロー移行の確認。下落相場基調の検証。
- **ユニチカ（3103）**: 5/14決算前の動向（天井-42%・営業利益+62.4%）。3,200円近辺押し目注視。

### Signals (weekly, fixed keys)
- us10y_accel: rising_pressure（4.310。プライベートクレジット米国債売却リスクで上昇圧力）
- hy_oas_widening: watch（BOE副総裁警告・プラクレ継続監視）
- vix_spike: gate_crossover（18.71。<18 gate超過。ただし20未満で構造的リスクオフ非該当）
- wti_shock: above_gate（94.4$。90$gate超過もボス「下落相場ベース」）
- eps_revision_chain: glass_core（AI相場最終局面・ガラスコア部材・ユニチカ3103注目）

## Previous (archived briefs)
- Weekly Brief | 2026-4-24_wk04（2026-04-21 → 2026-04-25）
  - see: logs/weekly/2026/2026-4-24_wk04/
- Weekly Brief | 2026-4-17_wk03（2026-04-14 → 2026-04-18）
  - see: logs/weekly/2026/2026-4-17_wk03/


## Weekly Brief | 2026-5-1_wk01（2026-04-27 → 2026-05-01）
created: 2026-05-03 (JST)

### Macro / Regime
- Regime: Neutral（equities=up / volatility=normal / oil=range / gold=range / crypto=strong / yields=rising）← wk04「Gold Bid」から転換。4/30介入5.4兆円・Gold range転換が主因。
- **4/28 BOJ 利上げなし + 植田ハト派確認**（6/16利上げ示唆なし）。VIX 16.99（wk04比-1.72）→ Add risk gate（<18）達成。
- **4/30 政府介入 5.4兆円（1年9ヶ月ぶり）**: 160.50→155.55→156.57。IMFルール上5/4〜5/6に第2弾介入の可能性大。NOBU氏：153.95が下値限界。
- **4月米国株月間**: S&P500 +10% / Nasdaq総合25,000台史上初（2020年以来最大）。5週陽線で過熱圏入り。
- **次の大本命は6/16日銀利上げ**: NOBU氏148.67ターゲット。5月は仕込み・準備フェーズ。

### Position / Orders
- Core: Gold（4,630・range転換・保有継続）/ 防衛継続保有。
- Mode: 押し目待ち（追撃禁止）。GW中154.00〜154.50 USDJPY押し目ロングが最優先アクション。
- 6/16利上げ前準備: 5月後半からドル円ショート想定エントリー水域設定開始（152円割れ→148.67）。

### Key Levels (close-based)
- US100: 27,710 / R=28,000 / S=26,400（押し目ゾーン）→26,000
- JP225: 59,513（5/1）/ R=60,000→60,051（前最高値）/ S=58,500
- USDJPY: 157.033 / 押し目=154.00〜154.50 / 下値限界=153.95 / 6/16後=148.67
- WTI: 101.94 / R=105〜110 / S=98〜100（押し目買い）→95
- XAUUSD: 4,630 / S=4,500 / 打診買い=4,450〜4,500
- VIX: 16.990 / US10Y: 4.378 / US2Y: 4.021 / BTC: 78,179

### Gates（最重要：終値で判定）
- Add risk ONLY if: VIX<18維持 + 介入底（154.00〜154.50）確認後 + US100 26,000維持（追撃禁止・分割限定）
- Reduce / pause if: US100 D1 close <26,000 OR VIX>22 OR WTI>110$再急騰 OR 第2弾介入後も底なし下落
- Hedge gate: Gold（4,450〜4,500打診買い）/ 防衛継続 / 6/16ドル円ショート準備

### This Week Focus（行動: 5/4-）
- **5/4〜5/6（GW中）**: 第2弾介入の有無。153.95が下値限界→154.00〜154.50押し目ロング。
- **5/7（水）GW明け**: JP225 60,000上抜けor58,500割れ / US100方向確認。
- **5/14（木）ユニチカ（3103）決算**: 営業利益+62.4%。3,200円近辺注視。
- **6/16日銀利上げ準備**: 5月後半からドル円ショート想定エントリー水域設定。

### Signals (weekly, fixed keys)
- us10y_accel: rising（4.378。プラクレ売却+インフレ懸念。4.50%接近で債券買い）
- hy_oas_widening: watch（介入後安定も地政学継続監視）
- vix_spike: add_risk_gate_open（16.99。<18達成。5週陽線過熱で追撃禁止）
- wti_shock: range_high（101.94。ホルムズ継続。イラン提案で金曜▲2%）
- eps_revision_chain: ai_overheating（Apple/CoreWeave牽引・Roblox▲17%・過熱圏）

## Weekly Brief | 2026-5-8_wk02（2026-05-04 → 2026-05-08）
created: 2026-05-09 (JST)

### Macro / Regime
- Regime: Neutral（equities=up / volatility=normal / oil=range / gold=range / crypto=strong / yields=rising）← wk01から継続。WTI 101→95ドル低下・JP225史上最大+5.58%・BTC 80,000突破が主な変化点。
- **GW第2弾介入（5月計約4.68兆円）**: 合計10兆円規模でも効果は約3円。三村財務官が「介入」→「日銀利上げ加速」へ明示的なバトンチェンジを宣言。0.5%利上げ観測浮上。
- **5/11 ベッセント来日・日銀総裁異例会談（最大イベント）**: 日銀利上げ加速→円高→ドル安→米国債買戻し誘導の三位一体構図。USDJPY「戻り売り優位のボーナスステージ」へ。
- **5/7 JP225 史上最大+5.58%**: GW中のUS100+5.5%が一気に反映。記憶者ストップ高+19%。過熱感から追いかけ買い禁物。
- **BTC 80,000突破**: 80,391ドル（週中）/ 80,186（snapshot）。強気バイアス継続。

### Position / Orders
- Core: Gold（4,720・上昇トレンド継続）/ 防衛継続保有。
- Mode: 追撃禁止。USDJPY戻り売り優位（157.25売り場・156.80以下「チャンス」）。
- 5/11会談後：USDJPY戻り売りエントリー判断。JP225押し目化を期待。

### Key Levels (close-based)
- US100: 29,234 / 過熱（+5.5%wk比）/ S=28,000→27,710→27,000
- JP225: ≈61,400〜62,174（5/8）/ 5/7史上最大+5.58% / S=60,051→58,500
- USDJPY: 156.621（snapshot）/ 売り圧=157.25（5/1から継続）/ 「チャンス」=156.80以下
- WTI: 95.420 / 押し目=93〜95 / R=96.60→101.54
- XAUUSD: 4,720.400 / R=4,754→4,857 / 押し目買い一択
- VIX: 17.190 / US10Y: 4.364（4.4%分水嶺）/ US2Y: 4.013 / BTC: 80,186

### Gates（最重要：終値で判定）
- Add risk ONLY if: VIX<18維持 + JP225押し目（58,500〜60,051圏）確認後 + US100過熱解消後（追撃禁止）
- Reduce / pause if: US100 D1 close <27,500 OR VIX>22 OR BOJ利上げ加速で日本株崩れ連鎖 OR US10Y>4.4%定着
- Hedge gate: Gold（上昇継続）/ 防衛継続 / 6/16前のUSDJPYショート段階的準備

### This Week Focus（行動: 5/11-）
- **5/11（月）ベッセント来日・日銀会談**: BOJ利上げ0.5%加速コンセンサス固まるか→最重要
- **USDJPY 157.25**: 戻り売り優位。突っ込み売り禁止。156.80以下「チャンス」。
- **JP225調整**: 日銀利上げ警戒での大きめ調整→58,500〜60,051圏が絶好の買い場候補。
- **5/14（木）ユニチカ（3103）決算**: 営業利益+62.4%。3,200円近辺注視。
- **6/16日銀利上げ前準備**: 5月後半からUSDJPYショート段階的構築開始（152円割れ→148.67）。

### Signals (weekly, fixed keys)
- us10y_accel: inflection_4_4（4.364。4.4%が分水嶺。ベッセント構図と連動）
- hy_oas_widening: watch（BOJ利上げ加速観測で市場構造変化を監視）
- vix_spike: add_risk_gate_open（17.19。<18継続。過熱感で追撃禁止）
- wti_shock: range_corrected（95.42。101→95に-6.4%。93〜96圏の押し目買いゾーン形成）
- eps_revision_chain: hidden_semi_rotation（記憶者ストップ高→隠れ半導体（ダイキン・HOYA等）へ資金シフト）

## Weekly Brief | 2026-5-15_wk03（2026-05-11 → 2026-05-15）
created: 2026-05-16 (JST)

### Macro / Regime
- Regime: Neutral（equities=up / volatility=normal / oil=range / gold=off / crypto=strong / yields=rising）← wk02継続も内部はリスクオフ前傾。gold range→off・VIX<18→>18（Add risk gate閉）・US10Y 4.4%突破。
- **世界的債券パニック→リスクオフ**: US10Y 4.568%（snapshot 4.595）パニック売り。JP10Y 2.7%・30年4%・プライム平均5.3%。日本トリプル安。
- **米中首脳会談 成功**: NVIDIA H200 中国10社向け解禁・ボーイング200機・大豆・LNG。5/21 NVDA決算まで「下げたら買い」上目線。
- **FRB**: シュミッド総裁「インフレ最大リスク」→年内利上げ確率2割→3割。
- **Gold 急落**: 4,720→4,544（-3.7%）gold=off。boss $3,150〜3,200を中期押し目買い場。

### Position / Orders
- Core: Gold（4,544・保有継続・新規は$3,150〜3,200深押し待ち）/ 防衛継続保有。
- Mode: 追撃禁止強化（VIX>18・US10Y>4.4%定着）。月曜深押し→反発を拾う準備。
- 5/21 NVDA決算まで押し目買い（株）×戻り売り（ドル円158後半→156）の二刀流。

### Key Levels (close-based)
- US100: 29,125 / 27,989赤丸反発→28,874レンジ / 29,662超で3万pt（追わない）
- JP225: ≈60,000周辺反発狙い / 63,150超で本格上昇 / 月曜ブラックマンデー想定
- USDJPY: 158.731 / 売り=158後半 / 買い戻し=156付近 / 下押し目安=157.60
- WTI: 101.160 ※boss view 60〜65ドルと乖離・要確認
- XAUUSD: 4,543.600（gold=off）/ 中期押し目買い=$3,150〜3,200
- VIX: 18.430（>18 gate閉）/ US10Y: 4.595（4.4%突破・上限4.6〜4.7%）/ US2Y: 4.258 / BTC: 81,051

### Gates（最重要：終値で判定）
- Add risk ONLY if: VIX<18回帰 + 月曜深押しの押し目確認 + US10Y 4.4%回帰（現在gate閉）
- Reduce / pause if: US10Y>4.4%定着（成立中）OR JP10Y>2.9% OR US100 D1 close<27,989 OR VIX>22
- Hedge gate: Gold（保有継続・深押し$3,150〜3,200待ち）/ 防衛継続 / 6/16前USDJPYショート準備

### This Week Focus（行動: 5/18-）
- **5/18（月）想定ブラックマンデー**: 債券パニック・トリプル安の波及度。深押しは押し目買い準備
- **5/21（木）NVDA決算**: 最大の通過点。通過後（5/22〜）調整警戒
- **JP10Y 2.9%**: 超えたら株式エクスポージャー一段落とし（最重要トリガー）
- **火曜後場（15:15以降）**: 日本株個別の本命仕込み（キオクシア285A・ユニチカ3103 等）
- **6/16日銀利上げ準備**: 0.75→1.00%ほぼ確実。USDJPYショート想定水域の段階的構築継続

### Signals (weekly, fixed keys)
- us10y_accel: panic_breakout_4_6（4.595。4.4%分水嶺突破。上限メド4.6〜4.7%）
- hy_oas_widening: watch（世界的債券パニック・JP10Y 2.7%異常水準・補正予算観測）
- vix_spike: add_risk_gate_closed（18.43。<18→>18でgate閉。20未満で構造的リスクオフ非該当）
- wti_shock: range_vs_boss_gap（実測101.160 / boss view 60〜65ドル・乖離要確認）
- eps_revision_chain: us_china_h200_unlock（米中会談成功・H200中国10社解禁。5/21決算まで上目線）

## Weekly Brief | 2026-5-22_wk04（2026-05-18 → 2026-05-22）
created: 2026-05-23 (JST)

### Macro / Regime
- Regime: Neutral（equities=up / volatility=normal / oil=range / gold=range / crypto=up / yields=rising）← wk03継続も内部品質が「リスクオフ前傾」から「AI テーマ主導・正常化」へシフト。gold「off」→「range」へ回復・VIX<18でAdd risk gate再開・BTC上トレンド。
- **AI テーマ主導**: SpaceX上場（6/12、時価総額300兆円規模）・Physical AI・量子（米国政府20億ドル拠出）が相場主導。5/21 NVDA決算通過後から新たな買い目線。
- **米国 3連休前のリスク調整**: メモリアルデー5/26月休場。3連休前のリスク調整＆ポジション整理局面。薄商いで月曜ボラティリティ上昇、押し目買い好機と注意が同居。
- **日本株上昇流れ**: Nikkei 61,287→62,282→62,689。3連休前リスク回避で62,900超でズドン急落警戒。60,000～63,300レンジ継続想定。
- **ドル円戻し売り待機**: USDJPY 159.155で159.50～60への戻し上げを待つ「休憩」モード。ロング入れない。6/3植田・6/16日銀会合に向け円高地雷を意識。

### Position / Orders
- Core: 米国株・日本株はV字回復後の押し目買い（高値追わない）。USDJPY 159.50～60での戻り売り待ち。
- Mode: 3連休前ボラ警戒継続も押し目買い環境再確認（VIX 16.7<18でAdd risk gate再開）。
- 6/3植田講演・6/16日銀会合に向け、円高加速の起点を探る展開が来週のテーマ。

### Key Levels (snapshot-based)
- US100: 29,481 / 30,185→30,540～30,600方向（停戦確定時） / 27,989赤丸以上の売り込みは買い場
- JP225: 66,351方向 / 67,500円視野 / 62,900超で青丸急落警戒 / 60,000～63,300レンジ
- USDJPY: 159.155 / 159.50～60戻し売り待ち / 160円は防衛ライン
- WTI: 96.6 / ノートレード（上下難） / 92.48超えから上昇利用可
- XAUUSD: 4,523 / レンジ確定（4,515～4,571）/ 4,600方向の小幅利用のみ
- VIX: 16.7（<18 Add risk gate再開） / US10Y: 4.558（4.4%定着化） / BTC: 76,673

### Gates（最重要：終値で判定）
- Add risk: OPEN（VIX<18）ただし3連休前ボラ警戒継続
- Reduce risk: US10Y>4.4%定着継続 / JP10Y>2.9% / US100 D1 close<27,989 / VIX>22
- Hedge gate: Gold保有継続（新規は4,515割れの押し目待ち）/ 防衛継続 / 6/3～6/16に向けUSDJPYショート段階構築

### This Week Focus（行動: 5/26-）
- **5/26（月）米国メモリアルデー**: 薄商い＆ポジション調整ボラ。月曜ギャップダウンは押し目買い好機
- **火曜以降CPI確認**: 再加速を待つ
- **SpaceX/AI量子テーマ**: 6/12上場まで買い目線維持
- **6/3植田講演・6/16日銀会合**: 円高地雷点灯の第一テクニカルシグナル。利上げ示唆を注視

---

## Weekly Brief | 2026-5-29_wk05（2026-05-25 → 2026-05-29）
created: 2026-05-30 (JST)

### Macro / Regime
- Regime: Neutral（equities=up / volatility=normal / oil=range / gold=range / crypto=range / yields=rising）← wk04継続も内部品質は「AI・量子テーマ主導 × BTC戻り売り転換」へ質的シフト。VIX 15.32で低ボラ環境。
- **AI・量子テーマ主導継続**: SpaceX/OpenAI/Anthropic上場期待（6/12）。Anthropic企業価値154兆円がOpenAIを上回る。IBM 1.5兆円量子投資で国策化観測。
- **停戦合意でリスクオン**: イラン米国60日間暫定停戦（トランプ署名待ち・過去6回否定歴）。ただし原油88ドル台の高止まりが「本質的に終わっていない」根拠。
- **US10Y上昇トレンド**: 4.453%。JPMダイモン「金利は格段に高くなる」で上振れ。ただし「金利上昇でも AI頼みで株は買える」スタンス維持。
- **BTC戻り売り転換**: 量子暗号解読リスク意識で「上がったら売る」へ転換。71,347ドル方向の下落利用推奨。

### Position / Orders
- Core: AI・量子テーマのロング目線継続（高値追わない）。BTC『上がったら売る』へ転換。ドル円160円が壁。
- Mode: イラン情勢の突発報道最重要。停戦否定で原油反発も、株式へのインパクト限定的か。
- 6月の大型触媒（6/3植田・6/12上場・6/16日銀）に向け、円高地雷が点灯するフェーズへ移行。

### Key Levels (snapshot-based)
- US100: 30,333 / AI押し目買い継続 / 高値追わず
- JP225: 66,351 / 67,500円視野 / 量子・防衛・AI関連が買い対象
- USDJPY: 159.27 / 160円が壁 / 当面円安バイアス / 6/3～6/16で円高地雷
- WTI: 87.36 / 停戦観測で下落も戦争継続見立て / 92.48超えから上昇利用可
- XAUUSD: 4,560.50 / 4,500ドル方向の上昇利用 / 騙し的下落で調整可能性
- VIX: 15.32（低ボラ・Add risk gate open） / US10Y: 4.453（上昇トレンド） / BTC: 73,536

### Gates（最重要：終値で判定）
- Add risk: OPEN（VIX<18）ただしイラン情勢突発報道に注意
- Reduce risk: US10Y>4.4%定着 / JP10Y>2.9% / US100 D1 close<29,900 / VIX>22
- Hedge gate: Gold保有継続 / BTC戻り売り警戻 / 6月大型触媒準備

### This Week Focus & Catalysts（行動: 6/1-）
- **6/3（火）植田総裁講演**: 円高地雷点灯の第一シグナル。インフレ期待・利上げ示唆を注視
- **6/12（木）SpaceX上場**: AI・量子テーマの最大触媒。上場まで買い目線継続
- **6/16（火）日銀金融政策決定会合**: 利上げ0.75→1.00%ほぼ確実。円高加速始動
- **イラン停戦確定or否定**: 最重要判断。否定時に原油反発も株式へのインパクト限定的か
- **BTC量子ニュース**: ブロックチェーン暗号解読リスク。ニュース次第で下落加速可能

---

## Weekly Brief | 2026-6-5_wk01（2026-06-01 → 2026-06-05）
created: 2026-06-07 (JST)

### Macro / Regime
- Regime: Neutral（equities=flat / volatility=normal / oil=range / gold=off / crypto=weak / yields=rising）← wk05「AI・量子テーマ主導」から **NFPサプライズ起点のリスクオフ・whipsaw** へ内部転換。equities up→flat・gold range→off・crypto range→weak。
- **NFP 172Kショックで相関転換**: 予想85K＋上方修正で "good news is bad news"。原油安でも利回り上昇。年内利上げ確率50.5%→72.7%、US10Y4.5%超・30年5%超。
- **半導体distribution主導の株安**: Nasdaq総合-4.18%（2025年4月以来最悪）・9週連騰ストップ。Broadcom-12%。CAPE 1.9σ割高×US10Y4.5%超のデュレーション直撃。
- **円キャリー巻き戻しが全資産の増幅器**: ドル円160介入水準。BOJ 6/15-16利上げ観測80%。円ショート満タン-114.7K・MS推計$500B+で部分巻き戻し中。
- **VIX急騰**: 21.51で6/5単日+39-40%。Add risk gate閉・Reduce risk〔VIX>18〕成立。

### Position / Orders
- Core: Gold CFD残ポジは4390で全撤退済（防衛的）→ $4,250-4,300のソブリン買いゾーンで分割買い場待ち。
- Mode: 6/16-17ダブル中銀まで観測優位・ポジション軽く。米株/日本株/BTCは戻り売り・ヘッジ優位。
- USDJPY: 160売りは介入取りの高勝率だが介入なしだと踏まれる両刃。ノーポジ推奨ゾーン。

### Key Levels (snapshot-based / 2026-06-07)
- US100: 28,957（wk05比-4.5%）/ 戻り売り / S=27,989赤丸（最終防衛）/ R=29,900
- JP225: 金曜終値の実測なし（5/7 ATH 62,833言及のみ・最も脆い）/ 6/16利上げで8-12%調整シナリオ
- USDJPY: 160.293（キングピン）/ R=160.5-162 / S=159.50→156→155
- WTI: 90.540 / $88-95レンジ
- XAUUSD: 4,365.30（2026年安値・gold=off）/ S=4,336→4,300/4,250（ソブリン買いゾーン）/ R=4,450→4,508
- VIX: 21.510（>18 gate閉）/ US10Y: 4.536（5%窺う）/ US2Y: 4.280 / BTC: 60,922（19ヶ月安値）

### Gates（最重要：終値で判定）
- Add risk: 閉（VIX 21.51>18）。再開＝VIX<18回帰 + 6/16-17ダブル中銀通過 + US100 27,989維持確認
- Reduce risk: VIX>18（成立中）/ US100 D1 close<27,989 / US10Y>4.6% / ドル円160実弾介入・円高カスケード / JP10Y>2.9%
- Hedge gate: Gold撤退済→$4,250-4,300分割買い場待ち / 長期ポートは一部利確・現金比率引き上げ意識

### This Week Focus & Catalysts（行動: 6/8-、6/16-17に向けて）
- **6/10（水）米CPI**: 上振れでUS10Y 4.7-4.8%トライ・利上げ織り込み加速
- **6/15-16 BOJ会合**: 25bp（以上）利上げ織り込み80%。1.0%＋タカ派で円高カスケード起点
- **6/16-17 FOMC（新議長Kevin Warsh初FOMC）**: ドット上方修正・利上げ語法リスク
- **ドル円160介入ゾーン**: 実弾介入で急激な円高フラッシュ（2024年8月は3週で円+10%）
- **半導体distribution伝播**: 6/10 Oracle決算が試金石。Russell2000+1.45%のGreat Rotation継続

## Weekly Brief | 2026-6-19_wk03（2026-06-15 → 2026-06-19）
created: 2026-06-20 (JST)
note: wk02（2026-6-12）はスルー。前々週 wk01 を比較基準（ボス指示 2026-06-20）

### Macro / Regime
- Regime: Neutral（equities=up / volatility=normal / oil=slump / gold=off / crypto=weak / yields=falling）← wk01「リスクオフ・whipsaw」から **6/16-17ダブル中銀通過＋停戦/ホルムズ再開でリスクオン回帰**（VIX 21.51→16.4・equities flat→up・yields rising→falling・oil range→slump）。
- **6/16-17ダブル中銀を通過**: FOMC 3.50-3.75%を4会合連続据え置き＋「利上げ予想に転換」のタカ派シフト（--news #3）。BOJ結果は1次資料に明示なし（創作回避）。
- **今週の新キングピン＝ドル円介入警戒**: 早朝161.80ピークは2024年4月29日の介入直前とほぼ同水準。月曜は米休場明けで薄商いの振り回し。
- **ホルムズ再開で株高・ドル高の綱引き**: 米イラン停戦＋ホルムズ再開でリスクオン。介入警戒が日本株・クロス円の上値を抑える。WTI-20.56%急落。
- **日経平均7万円超え**: 6/18終値71,053.49円（初の大台／--news #5）。上値危険ゾーン＝夏天井72,800青丸（2倍ルール）。

### Position / Orders
- Core: 長期コアは保有継続・積立。日経過熱・ドル円介入リスクで一部利確・現金比率点検。
- CFD: Gold CFD 2勝0敗・合計+7.40%（6/12建値4097→同日4197→6/18 4300の段階半値利確）。残1/4ロットを建値4097で週持ち越し。boss戦略4120-4060週足ネック反発買い（→4,230）。
- Mode: リスクオン回帰だが上値追い厳禁の綱引き。日経72,800-73,000青丸・NAS100 30,900で逆張り戻り売り。

### Key Levels (snapshot-based / 2026-06-20)
- US100: 30,406（wk01比+5.0%）/ レンジ / R=30,900逆張り短期 / S=29,900→28,957
- JP225: 6/18終値71,053.49円（初の7万円超え）/ 上値青丸72,800危険ゾーン / 73,000トライ後の急落警戒
- USDJPY: 161.289（ピーク約161.80）/ キングピン介入警戒 / R=162 / S=159.50→156→155
- WTI: 76.540（-20.56%・slump）/ 76.2/78.83自律反発条件付き
- XAUUSD: 4,172.90（gold=off）/ 4120-4060週足ネック反発買い→4,230
- VIX: 16.400（<18 Add risk gate再開）/ US10Y: 4.487（4.6%が重い・S=4.195）/ US2Y: 4.213 / BTC: 62,896（下落相場・66,200割れ→60,700）

### Gates（最重要：終値で判定）
- Add risk: 再開（VIX 16.4<18）。ダブル中銀通過＋停戦/ホルムズ再開でリスクオン回帰。ドル円介入警戒・米休場明け薄商いで上値追い慎重・分割限定
- Reduce / caution: ドル円161.80超で実弾介入/レートチェック→円高フラッシュ / JP225 72,800-73,000青丸拒否で急落 / US100 30,900拒否・D1 close<29,900 / US10Y>4.6%上抜け / VIX>18再上昇
- Hedge gate: 金は4120-4060週足ネック反発買い（→4,230）。CFDゴールド半値持ち越し。BTCは戻り売り目線・監視中心

### This Week Focus & Catalysts（行動: 6/22-）
- **ドル円161.80介入ゾーン**: 実弾介入orレートチェックで急激な円高フラッシュ（2024年8月は3週で円+10%）
- **日経72,800-73,000青丸**: 上値危険ゾーン・73,000トライ後の急落シナリオ（2倍ルール）
- **NAS100 30,900**: 火傷ゾーン・30,900周辺で一旦の下落を利用する逆張り短期
- **US10Y 4.6% / JP10Y 2.65%上抜け**: ドル円上値・円高反転タイミングの節目
- **米イラン協議再燃**: 6/19延期＝停戦継続も火種残る。ホルムズ再封鎖懸念で原油・金が反発

## Weekly Brief | 2026-6-26_wk04（2026-06-22 → 2026-06-26）
created: 2026-06-27 (JST)
market_theme: Risk-on reversal → Equities Down × PCE 4.1% sticky + Goolsbee hawkish × Mag7 memory-cost passthrough selloff × Iran re-escalation × USDJPY 162 intervention-watch

### Macro / Regime
- Regime: **Equities Down**（equities=down / volatility=normal / oil=slump / gold=off / crypto=weak / yields=rising）← wk03「リスクオン回帰（equities=up / yields=falling）」から **株安・金利上昇方向へ反転**。VIX 16.4→18.41で18超え再上昇＝Add risk gate再閉鎖。
- **利上げ警戒の再点火**: PCEデフレーター4.1%高止まり＋グールズビー総裁「物価上昇圧力は引き続き高すぎる」。FRB年内利上げの可能性が米金利上昇圧力・株高一服の根拠（yields=rising）。
- **Mag7メモリ転嫁の株安**: Appleがメモリ供給不足のコスト上昇で一斉値上げ（--news #4）。マグ7全面安 vs メモリ株（マイクロン等）逆行高の二極化。
- **米イラン再エスカ**: 米軍イラン爆撃→イラン報復・湾岸米軍基地攻撃＋ホルムズ商船攻撃（--news #1 #2）。wk03の停戦/ホルムズ再開から逆戻り。WTI反発も勢い弱い。
- **ドル円162レンジ・介入警戒継続**: 160後半〜162「上がったら売る」。162.20-162.50上値メド。片山/佐々木×ベッセント協議報道が急落トリガー。

### Position / Orders
- Core: 長期コアは保有継続も、利上げ警戒・株安方向でMag7偏重の点検・現金比率の見直し。米株は当面買わず、日本株（半導体/メモリ）は割安感（PER 21→18）で相対優位。
- CFD: 当週確定トレード0件。ゴールド残1/4（=0.5Lot・建値$4,097）を建値で泳がせ＋6/25 $3,992で1Lotロング追加（15m DT上抜け確定）を週持ち越し（boss大底圏押し目買い・3,930→4,000）。週足Fibo38.2（$4,060）上抜けで保有延長、TP$4,200/SL$3,960。
- Mode: 戻り売り優位。NAS100 28,957割れ→28,600下抜け想定・29,626超えで限定上昇のみ逆張り。日本株半導体と金は押し目買い。BTCは売り継続。

### Key Levels (snapshot-based / 2026-06-27)
- US100: 29,118（wk03比-4.2%・equities=down）/ 28,957割れ→28,600 / R=29,626超えで限定上昇
- JP225: 金曜終値の実測なし（boss：米株より明確に強い・72,600超え上昇期待・PER 21→18）
- USDJPY: 161.805（160後半〜162「上がったら売る」）/ R=162.20-162.50 / S=161.55 / 介入警戒・非対称（IMF残弾1発＋6/23協調会談／協調弾なら155方向・単独/出る前は161-162で踏まれる・NY連銀rate check判定）
- WTI: 69.230（-22.13%・slump）/ 地政学反発（勢い弱い）vs 供給回復（UAE85%・waiver・タンカー再稼働）の綱引き / 68.89割れ→$66.235最終サポート（Cushing在庫タイト次第）
- XAUUSD: 4,078.70（gold=off）/ boss大底圏で押し目買い・3,930→4,000 / CFD 6/25 $3,992ロング追加 / 床=週足Fibo38.2 $4,060（旧$4,250-4,300は6/24無効化）、終値$4,060割れで越週ポジ撤退・TP$4,200/SL$3,960
- 2s10s: +22.6bp（wk03 +27.4bp比フラット化・ベアフラットニング＝短期↑/長期↓） / VIX: 18.410（>18 Add risk gate再閉鎖）/ US10Y: 4.451（低下・4.6%が重い）/ US2Y: 4.225（利上げ警戒で上）/ BTC: 59,722（下落相場・56,869割れ→56,000）

### Gates（最重要：終値で判定）
- Add risk: 再閉鎖（VIX 18.41>18）。株安・利上げ警戒・イラン再エスカでボラ復元。18割れ回帰でリスクオン復元の綱引き
- Reduce / caution: VIX 18超え定着 / ドル円162台で実弾介入/レートチェック（協議報道）→深夜帯の円高フラッシュ / NAS100 28,957割れ→28,600下抜け / 米イラン交戦の拡大（覚書履行危機）
- Hedge gate: 金は大底圏で押し目買い（3,930→4,000）。CFDゴールド残1/4（=0.5Lot・建値$4,097）＋6/25 $3,992の1Lot追加を持ち越し（週足Fibo38.2 $4,060上抜けで保有延長・TP$4,200/SL$3,960）。日本株は半導体/メモリ押し目買い。BTCは売り継続

### This Week Focus & Catalysts（行動: 6/29-）
- **VIX 18上抜け定着**: 終値で18上抜け定着＝Add risk gate再閉鎖確定・Reduce再発火。18割れ回帰でリスクオン復元
- **ドル円162介入ゾーン**: 162.20-162.50からの戻り売り。協議報道で深夜帯の円高フラッシュ（24:30以降なし）
- **NAS100 28,957 / 29,626**: レンジ下抜け→28,600 vs 限定上昇フィボ0.5。マグ7は当面買わず・メモリ株は逆行高
- **米イラン交戦の行方**: 米軍イラン爆撃／イラン報復／ホルムズ商船攻撃（覚書履行危機）。原油・金上振れ・リスクオフ加速の火種
- **FRB高官発言**: グールズビー/カシュカリ/ウィリアムズ。PCE4.1%高止まりで利上げ警戒の週明けギャップ

---

# Trade-Main.md | GM Playbook (Week Start)
updated: 2026-07-04 JST

## Weekly Brief | 2026-7-3_wk01（2026-06-29 → 2026-07-03）
> 7/3米独立記念日で米市場は早期クローズ/休場＝薄商い。distilled: [distilled-gm-2026-7.md](../distilled/2026/distilled-gm-2026-7.md)

### Macro / Regime
- 機械regime **Equities Down** 継続だが内部品質転換。株安主因が wk04「PCE利上げ警戒＋Mag7メモリ転嫁」→ wk01「**韓国発の半導体AI個別材料**」へ入れ替わり（Anthropic×SamsungのAIチップ提携・競合報道＋韓国アルゴ取引規制→流動性低下・コスピVIX相当高止まり）。半導体以外は底堅く非半導体へシフト。
- 木曜雇用統計+5.7万（大幅未達）で利上げ観測やや後退も株安主因でない。**VIX 18.41→16.15で18割れ＝Add risk gate再開**。週次はUS100+0.7%・BTC+3.0%小反発。boss＝『深く下がったら買い』の押し目スタンス、半導体AIは戻り売り。

### Key Levels & Positions
- US100: 29,329（トライアングルレンジ）/ **29,089=両義の節目**（割れで加速 vs 押し目好機）/ 半導体AI戻り売り・非半導体シフト
- JP225: 69,744（今週初の機械実測・強トレンド・structure_led）/ boss想定65,840→67,179（実測は想定より上＝要確認）
- USDJPY: 161.337（本流円安の戻り高値売り）/ **R=162.268上抜けでトレンド転換** / 薄商いで覆面介入リスク
- Gold: 4,187.3（gold=off継続もboss中期上昇維持）/ 4129フロー・4193上抜けで戻り / **CFD 6/29 $4,041で1Lot利確(+1.28%)＋Total 1Lot週持越し（残0.5Lot建値$4,097＋7/1 $3,990で0.5Lot）・今週から日足環境足/4Hトレード足スウィング運用へ切替（4Hダウ崩れ15m実体確定で決済）**
- WTI: 68.78（-26.07%・slump）/ 68.80上抜け確認待ち→70.16
- BTC: 61,485（+3.0%・range）/ 60,300方向調整・AIチップ暗号解読リスク思惑で反発ロング見送り
- 金利: US10Y 4.372（順イールド+0.35%維持）/ **2s10s bull_flattening(5s10s +24.2bp)**＝長期低下主導 / 3m10s +70.9bp/positive・belly_elevated継続 / VIX 16.15（18割れ・Add risk gate再開）

### Gates（最重要：終値で判定）
- Add risk: **再開**（VIX 16.15<18）。株安が半導体個別要因＋雇用未達で利上げ観測後退がボラ低下に寄与。薄商い明け・介入警戒でスパイク余地
- Reduce / caution: VIX 18再上抜け定着 / ドル円162.268上抜け後の急反落（覆面介入） / US100 29,089割れの下落加速 / 韓国発半導体AI competition懸念の他資産波及
- Hedge gate: 金は戻り売り基本（4129フロー）＋中期押し目買い維持。CFDゴールドTotal 1Lot週持越し・日足環境足/4Hトレード足スウィングへ切替。日本株は強トレンドで相対優位。BTCは反発見送り

### This Week Focus & Catalysts（行動: 7/6-）
- **US100 29,089**: 両義の節目。割れで下落加速 vs 押し目買い好機。月曜寄り〜前場で割れなら分割押し目買い準備
- **ドル円162.268**: 上抜けでトレンド転換シグナル。薄商いで覆面介入（サプライズ円買い）フラッシュ警戒
- **韓国発半導体AI続報**: Anthropic×Samsung AIチップ提携・競合の続報。半導体AI distribution波及＋BTC暗号解読リスク思惑の火種
- **米独立記念日明けの薄商い**: 出来高減でテクニカル機能しにくい・週明けボラ
- **17時ラガルドECB総裁発言**: EURUSD急変動リスク

---

# Trade-Main.md | GM Playbook (Week Start)
updated: 2026-07-12 JST

## Weekly Brief | 2026-7-10_wk02（2026-07-06 → 2026-07-10）
> distilled: [distilled-gm-2026-7.md](../distilled/2026/distilled-gm-2026-7.md) / Boss: wr-2026-7-10.md

### Macro / Regime
- 機械regime **Equities Down → Neutral**。equities=flat / yields=rising / oil=range / VIX 15.03で Add risk 継続開放。
- boss主筋：**寄り天(午前天井)→一旦調整／為替レンジ**。メモリ・半導体買い戻し＋金曜時点イランリスク後退。最大イベント **7/14 米大手銀行決算**。
- --news(7/12)：米軍イラン空爆再開・ホルムズ閉鎖＝Boss金曜との**時間差**を監視。

### Key Levels & Positions
- US100: 29,825（wk01+1.7%）/ 三角持ち合い・寄り天→戻り売り
- JP225: 68,558（wk01-1.7%・30d+3.8%）/ 押し目~67,358 / mixed RS
- USDJPY: 161.672 / **intervention=watch** / 不意打ち介入警戒
- Gold: 4,104 / 4138→4175・押し目4080 / **CFD Total 1.5pips @4104.5 週持越し**
- WTI: 71.41 / 72.17・71.23 両サイド
- BTC: 64,127（+4.3%）/ 61477割れのみ下落利用
- 金利: US10Y 4.569 / US2Y 4.308 / 3m10s +87.4bp positive / VIX 15.03

### Gates
- Add risk: **開放継続**（VIX15）。寄り天優先で高値追わず
- Reduce: VIX18再上抜け / 介入フラッシュ / ホルムズ継続 / 銀行決算失望 / 三角下抜け
- Hedge: 金1.5pipsを4Hダウ崩れ管理。原油は両サイド

### This Week Focus（行動: 7/13-）
- **7/14 米大手銀行決算**
- **CPI / PPI**
- **USDJPY 介入 watch**
- **イラン・ホルムズ続報**
- **Gold 4138 / 4080 / CFD 4H決済ルール**

