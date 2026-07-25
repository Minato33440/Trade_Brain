---
week: 2026-7-24_wk04
date_range: 2026-07-20 -> 2026-07-24
created: 2026-07-25
tags: [gm_weekly, charts, macro, regime]
---

# Charts | 2026-7-24_wk04

## チャートファイル一覧（charts/）

| ファイル | 内容 |
|---------|------|
| `Portforio-2026-07-25.png` | 10ペア正規化比較プロット（取得期間 2026-06-25〜07-25） |
| `2026_07_25_snapshot.yaml` | レジームスナップショット（Equities Down / Oil Surge・VIX18.58・curve 3点・intervention upper_alert・relative_strength） |
| `2026-06-25 〜 2026-07-25.txt` | main.py --trade --news の実出力＋wk03比較＋**WTIソース乖離の注**＋**真の2s10s検証** |
| `Market conditions -2026-7-24~.txt` | Boss 1次市況（答え合わせ形式）＋ GMニュース ＋ X未取得メモ |
| `Portfolio-Total-2026-07-25.png` | 総合ポートフォリオ（ポートフォリオ .png） |
| `Portfolio-JP-Stocks-2026-07-25.png` | 国内株ポートフォリオ（東証株.png） |
| `Portfolio-US-Stocks-2026-07-25.png` | 米国株ポートフォリオ（米国株.png） |
| `x_headlines_raw_2026-7-24.txt` | Hermes/Grok x_search 試行ログ（**ライブ検索不可＝Evidence非採用**・透明性のため保全） |

## 今週の特徴

- **金曜に骨格が入れ替わった**: 木曜NY後の「原油高→インフレ→FRB利上げ→株全売り」から、**米イラン協議継続＋IEA/OECD戦略備蓄放出観測**でBrent-3.88%・WTI急落 → **ダウ+0.46%・S&P+0.05%がプラス転換、下げたのはNDX・日経・韓国だけ**＝指数間の完全分裂。「WTI100ドル→株全滅」は一旦否定
- **Regime は Equities Down 継続もラベル内部が転換**: oil range→**surge** / gold off→**range** / crypto range→**strong**。VIX 18.58で**Add risk gate 閉鎖継続**（2週連続）
- **金利が今週の共通ドライバー**: US10Y **4.679%**（52週高値4.714の後・18カ月ぶり高水準）／US2Y **4.331%**（52週高値4.366の後）＝**両ゾーンとも日中高値が52週高値**。FOMC利上げ確率 0%近辺→**38%**。US2Y STOCHRSI 100＝ピークアウト警戒
- **AI capex懸念**: Alphabet・Tesla決算（時間外-3%/-4%）の設備投資過大・FCF悪化がNDX下落の主因。Intelは良好で明暗が分岐
- **週末の半導体メガディール**: SKハイニックス→Nvidia等7,500億ドル＋サムスン→Broadcom 2,000億ドル（**計9,500億ドル**）。月曜ギャップアップ要因、日本の来週決算組に追い風
- **USDJPY 52週高値164.00に張り付き介入未実施**: 164突破で165まで真空だが**165到達前の急落が最大の非対称性**。upper_alert=true / coord_stage=meeting_held 据置
- **Gold off→range**: 安値4,024から**終値4,070.80の陽線切り返し**。**4,040が分岐、FOMC(7/29)が決着点**。CFDは 1.5Lot 持越し継続（$3,950ネック→**日足実体上抜け**→**4H上昇3波の起点**）
- ★ **年輪の実測検証**: Boss1次が真の2年債4.331%を与えたことで **真の2s10s +34.8bp > 機械5s10s +25.3bp** が確認され、`docs/system/2026-06-27_belly-elevated_rex-curve-error.md` の「5s10sは順イールド環境で最フラット区間＝逆イールド接近を過大評価しうる」が**本番データで裏付けられた**。主ゲージ 3m10s +87.4bp/positive、belly_premium +16.0→**+19.5bp** と瘤が膨張
- **要注意（ソース乖離）**: WTI は機械 **89.310**（→oil=surge判定）vs Boss金曜引け **85.15**。**regimeラベルの "Oil Surge" 部分はこの乖離に依存**（85.15なら約+18%＝range相当）。両論併記で扱う
- **X headlines**: 2週連続でライブ検索不可 → **未取得・Evidence非採用**（創作補完なし）
- **口座**: **NF日経エンタメ（586A）50口 新規**が唯一の株数変更。総資産 4,874,946円（**+98,100円 / +6.52%**）、牽引は GX半導体 +53,244円・三菱重 +26,400円
</content>
