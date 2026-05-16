# Step 2.5: fetch_universe.py 修正指示書 ── 上場日突合の追加

| 項目 | 内容 |
|---|---|
| 作成日 | 2026-05-12 |
| 作成 | Wiki-trade Rex（システム側） |
| 実装担当 | ClaudeCode |
| 前提 | `step2_universe_filter_spec.md` の続き |
| 関連ファイル | `fetch_universe.py`, `jquants_client.py`, `data/jpx_new_listings.csv`（本日配置済） |

---

## 1. 背景：J-Quants の限界判明

前回の Step 2 実装テストで以下が判明：

1. **J-Quants `/equities/master` には上場日フィールドが存在しない**
   - これは Free / Light / Standard / Premium 共通の API 仕様
   - V1 の `/listed/info` でも同様（公式リファレンス確認済）
   - レスポンスフィールド: `Date / Code / CompanyName / CompanyNameEnglish / Sector17Code / Sector17CodeName / Sector33Code / Sector33CodeName / ScaleCategory / MarketCode / MarketCodeName / MarginCode / MarginCodeName`

2. **`fins/summary` も日次クォータあり** → yfinance フォールバック（既実装）でカバー

3. **`/equities/bars/daily` でレート制限到達** → キャッシュ機能（既実装）でカバー

つまり、条件①「上場10年以内」を判定するための上場日データを **J-Quants 以外** のソースから取得する必要がある。

---

## 2. データソース：JPX 公式 新規上場会社情報

### 配置済みファイル

```
stock_screener/data/jpx_new_listings.csv  ← 本日 Wiki-trade Rex が配置
```

### CSV 仕様

- **エンコーディング**: UTF-8（BOMなし）
- **改行**: LF
- **カラム**: `listing_date, code, company_name, market`
  - `listing_date`: YYYY-MM-DD 形式
  - `code`: 銘柄コード（4桁数字 または 英字付き4桁、例: `5535`, `480A`）
  - `company_name`: 会社名（日本語、`（株）` プレフィックス含む）
  - `market`: 上場時点の市場区分
- **件数**: 384件
- **期間**: 2022-01-04 〜 2026-06-01（5年分）
- **出典**: JPX 公式「新規上場会社情報」（2022-2026 のバックナンバー統合）

### データ範囲の制約

- **JPX公式アーカイブは過去5年分のみ公開**（archives-01〜04 + current）
- 2021年以前に上場した銘柄は本 CSV に含まれない
- 条件①「上場10年以内」（2016年以降）の完全充足は不可能 → **「過去5年以内に上場」として運用**
- これはテンバガー候補としては実質的にむしろ厳しめの条件で、許容範囲

### 旧市場区分マッピング（重要）

2022年4月の東証市場区分再編より前のIPOには旧区分が記載されている：

| CSV内の `market` 値 | 解釈 | グロース市場としてカウントするか |
|---|---|---|
| `グロース` | 東証グロース | ✓ |
| `マザーズ` | 旧マザーズ（実質グロース前身） | **✓ カウントする** |
| `スタンダード` | 東証スタンダード | ✗ |
| `JQスタンダード` | 旧JASDAQスタンダード | ✗ |
| `プライム` | 東証プライム | ✗ |
| `第一部` | 旧東証第一部 | ✗ |
| `第二部` | 旧東証第二部 | ✗ |

実装では：

```python
GROWTH_MARKETS_HISTORICAL = {'グロース', 'マザーズ'}
```

として、両方をグロース相当として扱う。

---

## 3. fetch_universe.py の修正内容

### 3.1 修正方針

現状の `fetch_universe.py` で「条件①スキップ」となっていた箇所を、JPX CSV を読み込んで突合する形に書き換える。

### 3.2 処理フロー（修正後）

```
1. J-Quants /equities/master 取得（既実装、キャッシュ済）
2. JPX CSV 読み込み ← NEW
3. J-Quants 銘柄リスト × JPX CSV を 銘柄コード で突合 ← NEW
4. 突合できた銘柄 = 上場日が判明 → 条件①判定 ← NEW
5. 突合できなかった銘柄 = 上場日不明 → 「過去5年より前に上場」とみなし条件①脱落 ← NEW
6. グロース市場フィルタ（市場区分が現在グロースまたは過去マザーズ）
7. /equities/bars/daily で終値取得（既実装）
8. 時価総額算出（既実装、yfinanceフォールバックも既実装）
9. 条件③：時価総額300億円未満でフィルタ
10. CSV出力（既実装）
```

### 3.3 銘柄コード突合の注意点

- J-Quants の銘柄コードは5桁の場合がある（例: `86970` = 日本取引所グループ）
  - 末尾の `0` を除去すると4桁になる（`8697`）
  - JPX CSV は4桁（`8697` または `XXXA` 英字付き）
  - 突合時は J-Quants コードから末尾0を除去するか、4桁に正規化する処理が必要
- 英字付きコード（`480A` など）は正規化不要、そのまま使う

突合関数の実装例：

```python
def normalize_code(jquants_code: str) -> str:
    """J-Quantsの5桁コードを4桁に正規化"""
    s = str(jquants_code).strip()
    if len(s) == 5 and s.endswith('0'):
        return s[:4]
    return s
```

### 3.4 出力CSV のカラム追加

`universe_growth_<YYYYMMDD>.csv` に以下を追加：

| カラム | 内容 | ソース |
|---|---|---|
| `listing_date` | 上場日（YYYY-MM-DD） | JPX CSV |
| `listing_source` | 上場日のデータソース | `"jpx_csv"` or `"unknown"` |

### 3.5 ログ出力の追加

```
[INFO] JPX CSV 読込: 384 件
[INFO] J-Quants × JPX 突合: XX 件突合成功 / XX 件突合失敗（上場日不明）
[INFO] 条件①通過（過去5年以内上場）: XX 銘柄
[INFO] グロース市場（現グロース+旧マザーズ）: XX 銘柄
[INFO] 条件③通過（時価総額300億未満）: XX 銘柄  ← 最終ユニバース
```

---

## 4. 想定される動作

### 期待される最終ユニバース

- 全上場銘柄: 約4,400
- JPX CSV 突合成功（過去5年以内上場）: 約384 銘柄前後
- グロース市場（マザーズ含む）に限定: 約260-280 銘柄前後
- 時価総額300億円未満: **数十〜200銘柄程度に絞られる見込み**

数字が想定を大きく外れる場合は、運用側Rex（私）に報告すること。

### 既存実装との整合

- `jquants_client.py` のキャッシュ機能、yfinanceフォールバックは **そのまま活用**
- 修正は `fetch_universe.py` 内のフィルタロジック中心

---

## 5. ClaudeCode への確認・判断事項

実装着手前に以下を確認すること：

1. **J-Quants 銘柄コードの形式**
   - 実際にキャッシュされた `master_YYYYMMDD.json` を見て、コードが5桁か4桁か、英字付きか確認
   - 必要に応じて normalize 関数を調整

2. **JPX CSV の読み込み**
   - `pd.read_csv('data/jpx_new_listings.csv', dtype={'code': str})` で code 列を文字列として扱う
   - 数字始まりでも英字始まりでも全部 str で

3. **市場区分の現状確認**
   - J-Quants `/equities/master` の `MarketCodeName` フィールドで実際にどんな値が返るか確認
   - `グロース` という文字列マッチでよいか、コード（例: `0113`）でマッチすべきか

4. **突合失敗時の扱い**
   - 「上場日不明 = 過去5年より前に上場」と推定して条件①脱落で扱う（推奨）
   - 別案として「上場日不明はログに残してスキップ」もあり

### 仕様で迷ったら

実装着手前に運用側Rex またはボスに上げること。前回のように動かしてからクォータを消費するルートは避ける。今回は明日のクォータ復活で1回しか試行できない前提で設計する。

---

## 6. 終了条件

- `fetch_universe.py` が JPX CSV を読み込み、上場日突合付きで完走する
- ログに各フィルタ段階の通過銘柄数が出る
- 出力 CSV に `listing_date`, `listing_source` カラムが追加されている
- 最終ユニバース数が数十〜200銘柄程度に収まる（大きく外れたら報告）

---

## 7. 次のステップ（Step 3 への引き継ぎ）

Step 3 では各銘柄について EDINET 経由で：
- ④ 経営陣大株主比率
- ⑥ 営業CF（複数期）
- ⑧ 従業員平均年齢

を取得する。`jquants_client.py` 同様の `edinet_client.py` を作る前提で、Step 3 指示書は別途作成予定。

それまでに ClaudeCode が `fetch_universe.py` を完成させ、グロース市場の絞り込みユニバースが取れている状態を目指す。

---

*Wiki-trade Rex / 2026-05-12*
