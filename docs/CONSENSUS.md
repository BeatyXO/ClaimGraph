# Consensus Design

## Consensus question

For two immutable claims inside one graph scope:

> What is the strongest justified semantic relationship between Claim A and Claim B?

The contract does **not** ask whether either claim is factually true.

## Why comparative equivalence

Relationship classification is bounded but semantic. Different validators may explain the same relationship differently, so strict string equality would be inappropriate.

`prompt_comparative` lets validators independently classify the pair and compare the substantive result.

The equivalence criteria require agreement on the relation enum and deliberately ignore stylistic differences in the reason.

## Failure policy

The model is instructed to use `INCONCLUSIVE` when:

- key terms are undefined,
- relevant timeframes differ,
- graph scope does not line up,
- context is insufficient,
- conditions are too ambiguous to compare safely.

Malformed output is normalized to `INCONCLUSIVE`.

Consumers therefore fail closed: `can_coexist` returns `False` for `NONE` and `INCONCLUSIVE`.

## Pair canonicalization

Claims are immutable. Each graph stores at most one proposal lifecycle for a canonical unordered pair `(min_id, max_id)`.

Directional outcomes are encoded relative to that canonical pair:

- `A_ENTAILS_B`
- `B_ENTAILS_A`
- `A_DEPENDS_ON_B`
- `B_DEPENDS_ON_A`

Reverse queries invert only those directional enums. Symmetric relations remain unchanged.

This avoids duplicate or contradictory graph edges caused solely by querying the same pair in reverse order.
