# CLAUDE.md — Trade_Brain
# このファイルは ClaudeCode が Trade_Brain リポジトリで作業する際に自動で読み込まれる
# Trade_System の CLAUDE.md とは別運用
# 更新: 2026-04-18（週次運用ファイル 3 件統合版・RTK ルール反映）

---

## プロジェクト概要

REX AI Trade System のマクロ市況・戦略アーカイブ。
実装リポ（Trade_System）とは明確に分離されたナレッジシステム。

**目的**: 日次・週次の市況データと蒸留済み戦略判断を構造化・アーカイブし、
将来のトレード判断で過去事例を参照可能にする。

---

## 重要な区別（Trade_System との違い）

| 項目 | Trade_System | Trade_Brain |
|---|---|---|
| コード | src/*.py（凍結ファイルあり） | なし（データと Wiki のみ） |
| データ性質 | 静的（83,112本 / 凍結済み） | 動的（毎日追加される時系列） |
| 更新単位 | 指示書（#025 / #026d ...） | Daily / Weekly / Monthly |
| CLAUDE.md の主眼 | 凍結ファイル保護・API 整合 | スキーマ遵守・Wiki 同期・週次運用 |

**重要**: Trade_System の「凍結ファイル」「ADR F-4」などの規律は
このリポには適用されない。混同しないこと。

---

## チーム構成

| 役割 | 担当 | 権限 |
|---|---|---|
| ディレクター | Minato（ボス） | 全ての最終判断 |
| Advisor | Claude.ai（Opus 4.7 等） | 蒸留・構造化・Wiki 更新提案 |
| 実装 | ClaudeCode（Sonnet 4.6） | Ingest 実行・週次更新・ファイル操作 |

**Trade_System の Planner / Evaluator はこのリポには関与しない**（役割分担明確化）。

---

## 🦀 RTK（Rust Token Killer）プレフィックスルール（最重要・全工程共通）

**このリポジトリでは、すべての `git` コマンドは `rtk` プレフィックスを必須とする。**

```bash
# ❌ 間違い
git status
git add .
git commit -m "msg"
git push

# ✅ 正しい
rtk git status
rtk git add logs/gm/weekly/...
rtk git commit -m "msg"
rtk git push origin main
```

### 重要な適用範囲

- **対象**: すべての `git` コマンド
- **対象外**: `python`（パススルー）/ `rtk init` / `rtk gain` などの RTK メタコマンド自身
- **チェーン時**: `&&` で繋ぐ場合も各コマンドに `rtk` を付ける
  ```bash
  rtk git add . && rtk git commit -m "msg" && rtk git push
  ```

### 環境制約（Windows）

- Unix 系の自動フックは使用不可（Mac/Linux 専用）
- `~/.claude/CLAUDE.md` の指示経由で ClaudeCode が手動で `rtk` を付ける方式が唯一の動作モード
- 詳細: `docs/WEEKLY_UPDATE_WORKFLOW.md` §0（RTK 使用ルール）

---

## セッション開始手順

```
STEP 1: このファイル（CLAUDE.md）を読む ← 自動
STEP 2: docs/STATUS.md の末尾 Weekly Brief を読む（現在の市況・regime・gates を把握）
STEP 3: docs/Trade-Main.md の Weekly Index 末尾を確認（今週の運用方針）
STEP 4: docs/WEEKLY_UPDATE_WORKFLOW.md を確認（週末更新タスクの場合は必読）
STEP 5: docs/distillation_schema.md を確認（スキーマが最新か）
STEP 6: docs/STRATEGY_WIKI_GUIDE.md を確認（Wiki 運用時のみ）
STEP 7: 直近の distilled/YYYY/distilled-gm-YYYY-M.md を確認（蒸留データ最新状態）
STEP 8: 作業開始
```

想定所要時間: 約 5 分

---

## 実ディレクトリ構造（2026-04-20 raw/ → logs/ リネーム反映版）

```
Trade_Brain/
├── .CLAUDE.md
├── CLAUDE.md
├── README.md
├── .gitignore
├── .venv/
│
├── logs/                        # 生データ（Trade_System/logs/gm/ から移行済み・2026-04-20 raw/ からリネーム）
│   ├── daily/
│   │   └── 2026/               # 2026年3月〜 日次ログ（2025は存在しない）
│   │       ├── 2026-3-2.txt
│   │       ├── ...
│   │       └── 2026-4-17.txt
│   ├── weekly/
│   │   ├── 2025/               # 2025年 週次ポートフォリオ総括
│   │   └── 2026/               # 2026年 週次ポートフォリオ総括
│   │       ├── 2026-4-3_wk01/
│   │       ├── 2026-4-10_wk02/
│   │       └── 2026-4-17_wk03/
│   └── boss's-weeken-Report/   # 週末レポート（既存命名維持）
│
├── distilled/                  # 蒸留済み戦略アーカイブ（移行済み）
│   ├── 2025/
│   └── 2026/
│       ├── distilled-gm-2026-1.md
│       ├── distilled-gm-2026-2.md
│       ├── distilled-gm-2026-3.md
│       └── distilled-gm-2026-4.md
│
├── Strategy_Wiki/              # Obsidian Vault 同期対象（wiki/trade_brain/ のミラー）
│   ├── Regimes/
│   ├── Signals/
│   ├── Events/
│   ├── Instruments/
│   ├── Patterns/
│   ├── Hypotheses/
│   ├── Journal/
│   └── index.md
│
├── nlm_sources/                # NLM 投入用パッケージ
│   └── monthly/
│       └── YYYY-MM_brain_pack.md
│
└── docs/
    ├── STRATEGY_WIKI_GUIDE.md      # Wiki 構造ガイド（Strategy_Wiki/ 運用）
    ├── distillation_schema.md      # distilled の YAML/MD スキーマ仕様
    ├── STATUS.md                   # 週次ブリーフ時系列スタック（SSoT・毎週追記）
    ├── Trade-Main.md               # GM Playbook + Weekly Index + 3シナリオ運用指針
    └── WEEKLY_UPDATE_WORKFLOW.md   # 週末 Git 更新手順書（RTK / main.py 実行・チェックリスト）
```

---

## docs/ 配下ファイルの役割と参照優先順位

### 設計資料（参照系・変更頻度低）

| ファイル | 参照タイミング | 役割 |
|---|---|---|
| `STRATEGY_WIKI_GUIDE.md` | Strategy_Wiki/ 配下を操作する時 | YAML frontmatter 仕様・Dataview クエリ例・Ingest フロー |
| `distillation_schema.md` | distilled/*.md を編集する時 | YAML/MD スキーマ正式仕様 |

### 週次運用資料（操作系・頻繁に参照）

| ファイル | 参照タイミング | 役割 |
|---|---|---|
| `STATUS.md` | 毎セッション開始時（末尾を読む） | **現在進行形の市況 SSoT**。最新 Weekly Brief が「今週の前提」 |
| `Trade-Main.md` | 運用方針を確認する時 / 週末更新時 | **GM Playbook**。3 シナリオ（A: Risk-on / B: Whipsaw / C: Risk-off）・Weekly Index |
| `WEEKLY_UPDATE_WORKFLOW.md` | **週末 Git 更新時は必読** | 8 段階チェックリスト・`python main.py --trade --news` 実行指示・RTK ルール |

### 参照優先順位（衝突時）

```
RTK ルール:             WEEKLY_UPDATE_WORKFLOW.md > CLAUDE.md
命名規則（distilled）:  WEEKLY_UPDATE_WORKFLOW.md §4 STEP 7 = CLAUDE.md 命名規則（一致）
週次手順:               WEEKLY_UPDATE_WORKFLOW.md > Trade-Main.md > CLAUDE.md
スキーマ:               distillation_schema.md = 唯一の SSoT
Wiki 構造:              STRATEGY_WIKI_GUIDE.md = 唯一の SSoT
```

---

## ディレクトリの役割と変更ルール

### logs/ — 生データ

```
原則: 読み取り専用。追記のみ可（daily ログ追加）。
構造: logs/ 直下に daily / weekly / boss's-weeken-Report/ の 3 種類
既存ファイルの内容書き換えは禁止。

命名:
  logs/daily/YYYY/YYYY-M-D.txt
  logs/weekly/YYYY/YYYY-M-D_wkNN/
  logs/boss's-weeken-Report/{任意ファイル名}

注意:
  - daily は 2026 年 3 月開始のため、2025 は存在しない（意図通り）
  - weekly は 2025 / 2026 両方存在
  - boss's-weeken-Report/ は既存命名維持（タイポだが git 履歴保護のため変更しない）
  - 2026-04-20: 旧名は raw/ だったが、データ性質に合わせ logs/ にリネーム
```

### distilled/ — 蒸留済みアーカイブ

```
原則: 月次 1 ファイル。月内の週次は追記、月替わりで新規ファイル作成。
命名: distilled/YYYY/distilled-gm-YYYY-M.md
スキーマ: docs/distillation_schema.md に準拠（regime / decision / evidence / implication / tags）

変更ルール:
  - 過去月の distilled は凍結（事後訂正は注記付きで追記のみ）
  - 当月内は追記・修正可
  - 週をまたいで新ファイルを作ってはいけない
    （例: 3月第1〜5週はすべて distilled-gm-2026-3.md に追記）
```

### docs/STATUS.md — 週次ブリーフ時系列スタック

```
原則: 週末 Git 更新時に末尾に新しい Weekly Brief セクションを追加（追記型）。
構造: 各セクションは以下の統一フォーマット
  ## Weekly Brief | YYYY-M-D_wkNN（YYYY-MM-DD → YYYY-MM-DD）
  created: YYYY-MM-DD (JST)

  ### Macro / Regime
  ### Position / Orders
  ### Key Levels (close-based)
  ### Gates（最重要：終値で判定）
  ### This Week Focus
  ### Signals (weekly, fixed keys)

変更ルール:
  - 過去の Weekly Brief は改変しない（凍結）
  - 当週 Brief は金曜まで更新可、週末確定後は凍結
  - STATUS.md 末尾が常に「現在最新の市況」
```

### docs/Trade-Main.md — GM Playbook + Weekly Index

```
原則: 週末 Git 更新時に Weekly Index に当週エントリを追加。
構造:
  - GM Playbook（運用原則・3シナリオ・Monday AM ラベル）
  - 2026 Weekly Index（wkXX エントリ一覧）
  - Distilled Logs リンク
  - 末尾に Weekly Brief セクション（STATUS.md と連動）

変更ルール:
  - GM Playbook 本文の改訂はボス判断が必要
  - Weekly Index への当週追加は定型作業
```

### docs/WEEKLY_UPDATE_WORKFLOW.md — 週末運用マニュアル

```
原則: 手順の SSoT。週末 Git 更新時は必ず参照。
内容:
  §0: RTK プレフィックスルール（全工程共通）
  §1: ボスからの提供データ
  §2: python main.py --trade --news の実行
  §3: 週次フォルダ構成
  §4: チェックリスト 8 段階
  §5: パス・コマンド早見

変更ルール:
  - 手順変更は運用実証後に反映
  - コマンド変更（例: configs/rex_chat.py → main.py）は即座に反映
  - 2026-03-21 更新: python main.py --trade --news を正式コマンドに
```

### Strategy_Wiki/ — Obsidian Vault 同期

```
原則: REX_Brain_Vault/wiki/trade_brain/ と同期するミラー。
実体は Vault 側。このリポにはスナップショットを push する。

詳細: docs/STRATEGY_WIKI_GUIDE.md 参照

書き込み権限:
  - ClaudeCode が自動書き込み可能: Signals/ / Events/ / Instruments/
  - Advisor 提案のみ（承認後書き込み）: Regimes/ / Hypotheses/ / Patterns/
  - 書き込み禁止: index.md（自動生成）
```

### nlm_sources/ — NLM 投入用パッケージ

```
原則: 月次で distilled をパッケージ化して NLM に source_add する用。
命名: nlm_sources/monthly/YYYY-MM_brain_pack.md

投入先 NLM: REX_Trade_Brain（ID: 4abc25a0-4550-4667-ad51-754c5d1d1491）
```

---

## 不変ルール

```
1. raw/ の既存ファイル内容を書き換えない（追記のみ）
2. 過去月の distilled を遡って改変しない（注記追記のみ）
3. 過去の Weekly Brief（STATUS.md / Trade-Main.md 内）を改変しない
4. スキーマ違反の distilled を push しない（docs/distillation_schema.md 準拠）
5. Strategy_Wiki/ の更新は Vault 側を Source of Truth とする（リポはミラー）
6. Trade_System のファイルをこのリポから参照・編集しない（分離原則）
7. エラーが出たら自分で「想像で」修正しない。ボスに報告して停止
8. すべての git コマンドは rtk プレフィックスを必須とする（RTK ルール）
9. 週末 Git 更新は必ず docs/WEEKLY_UPDATE_WORKFLOW.md のチェックリストに従う
```

---

## 作業フロー

### A. Daily Ingest（単純な daily ログ追加）

```
1. logs/daily/YYYY/YYYY-M-D.txt を配置（追記のみ）
2. rtk git add logs/daily/YYYY/YYYY-M-D.txt
3. rtk git commit -m "Ingest: daily YYYY-M-D"
4. rtk git push
```

### B. Weekly Update（週末 Git 更新）

**⚠️ 週末 Git 更新の依頼を受けたら、市況テキスト受け取りより先に以下をボスに依頼する:**

> 「`python main.py --trade --news` を実行して、ターミナル出力とスナップショット結果をこのチャットに貼り付けてください。」

理由: 実測値なしで作成すると、推定値で一度作成した後に実データで再更新する二度手間が発生する。

**詳細手順**: `docs/WEEKLY_UPDATE_WORKFLOW.md` のチェックリスト 8 段階に従う。

```
概要:
  1. 提供データ確認（市況 + main.py --trade --news 出力 + トレード結果）
  2. python main.py --trade --news 実行
  3. track_trades.py summary で当週トレード Markdown 生成
  4. 週次フォルダ logs/weekly/YYYY/YYYY-M-D_wkNN/ 作成
  5. charts/ へのファイル配置
  6. meta.yaml / review.md / note.md / charts.md / trade_results.md 作成
  7. インデックス更新:
     - logs/weekly/YYYY/_index.md
     - docs/STATUS.md 末尾に Weekly Brief 追記
     - docs/Trade-Main.md の Weekly Index 追加
     - distilled/YYYY/distilled-gm-YYYY-M.md 追記（月内同一ファイル）
  8. Git 更新（RTK 必須）:
     rtk git add logs/weekly/YYYY/YYYY-M-D_wkNN/ \
                 logs/weekly/YYYY/_index.md \
                 docs/STATUS.md \
                 docs/Trade-Main.md \
                 distilled/YYYY/ \
                 data/private_trades.csv
     rtk git commit -m "weekly: YYYY-M-D_wkNN review + trade_results + charts"
     rtk git push origin main
```

### C. Monthly Distillation（月末集約）

```
1. 当月の週次 logs を distilled/YYYY/distilled-gm-YYYY-M.md に蒸留
   - regime / decision / evidence / implication / tags
2. Strategy_Wiki/ の以下を更新:
   - Regimes/ ← regime 転換があれば追記
   - Signals/ ← 新規 signal があれば新設、既存は status 更新
   - Events/ ← 新規イベントがあれば新設、終了イベントは archive
   - Instruments/ ← 価格帯・抵抗線情報を更新
3. nlm_sources/monthly/YYYY-MM_brain_pack.md を生成
4. NLM の REX_Trade_Brain に source_add
```

---

## 命名規則

```
logs:
  logs/daily/YYYY/YYYY-M-D.txt            例: logs/daily/2026/2026-4-17.txt
  logs/weekly/YYYY/YYYY-M-D_wkNN/         例: logs/weekly/2026/2026-4-17_wk03/
  logs/boss's-weeken-Report/{ファイル名}  （既存命名維持）

distilled:
  distilled/YYYY/distilled-gm-YYYY-M.md  例: distilled/2026/distilled-gm-2026-4.md
  （重要: 同月内は必ず同じファイルに追記。新月になった時点で新規作成）

wiki:
  Strategy_Wiki/Signals/{signal_id}.md   例: Signals/VIX_add_risk_gate.md
  Strategy_Wiki/Regimes/{regime_id}.md   例: Regimes/gold_bid.md
  Strategy_Wiki/Events/{event_id}.md     例: Events/BOJ_4_28_meeting.md
  Strategy_Wiki/Instruments/{symbol}.md  例: Instruments/US100.md

nlm_sources:
  nlm_sources/monthly/YYYY-MM_brain_pack.md  例: nlm_sources/monthly/2026-04_brain_pack.md

charts（週次フォルダ内）:
  charts/Portforio-YYYY-MM-DD.png           （実行日付でリネーム）
  charts/YYYY_MM_DD_snapshot.yaml           （そのままコピー）
  charts/YYYY-MM-DD 〜 YYYY-MM-DD.txt       （取得期間を〜でつなぐ）
  charts/Market conditions -YYYY-M-D~.txt   （市況 + news 統合）
  charts/GM Strategy-YYYY-M-D.txt           （ClaudeCode 作成）
```

---

## Git コミット手順（RTK 必須）

```bash
# ⚠️ 必ず最初に実行
rtk git pull --rebase

# 作業タイプ別のステージング
# A. Daily Ingest
rtk git add logs/daily/YYYY/

# B. Weekly Update
rtk git add logs/weekly/YYYY/YYYY-M-D_wkNN/ \
            logs/weekly/YYYY/_index.md \
            docs/STATUS.md \
            docs/Trade-Main.md \
            distilled/YYYY/ \
            data/private_trades.csv

# C. Docs Update
rtk git add docs/ README.md CLAUDE.md

# コミット & プッシュ
rtk git commit -m "{type}: {内容}"
rtk git push origin main
```

### コミットメッセージ規則

```
Ingest:    新規 raw/distilled/wiki 追加
Update:    既存 wiki ページ更新
weekly:    週末 Git 更新一括（review + trade_results + charts）
Schema:    スキーマ仕様の改訂
Docs:      ドキュメント更新
Fix:       誤記訂正（事実訂正は必ず注記付き）
Pack:      NLM パッケージ生成
```

### charts/ の Git 追跡ルール（2026-03-21〜）

```
*.txt / *.yaml / *.md → 追跡対象（自動包含）
*.png                  → ローカル専用（.gitignore で除外）
```

---

## 外部リソース参照先

```
対応 NLM:       REX_Trade_Brain
                ID: 4abc25a0-4550-4667-ad51-754c5d1d1491
                投入基準: distilled/ 配下のみ（raw/ は投入しない）

姉妹 NLM:       REX_System_Brain（Trade_System 用）
                ID: da84715f-9719-40ef-87ec-2453a0dce67e
                ※ このリポからは参照しない

Vault ルート:   C:\Python\REX_AI\REX_Brain_Vault\wiki\trade_brain\
姉妹リポ:       Minato33440/Trade_System（参照のみ・編集禁止）
データ移行元:   Trade_System/logs/gm/ → raw/ → logs/（2026-04-18 移行・2026-04-20 リネーム完了）
                Trade_System/versions/distilled/ → distilled/（2026-04-18 移行完了）
```

---

## データ移行履歴

| 日付 | 内容 |
|---|---|
| 2026-04-18 | Trade_System/logs/gm/ を raw/ に移行（gm/ 階層は除去してフラット化） |
| 2026-04-18 | Trade_System/versions/distilled/ を distilled/ に移行 |
| 2026-04-18 | Trade_System 側の logs/gm/ および versions/distilled/ は削除済み |
| 2026-04-18 | NLM 全面再構築: 旧 REX_Trade_Brain を MCP 切り離し、新規 2 件作成 |
| 2026-04-18 | Trade_System から週次運用ファイル 3 件を移設: |
|            | docs/STATUS.md / docs/Trade-Main.md / docs/WEEKLY_UPDATE_WORKFLOW.md |
| 2026-04-20 | raw/ を logs/ にリネーム（データ性質に合わせた命名変更） |
| 2026-04-20 | src/ 内スクリプトのパス参照を logs/ 構造に整合（daily_report_parser / data_fetch / settings 等） |
| 2026-04-20 | WEEKLY_UPDATE_WORKFLOW.md / CLAUDE.md / README.md の全パス表記を実構造に整合 |

---

## 発行

作成: 2026-04-18（Advisor / Claude Opus 4.7 提言による）
更新履歴:
  - 2026-04-18 朝: 初版
  - 2026-04-18 夜: データ移行完了・実構造に合わせて命名規則修正
  - 2026-04-18 夜（再）: 週次運用ファイル 3 件統合・RTK ルール反映・NLM ID 正式記載
  - 2026-04-20: raw/ → logs/ リネーム反映・全パス整合・WEEKLY_UPDATE_WORKFLOW 同期

管理: Minato（ボス）
