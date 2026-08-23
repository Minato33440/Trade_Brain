---
title: ツール出力残骸タグの除去（監査マニフェスト）
date: 2026-08-23
type: maintenance_manifest
tags: [maintenance, artifact_cleanup, audit]
---

# `</content>` 残骸タグの除去 — 監査マニフェスト（2026-08-23）

## 経緯

2026-8-21_wk03 の週次更新中、`distilled/2026/distilled-gm-2026-8.md` の末尾に `</content>` が
残っていることに気づき、リポジトリ全体を走査したところ **38ファイル**で同じ混入が見つかった。
いずれも ClaudeCode がファイルを生成した際に、**ツール出力の閉じタグが本文に紛れ込んだもの**。

うち `distilled-gm-2026-8.md` は、**wk03 の追記時に除去が不可避**だった（残すとファイル中央に紛れるため）
ので週次コミットに含まれ、**本マニフェストの対象は残り 37ファイル**。

## 判断の根拠（Boss / 2026-08-23）

> `</content>` はツール出力の残骸で、内容ではない。
> **遡及編集禁止の対象は「当時の判断を後の知識で上書きすること」であって、アーティファクトの除去はそれに当たらない。**

## 事前検査（条件3: 全 occurrence の目視）

| 検査項目 | 結果 |
|---|---|
| 総 occurrence | **37ファイル / 37 occurrence（各1件）** |
| 本文中で `</content>` を正当に言及しているファイル | ★**0件**（除外対象なし） |
| 末尾（EOF）にあるもの | **36件** |
| 末尾以外 | **1件** — `2026-6-26_wk04/charts/2026-05-28 〜 2026-06-27.txt`（直後に `</invoke>` が続くため EOF ではない） |
| 他の残骸タグ（`<content>` / `<invoke` / `</antml` / `</parameter>` 等） | ★**`</invoke>` が上記1件のみ。他は皆無** |
| **2026-8-21_wk03 フォルダ内の混入** | ★**なし**（→ 週次コミットを先行させて問題ない） |

## 除去方法

- **末尾の残骸トークンのみ**を除去（`</content>` および併発する `</invoke>`）
- 本文・改行コード（CRLF）は変更しない
- 各ファイルの diff は **削除のみ**（追加行ゼロ）であることを事後検証

## 対象ファイル一覧（37件）

| # | ファイル | `</content>` | `</invoke>` | 位置 |
|---:|---|---:|---:|---|
| 1 | `docs/system/2026-06-27_belly-elevated_rex-curve-error.md` | 1 | — | EOF |
| 2 | `docs/system/_index.md` | 1 | — | EOF |
| 3 | `logs/weekly/2026/2026-6-26_wk04/CFD_Strategy-2026-6-29.html` | 1 | — | EOF |
| 4 | `logs/weekly/2026/2026-6-26_wk04/CFD戦略-2026-6-29.md` | 1 | — | EOF |
| 5 | `logs/weekly/2026/2026-6-26_wk04/charts.md` | 1 | — | EOF |
| 6 | `logs/weekly/2026/2026-6-26_wk04/charts/2026-05-28 〜 2026-06-27.txt` | 1 | 1 | EOF |
| 7 | `logs/weekly/2026/2026-6-26_wk04/charts/Market conditions -2026-6-26~.txt` | 1 | — | EOF |
| 8 | `logs/weekly/2026/2026-6-26_wk04/meta.yaml` | 1 | — | EOF |
| 9 | `logs/weekly/2026/2026-6-26_wk04/note.md` | 1 | — | EOF |
| 10 | `logs/weekly/2026/2026-6-26_wk04/review.md` | 1 | — | EOF |
| 11 | `logs/weekly/2026/2026-6-26_wk04/trade_results.md` | 1 | — | EOF |
| 12 | `logs/weekly/2026/2026-7-24_wk04/CFD_Strategy-2026-7-27.html` | 1 | — | EOF |
| 13 | `logs/weekly/2026/2026-7-24_wk04/CFD戦略-2026-7-27.md` | 1 | — | EOF |
| 14 | `logs/weekly/2026/2026-7-24_wk04/charts.md` | 1 | — | EOF |
| 15 | `logs/weekly/2026/2026-7-24_wk04/charts/2026-06-25 〜 2026-07-25.txt` | 1 | — | EOF |
| 16 | `logs/weekly/2026/2026-7-24_wk04/charts/Market conditions -2026-7-24~.txt` | 1 | — | EOF |
| 17 | `logs/weekly/2026/2026-7-24_wk04/meta.yaml` | 1 | — | EOF |
| 18 | `logs/weekly/2026/2026-7-24_wk04/note.md` | 1 | — | EOF |
| 19 | `logs/weekly/2026/2026-7-24_wk04/review.md` | 1 | — | EOF |
| 20 | `logs/weekly/2026/2026-7-24_wk04/trade_results.md` | 1 | — | EOF |
| 21 | `logs/weekly/2026/2026-7-31_wk05/CFD_Strategy-2026-8-3.html` | 1 | — | EOF |
| 22 | `logs/weekly/2026/2026-7-31_wk05/CFD戦略-2026-8-3.md` | 1 | — | EOF |
| 23 | `logs/weekly/2026/2026-7-31_wk05/charts.md` | 1 | — | EOF |
| 24 | `logs/weekly/2026/2026-7-31_wk05/charts/2026-07-03 〜 2026-08-02.txt` | 1 | — | EOF |
| 25 | `logs/weekly/2026/2026-7-31_wk05/charts/Market conditions -2026-7-31~.txt` | 1 | — | EOF |
| 26 | `logs/weekly/2026/2026-7-31_wk05/meta.yaml` | 1 | — | EOF |
| 27 | `logs/weekly/2026/2026-7-31_wk05/note.md` | 1 | — | EOF |
| 28 | `logs/weekly/2026/2026-7-31_wk05/review.md` | 1 | — | EOF |
| 29 | `logs/weekly/2026/2026-7-31_wk05/trade_results.md` | 1 | — | EOF |
| 30 | `logs/weekly/2026/2026-8-7_wk01/CFD戦略-2026-8-10.md` | 1 | — | EOF |
| 31 | `logs/weekly/2026/2026-8-7_wk01/charts.md` | 1 | — | EOF |
| 32 | `logs/weekly/2026/2026-8-7_wk01/charts/2026-07-09 〜 2026-08-08.txt` | 1 | — | EOF |
| 33 | `logs/weekly/2026/2026-8-7_wk01/charts/Market conditions -2026-8-7~.txt` | 1 | — | EOF |
| 34 | `logs/weekly/2026/2026-8-7_wk01/meta.yaml` | 1 | — | EOF |
| 35 | `logs/weekly/2026/2026-8-7_wk01/note.md` | 1 | — | EOF |
| 36 | `logs/weekly/2026/2026-8-7_wk01/review.md` | 1 | — | EOF |
| 37 | `logs/weekly/2026/2026-8-7_wk01/trade_results.md` | 1 | — | EOF |

## 内訳（週別）

| 区分 | ファイル数 |
|---|---:|
| 2026-6-26_wk04 | 9 |
| 2026-7-24_wk04 | 9 |
| 2026-7-31_wk05 | 9 |
| 2026-8-7_wk01 | 8 |
| docs/system/ | 2 |
| **合計** | **37** |

## 事後検証

| 検証項目 | 結果 |
|---|---|
| 除去実行 | **37ファイル** |
| 再走査での残存（`</content>` / `</invoke>`） | ★**0件** |
| `git diff --numstat` が「削除のみ」（追加行ゼロ） | ★**37/37ファイルすべて** |
| 改行コード（CRLF/LF）の変化 | **なし**（`write_bytes` で書き戻し、本文・改行は不変） |

★ **除去は末尾の残骸トークンのみ**を対象とし、本文には一切触れていない。

### 参考: 同じ走査で見つかった別件（本コミットの対象外・週次コミットで是正済み）

`docs/STATUS.md` / `docs/Trade-Main.md` / `logs/weekly/2026/_index.md` は元が **LF** だが、
週次更新スクリプトの `pathlib.write_text` が Windows で **CRLF に変換**し、**全行が差分として出る**状態になっていた。
→ **`write_bytes` で LF に復元**し、3ファイルとも**純粋な追記差分**（+52/-0, +49/-0, +15/-0）に戻した。
★**追記型ファイル（STATUS.md は「過去Briefを改変しない」規約）で全行が書き換わると、規約が守られているかを diff で確認できなくなる。**

#### ★ 過去週の監査（Boss指示・2026-08-23）— 「どの週から検証可能か」の境界

`git log --numstat` で3ファイルの全履歴を確認した。**結論: 過去の週次コミットに全行書き換えは無い。**

| ファイル | 週次コミットの差分パターン | 全行書き換え |
|---|---|---|
| `docs/STATUS.md` | **全19コミットが `+N / -0` または `+N / -1`** | ★**なし** |
| `docs/Trade-Main.md` | 同上（`+N / -0` または `+N / -1`） | **1件のみ** → `d179a6e`（2026-04-20 `+31/-31`） |
| `logs/weekly/2026/_index.md` | 同上 | ★**なし** |

- `-1` は追記時に末尾行へ触れたことによるもので、**本文の書き換えではない**
- 唯一の全行差分 `d179a6e` は **`Docs: path consistency fix (logs/gm/ → logs/)` という意図的な一括置換**であり、
  アーティファクトでも改行コード事故でもない

**★ 検証可能な境界: `d63409f`（2026-04-25 / 2026-4-24_wk04）以降のすべての週次コミットで、
「過去の Weekly Brief を改変していない」ことが diff から機械的に検証できる。**
（それ以前は `f0d8aa9`（2026-04-19）の初期投入で、比較対象がない）

**なぜ今回だけ起きたか**: 従来の週次更新は **Edit ツール**（部分置換）で追記していたため改行コードが保たれていた。
本セッションでは **Python の `pathlib.write_text` で全文書き戻し**を行い、Windows 上で `
 → 
` に変換された。
→ **今後、追記型ファイルの更新では Edit ツールを使うか、`write_bytes` で改行コードを明示的に保持する。**

*作成: 2026-08-23 — ClaudeCode / 承認: Minato（条件4つ付きで掃除に賛成）*
