# STRATEGY_WIKI_GUIDE.md
# Strategy_Wiki / Vault（wiki/trade_brain/）運用ガイド
# 発行: 2026-04-18 / 全面改訂: 2026-04-22（Planner 起草）
# 改訂契機:
#   - MCP-Obsidian 横断検索基盤の導入（wiki/trade_system ⇔ wiki/trade_brain）
#   - Rolling Window 設計の採用（Instruments/ に直近4週内蔵）
#   - WEEKLY_UPDATE コマンド運用（--NLM 末尾フラグ式投入）の確立
#   - LLM Wiki 3 操作サイクル（Ingest / Compile / Lint）の骨格化

---

## 0. 位置づけと三層構造

### 0-1. Strategy_Wiki の役割

Strategy_Wiki は Trade_Brain リポジトリが保持する**構造化ナレッジ層**であり、
週次抽出された市況データ・レジーム判定・シグナル点灯履歴を、
Obsidian の関係検索（Dataview・リンク追跡）で即時参照できる形に整理した辞書。

本ガイドは **Trade_System 側の Rex_Trade_Wiki（wiki/trade_system/）とは別ルート**
として Vault 内に共存する。両者は共通タグ規約（§3）によって横断検索される。

### 0-2. REX_AI エコシステムにおける三層構造

```
┌────────────────────────────────────────────────────────────────┐
│              REX_Brain_Vault/ （ローカル Obsidian Vault）      │
│                      ★ハブ層・MCP-Obsidian 接続先★            │
│                                                                │
│  wiki/                                                         │
│  ├── trade_system/   ← Trade_System 側 Wiki（動的ロジック）   │
│  └── trade_brain/    ← 本 Wiki（静的市況データ）              │
│                                                                │
│  ※ MCP-Obsidian から両ルートを横断的に検索可能                │
└───────────────────────┬────────────────────────────────────────┘
                        │ 週次 Git push 時にコピー（ミラー）
                        ↓
┌────────────────────────────────────────────────────────────────┐
│            Trade_Brain/Strategy_Wiki/ （Git 追跡ミラー）        │
│                   最新状態のみ保持                              │
│                   過去状態は git log で復元                    │
│                   ※ snapshots/ ディレクトリは作らない          │
└───────────────────────┬────────────────────────────────────────┘
                        │ --NLM フラグ発動時にパッケージ化
                        ↓
┌────────────────────────────────────────────────────────────────┐
│      Trade_Brain/nlm_sources/monthly/YYYY-MM_brain_pack.md     │
│              NLM REX_Trade_Brain への投入パッケージ            │
└────────────────────────────────────────────────────────────────┘
```

### 0-3. Source of Truth の定義

| 層 | SoT | 更新主体 |
|---|---|---|
| Vault 側 `wiki/trade_brain/` | **ライブ編集の主戦場**（MCP-Obsidian 経由） | ClaudeCode / Advisor / Minato |
| Trade_Brain/Strategy_Wiki/ | Vault のミラー（Git push で同期） | ClaudeCode 自動 |
| nlm_sources/monthly/ | brain_pack の生成物 | ClaudeCode（`--NLM` フラグ発動時） |

Vault 側が常に最新。Strategy_Wiki/ は週次 Git push 時点のスナップショット
ではなく**最新状態の常時ミラー**であり、過去状態が必要な場合は git log で遡る。

---

## 1. ディレクトリ構造

```
Strategy_Wiki/
├── index.md                    # 全ページのカタログ（自動生成）
├── _RUNBOOK.md                 # 運用手順＋クエリガイド（手動・Advisor 管理）
├── log.md                      # Ingest/Compile/Lint/NLM Refresh 履歴（自動追記）
│
├── Regimes/                    # レジーム辞書（固定 5 種・インターフェース契約）
│   ├── equities_down_oil_surge.md
│   ├── neutral.md
│   ├── gold_bid.md
│   ├── risk_off.md
│   └── risk_on.md
│
├── Signals/                    # シグナル辞書（distilled decision から抽出）
│   ├── geopolitics/
│   │   ├── trump_48h_ultimatum.md
│   │   ├── hormuz_full_opening.md
│   │   └── ...
│   ├── volatility/
│   │   ├── VIX_add_risk_gate.md
│   │   └── ...
│   ├── rates/
│   │   ├── BOJ_rate_hike_risk.md
│   │   └── ...
│   ├── equity_structure/
│   │   ├── US100_resistance_blue2.md
│   │   └── ...
│   ├── fx/
│   │   └── GW_intervention_risk.md
│   └── commodity/
│       ├── WTI_hormuz_decline.md
│       └── gold_5060_target.md
│
├── Events/                     # イベントカレンダー（日付付き）
│   ├── monetary/
│   │   └── BOJ_4_28_meeting.md
│   ├── economic/
│   │   └── CPI_4_10.md
│   ├── geopolitical/
│   │   ├── ceasefire_4_22_deadline.md
│   │   └── us_china_summit_may.md
│   └── archive/                # 終了イベント
│
├── Instruments/                # 銘柄ページ★直近4週 Rolling Window 内蔵★
│   ├── US100.md
│   ├── JP225.md
│   ├── USDJPY.md
│   ├── WTI.md
│   ├── XAUUSD.md
│   ├── VIX.md
│   ├── US2Y.md
│   ├── US10Y.md
│   └── BTC_USD.md
│
├── Patterns/                   # 戦略パターン
│   ├── mon_tue_buy_wed_sell.md
│   └── ...
│
├── Hypotheses/                 # シナリオ A/B/C
│   ├── 2026-04_scenario_A_escalation.md
│   ├── 2026-04_scenario_B_ceasefire.md
│   └── 2026-04_scenario_C_full_crisis.md
│
└── Journal/                    # 週次日記（distilled への逆引き索引）
    └── 2026/
        ├── 2026-W14.md         # 2026-4-3_wk01
        ├── 2026-W15.md         # 2026-4-10_wk02
        └── 2026-W16.md         # 2026-4-17_wk03
```

### 1-1. メタファイル仕様（index.md / log.md / _RUNBOOK.md）

#### index.md（ClaudeCode が自動生成）

```markdown
# Strategy_Wiki Index
# 自動生成: YYYY-MM-DD HH:MM
# 編集禁止（手動変更は次回再生成時に上書きされる）

## Regimes（5）
- [[Regimes/gold_bid]] — active（since 2026-04-17・occurrences: 1）
- [[Regimes/neutral]] — historical（last: 2026-04-11）
- ...

## Signals（カテゴリ別）
### geopolitics（N）
- [[Signals/geopolitics/hormuz_full_opening]] — active（latest: 2026-04-17）
- ...

## Events（upcoming / in_progress / concluded）
### upcoming
- [[Events/monetary/BOJ_4_28_meeting]] — 2026-04-28
- ...

## Instruments（9）
- [[Instruments/US100]] — regime: gold_bid / close: 26,672
- ...

## Hypotheses
- [[Hypotheses/2026-04_scenario_B_ceasefire]] — validated
- ...
```

#### log.md（ClaudeCode が追記型で自動記録）

```markdown
# Strategy_Wiki Operation Log
# 追記のみ。過去エントリ改変禁止。

## [2026-04-22] compile | new signal created
- Signals/geopolitics/hormuz_full_opening.md（new）
- triggered by: distilled 2026-4-17_wk03 ingest

## [2026-04-22] ingest | wk03 → 7 pages updated
- Regimes/gold_bid.md（new）
- Signals/geopolitics/hormuz_full_opening.md（new）
- Signals/volatility/VIX_add_risk_gate.md（trigger added）
- Instruments/US100.md（4-week rolling updated）
- Instruments/WTI.md（4-week rolling updated）
- Instruments/XAUUSD.md（4-week rolling updated）
- Journal/2026/2026-W16.md（new）

## [2026-04-22] lint | weekly-check passed
- rolling window: 5週目削除 0 件
- orphan pages: 0
- contradictions: 0

## [2026-05-02] nlm_refresh | 2026-04_brain_pack.md added
- trigger: boss_manual (WEEKLY_UPDATE =2026-4-24 --NLM)
- sources_added: nlm_sources/monthly/2026-04_brain_pack.md
- RAG_test_passed: yes
```

`## [YYYY-MM-DD] {op} | {summary}` の prefix を統一することで、
`grep "^## \[" log.md | tail -20` で直近の操作履歴を即時追跡可能。

#### _RUNBOOK.md（手動・Advisor 管理）

詳細は §6（3 操作サイクル）と §7（NLM-RAG 併用設計）の本文参照。
_RUNBOOK.md 本体は本ガイドの該当章を要約する運用マニュアル。

---

## 2. YAML フロントマター仕様

すべてのページは `type:` フィールドで分類される。type の有効値は以下の 7 種で固定。
Dataview クエリの WHERE 節で typo を避けるため、type enum は厳密遵守する。

```
type enum: [regime, signal, event, instrument, hypothesis, journal, pattern]
```

### 2-1. Regime ページ

```yaml
---
type: regime
regime_id: gold_bid              # 固定 enum（§3-1 参照・変更には Evaluator 承認必要）
status: active                    # enum: active | historical
characteristics:
  equities: up                    # enum: up | down | range
  volatility: normal              # enum: low | normal | high
  oil: range                      # enum: surge | range | declining
  gold: bid                       # enum: bid | off | range
  crypto: strong                  # enum: strong | range | weak
  yields: falling                 # enum: rising | neutral | falling | flight
first_observed: 2026-04-17
last_active: 2026-04-17
historical_occurrences: 1
typical_duration: "2-4 weeks"
related_signals: [VIX_add_risk_gate, gold_5060_target, hormuz_full_opening]
distilled_sources:                # 逆引きリンク（必須）
  - distilled/2026/distilled-gm-2026-4.md#2026-4-17_wk03
---
```

### 2-2. Signal ページ

```yaml
---
type: signal
signal_id: VIX_add_risk_gate
category: volatility              # enum: geopolitics | volatility | rates |
                                  #       equity_structure | fx | commodity
status: active                    # enum: active | retired | watch
first_observed: 2026-04-10
latest_trigger: 2026-04-17
activation_condition: "VIX < 20"
deactivation_condition: "VIX > 25"
related_regimes: [neutral, gold_bid]
related_instruments: [US100, VIX]     # 共通タグ規約（§3-2）で instrument_id 厳密
historical_triggers:
  - date: 2026-04-10
    outcome: "US100 +2.38% following week"
  - date: 2026-04-17
    outcome: "pending"
confidence: medium                # enum: low | medium | high
distilled_sources:
  - distilled/2026/distilled-gm-2026-4.md#2026-4-10_wk02
  - distilled/2026/distilled-gm-2026-4.md#2026-4-17_wk03
---
```

### 2-3. Event ページ

```yaml
---
type: event
event_id: BOJ_4_28_meeting
scheduled_date: 2026-04-28
category: monetary                # enum: monetary | economic | geopolitical | corporate
severity: high                    # enum: high | medium | low
expected_outcome: "no rate hike"
actual_outcome: ""                # 終了後に記入（concluded 遷移時）
related_instruments: [USDJPY]
related_signals: [BOJ_rate_hike_risk, GW_intervention_risk]
status: upcoming                  # enum: upcoming | in_progress | concluded
distilled_sources:
  - distilled/2026/distilled-gm-2026-4.md#2026-4-17_wk03
---
```

### 2-4. Instrument ページ（★ Rolling Window 内蔵 ★）

```yaml
---
type: instrument
symbol: US100                     # 固定 enum（§3-2 参照）
category: equity_index            # enum: equity_index | fx | commodity | rates | vol | crypto
current_regime: gold_bid
latest_close: 26672.430
latest_snapshot_date: 2026-04-18
distilled_sources:                # 直近4週分の逆引きリンク
  - distilled/2026/distilled-gm-2026-4.md#2026-4-17_wk03
  - distilled/2026/distilled-gm-2026-4.md#2026-4-10_wk02
  - distilled/2026/distilled-gm-2026-4.md#2026-4-3_wk01
  - distilled/2026/distilled-gm-2026-3.md#2026-3-27_wk05
---

## 直近4週の終値推移（Rolling Window）

| week | close | 30d% | regime | key_event |
|---|---|---|---|---|
| 2026-W16 | 26,672 | +9.51% | gold_bid | hormuz_full_opening |
| 2026-W15 | 25,116 | +2.38% | neutral | VIX_add_risk_gate_open |
| 2026-W14 | 24,045 | -2.42% | equities_down_oil_surge | trump_48h_ultimatum |
| 2026-W13 | 23,132 | -8.45% | risk_off | vix_31_gate_breach |

## key_levels 推移（直近4週）

| week | role | price | source |
|---|---|---|---|
| 2026-W16 | next_target | 27,000 | wk03 |
| 2026-W16 | current_close | 26,672 | wk03 |
| 2026-W15 | blue2_resistance | 25,116 | wk02 |
| 2026-W14 | weekly_neckline | 24,045 | wk01 |

## テクニカル分析（直近4週の流れ）

3/30 の週足ネックライン 24,045$ 割れから 24,000$ 視野→ホルムズ解放で急反発→
「青丸2」レジスタンス 25,45x 突破→次は 27,000〜27,250pt...

## 過去履歴（archive 参照）

5週目より古いデータは以下を参照:
- logs/weekly/2026/_index.md
- distilled/2026/distilled-gm-2026-*.md
- git log（過去の Wiki 全状態を復元可能）
```

Rolling Window の保守は週次 Ingest および Lint で自動処理される（§6 参照）。

### 2-5. Hypothesis ページ

```yaml
---
type: hypothesis
hypothesis_id: 2026-04_scenario_A_escalation
status: pending                   # enum: pending | validated | invalidated
probability_at_inception: 0.55
inception_date: 2026-04-03
validation_date: ""
triggers:
  - "trump_48h_ultimatum"
  - "JASSM_ER_deployment"
expected_outcome: "WTI 120$ / US100 down"
actual_outcome: "invalidated at 2026-04-10 (ceasefire path taken)"
related_regime: equities_down_oil_surge
distilled_sources:
  - distilled/2026/distilled-gm-2026-4.md#2026-4-3_wk01
---
```

### 2-6. Journal ページ（週次・軽量索引）

```yaml
---
type: journal
week_id: 2026-4-17_wk03
iso_week: 2026-W16
regime: gold_bid
distilled_source: distilled/2026/distilled-gm-2026-4.md#2026-4-17_wk03
triggered_signals: [hormuz_full_opening, US100_blue2_breakout, regime_gold_bid]
new_signals_this_week: [hormuz_full_opening]
key_events: [ceasefire_4_22_deadline, BOJ_4_28_meeting]
evidence_snapshot:
  US100: 26672.430
  USDJPY: 158.584
  WTI: 83.850
  XAUUSD: 4857.600
  US2Y: 3.838
  VIX: 17.480
  US10Y: 4.246
  BTC_USD: 77126.875
---
```

### 2-7. Pattern ページ

```yaml
---
type: pattern
pattern_id: mon_tue_buy_wed_sell
category: weekly_timing
status: active
first_observed: 2026-04-10
confidence: medium
description: "月火で押し目買い→水曜で利確抜けの週内短期パターン"
related_signals: [US100_resistance_blue2]
---
```

---

## 3. 共通タグ規約（Trade_System Wiki との横断検索のため）

MCP-Obsidian が wiki/trade_system/ と wiki/trade_brain/ を横断検索する際、
同一の概念に異なる ID が割り当てられると検索が機能しない。
以下の enum は**両 Wiki で必ず共有**する。

### 3-1. regime_id（固定 5 種・Trade_System とのインターフェース契約）

```
regime_id enum:
  - equities_down_oil_surge   （株安・原油急騰）
  - neutral                   （中立）
  - gold_bid                  （リスクオン + Gold 同時強）
  - risk_off                  （リスクオフ）
  - risk_on                   （リスクオン）
```

**契約条項**:
- 新規 regime_id 追加・既存 regime_id 削除には **Evaluator 承認が必要**
- 本 enum は Trade_System のロット調整ロジックから参照される前提で固定
- distilled の regime フィールドも本 enum に準拠する必要あり（distillation_schema §2-1）
- 変更が必要な場合は ADR F-8 派生原則「共存保持の許容」に従い、
  追加前に Trade_System 側の参照経路を確認する

### 3-2. instrument_id（9 種・両 Wiki 共通）

```
instrument_id enum:
  - US100      （米国株・ナスダック 100）
  - JP225      （日経 225）
  - USDJPY     （ドル円）
  - WTI        （WTI 原油）
  - XAUUSD     （Gold）
  - VIX        （恐怖指数）
  - US2Y       （米 2 年金利）
  - US10Y      （米 10 年金利）
  - BTC_USD    （ビットコイン）
```

Trade_System 側 Patterns/ が `related_instruments: [USDJPY]` を持ち、
本 Wiki 側 Signals/fx/GW_intervention_risk.md も `related_instruments: [USDJPY]`
を持つ。これで MCP-Obsidian 上で「USDJPY 関連の全ナレッジ」を一発取得可能。

### 3-3. signal_id / event_id / hypothesis_id の命名規則

両 Wiki で共有するため、命名パターンを統一:

```
signal_id:      {subject}_{attribute}_{state?}
                例: VIX_add_risk_gate / US100_resistance_blue2 / hormuz_full_opening

event_id:       {subject}_{M_D}_{description?}
                例: BOJ_4_28_meeting / ceasefire_4_22_deadline / CPI_4_10

hypothesis_id:  {YYYY-MM}_{scenario_X}_{keyword}
                例: 2026-04_scenario_A_escalation / 2026-04_scenario_B_ceasefire

pattern_id:     {pattern_description_snake_case}
                例: mon_tue_buy_wed_sell / rolling_range_breakout
```

### 3-4. 共通タグ経由の横断クエリ例

```dataview
LIST
FROM ""
WHERE contains(related_instruments, "USDJPY")
  AND (type = "signal" OR type = "pattern" OR type = "event")
SORT type ASC, file.name ASC
```

これが wiki/trade_system/ と wiki/trade_brain/ の両ルートから
USDJPY 関連ページを一括列挙する横断クエリの基本形。

---

## 4. Rolling Window モデル（直近1ヶ月の環境認識保持）

### 4-1. 設計思想

裁量トレードは「直近1ヶ月の時系列推移の全体像」なしには次週戦略提案の
信ぴょう性が保てない。Wiki を「現時点のスナップショット」ではなく
「直近の流れを時系列で俯瞰できる構造」にする必要がある。

一方、全カテゴリに時系列セクションを持たせると保守負荷が爆発し、
原則α（シンプルな土台の保守）に反する。

**採用方針**: **Instruments/ のみ 4 週 Rolling Window を内蔵**し、
他カテゴリは現行辞書構造 + Journal の Dataview 集計で時系列を表現する。

### 4-2. Rolling Window が適用される対象

| カテゴリ | Rolling Window | 時系列表現方法 |
|---|---|---|
| Instruments/ | ✅ 4 週分の表を内蔵 | 各ページ中段の「直近4週の終値推移」「key_levels 推移」 |
| Regimes/ | ❌ | Journal Dataview で regime 遷移を集計 |
| Signals/ | ❌ | 各ページの `historical_triggers:` に最新数件を保持 |
| Events/ | ❌ | `status: upcoming/in_progress/concluded` で進行追跡 |
| Hypotheses/ | ❌ | `status` 遷移で検証経過を追跡 |
| Journal/ | ❌（各週1ファイル） | 全週次ファイルを Dataview で時系列集計 |

### 4-3. Rolling Window 保守ルール

```
■ 保持期間
  - 最新 4 週分のみ保持
  - 5 週目より古いエントリは週次 Lint で自動削除

■ 削除されたデータの救済経路
  - Journal/2026/2026-Wxx.md に週次単位で永続保存
  - distilled/2026/distilled-gm-2026-M.md に月次蒸留として永続保存
  - logs/weekly/2026/YYYY-M-D_wkNN/ に1次データとして永続保存
  - git log で過去の Wiki 全状態を復元可能

■ 週次 Ingest 時の自動更新
  1. 新週の distilled エントリを parse
  2. 該当する Instruments/*.md の「直近4週の終値推移」表の先頭行に追加
  3. 5 行目（=5 週前）があれば削除
  4. key_levels 推移表も同様に更新
  5. テクニカル分析セクションの冒頭 3 行を書き換え（古い記述は下に送る）
  6. distilled_sources: に新エントリを追加、最古エントリを削除
  7. log.md に更新ページを記録
```

### 4-4. 時系列俯瞰のクエリ例

```dataview
// 直近4週の regime 遷移（Journal から集計）
TABLE regime, triggered_signals
FROM "Strategy_Wiki/Journal"
WHERE iso_week >= "2026-W13"
SORT iso_week DESC
```

```dataview
// 直近4週で新規発火した全シグナル
TABLE new_signals_this_week
FROM "Strategy_Wiki/Journal"
WHERE iso_week >= "2026-W13"
SORT iso_week DESC
```

---

## 5. Dataview クエリ運用例

### 例 1: 今週予定のイベント

```dataview
TABLE scheduled_date, severity, related_instruments
FROM "Strategy_Wiki/Events"
WHERE status = "upcoming"
  AND scheduled_date >= date(today)
  AND scheduled_date <= date(today) + dur(7 days)
SORT scheduled_date ASC
```

### 例 2: 現在アクティブな全シグナル

```dataview
TABLE category, latest_trigger, confidence
FROM "Strategy_Wiki/Signals"
WHERE status = "active"
SORT latest_trigger DESC
```

### 例 3: 特定レジームに紐づくシグナル

```dataview
LIST
FROM "Strategy_Wiki/Signals"
WHERE contains(related_regimes, "gold_bid")
```

### 例 4: Instrument ごとの現状と直近終値

```dataview
TABLE current_regime, latest_close, latest_snapshot_date
FROM "Strategy_Wiki/Instruments"
SORT symbol ASC
```

### 例 5: 検証待ちシナリオ

```dataview
TABLE probability_at_inception, triggers, expected_outcome
FROM "Strategy_Wiki/Hypotheses"
WHERE status = "pending"
```

### 例 6: 特定週の振り返り（Journal からの逆引き）

```dataview
TABLE regime, triggered_signals, key_events
FROM "Strategy_Wiki/Journal"
WHERE iso_week = "2026-W16"
```

### 例 7: 横断検索（MCP-Obsidian・両 Wiki 統合）

```dataview
// USDJPY 関連の Trade_System / Trade_Brain 両 Wiki ページを統合列挙
LIST type + " | " + status
FROM ""
WHERE contains(related_instruments, "USDJPY")
SORT type ASC, file.name ASC
```

```dataview
// Gold Bid レジームに関連する全ナレッジ（両 Wiki 横断）
LIST
FROM ""
WHERE contains(related_regimes, "gold_bid")
   OR contains(current_regime, "gold_bid")
   OR regime = "gold_bid"
```

---

## 6. 3 操作サイクル: Ingest / Compile / Lint（LLM Wiki パターン）

本 Wiki は Karpathy の LLM Wiki パターンに準拠し、
**Ingest（取り込み）/ Compile（構造化）/ Lint（品質チェック）** の
3 操作を運用の骨格とする。

### 6-1. Ingest（取り込み・週次）

```
契機: WEEKLY_UPDATE コマンド発動時、WEEKLY_UPDATE_WORKFLOW.md の
      STEP 6 完了後（distilled 追記済）

手順:
  1. distilled/YYYY/distilled-gm-YYYY-M.md の最新週エントリを parse
  
  2. regime フィールドから:
     - Regimes/{regime_id}.md を確認
     - 既存なら historical_occurrences をインクリメント、last_active を更新
     - 未登録なら §6-2 Compile に移行
  
  3. decision フィールドから各 signal_id を抽出:
     - Signals/{category}/{signal_id}.md を確認
     - 既存なら historical_triggers に追記・latest_trigger 更新
     - 未登録なら §6-2 Compile に移行
  
  4. tags から event: プレフィックス抽出:
     - Events/{category}/{event_id}.md を確認
     - 既存なら status 更新（upcoming → in_progress → concluded）
     - 終了イベントは Events/archive/ に git mv
     - 未登録なら §6-2 Compile に移行
  
  5. evidence の各銘柄から:
     - Instruments/{symbol}.md の Rolling Window（§4-3）を更新
     - latest_close / latest_snapshot_date を更新
     - key_levels 推移表も更新
  
  6. tags から hypothesis: プレフィックス抽出:
     - Hypotheses/{hypothesis_id}.md の status を更新
  
  7. Journal/YYYY/YYYY-Wxx.md を新規作成（該当週の集約・§2-6 形式）
  
  8. index.md を再生成
  
  9. log.md に「## [YYYY-MM-DD] ingest | wkNN → N pages updated」を追記

想定触れるページ数: 10〜20 ページ/週
```

### 6-2. Compile（構造化・新規ページ起案時）

```
契機: Ingest 中に未登録の signal_id / event_id / regime_id / hypothesis_id を検出

手順:
  1. 検出された新規 ID のカテゴリを判別
  
  2. ClaudeCode が「新規ページ起案」を Advisor/Minato に提案:
     - 提案内容: YAML frontmatter のドラフト + 説明セクション
     - 出力先案: Signals/{category}/{signal_id}.md 等
  
  3. 承認後、ClaudeCode が新規ページを作成
     （※ Regimes/ の新設は Evaluator 承認必要・§3-1 契約条項）
  
  4. 関連する既存ページに相互リンクを追加:
     - related_signals / related_instruments / related_regimes を更新
  
  5. log.md に「## [YYYY-MM-DD] compile | new {type} created」を追記
```

### 6-3. Lint（品質チェック・週次＋月次）

```
■ 週次 Lint（Ingest 直後に自動実行）
  1. Rolling Window の 5 週目以降を削除（Instruments/ 全ページ）
  2. 孤立ページ検出:
     - どのページからも参照されていない Signals / Events を警告
  3. リンク切れ検出:
     - distilled_sources: が実在ファイルを指しているか確認
     - related_instruments の instrument_id が §3-2 enum に含まれるか確認
  4. 矛盾検出:
     - 同一 signal_id が異なる category に配置されていないか
     - regime status が複数アクティブになっていないか
  5. log.md に「## [YYYY-MM-DD] lint | weekly-check: N warnings」を追記

■ 月次 Lint（--NLM フラグ発動時の前段チェック）
  1. 週次 Lint の全項目
  2. 当月の Hypothesis 検証状況の確認
     - pending が多すぎないか（3 件超は警告）
     - validated/invalidated の根拠が distilled_sources に記録されているか
  3. 新設 Regimes の Evaluator 承認履歴確認
  4. 月次 brain_pack 生成前提条件の検証:
     □ 当月 distilled が全週追記完了
     □ 当月の Rolling Window 更新済
     □ 孤立ページ・矛盾ゼロ
  5. 合格なら brain_pack 生成へ進む（§7-3）
     不合格なら warning を log.md に記録し、ボスに修正依頼
```

---

## 7. NLM-RAG 併用設計（Wiki ↔ NLM の役割分担）

### 7-1. 時間スケール別の情報階層

```
【現在進行形】（当週）
  docs/STATUS.md 末尾 Weekly Brief
      ↓ Wiki も RAG もまだ不要。STATUS 読めば済む。

【直近1ヶ月の環境認識】★Wiki の守備範囲★
  Strategy_Wiki/Instruments/*.md の 4 週 Rolling Window
  Strategy_Wiki/Journal/2026/2026-Wxx.md の Dataview 集計
  Strategy_Wiki/Signals | Events | Regimes の現状辞書
      ↓ Obsidian で瞬時参照。RAG は呼ばない。

【1ヶ月超〜数ヶ月前の事例参照】★NLM-RAG の守備範囲★
  nlm_sources/monthly/YYYY-MM_brain_pack.md（NLM 投入済み）
      ↓ Wiki に残っていない古い事例や、意味類推が必要な問いはここ。

【1次履歴】（全時間スケールの原典）
  logs/weekly/YYYY/YYYY-M-D_wkNN/（全週次フォルダ）
  distilled/YYYY/distilled-gm-YYYY-M.md（全月次蒸留）
      ↓ Wiki にも RAG にも書かれていない詳細はここを直接読む。
```

### 7-2. 併用ルール

- **ルール 1**: Wiki は「直近1ヶ月の前景」、RAG は「1ヶ月超の背景」
- **ルール 2**: Wiki ページは必ず `distilled_sources:` で逆引きリンクを保持
- **ルール 3**: NLM-RAG は月次 brain_pack（distilled 全文 + Wiki 差分要約）を投入
- **ルール 4**: 戦略提案は最低 2 ソース併用（Wiki + distilled、必要なら RAG）

### 7-3. brain_pack.md の構成（Part 1〜4）

```markdown
# YYYY-MM_brain_pack.md

## Part 1: 該当月の distilled 全文
<distilled/YYYY/distilled-gm-YYYY-M.md の全文>

## Part 2: その月に新設された Wiki ページ
- Strategy_Wiki/Signals/geopolitics/hormuz_full_opening.md（new）
- Strategy_Wiki/Regimes/gold_bid.md（new・first_observed: 2026-04-17）
- Strategy_Wiki/Events/monetary/BOJ_4_28_meeting.md（new）

## Part 3: その月に更新された Wiki ページの差分要約
- Strategy_Wiki/Signals/volatility/VIX_add_risk_gate.md
  - 2026-04-10 追加 trigger（VIX 19.23）
  - 2026-04-17 追加 trigger（VIX 17.48）
- Strategy_Wiki/Instruments/US100.md
  - 4 週 Rolling 更新: 23,132 → 24,045 → 25,116 → 26,672
  - key_levels: 27,000 next_target 追加

## Part 4: その月に検証完了した Hypothesis
- 2026-04_scenario_A_escalation: invalidated（ceasefire path taken at wk02）
- 2026-04_scenario_B_ceasefire: validated（wk02 〜 wk03 で成立）
```

### 7-4. WEEKLY_UPDATE コマンド仕様（NLM 投入運用）

毎週末の Git 更新を開始するトリガー用語。
ClaudeCode は「WEEKLY_UPDATE」を受けたら、docs/WEEKLY_UPDATE_WORKFLOW.md の
チェックリスト 8 段階を順次実行する。

#### コマンド書式

```
# 通常週（NLM 投入なし）
WEEKLY_UPDATE =YYYY-M-DD

# NLM 投入を含める週（ボス判断・末尾に --NLM フラグ）
WEEKLY_UPDATE =YYYY-M-DD --NLM
```

#### コマンド例

```
# 4/24（金）Git 更新・NLM 投入なし
WEEKLY_UPDATE =2026-4-24

# 4/24（金）Git 更新・同時に 4 月分を NLM 投入
WEEKLY_UPDATE =2026-4-24 --NLM
```

#### `=YYYY-M-DD` 引数の意味

- 当週の識別日付（通常は金曜 Git 更新日）を明示
- この日付から暦月（YYYY-M）を自動判定し、**--NLM 発動時の投入対象月**として使用
- 例: `=2026-4-24` → 投入対象は `2026-04`
- 例: `=2026-5-1`  → 投入対象は `2026-05`
  - ボスが前月（4 月分）を wk01 で締めたい場合は `=2026-4-24 --NLM` を wk01 Git 更新時に指定する

#### `--NLM` 末尾フラグ発動時の処理

1. 月次 Lint 実行（§6-3 月次項目）→ 合格確認
2. brain_pack 生成（§7-3 Part 1〜4 構成）を `nlm_sources/monthly/YYYY-MM_brain_pack.md` として出力
3. REX_Trade_Brain（NLM ID: `4abc25a0-4550-4667-ad51-754c5d1d1491`）に `source_add`
4. RAG テストクエリ実行（汚染検出）:
   - 「当月の regime 転換をまとめて」→ 既知の転換が返ってくるか
   - 「当月の Gold 関連シグナル」→ 既知シグナルが返ってくるか
5. log.md に追記:
   ```
   ## [YYYY-MM-DD] nlm_refresh | YYYY-MM_brain_pack.md added
   - trigger: boss_manual (WEEKLY_UPDATE =YYYY-M-DD --NLM)
   - sources_added: nlm_sources/monthly/YYYY-MM_brain_pack.md
   - RAG_test_passed: yes/no
   ```

#### 投入忘れリスクヘッジ（5 週経過アラート）

ClaudeCode は WEEKLY_UPDATE 受領時、以下の条件で**警告文を自動生成**してボスに提示する:

- log.md の直近 `nlm_refresh` から 5 週以上経過している場合

警告は任意。ボス判断優先。「今回は要らない」ならスキップして通常更新。
相場推移で判断して翌月 wk01 以降に投入する運用も自然に許容される。

---

## 8. クエリガイド（Wiki / RAG / distilled の使い分け）

本章は _RUNBOOK.md に要約転記される運用マニュアル。

### 8-1. 第 1 段：標準クエリパターン早見表（頻出・定型）

|  問いの型 | 最初に引くべき | 次に引くべき | 最後に引くべき |
|---|---|---|---|
| 「今の市況は？」 | STATUS.md | Strategy_Wiki/Instruments/ | - |
| 「USDJPY の直近1ヶ月の流れ」 | Strategy_Wiki/Instruments/USDJPY.md | Journal Dataview | - |
| 「Gold Bid レジーム関連のシグナル一覧」 | Strategy_Wiki/Regimes/gold_bid.md | Signals/ Dataview | - |
| 「過去に VIX<18 で add risk した事例」 | Strategy_Wiki/Signals/volatility/VIX_add_risk_gate.md | NLM-RAG | distilled/ 直読 |
| 「ホルムズ関連の類似イベント履歴」 | NLM-RAG | distilled/ 直読 | - |
| 「先月から今月への regime 転換の経緯」 | NLM-RAG | Journal + distilled | - |
| 「数ヶ月前の特定日の判断理由」 | distilled/ 直読 | NLM-RAG | - |

### 8-2. 第 2 段：探索的クエリの判断原則（非定型・補完取得）

表に該当しない問いの場合、以下の 4 軸で引き先を組み合わせる:

#### 判断軸 1：時間スケール

- 当週〜4 週以内   → Wiki 主、必要に応じて distilled 直読で補完
- 1ヶ月〜3ヶ月     → NLM-RAG 主、Wiki で現状整合確認
- 3ヶ月超         → distilled 直読 主、NLM-RAG で意味類推補完

#### 判断軸 2：問いの型

- 「〜の状態は？」（現況確認）     → Wiki 起点
- 「〜の経緯は？」（時系列追跡）   → Journal + distilled
- 「〜に類似する過去は？」（事例） → NLM-RAG 起点
- 「〜の定義・契約は？」（辞書）   → Wiki Regimes/Signals/Events

#### 判断軸 3：確信度不足の処理

一次引きで不足を感じたら二次引きに進む。順序は固定しない:

```
Wiki → NLM-RAG → distilled 直読 → raw logs/weekly/ まで降りる
```

例: 「このレジームは過去類似があるか」と聞かれて
  - Wiki の historical_occurrences を見る（1 次）
  - 1 件だけで物足りない
  - NLM-RAG で意味類推（2 次）
  - さらに根拠欲しい
  - distilled/ を grep で遡る（3 次）

#### 判断軸 4：複数ソース統合の原則

戦略提案では**単一ソース依存を避ける**。信頼度の高い提案には:
- Wiki（現状の構造化理解）
- distilled（1 次事実としての裏取り）
- 必要なら NLM-RAG（過去類似事例の存在確認）

の**最低 2 ソース**を併用する。

### 8-3. Escape hatch（運用の柔軟性確保）

上記判断軸でも迷う場合:

- ボスに直接問う（判断軸不足を明示して）
- log.md に「## [YYYY-MM-DD] query | 判断保留 → 方針相談」と記録

不明なクエリパターンを抱え込まない。

---

## 9. ClaudeCode 書き込み権限

```
■ ClaudeCode が自動書き込み可能
  - Strategy_Wiki/Journal/*.md
  - Strategy_Wiki/Instruments/*.md（数値更新・Rolling Window 保守）
  - Strategy_Wiki/Signals/*.md（status / latest_trigger / historical_triggers 追記）
  - Strategy_Wiki/Events/*.md（status 更新・archive 移動）
  - Strategy_Wiki/index.md（自動生成）
  - Strategy_Wiki/log.md（追記のみ）

■ ClaudeCode は提案のみ（承認後書き込み）
  - Strategy_Wiki/Regimes/*.md（新規作成時・§3-1 契約条項で Evaluator 承認必要）
  - Strategy_Wiki/Hypotheses/*.md（新規作成・検証確定）
  - Strategy_Wiki/Patterns/*.md（新規作成）
  - Strategy_Wiki/Signals/{新規 category}/{新規 signal_id}.md

■ 書き込み禁止
  - _RUNBOOK.md（運用ルール変更は Advisor/ボス判断）
  - 過去 Journal エントリーの改変
  - log.md の過去エントリ改変
  - §3 共通タグ規約の enum 変更（Evaluator 承認必要）
```

---

## 10. 将来構想: Trade_System との連携

```
Trade_System/#030+ で想定されるレジームフィルター:

  window_scanner.py がエントリーシグナル発火
          ↓
  REX_Trade_Brain（NLM）または Vault wiki/trade_brain/ に
  「現在のレジーム？」クエリ
          ↓
  Regime が [gold_bid, neutral, risk_on] → 実行
  Regime が [equities_down_oil_surge, risk_off] → 見送り or ロット縮小

  この連携のために、Strategy_Wiki/Regimes/ の regime_id は
  Trade_System 側から参照される「契約（インターフェース）」となる（§3-1）。
```

合流点の物理基盤は `src/plotter.py` の両リポ共存保持（ADR F-8 派生原則）。
Trade_Brain 側の 8 ペア 30 日変動率データ → 市況レジーム判定 → Trade_System 側
優位性スコア → エントリーロット調整、という将来パイプラインが既に物理ファイル
レベルで用意されている。

導入タイミングは原則γ（安定性従属）。Trade_System 実装ロジックが安定してから。

---

*初版発行: 2026-04-18 / Advisor (Claude Opus 4.7)*
*全面改訂: 2026-04-22 / Planner（本リポ Trade_Brain 担当）*
*関連: Trade_Brain/docs/distillation_schema.md /*
*      Trade_Brain/docs/WEEKLY_UPDATE_WORKFLOW.md /*
*      Trade_System/docs/Trade_System_Wiki_Architecture.md /*
*      Trade_System/docs/ADR.md (F-8 派生原則)*
