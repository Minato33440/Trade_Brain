---
type: instruction
task: index_reverse_lookup_dryrun
stage: 1
engine: codex-5.5
skill_ize: false
created: 2026-07-05
author: Rex (Broker帽子 / Claude)
---

# 指示書: index 逆引き 通し稽古（一段目・codex 版・検証のみ・Skill化しない）

## engine
codex-5.5（Hermes Profile 起動）。生成物の frontmatter に `engine: codex-5.5` を必須。

## 役割（codex 向けに明示）
君は retrieval と観測だけを行う。逆引きを「一回だけ手で」通す。
- 設計判断はしない。ノード粒度の是非・分類の当否は「所見」として Broker(claude)+Boss に返す。
- Vault の index/（bridges\trade_brain\index\）には書かない・触らない（read のみ）。
- 成否は全て「未照合」。当たり外れを自分で確定しない。
- SKILL 化しない。手順の結晶化は証明後・二段目で Broker が行う。
この稽古の主目的は「ノードが実戦で効くか」＋「照合層なしで逆引きがどれだけ"もっともらしい物語"を作るか」の測定。

## 前提: 参照するガバナンスと構成
- 最初に AGENTS.md を読む（両利きレーン規約 2026-07-05 反映済み。canon は read のみ、
  scratch/coordination は Provider3分岐・新規/append 可・edit_file 禁止）。
- Vault: C:\Python\REX_AI\REX_Brain_Vault\bridges\trade_brain\
  index/
  ├── README.md   … 3 node-kind 枠（regime / theme / instrument / system ＋ 横断pattern）
  ├── themes/
  │   ├── jpy_policy_complex.md  … 介入＋BOJ経路＋carry の3面統合
  │   └── yen_carry_unwind.md    … 伝達帯（機械寄り判定3条件つき）
  └── patterns/
      └── same_news_bear_bull_timeframe_split.md  … 第一号
- 各ノードは distilled(canon) へ wikilink で戻る。distilled 本文は read のみ。
- 全ノードは outcome 未照合（backfill Stage2-3 未実施）。これは既知の前提。

## 入力
- 現在状態: scratch\claude\2026-7-3_wk01_prediction_seed.md ＋ 今週snapshot（distilled-gm-2026-7 の wk01）
- index ノード3本（上記）
- ノードが指す過去週の distilled 本文

## 出力先（両利き規約・codex レーン / 2026-07-05 命名）
- レポート: scratch\codex\2026-7-3_wk01_reverse_lookup_dryrun.md（新規作成）
- 記録: coordination\codex\<YYYY-MM-DD-hhmm>_reverse_lookup_dryrun.md（1エントリ=1ファイル・新規作成）
  ※ engine はフォルダ（coordination\codex\）が担うのでファイル名に codex_ は付けない。
  ※ 既存ファイルへの edit_file は禁止。coordination の共有単一ファイルへの追記もしない。
- 両生成物の frontmatter に `engine: codex-5.5` を記載。

## 手順（逆引き）
1. 現在状態の同定: prediction_seed から今の regime/theme を読む（RiskOff寄り・USDJPY162介入警戒・carry-unwind地雷・ai_semi弱強割れ）。
2. 入口選択: 該当ノードへ入る（jpy_policy_complex / yen_carry_unwind / same_news_bear_bull、regime=RiskOff）。
3. 過去週の引き出し: 各ノードが列挙する週から近いものを引く（特に 2024aug/apr replay 参照、直近の RiskOff/介入週＝6-26 / 6-19 / 6-5）。distilled本文で「当時どう読んだか・どんな設定だったか」を抽出。成否は未照合と明記。
4. 差分レポート生成: 「今 vs アナログ」。類似（なぜこのノードが引けたか）と反証（今回とアナログの違い）を必ずワンセットで。片側に寄せない。
5. 自己監査: どこで未照合のアナロジーから物語を組んだかを正直に列挙。

### レポート必須節
1. 現在状態の同定（入口に使った node と根拠）
2. 引けた過去週と各々の当時の読み（成否＝未照合を明記）
3. 差分（類似＋反証セット）… アナログとの違いを必ず併記
4. 設計フィードバック（Broker/Boss向け・所見であって判断でない）:
   - 節点の粒度: jpy_complex / carry_unwind は入口として 粗い / 適切 / 細い？
   - retrieval摩擦: 引く時に困った所・欲しかったのに無いノード
   - 照合層の要否: outcome未照合で逆引きがどれだけ物語化したか。backfill Stage2-3 が要る度合い。
   - ★engine差の所見: claude が設計した index を codex が入口から引けたか。記述が曖昧で引けなかった箇所（＝claude内部の暗黙知依存の疑い）を具体的に。
5. 自己監査（未検証アナロジーを組んだ箇所の正直な列挙）

## 非目標（やらないこと）
- SKILL.md 作成（証明後・二段目で Broker が起こす）
- Vault index/ への書込・編集（Broker/Boss canon）
- distilled 本文・canon への write（read のみ）
- アナロジーの強制・成否の創作・distilled外情報の追加
- ノード粒度の「修正」（是正は所見に留め、実施しない）

## 報告
完了後 Broker＋Boss へ: レポートパス ＋「節点は効いたか / 照合層は要るか / codex で引けたか」の一行判定。
