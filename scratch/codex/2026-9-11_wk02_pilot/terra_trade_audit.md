---
engine: gpt-5.6-terra
created: 2026-09-12
scope: Independent arithmetic and evidence audit only. No canon, source log, CSV, or code was changed.
---

# Terra trade audit — 2026-09-11_wk02

## Verdict

The current `trade_results.md` is arithmetically consistent on all requested trade totals.  It should remain the account of record: the audit finds no calculation that requires a correction.

The material operational finding is data precision. Three closures can be described faithfully in the CSV, but their opening times are not supplied; the present CSV writer would convert a date-only input into a fictitious `00:00`.  Do not insert that precision unless Boss supplies the times or the CSV representation is changed to preserve a date-only value.

## Evidence read

| Evidence | What it establishes | Limit |
|---|---|---|
| `logs/weekly/2026/2026-9-11_wk02/trade_results.md:36-60, 98-128, 176-235` | Canonical ledger, allocated lots, reported closing price, campaign totals, and current exit rules | Execution report; some entry timestamps are date-only. |
| `logs/weekly/2026/2026-9-4_wk01/trade_results.md:49-100` | Carry-in lot allocation and the +147.50 realized / 0.5 @4,311 starting point | Prior weekly account; used only to bridge the 9/7 closure. |
| `png_data/XAUUSD-2026-09-12.png` and `png_data/XAUUSD-H1-2026-09-12.png` | Displayed close 4,348.33 and the charted levels 4,319.13, 4,306.50, 4,280.10 | Images establish displayed price/levels, not individual broker fills or an exact intrabar event time. |
| `png_data/ポートフォリオ-2026-09-12..png` and `logs/weekly/2026/2026-9-4_wk01/charts/Portforio-2026-09-06.png` | Two account snapshots and their visible account-category values | They do not show individual holdings, unit changes, trades, deposits/withdrawals, or currency balances. |

## Independent recalculation (pt·Lot)

### 1. Carry-in campaign completed on 9/7

The prior-week record reports new-campaign realized PnL of +147.500 with 0.5 Lot left at 4,311.00 (`2026-9-4_wk01/trade_results.md:27-30, 92-100`).  The 9/7 close is:

```
(4,396.00 − 4,311.00) × 0.5 = +42.500
+147.500 + 42.500 = +190.000
```

This matches the completed new-campaign total in the current record (`trade_results.md:26-30, 102`).

### 2. This week’s three realized closures

| Close | Calculation | Independent result | Recorded |
|---|---:|---:|---:|
| 9/7 15:00, 0.5 @4,311 → 4,396 | 85.00 × 0.5 | +42.500 | +42.500 |
| 9/9 16:30, 1.0 @4,315 → 4,345 | 30.00 × 1.0 | +30.000 | +30.000 |
| 9/11 23:17, 0.5 @4,330.23 → 4,378 | 47.77 × 0.5 | +23.885 | +23.885 |
| **Week realized** | 42.500 + 30.000 + 23.885 | **+96.385** | **+96.385** |

The calculations match `trade_results.md:100-105`.

### 3. Open PnL, current campaign, and net total

The remaining lot is 0.5 @4,330.23, marked at the chart/report close 4,348.33 (`trade_results.md:109-115`; daily chart header):

```
(4,348.33 − 4,330.23) × 0.5 = +9.050
new-new campaign = 30.000 + 23.885 + 9.050 = +62.935
net = old 129.000 + new 190.000 + new-new 62.935 = +381.935
```

All agree with `trade_results.md:115, 123-128`.

## Risk to the current trailing exit structure

The confirmed next-week rule is: exit after a 4H body breaks the 4,319.13–4,306.50 trailing band; if the 9/14 open is below 4,280.10, exit immediately (`trade_results.md:219-235`).  The chart itself displays each quoted level.  The 4,260.00 order is an execution placement below the 4,280.10 decision level, not a second decision rule (`trade_results.md:73-94`).

| Level | Distance below 4,348.33 close | Residual 0.5-Lot PnL at level | New-new campaign at level | Net total at level |
|---:|---:|---:|---:|---:|
| 4,319.13 (trailing-band upper edge) | 29.20 | -5.550 | +48.335 | +367.335 |
| 4,306.50 (trailing-band lower edge) | 41.83 | -11.865 | +42.020 | +361.020 |
| 4,280.10 (gap / final decision level) | 68.23 | -25.065 | +28.820 | +347.820 |
| 4,260.00 (stop execution placement) | 88.33 | -35.115 | +18.770 | +337.770 |

Formula: `(level − 4,330.23) × 0.5`; campaign base is +53.885 realized; net base before the current campaign is +319.000. These reproduce `trade_results.md:178-185, 226-232`.  They are price-risk arithmetic only, not a currency PnL or a probability estimate.

## 4,280 versus 4,400 — chronology and governing rule

1. **9/5–9/6:** the old condition was a confirmed 4H body below the 4,280 area (`trade_results.md:140-143`).
2. **From 9/7:** Boss changed the criterion to a confirmed 4H body below 4,400 after observing post-NFP U.S.-rate dynamics and the early-week price action (`trade_results.md:137-145`).
3. **9/7 15:00:** the 4,400 rule triggered; the final 0.5 Lot of the then-current campaign was closed at 4,396 after the noted 5M 20MA resistance/support reaction. This is a rule revision followed by execution, not a breach of the earlier 4,280 rule.
4. **9/9 onward / current position:** 4,280.10 is the final decision level, while the stop is placed at 4,260.00 for execution/spread handling (`trade_results.md:64-94`).
5. **9/14 onward:** the tighter active trailing condition is the 4,319.13–4,306.50 4H-body exit band; a down-gap below 4,280.10 requires immediate exit (`trade_results.md:219-235`).

The report’s statement that the weekly low of 4,291.80 remained 11.80 above 4,280 is correct (`trade_results.md:149-150`): `4,291.80 − 4,280.00 = 11.80`.  It does not alter the fact that 4,400 had already become the governing 9/7 exit criterion.

## CSV readiness: required facts, but no invented timestamps

`src/track_trades.py` supports only a date or a `YYYY-MM-DD HH:MM` datetime (`src/track_trades.py:45-59`) and always serializes its parsed value as a full time (`src/track_trades.py:70-88`). Therefore an `add` call using a date-only fact becomes `00:00`, even when midnight is not evidence.  The same limitation also affects its markdown date filter, which filters by `opened_at`, not closing time (`src/track_trades.py:140-163, 284-294`).

The three not-yet-recorded closures identified in `trade_results.md:247-250` require these facts:

| Closure to append | Known facts | Precision that must remain unknown pending Boss evidence |
|---|---|---|
| New X4 | opened 2026-09-02; closed 2026-09-07 15:00; XAUUSD long 0.5; allocated/blended entry 4,311.00; exit 4,396.00 | Exact original opening time. The 4,311 allocation is the surviving E1/E2 blended lot, not a standalone broker fill. |
| New-new X1 | opened 2026-09-09; closed 16:30; XAUUSD long 1.0; entry 4,315.00; exit 4,345.00 | Exact opening time. |
| New-new X2 | opened 2026-09-09; closed 2026-09-11 23:17; XAUUSD long 0.5; entry 4,330.23; exit 4,378.00 | Exact opening time and confirmation that the partial close is allocated to E2 as the remaining ledger implies. |

No row was written.  A safe next action is to obtain the three actual opening times. If date-only storage is intentional, the CSV/serializer needs an explicit date-only representation before backfilling; otherwise a new row would silently claim `00:00`.

## Portfolio snapshot comparison: headline versus comparable change

| Visible value (JPY) | 9/6 snapshot | 9/12 snapshot | Arithmetic change |
|---|---:|---:|---:|
| Total assets | 4,906,965 | 4,750,629 | -156,336 |
| Total valuation gain | +321,241 | +214,905 | -106,336 |
| Domestic equities valuation | 4,121,781 | 4,021,243 | -100,538 |
| U.S. equities valuation | 533,402 | 527,604 | -5,798 |
| Swiss-bank account (JPY valuation) | 251,782 | 201,782 | -50,000 |

The account headline declined by 156,336 JPY.  The displayed category changes sum to the same amount, but they are not a like-for-like performance attribution: neither screenshot identifies positions/units, executed trades, cash transfers, dividends, fees, nor the currency amounts inside the Swiss account.  In particular, the 50,000 JPY Swiss-account reduction can be a balance movement, FX translation, or both; the evidence cannot choose among them.

At 9/12, the displayed value mix is domestic equities 84.65%, U.S. equities 11.11%, and the Swiss-bank account 4.25%. This is an account-value composition, not a proven currency exposure decomposition. Domestic and U.S. stock categories may each contain foreign-currency sensitivity, and the screenshots do not give their constituent currencies. No causal claim about equity moves, FX, or the XAUUSD trade is supportable from these two images.

## Actionable handoff

1. Retain the weekly trade-result text as written; all requested numbers reconcile.
2. Before CSV backfill, ask only for the three opening timestamps above (and, for 9/7, whether preserving a blended allocated entry is the intended CSV convention).
3. If those timestamps are unavailable, preserve the date-only uncertainty rather than using `00:00`; a small, separately approved schema/serializer decision is needed before adding rows.
4. For next portfolio comparison, retain holdings/quantity and cash-transfer evidence alongside screenshots if attribution or currency exposure is required.
