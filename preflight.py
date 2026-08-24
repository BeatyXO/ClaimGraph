from pathlib import Path

source = Path("contracts/claim_graph.py").read_text(encoding="utf-8")
tests = Path("tests/direct/test_claim_graph.py").read_text(encoding="utf-8")
docs = Path("README.md").read_text(encoding="utf-8") + Path("docs/CONSENSUS.md").read_text(encoding="utf-8")
checks = {
    "one canonical contract": source.count("class ClaimGraph(gl.Contract):") == 1,
    "consensus primitive present": "prompt_comparative" in source,
    "hostile output is fail-closed": "REL_INCONCLUSIVE" in source and "json.loads" in source,
    "state write after consensus": "self.records[self._proposal_key(proposal_id)]" in source,
    "bounded inputs": all(token in source for token in ("MAX_CLAIM", "MAX_CONTEXT", "MAX_RULES")),
    "pair replay protection": "relation already exists for claim pair" in source,
    "consumer fail-closed gate": "def can_coexist" in source and "REL_INCONCLUSIVE" in source,
    "lifecycle usability check": "def is_relation_usable" in source and "CLAIM_ACTIVE" in source,
    "finalized callback": 'on="finalized"' in source,
    "no deployer super-admin": "self.owner" not in source and "owner:" not in source,
    "pinned GenLayer dependency": source.startswith("# { \"Depends\": \"py-genlayer:"),
    "all terminal relations tested": all(value in tests for value in (
        "A_ENTAILS_B", "B_ENTAILS_A", "CONTRADICTS", "EQUIVALENT",
        "A_DEPENDS_ON_B", "B_DEPENDS_ON_A", "INDEPENDENT",
    )),
    "relation taxonomy documented": all(value in docs for value in (
        "A_ENTAILS_B", "CONTRADICTS", "EQUIVALENT", "INCONCLUSIVE",
    )),
    "no frontend directories": not any(Path(name).exists() for name in ("frontend", "app", "web")),
    "no environment file": not Path(".env").exists(),
}
for name, ok in checks.items():
    print(f"{'PASS' if ok else 'FAIL'}: {name}")
if not all(checks.values()):
    raise SystemExit(1)
print(f"preflight: {sum(checks.values())}/{len(checks)} passed")
