---
week: 2026-9-18_wk03
created: 2026-09-20
engine: gpt-6-astra
status: integrated_weekly_review
---

# 出典・採否・観測の境界

取得日2026-09-20 JST。ページの全文複製ではなく、主張ごとの確認記録。画像の値、政策事実、市場解釈、未確認を分ける。

|ID|出典|採用・制限|
|---|---|---|
|B1|[Boss市況原本](charts/boss_report_original.md)|当週の見立てと14銘柄の条件。外部事実は以下で再照合|
|B2|[CFD記録](trade_results.md)|Boss確定執行・stop変更・残玉。5M確定そのものは画像単独で検証していない|
|B3|[画像索引](charts.md)|当週14市場＋口座3＋15M。Astraが当週17枚と前ターン15Mを直接確認|
|B4|Bossの口座回答|数量変更なし。1655 NISA配当918円・9/17受渡の明細を後続で受領、現金差と照合済み|
|M1|[取得記録](charts/market_run.json) / [出力](charts/market_stdout.txt)|main.py --trade --news 1回・終了0。取得期間8/21〜9/20と個別as_ofを区別|
|M2|[snapshot](charts/2026_09_20_snapshot.yaml)|SPLIT、16改訂、rolling窓を保存。金の執行価格をGC=Fで置換しない|
|M3|[FRED補完](charts/fred_weekly_summary.json) / [取得行抜粋](charts/fred_public_csv_2026-09-20.txt)|DGS5/DFII5/DGS2/DGS10は9/17まで、BEは9/18まで。比較窓9/11→9/17を独立計算|
|M4|[入力保全manifest](charts/input_manifest.json)|初回入力SHAとアーカイブを検証。15M原本は別manifest|
|M5|[台帳追記](audit/csv_append_manifest.json)|当週部分利確のみ1行、既存bytes保持。CLIは開始日集計|
|P1|[FRB声明9/16](https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm)|25bp引上げ、3.75–4.00%、12対0。価格反応の単独原因にはしない|
|P2|[日銀9/18](https://www.boj.or.jp/mopo/mpmdeci/mpr_2026/k260918a.pdf)|1.25%、7対2、9/24適用。年内据え置き確約ではない|
|P3|[ECB9/10](https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2026/html/ecb.is260910~6a45359cfc.en.html)|25bp引上げ。9/18発言詳細と混同しない|
|P4|[JPX告知](https://www.jpx.co.jp/news/2040/20260918-01.html)|9/21–23対象デリバティブ祝日取引。各CFDの稼働を保証しない|
|P5|[BEA予定](https://www.bea.gov/news/2026/personal-income-and-outlays-july-2026)|9/30 08:30 EDT＝21:30 JST、8月PCE・年次改定|
|P6|[SPA9/19](https://spa.gov.sa/N2680557)|リヤド向け弾道ミサイル迎撃の発表まで。空港被害/原油供給損失は未確認。週末cutoff後|
|S1|Boss原本のReuters会談報道|9/24米中会談は報道ベースの予定。両政府の一次確認未取得|
|S2|[Farside](https://farside.co.uk/btc/)|Boss記載の金曜4.33億/週620万ドルは独立再集計未実施。補助記載に留め、売買根拠の必須条件にしない|

政策確認の詳細は[Terra市場監査](audit/wk03_market_source_audit.md)。9/19サウジ事案の厳密UTC時刻とNY引けの前後はソース時刻の追加照合余地があり、今週は「9/18金曜値確定後に取り込んだ週末材料」として価格理由に遡及しない。

## Agentの照合で直した点

- Luna初稿は当週でなく前週画像を抽出したため不採用。訂正版の当週数値はAstra目視と一致した。
- 訂正版も比較表では前々週の4,906,965を前週と取り違えていたため、その表は不採用。採用する前週末はmetaのcurrent値4,750,629。比較計算はAstraが再構築した。
- USD口座P/L、円口座P/L、FXCM終値は別基準。合算・すり替えしない。
- 金利同士の同日カーブまでSPLITで無効化しない。FXを使う相対強度の制限を対象に合わせる。

## X補助検索

[Grok依頼](charts/x_search_prompt.txt)は政策通過・円反転・週末原油供給リスクの原投稿3件に限定。結果の採否は後続のX検索照合欄へ記録する。投稿要約と引用先確認は別工程。



## X検索照合 — 9/20取得

Grok4.5／xai-oauthのワンショットが正常終了。依頼は3論点で、出力には反対材料を含む複数投稿が返った。原投稿URLはGrokのlive x_search結果に由来するが、Astraの直接取得は3件ともHTTP403となり本文の独立再確認はできなかった。**政策事実は公式ページで確認、Xは発言者の見方・追加調査候補として限定採用**する。

|テーマ|Grokが返した投稿・UTC時刻|内容と採否|
|---|---|---|
|FRB|[Mandeep Bhullar](https://x.com/mbhullar/status/2100286233742368893)・9/16 18:10:34 UTC|25bp/3.75–4.00%という主張はFRB公式と整合。higher-for-longerの解釈を声明そのものにしない|
|日銀・円|[Weston Nakamura](https://x.com/acrossthespread/status/2100796500356084094)・9/18 03:58:11 UTC|「反対票が円安原因」という単純説明への反論。介入がより重要という因果主張も未検証の市場解釈|
|週末原油|[Mario Nawfal](https://x.com/MarioNawfal/status/2101365705128255755)・9/19 17:40 UTC|フーシ派の攻撃・火災の主張を紹介。供給被害の確認ではない。SPAの迎撃発表・外交継続という反対材料と併記|

対立する投稿では利上げ後の株先物反発、被害未確定、外交継続も返った。支持投稿だけを抽出して原油上昇や円高を確定しない。いいね・RT数は返っておらず、注目度順位を付けない。投稿本文・タイムスタンプはGrok経由で、独立確認済みとしない。

Grokは9/18 20:00 UTC（NY現物16時）を便宜的な基準線に使った。この時刻は提供CFD/FX/金利の一律締め時刻ではない。9/19投稿は週末補足として使い、金曜価格の原因へ遡及しない。

[検索原出力](charts/grok_stdout.txt) / [実行記録](charts/grok_run.json) / [使用量](charts/grok_usage.json)。費用欄はcost_status=unknownで、estimated_cost_usd=0を無料と解釈しない。

## 2026-09-20 配当明細の後続確認

1655のNISA配当918円（3.4円×270口、税額0円、9/17受渡）をBoss提供明細で確認し、スイープ増加918円と全額照合済み。 口座週次増加117,679円＝保有評価差116,761円＋受取配当918円。[提供明細](charts/dividend_1655_2026-09-17.md)。画像未検出により残していた分類保留を解消した。
