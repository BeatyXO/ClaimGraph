# Deployment evidence

## Canonical deployment

The previous canonical deployment is historical because the deactivation-view fix changed contract source. The current canonical deployment is:

- Date: 2026-08-24
- Network: StudioNet
- Source commit: `1b720e1b0fb8f8a02dbd19a50642a5497f02b660`
- Deployment account: fresh local encrypted account; public deployer address `0x6B476BF35C4968F3f1775c0CA2110591b4B5FCBe`
- Contract address: `0xe0E09098A859734A9b75a337FF91376B69EEa3eD`
- Deployment transaction: `0x57e2bf4a773f82da7ed790f821e39f0accf099fb96e99f5cfc4be66bd621c9f4`
- Lifecycle: `ACCEPTED`
- Consensus result: `MAJORITY_AGREE`, one round, 3 agreeing validator votes observed before quorum cancellation of idle validators

The deployment was made from the exact current `contracts/claim_graph.py` at the source commit above. The contract source was not changed after deployment.

## Local evidence

- Contract: `contracts/claim_graph.py`
- Starting source commit audited: `a5e3cf7`
- Direct Mode baseline: 16 passed
- Repository/deployed normalized SHA-256: `fea4dd097474c0774a9985f0f53852b838822d297aba3757d0fc7b48d983df33`
- Retrieval command: `genlayer code 0xe0E09098A859734A9b75a337FF91376B69EEa3eD`
- Normalization: convert CRLF/CR to LF and trim trailing LF only
- Parity: `PASS` — retrieved source equals repository `contracts/claim_graph.py` after that normalization

## Live runtime evidence

- Create graph: `0xe38e5f8743ff2cbc440b4bf0aa20dffe69bd7ea726a9400d49bafcfd11b3b67e` → graph `1`, `ACTIVE`
- Register claim A: `0xbd488dce90a07d1a2b5b5379ea997a14b2d002db2f6a771e5b5350350559578b` → claim `1`, `ACTIVE`
- Register claim B: `0xcf44bc2b9fbb480d821f251e52fced5c4e3a312bc036013ec38b6c9ecd93a270` → claim `2`, `ACTIVE`
- Open relation: `0x118767c4fe348e3335db5d8acad02ccf6ee49d911a83baec38e895f114592eb6` → proposal `1`, `OPEN`
- Resolve relation: `0x6bab0d13456002a6464d2c1b74c024d3878041c9fea4961024385cd0a6d87c54` → `RESOLVED`, `EQUIVALENT`, `MAJORITY_AGREE`
- Pre-withdrawal views: `relation_between=EQUIVALENT`, `is_relation_usable=true`, `can_coexist=true`
- Withdraw claim B: `0x1e148fdf06e19bec489523ca62f4e31f59f595fcb595e4b1f064569fc7d1d293` → claim `2`, `WITHDRAWN`
- Post-withdrawal views: historical `relation_between=EQUIVALENT`; `is_relation_usable=false`; `can_coexist=false`

## Current-source contradiction and consumer evidence

- Contradiction graph: `0xb0905752a7da45c1d57e1baa4402544ea2166ce03d1975f712a2bc497dc26796`
- Contradiction claim A: `0x77ad9c16eed776b4e37c87ce0646beb373f439ec91092c0fecf50f5caa14a4a4`
- Contradiction claim B: `0x1b7820659ae842bf57e1f5a9b509ea59b33d4f9893adb175e40f784f36f676dd`
- Contradiction open: `0xd93a52cb9eb35a34faada1036166a44fc3460b39ba272546e6f906444b6e0d84`
- Contradiction resolution: `0x9a78d14f97f39a2ff1a48826d490e2ea4e572aff14021524f9338ec45fda3154` → `CONTRADICTS`, `conflicts=true`, `can_coexist=false`
- Consumer-compatible graph: `0xc9ecad606e21f5dd87954c673b13fd48b2640d682ca74615f3470187021d9c8d`
- Consumer claim A/B: `0x83ee603bb117623f1530034f2f6756f7ca89ad8c73fb30ecf172e33aed2b4734`, `0x0ad8694c71ef5d61bf98803ad5e0a118c2978d3085b75b5f8b105c8987f660f6`
- Compatible resolution: `0x073377193f5fd717c8ab79595f7b0fd17d619a13add2025bfb8b028d73bdecf5` → `EQUIVALENT`
- Corrected consumer deployment: `0x5b275B22A2aa3e1D9901f405625816f1295F6EC5`, tx `0x8520ab949127482b6bee67280136bcdd625d30eb4853b3eaf055124fbc323c49`
- Consumer positive adoption: `0xe2d332ec9d20070d781bb1e0ee855b959f6a29f327eb354cfadb135de8eebcf7` → `current_adoption=4:EQUIVALENT`
- Corrected negative consumer deployment: `0x7603E40DB532af22E107296bd731Efe04Ef5f5A0`, tx `0xdefa231d5a866f512a0bf24212a1fb44b5f328ac3682d620dfd9f3611c68e0f0`
- Consumer negative adoption: `0xacbd2ab3ebc796c2eedbd2d5e18148d807f51ec8c5cac58c6363d8c4910d4f85` → execution payload `EXPECTED: candidate has no resolved compatible relation`

The committed integration suite is real CLI/RPC coverage, not mocked consensus. With `CLAIMGRAPH_STUDIONET_LIVE=1` and `CLAIMGRAPH_LIVE_CONTRACT=0xe0E09098A859734A9b75a337FF91376B69EEa3eD`, `pytest -q tests/integration -s` collected 3 and passed 3. It verifies the live public surface, graph state, and machine-readable relation enum.

When a canonical deployment is made, record the exact source commit, public contract address, deployment transaction, lifecycle/finality wording, consensus result, and fresh safe/negative runtime transactions here. Do not reuse old runtime evidence after changing the contract source.
