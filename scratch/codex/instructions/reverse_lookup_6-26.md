---
type: instruction
task: outcome_verification_6-26
engine: codex-5.5
created: 2026-07-06
framing: neutral
---

# 指示書: 2026-6-26_wk04 outcome 照合

## 役割
retrieval と観測と照合を行う。設計判断はしない——粒度の是非は所見として Broker(claude) に返す。Vault index/（bridges\trade_brain\index\）には書かない・触らない（read のみ）。

## 照合品質の要件（最重要）
> 未確認を断定してはならない。資料から確認できないものは unverified / not_confirmed と明記し、
> その理由と、確認に必要な追加データを示すこと。**これは逃げではなく照合品質の一部である。**

- close ベースで intraday（ヒゲ・flash深度・日中の同時性）が見えない項目は、false でなく `unverified`（理由付き）とせよ。
- 6-26 の outcome 窓は短い（後続は 7-3 のみ、まだ1週）。4週先の判定は多くが未確定＝`unverified`が正常。無理に埋めるな。

## 独立判定（バイアス防止）
先行 misreads（[[2026-6-5_carry_unwind_latent]] / [[2026-6-19_intervention_carry_latent]]）は
outcome_record の**型の参照**にのみ使う。両週が latent だった事実に**引きずられず**、6-26 は自前の証拠で独立に判定せよ。
「latent の連続」を前提に置くな。fired の証拠があれば fired と書け。

## タスク
2026-6-26_wk04 の outcome 照合（backfill v1 Stage 2-3）。時点Tの読みを後続週の実価格・実挙動で照合する。

## 前提（最初に読む）
- CLAUDE.md（両利きレーン規約 / canon は read のみ）
- Vault index: bridges/trade_brain/index/ の README / themes/jpy_policy_complex / themes/yen_carry_unwind / patterns/same_news_bear_bull_timeframe_split
- backfill v1: REX_Brain_Vault/REX/workspace/trade_brain/2026-07-05_backfill_workflow_v1.md（Stage 2-A / 2-B / 3 の定義）
- 型の参照: misreads/2026-6-5_carry_unwind_latent.md / 2026-6-19_intervention_carry_latent.md

## 入力
- 時点Tの読み: distilled/2026/distilled-gm-2026-6.md の 2026-6-26_wk04
- outcome照合先: distilled-gm-2026-7.md の 2026-7-3_wk01（後続週の実close・現状これが唯一）
- index ノード（上記）

## 手順
1. 6-26 の時点Tの読みを抽出（記載レベル・regime・主要signal）。6-26 は regime=Equities Down、`carry_unwind_simultaneous_riskoff_2024_aug` タグ持ち。
2. Stage 2-A base層: 記載レベル vs 後続実価格（7-3 close）。貫通/回収/方向。確認できない先は unverified。
3. Stage 2-B theme署名:
   - yen_carry_unwind: 円高×リスク資産同時安が出たか（fired/latent）。carry ノード判定条件2（同時性）・条件3（円が主語）で切り分け。
   - 6-26 の株安の駆動が JPY か別要因（PCE/Goolsbee/Mag7/地政学等）かを、資料から確認できる範囲で切り分け。確認できなければ unverified。
4. Stage 3判定: A_regime_misread / B_timing / C_swept / D_lucky（+「当時見えていなかった差分」一行）。D_lucky を使う場合は「的中理由が読み通りか」を明示。

## 出力
- outcome_record: scratch/codex/2026-6-26_wk04_reverse_lookup.md（v1 の outcome_record スキーマに準拠）
- 記録: coordination/codex/<YYYY-MM-DD-hhmm>_outcome_6-26.md（1エントリ=1ファイル）
- 両生成物の frontmatter に engine: codex-5.5

### 必須節
1. 時点Tの読み
2. outcome（Stage 2-A base ＋ 2-B theme署名・照合結果。未確認は unverified＋理由＋必要データ）
3. Stage 3判定（差分一行つき）
4. 設計フィードバック（所見）: 節点は入口として効いたか・retrieval で困った所・欲しかったノード・照合層の要否
5. 自己監査: 未照合や薄い根拠からアナロジー・物語を組んだ箇所の正直な列挙

## 非目標
- Vault index/ への書込・編集、canon への write（read のみ）
- ソース外情報の追加・成否の創作
- 先行週の latent 結論への追従（独立判定せよ）
