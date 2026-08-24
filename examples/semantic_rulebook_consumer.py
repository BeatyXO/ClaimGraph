# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *


@gl.contract_interface
class IClaimGraph:
    class View:
        def can_coexist(self, graph_id: u256, claim_x: u256, claim_y: u256) -> bool:
            pass

        def relation_between(self, graph_id: u256, claim_x: u256, claim_y: u256) -> str:
            pass

    class Write:
        pass


class SemanticRulebookConsumer(gl.Contract):
    claim_graph: Address
    graph_id: u256
    protected_claim: u256
    adopted_claim: u256
    adopted_relation: str

    def __init__(self, claim_graph: Address, graph_id: u256, protected_claim: u256) -> None:
        self.claim_graph = claim_graph if isinstance(claim_graph, Address) else Address(claim_graph)
        self.graph_id = graph_id
        self.protected_claim = protected_claim
        self.adopted_claim = u256(0)
        self.adopted_relation = "NONE"

    @gl.public.write
    def adopt_compatible_claim(self, candidate_claim: u256) -> None:
        graph = IClaimGraph(self.claim_graph).view()
        if not graph.can_coexist(self.graph_id, self.protected_claim, candidate_claim):
            raise gl.vm.UserError("EXPECTED: candidate has no resolved compatible relation")
        self.adopted_claim = candidate_claim
        self.adopted_relation = graph.relation_between(
            self.graph_id,
            self.protected_claim,
            candidate_claim,
        )

    @gl.public.view
    def current_adoption(self) -> str:
        return str(self.adopted_claim) + ":" + self.adopted_relation
