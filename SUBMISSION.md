# GenLayer submission notes

- Category: standalone Intelligent Contract
- Title: ClaimGraph
- Purpose: persistent, consensus-backed semantic relationships between immutable claims inside an explicit interpretation scope.
- Repository: https://github.com/BeatyXO/ClaimGraph
- Canonical Studionet address: `0xe0E09098A859734A9b75a337FF91376B69EEa3eD`
- Deployment transaction: `0x57e2bf4a773f82da7ed790f821e39f0accf099fb96e99f5cfc4be66bd621c9f4` (`ACCEPTED`, `MAJORITY_AGREE`)

Consensus is required because entailment, contradiction, equivalence, and dependency are semantic judgments that deterministic EVM-style code cannot derive from differently worded claims. Validators independently compare the substantive relation through `prompt_comparative`; only the bounded relation enum becomes state. Deterministic code owns bounds, permissions, pair locks, lifecycle, parsing, callbacks, and fail-closed consumer gates.

This is not a thin LLM wrapper: claims and graph policy persist on-chain, consensus is load-bearing, and downstream contracts consume stable relation and compatibility views. Malformed or disputed reasoning remains `INCONCLUSIVE` and is not consumable.

Validation evidence: preflight 15/15, Direct Mode 26/26, GenVM lint passed for the contract and consumer example, and live StudioNet evidence covers deployment, `CONTRADICTS`, `EQUIVALENT`, consumer adoption/rejection, and withdrawal invalidation. Deployment source is commit `1b720e1b0fb8f8a02dbd19a50642a5497f02b660`; retrieved-source parity is SHA-256 PASS.
