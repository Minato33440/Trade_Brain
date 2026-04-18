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

## リポジトリ構成（2026-04-18 データ移行完了版）

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
    ├── STRATEGY_WIKI_GUIDE.md  # Wiki 構造ガイド
    └── distillation_schema.md  # distilled の YAML/MD スキーマ仕様
```

## 外部リソース参照先

```
対応 NLM:     REX_Trade_Brain（新設）
Vault ルート: C:\Python\REX_AI\REX_Brain_Vault\wiki\trade_brain\
姉妹リポ:     Minato33440/Trade_System
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
                    ↓
[Monthly distillation]
  Advisor が raw を蒸留
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
| 2026-04-18 | Trade_System から raw/ および distilled/ を移行 |
| 2026-04-18 | gm/ 階層を除去してフラット化（raw 配下は daily / weekly / boss's-weeken-Report） |

## 管理

- ディレクター: Minato（ボス）
- 運用: Advisor / ClaudeCode（Ingest 担当）
- 発行: 2026-04-18
