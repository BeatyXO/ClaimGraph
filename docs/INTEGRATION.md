# Integration Guide

ClaimGraph is designed to be imported by other Intelligent Contracts.

## Safe integration rule

A downstream contract should never treat an unresolved pair as compatible.

The repository integration suite runs the official `genlayer` CLI against StudioNet when explicitly configured with `CLAIMGRAPH_STUDIONET_LIVE=1` and `CLAIMGRAPH_LIVE_CONTRACT`. It performs real RPC reads and never mocks LLM output.

Use:

```python
if not graph.can_coexist(graph_id, protected_claim, candidate_claim):
    raise gl.vm.UserError("candidate has no resolved compatible relation")
```

`is_relation_usable` is the lifecycle-aware view. It returns `False` when the graph is inactive, either claim is withdrawn, or the pair is unresolved. `can_coexist` calls it first and therefore returns `False` for:

- `NONE`
- `INCONCLUSIVE`
- `CONTRADICTS`

`has_resolved_relation` and `relation_between` preserve historical graph truth after withdrawal. Consumers must use `is_relation_usable` or `can_coexist` for current decisions. `conflicts` remains historical: a withdrawn contradictory pair is still recorded as conflicting, while it is not currently usable.

and `True` for resolved non-conflicting semantic relations.

## When to use `relation_between`

Use the raw relation when the consumer needs more precision than a boolean gate. For example:

- governance engines may treat `EQUIVALENT` as a duplicate,
- dependency managers may react to `A_DEPENDS_ON_B`,
- rule systems may reject `CONTRADICTS`,
- registries may store entailment links.

## Callback

Each graph may optionally set a callback contract address. On a terminal relation, ClaimGraph attempts:

```text
on_claim_relation(graph_id, claim_a, claim_b, relation)
```

Callback failure does not revert the semantic decision. The proposal records whether the callback was sent successfully.

## Permission model

A graph can be:

- `permissionless=True`: anyone may register claims and open relation proposals.
- `permissionless=False`: only the graph creator may do so. There is no deployer super-admin.

This lets the same primitive serve public registries and controlled rulebooks.
