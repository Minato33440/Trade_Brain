# CLAUDE.md — Trade_Brain
# このファイルは ClaudeCode が Trade_Brain リポジトリで作業する際に自動で読み込まれる
# Trade_System の CLAUDE.md とは別運用
# 更新: 2026-04-18（データ移行完了・実ディレクトリ構造に合わせて命名規則を修正）

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
| CLAUDE.md の主眼 | 凍結ファイル保護・API 整合 | スキーマ遵守・Wiki 同期 |

**重要**: Trade_System の「凍結ファイル」「ADR F-4」などの規律は
このリポには適用されない。混同しないこと。

---

## チーム構成

| 役割 | 担当 | 権限 |
|---|---|---|
| ディレクター | Minato（ボス） | 全ての最終判断 |
| Advisor | Claude.ai（Opus 4.7 等） | 蒸留・構造化・Wiki 更新提案 |
| 実装 | ClaudeCode（Sonnet 4.6） | Ingest 実行・ファイル操作 |

**Trade_System の Planner / Evaluator はこのリポには関与しない**（役割分担明確化）。

---

## セッション開始手順

```
STEP 1: このファイル（CLAUDE.md）を読む ← 自動
STEP 2: docs/distillation_schema.md を確認（スキーマが最新か）
STEP 3: docs/STRATEGY_WIKI_GUIDE.md を確認（Wiki 運用ルール）
STEP 4: 直近の distilled/YYYY/distilled-gm-YYYY-M.md を確認（現在のレジーム把握）
STEP 5: 作業開始
```

---

## 実ディレクトリ構造（2026-04-18 データ移行完了版）

```
Trade_Brain/
├── .CLAUDE.md
├── CLAUDE.md
├── README.md
├── .gitignore
├── .venv/
│
├── raw/                        # 生データ（Trade_System/logs/gm/ から移行済み）
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
    ├── STRATEGY_WIKI_GUIDE.md
    └── distillation_schema.md
```

---

## ディレクトリの役割と変更ルール

### raw/ — 生データ

```
原則: 読み取り専用。追記のみ可（daily ログ追加）。
構造: raw/ 直下に daily / weekly / boss's-weeken-Report/ の 3 種類
既存ファイルの内容書き換えは禁止。

命名:
  raw/daily/YYYY/YYYY-M-D.txt
  raw/weekly/YYYY/YYYY-M-D_wkNN/
  raw/boss's-weeken-Report/{任意ファイル名}

注意:
  - daily は 2026 年 3 月開始のため、2025 は存在しない（意図通り）
  - weekly は 2025 / 2026 両方存在
  - boss's-weeken-Report/ は既存命名維持（タイポだが git 履歴保護のため変更しない）
```

### distilled/ — 蒸留済みアーカイブ

```
原則: 月次 1 ファイル。月内の週次は追記、月替わりで新規ファイル作成。
命名: distilled/YYYY/distilled-gm-YYYY-M.md
スキーマ: docs/distillation_schema.md に準拠（regime / decision / evidence / implication / tags）

変更ルール:
  - 過去月の distilled は凍結（事後訂正は注記付きで追記のみ）
  - 当月内は追記・修正可
```

### Strategy_Wiki/ — Obsidian Vault 同期

```
原則: REX_Brain_Vault/wiki/trade_brain/ と同期するミラー。
実体は Vault 側。このリポにはスナップショットを push する。

書き込み権限:
  - ClaudeCode が自動書き込み可能: Signals/ / Events/ / Instruments/
  - Advisor 提案のみ（承認後書き込み）: Regimes/ / Hypotheses/ / Patterns/
  - 書き込み禁止: index.md（自動生成）
```

### nlm_sources/ — NLM 投入用パッケージ

```
原則: 月次で distilled をパッケージ化して NLM に source_add する用。
命名: nlm_sources/monthly/YYYY-MM_brain_pack.md

投入先 NLM: REX_Trade_Brain
```

---

## 不変ルール

```
1. raw/ の既存ファイル内容を書き換えない（追記のみ）
2. 過去月の distilled を遡って改変しない（注記追記のみ）
3. スキーマ違反の distilled を push しない（docs/distillation_schema.md 準拠）
4. Strategy_Wiki/ の更新は Vault 側を Source of Truth とする（リポはミラー）
5. Trade_System のファイルをこのリポから参照・編集しない（分離原則）
6. エラーが出たら自分で「想像で」修正しない。ボスに報告して停止
```

---

## Ingest フロー（新規 daily ログ追加時）

```
1. raw/daily/YYYY/YYYY-M-D.txt を配置（追記のみ）
2. 該当週の raw/weekly/YYYY/YYYY-M-D_wkNN/ に週次総括を追加（金曜 or 週末）
3. 月替わりまたは月末に distilled/YYYY/distilled-gm-YYYY-M.md を更新
   - regime / decision / evidence / implication / tags を埋める
   - 前週との差分（「← wk02 から転換」等）を明記
4. Strategy_Wiki/ の以下を更新:
   - Regimes/ ← regime 転換があれば追記
   - Signals/ ← 新規 signal があれば新設、既存は status 更新
   - Events/ ← 新規イベントがあれば新設、終了イベントは archive
   - Instruments/ ← 価格帯・抵抗線情報を更新
5. 月末に nlm_sources/monthly/YYYY-MM_brain_pack.md を生成
6. NLM の REX_Trade_Brain に source_add
```

---

## 命名規則

```
raw:
  raw/daily/YYYY/YYYY-M-D.txt            例: raw/daily/2026/2026-4-17.txt
  raw/weekly/YYYY/YYYY-M-D_wkNN/         例: raw/weekly/2026/2026-4-17_wk03/
  raw/boss's-weeken-Report/{ファイル名}  （既存命名維持）

distilled:
  distilled/YYYY/distilled-gm-YYYY-M.md  例: distilled/2026/distilled-gm-2026-4.md

wiki:
  Strategy_Wiki/Signals/{signal_id}.md   例: Signals/VIX_add_risk_gate.md
  Strategy_Wiki/Regimes/{regime_id}.md   例: Regimes/gold_bid.md
  Strategy_Wiki/Events/{event_id}.md     例: Events/BOJ_4_28_meeting.md
  Strategy_Wiki/Instruments/{symbol}.md  例: Instruments/US100.md

nlm_sources:
  nlm_sources/monthly/YYYY-MM_brain_pack.md  例: nlm_sources/monthly/2026-04_brain_pack.md
```

---

## Git コミット手順

```bash
# ⚠️ 必ず最初に実行
git pull --rebase

git add raw/ distilled/ Strategy_Wiki/
git commit -m "Ingest: {内容}"
git push
```

### コミットメッセージ規則

```
Ingest:    新規 raw/distilled/wiki 追加
Update:    既存 wiki ページ更新
Schema:    スキーマ仕様の改訂
Docs:      ドキュメント更新
Fix:       誤記訂正（事実訂正は必ず注記付き）
Pack:      NLM パッケージ生成
```

---

## 外部リソース参照先

```
対応 NLM:       REX_Trade_Brain（新設）
Vault ルート:   C:\Python\REX_AI\REX_Brain_Vault\wiki\trade_brain\
姉妹リポ:       Minato33440/Trade_System（参照のみ・編集禁止）
データ移行元:   Trade_System/logs/gm/ → raw/（2026-04-18 移行完了）
                Trade_System/versions/distilled/ → distilled/（2026-04-18 移行完了）
```

---

## データ移行履歴

| 日付 | 内容 |
|---|---|
| 2026-04-18 | Trade_System/logs/gm/ を raw/ に移行（gm/ 階層は除去してフラット化） |
| 2026-04-18 | Trade_System/versions/distilled/ を distilled/ に移行 |
| 2026-04-18 | Trade_System 側の logs/gm/ および versions/distilled/ は削除済み |

---

## 発行

作成: 2026-04-18（Advisor / Claude Opus 4.7 提言による）
更新: 2026-04-18（データ移行完了・実構造に合わせて命名規則修正）
管理: Minato（ボス）
