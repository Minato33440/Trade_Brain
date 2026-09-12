---
name: gm-weekly
description: Trade_Brainの週末市況・トレード記録・戦略・Git更新を共通Broker手順で実行する。週次更新の依頼で使用し、Astraを通常の司令塔としつつOpus等へ引継ぎ可能。
---

# GM週次更新

## 入口

最初にリポジトリの[週次手順](../../../docs/WEEKLY_UPDATE_WORKFLOW.md)と[共通Broker運用](../../../docs/WEEKLY_BROKER_OPERATIONS.md)を読む。後者は2026-09-12のBoss合意を反映し、旧Opusの制限を固定registerとして再導入しない。通常はAstra統括、必要ならOpus-5等へ交代する。

## 実行

- 対象週を確認し、STATUS/Trade-Main末尾、当月distilled、前週carry_forwardと現在のGit状態を読む。入力はレポート末尾追記、画像、trade_results、継続中の受け渡しを含む。
- 新規週は`main.py --trade --news`で基準データを取得し、出力・時刻・入力版を保全。再開/追記対応では取得済み成果を使い、再取得が必要なら理由と新旧版を残す。PowerShellで`/dev/null`を渡さず、stdinは環境に合う方法で閉じる。
- 分業は品質と作業量で決める。抽出Agentの回答を照合し、重要数値は原資料で確定する。Grok X検索は必要な論点のみ、使う場合は当該Runtimeの利用可能なProfile/引数を確認する。結果は市場参加者の見解として出典・時刻・採否を記録。
- CSVの`size`は原資料の数量・単位をそのまま保持し、Lotを勝手に相対比率へ変換しない。当週実績は決済日で照合し、既存CLIの開始日集計と区別する。`data/private_trades.csv`は現在追跡対象だが、実行時にもGit状態を確認する。
- review/note/meta/charts/戦略・人間ビュー・蒸留・indexを更新する。可逆的修正を進め、原本と変更履歴を保全する。HTMLはオフラインで主要情報を読める構成を既定とし、表示確認する。
- `python scripts/validate_weekly_artifacts.py --week YYYY-M-D_wkNN`でローカル整合を検査する（PyYAMLはrequirements-test.txt）。出典の適合、画像読取り、戦略の妥当性は別途確認し、機械PASSのみで完了としない。
- 既存の依頼・承認に沿って対象差分だけを確定する。通常の週次Git更新依頼はcommit/pushを含む。RTKは利用可能なら使い、不在で停止しない。Git同期状況を確認し、未整理の作業を無理にrebaseしない。
- 作業結果・必要な修正・未決・次回への入力と計測範囲を残す。Provider交代時は共通方針の受け渡し項目を使用し、完了済み取得やCSV追記を重複させない。署名や実行担当は実際のモデルを記録し、旧モデルのCo-Authorを流用しない。

今回の基準は2026-9-11_wk02の成果物。前週の価格・件数・日付限定出口を現在値として継承せず、最新入力で更新する。完了報告は成果物・検証範囲・残る論点・Git結果を簡潔に示す。
