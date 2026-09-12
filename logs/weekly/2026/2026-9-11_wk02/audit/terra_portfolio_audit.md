---
engine: gpt-5.6-terra
created: 2026-09-12
scope: Screenshot-to-screenshot portfolio reconciliation. Source images, weekly records, private CSV, and code were not changed.
---

# Terra portfolio audit — 2026-09-06 to 2026-09-12

## Result

The same ten Japanese equity lots and the same two U.S. equity lots are visible in both snapshots. Every displayed share quantity and acquisition amount is unchanged, including GX Gold (425A) held separately as **750 shares in the taxable account** and **2,000 shares in NISA**. Therefore the stock-value changes are comparable mark-to-market changes for the displayed holdings; the screenshots show no purchase or sale.

Boss confirmed that 50,000 JPY was moved to a bank account. Removing that known cash movement from the account-headline comparison leaves **-106,336 JPY**, exactly the sum of Japanese equities **-100,538 JPY** and U.S. equities **-5,798 JPY**. The sweep account is a **sweep-dedicated bank account**, not a Swiss bank account; the earlier label was incorrect.

## Source images actually inspected

| Snapshot | Japanese equities | U.S. equities | Portfolio headline |
|---|---|---|---|
| 2026-09-06 | `logs/weekly/2026/2026-9-4_wk01/charts/Portfolio-JP-Stocks-2026-09-06.png` | `logs/weekly/2026/2026-9-4_wk01/charts/Portfolio-US-Stocks-2026-09-06.png` | `logs/weekly/2026/2026-9-4_wk01/charts/Portforio-2026-09-06.png` |
| 2026-09-12 | `png_data/東証株-2026-09-12..png` | `png_data/米国株-2026-09-12..png` | `png_data/ポートフォリオ-2026-09-12..png` |

## Headline reconciliation: reported account versus comparable base

| Item (JPY) | 9/6 | 9/12 | Change |
|---|---:|---:|---:|
| Displayed account assets | 4,906,965 | 4,750,629 | -156,336 |
| Known movement to bank account | — | 50,000 | -50,000 from displayed account |
| Comparable 9/12 value (displayed assets + moved cash) | 4,906,965 | 4,800,629 | **-106,336** |
| Japanese equity valuation | 4,121,781 | 4,021,243 | -100,538 |
| U.S. equity valuation | 533,402 | 527,604 | -5,798 |
| Stock valuation reconciliation | 4,655,183 | 4,548,847 | **-106,336** |

The 50,000-JPY transfer explains part of the account headline change; it is excluded from the comparable investment-value change. The category evidence reconciles exactly: `-100,538 + -5,798 = -106,336`.

## Japanese equities: holding-by-holding audit

All values are JPY. `acq/current` denotes acquisition unit price / displayed current unit price; `cost/value` denotes acquisition amount / evaluated value. A zero quantity in parentheses is the displayed sold-order quantity, not a reduction of the held quantity.

| Account | Code | Shares 9/6 → 9/12 | Acq/current 9/6 → 9/12 | Cost 9/6 → 9/12 | Value 9/6 → 9/12 | PnL 9/6 → 9/12 | Value change |
|---|---|---:|---|---:|---:|---:|---:|
| Taxable | 200A | 91 → 91 | 4,316 / 4,309 → 4,316 / 4,198 | 392,756 → 392,756 | 392,119 → 382,018 | -637 → -10,738 | -10,101 |
| Taxable | 425A | 750 → 750 | 363 / 373.4 → 363 / 358.1 | 272,250 → 272,250 | 280,050 → 268,575 | +7,800 → -3,675 | -11,475 |
| Taxable | 586A | 50 → 50 | 215 / 253 → 215 / 245.5 | 10,750 → 10,750 | 12,650 → 12,275 | +1,900 → +1,525 | -375 |
| Taxable | 6954 | 100 → 100 | 6,205 / 5,931 → 6,205 / 5,735 | 620,500 → 620,500 | 593,100 → 573,500 | -27,400 → -47,000 | -19,600 |
| Taxable | 7011 | 100 → 100 | 3,880 / 3,754 → 3,880 / 3,705 | 388,000 → 388,000 | 375,400 → 370,500 | -12,600 → -17,500 | -4,900 |
| **Taxable subtotal** |  |  |  | **1,684,256 → 1,684,256** | **1,653,319 → 1,606,868** | **-30,937 → -77,388** | **-46,451** |
| NISA | 1655 | 270 → 270 | 774 / 872.6 → 774 / 846.2 | 208,980 → 208,980 | 235,602 → 228,474 | +26,622 → +19,494 | -7,128 |
| NISA | 2243 | 174 → 174 | 2,680 / 4,244 → 2,680 / 4,299 | 466,320 → 466,320 | 738,456 → 741,066 | +272,136 → +274,746 | +2,610 |
| NISA | 2638 | 193 → 193 | 2,395 / 2,628 → 2,395 / 2,555 | 462,235 → 462,235 | 507,204 → 493,115 | +44,969 → +30,880 | -14,089 |
| NISA | 2847 | 80 → 80 | 2,652 / 3,005 → 2,652 / 2,944 | 212,160 → 212,160 | 240,400 → 235,520 | +28,240 → +23,360 | -4,880 |
| NISA | 425A | 2,000 → 2,000 | 394 / 373.4 → 394 / 358.1 | 788,000 → 788,000 | 746,800 → 716,200 | -41,200 → -71,800 | -30,600 |
| **NISA subtotal** |  |  |  | **2,137,695 → 2,137,695** | **2,468,462 → 2,414,375** | **+330,767 → +276,680** | **-54,087** |
| **Japanese total** |  |  |  | **3,821,951 → 3,821,951** | **4,121,781 → 4,021,243** | **+299,830 → +199,292** | **-100,538** |

The value and PnL changes agree row by row because every acquisition amount and quantity is unchanged. The two-account treatment of 425A is preserved: taxable 750 shares contributed -11,475 JPY, while NISA 2,000 shares contributed -30,600 JPY; together they contributed -42,075 JPY.

## U.S. equities: underlying USD and JPY conversion

| Ticker | Shares | Acquisition USD (unit / total) | 9/6 price / value USD | 9/12 price / value USD | USD value change | 9/6 JPY value / PnL | 9/12 JPY value / PnL | JPY value change |
|---|---:|---|---|---|---:|---|---|---:|
| GDX | 15 | 84.42 / 1,266.30 | 99.26 / 1,488.90 | 97.10 / 1,456.50 | -32.40 | 232,744 / +30,829 | 224,548 / +22,633 | -8,196 |
| SPCX | 13 | 147.13 / 1,912.69 | 147.95 / 1,923.35 | 151.21 / 1,965.73 | +42.38 | 300,658 / -9,418 | 303,056 / -7,020 | +2,398 |
| **Total** |  | **3,178.99** | **3,412.25** | **3,422.23** | **+9.98** | **533,402 / +21,411** | **527,604 / +15,613** | **-5,798** |

The unchanged 15 GDX and 13 SPCX shares make a mechanical decomposition possible. The implied portfolio conversion rate is approximately **156.3197 JPY/USD** on 9/6 and **154.1696 JPY/USD** on 9/12, a **-2.1501 JPY/USD** move. Using those two displayed total values:

```
Underlying USD-value effect at 9/6 rate = (3,422.23 − 3,412.25) × 156.3197 = +1,560.07 JPY
FX-translation effect on 9/12 USD value  = 3,422.23 × (154.1696 − 156.3197) = -7,358.07 JPY
Net displayed U.S.-equity change          = -5,798.00 JPY
```

This is a mechanical two-snapshot conversion decomposition, subject to screen rounding. It attributes the visible U.S.-equity change, not the return of the wider portfolio or a forecast for USD/JPY.

## Composition and bounded currency finding

At 9/12, the displayed account comprises Japanese equities 4,021,243 JPY (84.65%), U.S. equities 527,604 JPY (11.11%), and the sweep-dedicated bank account 201,782 JPY (4.25%). The directly evidenced USD-denominated stock exposure is **3,422.23 USD**, translated on the statement to **527,604 JPY**. The screenshots do not disclose the sweep account’s currency balance or the currency composition of Japanese-listed funds; no broader currency-exposure claim is justified.

## CSV candidate status

`terra_trade_csv_candidates.csv` in this same scratch folder contains only the three confirmed weekly closures in date-only form where the opening time is not known. It is a review artifact, not `data/private_trades.csv`, and must not be fed through `track_trades.py add` without preserving the date-only precision.
