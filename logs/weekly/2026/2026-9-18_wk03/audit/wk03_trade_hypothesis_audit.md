---
engine: gpt-5.6-terra
created: 2026-09-20
scope: independent_read_only_audit
week: 2026-9-18_wk03
source_authority: wk03 trade_results, wk02 carry-forward/addendum/meta/handoff, September distilled, wr-2026-9-18, and current private_trades.csv
write_boundary: Scratch audit only. No source artifact or CSV was edited.
---

# 2026-9-18_wk03 CFD / hypothesis independent audit

## Result

The reported wk03 CFD ledger is internally consistent.  One documented partial
exit adds +50.000 pt-Lot; the residual position is 1.0 Lot; and the marked
week-on-week increase is +114.785 pt-Lot.  The pre-existing 4,260 stop was
cancelled before the FOMC response and must not be represented as an exit.
The currently reported protective stop is 4,230 for the residual 1.0 Lot.

This audit does not authorize a trade, an order change, an automatic
re-entry, or a CSV write.

## CFD reconciliation

### Position path and documented exit count

| Stage | Quantity | Attribution | Audit result |
|---|---:|---|---|
| 9/11 carry | 0.5 Lot | 9/9 E2-derived, entry 4,330.23 | Confirmed baseline |
| 4,260 cancellation | 0.5 Lot | stop cancelled at 4H descending-line confluence; PA judgement substituted | Not an exit and not a new entry |
| 9/17 E3 | +1.0 Lot @4,279 | Boss-confirmed addition | 1.5 Lot total |
| 9/17 X3 | -0.5 Lot @4,379 | Assigned to E3 as stated | 1.0 Lot total |
| weekend carry | 1.0 Lot | 0.5 @4,330.23 plus 0.5 @4,279 | Confirmed |

`(4,379 - 4,279) x 0.5 = +50.000 pt-Lot`.

The documented count changes from 10 exits / 9 wins / 1 loss to **11 exits /
10 wins / 1 loss**.  E3 is an entry, the 4,260 cancellation is an order
change, and the 4,230 stop is a live protective-order level; none belongs in
the closed-exit count.

### Mark-to-market bridge

At the supplied Pepperstone mark C=4,378.45:

| Residual lot | Calculation | pt-Lot |
|---|---|---:|
| 0.5 @4,330.23 | (4,378.45 - 4,330.23) x 0.5 | +24.110 |
| 0.5 @4,279.00 | (4,378.45 - 4,279.00) x 0.5 | +49.725 |
| Total | weighted entry 4,304.615 | +73.835 |

Realised cumulative: 372.885 + 50.000 = **422.885 pt-Lot**.
Marked cumulative: 422.885 + 73.835 = **496.720 pt-Lot**.
Weekly bridge: 50.000 + (73.835 - 9.050) = **+114.785 pt-Lot**;
496.720 - 381.935 gives the same result.

If the live 1.0 Lot were executed at 4,230, its conditional price-difference
result would be -74.615 pt-Lot, as the wk03 report states.  That is a scenario,
not a realised loss or a reason to create a closed row now.

## CSV audit: schema and one candidate only

Current `data/private_trades.csv` schema is:

```text
opened_at,closed_at,symbol,direction,size,entry_price,exit_price,pnl_pct,pnl_amount,tag,notes
```

No existing row has the 9/17 close, entry 4,279, or exit 4,379.  When the
weekly owner performs the normal duplicate check, the one candidate row is:

```csv
2026-09-17,2026-09-17 21:30,XAUUSD,long,0.5000,4279.000000,4379.000000,2.3370,0.0000,"gold_long,partial_tp,new_new_campaign,event_fomc","新新X3。9/17に追加した1Lot@4279のうち0.5Lotを21:30 JSTに4379で利確。+50.000 pt-Lot。opened_atはBoss報告が日付のみのため日付精度。旧0.5Lot@4330.23は決済せず持越し。旧4260逆指値は4H下落トレンドライン交差を根拠に解除済みで、当該約定ではない。残1.0Lotには4230の全決済逆指値が報告されている。出典2026-9-18_wk03/trade_results.md。pnl_amount=0は既存形式の未入力値で、円貨実現額0を意味しない。"
```

`pnl_pct` is `(4,379 - 4,279) / 4,279 x 100 = 2.3370`; `pnl_amount=0.0000`
follows the current file convention and must not be treated as a monetary PnL.
The opening time is deliberately not invented.  This candidate does not solve
the separate, older wk03 X1/X2 backfill that remains pending.

## Carry-forward changes that must be explicit

1. The 9/14-only lower-gap exception and the former `4H body below
   4,319.13-4,306.50 plus weekly descending line` exit condition were prior
   context.  They are not standing instructions for later sessions.
2. The old 4,260 execution stop was explicitly cancelled.  Do not label the
   FOMC dip as a rule breach, a stop fill, or a sell-and-rebuy sequence.
3. The current state is the two residual lots above and the reported 4,230
   all-position stop.  Its entry time, order-amendment time, broker fill policy,
   and contract multiplier remain unverified.
4. Exact post-entry MAE remains unmeasured: the supplied 15M/daily/4H charts
   do not supply E3's time or a complete post-entry path.  A displayed bar low
   or a drawn level must not be substituted for MAE.
5. Do not carry prior week values, account state, or a generic Saturday cutoff
   into wk03.  `wr-2026-9-18.md` supplies named vendors, but says its prior-week
   comparisons have not independently verified perfectly matching reference
   times.

## P9--P12 and related hypothesis status

| Item | wk03 evidence/status | Required next handling |
|---|---|---|
| P9 | No exact event window was supplied. | Keep count unchanged. |
| P10 | No Boss definition of “statement date” was supplied. | Do not create dates or counts. |
| P11 | The report's reference comparison is TVC US2Y/JP2Y and FXCM USDJPY: 2Y spread 278.8bp (4.630-1.842) to 291.6bp (4.756-1.840), **+12.8bp**; USDJPY 153.468 to 156.854, **+2.21%**.  Its direction is expansion plus yen weakness, so it is not a counterexample. | Preserve counterexample **1** from 9/11.  Do not reset it, count this as proof, or advance the two-counterexample invalidation.  For the next evaluation, capture the two raw same-vendor observations with instrument, vendor, bar interval, comparison start/end, and actual cutoff; then apply the symmetric rule only once to that declared window. |
| P12 | The new report gives a later USDJPY level, but no same-feed/same-cutoff reconstruction of its original 9/9 test. | Formal status remains pending; do not infer success/failure from mixed FXCM/Yahoo windows. |

P11's current rule remains symmetric: both `spread contraction + USDJPY rise`
and `spread expansion + USDJPY fall` are counterexamples; two qualifying weekly
observations invalidate it.  The prior one-way wording remains history only.
The wk03 direction is compatible with the hypothesis but does not establish
causality; the report itself says the reference cutoffs are not completely
verified.

Rejected 8-2/8-3 are not revived by this week's price or nominal-yield data.
Likewise, WTI cash 100.026, high nominal yields, VIX 14.82, and BTC 80,911.10
are market observations, not approval to install a new threshold or combine
vendors into a causal measure.

## Audit disposition

Ready for the week owner to use as a read-only reconciliation input.  Before a
CSV write, recheck that the candidate is absent, retain date-only precision for
the entry, and keep the older X1/X2 backfill as a separate scope.  No source
files, Canon documents, images, or CSV rows were modified by this audit.
