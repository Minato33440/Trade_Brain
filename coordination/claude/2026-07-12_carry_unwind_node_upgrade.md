---
engine: claude
type: coordination_record
task: carry_unwind_node_upgrade
week: 2026-6-26_wk04
created: 2026-07-12
---

# 記録: 6-26 照合 → carry_unwind ノード定義格上げ

## 6-26 outcome（codex照合・std+unverified要件で実施）
- yen_carry_unwind: **latent（暫定1w）**。7-3で US100+0.72%/BTC+2.95%/VIX 18.41→16.15＝条件2の同時安不成立。
- 介入面: flash `not_confirmed_on_available_sources`（7-3は「介入なしで円高」明記）。
- Stage3: A_regime_misread_partial_1w。4週窓未取得のため B_timing/C_swept は unverified。D_lucky not_applicable。
- outcome窓は7-3のみ（1週）＝暫定。4週窓が埋まれば再判定。

## 運用則の実効検証（初回）
- unverified 要件が効いた: flash を "false" でなく "not_confirmed" ＋ required_data 付きで返した（A/Bのoverclaim箇所を是正）。
- 独立判定が守られた: codex 自己監査5-3で「latent連続に引きずらず6-26単独証拠で判定」を明記。
→ A/B→decision→運用則→実装のループが一周し、対策が初回実地で機能。

## 定義格上げ（Boss裁定 2026-07-12）
carry_unwind ノードに「満載頻発・発火稀」を**定義**として追加（所見→定義）。
- 6月3週連続 latent（6-5・6-19 確定 / 6-26 暫定1w）＝満載読みが並んでも fired ゼロ。
- `2024_aug_replay` を「発火予測子」から「setupテンプレート」へ再定位。満載週の既定値は latent。
- 更新: `bridges/trade_brain/index/themes/yen_carry_unwind.md`

## 保留（Boss未選択）
- 6-26 の misreads 昇格（option1）: 4週窓が埋まってから判断。現状は本記録が durable trace。
- データ粒度 gate の decision doc 明文化（option3）: 未実施。trap/flash 次元は日次/intraday OHLC 待ち、は所見として残す。
