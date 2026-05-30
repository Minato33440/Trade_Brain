# 週末市況データ取得スクリプト (weekly_data_fetch.ps1)
# 用途: Step 1a + Step 1b の自動実行
# 実行: powershell -ExecutionPolicy Bypass -File scripts/weekly_data_fetch.ps1

param(
    [string]$BossText = "",
    [string]$OutputDir = "logs/weekly",
    [switch]$SkipXSearch = $false
)

$ErrorActionPreference = "Stop"
$LogDir = $OutputDir
$Timestamp = Get-Date -Format "yyyy-MM-dd_HHmmss"

Write-Host "🚀 週末市況データ取得開始 ($Timestamp)" -ForegroundColor Green

# === Step 1a: 8ペア市場データ + GMニュース ===
Write-Host "`n📊 Step 1a: python main.py --trade --news 実行中..." -ForegroundColor Cyan

try {
    python main.py --trade --news < $null
    Write-Host "✅ Step 1a 完了" -ForegroundColor Green
}
catch {
    Write-Host "❌ Step 1a 失敗: $_" -ForegroundColor Red
    Write-Host "手動確認後、Boss に報告してください" -ForegroundColor Yellow
    exit 1
}

# === Step 1b: X市況ヘッドライン取得 ===
if (-not $SkipXSearch) {
    Write-Host "`n🐦 Step 1b: hermes x_search 実行中..." -ForegroundColor Cyan

    # 環境変数設定（必須）
    $env:HERMES_HOME = "C:\Users\Setona\AppData\Local\hermes"
    $HermesScriptsDir = "$env:HERMES_HOME\hermes-agent\venv\Scripts"

    # Hermes binary の存在確認
    if (-not (Test-Path $HermesScriptsDir)) {
        Write-Host "❌ Hermes スクリプトディレクトリが見つかりません: $HermesScriptsDir" -ForegroundColor Red
        Write-Host "💡 Hermes インストール状態を確認してください (hermes config)" -ForegroundColor Yellow
        exit 1
    }

    # PATH に Hermes を追加
    $env:Path += ";$HermesScriptsDir"

    # クエリ（市況センチメント重視）
    $Query = "latest market sentiment macroeconomic headlines FX JPY gold S&P500 stocks from last 7 days"
    $OutputFile = Join-Path $LogDir "x_headlines_raw_$Timestamp.txt"

    try {
        Write-Host "  Query: $Query"
        Write-Host "  実行: hermes -z ... -t x_search,vision"
        hermes -z $Query -t x_search,vision | Out-File -Encoding UTF8 $OutputFile
        Write-Host "✅ Step 1b 完了 → $OutputFile" -ForegroundColor Green
        Write-Host "  ファイルサイズ: $((Get-Item $OutputFile).Length) bytes"
    }
    catch {
        Write-Host "⚠️ Step 1b エラー: $_" -ForegroundColor Yellow
        Write-Host "  (これは非致命的。Step 2 で continue)" -ForegroundColor Yellow
        $OutputFile = $null
    }
}
else {
    Write-Host "⏭️ Step 1b スキップ (--SkipXSearch 指定)" -ForegroundColor Yellow
    $OutputFile = $null
}

# === 統計 ===
Write-Host "`n📋 取得サマリー:" -ForegroundColor Cyan
Write-Host "  ✅ 8ペア市場データ: charts/ に自動配置"
Write-Host "  ✅ GMニュース: 出力済"
if ($OutputFile) {
    Write-Host "  ✅ X ヘッドライン: $OutputFile"
} else {
    Write-Host "  ⚠️ X ヘッドライン: スキップ/失敗"
}

Write-Host "`n⏭️ 次のステップ:" -ForegroundColor Cyan
Write-Host "  1. Boss から市況テキスト（#1）・口座情報（#4）・トレード結果（#5）を受け取る"
Write-Host "  2. python src/integration/merge_weekly_sources.py で統合"
Write-Host "  3. 当週フォルダ作成・各 .md/.yaml 生成"
Write-Host "  4. git commit & push"

Write-Host "`n✨ Step 1a/1b 完了" -ForegroundColor Green
