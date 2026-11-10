import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from config import settings


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Keep the test result on the item so fixtures can see if it failed."""
    outcome = yield
    report = outcome.get_result()
    setattr(item, "rep_" + report.when, report)


@pytest.fixture
def driver(request):
    options = Options()
    if settings.HEADLESS:
        options.add_argument("--headless=new")
    if settings.NO_SANDBOX:
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    # keep Chrome's password manager popups out of the way
    options.add_experimental_option(
        "prefs",
        {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
        },
    )

    browser = webdriver.Chrome(options=options)
    yield browser

    failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed
    if failed:
        os.makedirs("screenshots", exist_ok=True)
        browser.save_screenshot(f"screenshots/{request.node.name}.png")
    browser.quit()
