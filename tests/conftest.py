import os
import re

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from config import settings


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Keep the test result on the item so fixtures can see if it failed."""
    outcome = yield
    report = outcome.get_result()
    setattr(item, "rep_" + report.when, report)


def build_chrome():
    options = ChromeOptions()
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
    return webdriver.Chrome(options=options)


def build_firefox():
    options = FirefoxOptions()
    if settings.HEADLESS:
        options.add_argument("-headless")
    options.add_argument("--width=1920")
    options.add_argument("--height=1080")
    options.set_preference("signon.rememberSignons", False)
    return webdriver.Firefox(options=options)


BROWSERS = {"chrome": build_chrome, "firefox": build_firefox}


@pytest.fixture
def driver(request):
    if settings.BROWSER not in BROWSERS:
        raise pytest.UsageError(
            f"BROWSER must be one of {sorted(BROWSERS)}, got '{settings.BROWSER}'"
        )
    browser = BROWSERS[settings.BROWSER]()
    yield browser

    failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed
    if failed:
        os.makedirs("screenshots", exist_ok=True)
        safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", request.node.name)
        browser.save_screenshot(f"screenshots/{settings.BROWSER}_{safe_name}.png")
    browser.quit()
