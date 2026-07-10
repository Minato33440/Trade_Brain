# 指示書: index/wrapup 生素材 事前抽出パス（週次実行の前に一度） — v2

## 役割
実行/抽出の帽子。抽出のみ行う。index/canon の設計判断はしない（Broker=Claude + Boss に戻す）。
Vault（C:\Python\REX_AI\REX_Brain_Vault\）には書かない。出力は下記 scratch\ / coordination\ のみ。
関所7.5の精神を抽出にも適用: ソース（boss市況 + 既存distilled）に忠実、外部情報の補完・創作禁止。

## 目的
週次実行の「前」に、時点Tの読みを結果が出る前に構造化捕獲する。
これが来週の outcome 照合（誤読/罠検出）の基準点になり、生成後 GM Strategy の関所7.5独立アンカーにもなる。

## 出力先（B案・平置きレイアウト）
- 抽出物2本 → `scratch\claude\`（engine別・使い捨て作業域）
- パスの記録・関所7.5照合ログ → `coordination\<pass>.md`（append-only・全engine共有）
  - **coordination への追記は append モードのみ**（write_file 全体上書き禁止＝履歴破壊防止）
- `logs\` には一切置かない（logs\=生データアーカイブに純化済み）

## 対象と出力

### Target A: 今週の前向きの読み → prediction-seed
入力: `logs\boss's-weeken-Report\<year>\wr-<YYYY-M-D>.md`（当週のboss市況のみ）
出力: `scratch\claude\<YYYY-M-D>_<week>_prediction_seed.md`（append-only）

全資産＋金利を構造化。**その週のboss市況に出た全レベル・全イベントを取りこぼさない**:
- instrument / regime読み / key_levels（値・方向・役割）/ pattern / signal / events / watch_trigger
- outcome_checkable: true/false（来週価格で機械照合できる読みか）
- trap_watch: true/false（薄商い・転換レベル等、sweep&reclaim が起きやすい地点か）
- 末尾に「来週の照合キュー」を同梱（outcome_checkable=true の項目を列挙）

※ レベル・イベントは各週の報告書から抽出する（前週の値を引きずらない）。

### Target B: 既存distilled → 統合 index feed
入力: `distilled\2025\` + `distilled\2026\` の確定済み全月ファイル（当週を除く）
出力: `scratch\claude\index_feed_raw.md`（append-only）

**粒度の注意（v1からの修正・実データ所見）**:
raw-tag は signal 141種でほぼ全単発 → **tag単独では連想ノードにならない**。
tag-起点の素朴な対応表は作らず、最初から**2軸で束ねる**:
- 第一軸 regime系譜: RiskOn / Neutral / GoldBid / RiskOff / RiskOff+EnergyShock
- 第二軸 theme束: iran_oil / gold / boj_hike / vix_gate / yen_intervention / us100_levels / yield_curve / ai_semi / btc

各週の close evidence（値）と regime ラベルを併記。成否は判明分のみ記載、未判明は「未照合」。
※ 新規判定を足さない。既存distilledに書かれている事実の再編のみ。theme分類は判断を含むので「規律内の再編」と明示。

**効率化（2回目以降）**: 初回で24週分の index_feed_raw は作成済み。
以降の週次は**当週の確定エントリを1件 append するだけ**。全24週の再走は不要。

## 非目標（やらないこと）
- Vault の index ノード構築（Broker=Claude の仕事、Boss許可制）→ `bridges\trade_brain\index\`
- 週次作業そのもの（main.py --trade --news 等）→ Boss が別途指示する
- ソース外の情報追加・相場解釈の上書き

## 報告
抽出完了後、Boss + Broker に: 抽出項目の要約 + 出力ファイルパス（2本）+ coordination ログのパスを短く報告して終了。

---

## 版数履歴
- **v2 (2026-07-04)**: 出力先を B案レイアウトへ修正（`logs\scratch\` → `scratch\`、抽出物=scratch\claude\ / 記録=coordination\ の分離）。coordination は append モード限定を明記。Target B の粒度を「tag対応表」から「regime系譜＋theme束の2軸」へ修正（141単発tag所見を反映）。2回目以降は当週1件appendのみに効率化。日付をテンプレ化し週次再利用可能に。
- v1 (2026-07-04): 初版。wk01(2026-7-3)実行時の出力先は logs\scratch\claude\、Target B は tag-起点対応表。全文は coordination ログ [1] に保存。
