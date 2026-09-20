---
engine: gpt-5.6-terra
created: 2026-09-20
fetched_at_jst: 2026-09-20T11:55:32+09:00
scope: FRED public CSV preservation and common-date weekly calculation
status: complete-with-publication-lag-preserved
---

# wk03 FRED補完 — 公表ラグを埋めない共通日計算

## 取得と原本

- 取得先: `https://fred.stlouisfed.org/graph/fredgraph.csv?id=<SERIES_ID>`
- 対象: `DGS5`, `DFII5`, `T5YIE`, `T5YIFR`, `DGS2`, `DGS10`。
- 取得時刻: **2026-09-20T11:55:32+09:00**。PowerShellのロケール表示は和暦になり得るため、保存時刻はグレゴリオ暦・ISO 8601で固定した。
- 抽出した原本行は [fred_public_csv_2026-09-20.txt](fred_public_csv_2026-09-20.txt)、構造化要約は [fred_weekly_summary.json](fred_weekly_summary.json) に保存した。

## 公表状態

`T5YIE` と `T5YIFR` は9/18まである。一方、`DGS5`、`DFII5`、`DGS2`、`DGS10` の最新非空欄は9/17である。これは `png_data/2026_09_20_snapshot.yaml` の **curve=9/17 / BE=9/18** と一致する。

ゆえに9/18のBEを9/17の名目・実質5年と減算しない。6系列すべてが揃う比較窓は **9/11 → 9/17** である。

| 系列 | 9/11 | 9/17 | 週次差 |
|---|---:|---:|---:|
| DGS5（名目5年） | 4.78% | 4.78% | 0bp |
| DFII5（実質5年） | 2.38% | 2.46% | +8bp |
| T5YIE（5年BE） | 2.40% | 2.32% | -8bp |
| T5YIFR（5年5年先） | 2.32% | 2.34% | +2bp |
| DGS2 | 4.63% | 4.67% | +4bp |
| DGS10 | 4.96% | 4.94% | -2bp |
| DGS10−DGS2 | 33bp | 27bp | -6bp |

## 恒等式検証

式は `DGS5 − DFII5 − T5YIE = 0`。

- 9/11: `4.78 − 2.38 − 2.40 = 0.00%`。
- 9/17: `4.78 − 2.46 − 2.32 = 0.00%`。
- 週次差: `0 − (+8) − (−8) = 0bp`。

したがって、同じ9/11→9/17窓では、名目5年は不変、実質5年は+8bp、5年BEは-8bpで恒等式残差は0bp。これは値の分解であり、金価格や政策反応の単独因果を証明しない。

## 9/18の扱い

9/18には `T5YIE=2.31%`、`T5YIFR=2.35%` が公開されているが、同日 `DGS5` と `DFII5` はこの取得時点で未公表である。よって、9/18について「実質5年」または同日恒等式を記録・推定しない。次回取得で同日のDGS5・DFII5が公表されてから、同日行として検証する。

## 一次政策根拠（短い引用）

- [Federal Reserve, 9/16](https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm): “raise the target range … to 3-3/4 to 4 percent.”
- [Bank of Japan, 9/18](https://www.boj.or.jp/mopo/mpmdeci/mpr_2026/k260918a.pdf): 「無担保コールレート（オーバーナイト物）を、1.25％程度で推移するよう促す。」
- [ECB, 9/10](https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2026/html/ecb.is260910~6a45359cfc.en.html): “raise the three key ECB interest rates by 25 basis points.”

各引用は政策決定の存在だけを支持する。FREDの市場金利・BEへの即時因果、または特定資産の値動きはこれらの短文から推論しない。
