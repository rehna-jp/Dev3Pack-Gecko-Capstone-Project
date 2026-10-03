# Issues

*Real incidents from your week, newest first. Thursday's project 04 needs at least one
that actually happened on devnet (not one you invented). The top three are what you would
bring up on Friday if asked "what went wrong".*

## 2026-10-02: verify_signed_transaction refused due to additionalProperties: false in Gecko MCP schema

- **What I saw:**
  ```text
  [  ok] sign      signed by 7osLGtZbKok51ZD5bPMLcYEjxcdQVDe5f3iMG1vwak7W
  [  NO] verify    REFUSED on signed bytes: asked 'the prepared bytes, signed', verify 'different bytes'
  Nothing was submitted.
  ```
  printed by `uv run buyer "one espresso" --devnet`.
- **What was actually wrong:** In `buyer/agent.py`, the `verify()` step body passed both `"signed_transaction"` and `"transaction"` in the arguments dictionary to Gecko. Gecko's hosted MCP schema for `verify_signed_transaction` strictly sets `"additionalProperties": false` and names the input property `"transaction"`. The unexpected `"signed_transaction"` key caused Gecko to reject the request and report that the signed bytes did not verify.
- **How I found it:** Queried `tools/list` on `https://mcp.geckovision.tech/orquestra/mcp` directly to inspect the JSON schema for `verify_signed_transaction`. The schema confirmed `"additionalProperties": false` and required `transaction`, not `signed_transaction`.
- **What I changed:** Updated `buyer/agent.py` to only pass `"transaction": run.signed`, removing the duplicate `"signed_transaction"` key from both `verify()` and `submit()`.
- **What it cost:** ~10 minutes of debugging. 0 SOL was lost because the runner's order stopped the transaction at `verify` before `submit`.
- **Would the checks have caught it?** Yes, the runner's strict requirement that `verify_signed_transaction` succeed before `submit_transaction` prevented unverified bytes from reaching the network.
