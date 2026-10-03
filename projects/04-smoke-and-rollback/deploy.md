# Check Server Deployment

## 1. Public Endpoint
- **URL**: `https://dev3rehna-check-server.fly.dev`
- **Transport**: Streamable HTTP / Server-Sent Events (SSE)
- **SSRF Protection**: Protected by `server/guard.py` (`is_public_url` standard library checks). Refuses loopback, RFC 1918, link-local, multicast, and non-HTTPS endpoints before making any RPC connections.

## 2. Sample Call: `check_purchase`

### Request
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "check_purchase",
    "arguments": {
      "intent": {
        "ask": "two bags of beans",
        "store": "dev3pack-cafe",
        "product": "Beans",
        "quantity": 2,
        "budget_raw": 2000000,
        "mint": "Eoqdd43nFQ9HzGq8HjBRVLCV6aTqCFRiwHy1ZVQheYSi",
        "buyer": "7osLGtZbKok51ZD5bPMLcYEjxcdQVDe5f3iMG1vwak7W",
        "network": "devnet",
        "store_authority": "Dt8quRFWgTMrrDgVa4GGFRJWksncskbs1tpYAQHkEPwJ",
        "menu_price_raw": 1500000
      },
      "prepared_answer": {
        "transaction": {
          "unsigned_transaction": "AQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAEDB1tVw..."
        },
        "status": "pass",
        "binding": "92dd3b410de8be6e9c313cf3a8cea058efd2f877e45b28d3a81c18ef52315867",
        "expires": {
          "last_valid_block_height": 492608644
        },
        "effects": {
          "tokens_out": [
            {
              "owner": "7osLGtZbKok51ZD5bPMLcYEjxcdQVDe5f3iMG1vwak7W",
              "amount_raw": "1500000"
            }
          ]
        }
      }
    }
  }
}
```

### Response
```json
{
  "passed": false,
  "field": "quantity",
  "asked": 2,
  "found": 1,
  "note": ""
}
```

## 3. Redeployment Command
```bash
fly deploy --app dev3rehna-check-server
```

## 4. Rollback Strategy
If the deployed check server or hosted endpoint is unavailable during the Friday defence:
1. Fall back to local stdio invocation:
   ```bash
   uv run python server/check_server.py
   ```
2. Or use the recorded buyer lane (`GECKO_SOURCE=recorded`) which executes the same check logic locally against fixture data without network dependencies:
   ```bash
   GECKO_SOURCE=recorded uv run buyer "one espresso" --devnet
   ```
