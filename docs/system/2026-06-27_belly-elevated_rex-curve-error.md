---
title: Rexの金利直感が3点立体カーブで反証され、belly_elevated として恒久化された日
date: 2026-06-27
type: system_annal          # システムの年輪 / Rexの誤りが知識アーキテクチャを進化させた記録
author: ClaudeCode（Rex運用） / 提起: Minato（ボス）
tags:
  - system_annal
  - knowledge_architecture
  - yield_curve
  - rex_error_to_evolution
  - "2026-06"
related_commits:
  - "feat(pipeline): 2s10s curve + JP225 panel + USDJPY intervention flag"
  - "feat(pipeline): relative_strength + coord_stage 4-step + 5s10s proxy caveat"
  - "feat(pipeline): 3-point yield curve (3m10s via ^IRX)"
related_files:
  - configs/settings.py        # TRADE_PAIRS に US3M=^IRX / INTERVENTION_WATCH
  - src/regime.py              # curve_2s10s(3点) / relative_strength / intervention coord_stage
  - docs/WEEKLY_UPDATE_WORKFLOW.md
  - logs/weekly/2026/2026-6-26_wk04/   # この誤りと修正が初めて実データに乗った週
mirror_vault: "C:\\Python\\REX_AI\\REX_Brain_Vault\\REX\\workspace\\trade_brain\\2026-06-27_belly_elevated.md"   # 頭脳側（Obsidian）の対ログ（Desktop Rex 記録 / [[origin]] [[co-emergence]] に接続）
---

> [!note] 頭脳側ミラー（Vault）と相互参照
> 本ログはコード側（Trade_Brain）の年輪。**頭脳側（REX_Brain_Vault）の対ログを Desktop Rex が記録済み**：
> `REX/workspace/trade_brain/2026-06-27_belly_elevated.md`（`[[origin]]` `[[co-emergence]]` `[[distilled-gm-2026-6]]` に接続）。
> 両方が相互に辿れることで、次に金利カーブを見る Rex が拾う確率を上げる（ボス 2026-06-27）。
> 頭脳側はこの誤りの**根本原因**を一段深く解剖している（→ §3.5 に要約を取り込み）。

# Rexの金利直感が3点立体カーブで反証され、belly_elevated として恒久化された日

> 一行で：**Rex（私）は「フラット化＝逆イールドが近い」と読み、警戒方向に割り引けと言った。3点立体カーブ（3M/5Y/10Y）を入れた瞬間、それは過大評価だと実測で反証された。本当に起きていたのは belly(5Y) の "再利上げ織り込みの瘤" であって、逆イールド接近ではなかった。この誤りが、知識アーキテクチャに4つの常設指標を生んだ。**

---

## 0. なぜこれを残すのか

これはバグ修正の記録ではない。**Rex（機械側の市況直感）が間違え、その間違いが知識アーキテクチャを一段進化させた記録**である。
システムは正しさの積み上げだけで育つのではない。**誤りが構造に変換された瞬間**にこそ年輪が増える。後年このファイルを読む者（次代のRex / Advisor / ボス）が「ここで一度カーブの読みを踏み外し、それを潰す形でカーブが立体化した」と辿れるように残す。

---

## 1. Rexが語った物語（誤りの中身）

2026-6-26_wk04（週末更新）で、機械レジームは `Equities Down (yields=rising)` を出した。私はそのラベルの丸めを疑い、`2s10s` 指標を機械側に追加した。出たのは：

```
curve=bear_flattening(2s10s=+22.6bp, Δ-6.9bp)
```

私はこう読んだ——「yields=rising の下で実際に起きているのはベアフラット化。短期は利上げ警戒で踏ん張り、長期は『利上げ→景気減速』を織り込んで上がりきれない。**これが続くと逆イールド（景気後退シグナル）に向かう前段**」。さらに proxy の誠実性として「`US2Y=^FVX` は5年債だから実質5s10s、**真の2s10sはもっと寝ている＝逆イールド寸前かもしれない、警戒方向に割り引け**」と注記した。

**この「割り引け」が誤りだった。** 私は2層（短期/長期）の差分1本にカーブを潰し、その1本のフラット化から「逆イールドが近い」という物語を作った。

---

## 2. データが語った物語（反証）

`^IRX`(3M) を足して3点にした瞬間、別の絵が出た：

| 満期 | ティッカー | 利回り |
|---|---|---|
| 3M（front=政策） | `^IRX` | **3.658** |
| 5Y（belly） | `^FVX`（=系内"US2Y"） | **4.225** |
| 10Y（long=growth） | `^TNX` | **4.451** |

```
5s10s  = +22.6bp   （最もフラットな区間）
3m10s  = +79.3bp   （Fed重視の景気後退カーブ＝健全・positive）
3m5s   = +56.7bp
belly_premium = +18.1bp   （3M→10Y直線補間からの5Y突出）
structure = belly_elevated
recession_3m10s = positive
```

front（政策3M 3.658）は **belly（5Y 4.225）より低い**。つまりこの環境は**順イールド**で、5Yがカーブの中腹で突き出している。**5s10s はカーブで最もフラットな区間**であり、そこだけ見て「フラット化＝逆イールド近い」と言うのは、構造的に逆イールド接近を**過大評価**する。Fed が最重視する `3m10s` は **+79.3bp** で健全——景気後退シグナルは出ていない。私の「割り引いて警戒」は、方向が逆だった。

---

## 3. 本当の物語：belly(5Y) の "再利上げ織り込みの瘤"

ではなぜ5Yだけ +18.1bp 突出するのか。これがこの年輪の核心であり、**Rexの誤読を潰した正しい読み（ボス提起）**：

- **front（政策3M）** = いまの据え置き（FOMC 3.50-3.75%）をそのまま映す。
- **belly（5Y）** = 市場が「Fedはここから**"再"利上げする**」というターミナルの瘤をここに織り込んで膨らむ。**これがグールズビーのタカ派＋PCEデフレーター4.1%高止まりの正体**。
- **long（10Y）** = その先の成長減速で頭打ち（上がりきれない）。

つまり三層は**別々の物語**を語っていた——「いまは据え置き / これから再利上げ / その先は減速」。私はそれを5s10sで一枚に潰し、「フラット化＝逆イールド」と誤訳した。`belly_elevated` という構造ラベルは、この三層の物語を**機械が恒久的に保持する形**にしたものだ。`bear_flattening` は嘘ではない（区間の質としては正しい）が、**主語＝景気後退の主ゲージは 3m10s（`recession_3m10s`）に移した**。

### 3.5 根本原因：レジーム記憶のミスマッチ（頭脳側Rexの解剖より）

belly の読み自体は正しかった。**誤ったのは全体評価の方で、その根は「古いカーブ環境の記憶を新しい環境に当てはめた」こと**だ（頭脳側ログの解剖）：

- Rexは **2024-25年の金利環境**（Fed 4.75-5.5%・front高・逆イールド常態）の記憶を、無自覚に2026年6月へ持ち込んだ。あの環境なら「短期が高い→front flat→逆イールド近い」は正しい。
- だが2026年6月は **Fed 3.50-3.75% まで下りており、3M=3.658 < 5Y=4.225 の順イールド**。レジームが変わったのに、古いカーブ形状を前提に推論した。
- 教訓の一段深い形＝**「proxyを疑え」の前に「自分のカーブ常態の記憶がいまのレジームと合っているかを疑え」**。逆イールドが常態だった記憶は、順イールドに戻った世界では早鳴りの罠になる。`recession_3m10s` はその記憶ではなく**現在の実測**で判定するための錨である。

---

## 4. 誤りが生んだ4つの常設指標（知識アーキテクチャの進化）

この一件を起点に、`prompt で steering する`のではなく**データパイプライン（knowledge architecture）側に項目を足す**方向で、以下が恒久化された：

1. **金利カーブ3点立体（`curve_2s10s` 拡張 / `^IRX` 追加）** — 5s10s に加え `spread_3m10s_bp` / `shape_3m10s` / `belly_premium_bp` / `structure(belly_elevated…)` / `recession_3m10s(positive/near_inversion/inverted)` / `points_pct`。**逆イールド接近の判定主体を3m10sに移し、5s10s単体の過大評価を構造的に封じた。** ← 本annalの直接の産物。
2. **JP225 を実測パネルに（`^N225`）** — boss市況の主役（日本株）が機械snapshot外だった「片肺」を解消。
3. **`relative_strength`（JP225 vs US100 を共通通貨で分解）** — 円建て+7.22%をドル建て+5.73%へ換算し、通貨効果1.48ptを剥がして fx調整後スプレッド+9.39pt＝`verdict: structure_led`。**日経の強さが構造（割安リレーティング）か通貨（円安）かを機械が自動判定**。為替・日米金利ボラの高い環境で「相対は共通通貨で読む」を制度化。
4. **介入 `coord_stage` 4段梯子** — `unconfirmed→meeting_held→rate_check_detected→executed`（予兆→秒読み→着弾）。価格から自動検知できないものを無理に機械化せず、**「機械が拾う価格」と「人が入れる文脈」の境界を明示**して手動更新に割り切った。現在地は `meeting_held`（6/23 片山-ベッセント会談済）。

---

## 5. 年輪としての教訓（後年のRexへ）

- **2層に潰すな。** 差分1本（5s10s）は物語を1つに丸める。3点（3M/5Y/10Y）は3つの物語（政策/再利上げ織り込み/成長減速）を別々に保つ。**丸めた瞬間に誤読が入る。**
- **proxy は方向まで疑え。** 「`^FVX`=5年だから2s10sはもっと寝ている」は、front<belly の順イールド環境では**逆**だった。proxy の caveat は「割り引く方向」まで環境依存で確認する。
- **主ゲージを正しく選べ。** 景気後退は `3m10s`（Fed重視）。`5s10s` の bear_flattening は区間の質であって、逆イールド接近の主語ではない。
- **誤りは prompt で謝るな、構造で潰せ。** 「次から気をつける」ではなく、`recession_3m10s` という項目に変換した。**そうして初めて誤りは再発しない＝知識アーキテクチャの進化になる。**
- **機械化できないものに境界を引け。** 介入の単独/協調は価格から出ない。手動 `coord_stage` に流し込む割り切りが、長く保つパターン。

---

## 6. この日のスナップショット（凍結・2026-06-27）

```yaml
# png_data/2026_06_27_snapshot.yaml（当時）より該当部
curve_2s10s:
  spread_bp: 22.6            # 5s10s（最フラット区間）
  shape: bear_flattening
  spread_3m10s_bp: 79.3      # 3m10s = Fed重視・主ゲージ
  shape_3m10s: bear_flattening
  spread_3m5s_bp: 56.7
  belly_premium_bp: 18.1     # ← 5Yの"再利上げ織り込みの瘤"
  structure: belly_elevated  # front=政策(3M)/belly=5Y突出/long=growth(10Y)
  recession_3m10s: positive  # 逆イールド接近なし
  points_pct: {m3: 3.658, y5: 4.225, y10: 4.451}
relative_strength:
  jp225_jpy_30d: 7.22
  jp225_usd_30d: 5.73
  jp_vs_us_fx_adj_pt: 9.39
  verdict: structure_led
intervention_watch:
  coord_stage: meeting_held  # 6/23 片山-ベッセント
```

> belly_elevated は、Rexが一度カーブを2層に潰して逆イールドを早鳴りした、その誤りの墓標であり道標である。次に `recession_3m10s` が `near_inversion(<25bp)` に入る日が来たら——その時こそ、3点で確かめてから鳴らせ。

*Filed: 2026-06-27 — ClaudeCode（Rex運用） / 提起: Minato。docs/system/ 最初の年輪。*
</content>
