# GenLayer submission notes

- Category: standalone Intelligent Contract
- Title: ClaimGraph
- Purpose: persistent, consensus-backed semantic relationships between immutable claims inside an explicit interpretation scope.
- Repository: https://github.com/BeatyXO/ClaimGraph
- Canonical Studionet address: not deployed/verified in this audit
- Deployment transaction: not available

Consensus is required because entailment, contradiction, equivalence, and dependency are semantic judgments that deterministic EVM-style code cannot derive from differently worded claims. Validators independently compare the substantive relation through `prompt_comparative`; only the bounded relation enum becomes state. Deterministic code owns bounds, permissions, pair locks, lifecycle, parsing, callbacks, and fail-closed consumer gates.

This is not a thin LLM wrapper: claims and graph policy persist on-chain, consensus is load-bearing, and downstream contracts consume stable relation and compatibility views. Malformed or disputed reasoning remains `INCONCLUSIVE` and is not consumable.

Validation evidence: Direct Mode 16/16 passed at the audited starting commit. A Studionet deployment and live runtime proof remain to be supplied before claiming final submission readiness.
