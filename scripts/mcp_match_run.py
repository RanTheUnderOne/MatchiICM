#!/usr/bin/env python3
"""ICM matching/01-load + 02-match, wired to the REAL prod MCP instead of _mock.

Pulls leads + properties from prod-mcp.nadlanai.org, maps them to the shape
scripts/match.py expects, runs the same deterministic match engine, and (with
--write) records the top match back to the DB via link_property_to_lead +
update_lead_properties_to_offer.

WhatsApp is NOT sent. For each matched lead it prints the reply text only:
    היי, מצאתי מאץ'

Usage:
  py scripts/mcp_match_run.py                 # dry-run, no DB writes
  py scripts/mcp_match_run.py --write         # commit matches to prod DB
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mcp_client import MCPClient, DEFAULT_USER, parse_repr
import match as match_engine

try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass

REPLY = "היי, מצאתי מאץ'"
OUT_DIR = Path(__file__).resolve().parent.parent / "phases/3-leads/matching/01-load/output"

# lead.transaction_type (sale/rent) -> match.py intent (buy/rent)
TYPE_INTENT = {"sale": "buy", "rent": "rent"}
_ID_RE = re.compile(r"ID:\s*(\d+)")


def load_leads(c):
    rows = c.call("list_leads", {"user_id": c.user_id, "limit": 200})
    leads = []
    for r in rows:
        leads.append({
            "id": r["phone"],                       # phone is the lead key in MCP
            "name": r.get("full_name"),
            "intent": TYPE_INTENT.get(r.get("transaction_type")),
            "rooms": r.get("rooms"),
            "city": r.get("preferred_city"),
            "neighborhood": None,                   # not stored on lead in MCP
            "budget": r.get("budget"),
        })
    return leads


def load_properties(c):
    listing = c.call("search_real_estate_properties", {"user_id": c.user_id, "limit": 200})
    ids = [int(x) for x in _ID_RE.findall(listing or "")]
    props = []
    for pid in ids:
        raw = c.call("get_property_full_details", {"property_id": pid, "user_id": c.user_id})
        d = parse_repr(raw) if isinstance(raw, str) else raw
        props.append({
            "id": d["id"],
            "transaction_type": d.get("transaction_type"),
            "city": d.get("city"),
            "neighborhood": d.get("neighborhood"),
            "rooms": d.get("rooms"),
            "asking_price": d.get("price"),
            "days_on_market": d.get("days_on_market", 999),
        })
    return props


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", default=DEFAULT_USER)
    ap.add_argument("--write", action="store_true", help="commit matches to prod DB")
    args = ap.parse_args()

    c = MCPClient(user_id=args.user)
    print(f"MCP session {c.session[:8]}… user={c.user_id}")

    leads = load_leads(c)
    props = load_properties(c)
    print(f"Loaded {len(leads)} leads x {len(props)} properties from MCP")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    match_input = {"leads": leads, "properties": props}
    (OUT_DIR / "match-input.json").write_text(
        json.dumps(match_input, ensure_ascii=False, indent=2), encoding="utf-8")

    # run the unchanged deterministic engine
    matches = []
    for lead in leads:
        for prop in props:
            reason = match_engine.hard_block(lead, prop)
            if reason:
                continue
            f = match_engine.soft_factors(lead, prop)
            matches.append({"lead_id": lead["id"], "lead_name": lead["name"],
                            "property_id": prop["id"], "fit": sum(f.values()),
                            "factors": f, "asking_price": prop["asking_price"]})

    by_lead = {}
    for lead in leads:
        ms = [m for m in matches if m["lead_id"] == lead["id"]]
        ms.sort(key=lambda m: (-m["fit"], m.get("asking_price") or 0))
        by_lead[lead["id"]] = ms[:3]

    print(f"\n{sum(1 for v in by_lead.values() if v)} leads matched:")
    for lead in leads:
        ms = by_lead[lead["id"]]
        if not ms:
            print(f"  {lead['name']} ({lead['id']}) -> no match")
            continue
        top = ms[0]
        print(f"  {lead['name']} ({lead['id']}) -> property {top['property_id']} "
              f"fit {top['fit']} {top['factors']}")
        print(f"     WhatsApp reply: {REPLY}")        # NOT sent — text only
        if args.write:
            offer_ids = [m["property_id"] for m in ms]
            c.call("link_property_to_lead",
                   {"phone": lead["id"], "user_id": c.user_id, "property_id": top["property_id"]})
            c.call("update_lead_properties_to_offer",
                   {"phone": lead["id"], "user_id": c.user_id, "property_ids": offer_ids})
            print(f"     [written] linked {top['property_id']}, offer {offer_ids}")

    if not args.write:
        print("\n(dry-run — no DB writes. Re-run with --write to commit.)")


if __name__ == "__main__":
    main()
