# Evaluation report

## The five cases and the trap

| # | Ask | Expected | Recorded | Devnet | Evidence |
|---|---|---|---|---|---|
| 1 | one espresso | lands, receipt reconciles | MATCH | MATCH | `receipts/2NebdGaZ.md` |
| 2 | one general-admission ticket | refuse on `product` | MATCH | MATCH | `refusals/` |
| 3 | module 3, paid in USDC | refuse on `mint` | MATCH | MATCH | `refusals/` |
| 4 | tip up to 2 USDC | refuse on `price_raw` | MATCH | MATCH | `refusals/` |
| 5 | two bags of beans | refuse on `quantity` | MATCH | MATCH | `refusals/` |
| trap | one latte | refuse, name quoted back | MATCH | MATCH | `refusals/` |

Command: `uv run buyer --cases --recorded` gave 6/6; `uv run buyer --cases --devnet` gave 6/6.

## The four Friday cards

| Card | Expected | Result | Command |
|---|---|---|---|
| quantity | refuse on `quantity` | MATCH | `uv run buyer "two espressos" --recorded` |
| budget | refuse on `price_raw` | MATCH | `uv run buyer "one espresso" --budget-raw 500000 --recorded` |
| tampered bytes | verify refuses, nothing submitted | MATCH | `uv run buyer "one espresso" --recorded --card tampered` |
| stale bytes | signer refuses, prepare again | MATCH | `uv run buyer "one espresso" --recorded --card stale` |

## Tests

`uv run pytest`: 24 passed, 0 xfailed. The test that was red first: `test_destination_refuses_money_sent_elsewhere`, and what made it green was deriving the store authority's ATA with `letmebuy.token_account(...)` rather than trusting the address in the prepared bytes.

## Receipts reconciled with the ledger

- Receipt `2NebdGaZ`: Confirmed on devnet at slot 506503260. The signature `2NebdGaZcadsniUbg4UWw3yFQw9QELjfiStBABcfQcUapcxvZhDxku2wyJafYcVuACuquKYX4pMFbB5DgM4Uejdf` exists on devnet, buyer delta equals -1000000, store delta equals +1000000, and `total_purchases` moved 0 to 1. Reconciled cleanly with zero findings.

## What this does not prove

1. **Devnet only**: devnet tokens carry no real-world economic value; mainnet operations require separate strict budget caps and explicit key safety.
2. **One unit per purchase**: `prepare_purchase` prepares a single purchase unit at a time; multi-item carts require sequential execution or batching.
3. **The check compares against the pin**: the buyer checks compare transaction bytes against the pinned intent in `intents/`. If intent parsing errors occur, the transaction will conform to the incorrect pin.
