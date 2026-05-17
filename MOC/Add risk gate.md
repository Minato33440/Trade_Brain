---
type: moc
concept: Add risk gate
tags:
  - moc
  - cfd_concept
---

# 🗺️ Add risk gate — MOC

> リスク追加可否ゲート（主に VIX<18 等の条件）の開閉履歴。frontmatter `add_risk_gate`（open/closed）も併せて参照。

## 該当週（自動集計）

```dataview
TABLE week AS "週", regime AS "Regime", add_risk_gate AS "Add状態", reduce_risk_gate AS "Reduce状態"
FROM #cfd_strategy
WHERE contains(file.outlinks, [[Add risk gate]])
SORT week ASC
```

## ゲート閉のみ抽出（要警戒週）

```dataview
TABLE week AS "週", regime AS "Regime", reduce_risk_gate AS "Reduce状態"
FROM #cfd_strategy
WHERE add_risk_gate = "closed"
SORT week ASC
```

## 補足
- 開条件の例: VIX<18 維持 ＋ 押し目確認 ／ 閉トリガー: VIX>18
- 関連: [[Reduce risk gate]] ・ [[リスクオン]] ・ [[VIX]] ・ [[レジーム]]

> Rex戦略データ正本は [[distilled-gm-2026-5|distilled]]。本MOCは人間用ナビゲーション。
