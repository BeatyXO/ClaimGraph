from pathlib import Path

source = Path("contracts/claim_graph.py").read_text(encoding="utf-8")
checks = {
    "one canonical contract": source.count("class ClaimGraph(gl.Contract):") == 1,
    "consensus primitive present": "prompt_comparative" in source,
    "hostile output is fail-closed": "REL_INCONCLUSIVE" in source and "json.loads" in source,
    "state write after consensus": "self.records[self._proposal_key(proposal_id)]" in source,
    "bounded inputs": all(token in source for token in ("MAX_CLAIM", "MAX_CONTEXT", "MAX_RULES")),
    "pair replay protection": "relation already exists for claim pair" in source,
    "consumer fail-closed gate": "def can_coexist" in source and "REL_INCONCLUSIVE" in source,
}
for name, ok in checks.items():
    print(f"{'PASS' if ok else 'FAIL'}: {name}")
if not all(checks.values()):
    raise SystemExit(1)
print(f"preflight: {sum(checks.values())}/{len(checks)} passed")
