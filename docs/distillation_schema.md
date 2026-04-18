# distillation_schema.md
# distilled/YYYY/distilled-gm-YYYY-M.md のスキーマ仕様
# 発行: 2026-04-18 / Advisor（Opus 4.7）
# 更新: 2026-04-18（データ移行完了）
# Source: 既存 distilled-gm-2026-4.md の構造を正式仕様化

---

## 0. 目的

distilled ファイルは「蒸留済み戦略アーカイブ」であり、以下を満たす必要がある:

1. **機械可読**: tags / regime ラベルで検索・集計可能
2. **人間可読**: ミナトが朝 1 分で全体把握できる
3. **NLM 最適化**: RAG クエリでピンポイントに引ける構造
4. **時系列連続性**: 前週との差分が明示される

---

## 1. ファイル構造

```
# distilled-gm-YYYY-M
月: YYYY-MM
命名ルール: M月内の全週はこのファイルに追記する。翌月になった時点で distilled-gm-YYYY-(M+1).md を新規作成。

---

## YYYY-M-D_wkNN（YYYY-MM-DD → YYYY-MM-DD）
- regime: {regime_label}（{詳細}）
- decision:
  - {signal_id}={status}（{根拠・数値}）
  - ...
- evidence (close / YYYY-MM-DD snapshot):
  - US100: {値}（{前月比%} / 30d）← {コメント}
  - USDJPY: ...
  - WTI: ...
  - XAUUSD: ...
  - US2Y: ...
  - VIX: ...
  - US10Y: ...
  - BTC/USD: ...
  - Regime (system): {regime_label}
- implication:
  - {運用結論 1}
  - {運用結論 2}
  - ...
- tags: [gm, monthly_distilled, YYYY-MM, YYYY-M-D_wkNN, signal:..., event:..., risk:..., hypothesis:...]

---

## YYYY-M-D_wk(NN+1)（...）
...
```

---

## 2. 必須フィールド仕様

### 2-1. regime

**定義**: その週の市況レジーム判定。

**有効値**（Signals から導出される統合ラベル）:

| regime_label | equities | volatility | oil | gold | crypto | yields |
|---|---|---|---|---|---|---|
| `Equities Down / Oil Surge` | down | high | surge | bid | weak | flight |
| `Neutral` | up | normal | range | off | range | rising |
| `Gold Bid` | up | normal | range | bid | strong | falling |
| `Risk Off` | down | high | range | bid | weak | flight |
| `Risk On` | up | low | range | off | strong | neutral |

**遷移記法**: `← wk(NN-1)「{旧 regime}」から転換` を付記する。

---

### 2-2. decision

**定義**: その週のシグナル状態リスト。

**status 値**:

| status | 意味 |
|---|---|
| `on` | シグナル発火・確定済み |
| `off` | シグナル解除・不成立 |
| `watch` | 監視中・確定待ち |

**命名規則**: signal_id は `snake_case` で、カテゴリを含める。

例:
```
trump_48h_ultimatum=on        （人物_イベント型）
VIX_add_risk_gate_open=on     （指標_条件_状態）
US100_neckline_24045=on       （銘柄_概念_数値）
BOJ_4_28_rate_hike_risk=watch （イベント_日付_内容）
scenario_A_escalation=watch   （シナリオ_識別子_種別）
```

---

### 2-3. evidence

**定義**: その週の終値スナップショット（close / YYYY-MM-DD）。

**必須銘柄**（8 銘柄固定）:

| 銘柄 | 用途 |
|---|---|
| US100 | 米国株指標 |
| USDJPY | 為替 |
| WTI | 原油 |
| XAUUSD | 金 |
| US2Y | 短期金利（FRB 期待） |
| VIX | ボラティリティ |
| US10Y | 長期金利 |
| BTC/USD | 暗号資産 |

**フォーマット**:
```
- {銘柄}: {数値}（{前月比%} / 30d）← {コメント}
```

末尾に必ず `Regime (system): {regime_label}` を付記。

---

### 2-4. implication

**定義**: evidence + decision から導かれる運用結論。

**書き方**: 箇条書き 3〜6 項目。各項目は「動作可能な判断」を含む。

例:
```
- 4/6-7 トランプ 48h 期限通過まで絶対 NO-GO。新規エントリー禁止。
- 期限通過後: 停戦合意確認 + US100 24,045$ 維持 + VIX<20 全条件揃ってから初動。
- エネルギー（WTI 保有継続）/ 防衛 / Gold 継続保有。
```

---

### 2-5. tags

**定義**: NLM と Dataview 両方で検索可能な構造化タグ。

**必須タグ**:
```
gm                       ← 全 distilled 共通
monthly_distilled        ← 全 distilled 共通
YYYY-MM                  ← 該当月
YYYY-M-D_wkNN            ← 該当週識別子
```

**カテゴリ別タグ**:
```
signal:{signal_id}      ← 関連シグナル（decision からの抽出）
event:{event_id}        ← 関連イベント（スケジュール型）
risk:{risk_label}       ← リスク識別子
hypothesis:{hypothesis} ← シナリオ識別子
pattern:{pattern_label} ← 戦略パターン
```

---

## 3. 運用ルール

### 3-1. 当月の追記

```
当月内の週次エントリーは同一ファイル末尾に追記する。
既存エントリーの書き換えは禁止（誤記は注記付き追記で訂正）。
```

### 3-2. 月替わり

```
翌月の第 1 週 wk01 エントリーから distilled-gm-YYYY-(M+1).md を新規作成。
前月ファイルは凍結（以降書き換え不可）。
```

### 3-3. 事後訂正

```
過去の evidence 数値等に誤記を発見した場合:
  1. 既存エントリーは改変しない
  2. ファイル末尾に「## 訂正ログ」セクションを追加
  3. 訂正日付・対象エントリー・訂正内容を明記
  4. 訂正は distilled の単位で行う（raw は追記禁止・訂正不可）
```

### 3-4. NLM への投入タイミング

```
月末: その月の distilled を nlm_sources/monthly/YYYY-MM_brain_pack.md に
      パッケージ化して REX_Trade_Brain に source_add する。
当月途中の更新: NLM 投入は月末までしない（頻繁な source 差し替えは RAG 精度を落とす）。
```

---

## 4. 検証チェックリスト

distilled 更新時に以下を確認:

```
□ regime が有効値（§2-1 のテーブル）のいずれか
□ decision の各行が {signal_id}={status}（{根拠}）形式
□ evidence に 8 銘柄全て + Regime (system) が含まれる
□ implication が 3 項目以上の箇条書き
□ tags に必須 4 タグ（gm / monthly_distilled / YYYY-MM / wkNN）
□ 前週との遷移記法（「← wk(NN-1) から転換」等）
□ スキーマ逸脱なし
```

---

## 5. データ移行履歴（2026-04-18 完了）

```
移行元:  Trade_System/versions/distilled/2025/*.md
        Trade_System/versions/distilled/2026/*.md（distilled-gm-2026-1 〜 4）

移行先:  Trade_Brain/distilled/2025/*.md
        Trade_Brain/distilled/2026/*.md

状態:   ✅ 移行完了（2026-04-18）
        既存スキーマは本仕様の原型であるため内容変更なし
        以降の distilled 更新は本仕様に準拠
```

---

## 6. 関連ファイルの命名規則（参考）

```
raw データ:
  raw/daily/YYYY/YYYY-M-D.txt            （例: raw/daily/2026/2026-4-17.txt）
  raw/weekly/YYYY/YYYY-M-D_wkNN/         （例: raw/weekly/2026/2026-4-17_wk03/）

distilled:
  distilled/YYYY/distilled-gm-YYYY-M.md  （例: distilled/2026/distilled-gm-2026-4.md）

NLM 投入パッケージ:
  nlm_sources/monthly/YYYY-MM_brain_pack.md  （例: nlm_sources/monthly/2026-04_brain_pack.md）
```

詳細な運用ルールは CLAUDE.md を参照。

---

*発行: 2026-04-18 / Advisor (Claude Opus 4.7)*
*更新: 2026-04-18（データ移行完了・関連命名規則追記）*
*次の改訂: スキーマ拡張が必要な場合は本ファイルを更新し、更新日を明記*
