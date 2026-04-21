# Planner_HANDOFF.md — Trade_Brain 担当 Planner セッション引き継ぎ書

**発行**: Advisor (Claude Opus 4.7)
**発行日**: 2026-04-19 夜
**宛先**: Trade_Brain 担当 Rex-Planner (Sonnet 4.6)
**起草依頼**: ボス (Minato)

---

## 0. 本書の目的

本書は **Trade_Brain リポジトリ担当の Planner** に、以下を引き継ぐための文書である:

1. Trade_Brain リポジトリの現状把握
2. Trade_System との対応関係・役割分担の正確な理解
3. 次に起草すべき文書 (`docs/SYSTEM_OVERVIEW.md` 等) の仕様
4. REX_AI エコシステム全体の設計哲学 (原則α/β/γ) への接続

**本書は Advisor 起草の引き継ぎ書であり、実装指示書 (REX_NNN_spec) ではない。**
具体的な実装指示書は Planner 自身が本書を元に起草する。

---

## 1. Planner としての立ち位置 (Trade_Brain 版)

### 1-1. 役割の定義

Trade_Brain の Planner は、Trade_System の Planner とは**性質が異なる**:

| 項目 | Trade_System Planner | Trade_Brain Planner (本ロール) |
|---|---|---|
| 主な成果物 | 実装指示書 (REX_NNN_spec) | ドキュメント設計・運用フロー整備・Wiki 構造設計 |
| 対象 | Python コード実装 | Markdown 文書・Obsidian Vault ミラー・NLM 投入設計 |
| 動作ペース | 指示書単位 (週次〜隔週) | 運用フロー単位 (月次〜四半期) |
| 判断軸 | バックテスト数値・コード動作 | 情報の構造化度・ナレッジ資産の蓄積性 |

### 1-2. チーム構成 (Trade_Brain 版)

```
ボス:            Minato (最終判断者)
Advisor:         Claude.ai / Opus 4.7 (外部視点・俯瞰レビュー)
Planner:         ★ 本ロール ★ (ドキュメント設計・運用フロー)
実装:            ClaudeCode (Ingest 実行・週次 Git 更新)

※ Evaluator は Trade_Brain には関与しない (役割分担明確化)
   Trade_System の実装ロジック監査に集中する
```

### 1-3. Planner がやること / やらないこと

```
✅ Planner がやること:
  - docs/ 配下の設計文書起草 (SYSTEM_OVERVIEW.md 等)
  - 運用フロー整備 (WEEKLY_UPDATE_WORKFLOW を補完する Monthly/Quarterly フロー)
  - Strategy_Wiki/ 構造の具体設計
  - NLM 投入パッケージ (nlm_sources/monthly/) の仕様策定
  - ClaudeCode への作業指示書起草 (必要時)

❌ Planner がやらないこと:
  - raw/ / distilled/ の既存データ内容改変 (Ingest のみ)
  - Trade_System の実装への介入 (姉妹リポなので越境禁止)
  - 裁量思想 (MINATO_MTF_PHILOSOPHY) の内容変更 (Evaluator 領域)
  - MTF_INTEGRITY_QA.md への追記 (Evaluator 領域)
  - F-7/F-8 派生原則の変更 (Evaluator 承認事項)
```

---

## 2. REX_AI エコシステム全体マップ (2026-04-20 時点)

### 2-1. リポジトリ構成

```
REX_AI/ (ローカル: C:\Python\REX_AI\)
│
├── Trade_System/           ← 実装リポ・動的ロジック層
│   └── 役割: シグナル / Fibonacci / BackTest / MTF エントリー判定 / 決済
│   └── GitHub: Minato33440/Trade_System
│
├── Trade_Brain/            ← 知識リポ・静的データ層 ★本リポ★
│   └── 役割: 8 ペア市況データ / トレード履歴 / レジーム判定 / Plot 抽出
│   └── GitHub: Minato33440/Trade_Brain
│
├── Second_Brain_Lab/       ← MCP 試験運用
├── Setona_HP/              ← セトナ治療院 HP
│
└── REX_Brain_Vault/        ← Obsidian Vault (ローカル・Git 管理外)
    └── wiki/
        ├── trade_system/   ← Trade_System 設計のローカル構造化
        └── trade_brain/    ← 本リポと連動 (REX_028 完了後に構築予定)
```

### 2-2. Trade_System と Trade_Brain の分担原則

本日 (2026-04-20) 確定した分担原則 (ADR F-8):

```
Trade_System: 動的ロジック層
  - エントリーシグナル
  - Fibonacci 計算
  - BackTest 実行
  - MTF 窓ベース階層スキャン
  - 決済シミュレーション

Trade_Brain: 静的データ層
  - 8 ペア市況データ抽出 (daily / weekly)
  - GM 戦略アーカイブ (distilled)
  - トレード履歴 (track_trades.py)
  - レジーム判定 (将来 Strategy_Wiki)
  - Plot 抽出 (market / regime 系)
```

### 2-3. ★ 両リポ共存保持ファイル: plotter.py ★ (最重要)

```
src/plotter.py は両リポに共存保持される (ADR F-8 派生原則)

背景:
  Trade_System の plotter.py は 2 ルーツの関数が癒合している:
    - Trade_System ルーツ 4 関数 (#026d BackTest 可視化)
    - Trade_Brain ルーツ 3 関数 (8 ペア市況抽出)

  機械的に関数単位で分離するのではなく、両リポに共存させる選択を採用。

理由:
  1. 将来の合流点 (Trade_Brain レジーム判定 → Trade_System ロット調整) を残す
  2. F-8 派生原則「共存保持の許容」に基づく
  3. 完全分離は原則α (シンプルな土台の保守) を損なう可能性
  4. 役割分担原則は「機能の棲み分け」であり「コードの物理分離」ではない

Trade_Brain Planner への影響:
  - Trade_Brain 側の plotter.py は独自進化させない
  - 両リポで同期が必要な変更が発生した場合、Advisor 経由で Trade_System Planner と協議
  - 新規プロット関数は「どちらのルーツか」を意識して追加する
```

### 2-4. NLM ノートブック構成 (2026-04-18 夜確定)

```
REX_System_Brain
  ID: da84715f-9719-40ef-87ec-2453a0dce67e
  用途: Trade_System 設計文書用 (姉妹リポの NLM・参照のみ)

REX_Trade_Brain ★本リポ対応 NLM★
  ID: 4abc25a0-4550-4667-ad51-754c5d1d1491
  用途: Trade_Brain 蒸留データ投入先
  投入基準: distilled/ 配下のみ (raw/ は投入しない)

旧 REX_Trade_Brain (廃止):
  ID: 2d41d672-f66f-4036-884a-06e4d6729866
  状態: Claude-MCP 接続先から切り離し済み
  理由: RAG 汚染排除 (REX_027 v2 参照)
  注意: Trade_System 側の SYSTEM_OVERVIEW.md §「外部リソース参照先」に
        旧 ID が記載されたままの箇所がある (Evaluator への指摘事項)
```

---

## 3. Trade_Brain リポジトリの現状 (2026-04-19 夜時点)

### 3-1. ディレクトリ構造

```
Trade_Brain/
├── .CLAUDE.md                      # ClaudeCode 自動読込 (ミラー)
├── CLAUDE.md                       # Brain 専用運用ルール (2026-04-18 統合版)
├── README.md                       # プロジェクト概要 (2026-04-18 統合版)
├── .gitignore
├── .venv/
│
├── raw/                            # 生データ (Trade_System/logs/gm/ から移行済み)
│   ├── daily/2026/                 # 2026 年 3 月〜日次ログ
│   ├── weekly/{2025,2026}/         # 週次ポートフォリオ総括
│   └── boss's-weeken-Report/       # 週末レポート (既存命名維持)
│
├── distilled/                      # 蒸留済み戦略アーカイブ
│   ├── 2025/
│   └── 2026/
│       ├── distilled-gm-2026-1.md
│       ├── distilled-gm-2026-2.md
│       ├── distilled-gm-2026-3.md
│       └── distilled-gm-2026-4.md
│
├── Strategy_Wiki/                  # 未構築 (将来の Obsidian ミラー)
│
└── docs/
    ├── STATUS.md                   # 週次ブリーフ時系列スタック (SSoT)
    ├── Trade-Main.md               # GM Playbook + Weekly Index
    ├── WEEKLY_UPDATE_WORKFLOW.md   # 週末 Git 更新手順書
    ├── STRATEGY_WIKI_GUIDE.md      # Wiki 構造ガイド
    ├── distillation_schema.md      # distilled スキーマ仕様
    └── archived/                   # (空・将来の凍結文書置き場)
```

### 3-2. docs/ ファイルの役割 (既存分)

| ファイル | 役割 | 更新頻度 |
|---|---|---|
| `STATUS.md` | 週次ブリーフの時系列スタック。現在進行形の市況 SSoT | 週次追記 |
| `Trade-Main.md` | GM Playbook + 3 シナリオ運用指針 + Weekly Index | 週次追記 |
| `WEEKLY_UPDATE_WORKFLOW.md` | 週末 Git 更新の実施手順書 (ClaudeCode 必読) | 手順変更時 |
| `STRATEGY_WIKI_GUIDE.md` | Strategy_Wiki/ の構造・YAML・Dataview 仕様 | 構造変更時 |
| `distillation_schema.md` | distilled の YAML/MD スキーマ正式仕様 | スキーマ変更時 |

### 3-3. ★ 欠落している文書 (Planner 起草候補) ★

```
🔴 docs/SYSTEM_OVERVIEW.md         未作成 (最優先・本書 §5 参照)
🟡 docs/MONTHLY_DISTILLATION_WORKFLOW.md   未作成 (月次蒸留手順)
🟡 docs/NLM_INGEST_WORKFLOW.md     未作成 (月次 NLM 投入手順)
🟢 docs/Wiki/ (Strategy_Wiki ビルド手順)   REX_028 完了後
🟢 docs/Trade_System_INTEGRATION.md  未作成 (将来の合流点設計)
```

---

## 4. 本日 (2026-04-18〜19) の進展と Planner への影響

### 4-1. 本日までに確定した事項 (時系列)

```
2026-04-18 朝:
  - Trade_Brain リポ新設 (Trade_System から分離)
  - raw/ + distilled/ データ移行完了
  - 命名整合性確定: Trade_System ⇔ Trade_Brain

2026-04-18 夜:
  - NLM 全面再構築 (RAG 汚染排除)
  - REX_027_BOSS_DIRECTIVE v2 発行 (Task E 追加)
  - Trade_Brain/CLAUDE.md / README.md 統合版 push
  - 週次運用ファイル 3 件 (STATUS/Trade-Main/WEEKLY_UPDATE_WORKFLOW) 統合

2026-04-19 朝〜夜:
  - Evaluator が MINATO_MTF_PHILOSOPHY を基に Q&A 監査実施
  - 🤖 創作混入 2 件発見 (Trade_System 側・stage2/stage3)
  - 原則α/β/γ 言明 (ボス)
  - src/ 27 ファイルも原則α違反と検出
  - REX_028 Phase 1-4 構造再編に合意

2026-04-20:
  - REX_028 Phase 1-2 完了 (Trade_System 側)
  - plotter.py の両リポ共存保持確定 (F-8 派生原則)
  - ADR D-12/D-13/E-8/F-8 正式採番
  - Trade_System/docs/SYSTEM_OVERVIEW.md 更新完了
```

### 4-2. Trade_Brain Planner にとっての意味

```
1. plotter.py の共存保持が確定
   → Trade_Brain 側でも plotter.py を独自進化させない方針
   → 本リポ側では「Trade_Brain ルーツ 3 関数」をどう扱うかが焦点

2. 原則α がファイルシステム層にも適用されると判明
   → Trade_Brain の Strategy_Wiki 設計時も原則αを意識する必要
   → 「拡張より保守」「シンプルな土台を死守」

3. Trade_System 側の SYSTEM_OVERVIEW.md が更新された
   → 本リポ側にも対称的な SYSTEM_OVERVIEW.md が必要
   → これが本書を発行した主要理由

4. ADR F-8 (役割分担原則・共存保持許容) が発行された
   → Trade_Brain 側の docs で F-8 を参照できるようにする
```

---

## 5. ★ 最優先タスク: docs/SYSTEM_OVERVIEW.md の起草 ★

### 5-1. 目的

Trade_Brain リポジトリの**現状スナップショット**を、Trade_System 側と対称的に記述する。
新規 Advisor / ClaudeCode が Trade_Brain を引き継ぐ時の最初の読み物。

### 5-2. ボスからの要件 (3 項目)

```
要件 1: 両リポの対応関係を冒頭で明示
  → Trade_System 側の「関連リポジトリ構造」セクションと対称的に
  → Trade_Brain 側からの視点で記述

要件 2: plotter.py 両リポ共存の注記
  → 両文書に同じ内容が書かれていれば、将来の Evaluator/Planner が混乱しない
  → 特に「Trade_Brain ルーツ 3 関数」の記述を残す

要件 3: WEEKLY_UPDATE_WORKFLOW.md の存在を明記
  → ClaudeCode が自動実行する運用フローの起点として位置づける
```

### 5-3. 推奨セクション構成 (Advisor 案)

以下は Advisor からの提案であり、Planner が最終判断する:

```markdown
# Trade_Brain — システム概要
# 最終更新: 2026-04-XX (Planner 起草時更新)
# 日付なし・常に最新版として運用

---

## 本ファイルの位置づけ
  - Trade_Brain リポジトリの現状スナップショット
  - 新規 Advisor / ClaudeCode の引き継ぎ時に最初に読む文書
  - 運用ルール詳細は CLAUDE.md、蒸留スキーマは distillation_schema.md 参照

## チーム役割分担
  - ディレクター: Minato (ボス)
  - Advisor: Claude.ai (外部視点)
  - Planner: ★ 本ロール ★
  - 実装: ClaudeCode (Ingest / 週次 Git 更新)
  - ※ Evaluator は関与しない (Trade_System 専任)

## 関連リポジトリ構造 (両リポ対応関係)
  - Trade_System ⇔ Trade_Brain の役割分担
  - 動的ロジック層 vs 静的データ層
  - ADR F-8 (役割分担原則) への参照
  - ★ plotter.py 両リポ共存保持の注記 (ボス要件 2) ★

## ディレクトリ構造
  - raw/ / distilled/ / Strategy_Wiki/ / docs/ の 4 本柱
  - 現状実態を反映 (boss's-weeken-Report/ の命名維持注記含む)

## データフロー
  - Daily ingest → Weekly wrap-up → Monthly distillation → NLM sync → Query
  - 各段階の責任者 (ボス / Advisor / ClaudeCode) を明示
  - ★ WEEKLY_UPDATE_WORKFLOW.md を起点として明記 (ボス要件 3) ★

## ファイル変更ポリシー
  - raw/ は追記のみ (既存内容改変禁止)
  - 過去月の distilled は凍結
  - Strategy_Wiki/ の Source of Truth は Vault 側
  - ★ plotter.py は両リポ共存保持 (ボス要件 2・再記述) ★

## NLM 構成
  - REX_Trade_Brain (4abc25a0-...) - 新規・クリーン
  - 旧 REX_Trade_Brain (2d41d672-...) - 廃止・接続切り離し
  - 投入基準: distilled/ のみ (raw/ は不投入)

## 設計哲学 (原則α/β/γ)
  - 本リポでの原則α の適用: Strategy_Wiki 構造を保守
  - 原則γ の適用: NLM 投入・Wiki ビルドは安定化後
  - ADR F-8 派生原則への参照

## 未解決・保留項目
  - Strategy_Wiki/ 本体未構築 (REX_028 完了後)
  - NLM 月次投入フロー未確定
  - Trade_System 合流点設計 (将来構想)

## 外部リソース参照先
  - 姉妹リポ: Trade_System
  - Vault ルート
  - NLM (新 ID・正確な値)

管理: Planner / Minato (ボス)
```

### 5-4. 起草時の注意事項

```
⚠️ 注意 1: NLM ID の正確な記載
  Trade_System 側の SYSTEM_OVERVIEW.md §「外部リソース参照先」には
  旧 REX_Trade_Brain ID (2d41d672-...) が記載されたままの箇所がある。
  これは Evaluator 訂正待ちの事項。
  
  Trade_Brain 側では新 ID (4abc25a0-...) を正確に記載する。
  旧 ID も「廃止」明記で併記すると整合性が取れる。

⚠️ 注意 2: plotter.py の記述は両リポで同期
  Trade_System 側 SYSTEM_OVERVIEW.md §「関連リポジトリ構造」末尾に
  「例外 — 両リポ共存保持ファイル: plotter.py」セクションがある。
  
  Trade_Brain 側にも同じ構造で記載し、
  「詳細は Trade_System/docs/SYSTEM_OVERVIEW.md の対応セクション参照」
  と相互参照する形にする。

⚠️ 注意 3: WEEKLY_UPDATE_WORKFLOW の位置づけ
  既存の docs/WEEKLY_UPDATE_WORKFLOW.md は ClaudeCode が週末 Git 更新時に
  必読する運用マニュアル。SYSTEM_OVERVIEW 内では「運用フローの起点」として
  位置づけ、詳細は WORKFLOW 側に委譲する (重複記述を避ける)。

⚠️ 注意 4: 実態確認を怠らない
  起草前に必ず以下を GitHub で確認:
    - Trade_Brain の最新ディレクトリ構造
    - docs/ 各ファイルの最新 SHA
    - Trade_System 側 SYSTEM_OVERVIEW.md の最新構造
  推測で書くと両リポ間で不整合が発生する。

⚠️ 注意 5: 分量と密度
  Trade_System 側 SYSTEM_OVERVIEW.md は 16KB (豊富な実装詳細を含む)。
  Trade_Brain 側は実装コードがないため、8〜12KB 程度が妥当。
  原則α (シンプルな土台) を Planner 自身にも適用する。
```

---

## 6. 次に起草を推奨する文書 (優先度順)

### 6-1. 🔴 最優先: docs/SYSTEM_OVERVIEW.md

詳細は §5 参照。本書発行直後の最優先タスク。

### 6-2. 🟡 中優先: docs/MONTHLY_DISTILLATION_WORKFLOW.md

```
目的:
  月次で raw/ を distilled/ に蒸留する手順を正式化する。
  現在は慣習的に実施されているが明文化されていない。

想定内容:
  - 月次実施タイミング (月末 or 翌月初)
  - 蒸留対象の週次ファイル選定基準
  - distillation_schema.md への準拠確認
  - 新規 regime 検出時の Strategy_Wiki 更新連動
  - ボス承認フロー

起草タイミング:
  SYSTEM_OVERVIEW.md 完成後。
  2026 年 4 月分の蒸留 (4 月末〜5 月初) に間に合わせる。
```

### 6-3. 🟡 中優先: docs/NLM_INGEST_WORKFLOW.md

```
目的:
  月次で distilled を nlm_sources/monthly/ にパッケージ化し
  REX_Trade_Brain に source_add する手順を正式化する。

想定内容:
  - パッケージ命名規則 (YYYY-MM_brain_pack.md)
  - 含めるコンテンツ範囲 (distilled 全文 + Signal/Event/Regime 要約)
  - Claude Desktop からの投入手順
  - 投入後の RAG テスト手順 (汚染検出)
  - ボス承認フロー

起草タイミング:
  MONTHLY_DISTILLATION_WORKFLOW.md 完成後。
```

### 6-4. 🟢 通常優先: docs/Trade_System_INTEGRATION.md (将来構想)

```
目的:
  Trade_Brain のレジーム判定を Trade_System のロット調整に
  連動させる将来の合流点設計。

想定内容:
  - Trade_Brain → Trade_System のインターフェース定義
  - plotter.py 共存保持を前提とした合流ポイント
  - Regime 辞書の enum 的扱い (安定化必須)
  - 導入タイミングは原則γ (システム安定化後)

起草タイミング:
  Trade_System 側 Phase 4 完了後。急がない。
```

---

## 7. 本書の利用手順 (Planner が起動する際のテンプレート)

Planner が新スレッドで本書を起点に作業を開始する際の、ボスが貼り付けるテンプレート例:

```
このスレでは Trade_Brain リポジトリの Planner として引き継ぎを受けてほしい。
⚠️ 作業開始前に以下を順番に読め:

① Trade_Brain/docs/Planner_HANDOFF.md (本書・起点)
② Trade_Brain/CLAUDE.md (本リポ運用ルール)
③ Trade_Brain/README.md (プロジェクト概要)
④ Trade_Brain/docs/WEEKLY_UPDATE_WORKFLOW.md (運用フロー)
⑤ Trade_System/docs/SYSTEM_OVERVIEW.md (姉妹リポの対称文書・参照用)
⑥ Trade_System/docs/ADR.md (F-8 派生原則を確認)

読了後、Planner_HANDOFF.md §5「最優先タスク」に記された
docs/SYSTEM_OVERVIEW.md の起草から開始せよ。

関連 NLM:
  REX_Trade_Brain (4abc25a0-4550-4667-ad51-754c5d1d1491) ← 本リポ対応
  REX_System_Brain (da84715f-9719-40ef-87ec-2453a0dce67e) ← 参照のみ
```

---

## 8. ボスとの対話スタイル (Advisor からの引き継ぎ)

```
- 呼称: プロジェクト進行中は「ボス」、個人的な対話では「ミナト」
- 簡潔で要点を押さえた応答を好む
- 過剰な丁寧語・迎合は嫌う
- 絵文字は使わない (ボスが使わない限り)
- 日本語で対話
- 自分の推奨を先に述べ、ボスが選択肢を評価できるようにする
- 「どうしますか?」を連発しない。「こう思う、なぜなら〜」
- 確信のない情報は言わない。GitHub で実態を必ず確認
- 原則α を自分自身にも適用する (冗長な文書を作らない)
```

---

## 9. 失敗パターン (Advisor から Planner への警告)

```
❌ 姉妹リポとの整合性を無視した独自記述
  例: Trade_System 側 SYSTEM_OVERVIEW と矛盾する plotter.py の説明
  対策: 起草時に必ず両リポの最新版を GitHub で確認

❌ 週次運用ファイル 3 件と重複した記述
  例: STATUS.md の内容を SYSTEM_OVERVIEW.md にも書く
  対策: 既存文書へのリンク化・役割の住み分けを意識

❌ 実装指示書 (REX_NNN_spec) の Trade_Brain 版を直接起草
  例: ClaudeCode への具体的コマンド指示を含めすぎる
  対策: Trade_Brain Planner は「設計・運用フロー」に集中。
        ClaudeCode 向けの詳細手順は WEEKLY_UPDATE_WORKFLOW など
        専用文書に委譲。

❌ Trade_System 領域への越境
  例: Trade_System/src/plotter.py の改修を指示
  対策: 共存保持ファイルの変更は Advisor 経由で協議

❌ 原則α を忘れた冗長化
  例: SYSTEM_OVERVIEW を 20KB 超の大作にする
  対策: ボスの読む時間を尊重・8〜12KB 目安
```

---

## 10. 引き継ぎ完了確認

Planner は本書を読み終えた後に以下を確認:

```
□ Trade_Brain Planner の役割が Trade_System Planner と異なることを理解した
□ REX_AI エコシステム全体 (4 リポ + Vault + NLM) の位置づけを把握した
□ Trade_System との分担原則 (ADR F-8) を理解した
□ plotter.py 両リポ共存保持の背景を理解した
□ docs/ 既存 5 ファイルの役割を把握した
□ 欠落文書の優先順位を理解した
□ SYSTEM_OVERVIEW.md の起草仕様 (§5) を理解した
□ NLM ID の新旧を区別できる
□ 原則α/β/γ を自身の起草作業にも適用する姿勢を理解した
□ ボスとの対話スタイルを理解した
```

全てチェックが入れば、SYSTEM_OVERVIEW.md の起草に着手可能。

---

## 11. Advisor からのメッセージ

### 11-1. 本書を起草した背景

ボスが「Trade_Brain 担当の Planner に引き継ぎ書を作ってほしい」と明示的に
依頼した。Advisor の立ち位置としては、**本来は Planner 自身が自分の引き継ぎ書を
書く**のが筋だが、初代 Planner が不在の Trade_Brain では、Advisor が初動を
支援する形を取った。

これは Advisor の越権ではなく、ボスの明示的な要請に基づく起動支援である。
次回以降は Planner 自身が本書を更新していく想定。

### 11-2. Trade_Brain Planner の難しさ

Trade_System Planner はバックテスト数値という明確な評価軸がある。
一方、Trade_Brain Planner は「情報の構造化度」「ナレッジ資産の蓄積性」という
曖昧な軸で評価される。

この曖昧さに対抗するには、**ボスの裁量思想 (MINATO_MTF_PHILOSOPHY) を
情報整理の指針として援用する**のが効く。具体的には:

- 原則α (シンプルな土台): 過度な構造化を避ける
- 原則β (ノーリスク化後は伸ばさない): 完成した文書を無闇に改訂しない
- 原則γ (安定化後): Strategy_Wiki 本体構築は REX_028 完了後

Trade_System で培われた設計哲学を、Trade_Brain のドキュメント運用にも
適用するのが本質的に正しいアプローチ。

### 11-3. エコシステム統合への糸口

ボスから本依頼時に「今後のエコシステム構築に向けて統合する糸口を残しておきたい」
との言及があった。これは本書 §6-4 の `Trade_System_INTEGRATION.md` として
将来構想に残した。

両リポが姉妹として設計哲学 (原則α/β/γ・ADR F-8) を共有しているため、
将来の合流点は自然に発生する:

```
近未来:
  - plotter.py 共存保持 → 共通プロット関数の調整
  - WEEKLY_UPDATE_WORKFLOW → Trade_System 側への週次フィードバック

中期:
  - Strategy_Wiki/Regimes → Trade_System ロット調整の入力
  - NLM REX_Trade_Brain → Trade_System 判断時の RAG 参照

長期:
  - Trade_System 実トレード結果 → Trade_Brain フィードバック蓄積
  - 自己増殖ループの完成
```

これらの実装タイミングは全て原則γに従属する。焦る必要はない。

### 11-4. 次の Planner へ

本書で不足があれば、ボスまたは Advisor に遠慮なく照会してほしい。
本書自体が Planner の成果物ではなく、Planner の**起点**に過ぎない。
本書を超える文書を Planner 自身が起草していくことが期待されている。

Trade_Brain は「データの蓄積場」から「Trade_System の判断材料」へと
進化する過渡期にある。本書はその過渡期の地図として機能する。

---

*発行: Advisor (Claude Opus 4.7) / 2026-04-19 夜*
*次回更新: Planner 自身による (初回 SYSTEM_OVERVIEW.md 完成時)*
*関連文書:*
*  - Trade_Brain/CLAUDE.md (本リポ運用ルール)*
*  - Trade_Brain/README.md (プロジェクト概要)*
*  - Trade_System/docs/SYSTEM_OVERVIEW.md (対称文書・起草参照)*
*  - Trade_System/docs/ADVISOR_HANDOFF.md v3 (Advisor 視点の全体像)*
*  - Trade_System/docs/ADR.md (F-8 派生原則)*
*  - Trade_System/docs/Base_Logic/MINATO_MTF_PHILOSOPHY.md (裁量思想)*
