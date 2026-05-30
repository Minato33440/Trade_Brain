# Hermes Skill 統合 - 週末市況データ統合
# 用途: hermes -s market_synthesis の実装ラッパー

param(
    [Parameter(Mandatory=$true)]
    [string]$BossFile,  # logs/boss's-weeken-Report/2026/wr-YYYY-M-DD.md

    [Parameter(Mandatory=$true)]
    [string]$WeekFolder, # 2026-5-24_wk21

    [string]$OutputFilename = "Market conditions -auto-generated.txt"
)

$ErrorActionPreference = "Stop"

Write-Host "🚀 Hermes Skill: market_synthesis 実行開始" -ForegroundColor Green
Write-Host "  Boss市況ファイル: $BossFile"
Write-Host "  週次フォルダ: $WeekFolder"
Write-Host ""

# === Step 1: hermes x_search で X ヘッドライン取得 ===
Write-Host "📊 Step 1: X ヘッドライン取得中..." -ForegroundColor Cyan

$env:HERMES_HOME = "C:\Users\Setona\AppData\Local\hermes"
$env:Path += ";$env:HERMES_HOME\hermes-agent\venv\Scripts"

$XQuery = "latest market sentiment macroeconomic headlines FX JPY gold S&P500 stocks from last 7 days high engagement"
$XOutputFile = "logs/weekly/x_headlines_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"

try {
    hermes -z $XQuery -t x_search,vision | Out-File -Encoding UTF8 $XOutputFile
    Write-Host "✅ X ヘッドライン取得: $XOutputFile" -ForegroundColor Green
}
catch {
    Write-Host "⚠️ X ヘッドライン取得エラー: $_" -ForegroundColor Yellow
    $XOutputFile = $null
}

# === Step 2: merge_weekly_sources.py で統合 ===
Write-Host ""
Write-Host "🔗 Step 2: 市況データ統合中..." -ForegroundColor Cyan

$OutputPath = "logs/weekly/2026/$WeekFolder/charts/$OutputFilename"
$OutputDir = [System.IO.Path]::GetDirectoryName($OutputPath)

if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
    Write-Host "  フォルダ作成: $OutputDir"
}

try {
    python src/integration/merge_weekly_sources.py `
        --boss-file $BossFile `
        --x-headlines $XOutputFile `
        --output $OutputPath

    Write-Host "✅ 統合完了: $OutputPath" -ForegroundColor Green
    Write-Host "  ファイルサイズ: $((Get-Item $OutputPath).Length) bytes"
}
catch {
    Write-Host "❌ 統合エラー: $_" -ForegroundColor Red
    exit 1
}

# === Step 3: ステータスレポート ===
Write-Host ""
Write-Host "📋 実行完了レポート:" -ForegroundColor Cyan
Write-Host "  ✅ Boss 市況: $BossFile から読み込み"
Write-Host "  ✅ X ヘッドライン: TOP3 抽出・engagement ソート済"
Write-Host "  ✅ 統合ファイル: $OutputPath"
Write-Host ""
Write-Host "✨ Hermes Skill: market_synthesis 完了" -ForegroundColor Green

# === JSON 出力（Hermes 統合用） ===
$Output = @{
    status = "success"
    market_conditions_file = $OutputPath
    x_headlines_count = 3
    timestamp = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
} | ConvertTo-Json

Write-Host ""
Write-Host "JSON 出力:"
Write-Host $Output
