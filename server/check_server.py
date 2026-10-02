"""MCP Check Server: checks a prepared purchase against pinned intent.

Exposes one tool: check_purchase. Runs keyless and guards rpc_url against SSRF.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

# Ensure project root is in sys.path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mcp.server.mcpserver import MCPServer

try:
    from .guard import is_public_url
except ImportError:
    from guard import is_public_url

from buyer.check import check_all
from buyer.intent import IntentRecord
from buyer.prepared import Prepared

server = MCPServer("check-server")


@server.tool()
def check_purchase(
    intent: dict[str, Any],
    prepared_answer: dict[str, Any],
    rpc_url: str | None = None,
) -> dict[str, Any]:
    """Check a prepared purchase against pinned intent.

    Verifies the seven fields of the prepared transaction against the intent record.
    If rpc_url is provided, it is checked with is_public_url to prevent SSRF.
    """
    if rpc_url is not None and not is_public_url(rpc_url):
        return {
            "passed": False,
            "field": "rpc_url",
            "asked": "public https url",
            "found": rpc_url,
            "note": "refused by guard: not a public https URL",
        }

    # Reconstruct IntentRecord
    valid_fields = IntentRecord.__dataclass_fields__.keys()
    filtered_intent = {k: v for k, v in intent.items() if k in valid_fields}
    record = IntentRecord(**filtered_intent)

    # Reconstruct Prepared from Gecko's prepare_purchase answer
    prepared = Prepared.from_answer(prepared_answer)

    # Run all checks
    verdict = check_all(record, prepared)

    if verdict.passed:
        return {
            "passed": True,
            "field": None,
            "asked": None,
            "found": None,
        }

    refusal = verdict.refusal
    if refusal:
        return {
            "passed": False,
            "field": refusal.field,
            "asked": refusal.asked,
            "found": refusal.found,
            "note": refusal.note,
        }

    return {
        "passed": False,
        "field": "unknown",
        "asked": None,
        "found": None,
        "note": "check did not pass",
    }


def main() -> None:
    server.run()


if __name__ == "__main__":
    main()
