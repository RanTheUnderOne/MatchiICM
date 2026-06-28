#!/usr/bin/env python3
"""ICM lead-scoring, wired to the REAL prod MCP instead of _mock/leads.json.

Pulls leads from prod-mcp.nadlanai.org, maps them to the shape scripts/lead_score.py
expects, runs the same deterministic scoring engine, and (with --write) saves a
deterministic score summary back via save_lead_ai_analysis.

Usage:
  py scripts/mcp_lead_score_run.py            # dry-run, no DB writes
  py scripts/mcp_lead_score_run.py --write    # save score summary to prod DB
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mcp_client import MCPClient, DEFAULT_USER
import lead_score as engine

try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass

OUT_DIR = Path(__file__).resolve().parent.parent / "phases/3-leads/lead-scoring/01-load/output"

# MCP lead.transaction_type (sale/rent) -> engine intent (buy/rent)
TYPE_INTENT = {"sale": "buy", "rent": "rent"}
# MCP status -> engine stage vocabulary
STATUS_STAGE = {"new": "new", "contacted": "contacted", "qualified": "qualified",
                "closed_won": "won", "closed_lost": "lost", "requires_manager": "contacted",
                "follow_up": "contacted"}


def load_leads(c):
    rows = c.call("list_leads", {"user_id": c.user_id, "limit": 200})
    leads = []
    for r in rows:
        leads.append({
            "id": r["phone"],
            "name": r.get("full_name"),
            "intent": TYPE_INTENT.get(r.get("transaction_type")),
            "budget": r.get("budget"),
            "stage": STATUS_STAGE.get(r.get("status"), "new"),
            "timeline": r.get("timeline"),          # not in MCP -> 0 pts
            "last_contact": r.get("last_interaction"),  # not in list_leads -> 0 pts
        })
    return leads


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", default=DEFAULT_USER)
    ap.add_argument("--write", action="store_true", help="save score summary to prod DB")
    args = ap.parse_args()

    c = MCPClient(user_id=args.user)
    print(f"MCP session {c.session[:8]}… user={c.user_id}")

    leads = load_leads(c)
    print(f"Loaded {len(leads)} leads from MCP")

    scored = sorted((engine.score_lead(l) for l in leads), key=lambda x: -x["score"])
    buckets = {"hot": [], "warm": [], "cold": []}
    for s in scored:
        buckets[s["bucket"]].append(s["id"])

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "scored.json").write_text(
        json.dumps({"scored": scored, "buckets": buckets}, ensure_ascii=False, indent=2),
        encoding="utf-8")

    print(f"\nScored {len(scored)} — hot {len(buckets['hot'])}, "
          f"warm {len(buckets['warm'])}, cold {len(buckets['cold'])}:")
    for s in scored:
        print(f"  {s['name']} ({s['id']}): {s['score']} ({s['bucket']}) {s['factors']}")
        if args.write:
            summary = (f"Lead score {s['score']}/100 ({s['bucket']}). "
                       f"Factors: {s['factors']}.")
            c.call("save_lead_ai_analysis",
                   {"phone": s["id"], "user_id": c.user_id, "ai_summary": summary})
            print(f"     [written] saved score summary")

    if not args.write:
        print("\n(dry-run — no DB writes. Re-run with --write to commit.)")


if __name__ == "__main__":
    main()
