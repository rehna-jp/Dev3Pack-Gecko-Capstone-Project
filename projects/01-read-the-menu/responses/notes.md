1.Product picked:
Espresso: price_raw: 100000, decimals: 6, mint: EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v (classic SPL token).

2.What prepare_purchase answered and why:
It returned refused: true with code receipt-failed. The store and product resolved correctly, but simulation showed the empty buyer wallet holds 0 SOL on mainnet and cannot pay the transaction fee.

3.The refusal from step 4:
Code product-unknown: 'geckocoffee' does not sell 'Unicorn latte'. Gecko refuses to guess what the buyer meant, refuses to pick a close match, and returns the list of 20 real menu items so the buyer can decide.

4.Comparison with Telegram:
Both the Telegram bot and the MCP response list the same store products (Espresso, Sparkling water, Cappuccino, etc.) with matching prices. The difference is that MCP returns structured raw JSON with whole-number price_raw, decimals, and mint public keys for programmatic checking, while Telegram returns human-formatted UI text (e.g. 0.1 USDC).
