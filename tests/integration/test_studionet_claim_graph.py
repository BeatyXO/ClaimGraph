import os

import pytest


pytestmark = pytest.mark.integration


@pytest.mark.skipif(
    os.environ.get("CLAIMGRAPH_STUDIONET_LIVE") != "1",
    reason="set CLAIMGRAPH_STUDIONET_LIVE=1 with an authenticated StudioNet environment",
)
def test_live_suite_requires_explicit_authenticated_environment():
    """Live scenarios are gated so they never silently use mocked consensus."""
    pytest.fail("Configure the official StudioNet/gltest fixture before running live integration tests")
