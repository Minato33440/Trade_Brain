---
type: coordination_handoff
subtype: reverse_lookup_dryrun
week: 2026-7-3_wk01
engine: codex-5.5
created: 2026-07-05-1531
status: completed
report: scratch/codex/2026-7-3_wk01_reverse_lookup_dryrun.md
outcome_status: unverified_all
---

# reverse_lookup_dryrun handoff — 2026-7-3_wk01

## 実施内容

`scratch/codex/instructions/reverse_lookup_dryrun.md` に従い、index 逆引き通し稽古を1回実施。

参照入口:

- `jpy_policy_complex`
- `yen_carry_unwind`
- `same_news_bear_bull_timeframe_split`
- RiskOff近傍文脈（現週の機械regimeは `Equities Down`）

参照した主な本文:

- `scratch/claude/2026-7-3_wk01_prediction_seed.md`
- `distilled/2026/distilled-gm-2026-7.md` wk01
- `distilled/2026/distilled-gm-2026-6.md` 6-5 / 6-19 / 6-26
- `distilled/2026/distilled-gm-2026-5.md` 5-1 / 5-8

## 一行判定

- 節点は効いたか: **効いた**。JPY複合→carry-unwind→AIニュース時間軸分裂の順で現在局面を引けた。
- 照合層は要るか: **強く要る**。outcome未照合でも6-5/6-19/6-26から十分もっともらしい物語が作れてしまう。
- codexで引けたか: **引けた**。ただし regime / ai_semi / us100_levels / vix_gate 未整備部分では distilled本文読解への手戻りが発生。

## Broker/Boss向けメモ

次に物理ノード化する候補としては、通し稽古上の摩擦から以下が有力。

1. `system/vix_add_risk_gate`
2. `themes/ai_semi`
3. `instruments/us100_levels`
4. `regime/Equities_Down` または `regime/RiskOff`
5. `patterns/thin_liquidity_flash_trap`（候補。米休場/薄商い/介入flash/節目sweep）

詳細は report を参照。
