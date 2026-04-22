# Trade_Brain — システム概要
# 最終更新: 2026-04-22（Planner 初版起草）
# 日付なし・常に最新版として運用

---

## 本ファイルの位置づけ

Trade_Brain リポジトリの**現状スナップショット**。新規 Advisor / ClaudeCode /
Planner の引き継ぎ時に最初に読む文書。運用ルール詳細は CLAUDE.md、蒸留スキーマは
`docs/distillation_schema.md`、Wiki 構造は `docs/STRATEGY_WIKI_GUIDE.md`、
週末運用手順は `docs/WEEKLY_UPDATE_WORKFLOW.md` を参照。

Trade_System 側の姉妹文書 `Trade_System/docs/SYSTEM_OVERVIEW.md` と対称的に
構成されており、両者を並べて読むことで REX_AI エコシステムの全体像を把握できる。

---

## チーム役割分担（Trade_Brain 版）

| 役割 | 担当 | 権限 |
|---|---|---|
| ディレクター | Minato（ボス） | 全ての最終判断 |
| Advisor | Claude.ai（Opus 4.7 等） | 蒸留・構造化・Wiki 更新提案・外部視点 |
| Planner | 本ロール（ドキュメント設計・運用フロー） | docs/ 起草・Wiki 構造設計 |
| 実装 | ClaudeCode（Sonnet 4.6） | Ingest 実行・週次 Git 更新・ファイル操作 |

**Evaluator は Trade_Brain には関与しない**（役割分担明確化）。
Evaluator は Trade_System の実装ロジック監査に専念する。

---

## 関連リポジトリ構造（姉妹リポとの対応関係）

本リポジトリは単独で稼働せず、姉妹リポジトリ Trade_System との役割分担で運用される。

```
REX_AI/
├── Trade_System/        ← 姉妹リポ（動的ロジック側）
│   └── 役割: シグナル / Fibonacci / BackTest / MTF エントリー判定 / 決済
│
└── Trade_Brain/         ← 本リポ（静的データ側）
    └── 役割: 8 ペア市況データ / トレード履歴 / レジーム判定 / Plot 抽出
```

**分担原則**（ADR F-8 役割分担原則）:
- Trade_Brain: 市況データ・トレード結果・Plot 抽出（静的データ層）
- Trade_System: エントリーシグナル・Fibonacci・BackTest（動的ロジック層）

### 例外 — 両リポ共存保持ファイル: `src/plotter.py`

本ファイルは複数ルーツが癒合したまま**両リポに共存保持される**。ADR F-8 派生原則
「共存保持の許容」により、機能単位の完全分離ではなく共存保持を許容する設計。

**Trade_Brain ルーツ 3 関数**:
- `save_normalized_plot` — 8 ペア正規化比較プロット生成
- `save_swing_debug_plot` — Swing High/Low 視覚化デバッグ
- `save_entry_debug_plot` — エントリーデバッグ可視化

**Trade_System ルーツ 4 関数**:
- `plot_base_scan` / `plot_swing_check` / `plot_4h_1h_structure` / `plot_1h_window_5m`

呼び出し経路は両リポで完全分離しているため干渉しない。将来の合流点
（Trade_Brain レジーム判定 → Trade_System ロット調整）を物理ファイルレベルで
残すための設計。詳細は `Trade_System/docs/ADR.md` の F-8 派生原則参照。

---

## リポジトリの二層構造（仕組み側 vs 1 次データ資産側）

本リポジトリの全ファイルは以下の二層に大別される。この区別が保守ルールの基本。

### 仕組み側（抽出プロセスを動かす機構）

| ファイル / ディレクトリ | 役割 |
|---|---|
| `main.py` | ラッパー。`configs.rex_chat.main()` を呼び出すエントリポイント |
| `src/` | データ抽出・分析スクリプト群（data_fetch / market / news / regime 等） |
| `configs/` | API キー・データパス等の設定 |
| `requirements.txt` | Python 依存ライブラリ |
| `docs/WEEKLY_UPDATE_WORKFLOW.md` | 週末 Git 更新の手順書（SSoT） |
| `docs/distillation_schema.md` | 蒸留スキーマ仕様 |
| `docs/STRATEGY_WIKI_GUIDE.md` | Wiki 構造・運用ガイド |
| `docs/SYSTEM_OVERVIEW.md`（本ファイル） | システム全体スナップショット |

**変更ルール**: 改修は実証後に反映。コマンド変更時は WORKFLOW.md を即同期更新。

### 1 次データ資産側（抽出成果・追記型）

| ディレクトリ / ファイル | 役割 | 更新単位 |
|---|---|---|
| `logs/daily/YYYY/` | 日次市況テキスト（ボス提供） | 日次追記 |
| `logs/weekly/YYYY/YYYY-M-D_wkNN/` | 週次抽出データ（7 ファイル構成） | 週次生成 |
| `logs/boss's-weeken-Report/` | 週末レポート（既存命名維持） | 週次追記 |
| `distilled/YYYY/distilled-gm-YYYY-M.md` | 月次蒸留アーカイブ（時系列スタック） | 当月追記・月替わりで凍結 |
| `Strategy_Wiki/` | Obsidian Vault ミラー（辞書型ナレッジ） | 週次 Ingest |
| `nlm_sources/monthly/` | NLM 投入パッケージ | `--NLM` フラグ発動時 |
| `data/private_trades.csv` | トレード履歴 | 随時追記 |
| `docs/STATUS.md` | 週次ブリーフ時系列スタック（現在進行形 SSoT） | 週次追記 |
| `docs/Trade-Main.md` | GM Playbook + Weekly Index | 週次追記 |

**変更ルール**（CLAUDE.md §不変ルール参照）:
- `logs/` の既存ファイル内容は書き換えない（追記のみ）
- 過去月の distilled は遡って改変しない（注記追記のみ）
- 過去の Weekly Brief（STATUS.md / Trade-Main.md 内）は凍結
- 事実訂正は「訂正ログ」セクションを新規追加する形で行う

---

## ディレクトリ構造（2026-04-22 時点）

```
Trade_Brain/
├── .CLAUDE.md                  # ClaudeCode 自動読込（ミラー）
├── CLAUDE.md                   # 本リポ運用ルール（2026-04-20 統合版）
├── README.md                   # プロジェクト概要
├── .gitignore
├── .venv/                      # Python 仮想環境
├── main.py                     # ラッパー（configs.rex_chat.main を呼ぶ）
├── requirements.txt            # 依存ライブラリ 9 本
│
├── src/                        # 抽出スクリプト群（11 ファイル）
│   ├── chat.py                     # 対話系
│   ├── daily_report_parser.py      # 日次ログパース
│   ├── data_fetch.py               # yfinance / polygon-api-client による価格取得
│   ├── forecast_simulation.py      # 予測シミュレーション
│   ├── history.py                  # 履歴管理
│   ├── market.py                   # 市況分析
│   ├── news.py                     # RSS ニュース取得（feedparser）
│   ├── plotter.py                  # ★両リポ共存保持★ 32.7KB
│   ├── regime.py                   # レジーム判定
│   ├── test_fetch_30days_multi.py  # 8 ペア 30 日変動率取得
│   ├── track_trades.py             # トレード履歴管理
│   └── utils.py                    # ユーティリティ
│
├── configs/                    # 設定ファイル
│   ├── settings.py                 # パス・API キー等
│   └── rex_chat.py                 # main() エントリポイント本体
│
├── logs/                       # 1 次データ資産（追記のみ）
│   ├── daily/
│   │   └── 2026/                   # 2026 年 3 月〜 日次ログ
│   ├── weekly/
│   │   ├── 2025/                   # 2025 年 週次ポートフォリオ総括
│   │   └── 2026/                   # 2026 年 週次（wk01 〜 wk03 実在）
│   │       ├── 2026-4-3_wk01/
│   │       ├── 2026-4-10_wk02/
│   │       └── 2026-4-17_wk03/
│   └── boss's-weeken-Report/   # 週末レポート（既存命名維持）
│
├── distilled/                  # 月次蒸留アーカイブ
│   ├── 2025/
│   └── 2026/
│       ├── distilled-gm-2026-1.md
│       ├── distilled-gm-2026-2.md
│       ├── distilled-gm-2026-3.md
│       └── distilled-gm-2026-4.md
│
├── Strategy_Wiki/              # Obsidian Vault ミラー（未構築・骨組み待ち）
│   ├── index.md                    # 全ページカタログ（自動生成）
│   ├── _RUNBOOK.md                 # 運用手順＋クエリガイド（手動）
│   ├── log.md                      # 3 操作履歴（自動追記）
│   ├── Regimes/                    # 5 種固定（インターフェース契約）
│   ├── Signals/                    # 6 カテゴリ × N ファイル
│   ├── Events/                     # 4 カテゴリ × N ファイル
│   ├── Instruments/                # ★ 4 週 Rolling Window 内蔵 ★
│   ├── Patterns/                   # 戦略パターン
│   ├── Hypotheses/                 # シナリオ A/B/C
│   └── Journal/                    # 週次索引
│
├── nlm_sources/                # NLM 投入用パッケージ
│   └── monthly/
│       └── YYYY-MM_brain_pack.md
│
├── data/
│   └── private_trades.csv      # トレード履歴（track_trades.py 管理）
│
└── docs/
    ├── SYSTEM_OVERVIEW.md      # 本ファイル
    ├── CLAUDE.md → ../CLAUDE.md（ルート直下の運用ルール）
    ├── Planner_HANDOFF.md      # Planner 引き継ぎ書（Advisor 起草）
    ├── STATUS.md               # 週次ブリーフ時系列スタック（SSoT・週次追記）
    ├── Trade-Main.md           # GM Playbook + Weekly Index
    ├── WEEKLY_UPDATE_WORKFLOW.md  # 週末 Git 更新手順書
    ├── STRATEGY_WIKI_GUIDE.md  # Wiki 構造・運用ガイド
    ├── distillation_schema.md  # 蒸留スキーマ正式仕様
    └── archived/               # 凍結文書置き場（空）
```

---

## データパイプライン（抽出→格納→蒸留→RAG）

本リポジトリの本質は「週次抽出される市況データを時系列で蓄積し、
最終的に NLM-RAG で検索可能な知識資産にする」パイプライン。
全体は 4 段階で構成される。

```
┌─── 【入力層】1 次データソース ─────────────────────────────────────┐
│                                                                     │
│  ① ボス提供（人間由来）             ② 自動取得（main.py --trade --news） │
│    ・Minato 市況テキスト             ・8 ペア 30 日変動率（最新値+%）  │
│    ・daily/YYYY-M-D.txt              ・レジームスナップショット YAML  │
│    ・boss's-weeken-Report/           ・8 ペア正規化 Plot（PNG）       │
│    ・private_trades.csv              ・GM キーワードニュース（RSS）   │
│                                                                     │
└────────────────────┬────────────────────────────────────────────────┘
                     │ ClaudeCode が WEEKLY_UPDATE_WORKFLOW.md に従う
                     ↓
┌─── 【処理層】logs/weekly/YYYY/YYYY-M-D_wkNN/ ─────────────────────┐
│                                                                     │
│  charts/ サブフォルダ（生データに最も近い層）                       │
│    ├── YYYY-MM-DD 〜 YYYY-MM-DD.txt   ← main.py --trade 出力ほぼ生  │
│    ├── YYYY_MM_DD_snapshot.yaml       ← レジーム構造化（機械生成）  │
│    ├── Market conditions -YYYY-M-D~.txt ← Minato 市況+news 統合    │
│    ├── GM Strategy-YYYY-M-D.txt       ← 9 セクション統合（ClaudeCode）│
│    └── Portforio-YYYY-MM-DD.png       ← 8 ペアプロット（PNG・ローカル専用）│
│                                                                     │
│  週次フォルダ直下（構造化ドキュメント層）                           │
│    ├── charts.md         ← charts/ の目次＋今週特徴                 │
│    ├── meta.yaml         ← snapshot+signals+decision_bias+event_risk│
│    ├── review.md         ← 結論/材料/Evidence/Implication/シナリオ   │
│    ├── note.md           ← Macro/Regime 解釈/Key gates/Portfolio    │
│    └── trade_results.md  ← track_trades.py summary 出力             │
│                                                                     │
└────────────────────┬────────────────────────────────────────────────┘
                     │ インデックス追記
                     ↓
┌─── 【SSoT 層】docs/ 週次追記ファイル ─────────────────────────────┐
│                                                                     │
│  logs/weekly/2026/_index.md   ← 当週エントリ追加                   │
│  docs/STATUS.md               ← Weekly Brief 末尾追記              │
│  docs/Trade-Main.md           ← Weekly Index + Distilled Logs 更新 │
│                                                                     │
└────────────────────┬────────────────────────────────────────────────┘
                     │ 同週内で蒸留追記
                     ↓
┌─── 【蒸留層】distilled/YYYY/distilled-gm-YYYY-M.md ───────────────┐
│                                                                     │
│  月内の全週（wk01 / wk02 / ...）を 1 ファイルに時系列スタック       │
│  各週エントリの正規化 5 項目:                                       │
│    - regime      （enum 5 種）                                      │
│    - decision    （signal_id = on/off/watch）                       │
│    - evidence    （close snapshot 8 銘柄）                          │
│    - implication （運用結論・箇条書き）                             │
│    - tags        （gm / monthly_distilled / signal: / event: / 他） │
│                                                                     │
└────────────────────┬───────────────────┬────────────────────────────┘
                     │ 週次              │ --NLM フラグ発動時
                     │ Wiki Ingest       │ 月次パッケージ化
                     ↓                   ↓
┌─── 【Wiki 層】─────────┐   ┌─── 【RAG 層】──────────────────────┐
│  Strategy_Wiki/         │   │  nlm_sources/monthly/              │
│   (Obsidian-Vault ミラー)│   │   YYYY-MM_brain_pack.md            │
│                         │   │   → REX_Trade_Brain (NLM) に投入   │
│  Instruments/ は        │   │   ID: 4abc25a0-4550-4667-ad51-     │
│  4 週 Rolling Window    │   │        754c5d1d1491                │
└─────────────────────────┘   └────────────────────────────────────┘
```

詳細手順は `docs/WEEKLY_UPDATE_WORKFLOW.md` の 8 段階チェックリスト参照。
Wiki Ingest ルールは `docs/STRATEGY_WIKI_GUIDE.md` §6（3 操作サイクル）参照。
NLM 投入ルールは `docs/STRATEGY_WIKI_GUIDE.md` §7-4（WEEKLY_UPDATE コマンド）参照。

---

## 時間スケール別の情報階層（戦略提案時の参照先）

情報は時間スケールごとに責務を分担している。戦略提案・環境認識で「どこを引くか」は
時間軸で決まる。

| 時間スケール | 主参照先 | 理由 |
|---|---|---|
| 当週（現在進行形） | `docs/STATUS.md` 末尾 Weekly Brief | 現在の市況 SSoT |
| 直近 1 ヶ月 | `Strategy_Wiki/Instruments/` 4 週 Rolling Window + Journal Dataview | Wiki 内で瞬時俯瞰可能 |
| 1 ヶ月超〜数ヶ月 | NLM-RAG（REX_Trade_Brain） | 月次 brain_pack で投入済 |
| 1 次履歴全期間 | `logs/weekly/` + `distilled/` 直読 | 全原典が永続保存 |

詳細なクエリガイドは `docs/STRATEGY_WIKI_GUIDE.md` §8 参照。

---

## 週次運用サイクル（WEEKLY_UPDATE コマンド）

週末 Git 更新は `WEEKLY_UPDATE` コマンドで一元化される。

### コマンド書式

```
# 通常週（NLM 投入なし）
WEEKLY_UPDATE =YYYY-M-DD

# NLM 投入を含める週（ボス判断・末尾 --NLM フラグ）
WEEKLY_UPDATE =YYYY-M-DD --NLM
```

### 実行例

```
# 4/24（金）Git 更新・NLM 投入なし
WEEKLY_UPDATE =2026-4-24

# 4/24（金）Git 更新・同時に 4 月分を NLM 投入
WEEKLY_UPDATE =2026-4-24 --NLM
```

### RTK プレフィックスルール

本リポでは**すべての git コマンドに `rtk` プレフィックス必須**。
詳細は `CLAUDE.md` §RTK ルール参照。

```bash
rtk git add logs/weekly/2026/2026-4-24_wk04/
rtk git commit -m "weekly: 2026-4-24_wk04 review + trade_results + charts"
rtk git push origin main
```

### 投入タイミングの判断

- 通常は月末週の Git 更新時に `--NLM` 付与
- 5 週目まである月は wk05 Git 更新時、4 週で終わる月は wk04 Git 更新時
- 前月分を翌月 wk01 で締めたい場合は `=前月の金曜日付 --NLM` で明示指定
- 5 週以上 NLM 投入が空いた場合、ClaudeCode が警告文を自動生成
- ボス判断で投入スキップも許容（RAG 汚染回避の meta 判断）

---

## 設計哲学（裁量思想の Trade_Brain への適用）

本リポは Trade_System と設計哲学（原則α/β/γ・ADR F-8）を共有する。

### 原則α（シンプルな土台の保守）

- 1 次データは追記のみ。過去改変禁止
- 過去月 distilled は凍結。注記追記のみで訂正
- Rolling Window は Instruments/ のみ（全カテゴリ拡張しない）
- Strategy_Wiki/ に snapshots/ ディレクトリは作らない（Git 履歴で代替）

### 原則β（ノーリスク化後は伸ばさない）

- 完成した docs/ 文書は無闇に改訂しない
- 確定した regime_id / instrument_id enum は契約として固定
- 新規カテゴリ追加は Evaluator/Advisor 承認後のみ

### 原則γ（導入タイミングは安定性従属）

- Strategy_Wiki 本体構築は `docs/` 骨格が整ってから
- NLM 投入は月次で一括（当月途中の投入は RAG 精度低下）
- Trade_System との合流点実装は Trade_System 安定化後

### ADR F-8 派生原則（共存保持の許容）

- `src/plotter.py` は両リポに共存保持（関数分割しない）
- 将来の合流点（Trade_Brain レジーム → Trade_System ロット）を物理ファイルで残す

---

## NLM 構成

```
稼働中（2026-04-18 新規構築済み）:
  REX_Trade_Brain  — 本リポ対応 NLM
    ID: 4abc25a0-4550-4667-ad51-754c5d1d1491
    投入基準: distilled/ 配下のみ（raw/ は不投入）
    投入経路: nlm_sources/monthly/YYYY-MM_brain_pack.md

姉妹 NLM（参照のみ・本リポからは投入しない）:
  REX_System_Brain — Trade_System 用
    ID: da84715f-9719-40ef-87ec-2453a0dce67e

廃止（MCP 切り離し済み）:
  旧 REX_Trade_Brain
    ID: 2d41d672-f66f-4036-884a-06e4d6729866
    切り離し理由: RAG 汚染排除（却下案・修正前実装の混入）
    切り離し日: 2026-04-18
    1 次履歴の参照先: Git コミット履歴
```

詳細は `Trade_System/docs/REX_027_BOSS_DIRECTIVE.md` v2 参照。

---

## 未解決・保留項目（引き継ぎ時の注意）

| 項目 | 状態 | 再開条件 |
|---|---|---|
| Strategy_Wiki/ 本体構築 | ⬜ 未着手（骨組み設計のみ完了） | `docs/STRATEGY_WIKI_GUIDE.md` 確定後 |
| MONTHLY_DISTILLATION_WORKFLOW.md | ⬜ 未作成 | SYSTEM_OVERVIEW 完了後 |
| NLM_INGEST_WORKFLOW.md | ⬜ 未作成 | MONTHLY_DISTILLATION 完了後 |
| Trade_System_INTEGRATION.md | ⬜ 未作成（将来構想） | Trade_System Phase 4 完了後 |
| 初回 `--NLM` 投入 | ⬜ 未実行 | 4/24 金曜 Git 更新以降・ボス判断 |
| Vault 側 `wiki/trade_brain/` 骨組み作成 | ⬜ 未着手 | メタ文書確定後 |
| 2025 年分 logs/weekly/ の遡及構造化 | ⬜ 保留 | 2026 年分安定後 |

---

## 外部リソース参照先

```
設計文書:
  docs/STRATEGY_WIKI_GUIDE.md      — Wiki 構造・運用ガイド
  docs/distillation_schema.md      — 蒸留スキーマ正式仕様
  docs/WEEKLY_UPDATE_WORKFLOW.md   — 週末 Git 更新手順書
  docs/Planner_HANDOFF.md          — Planner 引き継ぎ書（Advisor 起草）
  CLAUDE.md                        — ClaudeCode 運用ルール

1 次データ SSoT:
  docs/STATUS.md                   — 現在進行形 Weekly Brief スタック
  docs/Trade-Main.md               — GM Playbook + Weekly Index

Vault:
  C:\Python\REX_AI\REX_Brain_Vault\wiki\trade_brain\   — Obsidian ハブ
  Trade_Brain/Strategy_Wiki/                            — Git ミラー

NLM:
  REX_Trade_Brain   (4abc25a0-4550-4667-ad51-754c5d1d1491)  — 本リポ対応
  REX_System_Brain  (da84715f-9719-40ef-87ec-2453a0dce67e)  — 姉妹リポ用

GitHub:
  Minato33440/Trade_Brain         — 本リポ
  Minato33440/Trade_System        — 姉妹リポ

姉妹 SYSTEM_OVERVIEW:
  Trade_System/docs/SYSTEM_OVERVIEW.md  — 対称文書
```

---

## データ移行履歴

| 日付 | 内容 |
|---|---|
| 2026-04-18 | Trade_System/logs/gm/ → raw/ に移行（gm/ 階層除去） |
| 2026-04-18 | Trade_System/versions/distilled/ → distilled/ に移行 |
| 2026-04-18 | NLM 全面再構築（旧 REX_Trade_Brain MCP 切り離し・新規 2 件作成） |
| 2026-04-18 | 週次運用ファイル 3 件移設（STATUS / Trade-Main / WEEKLY_UPDATE_WORKFLOW） |
| 2026-04-19 | Planner_HANDOFF.md 起草（Advisor 発行） |
| 2026-04-20 | raw/ → logs/ リネーム（データ性質に合わせた命名） |
| 2026-04-20 | src/ 内パス参照を logs/ 構造に整合（依存問題解決） |
| 2026-04-22 | STRATEGY_WIKI_GUIDE.md 全面改訂（MCP-Obsidian 横断・Rolling Window・--NLM 運用） |
| 2026-04-22 | SYSTEM_OVERVIEW.md 初版起草（本ファイル） |

---

管理: Planner（本リポ Trade_Brain 担当）/ Minato（ボス）
*初版発行: 2026-04-22 / Planner 起草*
*関連: Trade_Brain/CLAUDE.md /*
*      Trade_Brain/docs/STRATEGY_WIKI_GUIDE.md /*
*      Trade_Brain/docs/WEEKLY_UPDATE_WORKFLOW.md /*
*      Trade_Brain/docs/distillation_schema.md /*
*      Trade_System/docs/SYSTEM_OVERVIEW.md（姉妹文書・対称参照）*
