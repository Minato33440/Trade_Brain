---
type: moc
concept: Reduce risk gate
tags:
  - moc
  - cfd_concept
---

# 🗺️ Reduce risk gate — MOC

> リスク削減ゲート（US10Y>4.4%定着 / VIX>22 / JP10Y>2.9% 等）の発火履歴。frontmatter `reduce_risk_gate`（clear/triggered）も併せて参照。

## 該当週（自動集計）

```dataview
TABLE week AS "週", regime AS "Regime", add_risk_gate AS "Add状態", reduce_risk_gate AS "Reduce状態"
FROM #cfd_strategy
WHERE contains(file.outlinks, [[Reduce risk gate]])
SORT week ASC
```

## 発火（triggered）週のみ抽出

```dataview
TABLE week AS "週", regime AS "Regime", add_risk_gate AS "Add状態", reduce_risk_gate AS "Reduce状態"
FROM #cfd_strategy
WHERE reduce_risk_gate = "triggered"
SORT week ASC
```

## 補足
- 発火条件の例: US10Y>4.4%定着 ／ JP10Y>2.9% ／ US100 D1 close 割れ ／ VIX>22
- 関連: [[Add risk gate]] ・ [[リスクオフ]] ・ [[債券パニック]] ・ [[US10Y]]

> Rex戦略データ正本は [[distilled-gm-2026-5|distilled]]。本MOCは人間用ナビゲーション。
