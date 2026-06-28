#!/usr/bin/env python3
"""CMA deterministic engine. No LLM. Same inputs -> same numbers.

Reads a subject property and a set of comparables, applies the adjustment
table from _config/cma-rules.md, and produces a value range, price position,
and confidence score. The LLM narrates this output but never recomputes it.

Usage:
  python scripts/cma_analyze.py --subject SUBJECT.json --comps COMPS.json --out ANALYSIS.json
"""
import argparse
import json
import sys
from datetime import date, datetime

# Windows consoles default to cp1252 and choke on ₪ / Hebrew. Force UTF-8.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass

# Adjustment percentages (fractions) from _config/cma-rules.md
ADJ = {
    "floor_no_elevator": 0.005,
    "floor_with_elevator": 0.002,
    "balcony": 0.02,
    "parking": 0.03,
    "renovated": 0.05,
}


def b(x):
    return 1 if x else 0


def months_since(d):
    if not d:
        return 0
    try:
        then = datetime.strptime(d, "%Y-%m-%d").date()
    except ValueError:
        return 0
    today = date.today()
    return (today.year - then.year) * 12 + (today.month - then.month)


def comp_ppsqm(c):
    price = c.get("price") or c.get("sold_price") or c.get("asking_price")
    size = c.get("size_sqm")
    if not price or not size:
        return None
    return price / size


def adjust(subject, comp, trend_3mo_pct):
    """Return comp price/sqm adjusted toward the subject's features."""
    base = comp_ppsqm(comp)
    if base is None:
        return None
    frac = 0.0
    # floor
    floor_pct = ADJ["floor_with_elevator"] if subject.get("elevator") else ADJ["floor_no_elevator"]
    frac += (subject.get("floor", 0) - comp.get("floor", 0)) * floor_pct
    # binary features
    frac += (b(subject.get("balcony")) - b(comp.get("balcony"))) * ADJ["balcony"]
    frac += (b(subject.get("parking")) - b(comp.get("parking"))) * ADJ["parking"]
    frac += (b(subject.get("renovated")) - b(comp.get("renovated"))) * ADJ["renovated"]
    # time: sold more than 3 months ago -> apply neighborhood trend
    if comp.get("status") == "sold" and months_since(comp.get("sold_date")) > 3:
        frac += (trend_3mo_pct or 0) / 100.0
    return round(base * (1 + frac), 2)


def confidence(n_comps, source_disagreement):
    score = 50 + min(40, max(0, (n_comps - 3) * 20))
    if source_disagreement:
        score -= 15
    score = max(0, min(100, score))
    band = "High" if score >= 75 else "Medium" if score >= 50 else "Low"
    return score, band


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", required=True)
    ap.add_argument("--comps", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    subject = json.load(open(args.subject, encoding="utf-8"))
    comps_doc = json.load(open(args.comps, encoding="utf-8"))
    comps = comps_doc.get("comps", [])
    stats = comps_doc.get("neighborhood_stats", {})
    trend = stats.get("trend_3mo_pct", 0)
    disagreement = bool(comps_doc.get("source_disagreement", False))

    if not subject.get("size_sqm"):
        raise SystemExit("ERROR: subject missing size_sqm — fix stage 01.")
    if len(comps) < 3:
        raise SystemExit(f"ERROR: only {len(comps)} comps — need >=3 (insufficient data).")

    adjusted = []
    for c in comps:
        a = adjust(subject, c, trend)
        if a is not None:
            adjusted.append({"id": c.get("id"), "source": c.get("source"),
                             "raw_ppsqm": round(comp_ppsqm(c), 2), "adjusted_ppsqm": a})

    est_ppsqm = round(sum(x["adjusted_ppsqm"] for x in adjusted) / len(adjusted), 2)
    size = subject["size_sqm"]
    mid = round(est_ppsqm * size)
    low, high = round(mid * 0.95), round(mid * 1.05)

    asking = subject.get("asking_price")
    position = None
    if asking:
        delta = (asking - mid) / mid
        position = ("מעל השוק" if delta > 0.05 else
                    "מתחת לשוק" if delta < -0.05 else "מחיר שוק")

    score, band = confidence(len(adjusted), disagreement)

    out = {
        "subject_id": subject.get("id"),
        "estimated_price_per_sqm": est_ppsqm,
        "estimate_range": {"low": low, "mid": mid, "high": high},
        "asking_price": asking,
        "price_position": position,
        "confidence": {"score": score, "band": band, "source_disagreement": disagreement},
        "comps_used": adjusted,
        "neighborhood_stats": stats,
    }
    json.dump(out, open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"OK: estimate {low:,}–{high:,} ₪ (mid {mid:,}), "
          f"position={position}, confidence={band}({score})")


if __name__ == "__main__":
    main()
