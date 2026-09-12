---
engine: gpt-6-astra
week: 2026-9-11_wk02
created: 2026-09-12
status: adopted_by_boss
---

# 週次Broker試行の採用

Bossは生成結果を確認し、今回のテスト成功と、次週から通常Astra統括で運用することを明示した。BrokerはProvider非固定、利用枠や適性に応じOpus-5等へ交代可能。旧Opusの作業制限は固定registerとせず教訓として臨機応変に運用する。

2026-9-11_wk02の成果物はセッション開始時に既にcommit `378fa85`へ記録済み、mainとorigin/mainは一致していた。今回の作業は共通Broker方針・Codex/Claude Skill入口・再利用検証器の整備。既存週次データの再取得やCSV再追記はしていない。

旧quality_gate/metaのpending表記は各資料作成時点の履歴。本メモはその後のBoss確認を記録する。価格・仮説・既存建玉の条件変更の指示ではない。従来の検証57項目・HTML表示確認、Rex追記の訂正は前回の成果物にある。今回の環境整備の検証結果は本メモへ追記する。

共通正本: docs/WEEKLY_UPDATE_WORKFLOW.md / docs/WEEKLY_BROKER_OPERATIONS.md。
次回入力: 当週レポート/末尾追記/画像/trade_results、前週carry_forward、最新coordination記録。
再開するBrokerは対象週・Git状態・完了工程・入力版・未決・利用可能なProviderを確認して続行する。

## 整備の検証

- Codex/Claude用のgm-weeklyとgm-weekly-update、計4入口のSkill構文検証PASS。
- 再利用検証器: 2026-9-11_wk02に対して61項目PASS、warning 0。読み取り専用で週次ファイルを変更していない。
- 検証器のテスト6件PASS: 別年の週とDecimal損益、実現/評価込み混同の検出、重複YAMLキー、アーカイブ改変、欠落リンク、週指定のパス逸脱。
- TerraによるClaude側Skill入口の読取引継ぎ演習: 既に378fa85へ記録済み・同期済みの当週を再実行せず、Grok不接続でも既存成果から完了と判定。Opus-5自体へ実際にモデル切替したテストではない。
- docsの改行を既存部分で保持し、運用更新以外の差分を抑えた。Provider固有の認証・Gateway・課金設定には変更なし。
