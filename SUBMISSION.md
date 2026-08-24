# GenLayer submission notes

- Category: standalone Intelligent Contract
- Title: ClaimGraph
- Purpose: persistent, consensus-backed semantic relationships between immutable claims inside an explicit interpretation scope.
- Repository: https://github.com/BeatyXO/ClaimGraph
- Canonical Studionet address: `0xFcE7CE9a24AfAC0De711679eb897cc35B45a7e7d`
- Deployment transaction: `0xa009a2d6b0f74d64a2e58c2d709d5505e9e31f2307017b0f2c8cc8984ab96c57` (`ACCEPTED`, `MAJORITY_AGREE`)

Consensus is required because entailment, contradiction, equivalence, and dependency are semantic judgments that deterministic EVM-style code cannot derive from differently worded claims. Validators independently compare the substantive relation through `prompt_comparative`; only the bounded relation enum becomes state. Deterministic code owns bounds, permissions, pair locks, lifecycle, parsing, callbacks, and fail-closed consumer gates.

This is not a thin LLM wrapper: claims and graph policy persist on-chain, consensus is load-bearing, and downstream contracts consume stable relation and compatibility views. Malformed or disputed reasoning remains `INCONCLUSIVE` and is not consumable.

Validation evidence: preflight 15/15, Direct Mode 25/25, GenVM lint passed for the contract and consumer example, and live StudioNet evidence covers deployment, graph creation, two claims, semantic resolution to `EQUIVALENT`, and withdrawal invalidation (`is_relation_usable=false`, `can_coexist=false` while historical relation data remains readable). Deployment source is commit `8c984a48af1d79f534c5beb1b887313716f367b8`.
