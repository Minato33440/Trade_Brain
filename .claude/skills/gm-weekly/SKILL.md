---
name: gm-weekly
description: Trade_Brain の週末 Git 更新工程（Weekly Update）を最初から最後まで実行する。毎週金曜終値後（実質土日）にボスが「週末更新を実行して」「/gm-weekly」等と依頼したら使う。対象週フォルダ（例 2026-6-12_wk02）の新規作成、main.py --trade --news とhermes x_searchによるデータ取得、トレード記録、review/meta/note/charts/trade_results 生成、CFD人間ビュー(hub MD/HTML)生成、_index/STATUS/Trade-Main/distilled の更新、関所7.5でのボス承認、RTK git push までを一括で担う。docs/WEEKLY_UPDATE_WORKFLOW.md の8段階チェックリストに準拠。
---

# gm-weekly — Trade_Brain 週末更新工程

毎週金曜終値時点の市況を構造化・アーカイブする定期ルーチン。`docs/WEEKLY_UPDATE_WORKFLOW.md` が SSoT、本Skillはその実行手順を運用知見込みで具体化したもの。**矛盾時は WEEKLY_UPDATE_WORKFLOW.md を優先**。

## 0. 起動時の前提確認

- カレント: `c:\Python\REX_AI\Trade_Brain`、`.venv` 有効。
- **RTK必須**: すべての `git` コマンドに `rtk` プレフィックス（チェーン時も各々に）。`python` は対象外（パススルー）。
- **ボス提供の1次資料は3点のみ**: #1 市況 `logs/boss's-weeken-Report/2026/wr-YYYY-M-D.md` / #4 口座スナップショット `png_data/`（PNG or YAML）/ #5 当週トレード結果（なければ「保有継続のみ」明示）。#2 --trade・#3 --news・#3.5 X headlines は自分で取得。
- **対象週フォルダ名 = `YYYY-M-D_wkNN`**: D=その週の金曜日、wkNN=その月の第N週（月初1-7=wk01, 8-14=wk02 …）。`logs/weekly/2026/_index.md` 末尾＋カレンダーで前週から推定し、ボス指定と一致を確認。
- **任意の事前調査**: 規模が大きいので、まず読み取り専用 Explore サブエージェント（Agentツール, subagent_type=Explore）で「最終処理済み週・対象週・不足データ・前週テンプレ場所」を地図化させると安全。実装本体（不可逆操作）はメインセッションで行う。

## 1. セッション開始の必読（CLAUDE.md STEP 1-7 準拠）

`docs/WEEKLY_UPDATE_WORKFLOW.md` / `docs/STATUS.md`末尾Weekly Brief / `docs/Trade-Main.md`末尾 / 直近 `distilled/2026/distilled-gm-2026-N.md` / 前週フォルダ `logs/weekly/2026/<前週>/`（review.md・meta.yaml・note.md・charts.md・trade_results.md・charts/ をテンプレとして読む）。

## 2. Step 1a — 8ペア市場データ + GMニュース取得

```bash
python main.py --trade --news < /dev/null
```
- 生成物: `png_data/multi_pairs_plot_8.png`、`png_data/YYYY_MM_DD_snapshot.yaml`、ターミナルに8ペア30日値・regime・GMニュース。
- 出力の **8ペア最新値・30日%・regimeラベル** を控える（これが Evidence の正本）。
- 失敗(exit≠0・データ欠落)時は**不変ルール7に従い創作補完せず停止・ボス報告**。

## 3. Step 1b — X市況ヘッドライン（マイナーデータ・失敗許容）

PowerShellで（バックグラウンド可）:
```powershell
$env:HERMES_HOME = "C:\Users\Setona\AppData\Local\hermes"
$env:Path += ";$env:HERMES_HOME\hermes-agent\venv\Scripts"
$q = "latest market sentiment macroeconomic headlines ... from last 7 days high engagement"
& "$env:HERMES_HOME\hermes-agent\venv\Scripts\hermes.exe" -z $q -t x_search,vision --accept-hooks | Out-File -Encoding UTF8 "logs\weekly\x_headlines_raw.txt"
```
- 取得失敗・空でもプロセス続行（前週は「取得ツイートなし」だった週もある）。聖域: hermes の出力先は必ず Trade_Brain 配下、REX_Brain_Vault へ書かない。

## 4. Step 3 — 当週トレードを記録 → summary

ボス提供の #5 を `src/track_trades.py add` で記録。**entry/exit/direction は前週記録やボス文言から事実ベースで。不明な精度は創作しない**（不変ルール7）。size は絶対ロットを書かず相対（例 0.33=1/3ロット）。
```bash
python src/track_trades.py add --opened-at "YYYY-MM-DD HH:MM" --closed-at "YYYY-MM-DD HH:MM" \
  --symbol XAUUSD --direction long --size 0.33 --entry 4438 --exit 4390 --tag "..." --notes "..."
```
- ⚠️ **bash の `$` 変数展開に注意**: notes 内の `$4250` 等は bash で空展開され化ける。`$`を避けて「4250ドル」表記にするか、記録後にEditでCSVを修正。
- summary は **PowerShell で UTF-8 強制**（bashだと cp932 で en-dash `–` がエラー）:
```powershell
$env:PYTHONUTF8=1; $env:PYTHONIOENCODING="utf-8"; python src/track_trades.py summary --start YYYY-MM-DD --end YYYY-MM-DD
```
- ⚠️ **`data/private_trades.csv` は .gitignore 対象**（"private"命名・ローカル専用）。git add しない。トレード内容は trade_results.md/review.md でリポ保全。force追加要否はボス判断。
- 残ポジ越週など opened_at が前週の場合、summary の `--start` を前週まで広げて拾う。

## 5. Step 4-5 — フォルダ作成 & charts 配置（PowerShell）

```powershell
$dst = "logs\weekly\2026\<YYYY-M-D_wkNN>\charts"; New-Item -ItemType Directory -Force -Path $dst | Out-Null
Copy-Item "png_data\multi_pairs_plot_8.png" "$dst\Portforio-YYYY-MM-DD.png"   # 日付=snapshotのdate.end
Copy-Item "png_data\YYYY_MM_DD_snapshot.yaml" "$dst\YYYY_MM_DD_snapshot.yaml"
# 口座PNG（ボス提供・ファイル名は週により異なる。例 東証株.png / 米国株 (2).png）をリネームコピー
Copy-Item "png_data\<国内株>.png" "$dst\Portfolio-JP-Stocks-YYYY-MM-DD.png"
Copy-Item "png_data\<米国株>.png" "$dst\Portfolio-US-Stocks-YYYY-MM-DD.png"
```
charts/ に作るテキスト2点:
- `YYYY-MM-DD 〜 YYYY-MM-DD.txt` … --trade 出力の取得期間+8ペア値（Writeで作成）。
- `Market conditions -YYYY-M-D~.txt` … ①ボス市況(wr-…md) ②--news出力 ③X headlines TOP3要約(日本語) を統合（Writeで作成。`src/integration/merge_weekly_sources.py` でも可だが手組みの方が整形しやすい）。

## 6. Step 6 — 主要5ファイル生成（前週フォルダをテンプレに）

`meta.yaml` / `review.md` / `note.md` / `charts.md` / `trade_results.md`。前週の構造・見出しを踏襲し、当週の実測値・ボス市況・トレード結果に差し替える。
- **Evidence は snapshot 実測値に忠実**。前週比(wkN-1→wkN)を併記。
- **snapshot 8ペアに JP225 は含まれない**。ボス市況に金曜終値の明示がなければ「金曜終値の実測なし」と書く（創作しない）。
- 機械regime と ボス前方視点が食い違う場合は**両論併記**。

## 7. Step 7 — インデックス・ステータス・distilled 更新

- `logs/weekly/2026/_index.md`: 末尾に当週エントリ追記（Regime/1行/Key gates/Links）。**過去週の欠落があれば補完してよい**（ナビ用・凍結対象外）。
- `docs/STATUS.md`: 末尾に `## Weekly Brief | …` 追記（Macro/Regime・Position/Orders・Key Levels・**Gates(終値判定)**・This Week Focus・Signals）。過去Briefは凍結・改変しない。
- `docs/Trade-Main.md`: ① 末尾に Weekly Brief 追記 ② Distilled Logs に当月行追加。※「2026 Weekly Index」は2月で更新停止しており直近運用では触らない。
- `distilled/2026/distilled-gm-2026-N.md`: **同月内は同ファイルに追記、月替わりで新規作成**（N=月番号）。書式: regime / decision(判断変更点) / evidence(close) / implication / tags。

## 8. Step 7.5 — 品質確認（関所・push前必須）

2基準を自己チェックし**ボスに報告して承認を得る**:
1. ボス1次テキストとの方向性矛盾がないこと
2. --trade/--news/x_search の実測・正規ソースにない情報を足していないこと（「おそらく」等の不確実性表現は対象外、ソース外情報の混入を検出）

矛盾・創作を見つけたら**該当箇所を直してから**報告。承認なしに push しない。判断が要る逸脱（欠落補完・新概念MOC・コミット範囲・private CSV等）は箇条書きでボスに確認。

## 9. Step 7.6 — 人間ビュー3レイヤー生成（関所承認後）

- `CFD戦略-YYYY-M-D.md`（**日付=行動週の月曜**）: hub。frontmatter(week/regime/add_risk_gate/reduce_risk_gate/tags) + 概念wikilink + Mermaid(pie/timeline) + リンク表(HTML詳細・[[distilled-gm-YYYY-M]]・review・meta・note・前後週ハブ) + 要点3行 + トリガー要点。
- `CFD_Strategy-YYYY-M-D.html`（同日付）: 自己完結HTML(Chart.js)。8ペア表+棒/ドーナツグラフ・レジーム/ゲート・3シナリオ・銘柄別アクション・週内タイムライン・監視トリガー・ポートフォリオ。**直近の既存hub/HTML（例 wk03 の CFD戦略-2026-5-18.md / .html）をテンプレに**コピー改変。
- 概念wikilinkは canonical表記固定。**canonical新概念**が出たら `MOC/<新concept>.md`（Dataview型・既存MOCをテンプレに）を新規作成し `MOC/_index.md` に追記（要ボス確認）。
- ポートフォリオ数値の1次提供がない週は**画像参照のみ**（数値創作禁止）。
- ⚠️ 直近 wk04/wk05 は hub未生成で「前週ハブ」リンクが切れている場合あり。実在する直近hubに繋ぐ。

## 10. Step 8 — Git 更新（RTK必須・承認後）

unstaged があると `git pull --rebase` が失敗するので、**ステージ→コミット→push** の順（リモート同期済みなら pull不要、push拒否時のみ pull --rebase）。
```bash
rtk git add logs/weekly/2026/<YYYY-M-D_wkNN>/ \
            logs/weekly/2026/_index.md docs/STATUS.md docs/Trade-Main.md \
            distilled/2026/distilled-gm-2026-N.md MOC/ \
            logs/weekly/x_headlines_raw.txt "logs/boss's-weeken-Report/2026/wr-YYYY-M-D.md"
rtk git commit -m "weekly: YYYY-M-D_wkNN review + trade_results + charts + CFD human-view (...要約...)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
rtk git push origin main
```
- `data/private_trades.csv` は .gitignore のため add しない（force要否はボス判断）。
- charts/ の png/txt/yaml/md は `<週フォルダ>/` 一括addで包含。
- 古い無関係な未追跡（前週以前の wr-*.md 等）は混ぜない。ボス指定の素材のみ。

## 完了報告に含めること

- 今週の地合い要約（regime転換・gates状態）と主要実測値。
- commit ハッシュ・push 結果。
- 関所判断事項（欠落補完/新MOC/コミット範囲/private CSV/創作回避箇所）の明示。
- 次の大型イベント（次週の山）。
