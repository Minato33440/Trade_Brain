---
engine: claude
type: coordination_record
task: ab_adjudication_6-19
week: 2026-6-19_wk03
created: 2026-07-06
---

# 裁定記録: 6-19 A/B outcome_record — D_lucky 論点

## 論点
strict版(Output-1)は US100 の方向的中を D_lucky に採用。std版(Output-2)は D_lucky を棄却し
「主語が違う＝A_regime_misread」と整理。両 draft が status:draft で並存し distill 時に曖昧。

## 裁定（backfill v1 定義）
- **std版を正**。label = A_regime_misread（駆動の帰属）＋介入・carry latent。
- 理由: D_lucky は US100 下落を carry/JPY thesis の"lucky"的中として**再結合**する。これは carry_unwind
  条件2/3 が断つべき「thesis↔outcome 結合」の復活で、index の反・物語化設計と矛盾する。std は結合を断つ＝整合。
- strict の D_lucky 直感（方向的中は thesis を検証しない）は**教訓として保全**、昇格記録に記載。

## 処置
- 昇格: `bridges/trade_brain/misreads/2026-6-19_intervention_carry_latent.md`（std版を canonical化）
- supersede: `scratch/codex/Output-1-...SUPERSEDED.md`（strict版・rename marker）
- 決定: `REX/workspace/2026-07-06_broker_register_decision.md`（A/B資産化・再起動条件）

## 意義
6-5 に続く carry latent 第二事例＝6月通して carry は一度も fired していない、の所見に前進。
A/B は目的達成: 命令調は単発では推論を大きく歪めない／verification では中立フレーミングが honest hedge を守る。
