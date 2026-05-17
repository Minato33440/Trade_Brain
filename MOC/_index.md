---
type: moc_index
tags:
  - moc
  - cfd_concept
---

# 🗺️ CFD戦略 概念MOC インデックス

`/gm-weekly` が週次ハブMD（`#cfd_strategy`）に打つ概念 wikilink を、Dataviewで自動集約するハブ群。
**Rex戦略データ正本は [[distilled-gm-2026-5|distilled]]。本MOC群は人間用ナビゲーション。**

> [!info] 動作条件
> Dataview コミュニティプラグインが有効な場合、各MOCの表は自動更新される。未導入時はコードブロックのまま表示（情報損失なし／導入で即有効化）。

## 概念MOC一覧

| 概念 | 説明 |
|---|---|
| [[リスクオフ]] | リスク資産回避局面の観測/想定週 |
| [[リスクオン]] | リスク選好局面の週 |
| [[Add risk gate]] | リスク追加可否ゲートの開閉履歴 |
| [[Reduce risk gate]] | リスク削減ゲートの発火履歴 |
| [[日銀利上げ]] | 日銀政策金利・利上げ観測の進展 |
| [[債券パニック]] | 国債利回り急騰・パニック売り局面 |
| [[ブラックマンデー]] | 週初急落（想定/実現）局面 |

## 全CFD戦略ハブ（時系列・自動）

```dataview
TABLE week AS "週", regime AS "Regime", add_risk_gate AS "Add状態", reduce_risk_gate AS "Reduce状態"
FROM #cfd_strategy
SORT week ASC
```

> 新概念が canonical 確定したら本インデックスに追記し、対応MOCを `MOC/` に新規作成する（`/gm-weekly` 手順7.6 のルール）。
