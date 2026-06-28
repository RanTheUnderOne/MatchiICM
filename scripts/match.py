#!/usr/bin/env python3
"""Lead<->Property matching deterministic engine. No LLM. Same inputs -> same fit.

Applies hard constraints + soft factor weights from _config/match-rules.md to
every (lead, property) pair. Hard-blocked pairs get no soft score. Output carries
an explainable factor breakdown so any fit number reproduces by hand.

Usage:
  py scripts/match.py --input MATCH-INPUT.json --out MATCHES.json
  (MATCH-INPUT.json = {"leads":[...], "properties":[...]})
"""
import argparse
import json
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass

# buy lead wants a sale listing; rent lead wants a rent listing
INTENT_TYPE = {"buy": "sale", "rent": "rent"}


def hard_block(lead, prop):
    if INTENT_TYPE.get(lead.get("intent")) != prop.get("transaction_type"):
        return f"intent {lead.get('intent')} != type {prop.get('transaction_type')}"
    if lead.get("city") != prop.get("city"):
        return f"city {lead.get('city')} != {prop.get('city')}"
    if abs((lead.get("rooms") or 0) - (prop.get("rooms") or 0)) > 1:
        return f"rooms {lead.get('rooms')} vs {prop.get('rooms')} (>1 apart)"
    return None


def soft_factors(lead, prop):
    budget = lead.get("budget") or 0
    price = prop.get("asking_price") or 0
    if price <= budget:
        budget_pts = 40
    elif price <= budget * 1.10:
        budget_pts = 20
    else:
        budget_pts = 0

    nb_pts = 30 if lead.get("neighborhood") == prop.get("neighborhood") else 0
    rooms_pts = 20 if lead.get("rooms") == prop.get("rooms") else 10

    dom = prop.get("days_on_market", 999)
    dom_pts = 10 if dom <= 14 else 5 if dom <= 30 else 0

    return {"budget": budget_pts, "neighborhood": nb_pts,
            "rooms_exact": rooms_pts, "days_on_market": dom_pts}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    doc = json.load(open(args.input, encoding="utf-8"))
    leads = doc.get("leads", [])
    props = doc.get("properties", [])
    if not leads or not props:
        raise SystemExit("ERROR: need both leads and properties in --input.")

    matches = []
    for lead in leads:
        for prop in props:
            reason = hard_block(lead, prop)
            if reason:
                matches.append({"lead_id": lead.get("id"), "property_id": prop.get("id"),
                                "blocked": True, "blocked_reason": reason})
                continue
            f = soft_factors(lead, prop)
            matches.append({"lead_id": lead.get("id"), "property_id": prop.get("id"),
                            "blocked": False, "fit": sum(f.values()), "factors": f,
                            "asking_price": prop.get("asking_price")})

    # rank per lead: top fit, tie-break lower asking_price
    by_lead = {}
    for lead in leads:
        ms = [m for m in matches if m["lead_id"] == lead.get("id") and not m["blocked"]]
        ms.sort(key=lambda m: (-m["fit"], m.get("asking_price") or 0))
        by_lead[lead.get("id")] = ms[:3]

    out = {"matches": matches, "top_by_lead": by_lead,
           "rules": "_config/match-rules.md"}
    json.dump(out, open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    n_ok = sum(1 for m in matches if not m["blocked"])
    n_blocked = sum(1 for m in matches if m["blocked"])
    print(f"OK: {len(matches)} pairs — {n_ok} scored, {n_blocked} blocked")
    for lid, ms in by_lead.items():
        if ms:
            top = ms[0]
            print(f"  {lid} -> {top['property_id']} fit {top['fit']} {top['factors']}")
        else:
            print(f"  {lid} -> no match")


if __name__ == "__main__":
    main()
