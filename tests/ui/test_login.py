import pytest

from config import settings
from pages.inventory_page import InventoryPage

pytestmark = pytest.mark.ui


@pytest.mark.smoke
def test_valid_login_lands_on_inventory(driver, login_page):
    login_page.login(settings.STANDARD_USER, settings.VALID_PASSWORD)
    assert InventoryPage(driver).is_loaded()


def test_locked_out_user_is_rejected(login_page):
    login_page.login(settings.LOCKED_USER, settings.VALID_PASSWORD)
    assert "locked out" in login_page.error_message()


def test_wrong_password_shows_error(login_page):
    login_page.login(settings.STANDARD_USER, "wrong_password")
    assert "do not match" in login_page.error_message()


def test_problem_user_can_log_in(driver, login_page):
    login_page.login("problem_user", settings.VALID_PASSWORD)
    assert InventoryPage(driver).is_loaded()


@pytest.mark.parametrize(
    "username,password",
    [
        ("invalid_user", settings.VALID_PASSWORD),
        ("STANDARD_USER", settings.VALID_PASSWORD),
        (settings.STANDARD_USER, "SECRET_SAUCE"),
        ("invalid_user", "wrong_password"),
    ],
)
def test_invalid_credential_matrix(login_page, username, password):
    login_page.login(username, password)
    assert "do not match" in login_page.error_message()


def test_empty_username_shows_required_error(login_page):
    login_page.login("", settings.VALID_PASSWORD)
    assert "Username is required" in login_page.error_message()


def test_empty_password_shows_required_error(login_page):
    login_page.login(settings.STANDARD_USER, "")
    assert "Password is required" in login_page.error_message()


def test_logout_returns_to_login(inventory, login_page):
    inventory.logout()
    assert login_page.is_displayed()
