import pytest

from utils.api_client import ReqResClient


@pytest.fixture(scope="session")
def api():
    # The classic ReqRes demo endpoints work without a key (daily limit applies).
    # If REQRES_API_KEY is set, the client sends it as the x-api-key header.
    return ReqResClient()
