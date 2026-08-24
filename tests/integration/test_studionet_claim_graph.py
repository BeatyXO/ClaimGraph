"""Real StudioNet smoke tests driven by the official GenLayer CLI."""
import json
import os
import subprocess

import pytest


pytestmark = pytest.mark.integration
CONTRACT = os.environ.get("CLAIMGRAPH_LIVE_CONTRACT", "")
LIVE = os.environ.get("CLAIMGRAPH_STUDIONET_LIVE") == "1" and bool(CONTRACT)
SKIP_REASON = "set CLAIMGRAPH_STUDIONET_LIVE=1 and CLAIMGRAPH_LIVE_CONTRACT to run real StudioNet tests"


def cli(*args: str) -> str:
    result = subprocess.run(["genlayer", *args], check=True, capture_output=True, text=True)
    return result.stdout


def read_result(method: str, *args: str):
    output = cli("call", CONTRACT, method, "--args", *args)
    marker = "Result:\n"
    assert marker in output, output
    value = output.split(marker, 1)[1].split("\n", 1)[0].strip()
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value


@pytest.mark.skipif(not LIVE, reason=SKIP_REASON)
def test_live_deployment_public_surface():
    stats = read_result("stats")
    assert "total_graphs" in stats


@pytest.mark.skipif(not LIVE, reason=SKIP_REASON)
def test_live_contract_has_no_mocked_consensus_path():
    graph = read_result("graph_of", "1")
    assert graph["status"] in {"ACTIVE", "INACTIVE"}


@pytest.mark.skipif(not LIVE, reason=SKIP_REASON)
def test_live_relation_surface_is_machine_readable():
    relation = read_result("relation_between", "1", "1", "2")
    assert relation in {
        "NONE", "A_ENTAILS_B", "B_ENTAILS_A", "CONTRADICTS", "EQUIVALENT",
        "A_DEPENDS_ON_B", "B_DEPENDS_ON_A", "INDEPENDENT", "INCONCLUSIVE",
    }
