#!/usr/bin/env python3
"""ICM CRM state-machine validator wired to prod MCP.

Loads leads from MCP, loads transition requests from mock (real later: chat intent),
validates each transition against adjacency matrix from crm-rules.md,
and (with --write) applies valid transitions via update_lead_stage.

Usage:
  py scripts/mcp_crm_run.py                      # dry-run, validate only
  py scripts/mcp_crm_run.py --write              # apply valid transitions
  py scripts/mcp_crm_run.py --transitions INPUT  # custom transition requests JSON
"""
import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mcp_client import MCPClient, DEFAULT_USER

try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass

SCRIPT_DIR = Path(__file__).resolve().parent
MOCK_DIR = SCRIPT_DIR.parent / "_mock"
CONFIG_DIR = SCRIPT_DIR.parent / "_config"
OUT_DIR = SCRIPT_DIR.parent / "phases/3-leads/crm-update/02-transition/output"

# Adjacency matrix from _config/crm-rules.md
# new → contacted, lost
# contacted → qualified, lost
# qualified → won, lost
# won, lost → terminal (no transition out)
ALLOWED = {
    "new":       {"contacted", "lost"},
    "contacted": {"qualified", "lost"},
    "qualified": {"won", "lost"},
    "won":       set(),   # terminal
    "lost":      set(),   # terminal
}

TERMINAL = {"won", "lost"}


def validate_transition(current_stage, target_stage):
    """Return (legal: bool, reason: str)."""
    if current_stage == target_stage:
        return False, f"no-op: already {current_stage}"
    if current_stage in TERMINAL:
        return False, f"terminal: {current_stage} cannot transition"
    allowed = ALLOWED.get(current_stage, set())
    if target_stage not in allowed:
        return False, f"illegal: {current_stage}→{target_stage}"
    return True, "ok"


def load_transition_requests(path=None):
    """Load transition requests from mock JSON (or custom path)."""
    src = Path(path) if path else MOCK_DIR / "crm-requests.json"
    if not src.exists():
        print(f"No transition requests at {src}")
        return []
    data = json.loads(src.read_text(encoding="utf-8"))
    return data.get("transitions", [])


def load_leads_with_stages(c):
    """Load all leads and their current CRM stages from MCP."""
    rows = c.call("list_leads", {"user_id": c.user_id, "limit": 200})
    leads = []
    for r in rows:
        phone = r.get("phone", "")
        try:
            stage_info = c.call("get_lead_stage", {"phone": phone, "user_id": c.user_id})
            stage = stage_info.get("stage", "new") if isinstance(stage_info, dict) else "new"
        except Exception:
            stage = "new"  # fallback if get_lead_stage fails
        leads.append({
            "phone": phone,
            "name": r.get("full_name", ""),
            "stage": stage,
        })
    return leads


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", default=DEFAULT_USER)
    ap.add_argument("--write", action="store_true", help="apply valid transitions to prod DB")
    ap.add_argument("--transitions", help="path to custom transition requests JSON")
    args = ap.parse_args()

    t0 = time.time()
    c = MCPClient(user_id=args.user)
    print(f"MCP session {c.session[:8]}… user={c.user_id}")

    # 1. Load leads
    leads = load_leads_with_stages(c)
    print(f"\nLoaded {len(leads)} leads:")
    by_phone = {}
    for l in leads:
        by_phone[l["phone"]] = l
        print(f"  {l['name']} ({l['phone']}): {l['stage']}")

    # 2. Load transition requests
    requests = load_transition_requests(args.transitions)
    print(f"\n{len(requests)} transition request(s):")
    for req in requests:
        print(f"  {req['lead_id']} → {req['to']}")

    # 3. Validate + apply
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    audit = []
    results = {"valid": 0, "applied": 0, "rejected": 0, "skipped": 0}

    print(f"\nValidating…")
    for req in requests:
        lid = req["lead_id"]
        target = req["to"]

        # Map mock lead_id (e.g. "L-1") to MCP phone — use request directly
        # In MCP, leads are keyed by phone. Mock uses "L-1" etc.
        # For now: try to find lead by matching lead_id as phone or by index
        lead = by_phone.get(lid)  # try direct phone match first
        if not lead:
            # Try index-based: L-1 → first lead, L-2 → second, etc.
            m = __import__('re').match(r"L-(\d+)", lid)
            if m:
                idx = int(m.group(1)) - 1
                if 0 <= idx < len(leads):
                    lead = leads[idx]

        if not lead:
            print(f"  {lid} → {target}: SKIP (lead not found)")
            results["skipped"] += 1
            audit.append({"lead_id": lid, "from": "?", "to": target,
                          "legal": False, "applied": False,
                          "reason": "lead not found", "at": time.strftime("%Y-%m-%dT%H:%M:%SZ")})
            continue

        current = lead["stage"]
        legal, reason = validate_transition(current, target)
        entry = {
            "lead_id": lid,
            "phone": lead["phone"],
            "name": lead["name"],
            "from": current,
            "to": target,
            "legal": legal,
            "applied": False,
            "reason": reason,
            "at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }

        if not legal:
            print(f"  {lid} ({lead['name']}): {current}→{target} REJECTED — {reason}")
            results["rejected"] += 1
            audit.append(entry)
            continue

        print(f"  {lid} ({lead['name']}): {current}→{target} VALID", end="")
        results["valid"] += 1

        if args.write:
            try:
                c.call("update_lead_stage", {
                    "phone": lead["phone"],
                    "user_id": c.user_id,
                    "stage": target,
                })
                entry["applied"] = True
                print(" [written]")
                results["applied"] += 1
            except Exception as e:
                entry["reason"] = f"write error: {e}"
                print(f" [FAIL: {e}]")
                results["rejected"] += 1
        else:
            print("")

        audit.append(entry)

    # 4. Save audit log
    audit_path = OUT_DIR / "audit-log.json"
    audit_path.write_text(json.dumps({
        "stats": results,
        "entries": audit,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nAudit: {audit_path}")

    elapsed = time.time() - t0
    print(f"\n{'='*50}")
    print(f"CRM Run: {results['valid']} valid, {results['applied']} applied, "
          f"{results['rejected']} rejected, {results['skipped']} skipped")
    print(f"Elapsed: {elapsed:.1f}s")

    if not args.write:
        print("(dry-run — no DB writes. Re-run with --write to commit.)")


if __name__ == "__main__":
    main()
