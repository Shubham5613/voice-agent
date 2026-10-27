"""Run simulated-customer scenarios against the deployed agent (text only, no voice minutes).

Usage: python tests/run_simulations.py [scenario_id_prefix ...] [--workers 4]
Writes tests/results/<id>.md transcripts and tests/results/summary.md
"""
import os, sys, json, pathlib, concurrent.futures as cf, time
import httpx
from dotenv import load_dotenv

ROOT = pathlib.Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")
H = {"xi-api-key": os.environ["ELEVENLABS_API_KEY"]}
AID = os.environ.get("ELEVEN_AGENT_ID") or json.loads((ROOT / "agent" / ".agent_state.json").read_text())["agent_id"]  # ELEVEN_AGENT_ID=... to test the public demo agent
SPEC = json.loads((ROOT / "tests" / "scenarios.json").read_text())
OUT = ROOT / "tests" / "results"; OUT.mkdir(exist_ok=True)


def run(sc: dict) -> dict:
    body = {"simulation_specification": {
                "simulated_user_config": {"prompt": {"prompt": sc["persona"] + "\n\n" + SPEC["_common_user_rules"]}},
                "dynamic_variables": SPEC["_leads"][sc["lead"]] | {"call_ref": f"sim-{sc['id']}-{int(time.time()*1000)}", "system__conversation_id": f"sim-{sc['id']}-{int(time.time()*1000)}"},  # tools scope idempotency by conversation id; sims must supply one
                "tool_mock_config": SPEC.get("_tool_mocks", {})},
            "new_turns_limit": 40}
    t0 = time.time()
    try:
        r = httpx.post(f"https://api.elevenlabs.io/v1/convai/agents/{AID}/simulate-conversation", headers=H, json=body, timeout=600)
        if r.status_code == 422 and "tool_mock_config" in r.text:  # older schema: retry without mocks
            body["simulation_specification"].pop("tool_mock_config"); r = httpx.post(r.url, headers=H, json=body, timeout=600)
        r.raise_for_status(); d = r.json()
    except Exception as e:
        return {"id": sc["id"], "error": (getattr(e, "response", None) and e.response.text[:300]) or str(e)[:300]}
    turns = d.get("simulated_conversation", [])
    an = d.get("analysis", {}) or {}
    evals = {k: (v.get("result") if isinstance(v, dict) else v) for k, v in (an.get("evaluation_criteria_results") or {}).items()}
    coll = {k: (v.get("value") if isinstance(v, dict) else v) for k, v in (an.get("data_collection_results") or {}).items()}
    tools = [c.get("tool_name") for t in turns for c in (t.get("tool_calls") or [])]
    agent_turns = [t for t in turns if t.get("role") == "agent" and (t.get("message") or "").strip()]
    long_turns = [t["message"] for t in agent_turns if sum(t["message"].count(x) for x in ".?!") > 3]
    fails = [c for c in sc.get("must_pass", []) if evals.get(c) == "failure"]
    missing = [t for t in sc.get("must_call", []) if t not in tools]
    forbidden = [t for t in sc.get("must_not_call", []) if t in tools]
    ok = not fails and not missing and not forbidden
    # transcript
    lines = [f"# {sc['id']}  —  {'PASS' if ok else 'FAIL'}", "", f"Persona: {sc['persona']}", "", "## Transcript"]
    for t in turns:
        msg = (t.get("message") or "").strip(); tc = [c.get("tool_name") for c in (t.get("tool_calls") or [])]
        if msg or tc:
            lines.append(f"- **{t.get('role')}**: {msg}" + (f"  `tools: {tc}`" if tc else ""))
    lines += ["", "## Evaluation", "```", json.dumps(evals, indent=1), "```", "## Collected", "```", json.dumps(coll, indent=1), "```",
              f"Tools called: {tools}", f"Failed criteria: {fails}", f"Missing tools: {missing}", f"Forbidden tools called: {forbidden}",
              f"Agent turns over 3 sentences: {len(long_turns)}", f"Duration: {time.time()-t0:.0f}s"]
    (OUT / f"{sc['id']}.md").write_text("\n".join(lines))
    return {"id": sc["id"], "ok": ok, "fails": fails, "missing": missing, "forbidden": forbidden, "tools": tools,
            "outcome": coll.get("outcome"), "hung_up_early": coll.get("hung_up_early"), "user_turns": sum(1 for t in turns if t.get("role") == "user"),
            "long_turns": len(long_turns), "evals": evals}


def main():
    argv = sys.argv[1:]; workers = 4
    if "--workers" in argv:
        i = argv.index("--workers"); workers = int(argv[i + 1]); argv = argv[:i] + argv[i + 2:]
    repeat = 1
    if "--repeat" in argv:
        i = argv.index("--repeat"); repeat = int(argv[i + 1]); argv = argv[:i] + argv[i + 2:]
    args = [a for a in argv if not a.startswith("--")]
    scs = [s for s in SPEC["scenarios"] if not args or any(s["id"].startswith(a) for a in args)]
    scs = [dict(s, id=f"{s['id']}{'' if repeat == 1 else f'__r{k+1}'}") for s in scs for k in range(repeat)]
    print(f"running {len(scs)} scenarios against {AID} with {workers} workers…")
    with cf.ThreadPoolExecutor(workers) as ex:
        results = list(ex.map(run, scs))
    rows = ["| scenario | result | outcome | user turns | long turns | failed criteria | missing tools | forbidden tools |", "|---|---|---|---|---|---|---|---|"]
    for r in results:
        if "error" in r:
            rows.append(f"| {r['id']} | ERROR | {r['error']} | | | | | |"); continue
        rows.append(f"| {r['id']} | {'PASS' if r['ok'] else 'FAIL'} | {r['outcome']} | {r['user_turns']} | {r['long_turns']} | {', '.join(r['fails'])} | {', '.join(r['missing'])} | {', '.join(r['forbidden'])} |")
    crit = {}
    for r in results:
        for k, v in (r.get("evals") or {}).items():
            crit.setdefault(k, {"success": 0, "failure": 0, "unknown": 0})[v or "unknown"] += 1
    rows += ["", "## Criteria across all scenarios", "| criterion | success | failure | n/a |", "|---|---|---|---|"]
    rows += [f"| {k} | {v['success']} | {v['failure']} | {v['unknown']} |" for k, v in crit.items()]
    base = {}
    for r in results:
        b = r["id"].split("__r")[0]; base.setdefault(b, []).append(bool(r.get("ok")))
    if any(len(v) > 1 for v in base.values()):
        rows += ["", "## Pass rate per scenario", "| scenario | passed | runs |", "|---|---|---|"]
        rows += [f"| {k} | {sum(v)} | {len(v)} |" for k, v in base.items()]
    passed = sum(1 for r in results if r.get("ok"))
    summary = f"# Simulation summary — {passed}/{len(results)} passed\n\n" + "\n".join(rows)
    (OUT / "summary.md").write_text(summary); print(summary)


if __name__ == "__main__":
    main()
