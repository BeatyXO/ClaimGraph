# Security model

ClaimGraph protects the integrity of semantic relationship records and the downstream decisions that consume them. It does not protect an external asset or establish that a claim is true.

## Trust boundaries

- Claim authors, graph creators, and callback contracts are untrusted input.
- Claim text, context, scope, and interpretation rules are data; prompts explicitly instruct validators not to follow instructions embedded in that data.
- The leader result is untrusted until the Equivalence Principle accepts it. Malformed or unknown relations become `INCONCLUSIVE`.
- Validators are assumed to execute the same comparison independently. A malicious validator majority remains an ecosystem-level limitation.

## Safety properties

State writes, pair canonicalisation, access control, bounds, replay protection, and compatibility gates are deterministic. A pair is written once, terminal relations cannot be replayed, and inconclusive or withdrawn results never make `can_coexist()` true. Semantic callbacks request `finalized` delivery; callback failure does not undo the accepted edge or create a privileged bypass. There is no contract-level deployer super-admin.

Claim text and model output are bounded. The contract does not execute URLs or treat model prose as a settlement instruction. Consumers must use the stable enum/boolean views and must fail closed on `NONE` or `INCONCLUSIVE`.

## Limitations

Semantic classification is not factual verification. Ambiguous or adversarial claims can be classified incorrectly despite consensus. Consumers must choose a sufficiently narrow graph scope and interpretation policy, and should not use ClaimGraph as a substitute for authorization, identity, or legal adjudication.
