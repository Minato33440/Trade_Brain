# STRATEGY_WIKI_GUIDE.md
# Strategy_Wiki / Vault（wiki/trade_brain/）運用ガイド
# 発行: 2026-04-18 / Advisor（Opus 4.7）

---

## 0. 位置づけ

Strategy_Wiki は Obsidian Vault `REX_Brain_Vault/wiki/trade_brain/` の
Git 管理ミラー。Source of Truth は Vault 側。

本ガイドは **Trade_System 側の Vault（wiki/trade_system/）とは別ルート** として
Vault 内に共存する。詳細は Trade_System の REX_027_ADVISOR_PROPOSAL.md を参照。

---

## 1. ディレクトリ構造

```
Strategy_Wiki/
├── index.md                    # 全ページのカタログ
├── _RUNBOOK.md                 # 運用手順
│
├── Regimes/                    # レジーム辞書
│   ├── equities_down_oil_surge.md
│   ├── neutral.md
│   ├── gold_bid.md
│   ├── risk_off.md
│   └── risk_on.md
│
├── Signals/                    # シグナル辞書（蒸留の decision から抽出）
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
├── Instruments/                # 銘柄ページ
│   ├── US100.md
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
└── Journal/                    # 週次日記（distilled への逆引き）
    └── 2026/
        ├── 2026-W14.md         # 2026-4-3_wk01
        ├── 2026-W15.md         # 2026-4-10_wk02
        └── 2026-W16.md         # 2026-4-17_wk03
```

---

## 2. YAML フロントマター仕様

### 2-1. Regime ページ

```yaml
---
type: regime
regime_id: gold_bid
status: active | historical
characteristics:
  equities: up
  volatility: normal
  oil: range
  gold: bid
  crypto: strong
  yields: falling
first_observed: 2026-04-17
historical_occurrences: 1
typical_duration: "2-4 weeks"
related_signals: [VIX_add_risk_gate, gold_5060_target]
---
```

### 2-2. Signal ページ

```yaml
---
type: signal
signal_id: VIX_add_risk_gate
category: volatility | geopolitics | rates | equity_structure | fx | commodity
status: active | retired | watch
first_observed: 2026-04-10
latest_trigger: 2026-04-17
activation_condition: "VIX < 20"
deactivation_condition: "VIX > 25"
related_regimes: [neutral, gold_bid]
related_instruments: [US100, VIX]
historical_triggers:
  - date: 2026-04-10
    outcome: "US100 +2.38% following week"
  - date: 2026-04-17
    outcome: "pending"
confidence: medium
---
```

### 2-3. Event ページ

```yaml
---
type: event
event_id: BOJ_4_28_meeting
scheduled_date: 2026-04-28
category: monetary | economic | geopolitical
severity: high | medium | low
expected_outcome: "no rate hike"
related_instruments: [USDJPY]
related_signals: [BOJ_rate_hike_risk, GW_intervention_risk]
status: upcoming | in_progress | concluded
---
```

### 2-4. Instrument ページ

```yaml
---
type: instrument
symbol: US100
category: equity_index
current_regime: gold_bid
key_levels:
  - price: 24045
    role: neckline
    source: "2026-4-3_wk01"
  - price: 25116
    role: blue2_resistance
    source: "2026-4-10_wk02"
  - price: 26672
    role: current_close
    source: "2026-4-17_wk03"
  - price: 27000
    role: next_target
    source: "2026-4-17_wk03"
latest_snapshot_date: 2026-04-17
---
```

### 2-5. Hypothesis ページ

```yaml
---
type: hypothesis
hypothesis_id: 2026-04_scenario_A_escalation
status: pending | validated | invalidated
probability_at_inception: 0.55
inception_date: 2026-04-03
validation_date: ""
triggers:
  - "trump_48h_ultimatum"
  - "JASSM_ER_deployment"
expected_outcome: "WTI 120$ / US100 down"
actual_outcome: "invalidated at 2026-04-10 (ceasefire path taken)"
related_regime: equities_down_oil_surge
---
```

### 2-6. Journal ページ（週次）

```yaml
---
type: journal
week_id: 2026-4-17_wk03
iso_week: 2026-W16
regime: gold_bid
distilled_source: distilled/2026/distilled-gm-2026-4.md
triggered_signals: [hormuz_full_opening, US100_blue2_breakout, regime_gold_bid]
key_events: [ceasefire_4_22_deadline, BOJ_4_28_meeting]
---
```

---

## 3. Dataview クエリ運用例

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

### 例 4: Instrument ごとの重要価格帯

```dataview
TABLE current_regime, key_levels
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

---

## 4. Ingest フロー（月次 distilled → Wiki 更新）

```
契機: 月次 distilled 更新（通常は週末・月末）

手順:
  1. distilled/YYYY/distilled-gm-YYYY-M.md の最新週を parse
  
  2. regime フィールドから:
     - Regimes/{regime_id}.md を確認
     - 未登録なら新設
     - 既存なら historical_occurrences をインクリメント
  
  3. decision フィールドから各 signal_id を抽出:
     - Signals/{category}/{signal_id}.md を確認
     - 新規 signal_id なら新設（カテゴリ判別）
     - 既存なら historical_triggers に追記・latest_trigger 更新
  
  4. tags から event: プレフィックス抽出:
     - Events/{category}/{event_id}.md を確認
     - 新規なら新設、終了イベントは Events/archive/ に移動
  
  5. evidence の各銘柄から:
     - Instruments/{symbol}.md の key_levels と latest_snapshot_date を更新
  
  6. tags から hypothesis: プレフィックス抽出:
     - Hypotheses/{hypothesis_id}.md を確認・status 更新
  
  7. Journal/YYYY/YYYY-Wxx.md を新規作成（該当週の集約）
  
  8. index.md を再生成

想定触れるページ数: 10〜20 ページ/週
```

---

## 5. ClaudeCode 書き込み権限

```
■ ClaudeCode が自動書き込み可能
  - Strategy_Wiki/Journal/*.md
  - Strategy_Wiki/Instruments/*.md（数値更新のみ）
  - Strategy_Wiki/Signals/*.md（status / latest_trigger / historical_triggers 追記）
  - Strategy_Wiki/Events/*.md（status 更新・archive 移動）
  - Strategy_Wiki/index.md

■ ClaudeCode は提案のみ（承認後書き込み）
  - Strategy_Wiki/Regimes/*.md（新規作成時）
  - Strategy_Wiki/Hypotheses/*.md（新規作成・検証確定）
  - Strategy_Wiki/Patterns/*.md（新規作成）
  - Strategy_Wiki/Signals/{新規 category}/{新規 signal_id}.md

■ 書き込み禁止
  - _RUNBOOK.md（運用ルール変更は Advisor/ミナト判断）
  - 過去 Journal エントリーの改変
```

---

## 6. NLM との連携

```
月次: nlm_sources/monthly/YYYY-MM_brain_pack.md を生成
      中身は:
        - 該当月の distilled 全文
        - その月に新設された Signals / Events / Regimes の要約
        - Hypothesis の検証結果
      
      REX_Trade_Brain に source_add

日次/週次: NLM への頻繁な source 投入は避ける（RAG 精度低下）
           Vault 側での Dataview クエリで対応
```

---

## 7. 将来構想: Trade_System との連携

```
Trade_System/#030+ で想定されるレジームフィルター:

  window_scanner.py がエントリーシグナル発火
          ↓
  REX_Trade_Brain に「現在のレジーム？」クエリ
          ↓
  Regime が [gold_bid, neutral, risk_on] → 実行
  Regime が [equities_down_oil_surge, risk_off] → 見送り or ロット縮小

  この連携のために、Strategy_Wiki/Regimes/ の regime_id は
  Trade_System 側から参照される「契約（インターフェース）」となる。
  
  → Regimes/ のページは安易に新設・削除しない（Evaluator 承認必要）
```

---

*発行: 2026-04-18 / Advisor (Claude Opus 4.7)*
*関連: Trade_System/docs/REX_027_ADVISOR_PROPOSAL.md*
