# Integration Guide

ClaimGraph is designed to be imported by other Intelligent Contracts.

## Safe integration rule

A downstream contract should never treat an unresolved pair as compatible.

Use:

```python
if not graph.can_coexist(graph_id, protected_claim, candidate_claim):
    raise gl.vm.UserError("candidate has no resolved compatible relation")
```

`can_coexist` returns `False` for:

- `NONE`
- `INCONCLUSIVE`
- `CONTRADICTS`

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
- `permissionless=False`: only the graph creator or ClaimGraph owner may do so.

This lets the same primitive serve public registries and controlled rulebooks.
