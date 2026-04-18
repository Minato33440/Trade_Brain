# Trade_Brain

REX AI Trade System のマクロ市況・戦略アーカイブ専用リポジトリ。

## 対比構造

```
Trade_System  ←→  Trade_Brain
  実装・コード     知識・判断
  （仕組み）       （頭脳）
```

| 観点 | Trade_System | Trade_Brain |
|---|---|---|
| 対象 | 過去データ（83,112本 / 2年分） | 現在進行形の市況 |
| 更新頻度 | 数値凍結後は不変 | 毎日増える |
| 参照頻度 | バックテスト時のみ | ほぼ毎日 |
| 目的 | ロジック最適化 | 意思決定支援 |
| 成果物 | PF / 勝率 / MaxDD | 実トレード判断 |

## リポジトリ構成（2026-04-18 データ移行完了版 + 週次運用ファイル統合版）

```
Trade_Brain/
├── .CLAUDE.md                  # ClaudeCode 自動読込（ミラー）
├── CLAUDE.md                   # Brain 専用運用ルール
├── README.md                   # 本ファイル
├── .gitignore
├── .venv/                      # Python 仮想環境
│
├── raw/                        # 生データ（Trade_System/logs/gm/ から移行済み）
│   ├── daily/
│   │   └── 2026/               # 2026年3月〜 日次ログ
│   ├── weekly/
│   │   ├── 2025/
│   │   └── 2026/
│   └── boss's-weeken-Report/   # 週末レポート
│
├── distilled/                  # 蒸留済み戦略アーカイブ（移行済み）
│   ├── 2025/
│   └── 2026/
│       └── distilled-gm-2026-M.md
│
├── Strategy_Wiki/              # Obsidian Vault 同期対象（wiki/trade_brain/ のミラー）
│   ├── Regimes/                # レジーム辞書
│   ├── Signals/                # シグナル辞書
│   ├── Events/                 # イベントカレンダー
│   ├── Instruments/            # 銘柄ページ（US100/USDJPY/WTI/XAUUSD/VIX/US2Y/US10Y/BTC）
│   ├── Patterns/               # 戦略パターン
│   ├── Hypotheses/             # シナリオ A/B/C
│   ├── Journal/                # 週次日記
│   └── index.md
│
├── nlm_sources/                # NLM 投入用パッケージ
│   └── monthly/
│       └── YYYY-MM_brain_pack.md
│
└── docs/
    ├── STRATEGY_WIKI_GUIDE.md      # Wiki 構造ガイド
    ├── distillation_schema.md      # distilled の YAML/MD スキーマ仕様
    ├── STATUS.md                   # 週次ブリーフ時系列スタック（毎週追記・SSoT）
    ├── Trade-Main.md               # GM Playbook + Weekly Index + 3シナリオ運用指針
    └── WEEKLY_UPDATE_WORKFLOW.md   # 週末 Git 更新手順書（RTK / main.py 実行・チェックリスト）
```

## docs/ 配下ファイルの役割分担

Trade_Brain の `docs/` は **設計資料** と **週次運用資料** の2系統で構成される。

### 設計資料（初期構築時に整備・変更頻度低）

| ファイル | 役割 | 更新頻度 |
|---|---|---|
| `STRATEGY_WIKI_GUIDE.md` | Strategy_Wiki/ の構造・YAML frontmatter・Dataview クエリ仕様 | 構造変更時のみ |
| `distillation_schema.md` | distilled ファイルの YAML/MD スキーマ正式仕様 | スキーマ変更時のみ |

### 週次運用資料（毎週 Git 更新時に追記 / 2026-04-18 Trade_System から移設）

| ファイル | 役割 | 更新頻度 | 位置づけ |
|---|---|---|---|
| `STATUS.md` | **週次ブリーフの時系列スタック**。macro/regime・position・key levels・gates・this week focus・signals を毎週追記。最新が現状、過去は下に積み上がる | 週次（追記型） | 現在進行形の市況の **Single Source of Truth** |
| `Trade-Main.md` | **GM Playbook**。運用原則・3シナリオ即応（A: Risk-on / B: Whipsaw / C: Risk-off）・Weekly Index（年次通し）・Distilled Logs リンク集・Monday AM ラベル運用 | 週次＋マニュアル更新時 | **運用ルールブック** 兼 **週次ナビゲーション** |
| `WEEKLY_UPDATE_WORKFLOW.md` | **週末 Git 更新の実施手順書**。RTK（Rust Token Killer）プレフィックスルール・`python main.py --trade --news` 実行指示・チェックリスト8段階・パス早見 | 手順変更時のみ | **運用オペレーションマニュアル**（ClaudeCode 必読） |

### 3ファイルの関係性

```
週末 Git 更新フロー:

  1. WEEKLY_UPDATE_WORKFLOW.md を読む
        ↓ （手順に従って）
  2. python main.py --trade --news 実行
        ↓ （データ取得）
  3. raw/weekly/YYYY/YYYY-M-D_wkNN/ 配下を生成
        ↓ （週末整理）
  4. STATUS.md 末尾に「Weekly Brief | YYYY-M-D_wkNN」追記
  5. Trade-Main.md の「Weekly Index」に当週エントリ追加
        ↓ （月末のみ）
  6. distilled/YYYY/distilled-gm-YYYY-M.md に蒸留エントリ追記
        ↓
  7. git add → commit → push
```

## 外部リソース参照先

```
対応 NLM:     REX_Trade_Brain（新設）
              ID: 4abc25a0-4550-4667-ad51-754c5d1d1491
Vault ルート: C:\Python\REX_AI\REX_Brain_Vault\wiki\trade_brain\
姉妹リポ:     Minato33440/Trade_System
              （対応 NLM: REX_System_Brain
                 ID: da84715f-9719-40ef-87ec-2453a0dce67e）
```

## ライフサイクル

```
[Daily]
  market data / news / Grok output
    → raw/daily/YYYY/YYYY-M-D.txt
                    ↓
[Weekly wrap-up]
  週次ポートフォリオ総括
    → raw/weekly/YYYY/YYYY-M-D_wkNN/
    → docs/STATUS.md に Weekly Brief 追記
    → docs/Trade-Main.md の Weekly Index に追加
                    ↓
[Monthly distillation]
  Advisor / ClaudeCode が raw を蒸留
    → distilled/YYYY/distilled-gm-YYYY-M.md
                    ↓
[Wiki Ingest]
  distilled から以下を抽出・更新:
    - Regimes/ / Signals/ / Events/ / Instruments/ / Hypotheses/
                    ↓
[NLM Sync]
  月次で nlm_sources/monthly/ にパッケージ化
    → REX_Trade_Brain に source_add
                    ↓
[Query]
  トレード判断時: NLM RAG + Vault Dataview で過去事例検索
```

## 姉妹プロジェクトとの連携ポイント（将来構想）

Trade_System の #030+ で想定されるレジームフィルターの基盤となる:

```
Trade_System/window_scanner がエントリーシグナル発火
                    ↓
REX_Trade_Brain にクエリ: 「現在のレジームは？」
                    ↓
Gold Bid / Neutral → 実行
Equities Down      → 見送り or ロット縮小
```

## データ移行履歴

| 日付 | 内容 |
|---|---|
| 2026-04-18 | Trade_System から `logs/gm/` を移行（`raw/` 配下にフラット化・`gm/` 階層除去） |
| 2026-04-18 | Trade_System から `versions/distilled/` を移行（`distilled/` 配下） |
| 2026-04-18 | NLM 全面再構築: 旧 REX_Trade_Brain を MCP 切り離し、新規 REX_System_Brain + REX_Trade_Brain 作成 |
| 2026-04-18 | Trade_System から週次運用ファイル 3 件を移設: `docs/STATUS.md` / `docs/Trade-Main.md` / `docs/WEEKLY_UPDATE_WORKFLOW.md` |

## 管理

- ディレクター: Minato（ボス）
- 運用: Advisor / ClaudeCode（Ingest・週次更新担当）
- 発行: 2026-04-18（週次運用ファイル統合版は同日夜改訂）
