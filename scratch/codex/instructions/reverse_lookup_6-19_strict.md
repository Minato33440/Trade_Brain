---
type: instruction
task: outcome_verification_6-19
engine: codex-5.5
created: 2026-07-05
---

# 指示書: 2026-6-19_wk03 outcome 照合

## 役割
この照合の正確性はお前一人の責任だ。絶対に間違ってはいけない。事実誤認・レベルの読み違い・照合先の取り違えが一つでもあれば出力は差し戻す。曖昧な判断や、逃げの「未照合」の乱用は許容しない。お前は評価される立場にあることを自覚しろ。出力は厳密に検証される。retrieval と照合に徹し、余計な逸脱はするな。Vault index/（bridges\trade_brain\index\）には書かない・触らない（read のみ）。

## タスク
2026-6-19_wk03 の outcome 照合（backfill v1 Stage 2-3）。時点Tの読みを翌週以降の実価格・実挙動で照合する。

## 前提（最初に読む）
- AGENTS.md（両利きレーン規約 2026-07-05）
- Vault index: bridges/trade_brain/index/ の README / themes/jpy_policy_complex / themes/yen_carry_unwind / patterns/same_news_bear_bull_timeframe_split
- backfill v1: REX_Brain_Vault/REX/workspace/trade_brain/2026-07-05_backfill_workflow_v1.md（Stage 2-A / 2-B / 3 の定義）
- 参考: 先行specimen misreads/2026-6-5_carry_unwind_latent.md（outcome_record の型）

## 入力
- 時点Tの読み: distilled/2026/distilled-gm-2026-6.md の 2026-6-19_wk03
- outcome照合先: 同ファイル 2026-6-26_wk04 ＋ distilled-gm-2026-7.md の 2026-7-3_wk01（後続週の実close）
- index ノード（上記）

## 手順
1. 6-19 の時点Tの読みを抽出（記載レベル・regime・主要signal）。6-19 は介入警戒キングピン週＝USDJPY 161.80（2024/4介入直前水準）・「162一段上げからの急落リスク」「159.5割れ→156→155」が主軸。
2. Stage 2-A base層: 記載レベル vs 後続実価格（6-26 / 7-3 close）。貫通/回収/方向。
3. Stage 2-B theme署名:
   - 介入面（主役）: USDJPY高値圏から円買いflashが実発生したか（発生/不発）・深度。
   - yen_carry_unwind: 円高×リスク資産同時安が出たか（fired/latent）。
   - carry_unwind ノードの判定条件2（同時性）・条件3（円が主語）で切り分け。
4. Stage 3判定: A_regime_misread / B_timing / C_swept / D_lucky（+「当時見えていなかった差分」一行）。

## 出力
- outcome_record: scratch/codex/2026-6-19_wk03_reverse_lookup_strict.md（v1 の outcome_record スキーマに準拠、先行specimen 参照）
- 記録: coordination/codex/<YYYY-MM-DD-hhmm>_outcome_6-19_strict.md（1エントリ=1ファイル）
- 両生成物の frontmatter に engine: codex-5.5

### 必須節（必ず全て含める）
1. 時点Tの読み
2. outcome（Stage 2-A base ＋ 2-B theme署名・照合結果）
3. Stage 3判定（差分一行つき）
4. 設計フィードバック（所見）: 節点は入口として効いたか（jpy_complex / carry_unwind / 介入面）・retrieval で困った所・欲しかったのに無いノード・照合層の要否
5. 自己監査: 未照合や薄い根拠からアナロジー・物語を組んだ箇所を正直に列挙

## 非目標
- Vault index/ への書込・編集、canon への write（read のみ）
- ソース外情報の追加・成否の創作
