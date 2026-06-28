#!/usr/bin/env python3
"""ICM Pipeline — Master orchestrator for MatchiICM workflows.

Zero-context bot entry point. Map all pipeline stages, run them in sequence or
individually, measure timing and reliability.

PIPELINE STAGES:
  1. match      — Lead→Property matching (mcp_match_run.py)
  2. score      — Lead scoring (mcp_lead_score_run.py)
  3. crm        — CRM state-machine validator (mcp_crm_run.py)
  4. brochure   — Property brochure PDF (mcp_brochure_run.py)
  5. fb-scan    — Facebook group scanner (mcp_facebook_scan_run.py)

Usage:
  py scripts/icm_pipeline.py                   # dry-run ALL stages
  py scripts/icm_pipeline.py --stage match     # run one stage
  py scripts/icm_pipeline.py --stage crm --write
  py scripts/icm_pipeline.py --list            # list stages + status
  py scripts/icm_pipeline.py --stage fb-scan --fb-group-url "https://..."
"""
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass

SCRIPT_DIR = Path(__file__).resolve().parent
PIPELINE_DIR = SCRIPT_DIR.parent

STAGES = {
    "match": {
        "script": "mcp_match_run.py",
        "description": "Lead→Property matching (match engine + MCP)",
        "produces": "phases/3-leads/matching/01-load/output/match-input.json",
        "writes_db": True,
    },
    "score": {
        "script": "mcp_lead_score_run.py",
        "description": "Lead scoring (deterministic factor-based)",
        "produces": "phases/3-leads/lead-scoring/01-load/output/scored.json",
        "writes_db": True,
    },
    "crm": {
        "script": "mcp_crm_run.py",
        "description": "CRM state-machine validation (new→contacted→...→won|lost)",
        "produces": "phases/3-leads/crm-update/02-transition/output/audit-log.json",
        "writes_db": True,
    },
    "brochure": {
        "script": "mcp_brochure_run.py",
        "description": "Museum-quality property brochure PDF",
        "produces": "phases/2-marketing/brochure/03-layout/output/brochure-mcp-*.pdf",
        "writes_db": False,
        "extra_args": ["--list"],  # default: list properties, not render
    },
    "fb-scan": {
        "script": "mcp_facebook_scan_run.py",
        "description": "Facebook group scanner (Apify → extract → dedupe → MCP)",
        "produces": "phases/3-leads/facebook-scan/output/scan-results.json",
        "writes_db": True,
        "needs_input": True,  # needs --fb-group-url or --raw-json
    },
}


def run_stage(name, info, write=False, extra_args=None):
    """Run a single pipeline stage. Returns (ok, elapsed, output)."""
    script_path = SCRIPT_DIR / info["script"]
    if not script_path.exists():
        return False, 0, f"SCRIPT NOT FOUND: {script_path}"

    cmd = [sys.executable, str(script_path)]
    if write and info.get("writes_db"):
        cmd.append("--write")
    if extra_args:
        cmd.extend(extra_args)

    print(f"\n{'─'*60}")
    print(f"STAGE: {name} — {info['description']}")
    print(f"  CMD: {' '.join(cmd)}")
    print(f"{'─'*60}")

    t0 = time.time()
    try:
        result = subprocess.run(
            cmd,
            cwd=str(PIPELINE_DIR),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=120,
        )
        elapsed = time.time() - t0
        output = result.stdout + result.stderr
        print(output)
        ok = result.returncode == 0
        return ok, elapsed, output
    except subprocess.TimeoutExpired:
        elapsed = time.time() - t0
        return False, elapsed, "TIMEOUT (120s)"
    except Exception as e:
        elapsed = time.time() - t0
        return False, elapsed, str(e)


def main():
    ap = argparse.ArgumentParser(description="ICM Pipeline Orchestrator")
    ap.add_argument("--stage", choices=list(STAGES) + ["all"],
                    default="all", help="Stage to run (default: all)")
    ap.add_argument("--write", action="store_true",
                    help="Commit DB writes (default: dry-run)")
    ap.add_argument("--list", action="store_true",
                    help="List stages and exit")
    ap.add_argument("--fb-group-url", help="Facebook group URL for fb-scan stage")
    ap.add_argument("--property-id", type=int, help="Property ID for brochure stage")
    ap.add_argument("--skip", nargs="*", choices=list(STAGES),
                    help="Stages to skip")
    args = ap.parse_args()

    if args.list:
        print("ICM Pipeline Stages:\n")
        for name, info in STAGES.items():
            db = "✎DB" if info.get("writes_db") else "RO"
            needs = " ⚡needs-input" if info.get("needs_input") else ""
            print(f"  {name:12s} {db:4s} {info['description']}{needs}")
            print(f"             → {info['produces']}")
        print(f"\nRun: py scripts/icm_pipeline.py [--stage <name>] [--write]")
        return

    print(f"ICM Pipeline — {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Mode: {'WRITE' if args.write else 'DRY-RUN'}")
    print(f"{'='*60}")

    skip = set(args.skip or [])
    stages_to_run = list(STAGES) if args.stage == "all" else [args.stage]

    results = {}
    total_t0 = time.time()

    for name in stages_to_run:
        if name in skip:
            print(f"\nSKIP: {name}")
            results[name] = {"ok": None, "elapsed": 0, "skipped": True}
            continue

        info = STAGES[name]
        extra = info.get("extra_args", [])[:]

        # Handle stage-specific args
        if name == "fb-scan" and args.fb_group_url:
            extra = ["--fb-group-url", args.fb_group_url]
        elif name == "fb-scan" and not args.fb_group_url:
            # Default: use mock data
            extra = ["--raw-json", str(PIPELINE_DIR / "_mock/fb-groups-raw.json")]
        if name == "brochure" and args.property_id:
            extra = ["--property-id", str(args.property_id)]

        if info.get("needs_input") and not extra:
            print(f"\nSKIP: {name} — needs input (--fb-group-url or --property-id)")
            results[name] = {"ok": None, "elapsed": 0, "skipped": True, "reason": "no input"}
            continue

        ok, elapsed, output = run_stage(name, info, args.write, extra)
        results[name] = {"ok": ok, "elapsed": elapsed, "output": output[-500:] if output else ""}

    # Summary
    total_elapsed = time.time() - total_t0
    print(f"\n{'='*60}")
    print(f"PIPELINE SUMMARY")
    print(f"{'='*60}")
    for name, r in results.items():
        if r.get("skipped"):
            reason = r.get("reason", "")
            print(f"  {name:12s} ⊘ SKIPPED {reason}")
        elif r["ok"]:
            print(f"  {name:12s} ✓ PASS ({r['elapsed']:.1f}s)")
        elif r["ok"] is False:
            print(f"  {name:12s} ✗ FAIL ({r['elapsed']:.1f}s)")
        else:
            print(f"  {name:12s} ? No result")

    print(f"\nTotal: {total_elapsed:.1f}s | Mode: {'WRITE' if args.write else 'DRY-RUN'}")

    # Save report
    report_path = SCRIPT_DIR / "pipeline-report.json"
    report_path.write_text(json.dumps({
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "mode": "write" if args.write else "dry-run",
        "total_elapsed_s": total_elapsed,
        "stages": {n: {"ok": r["ok"], "elapsed": r["elapsed"]}
                   for n, r in results.items()},
    }, indent=2), encoding="utf-8")
    print(f"\nReport: {report_path}")


if __name__ == "__main__":
    main()
