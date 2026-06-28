#!/usr/bin/env python3
"""Lead scoring deterministic engine. No LLM. Same inputs -> same numbers.

Reads leads and applies the factor table from _config/lead-rules.md to produce
a 0-100 score per lead, an explainable factor breakdown, and a bucket
(hot/warm/cold). The LLM narrates this output but never recomputes it.

Usage:
  py scripts/lead_score.py --leads LEADS.json --out SCORED.json
  (LEADS.json = {"leads":[...]} or a bare [...] array)
"""
import argparse
import json
import sys
from datetime import date, datetime

# Windows consoles default to cp1252 and choke on Hebrew. Force UTF-8.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass

# Factor weights from _config/lead-rules.md
TIMELINE = {"0-1mo": 30, "0-3mo": 25, "1-3mo": 20, "3-6mo": 10, "6mo+": 0, ">6mo": 0}
INTENT = {"buy": 20, "rent": 10}
STAGE = {"qualified": 10, "contacted": 5, "new": 2, "won": 0, "lost": 0}
BUDGET_RANGE = {"buy": (800_000, 5_000_000), "rent": (2_500, 15_000)}
HOT, WARM = 70, 40


def days_since(d):
    if not d:
        return 9999
    try:
        then = datetime.strptime(d, "%Y-%m-%d").date()
    except ValueError:
        return 9999
    return (date.today() - then).days


def score_budget(lead):
    b = lead.get("budget")
    if not b:
        return 0
    lo, hi = BUDGET_RANGE.get(lead.get("intent"), (None, None))
    if lo is None:
        return 10  # present but range unknown
    return 20 if lo <= b <= hi else 10


def score_recency(lead):
    d = days_since(lead.get("last_contact"))
    return 20 if d <= 7 else 10 if d <= 30 else 0


def score_lead(lead):
    f = {
        "timeline": TIMELINE.get(lead.get("timeline"), 0),
        "intent": INTENT.get(lead.get("intent"), 0),
        "budget": score_budget(lead),
        "recency": score_recency(lead),
        "stage": STAGE.get(lead.get("stage"), 0),
    }
    total = min(100, sum(f.values()))
    bucket = "hot" if total >= HOT else "warm" if total >= WARM else "cold"
    return {"id": lead.get("id"), "name": lead.get("name"),
            "score": total, "bucket": bucket, "factors": f}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--leads", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    doc = json.load(open(args.leads, encoding="utf-8"))
    leads = doc.get("leads", doc) if isinstance(doc, dict) else doc
    if not leads:
        raise SystemExit("ERROR: no leads to score.")

    scored = sorted((score_lead(l) for l in leads), key=lambda x: -x["score"])
    buckets = {"hot": [], "warm": [], "cold": []}
    for s in scored:
        buckets[s["bucket"]].append(s["id"])

    out = {"scored": scored, "buckets": buckets,
           "rules": "_config/lead-rules.md"}
    json.dump(out, open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"OK: scored {len(scored)} leads — "
          f"hot {len(buckets['hot'])}, warm {len(buckets['warm'])}, cold {len(buckets['cold'])}")
    for s in scored:
        print(f"  {s['id']} {s['name']}: {s['score']} ({s['bucket']}) {s['factors']}")


if __name__ == "__main__":
    main()
