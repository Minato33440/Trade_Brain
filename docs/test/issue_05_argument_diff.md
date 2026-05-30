# Issue ⑤: merge_weekly_sources.py 引数差分分析

**実行日**: 2026-05-24  
**対象ファイル**: 
- `src/integration/merge_weekly_sources.py`（実装）
- `docs/WEEKLY_UPDATE_WORKFLOW.md`（ドキュメント）
- `scripts/hermes_market_synthesis.ps1`（スクリプト）

---

## 1. 実装定義（merge_weekly_sources.py の argparse）

**行 169-183**: 実装されている引数

| 引数 | タイプ | デフォルト | 説明 |
|-----|--------|----------|------|
| `--boss-text` | str | None | Boss が提供する市況テキスト（直接渡し） |
| `--boss-file` | Path | None | Boss市況テキストのファイルパス |
| `--news-output` | Path | None | python main.py --news の出力ファイル |
| `--x-headlines` | Path | None | hermes -z -t x_search の出力ファイル |
| `--output` | Path | **REQUIRED** | 出力ファイルパス |
| `--dry-run` | bool | False | 出力ファイルを作成せず stdout に出力 |

**実装ロジック**（行 188-200）:
```python
# Boss市況テキスト の取得
boss_text = args.boss_text  # --boss-text で直接渡された値を優先
if args.boss_file:  # なければ --boss-file から読み込み
    boss_file_path = Path(args.boss_file)
    if boss_file_path.exists():
        with open(boss_file_path, 'r', encoding='utf-8') as f:
            boss_text = f.read()
```

**結論**: `--boss-text` と `--boss-file` は両立可能。実装上、どちらか一方で OK。

---

## 2. WEEKLY_UPDATE_WORKFLOW.md での使用

**行 350-354**: ドキュメントの実行例

```powershell
python src/integration/merge_weekly_sources.py `
  --boss-file "logs/boss's-weeken-Report/2026/wr-2026-5-22.md" `
  --news-output "logs/weekly/news_output.txt" `
  --x-headlines $X_HEADLINES `
  --output "logs/weekly/2026/$WeekFolder/charts/Market conditions -2026-5-22~.txt"
```

**使用引数**: `--boss-file`, `--news-output`, `--x-headlines`, `--output` **（4個）**

---

## 3. hermes_market_synthesis.ps1 での使用

**行 52-55**: スクリプトの実行例

```powershell
python src/integration/merge_weekly_sources.py `
    --boss-file $BossFile `
    --x-headlines $XOutputFile `
    --output $OutputPath
```

**使用引数**: `--boss-file`, `--x-headlines`, `--output` **（3個）**

---

## 4. 差分 🔍

### ❌ **差分点**

| ドキュメント | スクリプト | 実装サポート | 状態 |
|-----------|---------|----------|------|
| `--boss-file` | `--boss-file` | ✅ | 統一 |
| `--news-output` | ❌ なし | ✅ | **MISMATCH** |
| `--x-headlines` | `--x-headlines` | ✅ | 統一 |
| `--output` | `--output` | ✅ | 統一 |
| `--dry-run` | ❌ なし | ✅ | ドキュメント未記載 |

### 📍 **主要差分**

1. **`--news-output`**:
   - ✅ WEEKLY_UPDATE_WORKFLOW.md **で指定されている**
   - ❌ hermes_market_synthesis.ps1 **では指定されていない**
   - ✅ merge_weekly_sources.py **では実装されている（行 176-177）**

   **問題**: hermes_market_synthesis.ps1 が `--news-output` を忘れている可能性

2. **`--dry-run`** (新規):
   - ❌ どちらのドキュメント・スクリプトでも記載なし
   - ✅ merge_weekly_sources.py には実装されている（行 182-183）
   
   **問題**: デバッグ機能があるが、ドキュメントに記載されていない

---

## 5. 根本原因の仮説

### 仮説 A: hermes_market_synthesis.ps1 が不完全
- hermes_market_synthesis.ps1 は PowerShell スクリプト版として 先週に書かれた
- --news-output を忘れて実装
- WEEKLY_UPDATE_WORKFLOW.md は正式版として後から完成させた
- **結論**: hermes_market_synthesis.ps1 を修正すべき

### 仮説 B: WEEKLY_UPDATE_WORKFLOW.md が過剰
- merge_weekly_sources.py は本来 3引数（--boss-file, --x-headlines, --output）で十分
- WEEKLY_UPDATE_WORKFLOW.md が --news-output を「あったら使う」くらいの仕様で記載
- **結論**: --news-output は optional だから、どちらでも動作するはずだが、merge 結果が異なる

---

## 6. 実装動作の検証

### `--news-output` を指定した場合（WEEKLY_UPDATE_WORKFLOW.md）

**行 201-202** の `merge_sources()` 呼び出し:
```python
merged = merge_sources(boss_text, args.news_output, args.x_headlines)
```

**行 132-138** で GMニュースセクション生成:
```python
if news_output_path and news_output_path.exists():
    sections.append("\n## 📰 GMニュース（RSS + API）\n")
    try:
        with open(news_output_path, 'r', encoding='utf-8') as f:
            news_content = f.read().strip()
            sections.append(news_content)
```

**結果**: `--news-output` が指定されると、「📰 GMニュース」セクションが出力に含まれる

### `--news-output` を指定しない場合（hermes_market_synthesis.ps1）

**行 201-202** では `args.news_output = None` が渡される  
**行 132** の条件 `if news_output_path and news_output_path.exists():` は False  
**結果**: 「📰 GMニュース」セクションが出力に**含まれない**

---

## 7. 判定と推奨

### ✅ **合意のポイント**

1. **実装は正しい**: merge_weekly_sources.py は 6引数を全て正しく定義・処理している
2. **差分の原因は明確**: 
   - hermes_market_synthesis.ps1 が `--news-output` を忘れている（スクリプト側の漏れ）
   - WEEKLY_UPDATE_WORKFLOW.md は `--news-output` を含めている（ドキュメント側は完全）

### 🔧 **修正案**

#### Option A: hermes_market_synthesis.ps1 を修正（推奨）
- `--news-output "logs/weekly/news_output.txt"` を行 53 に追加
- merge 結果に「📰 GMニュース」セクションを含める

#### Option B: WEEKLY_UPDATE_WORKFLOW.md を修正（非推奨）
- `--news-output` 引数を削除
- 代わり、別途 GMニュース出力を Chart conditions に手動追加

#### 結論
**Option A（hermes_market_synthesis.ps1 修正）が妥当**  
→ news_output ファイルが既に存在するなら、統合に含めるべき

---

## 8. 付加情報

### `--news-output` の入力元

WEEKLY_UPDATE_WORKFLOW.md **行 116 / 300**:
```bash
python main.py --trade --news < /dev/null
```

この出力から:
- `logs/weekly/news_output.txt` に自動保存される（と想定）
- または、ターミナル出力を手動で `logs/weekly/news_output.txt` に保存

→ **次確認項目**: `python main.py --news` がどこに出力するか（stdout / ファイル）

### `--x-headlines` の入力元

WEEKLY_UPDATE_WORKFLOW.md **行 138 / 306**:
```powershell
hermes -z $query -t x_search,vision | Out-File -Encoding UTF8 "logs/weekly/x_headlines_raw.txt"
```

→ `logs/weekly/x_headlines_raw_TIMESTAMP.txt` として明示的に保存

---

## 総括

| 項目 | 判定 |
|------|------|
| merge_weekly_sources.py の実装 | ✅ 完全・正しい |
| WEEKLY_UPDATE_WORKFLOW.md | ✅ 完全（--news-output 含む） |
| hermes_market_synthesis.ps1 | ❌ 不完全（--news-output 抜け落ち） |
| 推奨アクション | **hermes_market_synthesis.ps1 を修正** |

