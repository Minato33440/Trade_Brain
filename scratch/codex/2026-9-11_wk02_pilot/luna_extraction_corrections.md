---
engine: gpt-5.6-luna
status: corrected_by_astra_review
task: 2026-9-11_wk02 pilot extraction corrections
as_of: 2026-09-12
mode: append-only correction record
---

# Luna correction record

親Astraの再確認結果に基づく訂正。元の `luna_extraction.md` は変更せず、訂正は本ファイルに分離する。

1. 米国株画像の銘柄名は **ヴァンエック 金鉱株ETF GDX (GDX NYSE Arca)**。Global X金融株／GDXYではない。画像の外貨損益は GDX **+190.20 USD**、SPCX **+53.04 USD**、合計 **+243.24 USD**。GDXの円換算損益は **+22,633円**（マイナスではない）。

2. 経済指標画像の数値列は左から **前回 / 予想 / 結果**。BLS一次資料（`https://www.bls.gov/news.release/archives/cpi_09112026.htm`）でCPIの結果を確認: コア前月比 **0.3%**、コア前年比 **2.4%**、前回はそれぞれ **0.2% / 2.5%**。したがって「CPI画像と本文が不一致」という元記録は撤回する。残る相違は、Michigan予想が画像 **51.1** 対レポート本文 **51.0**、表示時刻が画像 **23:00** 対本文の「CPIと同時」記述（21:30）である。

3. BTC画像は9/12朝の進行中の日足バー。表示は O=low **77,200.31**、C=high **77,262.47**、日足バー確定前であり、9/11終値として確定しない。source capture date は **2026-09-12** と注記する。+62.16 (+0.08%)も進行中バーの表示値。

4. 前週VIX **14.530** が同一TVCの前週画像終値かは、今回の確認では確実に照合できなかった。未確認として扱い、週次の機械値と断定しない。

5. ポートフォリオのスイープ用預り金の **50,000円減少**は評価損益の変化ではなく、銀行口座への移動。資産評価・損益の変化と分離する。

## Final correction findings

銘柄名・GDX円損益、CPI列順とBLS照合、BTCの未確定バー、Michiganの予想値／時刻差、スイープ移動の会計的分離を訂正済み。VIX前週値のみ未確認のまま残す。
