---
engine: gpt-6-astra
week: 2026-9-11_wk02
status: audit_trail
---

# Agent初稿と訂正の記録

初稿を成績表や確定情報として直接利用しない。最終採用値は当週review/metaとquality_gateにある。初稿を消すと再作業と監督の効果を測れないため、原形を保存した。

- Luna初稿のGDX名/円損益符号、指標列の読み順、BTC確定日を親Astraが訂正。Luna訂正版は親の訂正を記録したもので、独立再検証の成功を意味しない。
- Terra市場初稿のUSDJPY騰落率とBTC窓/P12不足は訂正ファイルを優先。
- Terra口座初稿の2243単価4299は4259が正しい。親が数量174×4259=741066で照合した。
- Terra最終レビューは主要条件をPASSとしたが、noteで9/9キャンペーンと全通算の表現が混同していた箇所、ハブのfrontmatter/リンク、snapshotのYAML生成欠陥は、その後の親検証で補正した。
- Astra basisは統合中間入力。後続のsnapshot形式修正・補完の採用情報はreview/sources/quality_gateが新しい。

- [luna_extraction.md](luna_extraction.md)
- [luna_extraction_corrections.md](luna_extraction_corrections.md)
- [terra_market_audit.md](terra_market_audit.md)
- [terra_market_audit_corrections.md](terra_market_audit_corrections.md)
- [terra_trade_audit.md](terra_trade_audit.md)
- [terra_portfolio_audit.md](terra_portfolio_audit.md)
- [final_market_review.md](final_market_review.md)
- [astra_verified_basis.md](astra_verified_basis.md)

前週機械VIX14.530は保存snapshotで確認済み。同一TVCの前週画像値は未確認という区別を最終稿へ採用した。

## Rex追記受領後の監査（2026-09-12）

- [損益・持ち越し照合](rex_addendum_trade_audit.md)
- [市場監査初稿](rex_addendum_market_audit.md)
- [市場監査の訂正](rex_addendum_market_audit_corrections.md): 初稿の一律06:00 cutoff・検出器完成という断定を撤回。前半の価格往復記録と台帳後半の証拠も分離。
- [親Astraの最終採否](../rex_addendum_integration.md)
- [追記前生成物のハッシュ](pre_rex_addendum/manifest.json)

入力追記もエージェント回答も原資料へ戻って検証する。今回の市場監査訂正版を初稿より優先する。
