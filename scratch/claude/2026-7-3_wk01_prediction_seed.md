---
type: prediction_seed
week: 2026-7-3_wk01
date_range: 2026-06-29 -> 2026-07-03
created: 2026-07-04
source: logs/boss's-weeken-Report/2026/wr-2026-7-3.md
hat: extraction-only (no index/canon design; Broker=Claude+Boss)
principle: append-only / prediction-at-T / source-faithful / no外部情報補完
status: sealed_before_gm_generation
---

# wk01 prediction-seed（時点Tの読み・結果が出る前に固定）

> 用途: 来週の outcome 照合（誤読/罠検出）の基準点 ＋ 生成後 GM Strategy の関所7.5独立アンカー。
> ソース = Boss市況 `wr-2026-7-3.md` のみ。--trade/--news 実測値・外部情報は含めない（それらとの照合で関所7.5が効く）。
> 抽出範囲 = 金曜終値時点（7/3 米独立記念日・早期クローズ/休場）の読み。

## マクロ地合い（時点Tの環境認識）

- 7/3(金)米独立記念日で米株・債券は早期クローズ/休場、出来高減で**テクニカルが機能しにくい薄商い**地合い。
- 木曜雇用統計 **非農業+5.7万人（大幅未達）・失業率4.2%** → 利上げ観測やや後退。
- ただし**株安の主因は雇用でなく韓国発材料**: ①Anthropic×Samsung が AIチップ領域で提携・競合との報道→半導体AI競合懸念で急落 ②韓国アルゴ取引規制→流動性低下・ボラ拡大警戒（コスピVIX相当が高止まり）。
- 半導体以外は底堅く、**非半導体への資金シフト**の動き。
- regime読み（boss一次・機械regimeは未取得）: 半導体個別要因主導の株安、金利要因ではない。

---

## 資産別 prediction-seed

### US100 / NASDAQ100
- regime読み: 目先下振れ警戒も基本スタンス「深く下がったら買い」。4H はボックス見えて実質**トライアングルレンジ**。
- key_levels:
  - `29,089` = 節目。**割れで下落加速**（下方向トリガー）／同時に**押し目買いの好機**と位置付け（両義）。
- pattern: triangle_range / dip_buy_on_break
- signal: 半導体AI（記憶/チップ系）=戻り売り・様子見、非半導体AIへ資金シフト
- events: 雇用統計+5.7万未達 / Anthropic×Samsung AIチップ提携報道→半導体競合懸念 / 韓国アルゴ取引規制→流動性低下
- watch_trigger: 月曜寄り〜前場で 29,089 割れ→分割押し目買い準備。米休場明けで荒れやすくポジション小さめ・損切り徹底。
- outcome_checkable: true（29,089 割れの有無・その後の反発/加速を来週価格で照合可）
- trap_watch: true（米休場明け薄商い＋節目割れ＝sweep&reclaim が起きやすい）

### JP225 / 日経平均
- regime読み: 底堅く強いトレンド継続・**押し目が浅い**。65,840円赤丸エリアからの反発で 67,179円方向を狙うのが本線。fib0.236 到達済で**もう一段の調整余地も**。
- key_levels:
  - `65,840` = 支持/赤丸/買い下がり水準
  - `67,179` = 戻り目標（上方向）
- pattern: shallow_pullback_strong_trend / fib0236_reached
- signal: 強トレンドで深押し限定想定・下がらなければ月曜そのまま上放れ余地
- events: （日本株個別の主触媒は明示なし・米半導体連動）
- watch_trigger: 65,840 接近→分割買い下がり、67,179 戻りで短期利確。
- outcome_checkable: true（65,840 反発 or 割れ・67,179 到達を照合可）
- trap_watch: false

### USDJPY
- regime読み: 木曜は**3つの円高材料が重なり介入なしで急速に円高続伸**、ただし本流は円安トレンド→基本戦略は**戻り高値売り**。
- key_levels:
  - `162.268` = 上値めど。**上抜けで円安再開/トレンド転換シグナル**（監視）。月曜中の到達は想定薄。
- pattern: return_high_sell / uptrend_pullback
- signal: 戻り売り優位・ポジション小さめ・損切り必須
- events: 3円高材料=①弱い雇用統計 ②ロイター報道（財務省が予告なしサプライズ介入も辞さない姿勢示唆）③高市首相周辺→日銀へ利上げ継続要求報道
- watch_trigger: 戻り高値からの戻り売り。米休場薄商いで**覆面介入（サプライズ円買い）リスク**要警戒。162.268 上抜けは転換監視。
- outcome_checkable: true（162.268 上抜け有無・戻り売り水準を照合可）
- trap_watch: true（米休場薄商い＋覆面介入示唆＝サプライズ円買いで sweep 発生地点）

### EURUSD
- regime読み: 天井圏で一旦調整、**フラッグ（旗型）レンジ継続**。1.140周辺が支持帯、反発で 1.14274 方向を想定。
- key_levels:
  - `1.140` = 支持/押し目買い
  - `1.14274` = 上方向目標
- pattern: flag_range / dip_buy
- signal: 1.140 接近で押し目買い意識
- events: 17時ラガルドECB総裁発言で急変動リスク
- watch_trigger: 1.140 接近での押し目買い。要人発言前後はポジション縮小・様子見。
- outcome_checkable: true（1.140 反発 or 割れ・1.14274 到達を照合可）
- trap_watch: false（ただしラガルド発言は event-driven ボラ源）

### WTI
- regime読み: 底打ちから切り返し。**68.80 超えで 70.16 方向の上昇継続**想定。ただし 6/30 高値からの売り圧が上値に控え、**fib0.236 戻し止まり**の可能性も。
- key_levels:
  - `68.80` = 上抜け確認水準（上方向トリガー）
  - `70.16` = 上値目標
- pattern: bottoming_reversal / fib0236_resistance
- signal: 68.80 上抜け確認後の押し目買い、上値売り圧ゾーンは深追い禁物
- events: 6/30 高値売り圧
- watch_trigger: 68.80 上抜け確認→押し目買い、70.16 接近で利確。
- outcome_checkable: true（68.80 上抜け・70.16 到達 or fib0.236 止まりを照合可）
- trap_watch: false

### Gold / XAUUSD
- regime読み: 高値圏で頭打ち、6/22以降の売り圧残存、目先 **4129 方向への下落フロー**想定。抵抗線上抜けなら 4193 方向の戻りも。**中期の上昇トレンド自体は崩れていない**（マネーサプライ拡大背景）。
- key_levels:
  - `4129` = 下落フロー目標/戻り売り（下方向）
  - `4193` = 抵抗。上抜けで戻り（上方向切替）
- pattern: top_rejection / sell_flow_with_midterm_uptrend
- signal: 4129 接近で戻り売り基本、抵抗上抜け確認で短期押し目買いに切替、中期は押し目買い目線維持
- events: 6/22以降の売り圧
- watch_trigger: 4129 接近で戻り売り／4193 抵抗上抜けで戻り想定。
- outcome_checkable: true（4129 到達・4193 上抜け有無を照合可）
- trap_watch: false
- note: CFD残ポジ管理は wk04 から継続（建値$4,097 残1Lot＋$3,990 追加。今週から日足環境足・4H足でのスウィング運用へ切替、残ポジは4Hダウ崩れ15m実体確定で決済予定）※boss指示書より

### BTC
- regime読み: 目先 **60,300ドル方向への調整入り**想定。本来は支持ライン反発狙いの場面だが、**今回に限り反発ロングを見送り**推奨。
- key_levels:
  - `60,300` = 調整目標（下方向）
- pattern: correction_leg / rebound_long_skipped
- signal: 60,300 接近の自動反発狙いロングは今回見送り・様子見優先
- events: Samsung×Anthropic AIチップ提携報道→将来的な暗号解読リスクへの思惑
- watch_trigger: 60,300 接近でも反発ロード見送り。AIチップ関連の続報ウォッチ。
- outcome_checkable: true（60,300 到達・反発の有無を照合可）
- trap_watch: false

### Yield curve（金利）
- regime読み: 米10年 **4.487%（+0.009）**・2年 **4.137%（+0.006）** 小幅上昇。長短スプレッド **+0.35%** でプラス圏維持＝**逆イールド未達・順イールド維持**。
- key_levels:
  - US10Y `4.487%` / US2Y `4.137%` / 2s10s spread `+0.35%`
- pattern: positive_curve_maintained
- signal: 株安は金利要因でなく半導体個別要因（金利は小幅上昇のみ）
- events: 雇用統計未達で利上げ観測やや後退
- watch_trigger: spread のフラット化/逆イールド接近が出れば景気後退織り込みへ（wk04 の bear_flattening 文脈の継続監視）。
- outcome_checkable: true（来週の 2s10s・3m10s 実測で照合可）
- trap_watch: false

---

## 照合キュー（来週 outcome 検証で見る点）

| instrument | 検証する読み | 判定軸 |
|---|---|---|
| US100 | 29,089 割れ→加速 or 押し目反発 | どちらに転んだか＋trap（割って即reclaim）か |
| JP225 | 65,840 反発→67,179 到達 / 深押し | 浅押し継続 vs 一段調整 |
| USDJPY | 戻り売り成立 / 162.268 上抜け / 覆面介入 | 円安再開 vs サプライズ円買いsweep |
| EURUSD | 1.140 支持→1.14274 | フラッグ上放れ vs 割れ |
| WTI | 68.80 上抜け→70.16 / fib0.236止まり | 上昇継続 vs 上値売り圧勝ち |
| Gold | 4129 下落 / 4193 上抜け | 戻り売り vs 中期押し目転換 |
| BTC | 60,300 調整 / 見送り判断の是非 | 調整入り vs 反発（見送りが正解だったか＝D_lucky枠の逆） |
| Yield | 順イールド維持 / フラット化 | 半導体個別要因の裏付け継続 vs 金利要因化 |

---

*このseedは wk01 GM Strategy 生成の「前」に封印。生成後の GM Strategy が①boss市況と方向一致②実測外情報の混入なし を、本seedとの照合で独立検証する（関所7.5アンカー）。*
