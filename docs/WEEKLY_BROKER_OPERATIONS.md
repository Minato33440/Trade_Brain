# GM週次更新 — Broker運用方針

合意日: 2026-09-12。Bossは2026-9-11_wk02の暫定Brokerテストと追記反映後の成果を確認し、成功と判断した。次週からAstraを通常の司令塔とする。この合意は今回の品質への評価であり、他モデルとの一般的な優劣や費用倍率の証明ではない。

## 担当を交代できる運用

Brokerは役割であり、Providerを固定しない。通常はAstraが事前協議・分業・統合・例外処理・最終確認を担当する。利用枠、可用性、作業適性に応じてOpus-5などへ引き継げる。利用可能な実モデルと認証済み環境を確認し、設定名から能力や料金を推測しない。交代のために既存Profileを恒久切替する必要はない。

初回の配分は再利用できる出発点である。Terraは数値・整合性・反対材料の照合、Lunaは抽出と照合準備、Grokは必要なX検索の補助。重要な数値や因果判断はBrokerが原資料へ戻って確定する。モデル名と人数を毎週の固定条件にせず、簡単な決定的処理はスクリプト、必要ならローカルモデルへ回す。品質が最優先で、枠の節約だけを理由に検証を省かない。

## 従来の制限を教訓として使う

旧Opusの作業手順、担当固定、機械的な停止・承認待ち、出力形式や作業順は、事故の理由を理解するための教訓として扱う。新しい固定registerへ積み直さない。現セッションで得たBossの指示・承認と実際のリスクに応じ、Brokerが工程を調整し、判断理由を短く残す。

|過去の運用例|今後の扱い|
|---|---|
|関所7.5で毎回いったん停止|品質レビューは実施する。すでに確認・承認された成果は、同じ承認を再要求せず確定へ進める。通常の週次Git更新依頼は、その対象範囲のcommit/pushまで含む。レビューだけの依頼ならレビューで完了する|
|1回エラーで全面停止|原因が判明した可逆的な修正・再試行はBroker判断で行う。結果が不明な外部書込みは状態確認してから再試行する。推測の連鎖で進めず、必要な入力や権限だけを確認する|
|データ取得は絶対1回|基準となる取得を固定し無目的な再取得を避ける。欠損・誤取得・公表後補完が必要なら理由と取得時点を記録し、新しい版として保全する|
|画像・数値の抽出AgentがPASSなら採用|計算や原資料との照合で採否を決める。Agent同士の一致は証拠を増やさない|
|固定のAgent数、Chart.js、Xを毎回3件|当週に必要な作業量へ調整する。HTMLはオフラインでも主要情報を読める形を既定とし、X検索は必要な論点に使う|
|RTKがなければ作業できない|RTKを利用可能なら優先。不在時は通常コマンドで進め、出力を絞る。本番設定を変えて無理に導入しない|

この方針は週次制作・実装の進め方を柔軟にするもの。実際の建玉条件や約定履歴、仮説の判定条件は、最新の合意・根拠と区別して扱う。条件を変更するときは旧条件・新条件・適用時点・理由を残す。単に『制限を柔軟化』したことから売買条件の変更や発注を導かない。

## 品質を継続する実務

週次工程の正本は[WEEKLY_UPDATE_WORKFLOW](WEEKLY_UPDATE_WORKFLOW.md)。以下は今回の実証から採用する確認観点であり、全週に同じ枚数・項目数を強制するチェックリストではない。

1. 事前協議の結果とレポート末尾追記を読み、事実・Bossの意図・解釈・反対材料・未決を分ける。前週carry_forwardをIDで照合する。
2. snapshotの値より先に日付整合、改訂履歴、比較窓を読む。商品、vendor、as_of、cutoffを保存し、異なる窓の値を一続きの時系列へ混ぜない。
3. 口座の資金移動と評価変化、CFDの実現と含み変化、キャンペーンと決済件数を照合。不明な契約倍率や時刻を補完しない。
4. 解釈から条件付き戦略へつなぎ、観測・行動・反証を対応させる。双方向の仮説なら両方向を点検し、判定条件の変更を隠さない。
5. review/note/meta/戦略/HTML/蒸留の結論をそろえる。原本と訂正履歴は残し、次週へ未決・解消項目を渡す。

今回のベースライン: [反映・訂正記録](../logs/weekly/2026/2026-9-11_wk02/rex_addendum_integration.md)、[持ち越し表](../logs/weekly/2026/2026-9-11_wk02/carry_forward.md)、[初回計測](../logs/weekly/2026/2026-9-11_wk02/pilot_run.md)。当該週の価格・件数・日付限定例外を次週の現在値としてコピーしない。

## 再利用する検証

Pythonと`requirements-test.txt`のPyYAMLを使い、リポジトリルートで次を実行する。この環境では`C:\Python313\python.exe`で動作確認済み。市場取得用`.venv`とは依存が異なる場合があるため、検証用Pythonを選ぶ。

```text
python scripts/validate_weekly_artifacts.py --week YYYY-M-D_wkNN
```

読み取り専用で、必要成果物・YAML重複キー・入力/アーカイブのハッシュ・口座の合計・損益接続・相対リンクを確認する。`--root`で別チェックアウトを指定できる。JSONは標準出力、失敗は終了コード1。不足した任意データはwarningとして区別する。必要なら出力を週次の検証記録へ保存する。

これは市場解釈やスクリーンショット読取りの正しさを保証しない。Brokerは当週の資料から計算の入力も照合し、HTMLを表示確認する。初回の34+23項目を将来の固定合格数にせず、当週の変更に必要な検査を足す。

## Provider交代の受け渡し

長い会話を渡すだけでなく、`coordination/<engine>/日時_話題.md`へ必要な状態を一つにまとめる。`engine`は実際の作成担当。秘密情報や認証トークンは含めない。

```yaml
engine: actual-model
week: YYYY-M-D_wkNN
broker_role: weekly_integration
status: in_progress
completed: []
remaining: []
input_manifest: relative/path
artifacts: []
adopted_decisions: []
unresolved_and_counterevidence: []
validation_results: []
git_state: {branch: main, head: actual-sha, staged: [], committed: [], pushed: []}
authorization: {scope: current-user-request, confirmed: [], needed: []}
runtime: {active_jobs: [], output_paths: []}
usage: {measurement_window: unknown, token_usage: unknown, account_allowance: unknown}
next_action: concrete-next-step
```

受け取るBrokerはファイルとGitの現状を確かめ、完了済みの取得・CSV追加・外部書込みを重複実行しない。利用枠の都合で引き継ぐ場合も、品質判断・未決・承認済み範囲を維持する。トークン、アカウント共通の利用枠、API費用は別々に記録し、欠測を0としない。

Codex入口は`.agents/skills/gm-weekly/`、Claude Code入口は`.claude/skills/gm-weekly/`。従来呼出しの`gm-weekly-update`もプロジェクト内の同名入口から共通手順へ接続する。他のRuntimeから実施する場合も本書と週次正本を渡す。Provider固有のMCPや恒久ルーティングの新設は、この合意だけでは必要ない。
