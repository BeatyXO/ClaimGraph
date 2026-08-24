# ClaimGraph

**A reusable GenLayer Intelligent Contract for persistent semantic relationships between immutable claims.**

ClaimGraph lets other contracts register claims inside an explicit interpretation scope, ask GenLayer validators to classify the relationship between a pair, and reuse the resulting edge as on-chain state.

It is intentionally **contract-only**. There is no frontend.

## Why this primitive exists

Traditional contracts can compare hashes, numbers, addresses, and exact strings. They cannot reliably answer questions such as:

- Does Claim A logically entail Claim B?
- Do two claims contradict each other under the same conditions?
- Are two differently worded claims materially equivalent?
- Does one claim depend on another?
- Are the claims independent?

Those relationships matter in governance rulebooks, registries, policy systems, agent commitments, compliance workflows, research records, and any application that needs to know whether new semantic state conflicts with existing semantic state.

ClaimGraph turns that judgment into a bounded, reusable GenLayer consensus primitive.

## Relation taxonomy

For a canonical pair `(A, B)`, consensus returns exactly one of:

| Relation | Meaning |
|---|---|
| `A_ENTAILS_B` | If A holds as written, B necessarily follows in the graph scope |
| `B_ENTAILS_A` | Reverse entailment |
| `CONTRADICTS` | A and B cannot both hold under the same relevant conditions |
| `EQUIVALENT` | A and B make materially the same assertion |
| `A_DEPENDS_ON_B` | A materially presupposes B without simple entailment |
| `B_DEPENDS_ON_A` | Reverse dependency |
| `INDEPENDENT` | No material relationship above applies |
| `INCONCLUSIVE` | Scope/context is insufficient for a reliable classification |

`relation_between()` automatically inverts directional relations when queried in reverse order.

## Why this is GenLayer-native

The semantic classification is performed inside a non-deterministic LLM block and finalized through `gl.eq_principle.prompt_comparative`.

The Equivalence Principle is intentionally narrow: validators must agree on the **relation enum**, while explanation wording may differ. The validator criteria explicitly distinguish contradiction from mere difference, necessary entailment from likelihood, equivalence from overlap, and dependency from entailment.

An invalid or malformed model response fails closed to `INCONCLUSIVE`.

## State model

ClaimGraph stores four layers of state:

1. **Graphs** — scope, interpretation rules, permission model, callback.
2. **Claims** — immutable text/context plus lifecycle status.
3. **Relation proposals** — consensus lifecycle and reasoning.
4. **Pair edges** — canonical resolved relation for a claim pair.

Claims are immutable after registration. A claim can be withdrawn, but its historical text is not rewritten.

A canonical pair lock prevents contradictory duplicate decisions for the same immutable pair. Inconclusive proposals are retried rather than replaced.

## Consumer-safe views

Downstream contracts can call:

- `relation_between(graph_id, claim_x, claim_y)`
- `has_resolved_relation(graph_id, claim_x, claim_y)`
- `conflicts(graph_id, claim_x, claim_y)`
- `can_coexist(graph_id, claim_x, claim_y)`

`is_relation_usable(graph_id, claim_x, claim_y)` is the lifecycle-aware consumer view. `relation_between()` and `has_resolved_relation()` preserve historical graph truth for auditability, while `is_relation_usable()` and `can_coexist()` fail closed when the graph is inactive or either claim is withdrawn. Relation callbacks request finalized delivery; callback failure does not corrupt the stored edge.

`can_coexist` is fail-closed: unresolved and inconclusive pairs return `False`.

See `examples/semantic_rulebook_consumer.py` for a minimal importer that refuses to adopt a candidate rule unless ClaimGraph has a resolved non-conflicting relation against a protected claim.

## Contract surface

### Writes

```text
create_graph(name, scope, interpretation_rules, permissionless, callback)
register_claim(graph_id, text, context)
open_relation(graph_id, claim_x, claim_y)
resolve_relation(proposal_id)
retry_inconclusive(proposal_id)
withdraw_claim(claim_id)
deactivate_graph(graph_id)
```

### Views

```text
graph_of(graph_id)
claim_of(claim_id)
proposal_of(proposal_id)
relation_between(graph_id, claim_x, claim_y)
has_resolved_relation(graph_id, claim_x, claim_y)
conflicts(graph_id, claim_x, claim_y)
can_coexist(graph_id, claim_x, claim_y)
stats()
```

## Example

Create a graph with a narrow scope:

```text
Scope:
Protocol fee rules for the same network and active policy period.

Interpretation rules:
Interpret claims literally. Material numeric limits and explicit conditions control.
```

Register:

```text
A: Protocol fees must never exceed 2%.
B: Protocol fees may be set to 3.5% for six months.
```

Open and resolve the pair. If validators classify it as `CONTRADICTS`, the edge persists and a consumer can reject B through `can_coexist`.

This differs from a truth oracle: ClaimGraph does **not** decide whether A or B is factually true. It decides the semantic relationship between immutable assertions.

## Repository layout

```text
contracts/
  claim_graph.py
examples/
  semantic_rulebook_consumer.py
tests/
  direct/
    conftest.py
    test_claim_graph.py
docs/
  CONSENSUS.md
  INTEGRATION.md
gltest.config.yaml
README.md
```

## Testing

The direct test suite covers:

- graph permissions and lifecycle
- claim registration
- canonical pair locking
- contradiction persistence
- directional relation inversion
- fail-closed malformed LLM output
- inconclusive retry
- withdrawal behavior
- consumer-safe unknown-pair behavior
- graph deactivation
- edge/stat accounting
- withdrawal invalidation while preserving historical relation data
- deployer isolation and every terminal relation enum

Run with the GenLayer direct test tooling used by Studio/`gltest`:

```bash
pytest tests/direct -q
```

## Deployment

Canonical StudioNet deployment: `0xe0E09098A859734A9b75a337FF91376B69EEa3eD`.

Deployment transaction: `0x57e2bf4a773f82da7ed790f821e39f0accf099fb96e99f5cfc4be66bd621c9f4` (`ACCEPTED`, `MAJORITY_AGREE`). The source commit was `1b720e1b0fb8f8a02dbd19a50642a5497f02b660`. Live proof includes `EQUIVALENT`, `CONTRADICTS`, consumer adoption/rejection, and post-withdrawal `can_coexist == false`; see `docs/DEPLOYMENT.md` for all hashes.

Deploy `contracts/claim_graph.py` to GenLayer Studio/StudioNet. The constructor takes no arguments.

The contract pins the current documented `py-genlayer` dependency hash in its first line.

## Design boundary

ClaimGraph is deliberately **not**:

- a truth-verification oracle
- a reputation score
- a generic content moderator
- a frontend application
- a thin "AI decides X" wrapper

Its reusable output is a persistent, canonical semantic edge that changes what downstream contracts can safely import or execute.
