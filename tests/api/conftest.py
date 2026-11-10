import pytest

from config import settings
from utils.api_client import ReqResClient


@pytest.fixture(scope="session")
def api():
    # ReqRes asks for a free API key (x-api-key header). Without one the live
    # service rejects most calls, so skip instead of reporting false failures.
    if "reqres.in" in settings.API_BASE_URL and not settings.REQRES_API_KEY:
        pytest.skip("Set REQRES_API_KEY to run API tests against reqres.in")
    return ReqResClient()
