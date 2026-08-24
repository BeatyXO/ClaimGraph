import json
import pytest

CONTRACT = "contracts/claim_graph.py"
ZERO = "0x0000000000000000000000000000000000000000"


def deploy(direct_deploy, direct_vm):
    contract = direct_deploy(CONTRACT)
    direct_vm.check_pickling = True
    return contract


def create_graph(contract, direct_vm, sender, permissionless=True):
    direct_vm.sender = sender
    return contract.create_graph(
        "Governance rules",
        "Rules governing protocol fee policy for the same network and active policy period.",
        "Interpret claims literally; material numeric limits and explicit conditions control.",
        permissionless,
        ZERO,
    )


def register_pair(contract, direct_vm, sender):
    direct_vm.sender = sender
    a = contract.register_claim(1, "Protocol fees must never exceed 2%.", "Applies to ordinary protocol fees.")
    b = contract.register_claim(1, "Protocol fees may be set to 3.5% for six months.", "Applies to ordinary protocol fees.")
    return a, b


def mock_relation(direct_vm, relation, reason="classified"):
    direct_vm.clear_mocks()
    direct_vm.mock_llm(
        r".*Classify the semantic relationship.*",
        json.dumps({"relation": relation, "reason": reason}),
    )


def test_create_graph_stores_scope_and_rules(direct_deploy, direct_vm, direct_alice):
    contract = deploy(direct_deploy, direct_vm)
    assert create_graph(contract, direct_vm, direct_alice) == 1
    graph = json.loads(contract.graph_of(1))
    assert graph["status"] == "ACTIVE"
    assert graph["permissionless"] is True
    assert "fee policy" in graph["scope"]


@pytest.mark.parametrize("name,scope,rules", [
    ("", "scope", "rules"),
    ("name", "", "rules"),
    ("name", "scope", ""),
])
def test_create_graph_rejects_empty_core_fields(direct_deploy, direct_vm, direct_alice, name, scope, rules):
    contract = deploy(direct_deploy, direct_vm)
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("EXPECTED"):
        contract.create_graph(name, scope, rules, True, ZERO)


def test_managed_graph_rejects_non_creator_claims(direct_deploy, direct_vm, direct_alice, direct_bob):
    contract = deploy(direct_deploy, direct_vm)
    create_graph(contract, direct_vm, direct_alice, permissionless=False)
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("EXPECTED"):
        contract.register_claim(1, "A claim", "")


def test_register_claim_records_graph_membership(direct_deploy, direct_vm, direct_alice):
    contract = deploy(direct_deploy, direct_vm)
    create_graph(contract, direct_vm, direct_alice)
    direct_vm.sender = direct_alice
    claim_id = contract.register_claim(1, "A claim", "context")
    claim = json.loads(contract.claim_of(claim_id))
    assert claim["graph_id"] == "1"
    assert claim["status"] == "ACTIVE"


def test_open_relation_canonicalizes_pair(direct_deploy, direct_vm, direct_alice):
    contract = deploy(direct_deploy, direct_vm)
    create_graph(contract, direct_vm, direct_alice)
    a, b = register_pair(contract, direct_vm, direct_alice)
    proposal_id = contract.open_relation(1, b, a)
    proposal = json.loads(contract.proposal_of(proposal_id))
    assert proposal["claim_a"] == str(a)
    assert proposal["claim_b"] == str(b)


def test_same_pair_cannot_be_opened_twice(direct_deploy, direct_vm, direct_alice):
    contract = deploy(direct_deploy, direct_vm)
    create_graph(contract, direct_vm, direct_alice)
    a, b = register_pair(contract, direct_vm, direct_alice)
    contract.open_relation(1, a, b)
    with direct_vm.expect_revert("EXPECTED"):
        contract.open_relation(1, b, a)


def test_contradiction_becomes_persistent_blocking_edge(direct_deploy, direct_vm, direct_alice):
    contract = deploy(direct_deploy, direct_vm)
    create_graph(contract, direct_vm, direct_alice)
    a, b = register_pair(contract, direct_vm, direct_alice)
    proposal = contract.open_relation(1, a, b)
    mock_relation(direct_vm, "CONTRADICTS")
    contract.resolve_relation(proposal)
    assert contract.relation_between(1, a, b) == "CONTRADICTS"
    assert contract.conflicts(1, a, b) is True
    assert contract.can_coexist(1, a, b) is False
    assert json.loads(contract.proposal_of(proposal))["status"] == "RESOLVED"


def test_directional_relation_is_inverted_for_reverse_query(direct_deploy, direct_vm, direct_alice):
    contract = deploy(direct_deploy, direct_vm)
    create_graph(contract, direct_vm, direct_alice)
    direct_vm.sender = direct_alice
    a = contract.register_claim(1, "All validator votes are recorded.", "")
    b = contract.register_claim(1, "Some validator votes are recorded.", "")
    proposal = contract.open_relation(1, a, b)
    mock_relation(direct_vm, "A_ENTAILS_B")
    contract.resolve_relation(proposal)
    assert contract.relation_between(1, a, b) == "A_ENTAILS_B"
    assert contract.relation_between(1, b, a) == "B_ENTAILS_A"


def test_malformed_model_output_fails_closed_as_inconclusive(direct_deploy, direct_vm, direct_alice):
    contract = deploy(direct_deploy, direct_vm)
    create_graph(contract, direct_vm, direct_alice)
    a, b = register_pair(contract, direct_vm, direct_alice)
    proposal = contract.open_relation(1, a, b)
    direct_vm.clear_mocks()
    direct_vm.mock_llm(r".*Classify the semantic relationship.*", "not-json")
    contract.resolve_relation(proposal)
    resolved = json.loads(contract.proposal_of(proposal))
    assert resolved["status"] == "INCONCLUSIVE"
    assert contract.can_coexist(1, a, b) is False


def test_inconclusive_relation_is_retryable(direct_deploy, direct_vm, direct_alice):
    contract = deploy(direct_deploy, direct_vm)
    create_graph(contract, direct_vm, direct_alice)
    a, b = register_pair(contract, direct_vm, direct_alice)
    proposal = contract.open_relation(1, a, b)
    mock_relation(direct_vm, "INCONCLUSIVE")
    contract.resolve_relation(proposal)
    contract.retry_inconclusive(proposal)
    assert json.loads(contract.proposal_of(proposal))["status"] == "OPEN"


def test_withdrawn_claim_cannot_enter_new_relation(direct_deploy, direct_vm, direct_alice):
    contract = deploy(direct_deploy, direct_vm)
    create_graph(contract, direct_vm, direct_alice)
    a, b = register_pair(contract, direct_vm, direct_alice)
    contract.withdraw_claim(a)
    with direct_vm.expect_revert("EXPECTED"):
        contract.open_relation(1, a, b)


def test_unknown_pair_fails_closed(direct_deploy, direct_vm, direct_alice):
    contract = deploy(direct_deploy, direct_vm)
    create_graph(contract, direct_vm, direct_alice)
    a, b = register_pair(contract, direct_vm, direct_alice)
    assert contract.relation_between(1, a, b) == "NONE"
    assert contract.has_resolved_relation(1, a, b) is False
    assert contract.can_coexist(1, a, b) is False


def test_deactivated_graph_blocks_new_claims(direct_deploy, direct_vm, direct_alice):
    contract = deploy(direct_deploy, direct_vm)
    create_graph(contract, direct_vm, direct_alice)
    contract.deactivate_graph(1)
    with direct_vm.expect_revert("EXPECTED"):
        contract.register_claim(1, "new claim", "")


def test_stats_track_resolved_edges(direct_deploy, direct_vm, direct_alice):
    contract = deploy(direct_deploy, direct_vm)
    create_graph(contract, direct_vm, direct_alice)
    a, b = register_pair(contract, direct_vm, direct_alice)
    proposal = contract.open_relation(1, a, b)
    mock_relation(direct_vm, "INDEPENDENT")
    contract.resolve_relation(proposal)
    stats = json.loads(contract.stats())
    assert stats["total_graphs"] == "1"
    assert stats["total_claims"] == "2"
    assert stats["total_edges"] == "1"
