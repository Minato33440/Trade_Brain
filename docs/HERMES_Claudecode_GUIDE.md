# Hermes CLI 統合ガイド（週末工程用）

**作成日**: 2026-05-24  
**対象**: Claude Code / 週末市況更新ワークフロー  
**責任者**: Claude Code（CLAUDE.md ガードレール適用）

---

## 概要

本ドキュメントは、**Desktop アプリ**で既に運用されている Hermes/Grok 統合を、**Claude Code** のターミナルからも利用できるようにした実装ガイドです。

### OAuth フロー（重要）

```
Hermes が保存した OAuth トークン（C:\Users\Setona\AppData\Local\hermes）
             ↓ (共有・再利用)
    ┌────────┴────────┐
    ↓                 ↓
hermes CLI         grok_oauth_bridge.py
(Claude Code       (Claude Desktop
 直叩き)           MCP wrapper)
    ↓                 ↓
SuperGrok API    → (同じトークン) → SuperGrok API
stdout           stdout → Claude
(結果)           (結果)
```

**重要**: Desktop MCP と Claude Code は "別々の API キー" を使用しているのではなく、Hermes が保存・管理する **同じ OAuth トークンを再利用** しています。そのため：
- 日次制限は **共有** される
- Desktop がダウンしても、Hermes CLI は OAuth 資格情報に access 可能
- bridge は subprocess ラッパー（stdout relay）に過ぎない

---

## フローの概略図

【Desktop（Boss）】              【Claude Code（Rex）】
┌─────────────────┐              ┌──────────────────┐
│ MCP Server      │              │ Terminal         │
│ grok_oauth ←──────same───────→ hermes-agent     │
│ (always-on)     │             (on-demand)       │
└─────────────────┘              └──────────────────┘
       ↓                                ↓
  Hermes 78スキル           weekly_data_fetch.ps1
  + Grok chat              ├─ python --trade --news
  + GUI対話                └─ hermes -z -t x_search
                                      ↓
                           merge_weekly_sources.py
                                      ↓
                           Market conditions -YYYY-M-D~.txt
                           (Boss市況 + GMニュース + X TOP3)

---

### 実装の狙い

| 側面 | Desktop MCP Bridge | Claude Code 直叩き |
|-----|-------------------|-------------------|
| **用途** | 定期運用・GUI対話（Hermes 78個スキル） | 週末工程・ターミナル駆動 |
| **実行モード** | MCP サーバー（always-on） | CLI コマンド（on-demand） |
| **-s 柔軟性** | 固定（bridge 側で決定） | 自由（直叩きで指定可） |
| **ガードレール** | bridge.py が enforce（聖域拒否） | CLAUDE.md ルールで担保 |
| **責任** | Boss（Desktop） | Claude Code（本規則） |

**方針**: 両ルートは独立。Desktop がダウンしても週末工程は実行可能。

---

## セットアップ確認

### 前提条件

```powershell
# 1. Hermes バイナリ確認
$env:HERMES_HOME = "C:\Users\Setona\AppData\Local\hermes"
Test-Path "$env:HERMES_HOME\hermes-agent\venv\Scripts\hermes.exe"  # → True なら OK

# 2. PATH に追加
$env:Path += ";$env:HERMES_HOME\hermes-agent\venv\Scripts"

# 3. OAuth セッション確認（X 検索が動作するか）
hermes -z "test" -t x_search

# 4. SuperGrok quota 確認
hermes config  # → x_search の日次制限を確認
```

### 環境変数設定

**PowerShell の場合**:
```powershell
# 毎回設定（セッション内で有効）
$env:HERMES_HOME = "C:\Users\Setona\AppData\Local\hermes"
$env:Path += ";$env:HERMES_HOME\hermes-agent\venv\Scripts"

# または $PROFILE に永続化（推奨）
# PowerShell プロフィールに以下を追加:
# $env:HERMES_HOME = "C:\Users\Setona\AppData\Local\hermes"
# $env:Path += ";$env:HERMES_HOME\hermes-agent\venv\Scripts"
```

**Git Bash の場合**:
```bash
# ~/.bashrc に追加
export HERMES_HOME=C:\Users\Setona\AppData\Local\hermes
export PATH="$HERMES_HOME/hermes-agent/venv/Scripts:$PATH"
```

---

## 週末工程での実行

### 最小限の実行（テスト用）

```powershell
# Step 1a: 8ペア市場データ
python main.py --trade --news

# Step 1b: X ヘッドライン取得
$env:HERMES_HOME = "C:\Users\Setona\AppData\Local\hermes"
$env:Path += ";$env:HERMES_HOME\hermes-agent\venv\Scripts"

hermes -z "market sentiment macroeconomic FX JPY gold from last 7 days" `
  -t x_search,vision | Out-File -Encoding UTF8 logs/weekly/x_headlines_raw.txt
```

### スクリプト経由の実行（推奨）

```powershell
# 一括実行（Step 1a + Step 1b）
powershell -ExecutionPolicy Bypass -File scripts/weekly_data_fetch.ps1

# 出力例:
# ✅ Step 1a 完了
# ✅ Step 1b 完了 → logs/weekly/x_headlines_raw_2026-05-24_150230.txt
```

### 統合ファイル生成

**Boss 市況ファイルから統合**:
```powershell
# Boss の市況ファイル（Markdown形式）
# 保存場所: logs/boss's-weeken-Report/2026/wr-YYYY-M-DD.md
# 例: logs/boss's-weeken-Report/2026/wr-2026-5-24.md

# 最新の x_headlines を自動検出
$X_HEADLINES = Get-ChildItem logs/weekly/x_headlines_raw*.txt -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1 -ExpandProperty FullName

# 統合実行
python src/integration/merge_weekly_sources.py `
  --boss-file "logs/boss's-weeken-Report/2026/wr-2026-5-24.md" `
  --news-output "logs/weekly/news_output.txt" `
  --x-headlines $X_HEADLINES `
  --output "logs/weekly/2026/2026-5-24_wk21/charts/Market conditions -2026-5-24~.txt"
```

**手動テキスト指定の場合**:
```powershell
python src/integration/merge_weekly_sources.py `
  --boss-text "【2026-05-20〜2026-05-24 市況】
  Sentiment: Neutral-to-bullish...
  VIX: 16-18 range..." `
  --x-headlines "logs/weekly/x_headlines_raw.txt" `
  --output "logs/weekly/2026/2026-5-24_wk21/charts/Market conditions -2026-5-24~.txt"
```

---

## トラブルシューティング

### ❌ `hermes: コマンドが見つかりません`

**原因**: PATH に Hermes スクリプトディレクトリが無い、または HERMES_HOME 未設定

**解決**:
```powershell
# 方法1: PATH に追加（推奨）
$env:HERMES_HOME = "C:\Users\Setona\AppData\Local\hermes"
$env:Path += ";$env:HERMES_HOME\hermes-agent\venv\Scripts"
hermes -z "test" -t x_search

# 方法2: 完全パスで実行
& "$env:HERMES_HOME\hermes-agent\venv\Scripts\hermes.exe" -z "test" -t x_search
```

### ❌ `タイムアウト（15秒以上応答なし）`

**原因**: `HERMES_HOME` 未設定 → OAuth 認証情報が見つからない

**解決**:
```powershell
# 必ず明示的に設定してから実行
$env:HERMES_HOME = "C:\Users\Setona\AppData\Local\hermes"
# 再実行
```

### ❌ `x_search: 403 Unauthorized`

**原因**: XAI API キー期限切れ、または OAuth リフレッシュ失敗

**解決**:
```bash
hermes setup  # Hermes 設定画面を開く → x_search 再認証
# または
hermes config edit  # 設定ファイルを直接確認
```

### ⚠️ `X ヘッドライン: 空の結果`

**原因**: 検索クエリが合致せず、ツイート取得 0 件

**対策**:
- クエリ文字列を修正（例: 日本語 → 英語、絞り込み追加）
- 日時範囲を広げる（`from last 7 days` → `from last 14 days`）
- 一時的に X API レート制限中の可能性

---

## セキュリティ・責任ルール

### ✅ 許可事項

- ✅ Trade_Brain/ 配下の読み取り・書き込み
- ✅ `/logs`, `/data`, `/charts` への出力
- ✅ X 検索（OAuth 確立済）
- ✅ Grok API 呼び出し（SuperGrok サブスク有効）

### ❌ 禁止事項

- ❌ `REX_Brain_Vault/` への書き込み（読み取り慎重）
- ❌ `raw/` ディレクトリへの Hermes コマンド直接実行
- ❌ 聖域（Obsidian vault）への自動修正・上書き
- ❌ API キーの log 出力・チャット送信

**違反時責任**: Claude Code が責任を持つ（ガードレール は CLAUDE.md で担保）

---

## 運用チェックリスト

毎週末、以下を確認してから実行:

- [ ] HERMES_HOME が正しく設定されているか（`echo $env:HERMES_HOME`）
- [ ] `python main.py --trade --news` が正常終了するか
- [ ] hermes バイナリが PATH に存在するか
- [ ] SuperGrok quota に余裕があるか（`hermes config`）
- [ ] 出力ファイルが UTF-8 で保存されているか
- [ ] Market conditions ファイルが所定パスに生成されたか

---

## 参考リンク

- **CLAUDE.md**: Hermes 環境ルール・ガードレール定義
  - `~/.claude/CLAUDE.md` → "Hermes CLI 直叩き運用" セクション

- **WEEKLY_UPDATE_WORKFLOW.md**: 週末工程の完全手順
  - `Trade_Brain/docs/WEEKLY_UPDATE_WORKFLOW.md` → "Step 1a / Step 1b"

- **merge_weekly_sources.py**: 統合スクリプト（ソースコード）
  - `Trade_Brain/src/integration/merge_weekly_sources.py`

- **weekly_data_fetch.ps1**: 一括実行スクリプト
  - `Trade_Brain/scripts/weekly_data_fetch.ps1`

---

## Hermes Skill 統合（2026-05-24〜）

本プロセスを Hermes Skill として登録し、Grok チャット内から呼び出す方法：

### セットアップ

```powershell
# Hermes skill をコピー
Copy-Item "scripts/hermes_market_synthesis.ps1" `
  "$env:HERMES_HOME\hermes-agent\skills\market-synthesis\market_synthesis.ps1"

# YAML メタデータ確認
Test-Path "$env:HERMES_HOME\skills\market_synthesis.yaml"  # → True
```

### 実行方法1: Claude Code terminal から直叩き

```powershell
powershell -File scripts/hermes_market_synthesis.ps1 `
  -BossFile "logs/boss's-weeken-Report/2026/wr-2026-5-24.md" `
  -WeekFolder "2026-5-24_wk21"
```

### 実行方法2: Hermes Skill として invoke（推奨）

```bash
hermes -s market_synthesis wr-2026-5-24.md 2026-5-24_wk21
```

または Grok チャット内から：

```
Boss: "週末市況を市況ファイルから取得して統合して"

→ Hermes (skill invoke market_synthesis)
  → Boss 市況読み込み
  → X ヘッドライン取得
  → 統合ファイル生成
  ✅ Market conditions -2026-5-24~.txt
```

### 実行方法3: Hermes MCP bridge 経由（Desktop 環境）

```
Claude Desktop:
  ask_grok(
    "market_synthesis skill で wr-2026-5-24.md と 2026-5-24_wk21 を使って実行"
  )
  
→ grok_oauth_bridge.py が subprocess で invoke
→ stdout → Claude Desktop に結果表示
```

---

## よくある質問

**Q1: Desktop の Hermes MCP が停止した場合、Claude Code の直叩きは動作するか？**  
A: はい。OAuth 認証情報（`C:\Users\Setona\AppData\Local\hermes`）はマシンレベルで保存されているため、Desktop がダウンしても Claude Code は hermes CLI を直接実行できます。

**Q2: SuperGrok の日次制限は共有か？**  
A: はい、共有されます。理由は以下の通り：

**OAuth フロー（正確な説明）**:
- **Hermes CLI**: `hermes -z "query"` 実行時、`C:\Users\Setona\AppData\Local\hermes` に保存済の OAuth トークンを使用 → SuperGrok へ直接アクセス
- **Claude Desktop MCP bridge**: `grok_oauth_bridge.py` が subprocess で `hermes -z` をラップ → **同じ保存済 OAuth トークンを再利用** → stdout 経由で Claude に結果を返す
- **Claude Code 直叩き**: `hermes -z` を terminal から実行 → 同じ保存済 OAuth トークンを再利用

つまり、Desktop MCP と Claude Code 直叩きは "異なる API キー" ではなく、**同じ OAuth トークン（Hermes が管理）を共有している** ため、日次リクエスト制限も共有されます。

**Q3: Hermes スキル（78個）は Claude Code から利用可能か？**  
A: 可能です。`-s polymarket`, `-s news_search` などでプリロードして、Grok チャット内で呼び出せます。

**Q4: Windows 以外（Mac/Linux）での動作は？**  
A: 環境変数パスを OS に合わせれば動作します（例: `/Users/setona/.local/hermes`）。

---

**最終更新**: 2026-05-24  
**作成責任**: Claudian (Claude Code)
