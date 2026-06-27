# docs/system/ — システムの年輪（System Annals）

このディレクトリは、**Rex（機械側の市況直感）や運用が間違え、その間違いが知識アーキテクチャを進化させた記録**を残す。
通常のバグ修正ログではない。「誤り → 構造への変換 → 恒久化」の瞬間だけをここに刻む。後年の Rex / Advisor / ボスが、システムがどこで踏み外しどう育ったかを辿れるようにするためのもの。

## 残す基準

- Rex の市況判断・指標の読みが、実測 or 上位の構造論で**反証**された
- その反証が prompt の手当てではなく**データパイプライン（knowledge architecture）側の常設項目**に変換された
- 結果として同種の誤りが**構造的に再発しなくなった**

## 命名

`YYYY-MM-DD_<短い主題>.md`（frontmatter に `type: system_annal`）

## 年輪一覧

- [2026-06-27 — Rexの金利直感が3点立体カーブで反証され、belly_elevated として恒久化された日](./2026-06-27_belly-elevated_rex-curve-error.md)
  — 5s10s 2層に潰して「フラット化＝逆イールド近い」と早鳴り → 3点(3M/5Y/10Y)で belly(5Y) の"再利上げ織り込みの瘤"と判明。`recession_3m10s` を主ゲージに、`curve_2s10s`3点立体・`relative_strength`・介入`coord_stage`4段を恒久化。
</content>
