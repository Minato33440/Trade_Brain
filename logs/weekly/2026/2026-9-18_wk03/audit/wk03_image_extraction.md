---
engine: gpt-5.6-luna
week: 2026-9-18_wk03
broker_role: image_extraction
status: extracted_read_only
source_note: "Repository image set: 2026-9-11_wk02/charts (account + 14 market charts, captured 2026-09-12) and 2026-9-18_wk03/charts/XAUUSD additions."
---

# wk03 image extraction

## Scope and cautions

- Read-only inspection. No original image or canon file was edited.
- The account screenshots and 14-chart set are dated 2026-09-12 and belong to the prior-week baseline (`2026-9-11_wk02`). They are not silently treated as 2026-09-18 closes.
- Chart vendor, instrument, timeframe, and top-bar OHLC were read from the image. The right-edge black/colored labels are treated as plotted levels or the last-price marker only when they agree with the top-bar OHLC. A cursor/crosshair or forecast arrow is not a close.
- Exact server cutoff for CFD/FX charts is not visible. Do not infer a blanket Saturday cutoff.

## Account images (2026-09-12 09:08 JST)

### Portfolio total

- Total assets: JPY 4,750,629.
- Evaluation P/L: +JPY 214,905 (+4.73%).
- Domestic stocks: JPY 4,021,243, displayed P/L +JPY 199,292 (+5.21%).
- US stocks: JPY 527,604, displayed P/L +JPY 15,613 (+3.05%).
- Sweep/buying-power account: JPY 201,782.
- The portfolio image has a “sweep excluded” checkbox. The visible total is the displayed total with the sweep line included; do not recompute from the pie chart.

### TSE/Japanese holdings

Values are the screenshot's displayed current price, quantity, valuation, and unrealized P/L. `取引単価` shows a smaller reference/average price above the current price in the screenshot; both are retained where legible.

| Account | Symbol/name | Qty | Current price | Value | Unrealized P/L |
|---|---|---:|---:|---:|---:|
| taxable | 200A 日経半導体ETF | 91 | JPY 4,198 | JPY 382,018 | -JPY 10,738 |
| taxable | 425A GXゴールド | 750 | JPY 358.1 | JPY 268,575 | -JPY 3,675 |
| taxable | 586A NF日経エンタ | 50 | JPY 245.5 | JPY 12,275 | +JPY 1,525 |
| taxable | 6954 ファナック | 100 | JPY 5,735 | JPY 573,500 | -JPY 47,000 |
| taxable | 7011 三菱重工 | 100 | JPY 3,705 | JPY 370,500 | -JPY 17,500 |
| NISA | 1655 iシェアーズ S&P500 | 270 | JPY 846.2 | JPY 228,474 | +JPY 19,494 |
| NISA | 2243 GX半導体 | 174 | JPY 4,259 | JPY 741,066 | +JPY 274,746 |
| NISA | 2638 GXロボ&AI | 193 | JPY 2,555 | JPY 493,115 | +JPY 30,880 |
| NISA | 2847 GX成長インフラ | 80 | JPY 2,944 | JPY 235,520 | +JPY 23,360 |
| NISA | 425A GXゴールド | 2,000 | JPY 358.1 | JPY 716,200 | -JPY 71,800 |

### US holdings

- US account displayed FX-converted valuation: JPY 527,604; USD valuation: USD 3,422.23.
- GDX (VanEck Gold Miners ETF): 15 shares, displayed USD 97.10, value USD 1,456.50 / JPY 224,548, unrealized +USD 190.20 / -JPY 22,633 currency-converted display.
- SPCX (Space Exploration Technologies A): 13 shares, displayed USD 151.21, value USD 1,965.73 / JPY 303,056, unrealized +USD 53.04 / -JPY 7,020 currency-converted display.
- The screenshot's account-level US P/L is +USD 243.24 (+7.65%) and +JPY 15,613 (+3.05%); USD and JPY P/L are different display bases.

## Account comparison against wk02 meta.yaml

The prior `2026-9-11_wk02/meta.yaml` records the same screenshot baseline:

- Prior total assets JPY 4,906,965 → current displayed JPY 4,750,629: -JPY 156,336.
- Confirmed bank transfer: JPY 50,000. Comparable assets including transfer: JPY 4,800,629, change -JPY 106,336.
- Japanese equities: JPY 4,121,781 → JPY 4,021,243: -JPY 100,538.
- US equities: JPY 533,402 → JPY 527,604: -JPY 5,798.
- Sweep: JPY 251,782 → JPY 201,782: -JPY 50,000.
- Unrealized P/L: JPY 321,241 → JPY 214,905: -JPY 106,336.

Interpretation boundary: the JPY 50,000 sweep decrease is consistent with the confirmed bank transfer, but the exact transfer timestamp is unknown. It must not be described as market loss. The remaining comparable-asset decline is -JPY 106,336 and is the valuation change bridge in meta.yaml. Do not infer additional unrecorded deposits/withdrawals.

## 14 market chart images (baseline captured 2026-09-12)

Top-bar OHLC is the primary extraction. Values below are image values, not newly fetched market data.

| File / instrument | Vendor | Timeframes shown | Daily top-bar OHLC / close | 4H top-bar OHLC / close |
|---|---|---|---|---|
| BTC-USD | Binance | 1D, 4H | O 77,200.31 H 77,262.47 L 77,200.31 C 77,262.47 (+0.08%) | O 77,200.31 H 77,262.47 L 77,200.31 C 77,262.47 (+0.08%) |
| DXY | TVC | 1D, 4H | O 99.096 H 99.368 L 98.965 C 99.094 (+0.002) | O 99.123 H 99.151 L 99.088 C 99.094 (-0.026) |
| JP10Y | TVC | 1D, 4H | O 2.973 H 2.997 L 2.963 C 2.987 (+0.064) | O 2.987 H 2.987 L 2.987 C 2.987 (+0.002) |
| JP225 | FOREX.com | 1D, 4H | O 64,083 H 64,916 L 63,068 C 64,686 (+603, +0.94%) | O 64,766 H 64,788 L 64,671 C 64,686 (-80, -0.12%) |
| JP2Y | TVC | 1D, 4H | O 1.839 H 1.846 L 1.832 C 1.842 (+0.013) | O 1.842 H 1.842 L 1.842 C 1.842 (-0.002) |
| US100 | Capital.com | 1D, 4H | O 29,121.9 H 29,478.4 L 29,018.7 C 29,371.2 (+258.8, +0.89%) | O 29,415.3 H 29,458.2 L 29,353.2 C 29,371.2 (-42.3, -0.14%) |
| US10Y | TVC | 1D, 4H | O 4.961 H 4.992 L 4.904 C 4.969 (+0.008) | O 4.973 H approx. 4.979 L 4.967 C 4.969 (-0.006); high is visually uncertain |
| US2Y | TVC | 1D, 4H | O 4.581 H 4.657 L 4.549 C 4.630 (+0.044) | O 4.647 H 4.647 L 4.621 C 4.630 (-0.014) |
| US30Y | TVC | 1D, 4H | O 5.371 H 5.424 L 5.309 C 5.356 (-0.010, -0.19%) | O 5.355 H 5.360 L 5.351 C 5.356 (0.000) |
| USDJPY | FXCM | 1D, 4H | O 154.419 H 154.617 L 153.238 C 153.468 (-0.951, -0.62%) | O 153.714 H 153.776 L 153.444 C 153.468 (-0.246, -0.16%) |
| VIX | TVC | 1D, 4H | O 17.51 H 17.71 L 15.59 C 15.85 (-2.00, -11.20%) | O 15.67 H 15.93 L 15.59 C 15.85 (+0.19, +1.21%) |
| WTI cash | BlackBull Markets | 1D, 4H | O 104.655 H 104.825 L 98.851 C 100.374 (-3.921, -3.76%) | O 100.156 H 101.109 L 99.865 C 100.374 (+0.208, +0.21%) |
| XAUUSD | Pepperstone | 1D, 4H | O 4,322.29 H 4,402.67 L 4,291.80 C 4,348.33 (+31.69, +0.73%) | O 4,358.44 H 4,360.17 L 4,342.79 C 4,348.33 (-10.07, -0.23%) |
| XAUUSD-H1 | Pepperstone | 1H, 15M | 1H O 4,348.37 H 4,351.59 L 4,345.38 C 4,348.33 (+0.11) | 15M O 4,346.35 H 4,349.46 L 4,345.38 C 4,348.33 (+1.70, +0.04%) |

Visible right-edge reference levels include, among others: USDJPY 153.398/153.468, US100 29,371.2, JP225 64,686, WTI 100.374, XAUUSD 4,348.33. These agree with the current-bar labels in the images. Colored horizontal lines and forecast arrows are authored levels/annotations, not closes.

## wk03 additions actually present in repository

### XAUUSD-2026-09-19.png

- Vendor Pepperstone; 1D and 4H panels.
- 1D top bar: O 4,344.14 H 4,399.75 L 4,334.37 C 4,378.45 (+36.86, +0.85%).
- 4H top bar: O 4,393.07 H 4,394.37 L 4,374.80 C 4,378.45 (-14.60, -0.33%).
- Right-edge current marker is 4,378.45; levels such as 4,381.54, 4,335.18, 4,268.13, and 4,225.65 are plotted reference levels, not cursor-derived closes.

### XAUUSD-15M-2026-09-20.png

- Vendor Pepperstone; 15M panel.
- Top bar: O 4,353.64 H 4,356.71 L 4,350.15 C 4,351.55 (-1.38, -0.03%).
- The black right-edge instrument label shows 4,378.45 from the chart's last displayed reference/current context, while the top-bar OHLC for the selected 15M candle shows C 4,351.55. Treat these as different UI contexts; for the selected candle, use 4,351.55 and retain 4,378.45 only as a separate right-edge marker.

## Extraction handoff

- Account quantities, unit prices, valuations, and P/L are sufficiently legible for reconciliation with wk02 meta.yaml; they match its `portfolio_snapshot_20260911` values.
- The confirmed external-flow item is JPY 50,000, with timing unspecified. No additional flow is evidenced by the images.
- Market closes should use top-bar OHLC and explicit vendor/timeframe. Do not use colored horizontal levels, arrows, or cursor/right-edge labels as replacements.
- The 14-chart set is a 2026-09-12 baseline; the only current wk03 repository images are the two XAUUSD images listed above.
