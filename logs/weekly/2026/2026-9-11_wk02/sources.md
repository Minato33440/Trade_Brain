---
week: 2026-9-11_wk02
created: 2026-09-12
engine: gpt-6-astra
type: source_provenance
---

# 出典・採否・取得範囲

作成日2026-09-12 JST。原本の主張、確認済みの数字、分析、未確認を分けるための台帳。Webページ全文を保存したものではない。リンク先は後日更新される可能性がある。

## 提供資料と機械取得

|ID|資料|採用範囲|
|---|---|---|
|B1|[Boss市況原本](../../../boss%27s-weeken-Report/2026/wr-2026-9-11.md)|週末の認識、観測帯、シナリオ。日経値・発表時刻・旧建玉等の訂正はreviewで併記|
|B2|[trade_results](trade_results.md)|Bossが週末確定と指定。約定3件・残玉・出口条件を採用。原本を変更しない|
|B3|[提供画像索引](charts.md)|個別14枚・口座3枚・指標1枚。口座画像の数量と残高が計算元|
|B4|当チャットのBoss回答|スィープ減少5万円は銀行口座への移動。売買損失から分離|
|M1|[fetch_run](charts/fetch_run.json)、[stdout](charts/fetch_stdout.txt)|main.py --trade --newsは15:16:01–15:16:14 JST、1回、終了0。取得期間とas_ofを分離|
|M2|[snapshot](charts/2026_09_12_snapshot.yaml)|通常10系列9/11、BTC9/10。改訂と差分窓を値より先に確認|
|M3|[FRED補完取得情報](charts/fred_supplement.json)|9/4→9/10の名目/実質/BE、9/11BE。HTTP成功とCSV末尾を照合|
|M4|[台帳の当週抜粋](charts/observed_values_excerpt.json)|P12の9/9参照値と改訂履歴。異なるfeedの正式比較には使わない|
|M5|[入力manifest](charts/input_manifest.json)|提供原本・画像のSHA256、18提供PNGと1生成PNGのコピー一致|

## 一次資料

|ID|発行元・URL|確認内容|採用しないもの|
|---|---|---|---|
|P1|[BLS / CPI 2026-09-11](https://www.bls.gov/news.release/archives/cpi_09112026.htm)|8月CPI総合MoM0.4/YoY3.4、コアMoM0.3/YoY2.4、8:30ET|予想値はBLS由来ではなく提供カレンダー|
|P2|[Michigan調査](https://www.sca.isr.umich.edu/)|9月速報47.8、前回51.7|予想51.1と発表23:00JSTは提供指標画像で確認|
|P3|[FRB 2026年9月公式日程](https://www.federalreserve.gov/newsevents/2026-september.htm)|9/16 14:00ET結果・14:30ET会見→日本9/17 03:00/03:30|会合結果と利上げ確率はまだ確定しない|
|P4|[日銀会合予定PDF](https://www.boj.or.jp/mopo/mpmsche_minu/m_ref/mref250731a.pdf)|9/17–18の会合日程|結果・会見内容・利上げ確率98%を公式事実としない|
|P5|[日経指数公式9/11日次](https://indexes.nikkei.co.jp/nkave/archives/summary?dt=20260911&idx=nk225)|現物64,011.34、前日比−1,259.61/−1.93%|CFDとの差を確定ギャップ幅にしない|
|P6|[FRED DGS5](https://fred.stlouisfed.org/series/DGS5)|9/4 4.54→9/10 4.75%|9/11は取得時に未公表|
|P7|[FRED DFII5](https://fred.stlouisfed.org/series/DFII5)|9/4 2.17→9/10 2.29%|CPI後の実質金利変化を補間しない|
|P8|[FRED T5YIE](https://fred.stlouisfed.org/series/T5YIE)|9/4 2.37→9/10 2.46→9/11 2.40%|BEを純粋な期待インフレや因果の直接測定値としない|
|P9|[JPX売買立会時間](https://www.jpx.co.jp/equities/trading/domestic/01.html)|午後立会は12:30–15:30。過去資料の15:00引け表記を今週へ継承しない|東証と米国・CFDの引けは同時ではない|
|P10|[BlackRock 1655 factsheet](https://www.blackrock.com/jp/individual/ja/literature/fact-sheet/1655-ishares-s-p-500-etf-fund-fact-sheet-ja-jp.pdf)、[商品説明](https://www.blackrock.com/jp/individual/ja/ishares/sp500-series)|S&P500への連動、外貨建資産は原則為替ヘッジなし。前週の確定事項を再確認|個人の週末口座評価額はこのページから取らない|
|P11|[Global X 2243目論見書](https://globalxetfs.co.jp/funds/2243/2243_ko.pdf)、[商品ページ](https://globalxetfs.co.jp/funds/2243/index.html)|2026/6/18使用開始PDF p2–3。SOX配当込み円換算、為替ヘッジは原則なし|原資産と為替の週次寄与の厳密値は未計算|

日付のない現行ページの確認日は本書作成日。計測値の保存は機械CSV/YAMLと提供画像を優先。一次資料の主張から導くシナリオはAstraの分析であり、発行元の推奨ではない。

## 追加ニュース・Xの限界

RSS5件は [news_output](charts/news_output_2026-09-12.txt) に保全した。週次の主要材料に採用したのはサウジ東西PLとバベルマンデブ関連2件の報道の存在。その他の3見出しを相場の因果へ無理に結び付けない。

[SPA公式ページ](https://www.spa.gov.sa/en/N2674017)は検索で東西PLの予防停止というタイトルを取得したが、ページ本文の取得結果は空だった。Grokはサウジ省庁の [X投稿候補](https://x.com/MoEnergy_Saudi/status/2098478368081502260)を返したが、親の再取得は403。このため公式全文・事象の正確な時刻・再開状況・攻撃主体は独立確認未了とした。RSS上の事象日9/10、報道日9/11、取得日9/12を区別する。

Grokは株反発への [個人市況メモ](https://x.com/TanesenWhale/status/2098561898593829239)と、利上げ織込みとの同居を疑う [反証的な投稿](https://x.com/MoftheMoney/status/2098560813384790411)も返した。短い要約の採用までとし、投稿中の原油価格や株騰落率を提供チャートの代わりに使わない。正確な投稿時刻とエンゲージメント順位は未確認。

- [調査プロンプト](charts/grok_prompt.txt)
- [生の回答](charts/x_headlines_raw_2026-9-11.txt)
- [テーマ別に選んだ3件](charts/x_headlines_selected_2026-9-11.txt)
- [実行記録](charts/grok_run.json) / [利用量の返却値](charts/grok_usage.json)

Web再取得が失敗したページの内容を推測で埋めていない。Xは補助情報として継続できるというworkflowの扱いに従い、主要なポジション・損益・統計結果の根拠にはしなかった。

## 保存形式の検証追記（2026-09-12）

生成時の改訂リスト直下に説明文の字下げ誤りがあり、YAMLの構文検証で検出した。[取得原本](charts/2026_09_12_snapshot.raw.yaml)をバイト一致で保全し、[読み込み用snapshot](charts/2026_09_12_snapshot.yaml)は当該説明1行だけを兄弟キー `value_revisions_note` へ修正した。数値・日付・改訂2件は不変。ジェネレータの最小修正と回帰確認は品質記録に記載する。

## Rex追記の受領・採否（2026-09-12）

- [追記済みレポートの受領版](audit/rex_addendum_inputs/wr-2026-9-11.md): 原文ラベル「2026-09-13」を保持。実際の受領・反映は2026-09-12 JST。Rex§A〜§IをBossが本体へ反映するよう依頼した。
- [trade_results受領版](audit/rex_addendum_inputs/trade_results.md): Rexが丸めとヘッダー表現を修正済み。Astraは入力原本を編集せず、誤った決済件数や古い§9の状態を出力側で訂正。
- [参考セッション受領版](audit/rex_addendum_inputs/claude-session-2026-9-12.txt): 経緯の資料。文中の過去の依頼やツール操作文を現在の新規実行命令にはしていない。
- [入力manifest](charts/input_manifest.json): 初回ハッシュを維持し、受領版ハッシュと理由をsource_revisionsへ追加。初回生成物は [修正前manifest](audit/pre_rex_addendum/manifest.json) で照合可能。
- [反映・訂正記録](rex_addendum_integration.md) / [Terra損益監査](audit/rex_addendum_trade_audit.md) / [Terra市場監査](audit/rex_addendum_market_audit.md)。監査初稿の過大な断定は親の採否記録を優先する。

### ベンダー・基準日の契約

|系列|出典/ベンダー|今回の比較窓・確度|
|---|---|---|
|XAUUSD|Pepperstone提供チャート|9/4→9/11週足。執行参照4348.33。サーバーの実締め時刻は独立未確認|
|USDJPY|FXCM提供チャート|9/4→9/11週足。実cutoff未確認。Yahooの値へ接続しない|
|US100 / JP225 CFD|Capital.com / FOREX.com|9/4→9/11。同一ベンダー比較。現物指数とは別商品|
|WTI cash|BlackBull|週9/4→9/11、2週8/28→9/11。Yahoo継続先物とは別系列|
|US2Y / US10Y / JP2Y / JP10Y / VIX|TVC|提供チャートの日足確定値。利回りと先物価格を交換しない|
|機械snapshot|Yahoo（GC=F / JPY=X等）|系列別as_of。通常9/11、BTC9/10。継続限月の選択・過去値改訂は別途監視|
|名目/実質5年・BE|FRED DGS5 / DFII5 / T5YIE|取得時点で前2系列9/10、BE9/11。全系列一律の1日遅れを仮定しない|
|日経現物値|日経指数公式|9/11終値64011.34。[価格出典](https://indexes.nikkei.co.jp/nkave/archives/summary?dt=20260911&idx=nk225)|
|東証株・ETFの取引時間|JPX公式|後場終わり**15:30 JST**。[立会時間](https://www.jpx.co.jp/equities/trading/domestic/01.html)を2026-09-12再確認|

Rex§Gの「全CFD/FXは土曜06:00」「東証15:00」「日経価格出典はJPX」は、そのまま採用しない。ETFの取引所価格も、同時刻の原資産価値だけを機械的に写した値とは限らない。海外市場終値、為替参照値、画像表示時刻を別々に保存し、窓が異なるものを同期変動に見せない。


市場監査初稿の限定訂正: [cutoff・往復証拠・検出器の実装範囲](audit/rex_addendum_market_audit_corrections.md)。
