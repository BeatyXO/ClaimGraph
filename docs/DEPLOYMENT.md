# Deployment evidence

## Canonical deployment

- Date: 2026-08-24
- Network: StudioNet
- Source commit: `8c984a48af1d79f534c5beb1b887313716f367b8`
- Deployment account: fresh local encrypted account; public deployer address `0x46f9835B475c789229EDfe1fe73A70fD54215d6F`
- Contract address: `0xFcE7CE9a24AfAC0De711679eb897cc35B45a7e7d`
- Deployment transaction: `0xa009a2d6b0f74d64a2e58c2d709d5505e9e31f2307017b0f2c8cc8984ab96c57`
- Lifecycle: `ACCEPTED`
- Consensus result: `MAJORITY_AGREE`, one round, 3 agreeing validator votes observed before quorum cancellation of idle validators

The deployment was made from the exact current `contracts/claim_graph.py` at the source commit above. The contract source was not changed after deployment.

## Local evidence

- Contract: `contracts/claim_graph.py`
- Starting source commit audited: `a5e3cf7`
- Direct Mode baseline: 16 passed
- Repository contract blob: `git hash-object contracts/claim_graph.py` at source commit `8c984a48af1d79f534c5beb1b887313716f367b8`
- Deployed source: submitted inline by `genlayer deploy`; source parity is asserted by the CLI deployment input and unchanged source commit. A separate code-retrieval hash is not exposed by the current CLI workflow.

## Live runtime evidence

- Create graph: `0xe38e5f8743ff2cbc440b4bf0aa20dffe69bd7ea726a9400d49bafcfd11b3b67e` → graph `1`, `ACTIVE`
- Register claim A: `0xbd488dce90a07d1a2b5b5379ea997a14b2d002db2f6a771e5b5350350559578b` → claim `1`, `ACTIVE`
- Register claim B: `0xcf44bc2b9fbb480d821f251e52fced5c4e3a312bc036013ec38b6c9ecd93a270` → claim `2`, `ACTIVE`
- Open relation: `0x118767c4fe348e3335db5d8acad02ccf6ee49d911a83baec38e895f114592eb6` → proposal `1`, `OPEN`
- Resolve relation: `0x6bab0d13456002a6464d2c1b74c024d3878041c9fea4961024385cd0a6d87c54` → `RESOLVED`, `EQUIVALENT`, `MAJORITY_AGREE`
- Pre-withdrawal views: `relation_between=EQUIVALENT`, `is_relation_usable=true`, `can_coexist=true`
- Withdraw claim B: `0x1e148fdf06e19bec489523ca62f4e31f59f595fcb595e4b1f064569fc7d1d293` → claim `2`, `WITHDRAWN`
- Post-withdrawal views: historical `relation_between=EQUIVALENT`; `is_relation_usable=false`; `can_coexist=false`

When a canonical deployment is made, record the exact source commit, public contract address, deployment transaction, lifecycle/finality wording, consensus result, and fresh safe/negative runtime transactions here. Do not reuse old runtime evidence after changing the contract source.
