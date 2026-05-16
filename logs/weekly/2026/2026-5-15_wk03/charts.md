---
week: 2026-5-15_wk03
date_range: 2026-05-11 -> 2026-05-15
created: 2026-05-16
tags:
  - gm_weekly
  - charts
  - macro
  - regime
---

# Charts | 2026-5-15_wk03

## チャートファイル一覧（charts/）

| ファイル | 内容 |
|---------|------|
| `Portforio-2026-05-16.png` | 8ペア正規化比較プロット（2026-04-16〜2026-05-16）※ローカル専用 |
| `2026_05_16_snapshot.yaml` | レジームスナップショット（Neutral / equities=up / gold=off / crypto=strong / yields=rising） |
| `2026-04-16 〜 2026-05-16.txt` | 8ペア30日変動率データ（snapshot.yamlより） |
| `Market conditions -2026-5-15~.txt` | Minato 1次市況テキスト（wr-2026-5-15.md）+ `python main.py --news` 出力 |
| `GM Strategy-2026-5-15.txt` | GM戦略統合テキスト（①〜⑨ / 実データ反映版） |

> **注記**: `Portforio-2026-05-16.png` は `python main.py --trade` で生成（`png_data/multi_pairs_plot_8.png`）。ローカル専用（.gitignore）。

## 今週の特徴
- **世界的債券パニック→リスクオフ**: US10Y 4.568%（snapshot 4.595）パニック売り。JP10Y 2.7%・30年4%・プライム平均5.3%。日本は株・債券・円のトリプル安。
- **US10Y 4.4%分水嶺突破**: 4.595。wk02 Reduce riskゲート条件（US10Y>4.4%定着）が成立。
- **VIX 18超え**: 18.43。Add risk gate（<18）が wk01以降初めて閉じた。
- **Gold 急落**: 4,720→4,544（-3.7%）。snapshot regime gold=off。boss $3,150〜3,200を中期押し目買い場と評価。
- **米中首脳会談 成功**: NVIDIA H200 中国10社向け解禁・ボーイング200機・大豆・LNG成約。5/21 NVDA決算まで「下げたら買い」上目線。
- **USDJPY 158.731**: wk02 156.621比+2.1円の円安戻し。介入後2円戻し止まり。6/16利上げほぼ確実。
- **WTI 101.160**: wk02 95.42比+6.0%（30日+6.83%）。※boss 60〜65ドル目線と乖離・要確認。
- **Regime Neutral継続（内部はリスクオフ前傾）**: gold=off化・Add risk gate閉・US10Y 4.4%突破で質的シフト。
