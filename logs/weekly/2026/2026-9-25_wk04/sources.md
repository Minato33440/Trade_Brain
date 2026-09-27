---
week: 2026-9-25_wk04
created: 2026-09-27
engine: gpt-6
status: source_reviewed
---

# 出典・採否・時点

価格の一次資料はBoss提供の当週チャート、CFD執行はBossの[trade_results](trade_results.md)、口座は9/26 20:42–20:43の3画面。画像原本とアーカイブのSHA-256は[入力manifest](charts/input_manifest.json)。当週レポートの原版は[boss_report_original](charts/boss_report_original.md)として保全した。

|ID|資料|採用範囲・制限|
|---|---|---|
|B1|[Boss週末レポート](charts/boss_report_original.md)|市況見立て・市場別条件。ニュース確認時点9/26 13:47 JST。レポート内の外部ニュースは出典を付ける|
|B2|[CFD結果](trade_results.md) / [証跡](charts/trade_evidence_manifest.json)|Gold当週決済0、1 Lot持越し、4,230基準・4,220注文水準。実際の注文設定画面・時刻・契約倍率は未確認|
|B3|[画像索引](charts.md)|市場14枚（US2Y重複1枚を含む）＋指標1枚＋口座3枚。Gold 1Hは別途アーカイブ。売/買気配を終値にしない|
|B4|[BTCチャート](charts/BTCUSD-2026-09-26.png)|Bossレポート執筆後に提供されたBinance画像。9/26撮影時点の84,153.73。画面には14:14:08と表示、タイムゾーンの独立確認はなし。9/25確定終値とは呼ばない|
|M1|[取得記録](charts/market_run.json) / [stdout](charts/market_stdout.txt)|`main.py --trade --news`を1回実行しexit 0、stderr空。市場系列は個別as_ofを先に読む|
|M2|[snapshot](charts/2026_09_27_snapshot.yaml)|`Neutral`、USDJPYのみ9/26、通常市場は9/25でSPLIT。BTCは24/7別枠。過去値改訂11件は現窓の表示であり、前週16件の消滅を意味しない|
|M3|[口座計算](portfolio_basis.json)|12銘柄の数量・評価額・評価損益と前週比を照合。スイープ+63円の原因は未確認。FX寄与は画面の丸め値からの会計分解|
|M4|[CLI集計](audit/trade_cli_summary.txt)|9/21〜25開始日で0件。Boss報告も当週新規/決済0。原本をCLI出力で置換しない|
|N1|[Yahoo RSS出力](charts/market_stdout.txt)|9/27取得の4件。イラン案拒否は報道として採用、供給損害や公式合意破棄と推定しない。市況レポートの9/26 13:47 cutoffより後の取得|
|X1|[Hermes Grok生出力](charts/grok_stdout.txt)|X検索で原投稿候補3件。原投稿は別経路で3件ともHTTP 403、本文・正確時刻・engagementは独立再確認できず。Xの主張を政策事実・入札統計・介入実施に昇格しない|

## 外部一次資料の照合

- [FRB 9/16声明](https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm): 25bp引上げ、目標3.75–4.00%、12対0。次回の決定は未確定。
- [日銀 9/18決定](https://www.boj.or.jp/mopo/mpmdeci/mpr_2026/k260918a.pdf): 1.25%程度、7対2。新方針は9/24から適用。今後の時期・速度は条件付き。
- [BEA 8月PCE次回案内](https://www.bea.gov/news/2026/personal-income-and-outlays-july-2026): 9/30 08:30 EDT＝21:30 JST、年次改定も同日。結果・予想値はここから作らない。
- [BLS 10月公表予定](https://www.bls.gov/schedule/2026/10_sched.htm)、[日銀公表予定](https://www.boj.or.jp/about/calendar/index.htm)、[Micron IR](https://investors.micron.com/news/press-release/2026/Micron-Technology-to-Report-Fiscal-Fourth-Quarter-Results-on-September-30-2026/default.aspx): 行動週のイベント時刻を確認するための資料。

イラン停戦案拒否はBossレポートのWSJ公開部分とReuters続報、当週`--news`のRSSが報じる内容として記す。今回WSJ本文を直接開けず、正式合意文、実際の通航量・供給損害の一次確認はない。Xが返した「米5年入札の海外比率」や「片山発言の文言」は公的原文に突合できず、条件判断に採用しない。

## 比較窓の境界

- Boss市場画像：9/26ファイルの各社チャート表示。株価指数CFD、金スポット系、WTI cash、TVC利回り、Binance BTCは商品・取引時間が異なる。
- 機械Yahoo系：US100/JP225/Gold futures/WTI futures/金利/VIXは9/25、USDJPYは9/26。金4,321.200は`GC=F`、BossのPepperstone4,284.99の代替終値にしない。
- FRED：2s10sは9/24、BEは9/25。3MをフロントにしたYahooカーブは利上げ期待判定に使わない。FREDとTVCを1系列に接続しない。
- 口座：東証ETFは日本引け、米株は米市場、口座画面は9/26夜。共通の同時刻リターンや証券口座の売買履歴をこの3画面だけから作らない。
