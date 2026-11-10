import os

# Everything is overridable through environment variables so the same
# tests can run locally, in CI, or against a mock server.
UI_BASE_URL = os.getenv("UI_BASE_URL", "https://www.saucedemo.com")
API_BASE_URL = os.getenv("API_BASE_URL", "https://reqres.in/api")
REQRES_API_KEY = os.getenv("REQRES_API_KEY", "")

HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
NO_SANDBOX = os.getenv("NO_SANDBOX", "false").lower() == "true"
EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", "10"))
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "15"))

VALID_PASSWORD = "secret_sauce"
STANDARD_USER = "standard_user"
LOCKED_USER = "locked_out_user"
