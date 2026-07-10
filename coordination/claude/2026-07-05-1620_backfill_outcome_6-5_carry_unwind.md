---
engine: claude
type: coordination_record
stage: "3→4"
task: backfill_outcome_specimen
week: 2026-6-5_wk01
created: 2026-07-05
---

# Stage 3→4 確定記録: 6-5 carry_unwind outcome 照合

## 実施
backfill v1 の specimen 第一号として 2026-6-5_wk01 の carry_unwind 読みを照合（Broker手動・canon: 6-19/6-26）。

## 判定
- fired_or_latent: **latent**（double CB 通過も円安継続＋US100ラリー＝クロス資産同時安なし）
- Stage3 label: A_regime_misread（方向）／ process-correct（監視のみ・pivot 指名は正）
- 4週窓後半の 6-26 リスクオフは PCE/Mag7/イラン駆動・円安のまま＝判定条件3で carry_unwind から除外

## 昇格（Boss承認 2026-07-05）
- 新規: `bridges/trade_brain/misreads/2026-6-5_carry_unwind_latent.md`（Vault）
- 更新: `bridges/trade_brain/index/themes/yen_carry_unwind.md`（outcome軸＋前方wikilink追加）

## 意義
carry_unwind の初 latent インスタンス。逆引きで 6-5 を risk-off 前例でなく「満載・不発」の反例として引ける状態に。
codex 一段目が名指しした「6-5→7-3 物語生成」に、outcome ラベルで反証を与えた。

## 次
残り 6-19 / 6-26 の照合（型は確定済み）→ その後 Python化を判断。
