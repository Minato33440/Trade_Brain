# 週末 Git データ更新工程（REX 参照用）

**毎週金曜日終値時点（実質土曜）で市況を更新する定期ルーチンワーク。**

## ルーチン概要

| タイミング | 入力 | コマンド | フォルダ | 例 |
|-----------|------|---------|---------|-----|
| **毎週金曜夜～土曜朝** | Boss 市況（金曜終値時点） | `/gm-weekly YYYY-M-DD_wkNN` | logs/weekly/2026/YYYY-M-D_wkNN/ | `/gm-weekly 2026-5-22_wk04` |

### 週フォルダ命名ルール

- **YYYY-M-DD**: その週の **金曜日の日付** （営業週の最終営業日）
- **wkNN**: その **月の第 N 週目**
  - 5月第3週: `2026-5-15_wk03` （5月15日金曜日）
  - 5月第4週: `2026-5-22_wk04` （5月22日金曜日） ← **現在実行中**
  - 5月第5週: `2026-5-29_wk05` （5月29日金曜日）

### Boss からの市況入力タイミング

金曜日終値後（実質土曜）、以下を提供：
1. **#1 市況テキスト**: `logs/boss's-weeken-Report/2026/wr-YYYY-M-DD.md`
2. **#4 ポートフォリオ口座**: `png_data/portfolio_snapshot_YYYY-MM-DD.*`
3. **#5 当週トレード結果**: あれば `private_trades.csv` に記録、なければ明示

その後、Claude Code が以下を実行：
```
/gm-weekly 2026-5-22_wk04
```

---

週末に「来週向け」の週次フォルダを更新する際の手順を整理。Rex 自身が後から見返して実行できるよう、入力元・出力先・チェック項目を明示する。

> **重要 (2026-04-20 更新)**: 本リポ Trade_Brain の実構造に合わせてパス表記を全並フラット化した：
> - `logs/gm/weekly/` → `logs/weekly/`（`gm/` 階層除去）
> - `logs/gm/daily/` → `logs/daily/`（同上）
> - `versions/distilled/` → `distilled/`（`versions/` 除去）

> **重要 (2026-05-24 更新)**: Hermes CLI 直叩き運用を開始。OAuth フロー の理解：
> - Hermes が保存・管理する OAuth トークン（`C:\Users\Setona\AppData\Local\hermes`）を、Desktop MCP bridge と Claude Code 直叩きが共有再利用
> - つまり「異なる認証」ではなく「同じセッションの異なるインターフェース」
> - SuperGrok の日次制限は共有される
> - 参考: `HERMES_INTEGRATION_GUIDE.md` の「OAuth フロー」セクション

---

## 🦀 RTK（Rust Token Killer）使用ルール（ClaudeCode 必読・全工程共通）

**すべてのターミナルコマンドは `rtk` プレフィックスを必須とする。**

```bash
# ❌ 間違い
git status
git add .
git commit -m "msg"
git push
python main.py --trade --news

# ✅ 正しい
rtk git status
rtk git add logs/weekly/...
rtk git commit -m "msg"
rtk git push origin main
python main.py --trade --news   # ← python は rtk 対象外（パススルー）
```

**Windows環境での注意**:
- Unix系の自動フックは使用不可（Mac/Linux専用）。
- `~/.claude/CLAUDE.md` の指示経由で ClaudeCode が手動で `rtk` を付ける方式が唯一の動作モード。
- `&&` でチェーンする場合も各コマンドに `rtk` を付ける：
  ```bash
  rtk git add . && rtk git commit -m "msg" && rtk git push
  ```
- `python` / `rtk init` / `rtk gain` などの RTK メタコマンド自体は `rtk` 不要。

---

## 📋 実行前の準備チェック（`/gm-weekly` コマンド実行前に確認）

- [ ] **#1 週末市況**: `logs/boss's-weeken-Report/2026/wr-YYYY-M-DD.md` に Boss が保存
  - 形式: Markdown（wr-2026-5-24.md を参考）
  - 内容: Overview / Key Bullish / Key Cautious / Regime / Bottom Line / Watch
  - 例: `wr-2026-5-24.md`

- [ ] **#4 GMポートフォリオ口座**: `png_data/` に配置（以下の形式で Boss から提供）
  - ファイル形式: PNG or YAML（スナップショット）
  - 内容: 資産残高・評価損益・内訳（国内株/米国株/預り金等）
  - パス例: `png_data/portfolio_snapshot_2026-05-24.png` または `.yaml`

- [ ] **#5 当週トレード結果**: 
  - あれば: `private_trades.csv` に記録済み（追加エントリ）
  - なければ: Boss が「保有継続のみ」等を明示

- [ ] **カレントディレクトリ**: `C:\Python\REX_AI\Trade_Brain` 確認
- [ ] **環境**: Python `.venv` 有効、Hermes PATH 設定済み

**すべて確認後、Boss が以下を実行**:
```
/gm-weekly 2026-5-22_wk04
```

**命名ルール確認**:
- `2026-5-22`: 金曜日の日付（営業週の最終営業日）
- `wk04`: 5月の第4週目（5月1-7日=wk01, 8-14日=wk02, 15-21日=wk03, 22-28日=wk04, 29-31日=wk05）

---

## ⚠️ 作業開始前のデータ取得フェーズ（ClaudeCode 必読・2026-05-24〜）

週末Git更新の依頼を受けたら、**ClaudeCode 自身が以下を順序で実行**する。

### Step 1a: 8ペア市場データ + GMニュース取得（既存）

```bash
python main.py --trade --news < /dev/null
```

- コード修正済（configs/rex_chat.py / 2026-05-16）: XAI_API_KEY なしでも `--trade --news` は動作、stdout は UTF-8 固定、データ出力後 exit 0。`< /dev/null` で非対話・クリーン終了。
- 出力（8ペア30日値・regime・GMニュース）を `charts/` 配下に自動配置、`png_data/` の plot/snapshot を週次フォルダへコピー。
- **news はライブ取得**: 週次更新開始時に1回実行し、その出力を確定採用する（最新情報を採る方針 / ボス 2026-05-16）。
- **失敗時（不変ルール7）**: exit≠0 / ペア欠落 / news欠落 等が出たら**自分で想像補完せず停止しボスに報告**。

**理由**: 実測値（各ペア最新値・30日変化率・レジームラベル・GMニュース）なしにファイルを作成すると、推定値で作成後に実データで全再更新する二度手間が発生する。実測データを先に確定させてからファイル作成に入る。

#### スナップショットの構造改善（2026-06-27〜 / boss 3項目）

`png_data/YYYY_MM_DD_snapshot.yaml` と `[regime]` 出力に以下が**機械側で自動付与**される。Evidence/レジーム判定で必ず参照すること（プロンプトでの手当てではなく知識アーキテクチャ側で保持）。

1. **JP225 を実測パネルに追加**（`TRADE_PAIRS` に `^N225`）。従来「snapshot8ペアにJP225含まれない」という注記は**不要**になった（9ペアに拡張）。boss市況の主役（日本株）の金曜終値が機械実測で取れる。`snapshot_30d."JP225"` と `panel.Risk` に出る。
2. **`curve_2s10s` セクション**（金利カーブの**3点立体** 3M/5Y/10Y / 2026-06-27 拡張）: `spread_bp`（5s10s=US10Y−US2Y[^FVX 5y proxy]）/ `change_bp` / `shape` ＋ **`spread_3m10s_bp`（3m10s=US10Y−US3M[^IRX]＝Fed重視の景気後退カーブ・逆イールド主ゲージ）** / `shape_3m10s` / `spread_3m5s_bp` / `belly_premium_bp`（5Yの直線補間からの突出度）/ `structure`（`belly_elevated`=front政策<belly5Y突出<long の瘤 等）/ `recession_3m10s`（`positive`/`near_inversion`<25bp/`inverted`）/ `points_pct`。**`yields` ラベルは2Y/10Y平均符号の丸めで、ベアフラット（短期↑/長期↓）を見落とす**ため、その補正指標。**読み方**: `shape`は各区間のフラット化の質、**逆イールド接近の本格警戒は `recession_3m10s` で判定**（5s10sは順イールド環境で最フラット区間＝逆イールド接近を過大評価しうるため）。`structure=belly_elevated`＝政策ターミナル織り込みの瘤（front=政策3M / belly=5Y突出 / long=growth 10Y）。
3. **`intervention_watch` セクション**（ドル円 介入監視）: `zone`（watch/calm・閾値161.5）/ `upper_alert`（162.2）/ `imf_ammo_remaining` / `last_meeting` / `coord_stage`（**4段梯子** `unconfirmed→meeting_held→rate_check_detected→executed`＝予兆→秒読み→着弾）/ `coord_stage_idx` / `coord_ladder` / `down_target` / `asymmetry` / `history`。**残弾・会談・介入実施は市場価格から自動検知できない**ため、`configs/settings.py` の `INTERVENTION_WATCH`（`coord_stage` 含む）を**手動更新**する運用（会談→rate check→実弾が確認された週に `coord_stage` を上げてからStep 1aを回す）。`rate_check_detected` に上がった瞬間に戦略軸が「162待ち伏せ売り」→「155-156底打ち確認」へ切替。
4. **`relative_strength` セクション**（2026-06-27〜 追加 / JP225 vs US100 を共通通貨で分解）: `jp225_jpy_30d` / `jp225_usd_30d`（=JP225/USDJPY のΔ・通貨効果除去）/ `currency_effect_pt` / `us100_30d` / `jp_vs_us_nominal_pt` / `jp_vs_us_fx_adj_pt`（本物の相対強度）/ `verdict`（`structure_led`=割安リレーティング主導 / `currency_led`=円安主導 / `mixed`）。**為替・日米金利ボラが高い環境では相対は共通通貨で読む**ための分解。日本株の強さが構造か通貨かで米株ヘッジとしての有効性が変わる。

→ これらは review/meta/note/distilled の Evidence・gates・Implication に反映し、人間ビュー（hub/HTML）の「レジーム/ゲート」「監視トリガー」にも織り込む。
※ `curve_2s10s` は3点（3M/5Y/10Y）を併記。`US2Y=^FVX`(5年)・`US3M=^IRX`(13週)。5s10sは順イールド環境で最フラット区間のため逆イールド接近を過大評価しうる→**主ゲージは `recession_3m10s`**（yamlの`note`参照）。

### Step 1b: X (Twitter) 市況ヘッドライン取得（新規・2026-05-24〜）

**目的**: 注目度の高い X ポストから、市況センチメント・重要なマクロイベント・相場を動かす政治経済ニュースを **3件** 抽出・要約。

```powershell
# PowerShell の場合（Windows）
$env:HERMES_HOME = "C:\Users\Setona\AppData\Local\hermes"
$env:Path += ";$env:HERMES_HOME\hermes-agent\venv\Scripts"

# X 検索クエリ: 最新マクロ経済・為替・株価の注目ポスト
$query = "market sentiment macroeconomic data FX JPY gold S&P500 financial news from last 7 days high engagement"

hermes -z $query -t x_search,vision | Out-File -Encoding UTF8 "logs/weekly/x_headlines_raw.txt"

Write-Host "✅ X headlines fetched → logs/weekly/x_headlines_raw.txt"
```

**処理フロー**（後述 Step 2で実施）:
1. `x_headlines_raw.txt` をパース → トップ3ツイート抽出
2. 各ツイートを 2-3 行に日本語要約（Grok vision or Python regex）
3. `Market conditions -YYYY-M-D~.txt` に統合

**失敗時**: 
- X キーボード制限 / OAuth 再認証エラー → HERMES_HOME ログを確認し Boss に報告
- ネットワークタイムアウト → hermes コマンド再実行（`--accept-hooks < /dev/null` で自動 continue）

---

**ボスが提供する1次資料は #1 市況 / #4 GMポートフォリオ口座 / #5 当週トレード結果 の3点のみ**（#2 --trade / #3 --news / #3.5 X headlines は ClaudeCode が自動取得）。

---

## 1. 僕（Minato）からの提供データ

週次更新前に、以下のいずれかで渡す想定。

| 項目 | 内容 | 用途 |
|------|------|------|
| **市況** | 週末時点のマクロ・地政・為替・株・商品の認識 | review.md / note.md の「先週動いた材料」「Evidence」 |
| **GMポートフォリオ口座情報** | 資産残高・評価損益・内訳（国内株/米国株/預り金等）・保有銘柄メモ | meta.yaml の `portfolio_snapshot_YYYYMMDD`、note.md の「GMポートフォリオ口座」 |
| **チャット上のトレード結果** | エントリー/決済の相談内容（symbol, direction, entry/exit, PnL, tag, notes） | private_trades.csv 追記の元。未記録分は track_trades.py add で反映 |

**注意**: トレード結果は随時 `private_trades.csv` に記録しておく。週末時点で未登録分があれば、ここで一括で `track_trades.py add` するか、Rex がチャットログから抽出して追記する。

---

## 2. データ取得コマンド（2026-03-21更新）

### ⚠️ 重要: コマンドの変更

旧コマンド（廃止）: `python configs/rex_chat.py --trade --news`
**新コマンド（確定）: `python main.py --trade --news`**

> 理由: システム構成変更により `configs/rex_chat.py` の直接実行では --trade/--news フラグが発動しなくなった。
> `main.py` が `configs/rex_chat.py` の `main()` を呼び出すエントリポイントとなっており、こちらから実行する。

### 2.1 `--trade` から得るもの

| 抽出物 | 保存場所（元） | 週次フォルダでの利用先 |
|--------|----------------|------------------------|
| **8ペア30日プロット** | `png_data/multi_pairs_plot_8.png` | `charts/Portforio-YYYY-MM-DD.png` にコピー保存 |
| **8ペア変動率テキスト** | ターミナル出力（取得期間・各ペア最新値・30日変化%） | `charts/YYYY-MM-DD 〜 YYYY-MM-DD.txt` として保存（日付は取得期間）|
| **レジームスナップショット** | `png_data/YYYY_MM_DD_snapshot.yaml` | `charts/YYYY_MM_DD_snapshot.yaml` にコピー保存 |

取得期間のファイル名例: `2026-02-19 〜 2026-03-21.txt`（取得期間をそのままファイル名に使う）

### 2.2 `--news` から得るもの

| 抽出物 | 内容 | 週次での利用 |
|--------|------|----------------|
| GMキーワードニュース | RSS から取得した投資・地政系ヘッドライン＋サマリ | `charts/Market conditions -YYYY-M-D~.txt` に市況テキストと合わせて保存 |

> **運用メモ**: `Market conditions -YYYY-M-D~.txt` には Minato の市況テキストも先頭に追記してから `--news` 出力を続けて貼ると一元管理しやすい。

### 2.3 `private_trades.csv` から抽出するもの

| 抽出物 | 内容 | 週次での利用 |
|--------|------|----------------|
| **当週のトレード一覧** | 該当週の opened_at でフィルタした全件 | `track_trades.py summary` で Markdown 生成 → `trade_results.md` と review.md の「Trades of the Week」 |

**charts/ 内の利用ファイル（確定パターン）**

- `multi_pairs_plot_8.png` → `charts/Portforio-YYYY-MM-DD.png`（実行日付でリネーム）
- `YYYY_MM_DD_snapshot.yaml` → `charts/YYYY_MM_DD_snapshot.yaml`（そのままコピー）
- 8ペア30日データ → `charts/YYYY-MM-DD 〜 YYYY-MM-DD.txt`（取得期間を〜でつなぐ）
- GM戦略 → `charts/GM Strategy-YYYY-M-DD.txt`

---

## 3. 先週フォーマットに基づく「Y-M-D_wk--」用ファイル新規作成

対象フォルダ: `logs/weekly/2026/YYYY-M-D_wkNN/`（例: `2026-3-20_wk04`）。

「先週」の同フォルダをテンプレートにし、以下を新規作成 or 更新する。

### 3.1 作成するファイル一覧

| ファイル | 内容の主な参照元 | 備考 |
|----------|------------------|------|
| **meta.yaml** | 先週の meta.yaml 構造、今週の regime/snapshot/portfolio | week, created, updated, snapshot, signals, decision_bias, portfolio_snapshot_YYYYMMDD |
| **review.md** | 僕の市況＋Evidence＋Implication、8ペア/プロット、ポートフォリオ、**Trades of the Week** | 結論・先週材料・Evidence・Implication・GM実務・監視項目。末尾に「Trades of the Week」セクションを追加 |
| **note.md** | 市況・マクロ、Key takeaways、Key gates、ポートフォリオ口座、Portfolio action | Macro/Regime・takeaways・gates・本日追記・Portfolio action・口座サマリ |
| **charts.md** | 先週の charts.md 構造 | 今週のチャート画像・データリンク（charts/ 内の .png, .yaml, .txt）を列挙 |
| **trade_results.md** | `track_trades.py summary --start YYYY-MM-DD --end YYYY-MM-DD` の出力 | 当週のトレード一覧＋概要（件数・勝率・合計PnL）。詳細検証用 |
| **CFD戦略-YYYY-M-D.md**（行動週の月曜日付） | 当週 review/meta/snapshot/boss市況 | 人間ビュー①: Obsidian索引ハブ。frontmatter(week/regime/gate/tags) ＋ 概念wikilink ＋ Mermaid(pie/timeline) ＋ 全リンク表（HTML詳細/distilled/前後週ハブ）。**Rex正本は distilled / 本書は人間用**（2026-05-16〜標準化）|
| **CFD_Strategy-YYYY-M-D.html** | 同上 | 人間ビュー②: 自己完結HTML（Chart.js）。8ペアグラフ・銘柄別アクション・タイムライン・トリガー・ポートフォリオ網羅。ハブMDの「📊詳細版」リンク先 |

### 3.2 charts/ サブフォルダに置くもの

| 種別 | 元ファイル（例） | 週次での名前（例） |
|------|------------------|---------------------|
| 8ペアプロット | `png_data/multi_pairs_plot_8.png` | `Portforio-2026-03-21.png` |
| レジームYAML | `png_data/2026_03_21_snapshot.yaml` | `2026_03_21_snapshot.yaml` |
| 30日データテキスト | `python main.py --trade` のターミナル出力 | `2026-02-19 〜 2026-03-21.txt` |
| 市況・ニューステキスト | Minato市況 + `python main.py --news` の出力 | `Market conditions -2026-3-21~.txt` |
| GM戦略テキスト | review/note/meta/30日データを統合して作成 | `GM Strategy-2026-3-21.txt` |
| その他チャート | 個別スクショ（JP225, US100, WTI 等） | 従来通り `charts/` に配置 |

### 3.3 review.md の「Trades of the Week」セクション

- **数値**: `track_trades.py summary` の「概要」を転記（トレード回数・勝ち/負け・勝率・合計PnL）。
- **代表トレード**: 1〜3件を要約（symbol, direction, pnl_%, tag, notes の要点）。
- **学び**: 今週の反省・改善点・来週の方針を 2〜3 行で記載。

---

## 🚀 クイックスタート（毎週金曜夜～土曜朝）

**Boss が市況 + ポートフォリオを提供したら、Claude Code で以下を実行**：

```
/gm-weekly YYYY-M-DD_wkNN
```

### コマンド形式の説明

- **YYYY-M-DD**: その週の **金曜日の日付** （例: 2026-5-22）
- **wkNN**: その月の **第 N 週目** （例: wk04 = 5月第4週）

### 実行例

```
/gm-weekly 2026-5-22_wk04    ← 現在実行中（5月22日金曜 = 5月第4週）
/gm-weekly 2026-5-29_wk05    ← 来週（5月29日金曜 = 5月第5週）
/gm-weekly 2026-6-5_wk01     ← 再来週（6月5日金曜 = 6月第1週）
```

### 自動実行内容

このコマンドで、以下が自動実行されます：
- ✅ Step 1a: `python main.py --trade --news` （8ペア市場データ + GM ニュース）
- ✅ Step 1b: `hermes -z -t x_search` で X ヘッドライン TOP3 取得
- ✅ Step 2: Boss 市況 + X ヘッドライン + GMニュース を統合
- ✅ Step 3: 当週トレード Markdown 生成（private_trades.csv から）
- ✅ Step 4-7: review.md / note.md / meta.yaml / charts.md 自動生成 + Git 更新（Boss 確認後）

---

## 4. 実行順（チェックリスト）

週末に、以下を上から順に実施する。

### フェーズ A: データ取得（自動化・2026-05-24〜）

- [ ] **1. 統合データ取得スクリプト実行**（ClaudeCode）

  **推奨: PowerShell スクリプト一括実行**
  ```powershell
  powershell -ExecutionPolicy Bypass -File scripts/weekly_data_fetch.ps1
  ```

  **または手動実行** (Step 1a + Step 1b):
  ```bash
  # Step 1a: 8ペア市場データ + GMニュース
  python main.py --trade --news < /dev/null

  # Step 1b: X 市況ヘッドライン（新規）
  $env:HERMES_HOME = "C:\Users\Setona\AppData\Local\hermes"
  & C:\Users\Setona\AppData\Local\hermes\hermes-agent `
    -z "latest market sentiment macroeconomic headlines FX JPY gold from last 7 days" `
    -t x_search,vision --accept-hooks < $null > logs/weekly/x_headlines_raw.txt
  ```

  **失敗時**（exit≠0・データ欠落）:
  - Step 1a: 不変ルール7に従い停止・報告（実測値なしでは進められない）
  - Step 1b: 警告のみ。X取得失敗でもプロセスは続行（マイナーデータ）

- [ ] **1b. ボス提供の1次資料を確認（#1/#4/#5 の3点のみ）**
  - #1 市況サマリ → `logs/boss's-weeken-Report/2026/wr-YYYY-M-DD.md` に保存
    - 形式: Markdown（前週の wr-2026-5-15.md を参考に）
    - 内容: Overview / Key Bullish Points / Key Cautious Points / Regime / Bottom Line / Watch List
  - #4 GMポートフォリオ口座（残高・評価損益・内訳。更新なし時は明示）
  - #5 当週トレード結果（なし＝「保有継続のみ」等を明示。未記録分は private_trades.csv に反映）

- [ ] **2. 手順1の出力をファイル化・配置＋ X ヘッドライン統合**（ClaudeCode）
  - ターミナル出力（8ペア変動率・レジーム）を `charts/YYYY-MM-DD 〜 YYYY-MM-DD.txt` に保存
  - **`png_data/multi_pairs_plot_8.png` を `charts/Portforio-YYYY-MM-DD.png` にコピー**（ClaudeCode が実行）
    ```powershell
    Copy-Item "png_data\multi_pairs_plot_8.png" "logs\weekly\2026\YYYY-M-D_wkNN\charts\Portforio-YYYY-MM-DD.png"
    ```
    - `YYYY-MM-DD` は `python main.py --trade` 実行日（スナップショットの `date.end` と同じ日付）
    - PNG も追跡対象（1次プロット資料として版管理。git add に含める / 2026-05-16〜変更）
  - **`png_data/YYYY_MM_DD_snapshot.yaml` を `charts/` にコピー**（ClaudeCode が実行）
    ```powershell
    Copy-Item "png_data\YYYY_MM_DD_snapshot.yaml" "logs\weekly\2026\YYYY-M-D_wkNN\charts\YYYY_MM_DD_snapshot.yaml"
    ```
  - **統合テキスト作成（新規・2026-05-24〜）**: `charts/Market conditions -YYYY-M-D~.txt`
    - **内容構成**:
      1. **Minato 市況テキスト** (Boss が提供)
      2. **`python main.py --news` の出力** (Step 1a より)
      3. **X ヘッドライン要約（新規）** (Step 1b より)
         - `logs/weekly/x_headlines_raw*.txt` から トップ3ツイート 抽出
         - 各ツイートを 2-3 行で日本語要約
         - engagement 指標（likes/retweets）で注目度判定

    - **実行方法** (`src/integration/merge_weekly_sources.py` を使用):
      ```powershell
      # 最新の x_headlines ファイルを自動検出
      $X_HEADLINES = Get-ChildItem logs/weekly/x_headlines_raw*.txt -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1 -ExpandProperty FullName

      # 統合実行（Boss市況ファイルを指定）
      # 例: 2026-5-22_wk04 の場合
      $WeekFolder = "2026-5-22_wk04"
      
      python src/integration/merge_weekly_sources.py `
        --boss-file "logs/boss's-weeken-Report/2026/wr-2026-5-22.md" `
        --news-output "logs/weekly/news_output.txt" `
        --x-headlines $X_HEADLINES `
        --output "logs/weekly/2026/$WeekFolder/charts/Market conditions -2026-5-22~.txt"
      ```

    - **スクリプト仕様** (`src/integration/merge_weekly_sources.py`):
      - ✅ JSON / Markdown / 混合形式の x_search 出力を自動判定パース
      - ✅ engagement スコア（likes+retweets）で TOP3 ソート
      - ✅ 各ツイート（著者/本文/engagement）を markdown で整形
      - ✅ Boss市況 + --news + X ヘッドライン を markdown フォーマットで統合
      - ✅ 出力ファイルは UTF-8 エンコーディング固定

- [ ] **3. 当週トレードの Markdown 生成**
  - 当週の月曜〜日曜の日付を決める（例: 2026-03-16〜2026-03-21）
  - `python src/track_trades.py summary --start 2026-03-16 --end 2026-03-21` を実行
  - 出力を `trade_results.md` として当週フォルダに保存
  - 同じ出力から「Trades of the Week」用の要約を抜き出し

- [ ] **4. 週次フォルダの確認・作成**
  - `logs/weekly/2026/YYYY-M-D_wkNN/` を新規作成（Minato がフォルダ作成）
  - `charts/` サブフォルダを確認

- [ ] **5. charts/ へのファイル配置確認**（ClaudeCode が手順2と同時に実施）
  - `Portforio-YYYY-MM-DD.png` ← `png_data/multi_pairs_plot_8.png` を Copy-Item でコピー（追跡対象）
  - `YYYY_MM_DD_snapshot.yaml` ← `png_data/YYYY_MM_DD_snapshot.yaml` を Copy-Item でコピー
  - `YYYY-MM-DD 〜 YYYY-MM-DD.txt` ← スナップショット `date.start〜date.end` を参照して命名
  - `Market conditions -YYYY-M-D~.txt` ← Minato 1次テキスト（boss's-weeken-Report/）＋ --news 出力
  - `GM Strategy-YYYY-M-D.txt` ← ClaudeCode が作成（①〜⑨構成）

- [ ] **6. 各 .md / .yaml の作成・更新**（ClaudeCode が担当）
  - meta.yaml: week, date_range, created, updated, snapshot, signals, portfolio_snapshot
  - review.md: 結論・材料・Evidence・Implication・GM実務・監視項目・**Trades of the Week**
  - note.md: Macro・takeaways・gates・本日追記・Portfolio action・口座
  - charts.md: 今週の charts/ 内ファイルを列挙
  - trade_results.md: 手順 3 の Markdown をそのまま保存

- [ ] **7. インデックス・ステータス・distilled の更新**（ClaudeCode が担当）
  - `logs/weekly/2026/_index.md`: 当週エントリを末尾に追加（Regime / 1行 / Key gates / Links）
  - `docs/STATUS.md`: 最新 "Weekly Brief | YYYY-M-D_wkNN" セクションを末尾に追加
  - `docs/Trade-Main.md`: ① "2026 Weekly Index" に当週エントリを追加 ② "Distilled Logs" リンクを更新 ③ 末尾に "Weekly Brief" セクションを追加
  - `distilled/2026/distilled-gm-2026-N.md`: 当週の distilled エントリを追記 or 新規作成
    - **命名ルール（重要）**: N は月番号。**同月内は必ず同じファイルに追記する。新月になった時点で新規ファイルを作成する。**
      - 例: 3月第1〜5週はすべて `distilled-gm-2026-3.md` に追記
      - 例: 4月第1週から `distilled-gm-2026-4.md` を新規作成
    - **週をまたいで新ファイルを作ってはいけない**（月内で -4, -5 のように分割しない）
    - 書式: regime / decision（判断変更点のみ） / evidence (close) / implication / tags

- [ ] **7.5. GM Strategy 品質確認（Git push 前・必須）**

  ### GM Strategy 品質基準
  作成後、以下2点をミナトが確認してからNLM投入候補とする：
  ① ミナト1次テキストとの方向性矛盾がないこと
  ② --trade/--newsの実測値にない情報が追加されていないこと

  > **注記**: 「おそらく」「と思われる」等の不確実性表現はチェック対象外。
  > GMマクロ戦略の性質上、特に地政学リスクが高い局面ではミナトの1次市況自体にこれらの表現が含まれる。
  > 不確実性の排除ではなく、**ソース外情報の混入**を検出することが本チェックの目的。

  **⚠️ 矛盾・エラー検出時の対応（ClaudeCode 必読）**：
  - 上記①②いずれかに該当する場合、`rtk git commit` を保留すること
  - 矛盾箇所を具体的に明示してミナトに確認を取る
  - ミナトの承認・修正指示を受けてから手順8へ進む
  - 承認なしに push しない

- [ ] **7.6. 人間ビュー3レイヤー生成（関所7.5承認後・必須 / 2026-05-16〜）**
  - `CFD戦略-YYYY-M-D.md`（ハブ）: frontmatter(week/regime/add_risk_gate/reduce_risk_gate/tags) ＋ 概念 wikilink ＋ Mermaid(pie/timeline) ＋ リンク表（HTML詳細・[[distilled-gm-YYYY-M]]・review・meta・note・前後週ハブ）＋ 要点3行＋トリガー要点
  - `CFD_Strategy-YYYY-M-D.html`（詳細）: 8ペアグラフ・レジーム/ゲート・シナリオ・銘柄別アクション・タイムライン・トリガー・ポートフォリオ
  - 概念 wikilink canonical 表記（表記揺れ禁止）: `リスクオン/リスクオフ/FOMC/日銀政策金利/日銀利上げ/ブラックマンデー/為替介入/レートチェック/債券パニック/Add risk gate/Reduce risk gate/レジーム/押し目買い/戻り売り/NVDA決算/米中首脳会談/ベッセント来日/GW介入` ＋銘柄 `US100/USDJPY/BTC/Gold/WTI/US10Y/VIX`
  - 概念MOC: `MOC/<concept>.md`（Dataview自動集計型）が既存。既存conceptはwikilinkを打つだけで自動成長。**canonical新概念**が出たら `MOC/<新concept>.md` をDataview型雛形で新規作成し `MOC/_index.md` に追記
  - **distilled が Rex 戦略データ正本。本2点＋MOCは人間用ビュー**（NLM投入対象外）。データは確定値に忠実・創作禁止・関所7.5判断を反映
  - 生成物は週次フォルダ直下に置き、手順8の `git add YYYY-M-D_wkNN/` 一括で追跡（MOC更新時は `git add MOC/` も）

- [ ] **8. Git 更新**
  - 以下を一括ステージ（`charts/` 内の PNG / テキスト / YAML すべて追跡対象。`git add YYYY-M-D_wkNN/` で一括包含）
    ```
    rtk git add logs/weekly/2026/YYYY-M-D_wkNN/ \
                logs/weekly/2026/_index.md \
                docs/STATUS.md \
                docs/Trade-Main.md \
                distilled/2026/ \
                data/private_trades.csv
    ```
  - コミット＆プッシュ
    ```
    rtk git commit -m "weekly: YYYY-M-D_wkNN review + trade_results + charts"
    rtk git push origin main
    ```
  - **charts/ の Git 追跡ルール（2026-03-21〜）**
    - `*.txt` / `*.yaml` / `*.md` → **追跡対象**（上記 `git add` で自動包含）
    - `*.png` → **追跡対象**（1次プロット資料として版管理 / 2026-05-16〜変更）
    - 新ファイルを charts/ に追加した場合も `rtk git add YYYY-M-D_wkNN/` で一括追加できる

---

## 5. パス・コマンド早見

| 用途 | パス or コマンド |
|------|------------------|
| 週次ルート | `Trade_Brain/logs/weekly/2026/` |
| 当週フォルダ例 | `2026-3-20_wk04/` |
| **8ペアデータ取得（確定）** | **`python main.py --trade --news`** |
| プロット（元） | `png_data/multi_pairs_plot_8.png` |
| スナップショット（元） | `png_data/YYYY_MM_DD_snapshot.yaml` |
| トレードCSV | `data/private_trades.csv` |
| トレード追記 | `python src/track_trades.py add --opened-at ... --closed-at ... --symbol ... --direction long/short --size ... --entry ... --exit ... [--tag ...] [--notes ...]` |
| 週次サマリ出力 | `python src/track_trades.py summary --start YYYY-MM-DD --end YYYY-MM-DD` |

---

## 6. 足りない場合の追加メモ

- **週番号（wkNN）**: その週の月曜日を含む ISO 週番号、または「3月第2週」などの通し番号で統一するとよい。先週が `wk03` なら今週は `wk04`。
- **日付範囲**: review/meta の `date_range` は「その週の月曜〜金曜」で揃える（例: `2026-03-16 -> 2026-03-20`）。
- **作成日**: `created` は週末にファイルを作った日、`updated` は最終更新日（月曜の追記などがあれば更新）。
- **30日データテキストのファイル名**: `python main.py --trade` 出力冒頭の「取得期間: YYYY-MM-DD 〜 YYYY-MM-DD」をそのままファイル名に使う。
- **GM Strategyファイル**: 8ペア30日データ・レジーム・Minato市況・news を統合してClaudeCodeが作成。セクション構成: ①8ペアサマリ ②週末市況 ③ファンダ ④テクニカル ⑤シナリオ ⑥押し目戦略 ⑦アクション ⑧参照データ ⑨総合解説(A-G)。

このドキュメントは、Rex / ClaudeCode が週末更新時に参照し、上記チェックリストとパスに従って作業できるようにするためのもの。
